FROM python:3
WORKDIR /app

RUN apt-get update && apt-get install -y cron supervisor vim && apt-get clean all

# PAM
RUN sed -i -e '/pam_loginuid.so/s/^/#/' /etc/pam.d/cron

# install scrapy, scrapy_splash and ScrapyElasticSearch
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pillow scrapy scrapy_splash ScrapyElasticSearch

# copy conf
COPY supervisord.conf /etc/supervisor/conf.d/

CMD ["/usr/bin/supervisord"]