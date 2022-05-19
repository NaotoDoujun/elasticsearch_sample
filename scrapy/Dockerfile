FROM python:3.8
WORKDIR /app

RUN apt-get update && apt-get install -y busybox-static && apt-get clean all

# install scrapy, scrapy_splash and ScrapyElasticSearch
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install Pillow==9.1.1 Scrapy==2.6.1 scrapy-splash==0.8.0 ScrapyElasticSearch==0.9.2

# crawl schedule every hour
RUN mkdir -p /var/spool/cron/crontabs/ \
  && echo '0 */1 * * * cd /app/sample_crawler && scrapy crawl news' > /var/spool/cron/crontabs/root

# copy sample_crawler
COPY sample_crawler .

ENTRYPOINT ["busybox", "crond", "-f", "-L", "/dev/stderr"]