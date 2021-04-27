
from models.utils import *
from models.model import myModel
import os
from sentence_transformers import SentenceTransformer
import torch
import ngtpy


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
        self.index = None
        self.searcher = SimpleSearcher.from_prebuilt_index("msmarco-passage")
        self.mapping = dict()
        for i in range(self.searcher.num_docs):
            self.mapping[i] = self.searcher.doc(i).docid()

            
    #must have a fast GPU and a big RAM storage
    def generate_embeddings(self,folder,batch_size=1000000):
        print("Warning : heavy operation , must have fast GPU and sufficent RAM storage...")
        
        j = 1
        batch_emb = []
        for i in range(self.searcher.num_docs):
            chaine=self.searcher.doc(i).raw()
            chaine=json.loads(chaine)['contents']
            batch_emb.append(chaine)
            if (i+1) % batch_size == 0:
                print("encoding batch : ",j)
                emb = self.model.encode(batch_emb)
                np.save(folder+"/msmarco-passage"+str(j)+".npy", emb)
                print(i+1," documens done.")
                emb = None
                j+=1
                batch_emb = []
        emb = self.model.encode(batch_emb)
        np.save(folder+"/msmarco-passage"+str(j)+".npy", emb)
    
    #must respect the generation conditions
    def generate_index(self,folder,index_path):
        n = len(os.listdir("file"))
        ngtpy.create(index_path, 768, distance_type='Cosine')
        index = ngtpy.Index(index_path)
        j=0
        for i in range(n):
            liste = np.load(folder+"/msmarco-passage"+str(i)+".npy",mmap_mode='r')
            for l in liste:
                l = list(map(float,list(l)))
                index.insert(l) # insert objects
                j+=1
                if j % 100000 == 0:
                    print(str(j)+" element indexted")
            liste = None
        print('building objects...')
        index.build_index()
        print('saving the index...')
        index.save()    
        
        
    def load_index(self,index_path):
        self.index = ngtpy.Index(index_path)
        
    def from_prebuilt_index():
        pass
            
    def get_scorces_query(self, id,query,k):
        out = dict()
        emb = self.model.encode(query)
        hits = self.index.search(emb,k,0.01)
        for hit in hits:
            out[self.mapping[hit[0]]] = 1-hit[1]

        return out
