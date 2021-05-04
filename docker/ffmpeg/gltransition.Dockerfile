# This is a contributed example of how to build ffmpeg-gl-transions using Docker
# If you use Docker, this should get the job done
# if you don't use Docker, you could still run the commands
# manually and get the same result

# docker build -t rustlekarl/ffmpeg-gltransition:n4.3.2-20210303 -t rustlekarl/ffmpeg-gltransition:latest -f docker/ffmpeg/gltransition.Dockerfile .
FROM ubuntu:20.04

MAINTAINER rustlekarl "rustlekarl@gmail.com"

ENV FFMPEG_VERSION "n4.3.2"

# everything is relative to /build
WORKDIR /build

# enable contrib/non-free
RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n" >/etc/apt/sources.list

ARG DEBIAN_FRONTEND=noninteractive

RUN export TZ=Asia/Shanghai

# update anything needed
RUN apt-get -y update && apt-get -y upgrade

# need dep
RUN apt-get -y install git \
                            apt-utils \
                            autoconf \
                            automake \
                            build-essential \
                            cmake \
                            g++ \
                            gcc \
                            git-core \
                            libass-dev \
                            libfdk-aac-dev \
                            libfreetype6-dev \
                            libglew-dev \
                            libglfw3-dev \
                            libglu1-mesa-dev \
                            libgnutls28-dev \
                            libmp3lame-dev \
                            libopus-dev \
                            libsdl2-dev \
                            libtheora-dev \
                            libtool \
                            libva-dev \
                            libvdpau-dev \
                            libvorbis-dev \
                            libvpx-dev \
                            libx264-dev \
                            libx265-dev \
                            libxcb-shm0-dev \
                            libxcb-xfixes0-dev \
                            libxcb1-dev \
                            libxvidcore-dev \
                            make \
                            nasm \
                            pkg-config \
                            texinfo \
                            wget \
                            xorg-dev \
                            yasm \
                            zlib1g-dev \
                            gperf \
                            libglew2.1

# get ffmpeg sources
RUN (cd /build; git clone -b "$FFMPEG_VERSION" https://gitee.com/fujiawei/FFmpeg.git ffmpeg)

# get ffmpeg-gl-transition modifications
# this pulls from the original master for standalone use
# but you could modify to copy from your clone/repository
RUN (cd /build; git clone https://gitee.com/fujiawei/ffmpeg-gl-transition.git; cd ffmpeg-gl-transition; git clone https://gitee.com/fujiawei/gl-transitions.git; cd /build/ffmpeg; git apply /build/ffmpeg-gl-transition/ffmpeg.diff; grep -v "define GL_TRANSITION_USING_EGL" /build/ffmpeg-gl-transition/vf_gltransition.c > /build/ffmpeg/libavfilter/vf_gltransition.c)

RUN (cd /build; git clone https://gitee.com/fujiawei/libass.git)

RUN (cd /build; git clone https://gitee.com/fujiawei/mirror.git)

RUN (cd /build; mv /build/mirror/freetype-2.10.4.tar.xz  /build/freetype-2.10.4.tar.xz; tar -xf freetype-2.10.4.tar.xz; cd freetype-2.10.4; ./configure --prefix=/usr --enable-freetype-config --disable-static; make; make install)

RUN (cd /build; mv /build/mirror/fribidi-1.0.9.tar.xz /build/fribidi-1.0.9.tar.xz; tar -xf fribidi-1.0.9.tar.xz; cd fribidi-1.0.9; ./configure --prefix=/usr; make; make install)

RUN (cd /build; mv /build/mirror/nasm-2.15.05.tar.xz /build/nasm-2.15.05.tar.xz; tar -xf nasm-2.15.05.tar.xz; cd nasm-2.15.05; ./configure --prefix=/usr; make; make install)

RUN (cd /build; mv /build/mirror/fontconfig-2.13.1.tar.bz2 /build/fontconfig-2.13.1.tar.bz2; tar -xf fontconfig-2.13.1.tar.bz2; cd fontconfig-2.13.1; rm -f src/fcobjshash.h; ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --disable-docs --docdir=/usr/share/doc/fontconfig-2.13.1; make; make install)

RUN (cd /build/libass; sh autogen.sh; ./configure --prefix=/usr --disable-static; make; make install)

ENV PKG_CONFIG_PATH=/usr/local/ass/lib/pkgconfig:$PKG_CONFIG_PATH

RUN (cd /build; git clone --depth=1 https://gitee.com/fujiawei/SVT-AV1; cd SVT-AV1; cd Build; cmake .. -G"Unix Makefiles" -DCMAKE_BUILD_TYPE=Release; make install)

# RUN (cd /build; git clone https://gitee.com/fujiawei/x264.git; cd x264; ./configure --prefix=/usr --enable-static --enable-shared; make && make install)

# configure/compile/install ffmpeg
RUN (cd /build/ffmpeg; ./configure --enable-gnutls --enable-gpl --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-libxvid --enable-nonfree --enable-opengl --enable-filter=gltransition --extra-libs='-lGLEW -lglfw -ldl')

# the -j speeds up compilation, but if your container host is limited on resources, you may need to remove it to force a non-parallel build to avoid memory usage issues
RUN (cd /build/ffmpeg; make -j && make install)

# needed for running it
RUN apt-get -y install xvfb

# try the demo
RUN (cd ffmpeg-gl-transition; ln -s /usr/local/bin/ffmpeg .)
RUN (cd ffmpeg-gl-transition; xvfb-run --auto-servernum -s '+iglx -screen 0 1920x1080x24' bash concat.sh)
# result would be in out.mp4 in that directory

#COPY testdata /build/testdata
#
#RUN (cd /build/testdata; ln -s /usr/local/bin/ffmpeg .)
#RUN (cd /build/testdata; bash test_drawtext.sh; bash test_libx264.sh)
#RUN (cd /build/testdata; xvfb-run --auto-servernum -s '+iglx -screen 0 1920x1080x24' bash test_gltransition.sh)

RUN rm -rf /build
RUN rm -rf /var/lib/apt/lists/* && apt-get -y purge

WORKDIR /root

# drop you into a shell to look around
# modify as needed for actual use
RUN echo "#!/bin/bash\nnohup Xvfb -ac :1 -screen 0 1280x1024x16 > /dev/null 2>&1 &\n/bin/bash" > /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV DISPLAY=:1

ENTRYPOINT ["/entrypoint.sh"]
