<!--
 * @Date: 2021.03.25T14:18:00+08:00
 * @Description: FFmpeg Media Filters
 * @LastEditors: Rustle Karl
 * @LastEditTime: 2021.05.10 12:35:58
-->

- [abitscope](#abitscope)
  - [参数](#参数)
  - [示例](#示例)
    - [对比](#对比)
- [adrawgraph](#adrawgraph)
  - [参数](#参数-1)
  - [示例](#示例-1)
    - [对比](#对比-1)
- [agraphmonitor](#agraphmonitor)
  - [参数](#参数-2)
  - [示例](#示例-2)
    - [对比](#对比-2)
- [ahistogram](#ahistogram)
  - [参数](#参数-3)
  - [示例](#示例-3)
    - [对比](#对比-3)
- [aphasemeter](#aphasemeter)
  - [参数](#参数-4)
  - [示例](#示例-4)
    - [对比](#对比-4)
- [avectorscope](#avectorscope)
  - [参数](#参数-5)
  - [示例](#示例-5)
    - [对比](#对比-5)
- [bench](#bench)
  - [参数](#参数-6)
  - [示例](#示例-6)
    - [对比](#对比-6)
- [abench](#abench)
  - [参数](#参数-7)
  - [示例](#示例-7)
    - [对比](#对比-7)
- [concat](#concat)
  - [参数](#参数-8)
  - [示例](#示例-8)
- [ebur128](#ebur128)
  - [参数](#参数-9)
  - [示例](#示例-9)
    - [对比](#对比-8)
- [interleave](#interleave)
  - [参数](#参数-10)
  - [示例](#示例-10)
    - [对比](#对比-9)
- [ainterleave](#ainterleave)
  - [参数](#参数-11)
  - [示例](#示例-11)
    - [对比](#对比-10)
- [metadata](#metadata)
  - [参数](#参数-12)
  - [示例](#示例-12)
    - [对比](#对比-11)
- [ametadata](#ametadata)
  - [参数](#参数-13)
  - [示例](#示例-13)
    - [对比](#对比-12)
- [perms](#perms)
  - [参数](#参数-14)
  - [示例](#示例-14)
    - [对比](#对比-13)
- [aperms](#aperms)
  - [参数](#参数-15)
  - [示例](#示例-15)
    - [对比](#对比-14)
- [realtime](#realtime)
  - [参数](#参数-16)
  - [示例](#示例-16)
    - [对比](#对比-15)
- [arealtime](#arealtime)
  - [参数](#参数-17)
  - [示例](#示例-17)
    - [对比](#对比-16)
- [select](#select)
  - [参数](#参数-18)
  - [示例](#示例-18)
    - [对比](#对比-17)
- [aselect](#aselect)
  - [参数](#参数-19)
  - [示例](#示例-19)
    - [对比](#对比-18)
- [sendcmd](#sendcmd)
  - [参数](#参数-20)
  - [示例](#示例-20)
    - [对比](#对比-19)
- [asendcmd](#asendcmd)
  - [参数](#参数-21)
  - [示例](#示例-21)
    - [对比](#对比-20)
- [setpts, asetpts](#setpts-asetpts)
  - [参数](#参数-22)
  - [示例](#示例-22)
    - [从 0 开始计数 PTS](#从-0-开始计数-pts)
    - [对比](#对比-21)
    - [加速播放效果](#加速播放效果)
    - [对比](#对比-22)
    - [减速播放效果](#减速播放效果)
    - [对比](#对比-23)
    - [强制为 25 的帧率](#强制为-25-的帧率)
    - [对比](#对比-24)
    - [设置有抖动的 25 帧率](#设置有抖动的-25-帧率)
    - [对比](#对比-25)
    - [应用一个 10 秒的输入偏置](#应用一个-10-秒的输入偏置)
    - [对比](#对比-26)
    - [从`直播源`和变基生成时间戳转换到当前时基时间戳](#从直播源和变基生成时间戳转换到当前时基时间戳)
    - [对比](#对比-27)
    - [按当前采样率生成时间戳](#按当前采样率生成时间戳)
    - [对比](#对比-28)
- [setrange](#setrange)
  - [参数](#参数-23)
  - [示例](#示例-23)
    - [对比](#对比-29)
- [settb](#settb)
  - [参数](#参数-24)
  - [示例](#示例-24)
    - [对比](#对比-30)
- [asettb](#asettb)
  - [参数](#参数-25)
  - [示例](#示例-25)
    - [对比](#对比-31)
- [showcqt](#showcqt)
  - [参数](#参数-26)
  - [示例](#示例-26)
    - [对比](#对比-32)
- [showfreqs](#showfreqs)
  - [参数](#参数-27)
  - [示例](#示例-27)
    - [对比](#对比-33)
- [showspatial](#showspatial)
  - [参数](#参数-28)
  - [示例](#示例-28)
    - [对比](#对比-34)
- [showspectrum](#showspectrum)
  - [参数](#参数-29)
  - [示例](#示例-29)
    - [对比](#对比-35)
- [showspectrumpic](#showspectrumpic)
  - [参数](#参数-30)
  - [示例](#示例-30)
    - [对比](#对比-36)
- [showvolume](#showvolume)
  - [参数](#参数-31)
  - [示例](#示例-31)
    - [对比](#对比-37)
- [showwaves](#showwaves)
  - [参数](#参数-32)
  - [示例](#示例-32)
    - [对比](#对比-38)
- [showwavespic](#showwavespic)
  - [参数](#参数-33)
  - [示例](#示例-33)
    - [对比](#对比-39)
- [sidedata](#sidedata)
  - [参数](#参数-34)
  - [示例](#示例-34)
    - [对比](#对比-40)
- [asidedata](#asidedata)
  - [参数](#参数-35)
  - [示例](#示例-35)
    - [对比](#对比-41)
- [spectrumsynth](#spectrumsynth)
  - [参数](#参数-36)
  - [示例](#示例-36)
    - [对比](#对比-42)
- [split](#split)
  - [参数](#参数-37)
  - [示例](#示例-37)
    - [对比](#对比-43)
- [asplit](#asplit)
  - [参数](#参数-38)
  - [示例](#示例-38)
    - [对比](#对比-44)
- [zmq](#zmq)
  - [参数](#参数-39)
  - [示例](#示例-39)
    - [对比](#对比-45)
- [azmq](#azmq)
  - [参数](#参数-40)
  - [示例](#示例-40)
    - [对比](#对比-46)
- [amovie](#amovie)
  - [参数](#参数-41)
  - [示例](#示例-41)
    - [对比](#对比-47)
- [movie](#movie)
  - [参数](#参数-42)
  - [示例](#示例-42)
    - [对比](#对比-48)

## abitscope

> https://ffmpeg.org/ffmpeg-filters.html#abitscope


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## adrawgraph

> https://ffmpeg.org/ffmpeg-filters.html#adrawgraph


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## agraphmonitor

> https://ffmpeg.org/ffmpeg-filters.html#agraphmonitor


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ahistogram

> https://ffmpeg.org/ffmpeg-filters.html#ahistogram


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## aphasemeter

> https://ffmpeg.org/ffmpeg-filters.html#aphasemeter


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## avectorscope

> https://ffmpeg.org/ffmpeg-filters.html#avectorscope


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## bench

> https://ffmpeg.org/ffmpeg-filters.html#bench


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## abench

> https://ffmpeg.org/ffmpeg-filters.html#abench


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## concat

> https://ffmpeg.org/ffmpeg-filters.html#concat

连接音频和视频流，把加入的媒体一个接一个的在一起。这个滤镜用于按段同步视频和音频流。所有的段都必须有相同的流（类型和个数），输出也是相同流（类型和个数）。

### 参数

- n 设置段的数量，默认为 2
- v 设置输出中视频流数量，则每个段中必须有输入视频流的数量。默认为 1
- a 设置输出中音频流数量，则每个段中必须有输入音频流的数量，默认为 0
- unsafe 激活不安全模式，这时如果段中有不同格式不会失败

滤镜有 `v+a` 个输出：先是一个视频输出，然后是音频输出。

有 `n x (v+a)`：有n段输出，每段都是 `v+a`。

相关的流并不总是有相同的时间，由于各种原因还包括不同的编解码帧大小或创作草稿。因此相关同步流（视频和对应音频）要连接，`concat` 滤镜将选择持续最长的流（视频的）为基准（除最后段的流），在每个流播放时通过让音频流垫长（重复部分）或者静默（截断）来实现视频流连续。

为了让滤镜工作正常，所有段都必须以 0 为时间戳开始。

所有应用的流在所有共同的领域必须有相同的参数，滤镜会自动选择一个通用的像素格式（色彩标注、编码颜色的标准和位深等），以及音频采样率和通道布局。但其他设置如视频分辨率必须由用户显式转换。

不同的帧率是可以接受的，但会导致输出帧率的变化，一定要配置输出文件来处理。

### 示例

```python
from ffmpeg import input
from tests import data

input_v1 = input(data.V1)
_ = input_v1.concat(input_v1).output(data.TEST_OUTPUTS_DIR / 'concat.mp4').run()

```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i C:\Users\Admin\Videos\FFmpeg\InputsData\v1.mp4 -filter_complex "[0][0]concat=n=2[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\FFmpeg\OutputsData\concat.mp4 -y -hide_banner
[11.9433s]
```

## ebur128

> https://ffmpeg.org/ffmpeg-filters.html#ebur128


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## interleave

> https://ffmpeg.org/ffmpeg-filters.html#interleave


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ainterleave

> https://ffmpeg.org/ffmpeg-filters.html#ainterleave


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## metadata

> https://ffmpeg.org/ffmpeg-filters.html#metadata


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ametadata

> https://ffmpeg.org/ffmpeg-filters.html#ametadata


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## perms

> https://ffmpeg.org/ffmpeg-filters.html#perms


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## aperms

> https://ffmpeg.org/ffmpeg-filters.html#aperms


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## realtime

> https://ffmpeg.org/ffmpeg-filters.html#realtime


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## arealtime

> https://ffmpeg.org/ffmpeg-filters.html#arealtime


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## select

> https://ffmpeg.org/ffmpeg-filters.html#select


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## aselect

> https://ffmpeg.org/ffmpeg-filters.html#aselect


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## sendcmd

> https://ffmpeg.org/ffmpeg-filters.html#sendcmd


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## asendcmd

> https://ffmpeg.org/ffmpeg-filters.html#asendcmd


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## setpts, asetpts

> https://ffmpeg.org/ffmpeg-filters.html#setpts

修改输入帧显示时间戳（PTS-presentation timestamp）。其中 `setpts` 对于视频帧，`asetpts` 对于音频帧。

### 参数

- expr 指定用于计算时间戳的表达式

表达式常量：

- FRAME_RATE 帧率，仅对于指定了帧率的视频
- PTS 输入的 PTS
- N 对输入视频帧计数或已经消耗的样本计数，不包括音频的当前帧，从 0 开始
- NB_CONSUMED_SAMPLES 采样数（因为音频是按固定频率采样，则一个采样其实就是自然的计时单位——类似帧率），不包括当前帧（仅对音频）
- NB_SAMPLES, S 当前帧中的采样数 ( 仅音频 )
- SAMPLE_RATE, SR 音频采样率
- STARTPTS 第一帧的 PTS
- STARTT 第一帧的按秒时间
- INTERLACED 指示当前帧是否交错
- T 当前帧的按秒时间
- POS 初始位置在文件中的偏移，为当前帧，如果为定义则本值也为定义
- PREV_INPTS 前一个帧的 PTS
- PREV_INT 前一帧按秒时间
- PREV_OUTPTS 前一帧的输出 PTS
- PREV_OUTT 前一帧按秒输出时间
- RTCTIME 时间单位为微秒 -microseconds. 现在被弃用，使用 time(0) 时
- RTCSTART 影片开始时间以微秒为单位
- TB 输入时间戳时基

### 示例

#### 从 0 开始计数 PTS

```python
# Start counting PTS from zero
_ = input(v1).setpts("PTS-STARTPTS").output(testdata_transform / "setpts1.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=PTS-STARTPTS[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts1.mp4 -y -hide_banner
[4.1000s]
```

#### 对比

[视频对比链接]

#### 加速播放效果

```python
# Apply fast motion effect
_ = input(v1).setpts("0.5*PTS").output(testdata_transform / "setpts2.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=0.5*PTS[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts2.mp4 -y -hide_banner
[3.8456s]
```

#### 对比

[视频对比链接]

#### 减速播放效果

```python
# Apply slow motion effect
_ = input(v1).setpts("2.0*PTS").output(testdata_transform / "setpts3.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=2.0*PTS[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts3.mp4 -y -hide_banner
[7.6312s]
```

#### 对比

[视频对比链接]

#### 强制为 25 的帧率

```python
# Set fixed rate of 25 frames per second
_ = input(v1).setpts("N/(25*TB)").output(testdata_transform / "setpts4.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=N/(25*TB)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts4.mp4 -y -hide_banner
[4.6901s]
```

#### 对比

[视频对比链接]

#### 设置有抖动的 25 帧率

```python
# Set fixed rate 25 fps with some jitter
_ = input(v1).setpts("1/(25*TB) * (N + 0.05 * sin(N*2*PI/25))").output(testdata_transform / "setpts5.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=1/(25*TB) * (N + 0.05 
* sin(N*2*PI/25))[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts5.mp4 -y -hide_banner
[4.8256s]
```

#### 对比

[视频对比链接]

#### 应用一个 10 秒的输入偏置

```python
# Apply an offset of 10 seconds to the input PTS
_ = input(v1).setpts("PTS+10/TB").output(testdata_transform / "setpts6.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=PTS+10/TB[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts6.mp4 -y -hide_banner
[4.4644s]
```

#### 对比

[视频对比链接]

#### 从`直播源`和变基生成时间戳转换到当前时基时间戳

```python
# Generate timestamps from a "live source" and rebase onto the current timebase
_ = input(v1).setpts("(RTCTIME - RTCSTART) / (TB * 1000000)").output(testdata_transform / "setpts7.mp4").run()

```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=(RTCTIME - RTCSTART) / (TB * 1000000)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts7.mp4 -y -hide_banner
[3.7406s]
```

#### 对比

[视频对比链接]

#### 按当前采样率生成时间戳

```python
# Generate timestamps by counting samples
_ = input(v1).setpts("N/SR/TB").output(testdata_transform / "setpts8.mp4").run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]setpts=N/SR/TB[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\setpts8.mp4 -y -hide_banner
[3.8506s]
```

#### 对比

[视频对比链接]

## setrange

> https://ffmpeg.org/ffmpeg-filters.html#setrange


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## settb

> https://ffmpeg.org/ffmpeg-filters.html#settb


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## asettb

> https://ffmpeg.org/ffmpeg-filters.html#asettb


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showcqt

> https://ffmpeg.org/ffmpeg-filters.html#showcqt


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showfreqs

> https://ffmpeg.org/ffmpeg-filters.html#showfreqs


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showspatial

> https://ffmpeg.org/ffmpeg-filters.html#showspatial


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showspectrum

> https://ffmpeg.org/ffmpeg-filters.html#showspectrum


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showspectrumpic

> https://ffmpeg.org/ffmpeg-filters.html#showspectrumpic


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showvolume

> https://ffmpeg.org/ffmpeg-filters.html#showvolume


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showwaves

> https://ffmpeg.org/ffmpeg-filters.html#showwaves


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showwavespic

> https://ffmpeg.org/ffmpeg-filters.html#showwavespic


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## sidedata

> https://ffmpeg.org/ffmpeg-filters.html#sidedata


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## asidedata

> https://ffmpeg.org/ffmpeg-filters.html#asidedata


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## spectrumsynth

> https://ffmpeg.org/ffmpeg-filters.html#spectrumsynth


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## split

> https://ffmpeg.org/ffmpeg-filters.html#split


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## asplit

> https://ffmpeg.org/ffmpeg-filters.html#asplit


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## zmq

> https://ffmpeg.org/ffmpeg-filters.html#zmq


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## azmq

> https://ffmpeg.org/ffmpeg-filters.html#azmq


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## amovie

> https://ffmpeg.org/ffmpeg-filters.html#amovie


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## movie

> https://ffmpeg.org/ffmpeg-filters.html#movie


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]
