# elasticsearch
elasticsearch and kibana

# Usage
```bash
docker-compose up -d --build
```

## how to use powershells
download latest wikipedia articles. i downloaded jawiki-latest-pages-articles.xml.bz2  
https://dumps.wikimedia.org/jawiki/

after unarchived bz2, run split_to_files.ps1.
it'll take long time to done.
```bash
pwsh ./split_to_files.ps1
```

after splited txt files, extract_header and footer.  
run extract_header_footer.ps1
```bash
pwsh ./extract_header_footer.ps1
```

lets import wikipedia datas.  
run import_data.ps1
```bash
pwsh ./import_data.ps1
```

after done, check out search query on kibana's Dev Tools like this.
```
GET /wikipedia/_search?pretty
{
  "query":{
    "match":{
      "text":"地理学"
    }
  },
  "_source": ["id", "title", "text"],
  "size": 100
}
```
