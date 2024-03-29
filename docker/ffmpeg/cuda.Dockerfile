# docker build -t rustlekarl/ffmpeg-gpu:latest -t rustlekarl/ffmpeg-gpu:ubuntu20.04-cuda11.2.1 -f cuda.Dockerfile .
# Docker on Windows unsupports cuda.

FROM nvidia/cuda:11.2.1-base-ubuntu20.04

MAINTAINER rustlekarl

RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n" >/etc/apt/sources.list

RUN apt update && apt install -y ffmpeg

WORKDIR /ffmpeg

ARG NGINX_VERSION=1.18.0
ARG NGINX_RTMP_VERSION=1.2.1
ARG FFMPEG_VERSION=4.3.1


##############################
# Build the NGINX-build image.
FROM ubuntu:18.04 as build-nginx
ARG NGINX_VERSION
ARG NGINX_RTMP_VERSION

# Build dependencies.
RUN apt update && apt install -y \
  build-essential \
  cmake \
  ca-certificates \
  curl \
  gcc \
  libc-dev \
  make \
  musl-dev \
  openssl \
  libssl-dev \
  libpcre3 \
  libpcre3-dev \
  pkg-config \
  zlib1g-dev \
  wget

# Get nginx source.
RUN cd /tmp && \
  wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
  tar zxf nginx-${NGINX_VERSION}.tar.gz && \
  rm nginx-${NGINX_VERSION}.tar.gz

# Get nginx-rtmp module.
RUN cd /tmp && \
  wget https://github.com/arut/nginx-rtmp-module/archive/v${NGINX_RTMP_VERSION}.tar.gz && \
  tar zxf v${NGINX_RTMP_VERSION}.tar.gz && rm v${NGINX_RTMP_VERSION}.tar.gz

# Compile nginx with nginx-rtmp module.
RUN cd /tmp/nginx-${NGINX_VERSION} && \
  ./configure \
  --prefix=/usr/local/nginx \
  --add-module=/tmp/nginx-rtmp-module-${NGINX_RTMP_VERSION} \
  --conf-path=/etc/nginx/nginx.conf \
  --with-threads \
  --with-file-aio \
  --with-http_ssl_module \
  --with-debug \
  --with-cc-opt="-Wimplicit-fallthrough=0" && \
  cd /tmp/nginx-${NGINX_VERSION} && make && make install

###############################
# Build the FFmpeg-build image.
FROM nvidia/cuda:11.1-devel-ubuntu20.04 as build-ffmpeg

ENV DEBIAN_FRONTEND=noninteractive
ARG FFMPEG_VERSION
ARG PREFIX=/usr/local
ARG MAKEFLAGS="-j4"

# FFmpeg build dependencies.
RUN apt update && apt install -y \
  build-essential \
  coreutils \
  cmake \
  libx264-dev \
  libx265-dev \
  libc6 \
  libc6-dev \
  libfreetype6-dev \
  libfdk-aac-dev \
  libmp3lame-dev \
  libogg-dev \
  libass9 \
  libass-dev \
  libnuma1 \
  libnuma-dev \
  libopus-dev \
  librtmp-dev \
  libvpx-dev \
  libvorbis-dev \
  libwebp-dev \
  libtheora-dev \
  libtool \
  libssl-dev \
  pkg-config \
  wget \
  yasm \
  git

# Clone and install ffnvcodec
RUN cd /tmp && git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git && \
  cd nv-codec-headers && make install

# Get FFmpeg source.
RUN cd /tmp/ && \
  wget http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
  tar zxf ffmpeg-${FFMPEG_VERSION}.tar.gz && rm ffmpeg-${FFMPEG_VERSION}.tar.gz

# Compile ffmpeg.
RUN cd /tmp/ffmpeg-${FFMPEG_VERSION} && \
  ./configure \
  --prefix=${PREFIX} \
  --enable-version3 \
  --enable-gpl \
  --enable-nonfree \
  --enable-small \
  --enable-libfdk-aac \
  --enable-openssl \
  --enable-libnpp \
  --enable-cuda \
  --enable-cuvid \
  --enable-nvenc \
  --enable-libnpp \
  --disable-debug \
  --disable-doc \
  --disable-ffplay \
  --extra-cflags=-I/usr/local/cuda/include \
  --extra-ldflags=-L/usr/local/cuda/lib64 \
  --extra-libs="-lpthread -lm" && \
  make && make install && make distclean

# Cleanup.
RUN rm -rf /var/cache/* /tmp/*

##########################
# Build the release image.
FROM nvidia/cuda:11.1-runtime-ubuntu20.04
LABEL MAINTAINER Alfred Gutierrez <alf.g.jr@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_DRIVER_VERSION=455
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,video,utility

# Set default ports.
ENV HTTP_PORT 80
ENV HTTPS_PORT 443
ENV RTMP_PORT 1935

# Set default options.
ENV SINGLE_STREAM ""
ENV MAX_MUXING_QUEUE_SIZE ""
ENV ANALYZEDURATION ""

RUN apt update && apt install -y --no-install-recommends \
  ca-certificates \
  curl \
  gettext \
  libpcre3-dev \
  libnvidia-decode-${NVIDIA_DRIVER_VERSION} \
  libnvidia-encode-${NVIDIA_DRIVER_VERSION} \
  libtheora0 \
  openssl \
  rtmpdump

COPY --from=build-nginx /usr/local/nginx /usr/local/nginx
COPY --from=build-nginx /etc/nginx /etc/nginx
COPY --from=build-ffmpeg /usr/local /usr/local
COPY --from=build-ffmpeg /usr/lib/x86_64-linux-gnu/libfdk-aac.so.1 /usr/lib/x86_64-linux-gnu/libfdk-aac.so.1

# Add NGINX path, config and static files.
ENV PATH "${PATH}:/usr/local/nginx/sbin"
RUN mkdir -p /opt/data && mkdir /www
ADD nginx-cuda.conf /etc/nginx/nginx.conf.template
ADD entrypoint.cuda.sh /opt/entrypoint.sh
RUN chmod gu+x /opt/entrypoint.sh
ADD static /www/static

EXPOSE 1935
EXPOSE 80

CMD /opt/entrypoint.sh
