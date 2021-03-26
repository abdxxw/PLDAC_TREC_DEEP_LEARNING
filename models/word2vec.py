
import BM25


class Word2vec(myModel):

    def __init__(self, data, prebuilt=True,ponderation=False):
        self.data = data
        self.prebuilt = prebuilt
        self.ponderation = ponderation
        self.bm25 = BM25(self.data,self.prebuilt) 

        if(self.prebuilt):
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
        else:
            self.searcher = SimpleSearcher(self.data)

        # must download it first 
        #!wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
        #!gunzip GoogleNews-vectors-negative300.bin.gz  

        self.model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True) 


    def vectorize(self, text: str) -> np.ndarray:

        if(ponderation == False):
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


    def get_scorces_query(self, query,k):
        hits = BM25.get_scorces_query(query,k)
        out = dict()
        
        for i in range(len(hits)):
            docID=hits[i].docid

            query = prepareText(query)

            chaine=self.searcher.doc(docID).raw()
            chaine=json.loads(chaine)['contents']
            chaine = prepareText(chaine)

            out[docID] = cosine_similarity(self.vectorize(query),self.vectorize(chaine))

        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)

    
    def run_all_queries(self, fileSave, queries, k):
        with open(fileSave, 'w') as runfile:
            cnt = 0
            print('Running {} queries in total'.format(len(queries)))
            for key,text in queries.items():
                hits = self.get_scorces_query(text,k)
                for i in range(0, len(hits)):
                    _ = runfile.write('{} Q0 {} {} {:.6f} Word2Vec\n'.format(key, hits[i].docid, i+1, hits[i].score))
                cnt += 1
                if cnt % 100 == 0:
                    print(f'{cnt} queries completed')










