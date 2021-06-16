# example-molecule-search
Example showcasing  the `GraphDocument` type for molecule search.



#### Installing dependencies

This package uses `rdkit` which is not pip installable. Hence you are highly encouraged to install it with conda using `conda_requiremnts.txt`. It is encouraged to do the following process in a conda environment which can be done with `conda create --name molecule_env conda`.

```bash
conda install --file conda_requirements.txt
```

The other packages that are required are pip installable and can be installed from `requirements.txt`

```
pip install -r requirements.txt
```



#### Running the application

To download the data and generate the embeddings for all the examples run:

```bash
python app.py index
```

This will create a `worspace` folder containing the indexed molecules in a `docs.json` file.

Once this finishes, to look at the search results for three examples run

```bash
python app.py search
```

This will present you with three queries and the top 4 closest molecules

```
molecule_str_query=CCOc1ccc2nc(S(N)(=O)=O)sc2c1
molecule_str=CCOc1ccc2nc(S(N)(=O)=O)sc2c1, score={'ref_id': 'd62522b2-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=CC(C)(C)OC(=O)c1ncn2c1[C@@H]1CCCN1C(=O)c1c(Br)cccc1-2, score={'value': 1.3071945, 'ref_id': 'd62522b2-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=c1ccc2sc(SN3CCOCC3)nc2c1, score={'value': 1.3963138, 'ref_id': 'd62522b2-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=CCN(CC)CCOc1ccc2nc(N(C)C)sc2c1, score={'value': 1.4383051, 'ref_id': 'd62522b2-cea0-11eb-ba25-787b8ab3f5de'}


molecule_str_query=CCN1C(=O)NC(c2ccccc2)C1=O
molecule_str=CCN1C(=O)NC(c2ccccc2)C1=O, score={'value': 0.00015133241, 'ref_id': 'd626a7ae-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=CCCCN(CCCC)C(C(N)=O)c1ccc(OC)cc1, score={'value': 0.8653555, 'ref_id': 'd626a7ae-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=CC(C)NNC(=O)c1ccncc1, score={'value': 0.9337485, 'ref_id': 'd626a7ae-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=CC(=O)SCc1ccco1, score={'value': 1.1091931, 'ref_id': 'd626a7ae-cea0-11eb-ba25-787b8ab3f5de'}


molecule_str_query=CC[C@]1(O)CC[C@H]2[C@@H]3CCC4=CCCC[C@@H]4[C@H]3CC[C@@]21C
molecule_str=CC[C@]1(O)CC[C@H]2[C@@H]3CCC4=CCCC[C@@H]4[C@H]3CC[C@@]21C, score={'value': 0.0017194913, 'ref_id': 'd627db2e-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=C=CC[C@]1(O)CC[C@H]2[C@@H]3CCC4=CCCC[C@@H]4[C@H]3CC[C@@]21C, score={'value': 2.2092874, 'ref_id': 'd627db2e-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=C[C@@]12CCC[C@H]1[C@@H]1CC[C@H]3C[C@@H](O)CC[C@]3(C)[C@H]1CC2, score={'value': 2.9367318, 'ref_id': 'd627db2e-cea0-11eb-ba25-787b8ab3f5de'}
molecule_str=C[C@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@@]21C, score={'value': 3.1421533, 'ref_id': 'd627db2e-cea0-11eb-ba25-787b8ab3f5de'}
```

