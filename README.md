# RI models
Some models that we used on MS-MARCO Passage ranking task.

# Results :
Validation Results on 2019 TREC 200 queries

BM25 Pyserini | Expension | FastText | Word2Vec | DistilBERT | MRR | NDCG@1000 | NDCG@10 | MAP
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
x |  |  |  |  | 0.8245 | 0.6067 | 0.5058 | 0.3773
x |  | x |  |  | 0.8593 | 0.6107 | 0.5188 | 0.3804
x |  |  | x |  | 0.8717 | 0.6116 | 0.5217 | 0.3787
 |  |  |  | x | 0.9302 | 0.6239 | 0.6577 | 0.3737
x |  |  |  | x | 0.9537 | 0.6963 | 0.6685 | 0.4518
x | x | x | x | x | x | x | x
