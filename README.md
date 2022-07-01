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

## BERT Serving Sample
Download model files from below link and place them in the bertserving/model   
[BERT-wiki-ja](https://drive.google.com/drive/folders/1aR9kA8gRN9cT_tXO36E-y33tC-qb5-SH)  
If you wanna try vector search, place "wiki-ja.model" in the scrapy/bert_test and run below commands in 'scrapy' container.
```bash
cd /app/bert_test
python3 bulk_bert_test.py
python3 search_test.py
```

## Image Search Sample
Download data from below link and place images/* dir in the scrapy/image_search/data  
[The Oxford-IIIT Pet Dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz)  
If you wanna try vector search, run below commands in 'scrapy' container.
```bash
$ cd /app/image_search
$ python3 bulk_image.py
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
$ python3 search_img.py
                   text     score
0      Abyssinian_3.jpg  1.000000
1      Abyssinian_1.jpg  0.998035
2     Abyssinian_67.jpg  0.998010
3    Abyssinian_179.jpg  0.998003
4          Bengal_1.jpg  0.997973
5    Abyssinian_180.jpg  0.997969
6        Bombay_108.jpg  0.997948
7      chihuahua_30.jpg  0.997927
8  Russian_Blue_106.jpg  0.997914
9        Bengal_110.jpg  0.997912
```