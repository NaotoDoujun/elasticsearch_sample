import pandas as pd
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet34, ResNet34_Weights
from collections import OrderedDict
from elasticsearch import Elasticsearch
import warnings
warnings.resetwarnings()
warnings.simplefilter('ignore', UserWarning)

es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
target_index = "img"

def search_with_vector(filepath, index):
  img = Image.open(filepath)
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
      index=index,
      size=10,
      query=script_query
  )
  return pd.DataFrame([
      OrderedDict({
          'text': row['_source']['text'], 
          'score': row['_score']
      }) for _, row in pd.DataFrame(response['hits']['hits']).iterrows()])

def main():
  filepath = '/app/imgsearch/data/images/Abyssinian_3.jpg' #search image
  print(search_with_vector(filepath, target_index))

if __name__ == '__main__':
  main()
  es.close()