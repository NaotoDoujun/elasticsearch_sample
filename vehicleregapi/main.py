# -*- coding: utf-8 -*-
import uvicorn
import logging
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import BertJapaneseTokenizer, BertModel
from elasticsearch import Elasticsearch

app = FastAPI()
logger = logging.getLogger('uvicorn')
MODEL_NAME = 'cl-tohoku/bert-base-japanese-whole-word-masking'
target_index = "vehicleregs"
tokenizer_jp = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
max_length = 256
max_size = 3

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
    return {"Api": "vehicle regulations search by cosineSimilarity [cl-tohoku/bert-base-japanese]"}

@app.post("/similardocs/")
def search_similardocs(item: Item):
    query_vector = embedding(item.text)
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
            'metadata_storage_name': row['_source']['metadata_storage_name'], 
            'summarized_text': row['_source']['summarized_text'], 
            'score': row['_score'],
        }
        for row in response['hits']['hits']
    ]

    return results
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200)