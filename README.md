# elasticsearch-sample
elasticsearch and kibana

## Usage
```bash
docker-compose up -d --build
```

## Use wikipedia cirrussearch dump
Download latest wikipedia cirrussearch dump file and place it in the 'wikisearchapi/wiki' folder.  
https://dumps.wikimedia.org/other/cirrussearch/  
I used 'jawiki-20220801-cirrussearch-content.json.gz' 

## Create index and bulk import jawiki
Run below command in 'wikisearchapi' container.
```bash
python3 /app/wiki/bulk_jawiki.py
```
If you wanna re-create index, enter y
```bash
root@ef85762ce1d9:/app# python3 /app/wiki/bulk_jawiki.py
Re-create index[jawiki] before bulk import? [Y]es/[N]o? >> y
 ****** bulk_import 1 [8.8 KB] started at 2022-05-21 03:36:37.542012 *****
 ****** bulk_import 1 [8.8 KB]    done at 2022-05-21 03:36:58.324974 *****
 ****** bulk_import 2 [8.8 KB] started at 2022-05-21 03:37:00.044334 *****
 ****** bulk_import 2 [8.8 KB]    done at 2022-05-21 03:37:21.928143 *****
 ****** bulk_import 3 [8.8 KB] started at 2022-05-21 03:37:23.277009 *****
```

## wiki search API - cosine similarity
API for searching similar sentences by cosine similarity is also provided.  
Open below link.  
[wiki search api](http://localhost:8000/docs)  

## Scrapy Sample
The sample crawls YahooJAPAN News every hour and imports them in the "news" index of Elasticsearch.  
You can change the index on the configuration drawer screeen on frontui.  
If you wanna crawl manually, do following command in 'scrapy' container.
```bash
scrapy crawl news
```

## Create index and bulk import images for imgsearchapi
Download data from below link and place images/* dir in the imgsearchapi/imgsearch/data  
[The Oxford-IIIT Pet Dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz)  
after that, run below commands in 'imgsearchapi' container for import images.
```bash
$ python3 /app/imgsearch/bulk_image.py
Re-create index[img] before bulk import? [Y]es/[N]o? >> y
 ****** bulk_import 1 [8.8 KB] started at 2022-07-01 22:12:47.811974 *****
 ****** bulk_import 1 [8.8 KB]    done at 2022-07-01 22:12:51.023641 *****
 ****** bulk_import 2 [8.8 KB] started at 2022-07-01 22:15:29.364207 *****
 ****** bulk_import 2 [8.8 KB]    done at 2022-07-01 22:15:32.618342 *****
 ****** bulk_import 3 [8.8 KB] started at 2022-07-01 22:18:26.305832 *****
 ****** bulk_import 3 [8.8 KB]    done at 2022-07-01 21:48:23.026140 *****
 ****** bulk_import 4 [8.8 KB] started at 2022-07-01 21:51:11.188884 *****
 ****** bulk_import 4 [8.8 KB]    done at 2022-07-01 21:51:18.016117 *****
 ****** bulk_import 5 [8.8 KB] started at 2022-07-01 21:54:02.526813 *****
 ****** bulk_import 5 [8.8 KB]    done at 2022-07-01 21:54:09.464060 *****
 ****** bulk_import 6 [8.8 KB] started at 2022-07-01 21:58:35.270934 *****
 ****** bulk_import 6 [8.8 KB]    done at 2022-07-01 21:58:39.750954 *****
 ****** bulk_import 7 [8.8 KB] started at 2022-07-01 22:02:33.183102 *****
 ****** bulk_import 7 [8.8 KB]    done at 2022-07-01 22:02:35.908420 *****
 ****** bulk_import 8 [3.22 KB] started at 2022-07-01 22:03:32.831363 *****
 ****** bulk_import 8 [3.22 KB]    done at 2022-07-01 22:03:33.913035 *****
```
API for searching similar images by cosine similarity is here.  
[image search api](http://localhost:8100/docs)  

## YouTube Indexer Sample
This sample crawls every hour by specific keywords and import results of texted speeches in the "tube" index of Elasticsearch.  
Refer to ".env.sample", make ".env" and put your "api_key" in it.

## Create Index and bulk import for Vehicle Regulations Search
Run below command in 'vehicleregapi' container.
```bash
python3 /app/vehicleregs/bulk_vehicleregs.py
```
If you wanna re-create index, enter y
```bash
$ python3 /app/vehicleregs/bulk_vehicleregs.py
Some weights of the model checkpoint at cl-tohoku/bert-base-japanese-whole-word-masking were not used when initializing BertModel: ['cls.predictions.bias', 'cls.seq_relationship.weight', 'cls.predictions.transform.dense.bias', 'cls.predictions.decoder.weight', 'cls.predictions.transform.LayerNorm.bias', 'cls.predictions.transform.LayerNorm.weight', 'cls.seq_relationship.bias', 'cls.predictions.transform.dense.weight']
- This IS expected if you are initializing BertModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing BertModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
Re-create index[vehicleregs] before bulk import? [Y]es/[N]o? >> y
 ****** bulk_import 1 [2.16 KB] started at 2022-08-24 11:36:31.147304 *****
 ****** bulk_import 1 [2.16 KB]    done at 2022-08-24 11:36:33.974822 *****
```
API for searching similar sentences by cosine similarity is here.  
[vehicle regulations api](http://localhost:8200/docs) 