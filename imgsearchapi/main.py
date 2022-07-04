import uvicorn
import logging
from fastapi import FastAPI, UploadFile, File
import io
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet34, ResNet34_Weights
from elasticsearch import Elasticsearch

app = FastAPI()
logger = logging.getLogger('uvicorn')
es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
target_index = "img"
max_size = 3

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/similarimgs/")
async def search_similarimgs(file: UploadFile = File(...)):
  request_object_content = await file.read()
  img = Image.open(io.BytesIO(request_object_content))
  model = resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)
  model.fc = nn.Identity()
  transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
  with torch.no_grad():
    target = transform(img.convert('RGB'))
    output = model(target[None, ...])
  query_vector = output[0].tolist()
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
    index=target_index,
    size=max_size,
    query=script_query
  )

  results = [
  {
      'text': row['_source']['text'], 
      'image_format': row['_source']['image_format'], 
      'image': row['_source']['image'], 
      'score': row['_score'],
  }
  for row in response['hits']['hits']
  ]

  return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)