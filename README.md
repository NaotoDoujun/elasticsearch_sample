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
Run below commands in 'scrapy' container.
```bash
curl -H "Content-Type: application/json" -XPUT 'http://elasticsearch:9200/jawiki?pretty' -d @/app/wiki/jawiki.json
python3 /app/wiki/bulk_jawiki.py
```