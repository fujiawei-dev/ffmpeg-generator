# This is a contributed example of how to build ffmpeg-gl-transions using Docker
# If you use Docker, this should get the job done
# if you don't use Docker, you could still run the commands
# manually and get the same result

# docker build -t rustlekarl/ffmpeg-generator:latest .
FROM rustlekarl/ffmpeg-gltransition:latest

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

WORKDIR /root

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /generator

COPY . /generator

RUN (cd /generator; python run_examples.py)

RUN rm -rf /generator/* && rm -rf /var/lib/apt/lists/* && apt-get -y purge

# Overlay parent's ENTRYPOINT
RUN echo "#!/bin/bash\nXvfb -ac :1 -screen 0 1280x1024x16 > /dev/null 2>&1" > /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
