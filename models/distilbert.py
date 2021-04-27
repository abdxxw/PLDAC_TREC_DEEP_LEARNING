
from models.utils import *
from models.model import myModel
import os
from sentence_transformers import SentenceTransformer
import torch
import ngtpy
import gdown



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

            
    #must have a fast GPU and a big RAM storage
    def generate_embeddings(self,batch_size=1000000):
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
                np.save("pieces/msmarco-passage"+str(j)+".npy", emb)
                print(i+1," documens done.")
                emb = None
                j+=1
                batch_emb = []
        emb = self.model.encode(batch_emb)
        np.save(folder+"/msmarco-passage"+str(j)+".npy", emb)
    
    #must respect the generation conditions
    def generate_index(self,index_path):
        n = len(os.listdir("file"))
        ngtpy.create(index_path, 768, distance_type='Cosine')
        index = ngtpy.Index(index_path)
        j=0
        for i in range(n):
            liste = np.load("pieces/msmarco-passage"+str(i)+".npy",mmap_mode='r')
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
        
        
    def load_index(self,index_path="indexes/emb"):
        self.index = ngtpy.Index(index_path)
        
    def from_prebuilt_index(self):
        grp = 'https://drive.google.com/uc?id=1-9s3OtgVzO46Fxy9ZUHS5wajKA-Z27iZ'
        grp_out = 'indexes/emb/grp'
        
        obj = 'https://drive.google.com/uc?id=1-H0mwdF37FO-iIeNfjwtTeseN_1Tc7nT'
        obj_out = 'indexes/emb/obj'
        
        prf = 'https://drive.google.com/uc?id=1-3HNZMinyvT9EmM2H3QMSJMTAz9O1uGu'
        prf_out = 'indexes/emb/prf'
        
        tre = 'https://drive.google.com/uc?id=1-1BPb-FGSA32gx_zrXh6guTOkQ9GuSSS'
        tre_out = 'indexes/emb/tre'
        
        gdown.download(grp, grp_out, quiet=False)
        gdown.download(obj, obj_out, quiet=False)
        gdown.download(prf, prf_out, quiet=False)
        gdown.download(tre, tre_out, quiet=False)
        
        self.load_index("indexes/emb")
            
    def get_scorces_query(self, id,query,k):
        out = dict()
        emb = self.model.encode(query)
        hits = self.index.search(emb,k,0.01)
        for hit in hits:
            out[self.searcher.doc(hit[0]).docid()] = 1-hit[1]

        return out
