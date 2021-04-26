
from pyserini.search import SimpleSearcher
from pyserini.search import get_topics

import json
from math import *
import numpy as np
import re
import unicodedata
import string

import fasttext
import fasttext.util

from gensim.models import Word2Vec


import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
nltk.download('stopwords')
nltk.download('punkt')

import pytrec_eval










def prepareText(data,lower=True,punc=True,chiffres=True,stemming=True,stopword=True,lang='english'):

    stop_words = set(stopwords.words(lang))
    stemmer = SnowballStemmer(language=lang)

    toChange = data

    if punc == True:
        p = string.punctuation 
        p += '\n\r\t'
        toChange = toChange.translate(str.maketrans(p, ' ' * len(p)))  
        
    if chiffres == True:
        toChange = re.sub('[0-9]+', '', toChange)

    if stemming == True:
        toChange = word_tokenize(toChange)
        toChange = " ".join(stemmer.stem(x) for x in toChange)

    if stopword == True:
        toChange = word_tokenize(toChange)
        toChange = " ".join(x for x in toChange if not x in stop_words)
        
                
    if lower == True:
        toChange = unicodedata.normalize('NFD', toChange).encode('ascii', 'ignore').decode("utf-8")
        toChange = toChange.lower()

    return toChange





def cosine_similarity(x,y):
        return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    
    
def trec_eval(qrels,run,metrics=["map","ndcg","P_10","Rprec","recip_rank"]):

    with open(qrels, 'r') as f_qrel:
        qrel = pytrec_eval.parse_qrel(f_qrel)

    with open(run, 'r') as f_run:
        run = pytrec_eval.parse_run(f_run)

    evaluator = pytrec_eval.RelevanceEvaluator(qrel, metrics)
    results = evaluator.evaluate(run)



    out = dict()
    for metric in metrics:
        value = pytrec_eval.compute_aggregated_measure(metric, [query_measures[metric] for query_measures in results.values()])
        print('{:25s}{:8s}{:.4f}'.format(metric, 'all', value))
        out[metric] = value
        
    return out



def combine_BM25(fileSave, firstResults, secondResults, alpha, modelName):
    
    with open(firstResults, 'r') as fst:
        runfst = pytrec_eval.parse_run(fst)
    
    with open(secondResults, 'r') as sec:
        runsec = pytrec_eval.parse_run(sec)

    with open(fileSave, 'w') as runfile:
        allqueries = list(set().union(list(runfst.keys()), list(runsec.keys())))

        for query in allqueries:

            docs1 = list(runfst.get(query,dict()).keys())
            docs2 = list(runsec.get(query,dict()).keys())
            hits = dict()
            for document in list(set().union(docs1,docs2)):
                hits[document] = runsec.get(query,dict()).get(document,0) * alpha + runfst.get(query,dict()).get(document,0) * (1-alpha)
            sor = sorted(hits.items(),reverse = True, key=lambda x: x[1])
            hits = dict(sor)

            for doc,score in hits.items():
                _ = runfile.write('{} Q0 {} {} {:.6f} {}\n'.format(query, doc, i+1, score,modelName))