# -*- coding: utf-8 -*-
import json, datetime, sys, math
import torch
from transformers import BertJapaneseTokenizer, BertModel
from elasticsearch import Elasticsearch, helpers
TARGET_FILE = "/app/vehicleregs/result.json"
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
target_index = "vehicleregs"
target_mapping = "/app/vehicleregs/vehicle_reg_mapping.json"
target_setting = "/app/vehicleregs/vehicle_reg_setting.json"
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

def create_vehiclereg_doc(json_line):
    text_vector = embedding(json_line['summarized_text'])
    return {
        'metadata_storage_name': json_line['metadata_storage_name'],
        'translated_text': json_line['translated_text'],
        'summarized_text': json_line['summarized_text'],
        'text_vector': text_vector
    }

def open_result_file(result_file, index_name, bulk_articles_limit, import_limit):
    with open(result_file) as f:
        results = json.load(f)
        data, count, import_count = [], 1, 0
        max = len(results['result'])
        if max < bulk_articles_limit:
            bulk_articles_limit = max
        for json_line in results['result']:
            progress(count, bulk_articles_limit)
            data.append({'_index': index_name, '_source':create_vehiclereg_doc(json_line)})
            if count % bulk_articles_limit == 0:
                import_count = do_bulk_import(data, import_count)
                data, count = [], 1
                if import_limit > 0 and import_count >= import_limit:
                    break
            else:
                count += 1

def bulk_import_vehicleregs(bulk_articles_limit=1000, import_limit=0):
    open_result_file(TARGET_FILE, target_index, bulk_articles_limit, import_limit)

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
    bulk_import_vehicleregs(1000, 1)
    
if __name__ == '__main__':
    main()
    es.close()