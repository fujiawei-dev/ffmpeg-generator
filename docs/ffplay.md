<!--
 * @Date: 2021.03.15T18:12:46+08:00
 * @Description: FFplay 常用命令
 * @LastEditors: Rustle Karl
 * @LastEditTime: 2021.04.30 10:37:13
-->

# FFplay 常用命令

## 播放控制

| 选项 | 说明 |
| ------------ | ------------ |
| q,ESC | 退出播放 |
| f | 全屏切换 |
| p,SPC | 暂停 |
| m | 静音播放 |
| 9，0 | 9 减少音量，0 增加音量 |
| a | 循环切换音频流 |
| v | 循环切换视频流 |
| t | 循环切换字幕流 |
| c | 循环切换节目 |
| w | 循环切换过滤器或显示模式 |
| s | 逐帧播放 |
| left/right | 向后/向前拖动 10 秒 |
| down/up | 向后/向前拖动 1 分钟 |
| 鼠标右键单击 | 拖动与显示宽度对应百分比的文件进行播放 |
| 鼠标左键双击 | 全屏切换 |

## 命令选项

| 主要选项 | 说明 |
| -------------- | -------------- |
| -x | 强制显示宽带 |
| -y height | 强制显示高度 |
| -video_size | 帧尺寸设置显示帧存储（WxH 格式），仅适用于类似原始 YUV 等没有包含帧大小（WxH）的视频，如果设备不支持该分辨率则报错 |
| -pixel_format | 格式设置像素格式 |
| -fs | 以全屏模式启动 |
| -an | 禁止音频（不播放声音） |
| -vn | 禁止视频（不播放视频） |
| -sn | 禁用字幕（不显示字幕） |
| -ss pos | 根据设置的秒进行定位拖动 |
| -t duration | 设置播放视频/音频长度 |
| -bytes | 按字节进行定位拖动（0=off 1=on -1=auto） |
| -seek_interval | 自定义左/右键定位拖动间隔（以秒为单位），默认10s |
| -nodisp | 关闭图形化显示窗口，视频将不显示 |
| -noborder | 无边框窗口 |
| -volume | 设置起始音量，range[0,100] |
| -f | 强制使用设置的格式进行解析，比如 `-f s16le` |
| -window_title | 设置窗口标题（默认为输入文件名） |
| -loop | 设置播放循环次数 |
| -showmode | 设置显示模式，0 显示视频，1 显示音频波形，2 显示音频频谱，缺省值为 0，如果视频不存在则自动选择 2 |
| -vf | 设置视频滤镜 |
| -af | 设置音频滤镜 |

## 高级选项

| 选项 | 说明 |
| -------------- | -------------- |
| -stats | 打印多个回放统计信息。包括显示流持续时间，编解码器参数，流中的当前位置，以及音频/视频同步差值。缺省值是自动开启，显示禁用指定-stats |
| -fast | 非标准化规范的多媒体兼容优化 |
| -genpts | 生产pts |
| -sync | 同步类型，将主时钟设置为audio，video或external，默认是audio |
| -ast | audio_stream_specifier 指定音频流索引，比如-ast 3，播放流索引为3的音频流 |
| -vst | video_stream_specifier 指定视频流索引 |
| -sst | subtitle_stream_specifier 指定字幕流索引 |
| -autoexit | 视频播放完毕后退出 |
| -exitonkeydown | 键盘按下任何键退出播放 |
| -exitonmousedown | 鼠标按下任何键退出播放 |
| -codec:media_specifier | 强制使用设置的多媒体解码器，a(音频)，v（视频）和s(字幕)，如 -codec:v h264_qsv |
| -acodec | 强制使用设置的音频解码器进行音频解码 |
| -vcodec | 强制使用设置的视频解码器进行视频解码 |
| -scodec | 强制使用设置的字幕解码器进行字幕解码 |
| -autorotate | 根据文件元数据自动旋转视频。值为0或1，默认为1 |
| -framedrop | 如果视频不同步则丢弃视频帧，当主时钟非视频时钟时默认开启，若需禁用使用选项-noframedrop |
| -inbuf | 不限制输入缓冲区大小，尽可能地从输入中读取尽可能多的数据。 |

## 过滤器

> 似乎不支持复杂滤镜

| 例子 | 命令 |
| -------------- | -------------- |
| 视频旋转 | ffplay -i test.mp4 -vf transpose=1 |
| 视频反转 | ffplay test.mp4 -vf hflip, ffplay test.mp4 -vf vflip |
| 视频旋转和反转 | ffplay test.mp4 -vf hflip,transpose=1 |
| 音频变速播放 | ffplay -i test.mp4 -af atempo=2 |
| 视频变速播放 | ffplay -i test.pm4 -vf setpts=PTS/2 |
| 音视频同时变速播放 | ffplay -i test.mp4 -vf setpts=PTS/2 -af atempo=2 |

## 代码示例

```python
from ffmpeg import ffplay_video
from tests import data

ffplay_video(data.V1, vf='transpose=1')
ffplay_video(data.V1, vf='hflip')
ffplay_video(data.V1, af='atempo=2')
ffplay_video(data.V1, vf='setpts=PTS/2')
ffplay_video(data.V1, vf='transpose=1,setpts=PTS/2', af='atempo=2')
```

## 命令行示例

### 播放一个音频文件

```shell
ffplay audio.aac
```

这时候会弹出一个窗口，一边播放音频文件，一边将播放声音的语谱图画到该窗口上。针对该窗口的操作如下，点击窗口的任意一个位置，ffplay 会按照点击的位置计算出时间的进度，然后跳到这个时间点上继续播放；按下键盘上的右键会默认快进 10s，左键默认后退 10s，上键默认快进 1min，下键默认后退 1min；按 ESC 键就是退出播放进程；如果按 w 键则将绘制音频的波形图等。

### 播放一个视频文件

```shell
ffplay video.mp4
```

这时候会直接在新弹出的窗口上播放该视频，如果想要同时播放多个文件，那么只需要在多个命令行下同时执行 ffplay 就可以了，按 s 键则可以进入 frame-step 模式，即按 s 键一次就会播放下一帧图像。

### 从第 30 秒开始播放 10 秒

```shell
# 从第 30 秒开始播放 10 秒
ffplay -ss 30 -t 10 long.mp4
```

### 循环播放

```shell
ffplay video.mp4 -loop 10
```

### 播放视频中的第一路音频流

```shell
ffplay video.mkv -ast 1
```

### 表示播放视频中的第一路视频流

```shell
ffplay video.mkv -vst 1
```

## 播放裸数据

### 播放 PCM 格式的音频

```shell
ffplay song.pcm -f s16le -channels 2 -ar 4
```

格式（-f）、声道数（-channels）、采样率（-ar）必须设置正确。其中任何一项参数设置不正确，都不会得到正常的播放结果。

WAV 格式的文件称为无压缩的格式，其实就是在 PCM 的头部添加 44 个字节，用于标识这个 PCM 的采样表示格式、声道数、采样率等信息，对于 WAV 格式音频文件，ffplay 可以直接播放，但是若让 ffplay 播放 PCM 裸数据的话，只要为其提供上述三个主要的信息，那么它就可以正确地播放了。

### 播放 YUV420P 格式的视频帧

```shell
ffplay -f rawvideo -pixel_format yuv420p -s 480*480 texture.yuv
```

格式（-f rawvideo代表原始格式）、表示格式（-pixel_format yuv420p）、宽高（-s 480*480）。

### 播放 RGB 的原始数据

```shell
ffplay -f rawvideo -pixel_format rgb24 -s 480*480 texture.rgb
```

## 音画同步

FFplay 中音画同步的实现方式其实有三种：以音频为主时间轴作为同步源；以视频为主时间轴作为同步源；以外部时钟为主时间轴作为同步源。在 ffplay 中默认的对齐方式也是以音频为基准进行对齐的。

播放器接收到的视频帧或者音频帧，内部都会有时间戳（PTS 时钟）来标识它实际应该在什么时刻进行展示。实际的对齐策略如下：比较视频当前的播放时间和音频当前的播放时间，如果视频播放过快，则通过加大延迟或者重复播放来降低视频播放速度；如果视频播放慢了，则通过减小延迟或者丢帧来追赶音频播放的时间点。关键就在于音视频时间的比较以及延迟的计算，在比较的过程中会设置一个阈值（Threshold），若超过预设的阈值就应该做调整（丢帧渲染或者重复渲染）。

### 指定对齐方式

```shell
# 以音频为主时间轴
ffplay 32037.mp4 -sync audio

# 以视频为主时间轴
ffplay 32037.mp4 -sync video

# 以外部时钟为主时间轴
ffplay 32037.mp4 -sync ext
```
