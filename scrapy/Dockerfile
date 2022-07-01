FROM python:3.8
WORKDIR /app

RUN apt-get update && apt-get install -y busybox-static && apt-get clean all

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt --no-cache-dir

# crawl schedule every hour
RUN mkdir -p /var/spool/cron/crontabs/ \
  && echo '0 */1 * * * cd /app/sample_crawler && scrapy crawl news' > /var/spool/cron/crontabs/root

# copy sample_crawler
COPY sample_crawler .

ENTRYPOINT ["busybox", "crond", "-f", "-L", "/dev/stderr"]