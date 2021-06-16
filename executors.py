import numpy as np
import dgl
import torch
import os
from typing import Tuple

from jina.types.document.graph import GraphDocument
from jina import DocumentArray, Document, Executor, requests
from utils import cosine_vectorized, euclidean_vectorized

cur_dir = os.path.dirname(os.path.abspath(__file__))

class MoleculeEncoder(Executor):
    
    def __init__(self, model_type: str='GCN_Tox21', *args, **kwargs):

        super().__init__(*args, **kwargs)
        from dgllife.model import load_pretrained
        self.model = load_pretrained(model_type)
        self.model.eval()

    @requests()
    def encode(self, docs: DocumentArray, *args, **kwargs):
        for d in docs:
            dgraph = GraphDocument(d)
            dgl_graph = dgraph.to_dgl_graph()
            dgl_graph = dgl.add_self_loop(dgl_graph)
            torch_features = torch.tensor(d.tags['agg_features'])
            d.embedding = self.model.forward(dgl_graph, feats=torch_features).detach().numpy().flatten()


class Indexer(Executor):

    def __init__(self, index_folder=f'{cur_dir}/workspace/', *args, **kwargs):
        self.index_folder = index_folder
        self.index_path = os.path.join(self.index_folder, 'docs.json')
        self._embedding_matrix = None

        if os.path.exists(self.index_path):
            self._docs = DocumentArray.load(self.index_path)
            self._embedding_matrix = np.stack(self._docs.get_attributes('embedding')) 

        else:
            self._docs = DocumentArray()

    @requests(on='/index')
    def index(self, docs: DocumentArray, *args, **kwargs):
        self._docs.extend(docs)

    @requests(on='/search')
    def search(self, docs: DocumentArray, parameters, **kwargs):
        top_k = int(parameters['top_k'])
        distance = parameters['distance']
        
        for query in docs:
            q_emb = np.array([query.get_attributes('embedding')])

            if distance == 'cosine':
                dist_query_to_emb = cosine_vectorized(q_emb, self._embedding_matrix)
            if distance == 'euclidean':
                dist_query_to_emb = euclidean_vectorized(q_emb, self._embedding_matrix)

            idx, dist_query_to_emb = self._get_sorted_top_k(dist_query_to_emb, top_k)

            for id, dist in zip(idx, dist_query_to_emb):
                match = Document(self._docs[int(id)], score=dist)
                query.matches.append(match)

    @staticmethod
    def _get_sorted_top_k(dist: 'np.array', top_k: int) -> Tuple['np.ndarray', 'np.ndarray']:
        """Find top-k smallest distances in ascending order.

        Idea is to use partial sort to retrieve top-k smallest distances unsorted and then sort these
        in ascending order. Equivalent to full sort but faster for n >> k. If k >= n revert to full sort.
        """
        if top_k >= dist.shape[1]:
            idx = dist.argsort(axis=1)[:, :top_k]
            dist = np.take_along_axis(dist, idx, axis=1)
        else:
            idx_ps = dist.argpartition(kth=top_k, axis=1)[:, :top_k]
            dist = np.take_along_axis(dist, idx_ps, axis=1)
            idx_fs = dist.argsort(axis=1)
            idx = np.take_along_axis(idx_ps, idx_fs, axis=1)
            dist = np.take_along_axis(dist, idx_fs, axis=1)

        return idx.flatten(), dist.flatten()

    def close(self):
        os.makedirs(self.index_folder, exist_ok = True)
        self._docs.save(self.index_path)

