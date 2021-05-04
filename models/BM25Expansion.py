from models.BM25 import BM25
from models.utils import *
import zipfile
import gdown

class BM25Expansion(BM25):

    def __init__(self, data=None, prebuilt=False,passage=True,query=True):
        self.name="BM25"
        self.data = data
        self.passage = passage
        self.query = query
        if prebuilt == True:
            self.passage = True
            self.get_prebuilt_expension_index()
            self.data = "indexes/expansion/"
            
        if(self.passage):
            
            self.name=self.name+"+Expansion"
            if self.data == None:
                self.data = "indexes/expansion/"
            self.searcher = SimpleSearcher(self.data)
        else:
            if self.data == None:
                self.data = "msmarco-passage"
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
            
        if query == True:
            self.searcher.set_rm3(7, 3, 0.9)
            self.name=self.name+"+RM3"
            
            
    def get_prebuilt_expension_index(self):
        if self.passage == True:
            
            data = 'https://drive.google.com/uc?id=1hr-SspPUWI9YvwaLFqDgZudE6i68QQQP'
            data_out = 'indexes/expansion/ind.zip'
            gdown.download(data, data_out, quiet=False)
            
            print("unzipping...")
            
            with zipfile.ZipFile("indexes/expansion/ind.zip", 'r') as f:
                f.extractall("indexes/expansion/")
            print("done...")
        else:
            print("no prebuilt index needed")
    

