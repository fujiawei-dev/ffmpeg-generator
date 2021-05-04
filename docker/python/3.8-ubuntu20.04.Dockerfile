# Docker file for a slim Ubuntu:20.04-based Python3.8 image
# docker build -t rustlekarl/python:3.8-ubuntu20.04 -t rustlekarl/python:latest -f docker/python/3.8-ubuntu20.04.Dockerfile .
FROM ubuntu:20.04

MAINTAINER rustlekarl "rustlekarl@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n" >/etc/apt/sources.list
RUN echo "[global]\nindex-url=http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com" > /etc/pip.conf

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && ln -s /usr/bin/pip3 pip \
  && pip3 --no-cache-dir install --upgrade pip

RUN rm -rf /var/lib/apt/lists/* && apt-get -y purge

# drop you into a shell to look around
# modify as needed for actual use
RUN echo "#!/bin/bash\n/bin/bash" > /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
