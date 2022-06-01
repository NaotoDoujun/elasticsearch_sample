from xml.etree.ElementInclude import include
import pandas as pd
from collections import OrderedDict
from bert_serving.client import BertClient
import sentencepiece as spm
from elasticsearch import Elasticsearch
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
target_index = "bert"

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

def search_with_vector(query, index):
  bsc = BertServingClient()
  query_vector = bsc.sentence2vec([query])[0].tolist()
  script_query = {
      "script_score": {
          "query": {"match_all": {}},
          "script": {
              "source": "(cosineSimilarity(params.query_vector, 'vector') + 1.0)/2",
              "params": {"query_vector": query_vector}
          }
      }
  }
  response = es.search(
      index=index,
      size=10,
      query=script_query
  )
  return pd.DataFrame([
      OrderedDict({
          'text': row['_source']['text'], 
          'score': row['_score']
      }) for _, row in pd.DataFrame(response['hits']['hits']).iterrows()])

def search_with_kuromoji(query, index):
  response = es.search(
      index=index,
      query={
        "match": {
            "text": query
        }
      }
  )
  return pd.DataFrame([
      OrderedDict({
          'text': row['_source']['text'], 
          'score': row['_score']
      }) for _, row in pd.DataFrame(response['hits']['hits']).iterrows()])

def search_with_kuromoji_and_vector(query, index):
  bsc = BertServingClient()
  query_vector = bsc.sentence2vec([query])[0].tolist()
  script_query = {
      "script_score": {
          "query": {
              "match": {
                  "text": query
              }
          },
          "script": {
              "source": "_score + (cosineSimilarity(params.query_vector, 'vector') + 1.0)/2",
              "params": {"query_vector": query_vector}
          }
      }
  }
  response = es.search(
      index=index,
      query=script_query
  )
  return pd.DataFrame([
      OrderedDict({
          'text': row['_source']['text'], 
          'score': row['_score']
      }) for _, row in pd.DataFrame(response['hits']['hits']).iterrows()])

def main():
  print('*** vector only ***')
  print(search_with_vector('今日は晴れです', target_index))
  print('*** kuromoji only ***')
  print(search_with_kuromoji('今日は晴れです', target_index))
  print('*** kuromoji and vector ***')
  print(search_with_kuromoji_and_vector('今日は晴れです', target_index))

if __name__ == '__main__':
  main()
  es.close()