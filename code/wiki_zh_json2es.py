import json
import os
import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

data_dir = './wiki_zh/'


class ElasticObj:
    def __init__(self, index_name, index_type, ip):
        """
        :param index_name: index name
        :param index_type: index type
        """
        self.index_name = index_name
        self.index_type = index_type

        # No user name password status
        self.es = Elasticsearch([ip])

        # User name password status
        # self.es = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    def create_index(self):
        '''
        Create index
        :param ex: Elasticsearch object
        :return:
        '''
        # Create mappings
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "title": {
                            'type': 'keyword'
                        },
                        "text": {
                            'type': 'text'
                        }
                    }
                }
            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings, ignore=[400, 404])
            print(res)

    # Import data
    def insert_data(self, inputfile):
        # Read data
        data = []
        with open(inputfile, 'r', encoding='utf-8') as f1:
            for ln in f1.readlines():
                data.append(json.loads(ln))

        ACTIONS = []
        for samp in data:
            action = {
                "_index": self.index_name,
                "_id": int(samp['id']),
                "_source": {
                    "title": samp['title'],
                    "text": samp["text"]
                }
            }
            ACTIONS.append(action)

        # Batch import
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        print(inputfile)
        print('import data:', success, '/', len(ACTIONS), '\n')
        del ACTIONS[0:len(ACTIONS)]


def main():
    obj = ElasticObj("wiki_zh", "_doc", ip="127.0.0.1")
    obj.create_index()

    for root, dirs, files in os.walk(data_dir):
        for fn in files:
            file_path = os.path.join(root, fn)
            obj.insert_data(file_path)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("\nTotal time elapsed: %s s" % (end - start))
