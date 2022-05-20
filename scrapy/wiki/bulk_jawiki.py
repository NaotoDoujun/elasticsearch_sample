# -*- coding: utf-8 -*-
import json
import gzip
import datetime
import time
from elasticsearch import Elasticsearch, helpers
es = Elasticsearch("http://elasticsearch:9200",timeout=100)

with gzip.open("/app/wiki/jawiki-20220516-cirrussearch-content.json.gz") as f:
    data = []
    count = 1
    bcount = 1
    for line in f:
        json_line = json.loads(line)
        if "index" not in json_line:
            doc = {
                'title': json_line['title'], 
                'text': json_line['text'],
                'category': json_line['category'],
                'outgoing_link': json_line['outgoing_link'],
                'timestamp': json_line['timestamp']
            }
            data.append({'_index':'jawiki', '_source':doc})
            if count % 1000 == 0:
                helpers.bulk(es, data)
                print('****** bulk {} done at {} *****'.format(bcount, datetime.datetime.now()))
                bcount += 1
                count = 1
                data = []
                if bcount >= 101:
                    break
            elif not line:
                helpers.bulk(es, data)
                print('****** bulk {} done at {} *****'.format(bcount, datetime.datetime.now()))
                data = []
                break
            else:
                count += 1

es.close()
