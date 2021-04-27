

class myModel:
    
    
    def fit(data):
        pass

    def get_scorces_query(id,query,k):
        pass

    def run_all_queries(self, fileSave, queries, k):
        with open(fileSave, 'w') as runfile:
            cnt = 0
            print('Running {} queries in total'.format(len(queries)))
            for key,text in queries.items():
                hits = self.get_scorces_query(key,text,k)
                i=1
                for id_doc,score in hits.items():
                    _ = runfile.write('{} Q0 {} {} {:.6f} {}\n'.format(key, id_doc, i, score,self.name))
                    i+=1
                cnt += 1
                if cnt % 100 == 0:
                    print(f'{cnt} queries completed')
        print("done.")