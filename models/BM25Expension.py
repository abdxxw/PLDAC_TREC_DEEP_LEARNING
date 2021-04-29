from models.model import BM25
from models.utils import *
import zipfile

class BM25Expension(BM25):

    def __init__(self, data=None, generate=False,passage=True,query=True):
        self.name="BM25"
        self.data = data
        self.passage = passage
        self.query = query
        if generate == True:
            self.passage = True
            self.get_prebuilt_expension_index()
            self.data = "indexes/expansion/"
            
        if(self.passage):
            
            self.name=self.name+"+Expension"
            if self.data == None:
                self.data = "indexes/expansion/"
            self.searcher = SimpleSearcher(self.data)
        else:
            if self.data == None:
                self.data = "msmarco-passage"
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
            
        if query == True:
            self.searcher.set_rm3(10, 10, 0.5)
            self.name=self.name+"+RM3"
            
            
    def get_prebuilt_expension_index(self):
        if self.passage == True:
            print("downloading...")
            
            data = 'https://drive.google.com/uc?id=1KnhispEvKnd5O-f9iKojiBm7IaAB9rcr'
            data_out = 'indexes/expansion/ind.zip'
            gdown.download(data, data_out, quiet=False)
            
            print("unzipping...")
            
            with zipfile.ZipFile("indexes/expansion/ind.zip", 'r') as f:
                f.extractall("indexes/expansion/")
            print("done...")
        else:
            print("no prebuilt index needed")
    

