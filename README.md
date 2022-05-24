# elasticsearch-sample
elasticsearch and kibana

## Usage
```bash
docker-compose up -d --build
```

## Use wikipedia cirrussearch dump
Download latest wikipedia cirrussearch dump file and place it in the 'scrapy/wiki' folder.  
https://dumps.wikimedia.org/other/cirrussearch/  
I used 'jawiki-20220516-cirrussearch-content.json.gz'  

## Create index with mapping and bulk import jawiki
Run below command in 'scrapy' container.
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

## Scrapy Sample
The sample crawls YahooJAPAN News every hour and imports them in the "news" index of Elasticsearch.  
You can change the index on the configuration drawer screeen on frontui.  
If you wanna crawl manually, do following command in 'scrapy' container.
```bash
scrapy crawl news
```