# -*- coding: utf-8 -*-
import json
from bert_serving.client import BertClient
import sentencepiece as spm
from elasticsearch import Elasticsearch, helpers
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
target_index = "bert"
target_mapping = "/app/bert_test/bert_mapping.json"
target_setting = "/app/bert_test/bert_setting.json"

class BertServingClient:
    def __init__(self, sp_model='wiki-ja.model', bert_server_ip='bertserving',bert_port=5555,bert_port_out=5556):
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(sp_model)
        self.bc = BertClient(
            ip=bert_server_ip, 
            port=bert_port,
            port_out=bert_port_out,
            check_version = False,
            check_length = False,
            timeout=10000)
        
    def sentence_piece_tokenizer(self, text):
        text = text.lower()
        return self.sp.EncodeAsPieces(text)
    
    def sentence2vec(self, sentences):
        parsed_texts = list(map(self.sentence_piece_tokenizer, sentences))
        return self.bc.encode(parsed_texts, is_tokenized=True)

def do_bulk_import():
  bsc = BertServingClient()
  texts = [
      '今日は晴れです',
      '明日は雨です',
      '今日は暑いです',
      '明日は涼しいです'
  ]
  vectors = bsc.sentence2vec(texts)
  docs = [
      {
          'text': text, 
          'vector': vector.tolist(), 
          '_index': target_index
      } 
      for text, vector in zip(texts, vectors)
  ]
  helpers.bulk(es, docs)

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
  do_bulk_import()

if __name__ == '__main__':
  main()
  es.close()