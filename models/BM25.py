from models.utils import *
from models.model import myModel

class BM25(myModel):

    def __init__(self, data="msmarco-passage", prebuilt=True):
        self.name = "BM25_Pyserini"
        self.data = data
        self.prebuilt = prebuilt
        if(self.prebuilt):
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
        else:
            self.searcher = SimpleSearcher(self.data)

    def get_scorces_query(self, id,query,k):
        hits = self.searcher.search(query, k)
        out = dict()
        for hit in hits:
          out[hit.docid] = hit.score
        return out

    