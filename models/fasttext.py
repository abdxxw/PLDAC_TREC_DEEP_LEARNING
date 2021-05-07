
from models.utils import *
from models.model import myModel


class Fasttext(myModel):

    def __init__(self, file,searcher):
        self.name = 'FastText'
        self.firststage = file
        self.oldrun = run_parser(file)
        fasttext.util.download_model('en', if_exists='ignore')
        self.model = fasttext.load_model('cc.en.300.bin')
        self.searcher = searcher

    def set_firststage(self,file):
        self.firststage= file
        self.oldrun = run_parser(file)
        
    def get_scorces_query(self, id,query,k):
        q_results = self.oldrun.get(id,dict())
        out = dict()
        
        for key,score in q_results.items():

            query = prepareText(query)

            chaine=self.searcher.doc(key).raw()
            chaine=json.loads(chaine)['contents']
            chaine = prepareText(chaine)

            out[key] = cosine_similarity(self.model.get_sentence_vector(query),self.model.get_sentence_vector(chaine))

        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)
