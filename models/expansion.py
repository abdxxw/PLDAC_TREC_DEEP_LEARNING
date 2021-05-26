
import json
import os
import gdown

def convert_collection_to_json(path,Foutput,max_docs_per_file=1000000):
    ####convert collection to json###########
    index_fichier = 0
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            doc_id, doc_text = line.rstrip().split('\t')
            if i % max_docs_per_file == 0:
                if i > 0:
                    res.close()
                output_path = os.path.join(Foutput, 'docs{:02d}.json'.format(index_fichier))
                res = open(output_path, 'w', encoding='utf-8', newline='\n')
                index_fichier += 1
            output_dict = {'id': doc_id, 'contents': doc_text}
            res.write(json.dumps(output_dict) + '\n')

            if i % 100000 == 0:
                print(i)
    res.close() 
    

stop_words = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there',
              'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they',
              'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
              'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who',
              'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below',
              'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me',
              'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our',
              'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she',
              'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and',
              'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then',
              'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
              'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too',
              'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't',
              'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
              'how', 'further', 'was', 'here', 'than'}



def prepare(text):
    prepoc = text.lower().replace('.', ' ').replace(',', ' ').replace('?', ' ')
    return [word for word in prepoc.split() if word not in stop_words]



def split_new_repeated(pred_text, doc_text):
    # split new and repeated prediction words
    pred_r = []
    pred_new = []

    doc_text_set = set(prepare(doc_text))
    processed_pred_text = prepare(pred_text)
    for word in processed_pred_text:
        if word in doc_text_set:
            pred_r.append(word)
        else:
            pred_new.append(word)

    return pred_new, pred_r


def create_passage_expansion(Foutput,path,pred,max_docs_per_file=1000000,new_pred=1,s_predictions=False,r_prediction_c=1,orig_copies=1,prediction_c=1) :
    index_fichier = 0
    words_n = 0
    nombre_words = 0

    with open(path) as f_corpus, open(pred) as f_pred:
        for i, (line_doc, line_pred) in enumerate(zip(f_corpus, f_pred)):
            if i % max_docs_per_file == 0:
                if i > 0:
                    res.close()
                output_path = os.path.join(Foutput, f'docs{index_fichier:02d}.json')
                res = open(output_path, 'w')
                index_fichier += 1

            doc_id, doc_text = line_doc.rstrip().split('\t')
            pred_text = line_pred.rstrip()

            contenu = ''
            if s_predictions:
                pred_new, pred_repeated = split_new_repeated(pred_text, doc_text)
                words_n += len(pred_new)
                nombre_words += len(pred_new) + len(pred_repeated)

                contenu += (doc_text + ' ') * orig_copies
                contenu += (' '.join(pred_repeated) + ' ') * r_prediction_c
                contenu += (' '.join(pred_new) + ' ') * new_pred
            else:
                contenu += (doc_text + ' ') * orig_copies
                contenu += (pred_text + ' ') * prediction_c

            output_dict = {'id': doc_id, 'contenu': contenu}
            res.write(json.dumps(output_dict) + '\n')

            if i % 100000 == 0:
                print(i)
    res.close()
    
    

