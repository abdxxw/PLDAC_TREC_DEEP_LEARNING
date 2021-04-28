# RI models
Some models that we used on MS-MARCO Passage ranking task.

# Results :
Validation Results on 2019 TREC 200 queries

BM25 Pyserini | Expension | FastText | DistilBERT | MRR | NDCG@1000 | NDCG@10 | MAP
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
x |  |  |  | 0.8245 | 0.6067 | 0.5058 | 0.3773
x |  | x |  | 0.8593 | 0.6107 | 0.5188 | 0.3804
x | x | x | x | x | x | x | x
