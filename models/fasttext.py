
import BM25

class Fasttext(myModel):

    def __init__(self, data, prebuilt=True):
        self.data = data
        self.prebuilt = prebuilt
        self.pretrained = pretrained
        self.bm25 = BM25(self.data,self.prebuilt) 

        if(self.prebuilt):
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
        else:
            self.searcher = SimpleSearcher(self.data)

        fasttext.util.download_model('en', if_exists='ignore')
        self.model = fasttext.load_model('cc.en.300.bin')


    def get_scorces_query(self, query,k):
        hits = BM25.get_scorces_query(query,k)
        out = dict()
        
        for i in range(len(hits)):
            docID=hits[i].docid

            query = prepareText(query)

            chaine=self.searcher.doc(docID).raw()
            chaine=json.loads(chaine)['contents']
            chaine = prepareText(chaine)

            out[docID] = cosine_similarity(self.model.get_sentence_vector(query),self.model.get_sentence_vector(chaine))

        sor = sorted(out.items(),reverse = True, key=lambda x: x[1])
        return dict(sor)

    
    def run_all_queries(self, fileSave, queries, k):
        with open(fileSave, 'w') as runfile:
            cnt = 0
            print('Running {} queries in total'.format(len(queries)))
            for key,text in queries.items():
                hits = self.get_scorces_query(text,k)
                for i in range(0, len(hits)):
                    _ = runfile.write('{} Q0 {} {} {:.6f} FastText\n'.format(key, hits[i].docid, i+1, hits[i].score))
                cnt += 1
                if cnt % 100 == 0:
                    print(f'{cnt} queries completed')