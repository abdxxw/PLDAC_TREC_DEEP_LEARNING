
from models.utils import *
from models.model import myModel
from sentence_transformers import CrossEncoder

class Reranker(myModel):

    # exemples of models
    # Electra= 'cross-encoder/ms-marco-electra-base'
    # TinyBert ='cross-encoder/ms-marco-TinyBERT-L-6'
    # miniLM = 'cross-encoder/ms-marco-MiniLM-L-12-v2'
    
    def __init__(self, file,searcher,model="cross-encoder/ms-marco-MiniLM-L-12-v2",name="MiniLM"):
        self.name = name
        self.firststage = file
        self.oldrun = run_parser(file)
        self.model = CrossEncoder(model)
        self.searcher = searcher

    def set_firststage(self,file):
        self.firststage = file
        self.oldrun = run_parser(file)

    def get_scorces_query(self, id,query,k):
        q_results = self.oldrun.get(id,dict())
        tmp = []
        
        for key,score in q_results.items():
    
            chaine=self.searcher.doc(key).raw()
            chaine=json.loads(chaine)['contents']
    
            tmp.append((query,chaine))
        scores = self.model.predict(tmp)
        out = dict()
        for i,key in enumerate(q_results.keys()):
          out[key] = scores[i]
        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)