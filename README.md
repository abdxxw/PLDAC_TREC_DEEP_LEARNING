# RI models
Some models that we used on MS-MARCO Passage ranking task.


# Our CARP6 model : 

![alt text](https://i.ibb.co/HNm24wx/all.png)


# Term Expension : 

![alt text](https://i.ibb.co/hVMQ3Bw/exp.png)


# Embedding Index : 

![alt text](https://i.ibb.co/2sDsVyW/emb.png)

# Results :
Validation Results on 2019 TREC 200 queries

BM25 Pyserini | Passage Expension | DistilBERT (First Stage) | FastText Reranking | Word2Vec Reranking | MRR | NDCG@1000 | NDCG@10 | MAP
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
| x |  |  |  |  | 0.8245 | 0.6067 | 0.5058 | 0.3773
| x |  |  | x |  | 0.8593 | 0.6107 | 0.5188 | 0.3804
| x |  |  |  | x | 0.8717 | 0.6116 | 0.5217 | 0.3787
|  |  | x |  |  | 0.9302 | 0.6239 | 0.6577 | 0.3737
| x | x |  |  |  | 0.8884 | 0.6929 | 0.6417 | 0.4625
| x |  | x |  |  | 0.9537 | 0.6963 | 0.6685 | 0.4518
| x | x | x |  |  | 0.9364 | 0.7338 | 0.7151 | 0.5253


Validation Results on MSMARCO dev dataset 6980 queries

Model | MRR | NDCG@1000 | NDCG@10 | MAP
------------ |------------ | ------------- | ------------- | ------------- 
| BM25 | 0.1960 | 0.3116 | 0.2284 | 0.1926
| BM25 Expension | 0.2848 | 0.4099 | 0.3329 | 0.2805
| DistilBERT | 0.3303 | 0.4411 | 0.3747 | 0.3250
| BM25 EXP + DistilBERT | 0.3575 | 0.4757 | 0.4096 | 0.3524
| miniLM reranking | 0.4167 | 0.5273 | 0.4713 | 0.4107
| tinyBERT reranking | 0.3428 | 0.4633 | 0.3941 | 0.3381
| ELECTRA reranking | 0.3861 | 0.5019 | 0.4417 | 0.3802

