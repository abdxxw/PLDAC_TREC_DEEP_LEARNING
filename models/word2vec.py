
from models.utils import *
from models.model import myModel


class Word2Vec(myModel):

    def __init__(self, file,searcher,ponderation=False):
        self.name = 'Word2Vec'
        self.firststage = file
        self.oldrun = run_parser(file)
        self.searcher = searcher
        self.ponderation = ponderation

        # must download it first 
        #!wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
        #!gunzip GoogleNews-vectors-negative300.bin.gz  

        self.model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True) 


    def set_firststage(self,file):
        self.firststage= file
        self.oldrun = run_parser(file)
        

        

    def vectorize(self, text: str) -> np.ndarray:

        if(self.ponderation == False):
            words = word_tokenize(text)
            word_vecs = []
            for word in words:
                try:
                    vec = self.model[word]
                    word_vecs.append(vec)
                except KeyError:
                    # Ignore, if the word doesn't exist in the vocabulary
                    pass

        else:
            vectorizer = TfidfVectorizer(min_df=1)
            text = [text]
            X = vectorizer.fit_transform(text)
            idf = vectorizer.idf_
            d = dict(zip(vectorizer.get_feature_names(), idf))

            word_vecs = []
            for word,weight in d.items():
                try:
                    vec = self.w2v_model[word] * weight
                    word_vecs.append(vec)
                except KeyError:
                    # Ignore, if the word doesn't exist in the vocabulary
                    pass
        
        vector = np.mean(word_vecs, axis=0)
        return vector

    def get_scorces_query(self, id,query,k):
        q_results = self.oldrun.get(id,dict())
        out = dict()
        
        for key,score in q_results.items():

            chaine=self.searcher.doc(key).raw()
            chaine=json.loads(chaine)['contents']
            try:
                out[key] = cosine_similarity(self.vectorize(query),self.vectorize(chaine))
                if len(out[key] > 1):
                    out[key] = 0
            except:
                out[key] = 0
        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)











