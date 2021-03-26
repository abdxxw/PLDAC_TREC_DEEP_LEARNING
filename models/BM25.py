import utils


class BM25(myModel):

    def __init__(self, data, prebuilt=True):
        self.data = data
        self.prebuilt = prebuilt
        if(self.prebuilt):
            self.searcher = SimpleSearcher.from_prebuilt_index(self.data)
        else:
            self.searcher = SimpleSearcher(self.data)

    def get_scorces_query(self, query,k):
        hits = self.searcher.search(query, k)
        return hits

    
    def run_all_queries(self, fileSave, queries, k):
        with open(fileSave, 'w') as runfile:
            cnt = 0
            print('Running {} queries in total'.format(len(queries)))
            for key,text in queries.items():
                hits = self.get_scorces_query(text,k)
                for i in range(0, len(hits)):
                    _ = runfile.write('{} Q0 {} {} {:.6f} BM25\n'.format(key, hits[i].docid, i+1, hits[i].score))
                cnt += 1
                if cnt % 100 == 0:
                    print(f'{cnt} queries completed')