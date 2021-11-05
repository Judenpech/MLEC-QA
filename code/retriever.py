import json
import time
from tqdm import tqdm
from elasticsearch import Elasticsearch

data_dir = './data_raw/'
target_dir = './data/'
etype = 'Clinic'  # Clinic, Stomatology, PublicHealth, TCM, CWM
file = etype + '.json'


def get_wiki_doc(search_query, res_not_found):
    search_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": search_query
                        }
                    }
                ]
            }
        },
        "size": 1
    }

    es = Elasticsearch(index='wiki_zh', ip="127.0.0.1", )
    res = es.search(index='wiki_zh', body=search_body, request_timeout=30)

    # for hit in res['hits']['hits']:
    #     print(hit['_source'])

    try:
        res_txt = res['hits']['hits'][0]['_source']['text']
    except:
        res_not_found = 1
        res_txt = ""

    return res_txt, res_not_found


def elasticsearch_retriever():
    print(file)
    with open(data_dir + file, 'r', encoding='utf-8') as f1:
        data_json = json.load(f1)

    data_wiki_ls = []
    res_not_found = 0

    for samp in tqdm(data_json):
        docs = ""
        for op in samp['options']:
            search_query = samp['qtext'] + samp['options'][op]

            doc, rnf = get_wiki_doc(search_query, 0)
            docs += doc
            if rnf:
                print(samp)
                res_not_found += rnf

        data_wiki_dict = {'qid': samp['qid'],
                          'qtype': samp['qtype'],
                          'qtext': samp['qtext'],
                          'options': samp['options'],
                          'answer': samp['answer'],
                          'docs': docs}

        data_wiki_ls.append(data_wiki_dict)

    data_wiki_json = json.dumps(data_wiki_ls, ensure_ascii=False)
    with open(target_dir + etype + '.json', 'w', encoding='utf-8') as f1:
        f1.write(data_wiki_json)

    print('\nNo search results: ', res_not_found)


if __name__ == '__main__':
    start = time.time()
    elasticsearch_retriever()
    end = time.time()
    print("\nTotal time elapsed: %s s" % (end - start))
