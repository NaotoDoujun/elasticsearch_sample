# -*- coding: utf-8 -*-
import json, gzip, datetime, sys, math
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import torch
from transformers import BertJapaneseTokenizer, BertModel
from elasticsearch import Elasticsearch, helpers
TARGET_FILE = "/app/wiki/jawiki-20220801-cirrussearch-content.json.gz"
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
target_index = "jawiki"
target_mapping = "/app/wiki/jawiki_mapping.json"
target_setting = "/app/wiki/jawiki_setting.json"
auto_abstractor = AutoAbstractor()
auto_abstractor.tokenizable_doc = MeCabTokenizer()
auto_abstractor.delimiter_list = ["。", "\n"]
abstractable_doc = TopNRankAbstractor()
tokenizer_jp = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
max_length = 256
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)

def progress(current, pro_size):
    return print('\r making bulk data {0}% {1}/{2}'.format(
        math.floor(current / pro_size * 100.), 
        current, 
        pro_size), end='')

def convert_size(size, unit="B"):
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    i = units.index(unit.upper())
    size = round(size / 1024 ** i, 2)
    return f"{size} {units[i]}"

def summarize(text):
    result_dict = auto_abstractor.summarize(text, abstractable_doc)
    results = [x.replace('\n','') for x in result_dict["summarize_result"]]
    return ''.join(results)

def embedding(text):
    tokenized_inputs = tokenizer_jp(text, max_length=max_length, padding='max_length', truncation=True, return_tensors='pt')
    attention_mask = tokenized_inputs['attention_mask']
    with torch.no_grad():
        output = model(**tokenized_inputs)
        last_hidden_state = output.last_hidden_state
        averaged_hidden_state = (last_hidden_state * attention_mask.unsqueeze(-1)).sum(1) \
            / attention_mask.sum(1, keepdim=True)
    return averaged_hidden_state[0].tolist()

def do_bulk_import(import_data, count):
    if len(import_data) > 0:
        size = sys.getsizeof(import_data)
        count += 1
        print('\r ****** bulk_import {} [{}] started at {} *****'.format(
            count, 
            convert_size(size, "KB"),
            datetime.datetime.now()))
        helpers.bulk(es, import_data)
        print('\r ****** bulk_import {} [{}]    done at {} *****'.format(
            count, 
            convert_size(size, "KB"), 
            datetime.datetime.now()))
    return count

def create_wiki_doc(curid, json_line):
    summarized_text = summarize(json_line['text'])
    text_vector = embedding(summarized_text)
    return {
        'curid': curid,
        'title': json_line['title'], 
        'text': json_line['text'],
        'summarized_text': summarized_text,
        'text_vector': text_vector,
        'category': json_line['category'],
        'outgoing_link': json_line['outgoing_link'],
        'timestamp': json_line['timestamp']
    }

def open_cirrussearch_file(cirrussearch_file, index_name, bulk_articles_limit, import_limit):
    with gzip.open(cirrussearch_file) as f:
        data, curid, count, import_count = [], 0, 1, 0
        for line in f:
            if not line:
                import_count = do_bulk_import(data, import_count)
                data = []
                break
            else:
                json_line = json.loads(line)
                if "index" not in json_line:
                    progress(count, bulk_articles_limit)
                    data.append({'_index': index_name, '_source':create_wiki_doc(curid, json_line)})
                    if count % bulk_articles_limit == 0:
                        import_count = do_bulk_import(data, import_count)
                        data, count = [], 1
                        if import_limit > 0 and import_count >= import_limit:
                            break
                    else:
                        count += 1
                else:
                    curid = json_line['index']['_id']

def bulk_import_wiki(bulk_articles_limit=1000, import_limit=0):
    open_cirrussearch_file(TARGET_FILE, target_index, bulk_articles_limit, import_limit)

def make_index():
    if es.indices.exists(index=target_index):
        es.indices.delete(index=target_index)
    
    with open (target_setting) as fs:
        setting = json.load(fs)
        with open(target_mapping) as fm:
            mapping = json.load(fm)
            es.indices.create(index=target_index, mappings=mapping, settings=setting)

def check_recreate_index():
    while True:
        inp = input('Re-create index[{}] before bulk import? [Y]es/[N]o? >> '.format(target_index)).lower()
        if inp in ('y', 'yes', 'n', 'no'):
            inp = inp.startswith('y')
            break
        print('Error! Input again.')
    return inp

def main():
    if check_recreate_index():
        make_index()
    bulk_import_wiki(1000, 1)
    
if __name__ == '__main__':
    main()
    es.close()