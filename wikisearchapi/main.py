# -*- coding: utf-8 -*-
import uvicorn
import json, urllib, logging
from fastapi import FastAPI
from pydantic import BaseModel
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import torch
from transformers import BertJapaneseTokenizer, BertModel
from elasticsearch import Elasticsearch

app = FastAPI()
logger = logging.getLogger('uvicorn')
TARGET_FILE = "/app/wiki/jawiki-20220801-cirrussearch-content.json.gz"
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
target_index = "jawiki"
auto_abstractor = AutoAbstractor()
auto_abstractor.tokenizable_doc = MeCabTokenizer()
auto_abstractor.delimiter_list = ["。", "\n"]
abstractable_doc = TopNRankAbstractor()
tokenizer_jp = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
max_length = 256
max_size = 3

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

class Item(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Api": "jawiki search by cosineSimilarity [cl-tohoku/bert-base-japanese]"}

@app.post("/similardocs/")
def search_similardocs(item: Item):
    summarized_text = summarize(item.text)
    query_vector = embedding(summarized_text)
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    response = es.search(
        index=target_index,
        size=max_size,
        query=script_query
    )
    results = [
        {
            'title': row['_source']['title'], 
            'text': row['_source']['text'], 
            'score': row['_score'],
        }
        for row in response['hits']['hits']
    ]

    # knn_query = {
    #     "knn": {
    #         "field": "text_vector",
    #         "query_vector": query_vector,
    #         "k": 10,
    #         "num_candidates": 100
    #     },
    #     "_source": False
    # }
    # knn_url = 'http://elasticsearch:9200/{}/_knn_search'.format(target_index)
    # headers = {
    #     'Content-Type': 'application/json',
    # }
    # knn_req = urllib.request.Request(knn_url, json.dumps(knn_query).encode(), headers)
    # with urllib.request.urlopen(knn_req) as knn_res:
    #     body = knn_res.read().decode()
    #     print(body)

    return results
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)