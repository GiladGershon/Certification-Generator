# syntax=docker/dockerfile:1

FROM python:3.9.13

WORKDIR /cert-gen-app 

RUN curl -s -o redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz
RUN mkdir -p /usr/local/lib/
RUN chmod a+w /usr/local/lib/
RUN tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
RUN rm redis-stable.tar.gz
RUN cd /usr/local/lib/redis-stable/ && make && make install
COPY 6379.conf /usr/local/etc/redis/6379.conf
RUN redis-server /usr/local/etc/redis/6379.conf



COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update 
RUN apt-get install default-jre -y
RUN apt-get install libreoffice --no-install-recommends -y

COPY  . .


CMD ["python", "run.py" , "webapp"]




