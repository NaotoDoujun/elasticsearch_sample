FROM python:3.8
WORKDIR /app

RUN apt-get update && apt-get install -y cron supervisor vim && apt-get clean all

# PAM
RUN sed -i -e '/pam_loginuid.so/s/^/#/' /etc/pam.d/cron

# install scrapy, scrapy_splash and ScrapyElasticSearch
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install Pillow==9.1.1 Scrapy==2.6.1 scrapy-splash==0.8.0 ScrapyElasticSearch==0.9.2

# copy conf
COPY supervisord.conf /etc/supervisor/conf.d/

# copy sample_crawler
COPY sample_crawler .

CMD ["/usr/bin/supervisord"]