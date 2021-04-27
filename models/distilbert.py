
from models.utils import *
from models.model import myModel
import os
from sentence_transformers import SentenceTransformer

class DistilBert(myModel):

    def __init__(self):
        if torch.cuda.is_available():       
            device = torch.device("cuda")
            print(f'There are {torch.cuda.device_count()} GPU(s) available.')
            print('Device name:', torch.cuda.get_device_name(0))
        
        else:
            print('No GPU available, using the CPU instead.')
            device = torch.device("cpu")
            
        self.name = 'DistilBert'
        self.model = SentenceTransformer('msmarco-distilbert-base-v3')
        self.model = self.model.to(device)

            
    #must have a fast GPU and a big RAM storage
    def generate_embeddings(self,folder,batch_size=1000000):
        print("Warning : heavy operation , must have fast GPU and sufficent RAM storage...")
        searcher = SimpleSearcher.from_prebuilt_index("msmarco-passage")
        j = 1
        batch_emb = []
        for i in range(searcher.num_docs):
            if i+1 % batch_size == 0:
                print(i," documens done.")
                emb = self.model.encode(batch_emb)
                np.save(folder+"/msmarco-passage"+str(j)+".npy", emb)
                emb = None
                j+=1
                batch_emb = []
            chaine=searcherPassages.doc(i).raw()
            chaine=json.loads(chaine)['contents']
            batch_emb.append(chaine)
                
                
                
    def get_scorces_query(self, id,query,k):
        oldrun = run_parser(self.firststage)
        q_results = oldrun.get(id,dict())
        out = dict()
        
        for key,score in q_results.items():

            query = prepareText(query)

            chaine=self.searcher.doc(key).raw()
            chaine=json.loads(chaine)['contents']
            chaine = prepareText(chaine)

            out[key] = cosine_similarity(self.model.get_sentence_vector(query),self.model.get_sentence_vector(chaine))

        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)
