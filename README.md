<!--
 * @Date: 2021.02.30 17:30:51
 * @LastEditors: Rustle Karl
 * @LastEditTime: 2021.05.25 08:27:32
-->

# FFmpeg Generator

> A FFmpeg command generator and actuator.

Python bindings for FFmpeg - with almost all filters support, even `gltransition` filter.

- [FFmpeg Generator](#ffmpeg-generator)
  - [Overview](#overview)
  - [TODO](#todo)
  - [Installation](#installation)
  - [Documents](#documents)
  - [GLTransition Filter](#gltransition-filter)
  - [Video Sources](#video-sources)
    - [Play by FFplay](#play-by-ffplay)
    - [Preview by FFmpeg](#preview-by-ffmpeg)
    - [Save Video from video sources](#save-video-from-video-sources)
  - [More Examples](#more-examples)
    - [Get Stream Info](#get-stream-info)
    - [Play a Video](#play-a-video)
    - [Generate Thumbnail for Video](#generate-thumbnail-for-video)
    - [Convert Video to Numpy Array](#convert-video-to-numpy-array)
    - [Read Single Video Frame as JPEG](#read-single-video-frame-as-jpeg)
    - [Convert Sound to Raw PCM Audio](#convert-sound-to-raw-pcm-audio)
    - [Assemble Video from Sequence of Frames](#assemble-video-from-sequence-of-frames)
    - [Audio/Video Pipeline](#audiovideo-pipeline)
    - [Mono to Stereo with Offsets and Video](#mono-to-stereo-with-offsets-and-video)
    - [Process Frames](#process-frames)
    - [FaceTime Webcam Input](#facetime-webcam-input)
    - [Stream from a Local Video to HTTP Server](#stream-from-a-local-video-to-http-server)
    - [Stream from RTSP Server to TCP Socket](#stream-from-rtsp-server-to-tcp-socket)
  - [Special Thanks](#special-thanks)

## Overview

This project is based on [`ffmpeg-python`](https://github.com/kkroening/ffmpeg-python). But rewrite all.

- support video sources
- support almost all filters
- support FFplay&FFprobe
- enable cuda hwaccel by default, or close globally by code below

```python
from ffmpeg import settings

settings.CUDA_ENABLE = False
```

## Installation

```shell
pip install -U ffmpeg-generator
```

## Documents

FFmpeg comes with more than 450 audio and video media filters. 
It is recommended to read the official documentation.

- [FFmpeg Homepage](https://ffmpeg.org/)
- [FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)
- [FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)

Or read my study notes, plan to demonstrate all the filters, but written in Chinese. Not all done yet.

- [All Examples for Audio Filters](docs/afilters.md)
- [All Examples for Video Filters](docs/vfilters.md)
- [All Examples for Audio/Video Sources](docs/sources.md)
- [All Examples for Media Filters](docs/avfilters.md)
- [Introduce Usage of FFplay](docs/ffplay.md)
- [More Notes](https://github.com/studying-notes/ffmpeg-notes)

## GLTransition Filter

```python
from ffmpeg import avfilters, input, vfilters, vtools
from ffmpeg.transitions import GLTransition, GLTransitionAll
from tests import data

# OpenGL Transition

"""Combine two videos with transition effects."""

for e in GLTransitionAll:
    vtools.concat_2_videos_with_gltransition(data.TEST_OUTPUTS_DIR / (e + ".mp4"),
                                             data.SHORT0, data.SHORT1, offset=1,
                                             duration=2, source=eval("transitions." + e))

"""Combine multiple videos with transition effects."""

in0 = input(data.SHORT0).video
in1 = input(data.SHORT1).video
in2 = input(data.SHORT2).video

in0_split = in0.split()
in0_0, in0_1 = in0_split[0], in0_split[1]
in0_0 = in0_0.trim(start=0, end=3)
in0_1 = in0_1.trim(start=3, end=4).setpts()

in1_split = in1.split()
in1_0, in1_1 = in1_split[0], in1_split[1]
in1_0 = in1_0.trim(start=0, end=3)
in1_1 = in1_1.trim(start=3, end=4).setpts()

in2_split = in2.split()
in2_0, in2_1 = in2_split[0], in2_split[1]
in2_0 = in2_0.trim(start=0, end=3)
in2_1 = in2_1.trim(start=3, end=4).setpts()

gl0_1 = vfilters.gltransition(in0_1, in1_0, source=GLTransition.Angular)
gl1_2 = vfilters.gltransition(in1_1, in2_0, source=GLTransition.ButterflyWaveScrawler)

# transition
_ = avfilters.concat(in0_0, gl0_1, gl1_2, in2_1).output(
        data.TEST_OUTPUTS_DIR / "3_transition.mp4",
        vcodec="libx264",
        v_profile="baseline",
        preset="slow",
        movflags="faststart",
        pixel_format="yuv420p",
).run()

# transition + image watermark
v_input = avfilters.concat(in0_0, gl0_1, gl1_2, in2_1)
i_input = input(data.I1).scale(w=100, h=100)
v_input.overlay(i_input, x=30, y=30).output(
        data.TEST_OUTPUTS_DIR / "3_transition_image.mp4",
        vcodec="libx264",
        v_profile="baseline",
        preset="slow",
        movflags="faststart",
        pixel_format="yuv420p",
).run()

# transition + image watermark + text watermark
v_input = avfilters.concat(in0_0, gl0_1, gl1_2, in2_1). \
    drawtext(text="Watermark", x=150, y=150, fontsize=36, fontfile=data.FONT1)
i_input = input(data.I1).scale(w=100, h=100)
v_input.overlay(i_input, x=30, y=30).output(
        data.TEST_OUTPUTS_DIR / "3_transition_image_text.mp4",
        vcodec="libx264",
        v_profile="baseline",
        preset="slow",
        movflags="faststart",
        pixel_format="yuv420p",
).run()

# transition + image watermark + text watermark + music
v_input = avfilters.concat(in0_0, gl0_1, gl1_2, in2_1). \
    drawtext(text="Watermark", x=150, y=150, fontsize=36, fontfile=data.FONT1)
i_input = input(data.I1).scale(w=100, h=100)
a_input = input(data.A1).audio
v_input.overlay(i_input, x=30, y=30).output(
        a_input,
        data.TEST_OUTPUTS_DIR / "3_transition_image_text_music.mp4",
        acodec="copy",
        vcodec="libx264",
        v_profile="baseline",
        shortest=True,
        preset="slow",
        movflags="faststart",
        pixel_format="yuv420p",
).run()
```

## Video Sources

### Play by FFplay

```python
from ffmpeg import run_ffplay

_ = run_ffplay("allrgb", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("color=c=red@0.2:s=1600x900:r=10", f="lavfi")
_ = run_ffplay("haldclutsrc", f="lavfi")
_ = run_ffplay("pal75bars", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("rgbtestsrc=size=900x600:rate=60", f="lavfi")
_ = run_ffplay("smptebars=size=900x600:rate=60", f="lavfi")
_ = run_ffplay("smptehdbars=size=900x600:rate=60", f="lavfi")
_ = run_ffplay("testsrc=size=900x600:rate=60", f="lavfi")
_ = run_ffplay("testsrc2=s=900x600:rate=60", f="lavfi")
_ = run_ffplay("yuvtestsrc=s=900x600:rate=60", f="lavfi")
```

### Preview by FFmpeg

```python
from ffmpeg import input_source

_ = input_source("testsrc", size="900x600", rate=60).output(preview=True).run_async()
_ = input_source("testsrc2", size="900x600", rate=60).output(preview=True).run_async()
```

### Save Video from video sources

```python
from ffmpeg import input_source

_ = input_source("testsrc", size="900x600", rate=60, duration=30).output("source_testsrc.mp4").run()
```

## More Examples

### Get Stream Info

```python
from ffmpeg import FFprobe

meta = FFprobe("path/to/file")

# all stream
print(meta.metadata)

# video stream
print(meta.video)
print(meta.video_duration)
print(meta.video_scale)

# audio stream
print(meta.audio)
print(meta.audio_duration)
```

### Play a Video

```python
from ffmpeg import ffplay_video
from tests import data

ffplay_video(data.V1, vf='transpose=1')
ffplay_video(data.V1, vf='hflip')
ffplay_video(data.V1, af='atempo=2')
ffplay_video(data.V1, vf='setpts=PTS/2')
ffplay_video(data.V1, vf='transpose=1,setpts=PTS/2', af='atempo=2')
```

### Generate Thumbnail for Video

```python
from ffmpeg import vtools

vtools.generate_video_thumbnail(src="src", dst="dst", start_position=3, width=400, height=-1)
```

### Convert Video to Numpy Array

```python
from ffmpeg import vtools

vtools.convert_video_to_np_array(src="src")
```

### Read Single Video Frame as JPEG

```python
from ffmpeg import vtools

vtools.read_frame_as_jpeg(src="src", frame=10)
```

### Convert Sound to Raw PCM Audio

```python
from ffmpeg import atools

audio = '/path/to/audio.m4a'
dst = '/path/to/dst.pcm'

atools.convert_audio_to_raw_pcm(src=audio, dst=None)
atools.convert_audio_to_raw_pcm(src=audio, dst=dst)
```

### Assemble Video from Sequence of Frames

```python
from ffmpeg import vtools

# on Linux
vtools.assemble_video_from_images('/path/to/jpegs/*.jpg', pattern_type='glob', frame_rate=25)

# on Windows
vtools.assemble_video_from_images('/path/to/jpegs/%02d.jpg', pattern_type=None, frame_rate=25)
```

> https://stackoverflow.com/questions/31201164/ffmpeg-error-pattern-type-glob-was-selected-but-globbing-is-not-support-ed-by

With additional filtering:

```python
import ffmpeg

ffmpeg.input('/path/to/jpegs/*.jpg', pattern_type='glob', framerate=25). \
    filter('deflicker', mode='pm', size=10). \
    filter('scale', size='hd1080', force_original_aspect_ratio='increase'). \
    output('movie.mp4', crf=20, preset='slower', movflags='faststart', pix_fmt='yuv420p'). \
    view(save_path='filter_graph').run()
```

### Audio/Video Pipeline

```python
import ffmpeg
from ffmpeg import avfilters

in1 = ffmpeg.input("input.mp4")
in2 = ffmpeg.input("input.mp4")

v1 = in1.video.hflip()
a1 = in2.audio

v2 = in2.video.reverse().hue(s=0)
a2 = in2.audio.areverse().aphaser()

joined = avfilters.concat(v1, a1, v2, a2, v=1, a=1).Node

v3 = joined[0]
a3 = joined[1].volume(0.8)

v3.output(a3, 'v1_v2_pipeline.mp4').run()
```

### Mono to Stereo with Offsets and Video

```python
import ffmpeg
from ffmpeg import afilters
from tests import data

input_video = ffmpeg.input(data.V1)
audio_left = ffmpeg.input(data.A1).atrim(start=15).asetpts("PTS-STARTPTS")
audio_right = ffmpeg.input(data.A1).atrim(start=10).asetpts("PTS-STARTPTS")

afilters.join(audio_left, audio_right, inputs=2, channel_layout="stereo"). \
    output(input_video.video, "stereo_video.mp4", shortest=None, vcodec="copy").run()
```

### Process Frames

- Decode input video with ffmpeg
- Process each video frame with python
- Encode output video with ffmpeg

```python
import subprocess

import numpy as np

from ffmpeg import constants, FFprobe, input, settings
from tests import data

settings.CUDA_ENABLE = False


def ffmpeg_input_process(src):
    return input(src).output(constants.PIPE, format="rawvideo",
                             pixel_format="rgb24").run_async(pipe_stdout=True)


def ffmpeg_output_process(dst, width, height):
    return input(constants.PIPE, format="rawvideo", pixel_format="rgb24",
                 width=width, height=height).output(dst, pixel_format="yuv420p"). \
        run_async(pipe_stdin=True)


def read_frame_from_stdout(process: subprocess.Popen, width, height):
    frame_size = width * height * 3
    input_bytes = process.stdout.read(frame_size)

    if not input_bytes:
        return

    assert len(input_bytes) == frame_size

    return np.frombuffer(input_bytes, np.uint8).reshape([height, width, 3])


def process_frame_simple(frame):
    # deep dream
    return frame * 0.3


def write_frame_to_stdin(process: subprocess.Popen, frame):
    process.stdin.write(frame.astype(np.uint8).tobytes())


def run(src, dst, process_frame):
    width, height = FFprobe(src).video_scale

    input_process = ffmpeg_input_process(src)
    output_process = ffmpeg_output_process(dst, width, height)

    while True:
        input_frame = read_frame_from_stdout(input_process, width, height)

        if input_frame is None:
            break

        write_frame_to_stdin(output_process, process_frame(input_frame))

    input_process.wait()

    output_process.stdin.close()
    output_process.wait()


if __name__ == '__main__':
    run(data.SHORT0, data.TEST_OUTPUTS_DIR / "process_frame.mp4", process_frame_simple)
```

### FaceTime Webcam Input

```python
import ffmpeg

def facetime():
    ffmpeg.input("FaceTime", format="avfoundation",
                 pixel_format="uyvy422", framerate=30). \
        output("facetime.mp4", pixel_format="yuv420p", frame_size=100).run()
```

### Stream from a Local Video to HTTP Server

```python
from ffmpeg import input

input("video.mp4").output("http://127.0.0.1:8080",
                      codec="copy",  # use same codecs of the original video
                      listen=1,  # enables HTTP server
                      f="flv").\
    with_global_args("-re").\
    run()  # argument to act as a live stream
```

To receive the video you can use ffplay in the terminal:

```shell
ffplay -f flv http://localhost:8080
```

### Stream from RTSP Server to TCP Socket

```python
import socket
from ffmpeg import input

server = socket.socket()
process = input('rtsp://%s:8554/default').\
    output('-', format='h264').\
    run_async(pipe_stdout=True)

while process.poll() is None:
    packet = process.stdout.read(4096)
    try:
        server.send(packet)
    except socket.error:
        process.stdout.close()
        process.wait()
        break
```

## Special Thanks

- [The FFmpeg-Python Project](https://github.com/kkroening/ffmpeg-python)
