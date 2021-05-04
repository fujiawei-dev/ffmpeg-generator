# docker build -t rustlekarl/ffmpeg-golang:latest -t rustlekarl/ffmpeg-golang:ubuntu-focal -f golang.Dockerfile .

FROM lsiobase/ffmpeg:bin as binstage
FROM lsiobase/ubuntu:focal

MAINTAINER rustlekarl

# Add files from binstage
COPY --from=binstage / /

ARG DEBIAN_FRONTEND=noninteractive

# hardware env
ENV \
 LIBVA_DRIVERS_PATH="/usr/lib/x86_64-linux-gnu/dri" \
 NVIDIA_DRIVER_CAPABILITIES="compute,video,utility" \
 NVIDIA_VISIBLE_DEVICES="all"

ENV TZ="Asia/Shanghai"

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n" >/etc/apt/sources.list

# update anything needed
RUN apt-get -y update && apt-get -y upgrade

# need dep
RUN \
 echo "**** install runtime ****" && \
 apt-get install -y \
	i965-va-driver \
	libexpat1 \
	libgl1-mesa-dri \
	libglib2.0-0 \
	libgomp1 \
	libharfbuzz0b \
	libv4l-0 \
	libx11-6 \
	libxcb1 \
	libxext6 \
	libxml2

# golang
RUN apt-get -y install golang-go make

RUN go env -w GOPROXY=https://goproxy.cn,direct && go env -w GOSUMDB=off && go env -w GO111MODULE=on

RUN \
 echo "**** clean up ****" && \
 rm -rf \
	/var/lib/apt/lists/* \
	/var/tmp/*

# Set up project directory
WORKDIR "/ffmpeg"

CMD /bin/bash
