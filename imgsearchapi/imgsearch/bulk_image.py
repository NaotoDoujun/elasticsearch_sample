# -*- coding: utf-8 -*-
import os, glob, json, datetime, sys, math
import torch
import torch.nn as nn
from torchvision.models import resnet34, ResNet34_Weights
from elasticsearch import Elasticsearch, helpers
from image_dataset import *
import warnings
warnings.resetwarnings()
warnings.simplefilter('ignore', UserWarning)

es = Elasticsearch("http://elasticsearch:9200", request_timeout=100)
target_index = "img"
target_mapping = "/app/imgsearch/img_mapping.json"
images_path = "/app/imgsearch/data/images"
image_format = "jpeg"

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

def bulk_import_img(bulk_images_limit=1000):
  l = glob.glob(os.path.join(images_path, '*.jpg'))
  dataset = ImageDataSet(images_path, l, image_format)
  dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)
  model = resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)
  model.fc = nn.Identity()
  count, import_data, import_count = 1, [], 0
  for i, (data, filepath, img_base64) in enumerate(dataloader):
    with torch.no_grad():
      output = model(data)
    doc = {}
    filename = filepath[0].split("/")[-1]
    doc["text"] = filename
    doc["image"] = img_base64
    doc["image_format"] = image_format
    doc["vector"] = output[0].tolist()
    progress(count, bulk_images_limit)
    import_data.append({'_index': target_index, '_source': doc})
    if count % bulk_images_limit == 0:
      import_count = do_bulk_import(import_data, import_count)
      count, import_data = 1, []
    elif len(dataloader) == i + 1 and len(import_data) > 0:
      import_count = do_bulk_import(import_data, import_count)
      count, import_data = 1, []
    else:
      count += 1

def make_index():
  if es.indices.exists(index=target_index):
      es.indices.delete(index=target_index)
  with open(target_mapping) as fm:
      mapping = json.load(fm)
      es.indices.create(index=target_index, mappings=mapping)

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
  bulk_import_img(1000)
    
if __name__ == '__main__':
  main()
  es.close()