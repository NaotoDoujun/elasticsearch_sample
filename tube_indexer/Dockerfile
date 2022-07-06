FROM python:3.8
WORKDIR /app

RUN apt-get update && apt-get install -y busybox-static libsndfile1 ffmpeg && apt-get clean all

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt --no-cache-dir

# crawl schedule every hour
RUN mkdir -p /var/spool/cron/crontabs/ \
  && echo '0 */1 * * * cd /app && python3 main.py' > /var/spool/cron/crontabs/root

# copy
COPY . .

ENTRYPOINT ["busybox", "crond", "-f", "-L", "/dev/stderr"]