import os
import sys
import pickle

from executors import MoleculeEncoder, Indexer

from jina.types.document.graph import GraphDocument
from jina import Flow, DocumentArray

cur_dir = os.path.dirname(os.path.abspath(__file__))


def create_docs(dataset):
    docs = []
    for molecule_str, dgl_graph, label, mask in dataset:
        tags={'molecule_str': molecule_str,
              'agg_features': dgl_graph.ndata['h'].detach().numpy().tolist(),
              'label': label.detach().numpy().tolist(),
              'mask': mask.detach().numpy().tolist()}
        gdoc = GraphDocument.load_from_dgl_graph(dgl_graph)
        gdoc.tags = tags
        docs.append(gdoc)
        
    return DocumentArray(docs)

def load_dataset():
    from dgllife.data import Tox21
    from dgllife.utils import smiles_to_bigraph, CanonicalAtomFeaturizer

    dataset = Tox21(smiles_to_bigraph, CanonicalAtomFeaturizer())
    return dataset


def print_indices(response):
    for doc in response.docs:
        print(f"\n\n\nmolecule_str_query={doc.tags['molecule_str']}")
        for match in doc.matches:
            print(f"molecule_str={match.tags['molecule_str']}, score={match.score}")


if __name__ == '__main__':
    n_queries = 3

    if sys.argv[1] == 'index':
        print('indexing started')
        dataset = load_dataset()
        documents = create_docs(dataset)

        for i in range(n_queries):
            with open(f'./query_{i}.pkl', 'wb') as file:
                pickle.dump(documents[i], file)

        f = Flow().add(uses=MoleculeEncoder).add(uses=Indexer)
        with f:
            print('flow posted')
            f.post('/index',
                   inputs=documents)

    elif sys.argv[1] == 'search':
        
        dataset = load_dataset()
        queries = create_docs([dataset[i] for i in range(n_queries)])
        
        f = Flow().add(uses=MoleculeEncoder).add(uses=Indexer)
        with f:
            f.post('/search',
                   inputs=queries,
                   parameters={'top_k': 4, 'distance': 'euclidean'},
                   on_done=print_indices)
    else:
        raise NotImplementedError(f'unsupported mode {sys.argv[1]}')