
import json
import os

def convert_collection_to_json(collection_path,output_folder,max_docs_per_file=1000000):
    ####convert collection to json###########
    file_index = 0
    with open(collection_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            doc_id, doc_text = line.rstrip().split('\t')
            if i % max_docs_per_file == 0:
                if i > 0:
                    output_jsonl_file.close()
                output_path = os.path.join(output_folder, 'docs{:02d}.json'.format(file_index))
                output_jsonl_file = open(output_path, 'w', encoding='utf-8', newline='\n')
                file_index += 1
            output_dict = {'id': doc_id, 'contents': doc_text}
            output_jsonl_file.write(json.dumps(output_dict) + '\n')

            if i % 100000 == 0:
                print(i)
    output_jsonl_file.close() 
    

# stopwords
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
    # process text by tokenizing and removing stopwords
    processed = text.lower().replace('.', ' ').replace(',', ' ').replace('?', ' ')
    return [word for word in processed.split() if word not in stop_words]



def split_new_repeated(pred_text, doc_text):
    # split new and repeated prediction words
    pred_repeated = []
    pred_new = []

    doc_text_set = set(prepare(doc_text))
    processed_pred_text = prepare(pred_text)
    for word in processed_pred_text:
        if word in doc_text_set:
            pred_repeated.append(word)
        else:
            pred_new.append(word)

    return pred_new, pred_repeated


def create_passage_expansion(output_folder,collection_path,predictions,max_docs_per_file=1000000,new_prediction_copies=1,split_predictions=False,repeated_prediction_copies=1,original_copies=1,prediction_copies=1) :
    file_index = 0
    new_words = 0
    total_words = 0

    with open(collection_path) as f_corpus, open(predictions) as f_pred:
        for i, (line_doc, line_pred) in enumerate(zip(f_corpus, f_pred)):
            # Write to a new file when the current one reaches maximum capacity.
            if i % max_docs_per_file == 0:
                if i > 0:
                    output_jsonl_file.close()
                output_path = os.path.join(output_folder, f'docs{file_index:02d}.json')
                output_jsonl_file = open(output_path, 'w')
                file_index += 1

            doc_id, doc_text = line_doc.rstrip().split('\t')
            pred_text = line_pred.rstrip()

            contents = ''
            if split_predictions:
                pred_new, pred_repeated = split_new_repeated(pred_text, doc_text)
                new_words += len(pred_new)
                total_words += len(pred_new) + len(pred_repeated)

                contents += (doc_text + ' ') * original_copies
                contents += (' '.join(pred_repeated) + ' ') * repeated_prediction_copies
                contents += (' '.join(pred_new) + ' ') * new_prediction_copies
            else:
                contents += (doc_text + ' ') * original_copies
                contents += (pred_text + ' ') * prediction_copies

            output_dict = {'id': doc_id, 'contents': contents}
            output_jsonl_file.write(json.dumps(output_dict) + '\n')

            if i % 100000 == 0:
                print(i)
    output_jsonl_file.close()
    


    


