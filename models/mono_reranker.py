from pygaggle.rerank.base import Query, Text
from pygaggle.rerank.transformer import MonoT5,MonoBERT
from models.utils import *
from models.model import myModel

      
class Reranker(myModel):
    
    def __init__(self, file,searcher,name="monoT5"):
        self.name = name
        self.firststage = file
        self.oldrun = run_parser(file)
        self.searcher = searcher
        if(name=="monoT5"):
          self.model = MonoT5()
        if(name=="monobert"):
          self.model = MonoBERT()

    def set_firststage(self,file):
        self.firststage = file
        self.oldrun = run_parser(file)

    def get_scorces_query(self,id,query,k):
        q_results = self.oldrun.get(id,dict())
        tmp = []
        query = Query(query)
        for key,score in q_results.items():
            chaine=self.searcher.doc(key).raw()
            chaine=json.loads(chaine)['contents']
            tmp.append(Text(chaine, {'docid': key}, 0))
            
        reranked = self.model.rerank(query, tmp)
        out = dict()
        for i,key in enumerate(q_results.keys()):
          out[reranked[i].metadata["docid"]] = reranked[i].score
        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)