<!--
 * @Date: 2021.03.08T22:56:00+08:00
 * @Description: All Examples for Video Filters
 * @LastEditors: Rustle Karl
 * @LastEditTime: 2021.04.30 12:28:42
-->

FFmpeg 自带了大概有 450 多个音视频媒体滤镜，基本上涵盖了视频处理的绝大部分功能。但是由于对这些滤镜不可能了如指掌，甚至大部分滤镜都没见过，就可能不知道如何实现一个需求，所以还是有必要尝试一遍 FFmpeg 的全部滤镜吧。所以就决定写一下这个系列，力求给出每个滤镜的示例及最终结果对比视频/图，但也有可能中途夭折。

该系列文章的 FFmpeg 命令都是由 FFmepg-Generator 生成的，不论是出于复用考量，还是方便书写，记原生命令太为难普通人了。不过该项目现在还在测试中，暂时未开源。

FFmpeg 的滤镜参数可以是位置参数，即不提供参数名，只提供参数值，这种情况下参数的顺序是不可以改变的；另一种的关键词参数，以键值对的形式指明参数，位置可不限。

颜色、尺寸、时间等表达式的语法规则：

> https://ffmpeg.org/ffmpeg-utils.html

部分实在是用不到的或者暂时不理解用处的滤镜暂时省略，今后如有用到再补。

```python
from ffmpeg import input, merge_outputs, vfilters, vtools
```

## addroi

> https://ffmpeg.org/ffmpeg-filters.html#addroi

ROI（region of interest），感兴趣区域。机器视觉、图像处理中，从被处理的图像以方框、圆、椭圆、不规则多边形等方式勾勒出需要处理的区域，称为感兴趣区域，ROI。

该滤镜用于指定视频中若干个区域为感兴趣区域，但是视频帧信息不改变，只是在 metadata 中添加 roi 的信息，影响稍后的编码过程，通过多次应用该滤镜可以标记多个区域。

### 参数

- x 与帧左边的像素距离
- y 与帧上边的像素距离
- w 区域像素宽，iw 表示输入帧宽
- h 区域像素高，ih 表示输入帧高
- qoffset 标记区域编码质量偏移，介于 -1 到 1，负值表示更高质量，0 表示保持质量，正值表示更低质量，可以认为是不感兴趣
- clear 设置为 true 则移除全部已存在的区域标记

### 示例 - 标记视频的中心区域

为了对比明显，设置了最差质量。

```python
_ = input(src).addroi(x="iw/4", y="ih/4", w="iw/2", h="ih/2", qoffset=1, clear=1).output(dst).run()
```

> 该代码可生成下面的命令并执行，最后给出运行时间。

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]addroi=clear=1:h=ih/2:qoffset=1:w=iw/2:x=iw/4:y=ih/4[tag0]" -map [tag0] testdata\media\v0_addroi.mp4 -y -hide_banner
[0.5302s]
```

#### 对比

原视频 221 KB，合成视频 202 KB。对比视频（默认左边原视频）：

```python
vtools.compare_2_videos(src, dst, src_dst_compare)
```

> 之后对比用的代码都是一样，所以就这里写一次。

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\v0_addroi.mp4 -filter_complex "[0]pad=w=2*iw[tag0];[tag0][1]overlay=x=w[tag1]" -map [tag1] testdata\media\v0_addroi_compare.mp4 -y -hide_banner
[1.0771s]
```

https://www.bilibili.com/video/BV1iv411h7Eq/

## alphaextract

> https://ffmpeg.org/ffmpeg-filters.html#alphaextract

从输入中提取 alpha 分量作为灰度视频。这对于 `alphamerge` 过滤器特别有用。

### 参数

无

### 示例

首先要确定输入的视频有 alpha 通道，不存在则报错。即必须是 RGBA 格式的，不然会提取失败。RGBA 格式是在普通的 RGB 格式基础上增长了一个 alpha 分量，该分量用于表示图像的透明度。

太遗憾了，我找不到这种符合格式的视频，最终用了 PNG 格式的图片代替视频测试：

```python
_ = input(src).alphaextract().output(dst).run()
```

```
ffmpeg -i testdata\i2.png -filter_complex "[0]alphaextract[tag0]" -map [tag0] testdata\i2_alphaextract.png -y -hide_banner
[0.1415s]
```

#### 对比

![](https://i.loli.net/2021/03/10/piTZjoF253lG8Dg.png)

## alphamerge

> https://ffmpeg.org/ffmpeg-filters.html#alphamerge

用第二个输入视频的灰度值添加或替换第一个输入视频的 alpha 分量。 可以与 `alphaextract` 一起使用，以允许传输或存储具有 alpha 格式但不支持 alpha 通道的帧序列。

### 参数

无

### 示例

```python
_ = input(src).movie(filename=i2_alpha.as_posix()).alphamerge().output(dst).run()
```

```
ffmpeg -i testdata\i3.png -filter_complex "movie=filename=testdata/i2_alpha.png[tag0];[0][tag0]alphamerge[tag1]" -map [tag1] testdata\i3_alphamerge.png -y -hide_banner
```

等价写法：

```python
_ = input(src).alphamerge(input(i2_alpha)).output(dst).run()
```

```
ffmpeg -i testdata\i3.png -i testdata\i2_alpha.png -filter_complex "[0][1]alphamerge[tag0]" -map [tag0] testdata\i3_alphamerge.png -y -hide_banner
[0.1514s]
```

#### 对比

找不到可用视频素材，仍以图片测试，黑色部分表示透明。

![](https://i.loli.net/2021/03/11/5xqBnRTLoVUfzGZ.png)

## amplify

> https://ffmpeg.org/ffmpeg-filters.html#amplify

放大当前帧和相邻帧相同位置的像素差异。

### 参数

- radius 设置取相邻帧的数量，范围 1 ~ 63，默认 2，比如设置为 3，即取前后各 3 帧加上当前帧，计算 7 帧的平均值
- factor 设置差异放大因子，范围 0 ~ 65535，默认 2
- threshold 设置差异上限，范围 0 ~ 65535，默认 2，任何大于等于该上限的像素差异都不会放大（差异已经够大，所以不再放大）。
- tolerance 设置差异下限，范围 0 ~ 65535，默认 0，任何小于该下限的像素差异都不会放大（差异过小）。
- low 设置更改源像素的下限。默认是 65535。取值范围是 0 ~ 65535。降低源像素值的最大可能值。
- high 设置更改源像素的上限。 默认值为 65535。允许的范围是 0 到 65535。增加源像素值的最大可能值。
- planes 设置进行处理的通道。 默认为全部。 允许范围是 0 到 15。

### 示例

```python
_ = input(src).amplify(radius=3, factor=10, threshold=50).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]amplify=factor=10:radius=3:threshold=50[tag0]" -map [tag0] testdata\media\v0_amplify.mp4 -y -hide_banner
[1.0090s]
```

#### 对比

https://www.bilibili.com/video/BV1V54y1a7Um

## ass

> https://ffmpeg.org/ffmpeg-filters.html#ass

可添加 ASS 格式的字幕。参数及用法与 subtitles 滤镜基本一致。

### 参数

- shaping 设置渲染引擎。
  - auto 默认的 `libass` 引擎
  - simple `font-agnostic` 引擎
  - complex `OpenType` 引擎

其他参数与 subtitles 滤镜相同。

### 示例

字幕文件由[Aegisub](https://aegi.vmoe.info/downloads/)软件手工制作。

```python
_ = input(src).ass(filename=media_v0_ass.as_posix()).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]ass=filename=testdata/media/0.ass[tag0]" -map [tag0] testdata\media\v0_ass.mp4 -y -hide_banner
[0.6707s]
```

#### 对比

https://www.bilibili.com/video/BV1Fv411a7L1/

## atadenoise

> https://ffmpeg.org/ffmpeg-filters.html#atadenoise

自适应时域平均降噪器 (Adaptive Temporal Averaging Denoiser)。

### 参数

- 0a 设置 1 通道阈值 A，范围 0 ~ 0.3，默认 0.02
- 0b 设置 1 通道阈值 B，范围 0 ~ 5，默认0.04
- 1a 同上类推
- 1b 同上类推
- 2a 同上类推
- 2b 同上类推
- s 设置用于平均的帧数，范围 5 到 129 的奇数，默认 9
- p 设置通道，默认全部
- a 设置算法过滤器将用于平均的变量。 默认为 p 并行。 也可以将其设置为 s 串行。并行可以比串行更快。 并行将在第一个变化大于阈值时提前中止，而串行将继续处理帧的另一侧（等于或小于阈值时）。
- 0s 同下类推
- 1s 同下类推
- 2s 为通道设置 sigma。 默认值为 32767。有效范围是 0 到 32767。控制由尺寸定义的半径中每个像素的权重。 默认值表示每个像素具有相同的权重。 设置为 0 可以有效地禁用过滤。

### 示例

```python
_ = input(src).atadenoise(s=25).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]atadenoise=s=25[tag0]" -map [tag0] testdata\media\v0_atadenoise.mp4 -y -hide_banner
[1.5373s]
```

#### 对比

肉眼看不出差别：

[视频对比链接]

## avgblur

> https://ffmpeg.org/ffmpeg-filters.html#avgblur

平均模糊滤波器。

### 参数

- sizeX 水平半径
- sizeY 垂直半径
- planes 通道，默认全部

### 示例

```python
_ = input(src).avgblur(x=10, y=10).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]avgblur=sizeX=10:sizeY=10[tag0]" -map [tag0] testdata\media\v0_avgblur.mp4 -y -hide_banner
[0.7048s]
```

#### 对比

[视频对比链接]

## bbox

> https://ffmpeg.org/ffmpeg-filters.html#bbox

计算输入帧亮度通道中非黑色像素的边界框。

该过滤器计算包含所有像素的边界框，这些像素的亮度值大于最小允许值。 描述边界框的参数打印在过滤器日志中。对于输出视频无影响。

### 参数

- min_val 最小亮度值，默认 16

### 示例

```python
_ = input(src).bbox(min_val=100).output(dst).run(capture_stderr=False,capture_stdout=False)
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]bbox=min_val=100[tag0]" -map [tag0] testdata\media\v0_bbox.mp4 -y -hide_banner
[0.9152s]
```

#### 对比

只是输出了描述边界框的参数，对于输出视频无影响。


## bilateral

> https://ffmpeg.org/ffmpeg-filters.html#bilateral

双边过滤器，在保留边缘的同时进行空间平滑。

### 参数

- sigmaS 设置高斯函数的 sigma 以计算空间权重。 允许范围为 0 到 512。默认值为 0.1
- sigmaR 设置高斯函数的 sigma 以计算范围权重。允许范围为 0 到 1。默认值为 0.1
- planes 设置通道，默认第一通道

### 示例

```python
_ = input(src).bilateral(s=12, r=0.3).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]bilateral=sigmaR=0.3:sigmaS=12[tag0]" -map [tag0] testdata\media\v0_bilateral.mp4 -y -hide_banner
[1.6872s]
```

#### 对比

[视频对比链接]


## 10 bitplanenoise

> https://ffmpeg.org/ffmpeg-filters.html#bitplanenoise

显示和测量位通道噪声。

### 参数

- bitplane 指定分析通道，默认 1
- filter 从上面设置的位通道中滤除噪点像素，默认设置为禁用。

### 示例

```python
_ = input(src).bitplanenoise(filter=True).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]bitplanenoise=filter=True[tag0]" -map [tag0] testdata\media\v0_bitplanenoise.mp4 -y -hide_banner
[0.8679s]
```

#### 对比

[视频对比链接]

## blackdetect

> https://ffmpeg.org/ffmpeg-filters.html#blackdetect

检测视频中全黑的段落。

过滤器将其检测分析以及帧元数据输出到日志。 如果找到至少指定了最小持续时间的黑色段，则会将带有开始和结束时间戳记以及持续时间的行打印到带有级别信息的日志中。 另外，每帧打印一条带调试级别的日志行，显示该帧检测到的黑色量。

过滤器还将键为 lavfi.black_start 的元数据附加到黑色段的第一帧，并将键为 lavfi.black_end 的元数据附加到黑色段结束后的第一帧。该值是帧的时间戳。无论指定的最短持续时间如何，都会添加此元数据。

### 参数

- black_min_duration, d 设置检测到的最小黑屏持续时间（以秒为单位），必须是非负浮点数，默认 2.0
- picture_black_ratio_th, pic_th 设置用于考虑图片“黑色”的阈值，表示比率的最小值：`nb_black_pixels / nb_pixels`，超过该阈值即认为是黑屏，默认 0.98
- pixel_black_th, pix_th 设置用于考虑像素“黑色”的阈值。阈值表示将像素视为“黑色”的最大像素亮度值。 提供的值根据以下公式缩放：`absolute_threshold = luminance_minimum_value + pixel_black_th * luminance_range_size`，`luminance_range_size和luminance_minimum_value` 取决于输入的视频格式，YUV 全范围格式的范围是[0-255]，YUV 非全范围格式的范围是[16-235]。默认 0.10

### 示例

```python
_ = input(src).blackdetect(d=2, pix_th=0.00).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]blackdetect=d=2:pix_th=0.0[tag0]" -map [tag0] testdata\media\v0_blackdetect.mp4 -y -hide_banner
[0.3799s]
```

#### 对比

只是打印了信息和写入了元数据，输出视频与原视频肉眼看无差别。

## blackframe

> https://ffmpeg.org/ffmpeg-filters.html#blackframe

检测全黑的帧。 输出行包括检测到的帧的帧号，黑度百分比，文件中的位置或 -1 以及以秒为单位的时间戳。

为了显示输出行，至少将日志级别设置为 AV_LOG_INFO 值。

此过滤器导出帧元数据 lavfi.blackframe.pblack。该值表示图片中低于阈值的像素百分比。

### 参数

- amount 必须低于阈值的像素百分比；默认为 98
- threshold 阈值，低于该阈值将被视为黑色；默认为 32


### 示例

```python
_ = input(src).blackframe(amount=95, threshold=24).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]blackframe=amount=95:threshold=24[tag0]" -map [tag0] testdata\media\v0_blackframe.mp4 -y -hide_banner
[0.8265s]
```

#### 对比

只是打印了信息和写入了元数据，输出视频与原视频肉眼看无差别。

## blend

> https://ffmpeg.org/ffmpeg-filters.html#blend

将两个视频帧混合在一起。输入两个视频流，第一个输入作为上层帧，第二个输入作为底层帧，控制底层和上层帧显示的权重。

`tblend` 从单个流中获取两个连续的帧，并输出将新帧混合到旧帧上获得的结果。

### 参数

- c0_mode
- c1_mode
- c2_mode
- c3_mode
- all_mode 为特定的像素分量或所有像素分量设置混合模式。默认 normal。有效的模式有：

  - ‘addition’
  - ‘grainmerge’
  - ‘and’
  - ‘average’
  - ‘burn’
  - ‘darken’
  - ‘difference’
  - ‘grainextract’
  - ‘divide’
  - ‘dodge’
  - ‘freeze’
  - ‘exclusion’
  - ‘extremity’
  - ‘glow’
  - ‘hardlight’
  - ‘hardmix’
  - ‘heat’
  - ‘lighten’
  - ‘linearlight’
  - ‘multiply’
  - ‘multiply128’
  - ‘negation’
  - ‘normal’
  - ‘or’
  - ‘overlay’
  - ‘phoenix’
  - ‘pinlight’
  - ‘reflect’
  - ‘screen’
  - ‘softlight’
  - ‘subtract’
  - ‘vividlight’
  - ‘xor’

- c0_opacity
- c1_opacity
- c2_opacity
- c3_opacity
- all_opacity 设置特定像素组件或所有像素组件的混合不透明度。 仅与像素成分混合模式结合使用。

- c0_expr
- c1_expr
- c2_expr
- c3_expr
- all_expr 设置特定像素分量或所有像素分量的混合表达式。 如果设置了相关的模式选项，则将忽略。表示式可用变量：

  - N 过滤后的帧的序号，从 0 开始
  - X
  - Y 当前样本的坐标
  - W
  - H 当前过滤通道的宽度和高度
  - SW
  - SH 被过滤通道的宽度和高度比例。 它是当前通道尺寸与亮度通道尺寸之间的比率，例如 对于 yuv420p 帧，亮度通道的值为 1,1，色度通道的值为 0.5,0.5
  - T 当前帧的时间，以秒为单位
  - TOP 第一个视频帧（顶层）当前位置的像素分量值
  - BOTTOM 第二个视频帧（底层）当前位置的像素分量值

`blend` 支持 `framesync` 参数。

### 示例

### 在 4 秒内从底层过渡到顶层

```python
_ = vfilters.blend(in1, in2, all_expr='A*(if(gte(T,4),1,T/4))+B*(1-(if(gte(T,4),1,T/4)))').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=A*(if(gte(T\,4)\,1\,T/4))+B*(1-(if(gte(T\,4)\,1\,T/4)))[tag0]" -map [tag0] testdata\media\v0_v1_blend_1.mp4 -y -hide_banner
[1.6540s]
```

#### 对比

[视频对比链接]

### 从顶层到底层的线性水平过渡

```python
_ = vfilters.blend(in1, in2, all_expr='A*(X/W)+B*(1-X/W)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=A*(X/W)+B*(1-X/W)[tag0]" -map [tag0] testdata\media\v0_v1_blend_2.mp4 -y -hide_banner
[2.4407s]
```

#### 对比

[视频对比链接]

### 1x1 棋盘格效果

```python
_ = vfilters.blend(in1, in2, all_expr='if(eq(mod(X,2),mod(Y,2)),A,B)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=if(eq(mod(X\,2)\,mod(Y\,2))\,A\,B)[tag0]" -map [tag0] testdata\media\v0_v1_blend_3.mp4 -y -hide_banner
[0.8931s]
```

#### 对比

[视频对比链接]

### 从右边揭开效果

```python
_ = vfilters.blend(in1, in2, all_expr='if(gte(N*SW+X*T,W),A,B)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=if(gte(N*SW+X*T\,W)\,A\,B)[tag0]" -map [tag0] testdata\media\v0_v1_blend_4.mp4 -y -hide_banner
[2.3491s]
```

#### 对比

[视频对比链接]

### 从上边揭开效果

```python
_ = vfilters.blend(in1, in2, all_expr='if(gte(Y-N*SH*T,0),A,B)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=if(gte(Y-N*SH*T\,0)\,A\,B)[tag0]" -map [tag0] testdata\media\v0_v1_blend_5.mp4 -y -hide_banner
[0.9813s]
```

#### 对比

[视频对比链接]

### 从右下角揭开效果

```python
_ = vfilters.blend(in1, in2, all_expr='if(gte(T*SH*40+Y*T,H)*gte((T*40*SW+X)*W/H,W),A,B)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=if(gte(T*SH*40+Y*T\,H)*gte((T*40*SW+X)*W/H\,W)\,A\,B)[tag0]" -map [tag0] testdata\media\v0_v1_blend_6.mp4 -y -hide_banner
[1.8537s]
```

#### 对比

[视频对比链接]

### 对角显示

```python
_ = vfilters.blend(in1, in2, all_expr='if(gt(X,Y*(W/H)),A,B)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -i testdata\media\1.mp4 -filter_complex "[0][1]blend=all_expr=if(gt(X\,Y*(W/H))\,A\,B)[tag0]" -map [tag0] testdata\media\v0_blend.mp4 -y -hide_banner
[0.8858s]
```

#### 对比

[视频对比链接]

### 显示当前帧和上一帧之间的差异

```python
_ = in1.tblend(all_mode="grainextract").output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]tblend=all_mode=grainextract[tag0]" -map [tag0] testdata\media\v0_v1_blend_8.mp4 -y -hide_banner
[0.4555s]
```

#### 对比

[视频对比链接]

## bm3d

> https://ffmpeg.org/ffmpeg-filters.html#bm3d

用块匹配 3D 算法（Block-Matching 3D algorithm）对帧进行消噪。

### 参数

- sigma 设置降噪强度。 默认值为 1。允许的范围是 0 到 999.9。去噪算法对 sigma 非常敏感，因此请根据信号源进行调整。
- block 设置本地补丁大小。 这将以 2D 设置尺寸。
- bstep 设置处理块的滑动步长。 默认值为 4。允许的范围是 1 到 64。较小的值允许处理更多的参考块，并且速度较慢。
- group 设置第 3 维相似块的最大数量。默认值为 1。设置为 1 时，不执行块匹配。较大的值可以在一个组中包含更多块。允许范围是 1 到 256。
- range 设置搜索块匹配的半径。 默认值为 9。允许的范围是 1 到 INT32_MAX。
- mstep 在两个搜索位置之间设置步长以进行块匹配。 默认值为 1。允许的范围是 1 到 64。越小越慢。
- thmse 设置块匹配的均方误差阈值。 有效范围是 0 到 INT32_MAX。
- hdthr 为 3D 转换域中的硬阈值设置阈值参数。 较大的值将导致频域中的更强硬阈值滤波。
- estim 设置过滤评估模式。 可以是 basic 或 final。 默认为 basic。
- ref 如果启用，过滤器将使用第二流进行块匹配。 estim 为 basic 则默认禁用，如果 estim 是 final，则始终默认启用。
- planes 设置过滤的通道。 默认值是除 alpha 以外的所有通道。

### 示例

```python
_ = input(src).bm3d(sigma=3, block=4, bstep=2, group=1, estim="basic").output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]bm3d=block=4:bstep=2:estim=basic:group=1:sigma=3[tag0]" -map [tag0] testdata\media\v0_bm3d.mp4 -y -hide_banner
[9.0762s]
```

#### 对比

差别不大。

[视频对比链接]

## boxblur

> https://ffmpeg.org/ffmpeg-filters.html#boxblur

boxblur 算法滤镜。

### 参数

- luma_radius, lr
- chroma_radius, cr
- alpha_radius, ar 用于为框半径设置一个表达式，以像素为单位来模糊相应的输入通道。半径值必须为非负数，并且对于亮度和 alpha 通道，不得大于表达式 min(w,h)/2 的值，对于色度，不得大于 min(cw,ch)/2 的值。luma_radius 的默认值为 “2”。如果未指定，则 chroma_radius 和 alpha_radius 默认为 luma_radius 设置的相应值。可用的常量有：
  - w
  - h 输入视频的像素宽和高
  - cw
  - ch 输入色度图像的像素宽和高
  - hsub
  - vsub 水平和垂直色度子样本值。 例如，对于像素格式 “yuv422p”，hsub 为 2，vsub 为 1

- luma_power, lp
- chroma_power, cp
- alpha_power, ap 指定将 boxblur 滤镜应用到相应通道的次数。luma_power 的默认值为 2。如果未指定，则 chroma_power 和 alpha_power 默认为 luma_power 设置的相应值。值为 0 将禁用效果。

### 示例

```python
_ = input(src).boxblur(luma_radius="min(h,w)/10", luma_power=1,
                       chroma_radius="min(cw,ch)/10", chroma_power=1). \
    output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]boxblur=chroma_power=1:chroma_radius=min(cw\,ch)/10:luma_power=1:luma_radius=min(h\,w)/10[tag0]" -map [tag0] testdata\media\v0_boxblur.mp4 -y -hide_banner
[0.7788s]
```

#### 对比

[视频对比链接]

## bwdif

> https://ffmpeg.org/ffmpeg-filters.html#bwdif

反交错滤波器 Bob Weaver Deinterlacing Filter。基于 yadif 运动自适应反交错，使用 w3fdif 和三次插值算法。

### 参数

- mode 交错扫描模式
  - 0, send_frame 每帧输出一帧
  - 1, send_field 每个场输出一帧，默认
- parity 假定输入的交错视频进行了图像场奇偶校验
  - 0, tff 假定顶部场优先
  - 1, bff 假定底部场优先
  - -1, auto 自动检测场奇偶校验，默认，如果隔行扫描是未知的，或者解码器未导出此信息，则将假定顶场优先。
- deint 指定反交错的帧
  - 0, all 默认，全部
  - 1, interlaced 仅反交错帧标记为隔行扫描

### 示例

```python
_ = input(src).bwdif(mode=0, parity=0, deint=0).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]bwdif=deint=0:mode=0:parity=0[tag0]" -map [tag0] testdata\media\v0_bwdif.mp4 -y -hide_banner
[1.5152s]
```

#### 对比

肉眼看不出差别。

## cas

> https://ffmpeg.org/ffmpeg-filters.html#cas

对视频流应用对比度自适应锐化滤波器（Contrast Adaptive Sharpen）。

### 参数

- strength 设置锐化强度。 0~1，预设值为0。
- planes 设置通道。

### 示例

```python
_ = input(src).cas(strength=1).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]cas=strength=1[tag0]" -map [tag0] testdata\media\v0_cas.mp4 -y -hide_banner
[2.2220s]
```

#### 对比

[视频对比链接]

## chromahold

> https://ffmpeg.org/ffmpeg-filters.html#chromahold

删除除某些颜色以外的所有颜色的所有颜色信息。

### 参数

- color 不会被中性色度取代的颜色。
- similarity 与上述颜色的相似度百分比。 0.01 仅匹配确切的键色，而 1.0 匹配所有键色。
- blend 混合百分比。 0.0 使像素要么全灰，要么根本不灰。 值越高，保留的颜色越多。
- yuv 表示通过的颜色已经是 YUV 而不是 RGB。启用此功能后，文字颜色（如“green”或“red”）不再有意义。 这可以用来传递确切的 YUV 值作为十六进制数。

### 示例

```python
_ = input(src).chromahold(color="white", similarity=0.03).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]chromahold=color=white:similarity=0.03[tag0]" -map [tag0] testdata\media\v0_chromahold.mp4 -y -hide_banner
[1.6571s]
```

#### 对比

[视频对比链接]

## chromakey

> https://ffmpeg.org/ffmpeg-filters.html#chromakey

YUV 颜色空间颜色/色度键控。用途之一就是从绿幕背景视频中提取人物合成到其他视频中。

### 参数

- color 将被透明取代的颜色。
- similarity 与上述颜色的相似度百分比。 0.01 仅匹配确切的键色，而 1.0 匹配所有键色。
- blend 混合百分比。 0.0 使像素要么全透明，要么根本不透明。 较高的值会导致半透明像素，像素的颜色越接近关键颜色的透明度越高。
- yuv 表示通过的颜色已经是 YUV 而不是 RGB。启用此功能后，文字颜色（如“green”或“red”）不再有意义。 这可以用来传递确切的 YUV 值作为十六进制数。

### 示例

```python
_ = input(src).chromakey(color="gray", similarity=0.02).output(dst).run()
```

```
ffmpeg -i testdata\i3.png -filter_complex "[0]chromakey=color=gray:similarity=0.02[tag0]" -map [tag0] testdata\media\v1_chromakey.png -y -hide_banner
```

#### 对比

[视频对比链接]

## chromanr

> https://ffmpeg.org/ffmpeg-filters.html#chromanr

降低色度噪点。

### 参数

- thres 设置平均色度值的阈值。低于该阈值的当前像素和相邻像素的 Y，U 和 V 像素分量的绝对差之和将用于平均。亮度分量保持不变，并复制到输出。默认值为 30。允许的范围是 1 到 200。
- sizew 设置用于平均的矩形的水平半径。允许范围是 1 到 100。默认值是 5。
- sizeh 设置用于平均的矩形的垂直半径。允许范围是 1 到 100。默认值是 5。
- stepw 平均时设置水平步长。默认值为 1。允许的范围是 1 到 50。对加速过滤很有用。
- steph 平均时设置垂直步长。默认值为 1。允许的范围是 1 到 50。对加速过滤很有用。
- threy 设置 Y 阈值以平均色度值。为当前像素和近邻像素的 Y 分量之间的最大允许差异设置更好的控制。默认值为 200。允许的范围是 1 到 200。
- threu 设置 U 阈值以平均色度值。为当前像素和近邻像素的 U 分量之间的最大允许差异设置更好的控制。默认值为 200。允许的范围是 1 到 200。
- threv 设置 V 阈值以平均色度值。为当前像素和近邻像素的 V 分量之间的最大允许差异设置更好的控制。默认值为 200。允许的范围是 1 到 200。

### 示例

```python
_ = input(src).chromanr(thres=100, sizew=20).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]chromanr=sizew=20:thres=100[tag0]" -map [tag0] testdata\media\v0_chromanr.mp4 -y -hide_banner
[1.6579s]
```

#### 对比

差别不明显。

## chromashift

> https://ffmpeg.org/ffmpeg-filters.html#chromashift

水平和/或垂直移动色度像素。

### 参数

- cbh 设置数量以水平移动蓝色色度 chroma-blue。
- cbv 同上垂直
- crh 设置数量以水平移动红色色度 chroma-red。
- crv 同上垂直
- edge 设置边缘模式：smear, default, warp

### 示例

```python
_ = input(src).chromashift(cbh=100, cbv=-100, crh=100, crv=-100).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]chromashift=cbh=100:cbv=-100:crh=100:crv=-100[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_chromashift.mp4 -y -hide_banner
[1.2807s]
```

> 这里开启了 Cuda 加速设置，之后也是默认开启加速。

#### 对比

[视频对比链接]

## ciescope

> https://ffmpeg.org/ffmpeg-filters.html#ciescope

显示覆盖像素的 CIE 彩色图表。

### 参数

- system 设置颜色系统
  - ‘ntsc, 470m’
  - ‘ebu, 470bg’
  - ‘smpte’
  - ‘240m’
  - ‘apple’
  - ‘widergb’
  - ‘cie1931’
  - ‘rec709, hdtv’
  - ‘uhdtv, rec2020’
  - ‘dcip3’
- cie 设置 CIE 系统
  - ‘xyy’
  - ‘ucs’
  - ‘luv’
- gamuts 设置要绘制的色域
- size 设置 ciescope 大小，默认情况下设置为 512
- intensity 设置用于将输入像素值映射到 CIE 图的强度
- contrast 设置对比度以绘制超出主动色彩系统色域的颜色
- corrgamma 正确显示范围的伽玛，默认启用
- showwhite 显示 CIE 图上的白点，默认禁用
- gamma 设置输入伽玛。 仅与 XYZ 输入色彩空间一起使用

### 示例

```python
_ = input(src).ciescope(size=1024, intensity=1, contrast=1).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]ciescope=contrast=1:intensity=1:size=1024[tag0]" -map [tag0] testdata\media\v0_ciescope.mp4 -y -hide_banner
[2.4198s]
```

> 生成的视频不支持 10 bit 编码，无法进行 Cuda 加速。

#### 对比

[视频对比链接]

## codecview

> https://ffmpeg.org/ffmpeg-filters.html#codecview

可视化某些编解码器导出的信息。

某些编解码器可以使用边数据或其他方式通过帧导出信息。 例如，某些基于 MPEG 的编解码器通过编解码器 flags2 选项中的 export_mvs 标志导出运动矢量。

### 参数

- mv 设置运动矢量进行可视化
  - ‘pf’ P-frames 前向预测
  - ‘bf’ B-frames 前向预测
  - ‘bb’ B-frames 后向预测
- qp 使用色度通道显示量化参数
- mv_type 设置运动矢量类型以使其可视化。 包括所有帧的 MV，除非 frame_type 选项指定。
  - ‘fp’ 前向预测
  - ‘bp’ 后向预测
- frame_type 设置帧类型以可视化运动矢量
  - ‘if’ I-frames
  - ‘pf’ P-frames
  - ‘bf’ B-frames

### 示例

```python
_ = input(src).codecview(mv_type="fp").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]codecview=mv_type=fp[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_codecview.mp4 -y -hide_banner
[1.7066s]
```

#### 对比

这个命令似乎是只属于 FFplay 的，用 FFmpeg 处理后无差别。

```shell
ffplay -flags2 +export_mvs testdata\media\0.mp4 -vf codecview
=mv=pf+bf+bb
```

## colorbalance

> https://ffmpeg.org/ffmpeg-filters.html#colorbalance

修改输入框的原色（红色，绿色和蓝色）的强度。

滤镜允许在阴影，中间调或高光区域中调整输入框，以实现红蓝，绿洋红或蓝黄色平衡。

正调整值会将平衡移向原色，负调整值将移向互补色。

### 参数

- rs
- gs
- bs 调整红色，绿色和蓝色阴影（最暗的像素）
- rm
- gm
- bm 调整红色，绿色和蓝色中间色调（中等像素）
- rh
- gh
- bh 调整红色，绿色和蓝色高光（最亮的像素），允许的选项范围为 [-1.0, 1.0]。默认值是 0
- pl 更改色彩平衡时保持亮度， 默认设置为禁用

### 示例

```python
_ = input(src).colorbalance(rs=0.3).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorbalance=rs=0.3[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorbalance.mp4 -y -hide_banner
[1.9180s]
```

#### 对比

[视频对比链接]

## colorcontrast

> https://ffmpeg.org/ffmpeg-filters.html#colorcontrast

调整 RGB 组件之间的颜色对比度。

### 参数

- rc 设置红-青对比度。默认值为 0.0。允许的范围是 -1.0 到 1.0。
- gm 设置绿色-品红对比度。默认值为 0.0。允许的范围是 -1.0 到 1.0。
- by 设置蓝-黄对比度。默认值为 0.0。允许的范围是 -1.0 到 1.0。
- rcw
- gmw
- byw 通过选项值设置每个 rc 的权重 gm。默认值为 0.0。允许范围是 0.0 到 1.0。如果所有权重均为 0.0，则禁用过滤。
- pl 设置保存亮度。默认值为 0.0。允许范围是 0.0 到 1.0。

### 示例

No such filter: 'colorcontrast'

官网英文文档虽然还有这个滤镜的说明，但最新版找不到这个滤镜，Google 也找不到这个滤镜的信息，可能已经移除？

## colorcorrect

> https://ffmpeg.org/ffmpeg-filters.html#colorcorrect

有选择地调整彩色白平衡。 该滤镜在 YUV 色彩空间中运行。

### 参数

- rl 设置红色阴影点。允许的范围是 -1.0 到 1.0。预设值为 0。
- bl 设置蓝色阴影点。允许的范围是 -1.0 到 1.0。预设值为 0。
- rh 设置红色高光点。允许的范围是 -1.0 到 1.0。预设值为 0。
- bh 设置红色高光点。允许的范围是 -1.0 到 1.0。预设值为 0。
- saturation 设置饱和度。允许范围是 -3.0 到 3.0。预设值为 1。

### 示例

No such filter: 'colorcorrect'

官网英文文档虽然还有这个滤镜的说明，但最新版找不到这个滤镜，Google 也找不到这个滤镜的信息，可能已经移除？

## colorchannelmixer

> https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer

通过重新混合颜色通道来调整视频输入帧。

该滤镜通过添加与相同像素的其他通道关联的值来修改颜色通道。 例如，如果要修改的值为红色，则输出值为：

```
red=red*rr + blue*rb + green*rg + alpha*ra
```

### 参数

- rr
- rg
- rb
- ra 调整输入红色，绿色，蓝色和 Alpha 通道对输出红色通道的贡献。rr 的默认值为 1，rg，rb 和 ra 的默认值为 0。
- gr
- gg
- gb
- ga 调整输入红色，绿色，蓝色和 Alpha 通道对输出绿色通道的贡献。gg 的默认值为 1，gr，gb 和 ga 的默认值为 0。
- br
- bg
- bb
- ba 调整输入红色，绿色，蓝色和 Alpha 通道对输出蓝色通道的贡献。bb 的默认值为 1，而 br，bg 和 ba 的默认值为 0。
- ar
- ag
- ab
- aa 调整输入红色，绿色，蓝色和 Alpha 通道对输出 Alpha 通道的贡献。aa 的默认值为 1，ar，ag 和 ab 的默认值为 0。

以上参数范围：[-2.0, 2.0]

- pl 更改颜色时保持亮度。允许的范围是 [0.0, 1.0]。默认值为 0.0，相当于禁用。

### 示例

#### 转换为灰度

```python
_ = input(src).colorchannelmixer(.3, .4, .3, 0, .3, .4, .3, 0, .3, .4, .3).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorchannelmixer=0.3:0.4:0.3:0:0.3:0.4:0.3:0:0.3:0.4:0.3[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorchannelmixer.mp4 -y -hide_banner
[0.4375s]
```

### 棕褐色调

```python
_ = input(src).colorchannelmixer(.393,.769,.189,0,.349,.686,.168,0,.272,.534,.131).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorchannelmixer=0.393:0.769:0.189:0:0.349:0.686:0.168:0:0.272:0.534:0.131[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorchannelmixer.mp4 -y -hide_banner
[0.4482s]
```

#### 对比

[视频对比链接]

## colorize

> https://ffmpeg.org/ffmpeg-filters.html#colorize

在视频流上覆盖纯色。

### 参数

- hue 设置色调。允许的范围是 0 到 360。默认值为 0。
- saturation 设置色彩饱和度。允许范围是 0 到 1。默认值是 0.5。
- lightness 设置颜色亮度。允许范围是 0 到 1。默认值为 0.5。
- mix 设置光源亮度的混合。默认情况下设置为 1.0。允许范围是 0.0 到 1.0。

### 示例

No such filter: 'colorcorrect'

官网英文文档虽然还有这个滤镜的说明，但最新版找不到这个滤镜，可能已经移除？

## colorkey

> https://ffmpeg.org/ffmpeg-filters.html#colorkey

RGB 色彩空间颜色键控。

### 参数

- color 将被替换为透明的颜色。
- similarity 与关键颜色的相似性百分比。0.01 仅匹配确切的键色，而 1.0 匹配所有键色。
- blend 混合百分比。0.0 使像素完全透明或完全不透明。较高的值会导致半透明像素，而透明度越高，像素颜色与键颜色越相似。

### 示例

```python
_ = input(src).colorkey(color="white", similarity=0.02, blend=0).output(dst).run()
```

```
ffmpeg -i testdata\i3.png -filter_complex "[0]colorkey=blend=0:color=white:similarity=0.02[tag0]" -map [tag0] testdata\media\i3_colorkey.png -y -hide_banner
[0.0732s]
```

#### 对比

黑色部分为透明。

[视频对比链接]

## colorhold

> https://ffmpeg.org/ffmpeg-filters.html#colorhold

移除除特定颜色外的所有 RGB 颜色的所有颜色信息。

### 参数

- color 不会被中性灰色替代的颜色。
- similarity 与上述颜色的相似度百分比。 0.01 仅匹配确切的键色，而 1.0 匹配所有键色。
- blend 混合百分比。 0.0 使像素要么全灰，要么根本不灰。 值越高，保留的颜色越多。

### 示例

```python
_ = input(src).colorhold(color="red", similarity=0.05, blend=0.2).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorhold=blend=0.2:color=red:similarity=0.05[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorhold.mp4 -y -hide_banner
[0.5202s]
```

#### 对比

[视频对比链接]

## colorlevels

> https://ffmpeg.org/ffmpeg-filters.html#colorlevels

用电平调整视频输入帧。

### 参数

rimin
gimin
bimin
aimin 调整红，绿，蓝和 alpha 输入黑点。允许的选项范围为 [-1.0,1.0]。默认值是 0。
rimax
gimax
bimax
aimax 调整红，绿，蓝和 alpha 输入白点。允许的选项范围为 [-1.0,1.0]。默认值是 1。输入级别用于亮化高光 ( 亮色调 )，暗阴影 ( 暗色调 )，改变明暗色调的平衡。
romin
gomin
bomin
aomin 调整红，绿，蓝和输出黑点。允许的选项范围是 [0,1.0]。默认值是 0。
romax
gomax
bomax
aomax 调整红，绿，蓝和 alpha 输出白点。允许的选项范围是 [0,1.0]。默认值是 1。输出电平允许手动选择一个受限的输出电平范围。

### 示例

#### 画面变暗

```python
_ = input(src).colorlevels(rimin=0.558, gimin=0.058, bimin=0.058).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorlevels=bimin=0.058:gimin=0.058:rimin=0.558[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorlevels1.mp4 -y -hide_banner
[0.4217s]
```

#### 增加对比度

```python
_ = input(src).colorlevels(rimin=0.39, gimin=0.39, bimin=0.39, rimax=0.6,
                           gimax=0.6, bimax=0.6).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorlevels=bimax=0.6:bimin=0.39:gimax=0.6:gimin=0.39:rimax=0.6:rimin=0.39[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorlevels2.mp4 -y -hide_banner
[1.5766s]
```

#### 画面变亮

```python
_ = input(src).colorlevels(rimax=0.602, gimax=0.602, bimax=0.602).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorlevels=bimax=0.602:gimax=0.602:rimax=0.602[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorlevels3.mp4 -y -hide_banner
[1.5676s]
```

#### 增加明亮度

```python
_ = input(src).colorlevels(romin=0.5, gomin=0.5, bomin=0.5).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorlevels=bomin=0.5:gomin=0.5:romin=0.5[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorlevels4.mp4 -y -hide_banner
[1.6679s]
```

#### 对比

[视频对比链接]

## colormatrix

> https://ffmpeg.org/ffmpeg-filters.html#colormatrix

转换色彩矩阵。

### 参数

- src
- dst 指定源和目标颜色矩阵。 必须同时指定这两个值。
  - ‘bt709’ BT.709
  - ‘fcc’ FCC
  - ‘bt601’ BT.601
  - ‘bt470’ BT.470
  - ‘bt470bg’ BT.470BG
  - ‘smpte170m’ SMPTE-170M
  - ‘smpte240m’ SMPTE-240M
  - ‘bt2020’ BT.2020

### 示例

```python
_ = input(src).colormatrix("bt601","smpte240m").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colormatrix=bt601:smpte240m[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colormatrix.mp4 -y -hide_banner
[0.4466s]
```

#### 对比

[视频对比链接]

## colorspace

> https://ffmpeg.org/ffmpeg-filters.html#colorspace

转换色彩空间，转印特性或色彩原色。 输入视频的大小必须均匀。

### 参数

- all 一次指定所有颜色属性。
  - ‘bt470m’ BT.470M
  - ‘bt470bg’ BT.470BG
  - ‘bt601-6-525’ BT.601-6 525
  - ‘bt601-6-625’ BT.601-6 625
  - ‘bt709’ BT.709
  - ‘smpte170m’ SMPTE-170M
  - ‘smpte240m’ SMPTE-240M
  - ‘bt2020’ BT.2020

- space 指定输出色彩空间。
  - ‘bt709’ BT.709
  - ‘fcc’ FCC
  - ‘bt470bg’ BT.470BG or BT.601-6 625
  - ‘smpte170m’ SMPTE-170M or BT.601-6 525
  - ‘smpte240m’ SMPTE-240M
  - ‘ycgco’ YCgCo
  - ‘bt2020ncl’ BT.2020 with non-constant luminance

- trc 指定输出传输特性。
  - ‘bt709’ BT.709
  - ‘bt470m’ BT.470M
  - ‘bt470bg’ BT.470BG
  - ‘gamma22’ Constant gamma of 2.2
  - ‘gamma28’ Constant gamma of 2.8
  - ‘smpte170m’ SMPTE-170M, BT.601-6 625 or BT.601-6 525
  - ‘smpte240m’ SMPTE-240M
  - ‘srgb’ SRGB
  - ‘iec61966-2-1’ iec61966-2-1
  - ‘iec61966-2-4’ iec61966-2-4
  - ‘xvycc’ xvycc
  - ‘bt2020-10’ BT.2020 for 10-bits content
  - ‘bt2020-12’ BT.2020 for 12-bits content

- primaries 指定输出颜色原色。
  - ‘bt709’ BT.709
  - ‘bt470m’ BT.470M
  - ‘bt470bg’ BT.470BG or BT.601-6 625
  - ‘smpte170m’ SMPTE-170M or BT.601-6 525
  - ‘smpte240m’ SMPTE-240M
  - ‘film’ film
  - ‘smpte431’ SMPTE-431
  - ‘smpte432’ SMPTE-432
  - ‘bt2020’ BT.2020
  - ‘jedec-p22’ JEDEC P22 phosphors

- range 指定输出颜色范围。
  - ‘tv’ TV (restricted) range
  - ‘mpeg’ MPEG (restricted) range
  - ‘pc’ PC (full) range
  - ‘jpeg’ JPEG (full) range

- format 指定输出颜色格式。
  - ‘yuv420p’ YUV 4:2:0 planar 8-bits
  - ‘yuv420p10’ YUV 4:2:0 planar 10-bits
  - ‘yuv420p12’ YUV 4:2:0 planar 12-bits
  - ‘yuv422p’ YUV 4:2:2 planar 8-bits
  - ‘yuv422p10’ YUV 4:2:2 planar 10-bits
  - ‘yuv422p12’ YUV 4:2:2 planar 12-bits
  - ‘yuv444p’ YUV 4:4:4 planar 8-bits
  - ‘yuv444p10’ YUV 4:4:4 planar 10-bits
  - ‘yuv444p12’ YUV 4:4:4 planar 12-bits

- fast 进行快速转换，从而跳过 gamma/primary 校正。 这将大大减少 CPU 的使用，但是在数学上是不正确的。 要使输出与由 colormatrix 滤镜产生的输出兼容，请使用 fast = 1。

- dither 指定抖动模式。
  - ‘none’ 无
  - ‘fsb’ Floyd-Steinberg 抖动

- wpadapt 白点适应模式。
  - ‘bradford’ Bradford
  - ‘vonkries’ von Kries
  - ‘identity’ identity

iall 一次覆盖所有输入属性。与 all 相同的接受值。
ispace 覆盖输入色彩空间。与 space 相同的接受值。
iprimaries 覆盖输入颜色原色。接受的值与 primaries 相同。
itrc 覆盖输入传输特性。与 trc 相同的接受值。
irange 覆盖输入颜色范围。与 range 相同的接受值。

过滤器将转印特性，颜色空间和颜色原色转换为指定的用户值。 如果未指定，则输出值将基于 “all” 属性设置为默认值。 如果也未指定该属性，则过滤器将记录错误。 默认情况下，输出颜色范围和格式与输入颜色范围和格式的值相同。 输入传输特性，颜色空间，颜色原色和颜色范围应在输入数据上设置。 如果缺少任何这些，过滤器将记录一个错误，并且不会进行任何转换。

### 示例

```python
_ = input(src).colorspace("smpte240m").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]colorspace=smpte240m[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_colorspace.mp4 -y -hide_banner

Unsupported input primaries 2 (unknown)
```

报错，另外不太理解这个滤镜，今后如果涉及再补。

## colortemperature

> https://ffmpeg.org/ffmpeg-filters.html#colortemperature

调整视频中的色温以模拟环境色温的变化。

### 参数

- temperature 以开氏温度设置温度。允许的范围是 1000 到 40000。默认值是 6500K。
- mix 设置混合并过滤输出。允许范围是 0 到 1。默认值为 1。
- pl 设置保留亮度。允许的范围是 0 到 1。默认值是 0。

### 示例

No such filter: 'colortemperature'

官网英文文档虽然还有这个滤镜的说明，但最新版找不到这个滤镜，可能已经移除？

## convolution

> https://ffmpeg.org/ffmpeg-filters.html#convolution

应用 3x3、5x5、7x7 或水平/垂直（最多 49 个元素）的卷积。

### 参数

- 0m
- 1m
- 2m
- 3m 为每个通道设置矩阵。矩阵在方模式下是 9、25 或 49 个有符号整数的序列，在行模式下是 1 到 49 个奇数个有符号整数的序列。

- 0rdiv
- 1rdiv
- 2rdiv
- 3rdiv 为每个通道的计算值设置乘数。如果未设置或为 0，则它​​将是所有矩阵元素的总和。

- 0bias
- 1bias
- 2bias
- 3bias 为每个通道设置偏差。该值被加到相乘的结果上。用于使整个图像更亮或更暗。默认值为 0.0。

- 0mode
- 1mode
- 2mode
- 3mode 为每个通道设置矩阵模式。可以是 square, row, column。默认为 square。

### 示例

#### 锐化

```python
_ = input(src).convolution(
        "0 -1 0 -1 5 -1 0 -1 0",
        "0 -1 0 -1 5 -1 0 -1 0",
        "0 -1 0 -1 5 -1 0 -1 0",
        "0 -1 0 -1 5 -1 0 -1 0"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0m=0 -1 0 -1 5 -1 0 -1 0:1m=0 -1 0 -1 5 -1 0 -1 0:2m=0 -1 0 -1 5 -1 0 -1 0:3m=0 -1 0 -1 5 -1 0 -1 0[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution1.mp4 -y -hide_banner
[0.4257s]
```

#### 对比

[视频对比链接]

#### 模糊

```python
_ = input(src).convolution(
        "1 1 1 1 1 1 1 1 1",
        "1 1 1 1 1 1 1 1 1",
        "1 1 1 1 1 1 1 1 1",
        "1 1 1 1 1 1 1 1 1",
        "1/9", "1/9", "1/9", "1/9"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0m=1 1 1 1 1 1 1 1 1:0rdiv=1/9:1m=1 1 1 1 1 1 1 1 1:1rdiv=1/9:2m=1 1 1 1 1 1 1 1 1:2rdiv=1/9:3m=1 1 1 1 1 1 1 1 1:3rdiv=1/9[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution2.mp4 -y -hide_banner
[0.3846s]
```

#### 对比

[视频对比链接]

#### 边缘强化

```python
_ = input(src).convolution(
        "0 0 0 -1 1 0 0 0 0",
        "0 0 0 -1 1 0 0 0 0",
        "0 0 0 -1 1 0 0 0 0",
        "0 0 0 -1 1 0 0 0 0",
        "5", "1", "1", "1", "0",
        "128", "128", "128"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0bias=0:0m=0 0 0 -1 1 0 0 0 0:0rdiv=5:1bias=128:1m=0 0 0 -1 1 0 0 0 0:1rdiv=1:2bias=128:2m=0 0 0 -1 1 0 0 0 0:2rdiv=1:3bias=128:3m=0 0 0 -1 1 0 0 0 0:3rdiv=1[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution3.mp4 -y -hide_banner
[0.3373s]
```

#### 对比

[视频对比链接]

#### 边缘检测

```python
_ = input(src).convolution(
        "0 1 0 1 -4 1 0 1 0",
        "0 1 0 1 -4 1 0 1 0",
        "0 1 0 1 -4 1 0 1 0",
        "0 1 0 1 -4 1 0 1 0",
        "5", "5", "5", "1", "0",
        "128", "128", "128"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0bias=0:0m=0 1 0 1 -4 1 0 1 0:0rdiv=5:1bias=128:1m=0 1 0 1 -4 1 0 1 0:1rdiv=5:2bias=128:2m=0 1 0 1 -4 1 0 1 0:2rdiv=5:3bias=128:3m=0 1 0 1 -4 1 0 1 0:3rdiv=1[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution4.mp4 -y -hide_banner
[0.3418s]
```

#### 对比

[视频对比链接]

#### 包括对角线的拉普拉斯边缘检测

```python
_ = input(src).convolution(
        "1 1 1 1 -8 1 1 1 1",
        "1 1 1 1 -8 1 1 1 1",
        "1 1 1 1 -8 1 1 1 1",
        "1 1 1 1 -8 1 1 1 1",
        "5", "5", "5", "1", "0",
        "128", "128", "0"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0bias=0:0m=1 1 1 1 -8 1 1 1 1:0rdiv=5:1bias=128:1m=1 1 1 1 -8 1 1 1 1:1rdiv=5:2bias=128:2m=1 1 1 1 -8 1 1 1 1:2rdiv=5:3bias=0:3m=1 1 1 1 -8 1 1 1 1:3rdiv=1[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution5.mp4 -y -hide_banner
[0.3472s]
```

#### 对比

[视频对比链接]

#### 浮雕效果

```python
_ = input(src).convolution(
        "-2 -1 0 -1 1 1 0 1 2",
        "-2 -1 0 -1 1 1 0 1 2",
        "-2 -1 0 -1 1 1 0 1 2",
        "-2 -1 0 -1 1 1 0 1 2"). \
    output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]convolution=0m=-2 -1 0 -1 1 1 0 1 2:1m=-2 -1 0 -1 1 1 0 1 2:2m=-2 -1 0 -1 1 1 0 1 2:3m=-2 -1 0 -1 1 1 0 1 2[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_convolution6.mp4 -y -hide_banner
[0.3639s]
```

#### 对比

[视频对比链接]

## convolve

> https://ffmpeg.org/ffmpeg-filters.html#convolve

使用第二流作为脉冲在频域中应用视频流的 2D 卷积。

### 参数

- planes 设置通道
- impulse 设置将处理哪些脉冲视频帧，first/all，默认 all

### 示例

不懂，太专业了，素材也不好找。

## copy

> https://ffmpeg.org/ffmpeg-filters.html#copy

将输入视频源原样复制到输出。

### 参数

无。

### 示例

```python
_ = input(src).copy().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]copy[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_copy.mp4 -y -hide_banner
```

## coreimage

> https://ffmpeg.org/ffmpeg-filters.html#coreimage

在 Apple OSX 上使用 Apple 的 CoreImage API 在 GPU 上进行视频过滤。

硬件加速基于 OpenGL 上下文。通常，这意味着它是由视频硬件处理的。但是，存在基于软件的 OpenGL 实现，这意味着无法保证硬件处理。这取决于各自的 OSX。

Apple 提供了许多滤镜和图像生成器，其中包含多种选择。过滤器必须通过其名称及其选项进行引用。

无 Apple OSX 设备，略过。

## cover_rect

> https://ffmpeg.org/ffmpeg-filters.html#cover_rect

覆盖一个矩形对象。

### 参数

- cover 可选封面图片的文件路径，必须是 yuv420。
- mode 覆盖模式。
  - cover 用提供的图像覆盖
  - blur 通过插值周围的像素覆盖

### 示例

找不到素材，暂略。

## crop

> https://ffmpeg.org/ffmpeg-filters.html#crop

将输入视频裁剪为给定的尺寸。

### 参数

- w, out_w 输出视频的宽度。默认为 iw。在过滤器配置期间，或者在发送 “w” 或 “out_w” 命令时，该表达式仅计算一次。
- h, out_h 输出视频的高度。默认为 ih。在过滤器配置过程中，或者在发送 “h” 或 “out_h” 命令时，该表达式仅计算一次。w,h 表达式可以包含以下变量：
  - x 
  - y x 和 y 的计算值，每一帧都会被计算
  - in_w
  - in_h 输入的宽度和高度
  - iw
  - ih 与 in_w 和 in_h 相同
  - out_w
  - out_h 输出（裁剪）的宽度和高度
  - ow
  - oh 与 out_w 和 out_h 相同
  - a 与 iw / ih 相同
  - sar 输入样本宽高比
  - dar 输入显示宽高比，与 (iw/ih) * sar 相同
  - hsub
  - vsub 水平和垂直色度子样本值。例如，对于像素格式 “yuv422p”，hsub 为 2，vsub 为 1。
  - n 输入帧的编号，从 0 开始。
  - pos 输入框在文件中的位置，如果未知，则为 NAN
  - t 时间戳记，以秒为单位。 如果输入的时间戳未知，则为 NAN。

- x 输入视频中输出视频左边缘的水平位置。默认为 (in_w-out_w)/2。每帧评估该表达式。
- y 输入视频中输出视频顶部边缘的垂直位置。默认为 (in_h-out_h)/2。每帧评估该表达式。
- keep_aspect 如果设置为 1，则通过更改输出样本的宽高比，将使输出显示的宽高比与输入相同。默认为 0。
- exact 启用精确裁剪。如果启用，则将按照指定的确切宽度 / 高度 / x / y 裁剪子采样视频，并且不会四舍五入到最接近的较小值。默认为 0。

out_w 的表达式可能取决于 out_h 的值，out_h 的表达式可能取决于 out_w，但是它们不能取决于 x 和 y，因为 x 和 y 在 out_w 和 out_h 之后求值。

x 和 y 参数指定输出（非裁剪）区域左上角位置的表达式。将对每个帧进行评估。如果评估值无效，则将其近似为最接近的有效值。

x 的表达式可能取决于 y，而 y 的表达式可能取决于 x。

### 示例

```python
_ = input(src).crop("in_w/2","in_h/2","in_w/2","in_h/2").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]crop=in_w/2:in_h/2:in_w/2:in_h/2[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_crop01.mp4 -y -hide_banner
[0.3990s]
```

#### 对比

[视频对比链接]

## cropdetect

> https://ffmpeg.org/ffmpeg-filters.html#cropdetect

自动检测裁剪大小。计算必要的裁剪参数，并通过记录系统打印推荐的参数。 检测到的尺寸对应于输入视频的非黑色区域。

### 参数

- limit 设置较高的黑色值阈值，可以选择从零到所有值（对于 8 位格式为 255 ）进行指定。大于设定值的强度值被认为是非黑色的。默认值为 24。您还可以指定一个介于 0.0 和 1.0 之间的值，该值将根据像素格式的位深进行缩放。
- round 宽度 / 高度应被其整除的值。默认值为 16。偏移量会自动调整为使视频居中。使用 2 仅获得均匀尺寸。对大多数视频编解码器进行编码时，最好使用 16。
- skip 设置跳过评估的初始帧数。默认值为 2。范围为 0 到 INT_MAX。最新版本 Option 'skip' not found。
- reset_count, reset 设置计数器，该计数器确定 cropdetect 将在多少帧后重置之前检测到的最大视频区域，然后重新开始以检测当前的最佳作物区域。预设值为 0。当频道徽标使视频区域失真时，此功能很有用。0 表示 “从不重置 ”，并返回播放期间遇到的最大区域。


### 示例

```python
_ = input(src).cropdetect(limit=200, round=20,  reset_count=0).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]crop=in_w/2:in_h/2:in_w/2:in_h/2[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_crop01.mp4 -y -hide_banner
[0.3990s]
```

#### 对比

仅是打印了相关参数，对于合成视频无影响。

## cue

> https://ffmpeg.org/ffmpeg-filters.html#cue

将视频过滤延迟到给定的时钟时间戳。过滤器首先传递预滚动帧数，然后最多缓冲所有帧缓冲数并等待提示。到达提示后，它转发缓冲的帧以及输入中的任何后续帧。

该过滤器可用于同步多个 ffmpeg 进程的输出，以便实时输出设备（如 decklink ）。通过将延迟置于过滤链和预缓冲帧中，该过程可以将数据传递到几乎达到目标时钟时间戳记之后立即输出。

不能保证完美的帧精度，但是对于某些用例来说，结果是足够好的。

### 参数

- cue 提示时间戳记，以 UNIX 时间戳记表示，以微秒为单位。默认值为 0。
- preroll 要传递的内容持续时间（以秒为单位）作为预卷。默认值为 0。
- buffer 等待提示之前要缓冲的内容的最大持续时间（以秒为单位）。默认值为 0。

### 示例

不太懂，暂略。

## curves

> https://ffmpeg.org/ffmpeg-filters.html#curves

根据曲线函数调整颜色。

该滤镜类似于 Adobe Photoshop 和 GIMP 曲线工具。每个组件（红色，绿色和蓝色）的值均由 N 个关键点定义，它们使用平滑曲线相互关联。x 轴表示来自输入帧的像素值，y 轴表示要为输出帧设置的新像素值。

默认情况下，分量曲线由两个点（0;0）和（1;1）定义。这将创建一条直线，其中每个原始像素值都被“调整”为其自己的值，这意味着图像不会发生变化。

过滤器使您可以重新定义这两点并添加更多内容。将定义一条新曲线（使用自然三次样条插值法）以平滑地通过所有这些新坐标。新定义的点必须在 x 轴上严格增加，并且它们的 x 和 y 值必须在 [0;1] 区间内。如果计算出的曲线恰好在向量空间之外，则将相应地剪切值。

### 参数

- preset 选择一种可用的颜色预设。 除了 r/g/b 参数外，还可以使用此选项。 在这种情况下，后面的选项优先于预设值。
  - ‘none’ 默认
  - ‘color_negative’
  - ‘cross_process’
  - ‘darker’
  - ‘increase_contrast’
  - ‘lighter’
  - ‘linear_contrast’
  - ‘medium_contrast’
  - ‘negative’
  - ‘strong_contrast’
  - ‘vintage’
- master 设置主控关键点。 这些点将定义第二遍映射。 有时称为“亮度”或“值”映射。 它可以与 r/g/b/all 一起使用，因为它的作用类似于后处理 LUT。
- red 设置红色组件的关键点。
- green 同上
- blue 同上
- all 设置所有组件的关键点（不包括主组件）。 除其他关键点组件选项外，还可以使用。 在这种情况下，未设置的组件将在全部设置后退。
- psfile 指定要从中导入设置的 Photoshop 曲线文件（.acv）。
- plot 将曲线的 Gnuplot 脚本保存在指定文件中。

为了避免某些 filtergraph 语法冲突，需要使用以下语法定义每个关键点列表：

```
x0/y0 x1/y1 x2/y2
```

### 示例

#### 稍微增加蓝色的中间水平

```python
_ = input(src).curves(blue='0/0 0.5/0.58 1/1').output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]curves=blue=0/0 0.5/0.58 1/1[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_curves1.mp4 -y -hide_banner
[0.6140s]
```

#### 对比

[视频对比链接]

#### 复古效果

```python
_ = input(src).curves(
        red='0/0.11 .42/.51 1/0.95',
        green='0/0 0.50/0.48 1/1',
        blue='0/0.22 .49/.44 1/0.8'
).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]curves=blue=0/0.22 .49/.44 1/0.8:green=0/0 0.50/0.48 1/1:red=0/0.11 .42/.51 1/0.95[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_curves2.mp4 -y -hide_banner
[0.4459s]
```

这个例子也可以用预设值实现：

```python
_ = input(src).curves(preset="vintage").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]curves=preset=vintage[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_curves3.mp4 -y -hide_banner
[1.1474s]
```

#### 对比

[视频对比链接]

## datascope

> https://ffmpeg.org/ffmpeg-filters.html#datascope

视频数据分析过滤器。

此过滤器显示部分视频的十六进制像素值。

### 参数

- size 设置输出视频大小。
- x 设置从哪里拾取像素的x偏移量。
- y 设置从像素拾取位置的y偏移。
- mode 设定范围模式：
  - mono 在黑色背景上绘制带有白色的十六进制像素值。
  - color 在黑色背景上用输入的视频像素颜色绘制十六进制像素值。
  - color2 在从输入视频中拾取的彩色背景上绘制十六进制像素值，以这种方式拾取文本颜色，使其始终可见。
- axis 在视频的左侧和顶部绘制行号和列号。
- opacity 设置背景不透明度。
- format 设置显示编号格式。hex/dec，默认 hex。
- components 设置要显示的像素分量。 默认情况下，显示所有像素分量。

### 示例

```python
_ = input(src).datascope(mode="color").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\v0_datascope.mp4 -filter_complex "[0]pad=w=2*iw[tag0];[tag0][1]overlay=x=w[tag1]" -vcodec h264_nvenc -map [tag1] C:\Users\Admin\Videos\contrast\v0_datascope_compare.mp4 -y -hide_banner
[0.5779s]
```

#### 对比

输出的视频全黑，不太懂。

## dblur

> https://ffmpeg.org/ffmpeg-filters.html#dblur

定向模糊滤镜。

### 参数

- angle 设置方向模糊的角度。
- radius 设置方向模糊的半径。
- planes 设置通道。默认全部。

### 示例

```python
_ = input(src).dblur(angle=30, radius=10).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]dblur=angle=30:radius=10[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_dblur.mp4 -y -hide_banner
[1.5746s]
```

#### 对比

[视频对比链接]

## dctdnoiz

> https://ffmpeg.org/ffmpeg-filters.html#dctdnoiz

使用 2D DCT （频域滤波）对帧进行消噪。此过滤器为不是实时系统设计的。

### 参数

- sigma 设置噪声 sigma 常数。此 sigma 定义 3 * sigma 的硬阈值；低于此阈值的每个 DCT 系数（绝对值）都将被丢弃。如果需要更高级的过滤，请参见 expr。默认值为 0。
- overlap 设置每个块的重叠像素数。由于过滤器的速度可能很慢，因此您可能希望降低此值，但代价是效率较低的过滤器和各种伪像的风险。如果重叠的值不允许处理整个输入的宽度或高度，则将显示警告，并且不会对相应的边框进行反色处理。默认值为 blockize-1，这是可能的最佳设置。
- expr 设置系数因子表达式。对于 DCT 块的每个系数，该表达式将被评估为系数的乘数值。如果设置了此选项，则将忽略 sigma 选项。系数的绝对值可通过 c 变量访问。
- n 使用位数设置 blocksize。1 << n 定义 blocksize，即已处理块的宽度和高度。默认值为 3 （ 8x8 ），对于 16x16 的 blocksize，可以将其提高到 4。请注意，更改此设置会对速度处理产生重大影响。同样，更大的 blocksize 并不一定意味着更好的去噪。

### 示例

```python
_ = input(src).dctdnoiz(4.5).output(dst).run()
_ = input(src).dctdnoiz(expr="gte(c, 4.5*3)").output(dst).run() # 等价
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]dctdnoiz=4.5[tag0]" -vcodec h264_nvenc -map [tag0] testdata\media\v0_dctdnoiz1.mp4 -y -hide_banner
[5.9960s]
```

#### 对比

[视频对比链接]

## deband

> https://ffmpeg.org/ffmpeg-filters.html#deband

从输入视频中删除条带失真。 通过将带状像素替换为参考像素的平均值来工作。

### 参数

- 1thr
- 2thr
- 3thr
- 4thr 设置每个通道的条带检测阈值。默认值为 0.02。有效范围是 0.00003 至 0.5。如果当前像素和参考像素之间的差异小于阈值，则将其视为带状。
- range, r 条带检测范围（以像素为单位）。默认值为 16。如果为正，将使用 0 到设置值范围内的随机数。如果为负，将使用确切的绝对值。该范围定义了当前像素周围四个像素的平方。
- direction, d 设置以弧度为单位的方向，将从该方向比较四个像素。如果为正，则将选择从 0 到设置方向的随机方向。如果为负，则将选择绝对值的精确值。例如，方向 0，-PI 或 -2 * PI 弧度将仅选择同一行上的像素，而 -PI / 2 将仅选择同一列上的像素。
- blur, b 如果启用，则将当前像素与所有四个周围像素的平均值进行比较。默认启用。如果禁用，则将当前像素与周围的所有四个像素进行比较。如果只有与周围像素的所有四个差异均小于阈值，则该像素被视为带状。
- coupling, c 如果启用，则当且仅当所有像素分量都被镶边时，例如，才改变当前像素。针对所有颜色分量触发条带检测阈值。默认设置为禁用。

### 示例

```python
_ = input(src).deband(r=32).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]deband=r=32[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_deband.mp4 -y -hide_banner
[1.5303s]
```

#### 对比

[视频对比链接]

## deblock

> https://ffmpeg.org/ffmpeg-filters.html#deblock

从输入视频中删除阻塞的伪像。

### 参数

- filter 设置过滤器类型，可以是弱的或强的。默认值为强。这控制了应用哪种类型的解块。
- block 设置块的大小，允许的范围是 4 到 512。默认值为 8。
- alpha
- beta
- gamma
- delta 设置阻塞检测阈值。允许的范围是 0 到 1。默认值为：alpha 为 0.098，其余为 0.05。使用较高的阈值可提供更多的解块强度。设置 Alpha 控制阈值检测在块的精确边缘。其余选项可控制边缘附近的阈值检测。下方 / 上方或左侧 / 右侧的每个。将其中任何一个设置为 0 将禁用解块。
- planes 设置通道。

### 示例

```python
_ = input(src).deblock(filter="weak", block=4).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]deblock=block=4:filter=weak[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_deblock.mp4 -y -hide_banner
[1.4129s]
```

#### 对比

[视频对比链接]

## decimate

> https://ffmpeg.org/ffmpeg-filters.html#decimate

定期删除重复的帧。

### 参数

- cycle 设置将被删除的帧数。设置为 N 意味着每批 N 帧中的一帧将被删除。默认是 5。
- dupthresh 设置重复检测阈值。如果一个帧的差度量小于或等于这个值，那么它被声明为重复。默认是 1.1
- scthresh 设置场景变化阈值。默认值为 15。
- blockx
- blocky 设置度量标准计算期间使用的 x 和 y 轴块的大小。较大的块可提供更好的噪声抑制，但对小动作的检测也较差。必须是 2 的幂。默认值为 32。
- ppsrc 将主要输入标记为预处理输入，然后激活干净的源输入流。这允许使用各种过滤器对输入进行预处理，以帮助度量计算，同时保持帧选择无损。设置为 1 时，第一个流用于预处理输入，第二个流是干净的源，从中选择保留的帧。默认值为 0。
- chroma 设置在度量标准计算中是否考虑色度。默认值为 1。

### 示例

```python
_ = input(src).decimate(cycle=10).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]decimate=cycle=10[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_decimate.mp4 -y -hide_banner
[0.4016s]
```

#### 对比

[视频对比链接]

## deconvolve

> https://ffmpeg.org/ffmpeg-filters.html#deconvolve

使用第二流作为冲量，在频域中对视频流进行 2D 反卷积。

### 参数

- planes 设置处理通道
- impulse 设置将处理哪些脉冲视频帧，first/all，默认 all
- noise 进行除法时请设置噪音。默认值为 0.0000001。当宽度和高度不相同且不是 2 的幂时，或者在卷积之前的流具有噪声时，此选项很有用

### 示例

不太懂，略。

## dedot

> https://ffmpeg.org/ffmpeg-filters.html#dedot

减少视频的交叉亮度（dot-crawl）和交叉颜色（rainbows）。

### 参数

- m 设置操作模式。可以结合使用 dotcrawl 来降低交叉亮度，和 / 或结合使用 rainbows 来降低交叉颜色。
- lt 设置空间亮度阈值。较低的值会增加交叉亮度的降低。
- tl 设置时间亮度的容忍度。较高的值会增加交叉亮度的降低。
- tc 设置色度时间变化的容限。较高的值会增加交叉色的减少。
- ct 设置时间色度阈值。较低的值会增加交叉色的减少。

### 示例

```python
_ = input(src).dedot(m="rainbows").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]dedot=m=rainbows[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_dedot.mp4 -y -hide_banner
[0.4043s]
```

#### 对比

[视频对比链接]

## deflate

> https://ffmpeg.org/ffmpeg-filters.html#deflate

对视频应用放气效果。该过滤器通过仅考虑低于像素的值，将像素替换为 local（ 3x3 ）平均值。

### 参数

- threshold0
- threshold1
- threshold2
- threshold3 限制每个通道的最大变化，默认值为 65535。如果为 0，则通道将保持不变。

### 示例

```python
_ = input(src).deflate().output(dst).run()
```

```
 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]deflate[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_deflate.mp4 -y -hide_banner
[0.4110s]
```

#### 对比

不太理解。

[视频对比链接]

## deflicker

> https://ffmpeg.org/ffmpeg-filters.html#deflicker

消除时间帧亮度变化。

### 参数

- size 以帧为单位设置移动平均滤波器的大小。 默认值为5。允许的范围为2-129。
- mode 设置平均模式以平滑时间亮度变化。
  - ‘am’ Arithmetic mean
  - ‘gm’ Geometric mean
  - ‘hm’ Harmonic mean
  - ‘qm’ Quadratic mean
  - ‘cm’ Cubic mean
  - ‘pm’ Power mean
  - ‘median’ Median
- bypass 实际上不修改帧。当只需要元数据时很有用。

### 示例

```python
_ = input(src).deflicker(size=10, mode="qm").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]deflicker=mode=qm:size=10[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_deflicker.mp4 -y -hide_banner
[1.1614s]
```

#### 对比

[视频对比链接]

## dejudder

> https://ffmpeg.org/ffmpeg-filters.html#dejudder

删除部分隔行电视转播的内容所产生的抖动。

可以通过例如 pullup 滤波器引入抖动。 如果原始源是部分电视 pullup 的内容，则 dejudder 的输出将具有可变的帧速率。 可能会更改记录的容器帧速率。 除了该更改之外，此过滤器将不会影响恒定帧率的视频。

### 参数

- cycle 指定抖动在其上重复的窗口的长度。接受大于 1 的任何整数
- 4 如果原件以 24 fps 到 30 fps 的速度转换（从电影胶片到 NTSC ），默认
- 5 如果原件以 25 fps 到 30 fps 的速度转播（从 PAL 到 NTSC ）
- 20 如果两者混合。

### 示例

找不到适用素材。

## delogo

> https://ffmpeg.org/ffmpeg-filters.html#delogo

通过简单地对周围像素进行插值来隐藏电视台徽标。 只需设置一个覆盖徽标的矩形，然后观察它消失（有时会出现更难看的东西，结果可能会有所不同）。

### 参数

- x
- y 必须指定徽标的左上角坐标。
- w
- h 必须指定要清除的徽标的宽度和高度。
- band, t 指定矩形的模糊边缘的厚度（添加到 w 和 h ）。默认值为 1。不建议使用此选项，不再建议设置更高的值。
- show 设置为 1 时，屏幕上会绘制一个绿色矩形，以简化查找正确的 x，y，w 和 h 参数的过程。默认值为 0。矩形绘制在最外面的像素上，这些像素将（部分）替换为插值。在每个方向上紧接此矩形之外的下一个像素的值将用于计算矩形内的插值像素值。

### 示例

暂略。

## derain

> https://ffmpeg.org/ffmpeg-filters.html#derain

使用基于卷积神经网络的 derain 方法去除输入图像/视频中的雨水/雾。

### 参数

- filter_type derain/dehaze
- dnn_backend native/tensorflow
- model 设置模型文件的路径，以指定网络体系结构及其参数。请注意，不同的后端使用不同的文件格式。TensorFlow 和 native 后端只能按其格式加载文件。

### 示例

缺少素材，略。

## deshake

> https://ffmpeg.org/ffmpeg-filters.html#deshake

消除抖动/防抖，尝试解决水平和/或垂直偏移的微小变化。该滤镜有助于消除手持相机，撞击三脚架，在车辆上行驶等引起的相机抖动。

### 参数

- x
- y
- w
- h 指定一个限制运动矢量搜索的矩形区域。如果需要，可以将运动矢量的搜索限制在由其左上角，宽度和高度定义的帧的矩形区域中。这些参数与可用于可视化边界框位置的绘图框过滤器具有相同的含义。当运动矢量搜索可能会使**对象在帧内同时运动对于摄像机运动造成混淆**时，此功能很有用。如果 x，y，w 和 h 中的任何一个或全部设置为 -1，则使用整个帧。这样就可以设置以后的选项，而无需为运动矢量搜索指定边界框。**默认搜索整个帧**。
- rx
- ry 在 0 和 64 像素范围内，指定在 x 和 y 方向上的最大移动范围。默认值 16。
- edge 指定如何生成像素以填充帧边缘的空白。
  - ‘blank, 0’ 填零
  - ‘original, 1’ 原始图像
  - ‘clamp, 2’ 拉伸边值
  - ‘mirror, 3’ 镜面边缘，默认
- blocksize 指定用于运动搜索的块大小。范围 4-128 像素，默认为 8。
- contrast 指定块的对比度阈值。仅考虑具有超过指定对比度（最暗像素与最亮像素之间的差异）的块。范围 1-255，默认值为 125。
- search 指定搜索策略。
  - exhaustive 详尽搜索
  - less 非详尽搜索
- filename 如果设置，则将运动搜索的详细日志写入指定的文件。

### 示例

该滤镜假定相机是相对物体是静止的，只有轻微抖动，如果相机或者物体是运动的，效果很差，甚至会加剧抖动幅度。

```python
_ = input(data.SHAKE1).deshake(x=20, y=20, w=100, h=100).output(data.TEST_OUTPUTS_DIR / 'deshake.mp4').run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i C:\Users\Admin\Videos\FFmpeg\InputsData\s1.MOV -filter_complex "[0]deshake=h=100:w=100:x=20:y=20[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\FFmpeg\OutputsData\deshake.mp4 -y -hide_banner
[29.4678s]
```

## despill

> https://ffmpeg.org/ffmpeg-filters.html#despill

消除由绿屏或蓝屏的反射颜色引起的不必要的前景色污染。

### 参数

- type 设置消除类型。
- mix 设置 spillmap 的生成方式。
- expand 设置要除去仍然残留的溢出物的量。
- red 控制溢出区域中的红色量。
- green 控制溢出区域的绿色量。绿屏应该为 -1。
- blue 控制溢出区域中的蓝色量。蓝屏应为 -1。
- brightness 控制溢出区域的亮度，并保留颜色。
- alpha 从生成的 spillmap 修改 alpha。

### 示例

暂略，缺少素材。

## detelecine

> https://ffmpeg.org/ffmpeg-filters.html#detelecine

对电视电影操作进行精确的逆运算。 它要求使用模式选项指定的预定义模式，该模式必须与传递给电视电影滤镜的模式相同。

### 参数

- first_field top/bottom
- pattern 一串数字，代表希望应用的下拉模式。预设值为 23。
- start_frame 一个数字，表示第一帧相对于电视电影图案的位置。如果流被剪切，将使用此方法。默认值为 0。

### 示例

略，不懂。

## dilation

> https://ffmpeg.org/ffmpeg-filters.html#dilation

将膨胀效果应用于视频。该滤镜将像素替换为 local （ 3x3 ）最大值。

### 参数

- threshold0
- threshold1
- threshold2
- threshold3 限制每个通道的最大变化，默认值为 65535。如果为 0，则通道将保持不变。
- coordinates 指定要参考像素的标志。 默认值为 255，即全部使用了八个像素。

### 示例

略，不懂。

## displace

> https://ffmpeg.org/ffmpeg-filters.html#displace

如第二和第三输入流所示，移动像素。它接受三个输入流并输出一个流，第一个输入是源，第二个和第三个输入是位移图。第二个输入指定沿 x 轴位移像素的数量，而第三个输入指定沿 y 轴位移像素的数量。 如果位移图流之一终止，则将使用该位移图的最后一帧。请注意，位移贴图一旦生成，便可以反复使用。

### 参数

- edge 设置超出范围的像素的位移行为。
  - blank 缺少的像素将替换为黑色像素。
  - smear 相邻像素会散开以替换丢失的像素。默认。
  - wrap 超出范围的像素将被包裹，因此它们指向另一侧的像素。
  - mirror 超出范围的像素将替换为镜像像素。

### 示例

不懂，过于复杂。略。

## dnn_processing

> https://ffmpeg.org/ffmpeg-filters.html#dnn_processing

用深度神经网络进行图像处理。 它与另一个过滤器一起使用，该过滤器将帧的像素格式转换为 dnn 网络所需的格式。

### 参数

- dnn_backend native/tensorflow/openvino
- model 设置模型文件的路径，以指定网络体系结构及其参数。 请注意，不同的后端使用不同的文件格式。 TensorFlow，OpenVINO 和 native 后端只能按其格式加载文件。
- input 设置 DNN 网络的输入名称。
- output 设置 DNN 网络的输出名称。
- async 如果设置了 DNN，则使用异步执行（默认值：set）；如果后端不支持异步，则回滚以同步执行。

### 示例

暂略。

## drawbox

> https://ffmpeg.org/ffmpeg-filters.html#drawbox

在输入图像上绘制一个彩色框。

### 参数

- x
- y 这些表达式指定框的左上角坐标。默认为 0。
- w
- h 指定方框的宽度和高度的表达式;如果为 0，则解释为输入的宽度和高度。默认值为 0。
- color 指定框的颜色。如果使用特殊值反转，则框边颜色与亮度反转的视频相同。
- thickness, t 该表达式设置框边缘的厚度。填充值将创建一个填充框。预设值为 3。
- replace 如果输入包含 Alpha，则适用。值为 1 时，涂色框的像素将覆盖视频的颜色和 Alpha 像素。默认值为 0，它将框与输入合成，而视频的 Alpha 保持不变。

x,y,w,h,t 表达式可用变量，允许相互引用：

  - dar 输入显示宽高比，与（w / h）* sar相同。
  - hsub
  - vsub 水平和垂直色度子样本值。 例如，对于像素格式“ yuv422p”，hsub为2，vsub为1。
  - ih 
  - iw 输入的宽度和高度。
  - sar 输入样本的宽高比。
  - x
  - y 绘制框的x和y偏移坐标。
  - w
  - h 绘制框的宽度和高度。
  - t 绘制框的厚度。

### 示例

#### 在边缘画一个黑框

```python
_ = input(src).drawbox().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawbox[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawbox1.mp4 -y -hide_banner
[1.2132s]
```

##### 对比

[视频对比链接]

#### 画一个红色半透明框

```python
_ = input(src).drawbox(10, 20, 200, 60, "red@0.5").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawbox=10:20:200:60:red@0.5[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawbox2.mp4 -y -hide_banner
[0.6584s]
```

##### 对比

[视频对比链接]

#### 画框填充粉色

```python
_ = input(src).drawbox(x=10, y=10, w=100, h=100, color="pink@0.5", thickness="fill").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawbox=color=pink@0.5:h=100:thickness=fill:w=100:x=10:y=10[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawbox3.mp4 -y -hide_banner
[0.4018s]
```

##### 对比

[视频对比链接]

#### 表达式画框

```python
_ = input(src).drawbox(x="-t", y="0.5*(ih-iw/2.4)-t", w="iw+t*2", h="iw/2.4+t*2",
                       thickness=2, color="red").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawbox=color=red:h=iw/2.4+t*2:thickness=2:w=iw+t*2:x=-t:y=0.5*(ih-iw/2.4)-t[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawbox3.mp4 -y -hide_banner
[0.3558s]
```

##### 对比

[视频对比链接]

## drawgraph

> https://ffmpeg.org/ffmpeg-filters.html#drawgraph

使用输入的视频元数据绘制图形。

### 参数

- m1 设置第一帧元数据键，从中将使用元数据值绘制图形。
- fg1 设置第一个前景色。
- m2
- fg2
- m3
- fg3
- m4
- fg4
- min 设置元数据值的最小值。
- max 设置元数据值的最大值。
- bg 设置图形背景颜色。 默认为白色。
- mode 设置图形模式。bar/dot/line，默认 line。
- slide 设置幻灯片模式。
  - frame 当到达右边框时绘制新帧。默认。
  - replace 用新列替换旧列。
  - scroll 从右向左滚动。
  - rscroll 从左向右滚动。
  - picture 画单张画。
- size 设置图形视频的大小。默认 900x256
- rate, r 设置输出帧速率。缺省值为 25。

前景色表达式可以使用以下变量：
- MIN
- MAX 元数据值的最大/小值。
- VAL 当前元数据键值。

颜色定义为 0xAABBGGRR。

### 示例

不懂，略。

## drawgrid

> https://ffmpeg.org/ffmpeg-filters.html#drawgrid

在输入图像上绘制网格。

### 参数

- x
- y 这些表达式指定框的左上角坐标。默认为 0。
- w
- h 指定方框的宽度和高度的表达式;如果为 0，则解释为输入的宽度和高度。默认值为 0。
- color 指定框的颜色。如果使用特殊值反转，则框边颜色与亮度反转的视频相同。
- thickness, t 该表达式设置框边缘的厚度。填充值将创建一个填充框。预设值为 3。
- replace 如果输入包含 Alpha，则适用。值为 1 时，涂色框的像素将覆盖视频的颜色和 Alpha 像素。默认值为 0，它将框与输入合成，而视频的 Alpha 保持不变。

x,y,w,h,t 表达式可用变量，允许相互引用：

  - dar 输入显示宽高比，与（w / h）* sar相同。
  - hsub
  - vsub 水平和垂直色度子样本值。 例如，对于像素格式“ yuv422p”，hsub为2，vsub为1。
  - ih 
  - iw 输入的宽度和高度。
  - sar 输入样本的宽高比。
  - x
  - y 绘制框的x和y偏移坐标。
  - w
  - h 绘制框的宽度和高度。
  - t 绘制框的厚度。

### 示例

```python
_ = input(src).drawgrid(w=100, h=100, thickness=2, color="red@0.5").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawgrid=color=red@0.5:h=100:thickness=2:w=100[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawbox3.mp4 -y -hide_banner
[1.1525s]
```

#### 对比

[视频对比链接]

## drawtext

> https://ffmpeg.org/ffmpeg-filters.html#drawtext

使用 libfreetype 库在视频顶部的指定文件中绘制文本字符串或文本。

### 参数

- box 用于使用背景色在文本周围绘制框。该值必须为 1 启用或 0 禁用。box 的默认值为 0。
- boxborderw 使用 boxcolor 设置要在框周围绘制的边框的宽度。boxborderw 的默认值为 0。
- boxcolor 用于在文本周围绘制框的颜色。默认白色。
- line_spacing 使用框设置要在框周围绘制的边框的行距（以像素为单位）。 line_spacing 的默认值为 0。
- borderw 使用 bordercolor 设置要在文本周围绘制的边框的宽度。borderw 的默认值为 0。
- bordercolor 设置用于在文本周围绘制边框的颜色。默认黑色。
- expansion 选择文本的扩展方式。none/strftime/normal。默认 normal。
- basetime 设置计数的开始时间。值以微秒为单位。仅在不建议使用的 strftime 扩展模式下应用。要在正常扩展模式下进行仿真，请使用 pts 函数，并提供开始时间（以秒为单位）作为第二个参数。
- fix_bounds 如果为 true，检查并修复文本坐标以避免剪贴。
- fontcolor 用于绘制字体的颜色。默认黑色。
- fontcolor_expr 以与文本相同的方式扩展以获得动态 fontcolor 值的字符串。默认情况下，此选项的值为空，并且不进行处理。设置此选项后，它将覆盖 fontcolor 选项。
- font 用于绘制文本的字体系列。 默认 Sans。
- fontfile 用于绘制文本的字体文件。 该路径必须包括在内。 如果禁用 fontconfig 支持，则此参数是必需的。
- alpha 应用 Alpha 混合绘制文本。该值可以是 0.0 到 1.0 之间的数字。该表达式也接受相同的变量 x，y。默认值为 1。请参阅 fontcolor_expr。
- fontsize 用于绘制文本的字体大小。 fontsize 的默认值为 16。
- text_shaping 如果设置为 1，则在绘制文本之前，先尝试使其变形（例如，反转从右到左文本的顺序并连接阿拉伯字符）。否则，只需完全按照给定的文字绘制即可。默认情况下为 1 （如果支持）。
- ft_load_flags 用于加载字体的标志。这些标志对应 libfreetype 支持的标志，是以下值的组合：
  - default
  - no_scale
  - no_hinting
  - render
  - no_bitmap
  - vertical_layout
  - force_autohint
  - crop_bitmap
  - pedantic
  - ignore_global_advance_width
  - no_recurse
  - ignore_transform
  - monochrome
  - linear_design
  - no_autohint
- shadowcolor 用于在绘制的文本后面绘制阴影的颜色。
- shadowx
- shadowy 文本阴影位置相对于文本位置的 x 和 y 偏移量。它们可以是正值或负值。两者的默认值为“0”。
- start_number n/frame_num 变量的起始帧号。系统默认值为“0”。
- tabsize 用于呈现 tab 的空格数的大小。 预设值为 4。
- timecode 将初始时间码表示形式设置为 "hh:mm:ss[:;.]ff"。 它可以与或不与 text 参数一起使用。 必须指定 timecode_rate 选项。
- timecode_rate 设置时间码帧速率（仅时间码）。 值将四舍五入到最接近的整数。 最小值为 “1”。 帧速率 30 和 60 支持丢帧时间码。
- tc24hmax 如果设置为 1，则 timecode 选项的输出将在 24 小时左右结束。默认值为 0 （禁用）。
- text 要绘制的文本字符串。文本必须是 UTF-8 编码字符的序列。如果未使用参数 textfile 指定文件，则此参数是必需的。
- textfile 包含要绘制的文本的文本文件。文本必须是 UTF-8 编码字符的序列。如果未使用参数 text 指定文本字符串，则此参数是必需的。如果同时指定了文本和文本文件，则会引发错误。
- reload 如果设置为 1，则文本文件将在每帧之前重新加载。 请确保以原子方式进行更新，否则可能会被部分读取，甚至失败。
- x
- y 这些表达式指定在视频帧中将在其中绘制文本的偏移量。它们相对于输出图像的顶部 / 左侧边框。x 和 y 的默认值为 “0”。

x 和 y 的参数是包含以下常量和函数的表达式：
  - dar 输入显示宽高比，与（w / h）* sar 相同。
  - hsub
  - vsub 水平和垂直色度子样本值。 例如，对于像素格式 “yuv422p”，hsub 为 2，vsub 为 1。
  - line_h, lh 每行文字的高度。
  - main_h, h, H
  - main_w, w, W 输入高度/宽度。
  - max_glyph_a, ascent 对于所有渲染的字形，从基线到用于放置字形轮廓点的最高 / 上网格坐标的最大距离。由于网格的方向（ Y 轴朝上），因此该值为正值。
  - max_glyph_d, descent 对于所有渲染的字形，从基线到用于放置字形轮廓点的最低网格坐标的最大距离。由于网格的方向，这是一个负值，Y 轴朝上。
  - max_glyph_h 最大字形高度，即渲染文本中包含的所有字形的最大高度，它等效于 ascent - descent。
  - max_glyph_w 最大字形宽度，即所呈现文本中包含的所有字形的最大宽度。
  - n 输入帧的数量，从 0 开始。
  - rand(min, max) 返回介于最小值和最大值之间的随机数。
  - sar 输入样本的宽高比。
  - t 以秒为单位的时间戳，如果输入的时间戳未知，则为 NAN。
  - text_h, th 
  - text_w, tw 呈现文字的宽度/高度。
  - x
  - y 绘制文本的位置的 x 和 y 偏移坐标。x/y 可以相互引用。
  - pict_type 当前帧图片类型的一个字符描述。
  - pkt_pos 当前数据包在输入文件或流中的位置（以字节为单位，从输入开始算起）。值 -1 表示此信息不可用。
  - pkt_duration 当前数据包的持续时间（以秒为单位）。
  - pkt_size 当前数据包的大小（以字节为单位）。

## 文本表达式

设置为 none，则逐字打印文本。设置为 normal，则使用以下扩展机制：

反斜杠字符 “\”，后跟任何字符，始终扩展为第二个字符。

`％{...}` 形式的序列被扩展。大括号之间的文本是函数名称，后面可能跟有以 “:” 分隔的参数。如果参数包含特殊字符或定界符 “:”、“}”，则应将其转义。

请注意，它们也可能必须转义为 filter 参数字符串中的 text 选项的值和 filtergraph 描述中的 filter 参数，并且还可能要转义为多达四个转义级别的 shell，使用文本文件可以避免这些问题。

以下函数可用：

- expr, e 表达式求值结果。它必须接受一个参数，指定要计算的表达式，该参数接受与 x 和 y 值相同的常量和函数。注意，并不是所有常量都应该被使用，例如，在计算表达式时文本大小是未知的，因此常量 text_w 和 text_h 将有一个未定义的值。
- expr_int_format, eif 第一个参数是要评估的表达式，就像 expr 函数一样。第二个参数指定输出格式。允许的值为 “x”，“X”，“d” 和 “u”。它们与 printf 函数中的对待完全相同。第三个参数是可选的，它设置输出所占据的位置数。它可用于从左侧添加零填充。
- gmtime 过滤器运行的时间，用 UTC 表示。它可以接受一个参数: strftime() 格式字符串。
- localtime 过滤器运行的时间，以当地时区表示。它可以接受一个参数: strftime() 格式字符串。
- metadata 帧元数据。接受一两个参数。第一个参数是必需参数，它指定元数据密钥。第二个参数是可选的，并指定默认值，当未找到元数据键或该参数为空时使用。可以通过检查以运行 ffprobe -show_frames 打印的每个帧部分中包含的 TAG 开头的条目来标识可用的元数据。也可以使用在过滤器中生成的字符串元数据（通向绘画文本过滤器）。
- n, frame_num 帧号，从0开始。
- pict_type 当前图片类型的一个字符描述。
- pts 当前帧的时间戳。它最多可以有三个参数。第一个参数是时间戳的格式，它默认将转换秒作为具有微秒精度的十进制数，hms 表示格式化的 [-]HH:MM:SS。具有毫秒精度的 mmm 时间戳。gmtime 表示格式为 UTC 时间的帧的时间戳，localtime 表示格式为本地时区时间的帧的时间戳。第二个参数是添加到时间戳的偏移量。如果格式设置为 hms，则可以提供第三个参数 24HH，以 24 小时格式 (00-23) 表示已格式化时间戳的小时部分。如果格式设置为 localtime 或 gmtime，则可以提供第三个参数：strftime() 格式字符串。缺省情况下，格式为 YYYY-MM-DD HH:MM:SS。

## 改变进行中的参数

```
sendcmd=c='56.0 drawtext reinit fontsize=56\:fontcolor=green\:text=Hello\\ World'
```

### 示例

#### 简单文本

```python
_ = input(src).drawtext(fontfile=f1, text="测试绘制文本", fontsize=36).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=36:text=测试绘制文本[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext.mp4 -y -hide_banner
[0.5606s]
```

> 转义相当复杂。

#### 对比

[视频对比链接]

#### 指定颜色、背景框、背景色

```python
_ = input(src).drawtext(fontfile=f1, text="测试绘制文本", x=100, y=50,
                        fontsize=24, fontcolor="yellow@0.2", box=1,
                        boxcolor="red@0.2").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=box=1:boxcolor=red@0.2:fontcolor=yellow@0.2:fontfile=testdata\\\\f1.ttf:fontsize=24:text=测试绘制文本:x=100:y=50[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext2.mp4 -y -hide_banner
[0.3209s]
```

#### 对比

[视频对比链接]

#### 居中显示文本

```python
_ = input(src).drawtext(fontfile=f1, text="测试绘制文本", fontsize=36,
                        x="(w-text_w)/2", y="(h-text_h)/2").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=36:text=测试绘制文本:x=(w-text_w)/2:y=(h-text_h)/2[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext3.mp4 -y -hide_banner
[0.3359s]
```

#### 对比

[视频对比链接]

#### 每秒变换随机位置

```python
_ = input(src).drawtext(fontfile=f1, text="测试绘制文本", fontsize=36,
                        x="if(eq(mod(t,1),0),rand(0,(w-text_w)),x)",
                        y="if(eq(mod(t,1),0),rand(0,(h-text_h)),y)").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=36:text=测试绘制文本:x=if(eq(mod(t\,1)\,0)\,rand(0\,(w-text_w))\,x):y=if(eq(mod(t\,1)\,0)\,rand(0\,(h-text_h))\,y)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext4.mp4 -y -hide_banner
[0.3033s]
```

#### 对比

[视频对比链接]

#### 从左往右滚动文本

```python
_ = input(src).drawtext(fontfile=f1, text="Show a text line sliding from right to "
                                          "left in the last row of the video frame. The file"
                                          " LONG_LINE is assumed to contain a single line "
                                          "with no newlines.", fontsize=16,
                        y="h-line_h", x="-50*t").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=16:text=Show a text line sliding from right to left in the last row of the video frame. The file LONG_LINE is assumed to contain a single line with no newlines.:x=-50*t:y=h-line_h[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext5.mp4 -y -hide_banner
[0.6457s]
```

#### 对比

[视频对比链接]

#### 从下往上滚动文本

```python
_ = input(src).drawtext(fontfile=f1, text="Show the text off the bottom of "
                                          "the frame and scroll up.",
                        fontsize=16, y="h-20*t").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=16:text=Show the text off the bottom of the frame and scroll up.:y=h-20*t[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext6.mp4 -y -hide_banner
[0.3349s]
```

#### 对比

[视频对比链接]

#### 中心绘制绿色的字母

```python
_ = input(src).drawtext(fontfile=f1, text="G", fontcolor="green", fontsize=36,
                        x="(w-max_glyph_w)/2", y="h/2-ascent").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontcolor=green:fontfile=testdata\\\\f1.ttf:fontsize=36:text=G:x=(w-max_glyph_w)/2:y=h/2-ascent[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext7.mp4 -y -hide_banner
[0.3204s]
```

#### 对比

[视频对比链接]

#### 间歇性显示

```python
_ = input(src).drawtext(fontfile=f1, text="间歇性显示", fontsize=36,
                        x=100, y="x/dar", enable="lt(mod(t,1),0.5)").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=enable=lt(mod(t\,1)\,0.5):fontfile=testdata\\\\f1.ttf:fontsize=36:text=间歇性显示:x=100:y=x/dar[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext8.mp4 -y -hide_banner
[0.4989s]
```

#### 对比

[视频对比链接]

#### 根据视频分辨率调整

```python
_ = input(src).drawtext(fontfile=f1, text="测试绘制文本",
                        fontsize="h/10", x="(w-text_w)/2",
                        y="(h-text_h*2)").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=h/10:text=测试绘制文本:x=(w-text_w)/2:y=(h-text_h*2)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext9.mp4 -y -hide_banner
[0.3431s]
```

#### 对比

[视频对比链接]

#### 显示实时时间

```python
_ = input(src).drawtext(fontfile=f1, text="%{localtime:%a %b %d %Y}",
                        fontsize=36).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]drawtext=fontfile=testdata\\\\f1.ttf:fontsize=36:text=%{localtime\\:%a %b %d %Y}[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_drawtext10.mp4 -y -hide_banner
[0.3401s]
```

#### 对比

[视频对比链接]

## edgedetect

> https://ffmpeg.org/ffmpeg-filters.html#edgedetect

检测并绘制边缘。 过滤器使用 Canny Edge Detection 算法。

### 参数

- low
- high 设置 Canny 阈值算法使用的低和高阈值。高阈值选择 “ 强 ” 边缘像素，然后通过 8 连接将其与低阈值选择的 “ 弱 ” 边缘像素连接。高低阈值必须在 [0,1] 范围内选择，低应小于或等于高。低的默认值为 20/255，高的默认值为 50/255。
- mode 定义绘图模式。
  - wires 在黑色背景上绘制白色/灰色线。默认。
  - colormix 混合颜色以创建绘画/卡通效果。
  - canny 在所有选定通道上应用 Canny 边缘检测器。
- planes 设置通道。

### 示例

#### 标准边缘检测

```python
_ = input(src).edgedetect(low=0.1, high=0.4).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]edgedetect=high=0.4:low=0.1[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_edgedetect.mp4 -y -hide_banner
[1.0472s]
```

##### 对比

[视频对比链接]

#### 绘画效果

```python
_ = input(src).edgedetect(mode="colormix", high=0).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]edgedetect=high=0:mode=colormix[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_edgedetect2.mp4 -y -hide_banner
[1.7482s]
```

#### 对比

[视频对比链接]

## elbg

> https://ffmpeg.org/ffmpeg-filters.html#elbg

使用 ELBG （增强的 LBG ）算法应用后代效果。对于每个输入图像，滤镜将根据给定的码本长度（即不同输出颜色的数量）计算从输入到输出的最佳映射。

### 参数

- codebook_length, l 设置码本长度。该值必须是一个正整数，并且代表不同输出颜色的数量。默认值为 256。
- nb_steps, n 设置最大迭代次数以应用于计算最佳映射。值越高，结果越好，计算时间也越长。预设值为 1。
- seed, s 设置随机种子，必须为 0 到 UINT32_MAX 之间的整数。如果未指定，或者显式设置为 -1，则过滤器将尽最大努力尝试使用良好的随机种子。
- pal8 设置 pal8 输出像素格式。此选项不适用于码本长度大于 256 的情况。

### 示例

不懂，略。

## entropy

> https://ffmpeg.org/ffmpeg-filters.html#entropy

在视频帧的颜色通道的直方图中测量灰度级熵。

### 参数

- mode 可以是 normal / diff。 默认是 normal 的。diff 模式可测量直方图增量值的熵，相邻直方图值之间的绝对差。

### 示例

不懂，略。

## epx

> https://ffmpeg.org/ffmpeg-filters.html#epx

应用专为像素艺术设计的 EPX 放大滤镜。

### 参数

- n 设置缩放尺寸：2xEPX 为 2，3xEPX 为 3。默认值为 3。

### 示例

不懂，略。

## eq

> https://ffmpeg.org/ffmpeg-filters.html#eq

设置亮度，对比度，饱和度和近似伽玛调整。

### 参数

- contrast 设置对比度表达式。 该值必须是 -1000.0 到 1000.0 范围内的浮点值。默认值为 “1”。
- brightness 设置亮度表达式。 该值必须是 -1.0 到 1.0 范围内的浮点值。默认值为 “0”。
- saturation 设置饱和度表达式。该值必须是介于 0.0 到 3.0 之间的浮点数。默认值为 “1”。
- gamma 设置伽玛表达式。 该值必须是介于 0.1 到 10.0 之间的浮点数。默认值为“1”。
- gamma_r 将伽玛表达式设置为红色。该值必须是介于 0.1 到 10.0 之间的浮点数。默认值为“1”。
- gamma_g 将伽玛表达式设置为绿色。该值必须是介于 0.1 到 10.0 之间的浮点数。默认值为“1”。
- gamma_b 将伽玛表达式设置为蓝色。该值必须是介于 0.1 到 10.0 之间的浮点数。默认值为“1”。
- gamma_weight 设置伽玛权重表达式。它可用于减少高伽玛值对明亮图像区域（例如，图像区域）的影响。防止它们过度放大而变成纯白色。该值必须是 0.0 到 1.0 范围内的浮点数。值 0.0 会完全降低伽玛校正，而值 1.0 会使它保持其全部强度。默认值为“1”。
- eval 在评估亮度，对比度，饱和度和伽玛表达式时设置。
  - init 在过滤器初始化期间或处理命令时仅对表达式求值一次，默认
  - frame 计算每个传入帧的表达式，表达式可以使用以下变量：
    - n 输入帧的帧数从 0 开始
    - pos 输入文件中相应数据包的字节位置，如果未指定，则为 NAN
    - r 输入视频的帧速率，如果输入帧速率未知，则为 NAN
    - g 以秒为单位的时间戳，如果输入的时间戳未知，则为 NAN

### 示例

暂略。

## erosion

> https://ffmpeg.org/ffmpeg-filters.html#erosion

对视频应用腐蚀效果。该滤镜将像素替换为 local （ 3x3 ）最小值。

### 参数

- threshold0
- threshold1
- threshold2
- threshold3 限制每个通道的最大变化，默认值为 65535。如果为 0，则通道将保持不变。
- coordinates 指定要参考像素的标志。 默认值为 255，即全部使用了八个像素。

### 示例

略，不懂。

## estdif

> https://ffmpeg.org/ffmpeg-filters.html#estdif

对输入视频进行反交错处理（“estdif”代表“边缘坡度追踪反交错过滤器”）。

仅空间过滤器，使用边缘斜率跟踪算法对缺失的线进行插值。

### 参数

- mode 采用隔行扫描方式。
  - frame 每帧输出一帧。
  - field 每个场输出一帧。默认。
- parity 为输入的隔行视频假定了图片字段奇偶校验。
  - tff 假设最上面的字段是第一位。
  - bff 假设最下面的字段是第一位。
  - auto 启用字段奇偶校验的自动检测。默认。
- deint 指定要去隔行的帧。
  - all 去隔行扫描所有帧。
  - interlaced 仅反交错帧标记为隔行扫描。
- rslope 指定边缘坡度跟踪的搜索半径。 默认值为 1。允许的范围是 1 到 15。
- redge 指定搜索半径以获得最佳边缘匹配。 默认值为 2。允许的范围是 0 到 15。
- interp 指定使用的插值。 默认为 4 点插补。
  - 2p 2 点插补
  - 4p 4 点插补
  - 6p 6 点插补

### 示例

暂略。

## exposure

> https://ffmpeg.org/ffmpeg-filters.html#exposure

调整视频流的曝光。

### 参数

- exposure 在 EV 中设置曝光校正。允许的范围是 -3.0 到 3.0 EV。默认值为 0 EV。
- black 设置黑电平校正。允许的范围是 -1.0 到 1.0。预设值为 0。

### 示例

No such filter: 'colorcorrect'

官网英文文档虽然还有这个滤镜的说明，但最新版找不到这个滤镜，可能已经移除？

## extractplanes

> https://ffmpeg.org/ffmpeg-filters.html#extractplanes

从输入视频流中提取颜色通道分量到单独的灰度视频流中。

### 参数

- planes 指定提取通道。
  - ‘y’
  - ‘u’
  - ‘v’
  - ‘a’
  - ‘r’
  - ‘g’
  - ‘b’

选择输入中不可用的通道将导致错误。 这意味着无法同时选择带有 yuv 通道的 rgb 通道。

### 示例

```python
v0_extract = input(src).extractplanes(planes="y+u+v")
e1, e2, e3 = v0_extract[0], v0_extract[1], v0_extract[2]
_ = merge_outputs(e1.output(testdata_transform / "v0_extractplanes_y.mp4"),
                  e2.output(testdata_transform / "v0_extractplanes_u.mp4"),
                  e3.output(testdata_transform / "v0_extractplanes_v.mp4")).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]extractplanes=y+u+v[tag0][tag1][tag2]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_extractplanes_y.mp4 -vcodec h264_nvenc -map [tag1] C:\Users\Admin\Videos\transform\v0_extractplanes_u.mp4 -vcodec h264_nvenc -map [tag2] C:\Users\Admin\Videos\transform\v0_extractplanes_v.mp4 -y -hide_banner
[0.6920s]
```

#### 对比

[视频对比链接]

## fade

> https://ffmpeg.org/ffmpeg-filters.html#fade

对输入视频应用淡入/淡出效果。

### 参数

- type, t 效果类型可以是“in”（淡入），也可以是“out”（淡入）。默认为 in。
- start_frame, s 指定要开始应用淡入淡出效果的帧的编号。默认值为 0。
- nb_frames, n 淡入淡出效果持续的帧数。在淡入效果结束时，输出视频将具有与输入视频相同的强度。在淡出过渡结束时，输出视频将使用选定的颜色填充。默认值为 25。
- alpha 如果设置为 1，则如果输入中存在一个 alpha 通道，则仅淡入该通道。预设值为 0。
- start_time, st 指定开始应用淡入淡出效果的帧的时间戳（以秒为单位）。如果同时指定了 start_frame 和 start_time，则淡入淡出将以最后一个为准。默认值为 0。
- duration, d 淡入淡出效果必须持续的秒数。在淡入效果结束时，输出视频将具有与输入视频相同的强度，在淡出过渡结束时，输出视频将被选定的颜色填充。如果同时指定了 duration 和 nb_frames，则使用 duration。默认值为 0（默认使用 nb_frames）。
- color, c 指定淡入淡出的颜色。默认值为“黑色”。

### 示例

#### 最初 30 帧淡入

```python
_ = input(src).fade("in", 0, 30).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=in:0:30[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fade1.mp4 -y -hide_banner
[0.3845s]
```

#### 对比

[视频对比链接]

#### 最后 45 帧淡出

```python
_ = input(src).fade("out", 100, 45).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=out:100:45[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fade2.mp4 -y -hide_banner
[0.4127s]
```

#### 对比

[视频对比链接]

#### 同时添加淡入淡出

```python
_ = input(src).fade("in", 0, 25).fade("out", 75, 25).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=in:0:25[tag0];[tag0]fade=out:75:25[tag1]" -vcodec h264_nvenc -map [tag1] C:\Users\Admin\Videos\transform\v0_fade3.mp4 -y -hide_banner
[0.3532s]
```

#### 对比

[视频对比链接]

#### 指定淡入颜色

```python
_ = input(src).fade("in", 5, 20, color="yellow").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=in:5:20:color=yellow[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fade4.mp4 -y -hide_banner
[0.5072s]
```

#### 对比

[视频对比链接]

#### 设置透明度

```python
_ = input(src).fade("in", 0, 25, alpha=1).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=in:0:25:alpha=1[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fade5.mp4 -y -hide_banner
[0.4154s]
```

#### 对比

[视频对比链接]

#### 按秒设置淡入

```python
_ = input(src).fade(t="in", start_time=1, duration=2).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fade=duration=2:start_time=1:t=in[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fade6.mp4 -y -hide_banner
[0.3846s]
```

#### 对比

[视频对比链接]

## fftdnoiz

> https://ffmpeg.org/ffmpeg-filters.html#fftdnoiz

使用 3D FFT（频域滤波）对帧进行消噪。

### 参数

- sigma 设置噪声 sigma 常数。这设置了去噪强度。默认值是 1。允许的范围是 0 到 30。使用非常高的 sigma 和较低的重叠可能会产生阻塞伪像。
- amount 设置去噪量。默认情况下，所有检测到的噪声都会降低。默认值为 1。允许的范围是 0 到 1。
- block 设置块的大小，默认为 4，可以是 3、4、5 或 6。以像素为单位的块的实际大小为块的幂的 2，因此默认情况下，以像素为单位的块大小为 2 ^ 4，即 16。
- overlap 设置块重叠。默认值为 0.5。允许范围是 0.2 到 0.8。
- prev 设置用于降噪的先前帧数。默认情况下设置为 0。
- next 设置要用于降噪的下一帧数。默认情况下设置为 0。
- planes 默认情况下，将被过滤的设置通道是所有可用的过滤（除 alpha 之外）。

### 示例

暂略。

## fftfilt

> https://ffmpeg.org/ffmpeg-filters.html#fftfilt

将任意表达式应用于频域中的样本。

### 参数

- dc_Y 调整图像亮度通道的直流值（增益）。过滤器接受范围为 0 到 1000 的整数值。默认值设置为 0。
- dc_U 调整图像第一色度通道的直流值（增益）。过滤器接受范围为 0 到 1000 的整数值。默认值设置为 0。
- dc_V 调整图像第二色度通道的 dc 值（增益）。过滤器接受范围为 0 到 1000 的整数值。默认值设置为 0。
- weight_Y 设置亮度通道的频域权重​​表达式。
- weight_U 设置第一个色度通道的频域权重​​表达式。
- weight_V 设置第二色度通道的频域权重​​表达式。
- eval 在计算表达式时设置。
  - init 在过滤器初始化期间仅对表达式求值一次。默认。
  - frame 计算每个传入帧的表达式。
- X
- Y 当前样本的坐标。
- W
- H 图像的宽度和高度。
- N 输入帧数，从 0 开始。

### 示例

```python
_ = input(src).fftfilt(dc_Y=0, weight_Y='squish((Y+X)/100-1)').output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fftfilt=dc_Y=0:weight_Y=squish((Y+X)/100-1)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fftfilt4.mp4 -y -hide_banner
[1.8354s]
```

#### 对比

[视频对比链接]

## field

> https://ffmpeg.org/ffmpeg-filters.html#field

使用跨步算法从隔行扫描图像中提取单个字段，以避免浪费CPU时间。 输出帧被标记为非隔行扫描。

### 参数

- type 指定是提取顶部（如果值为 0 或 top）还是底部字段（如果值为 1 或 bottom）。

### 示例

暂略。

## fieldhint

> https://ffmpeg.org/ffmpeg-filters.html#fieldhint

通过从 hint 文件以数字形式提供的周围帧中复制顶部和底部字段来创建新帧。

### 参数

- hint 设置包含提示的文件：绝对 / 相对帧号。剪辑中的每一帧必须有一行。每行必须包含两个数字，并用逗号分隔，并可以选择后面跟 - 或 +。文件每一行上提供的数字不能超出 [N-1，N+1]，其中对于绝对模式，N 是当前帧号；对于相对模式，其数字不能超出 [-1，1] 范围。第一个数字告诉从哪个帧拾取顶部场，第二个数字告诉从哪个帧拾取底部场。如果可选地在其后跟 + 输出帧，则将其标记为隔行扫描；否则，如果其后跟 - 输出帧，则将其标记为逐行扫描，否则将与输入帧标记为相同。如果可选地后跟 t，则输出帧将仅使用顶场，或者在 b 的情况下，将仅使用底场。如果行以＃或;开头 该行被跳过。
- mode absolute/relative

relative 模式 hint 文件示例

```
0,0 - # first frame
1,0 - # second frame, use third's frame top field and second's frame bottom field
1,0 - # third frame, use fourth's frame top field and third's frame bottom field
1,0 -
0,0 -
0,0 -
1,0 -
1,0 -
1,0 -
0,0 -
0,0 -
1,0 -
1,0 -
1,0 -
0,0 -
```

### 示例

不懂，略。

## fieldmatch

> https://ffmpeg.org/ffmpeg-filters.html#fieldmatch

反向电视电影的场匹配滤波器。它旨在从电视广播流中重建渐进帧。该滤波器不会丢失重复的帧，因此要实现完整的反电视电影 `fieldmatch`，需要紧随其后的是抽取滤波器，例如滤波器图中的抽取。

场匹配和抽取的分离尤其是由在两者之间插入去隔行滤波器回退的可能性引起的。如果源混合了电视转播和真实的隔行扫描内容，则 `fieldmatch` 将无法匹配隔行扫描部分的字段。但是这些剩余的精梳帧将被标记为隔行扫描，因此可以在抽取前由更高版本的过滤器（例如 yadif）进行去隔行处理。

除了各种配置选项之外，`fieldmatch` 还可以通过 ppsrc 选项激活第二个可选流。如果启用，则帧重构将基于第二个流中的字段和帧。这样可以对第一个输入进行预处理，以帮助滤波器的各种算法，同时保持输出无损（假设字段正确匹配）。通常，现场感知的降噪器或亮度 / 对比度调整会有所帮助。

请注意，此过滤器使用与 TIVTC / TFM（AviSynth 项目）和 VIVTC / VFM（VapourSynth 项目）相同的算法。后者是 TFM 的轻型克隆，场匹配基于该克隆。尽管语义和用法非常接近，但某些行为和选项名称可能有所不同。

目前，抽取滤波器仅适用于恒定帧频输入。如果您的输入混合了电视转播（30fps）和渐进式内容，且帧率较低，例如 24fps，请使用以下过滤器链产生必要的 cfr 流：`dejudder,fps=30000/1001,fieldmatch,decimate`。

### 参数

不懂，略。

## fieldorder

> https://ffmpeg.org/ffmpeg-filters.html#fieldorder

转换输入视频的场序。

### 参数

- order 输出字段顺序。 有效值是 tff（对于顶部字段优先，默认）或 bff（对于底部字段优先）。

通过将图片内容上移或下移一行，然后用适当的图片内容填充剩余的行来完成转换。此方法与大多数广播现场顺序转换器一致。

如果未将输入视频标记为隔行扫描，或者已将其标记为具有所需的输出场顺序，则此过滤器不会更改传入的视频。

在转换为 PAL DV 材料或从中转换为 PAL DV 材料时，此功能非常有用，这是最先考虑的。

### 示例

不懂，略。

## fifo / afifo

> https://ffmpeg.org/ffmpeg-filters.html#fifo_002c-afifo

缓冲输入图像并在需要时发送它们。当由 libavfilter 帧自动插入时，十分有用。不带参数。

## fillborders

> https://ffmpeg.org/ffmpeg-filters.html#fillborders

填充输入视频的边框，而无需更改视频流尺寸。 有时，视频的四个边缘可能有垃圾，您可能不希望裁剪视频输入以使大小保持为某个数字的倍数。

### 参数

- left 从左边框填充的像素数。
- right 从右边框填充的像素数。
- top 从顶部边框填充的像素数。
- bottom 从底部边框填充的像素数。
- mode 设置填充模式。
  - smear 使用最外面的像素填充像素，默认
  - mirror 使用镜像填充像素（半采样对称）
  - fixed 用恒定值填充像素
  - reflect 使用反射填充像素（整个样本对称）
  - wrap 使用包装填充像素
  - fade 淡入像素至恒定值
- color 在固定或淡入淡出模式下为像素设置颜色。 默认为黑色。

### 示例

```python
_ = input(src).fillborders(left=50, right=50, top=50, bottom=50, mode="mirror").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fillborders=bottom=50:left=50:mode=mirror:right=50:top=50[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fillborders.mp4 -y -hide_banner
[0.4578s]
```

#### 对比

[视频对比链接]

## find_rect

> https://ffmpeg.org/ffmpeg-filters.html#find_rect

查找矩形对象。

### 参数

- object 对象图像的文件路径，必须为 gray8。
- threshold 检测阈值，默认为 0.5。
- mipmaps mipmap 的数量，默认为 3。
- xmin, ymin, xmax, ymax 指定要搜索的矩形。

### 示例

缺素材，暂略。

## floodfill

> https://ffmpeg.org/ffmpeg-filters.html#floodfill

用指定值填充具有相同像素值的区域。

Flood fill 算法是从一个区域中提取若干个连通的点与其他相邻区域区分开（或分别染成不同颜色）的经典算法。因为其思路类似洪水从一个区域扩散到所有能到达的区域而得名。

### 参数

- x 设置像素 x 坐标。
- y
- s0 设置源 #0 组件值。
- s1
- s2
- s3
- d0 设置目标 #0 组件值。
- d1
- d2
- d3

### 示例

```python
_ = input(src).geq(
        r="if(lte(r(X,Y),48),0,r(X,Y))",
        g="if(lte(g(X,Y),48),0,g(X,Y))",
        b="if(lte(b(X,Y),48),0,b(X,Y))",
).floodfill(10, 10, 0, 40, 0, 0, 84, 0).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]format=rgb24,geq="r=if(lte(r(X,Y),48),0,r(X,Y)):g=if(lte(g(X,Y),48),0,g(X,Y)):b=if(lte(b(X,Y),48),0,b(X,Y))",floodfill=10:40:0:0:0:255:0:0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_floodfill.mp4 -y -hide_banner
```

#### 对比

[视频对比链接]

## format

> https://ffmpeg.org/ffmpeg-filters.html#format

将输入视频转换为指定的像素格式之一。 Libavfilter 会尝试选择一个适合作为下一个过滤器输入的对象。

### 参数

- pix_fmts 以“|”分隔的像素格式名称列表，表示或，例如“pix_fmts=yuv420p|monow|rgb24”。

### 示例

```python
_ = input(src).format("yuv420p", "yuv444p", "yuv410p").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]format=pix_fmts=yuv420p|yuv444p|yuv410p[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_format.mp4 -y -hide_banner
[0.4748s]
```

#### 对比

[视频对比链接]

## fps

> https://ffmpeg.org/ffmpeg-filters.html#fps

通过根据需要复制或删除帧，将视频转换为指定的恒定帧速率。

### 参数

- fps 所需的输出帧速率。默认值为 25。
- start_time 假设第一个 PTS 应该是给定的值，以秒为单位。这允许在流的开头进行填充 / 修剪。默认情况下，不对第一帧的预期 PTS 做任何假设，因此不进行填充或修整。例如，可以将其设置为 0，以在视频流在音频流之后开始时以第一帧的副本填充开头，或者以负 PTS 修剪任何帧。
- round 时间戳（PTS）舍入方法。
  - zero 四舍五入
  - inf 从 0 舍入
  - down 向 -infinity 舍入
  - up 向 +infinity 舍入
  - near 四舍五入到最接近的
- eof_action 读取最后一帧时执行的操作。
- round 使用与其他帧相同的时间戳取整方法。
- pass 如果尚未达到输入持续时间，则通过最后一帧。

或者，可以将选项指定为扁平字符串：`fps[:start_time[:round]]`。

### 示例

```python
_ = input(src).fps(fps=60).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]fps=fps=60[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_fps.mp4 -y -hide_banner
[0.4259s]
```

#### 对比

[视频对比链接]

## framepack

> https://ffmpeg.org/ffmpeg-filters.html#framepack

将两个不同的视频流打包到一个立体视频中，在支持的编解码器上设置适当的元数据。 这两个视图应具有相同的大小和帧速率，并且在较短的视频结束时将停止处理。 请注意，您可以使用 scale 和 fps 过滤器方便地调整视图属性。

### 参数

- format 所需的包装格式。 支持的值为：
  - sbs 视图彼此相邻（默认）。
  - tab 这些视图是彼此叠置的。
  - lines 视图按行排列。
  - columns 视图按列打包。
  - frameseq 视图在时间上是交错的。

### 示例

#### 将左右视图转换为帧序视频

```python
_ = input(src).framepack(input(src), format="frameseq").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0][1]framepack=format=frameseq[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_framepack5.mp4 -y -hide_banner
[0.4380s]
```

#### 对比

[视频对比链接]

#### 将视图转换为与输入具有相同输出分辨率的并排视频

```python
_ = input(src).framepack(input(src), format="sbs").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0][1]framepack=format=sbs[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_framepack1.mp4 -y -hide_banner
[0.4808s]
```

#### 对比

[视频对比链接]

## framerate

> https://ffmpeg.org/ffmpeg-filters.html#framerate

通过从源帧中插入新的视频输出帧来更改帧速率。

此过滤器不能与隔行扫描媒体一起正常使用。 如果要更改隔行扫描媒体的帧速率，则需要在此滤镜之前进行反隔行扫描，并在此滤镜之后进行重新隔行扫描。

### 参数

- fps 指定每秒的输出帧数。也可以将此选项单独指定为一个值。默认值为 50。
- interp_start 指定一个范围的起点，在该范围内将创建输出帧为两个帧的线性插值。范围是 [0-255]，默认值为 15。
- interp_end 指定将要创建输出帧的范围的终点，以两个帧的线性插值。范围是 [0-255]，默认值是 240。
- scene 将检测到场景变化的级别指定为 0 到 100 之间的值，以指示新场景； 较低的值表示当前帧引入新场景的可能性较低，而较高的值表示当前帧很可能是一个新场景。默认值为 8.2。
- flags 指定影响过滤过程的标志。
  - scene_change_detect, scd 使用选项场景的值启用场景更改检测。 默认情况下启用此标志。

### 示例

```python
_ = input(src).framerate(fps=60).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]framerate=fps=60[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_framerate.mp4 -y -hide_banner
[0.4547s]
```

#### 对比

[视频对比链接]

## framestep

> https://ffmpeg.org/ffmpeg-filters.html#framestep

每第 N 帧选择一帧。

### 参数

- step 在每个步骤帧之后选择帧。 允许值为大于 0 的正整数。默认值为 1。

### 示例

```python
_ = input(src).framestep(step=5).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]framestep=step=5[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_framestep.mp4 -y -hide_banner
[0.3699s]
```

#### 对比

[视频对比链接]

## freezedetect

> https://ffmpeg.org/ffmpeg-filters.html#freezedetect

检测静止的视频。

当此筛选器检测到输入视频在指定持续时间内内容没有明显变化时，会记录一条消息并设置帧元数据。视频静止检测可计算视频帧所有分量的平均平均绝对差，并将其与本底噪声进行比较。

打印时间和持续时间以秒为单位。lavfi.freezedetect.freeze_start 元数据密钥在时间戳等于或超过检测持续时间的第一帧上设置，并且包含冻结的第一帧的时间戳。lavfi.freezedetect.freeze_duration 和 lavfi.freezedetect.freeze_end 元数据密钥在冻结后的第一帧上设置。

### 参数

- noise, n 设置噪声容限。可以以 dB 指定（如果在指定值后附加“dB”）或 0 到 1 之间的差异比率。默认值为 -60dB 或 0.001。
- duration, d 设置冻结持续时间，直到通知为止（默认为 2 秒）。

### 示例

暂略。

## freezeframes

> https://ffmpeg.org/ffmpeg-filters.html#freezeframes

冻结视频帧。

该过滤器使用来自第二个输入的帧冻结视频帧。

### 参数

- first 设置从其开始冻结的第一帧的编号。
- last 设置结束冻结的最后一帧的编号。
- replace 设置来自第二个输入的帧数，它将代替替换的帧。

### 示例

暂略。

## frei0r

> https://ffmpeg.org/ffmpeg-filters.html#frei0r

对输入视频应用 frei0r 效果。

### 参数

- filter_name 要加载的 frei0r 效果的名称。如果定义了环境变量 FREI0R_PATH，则会在 FREI0R_PATH 中用冒号分隔的列表指定的每个目录中搜索 frei0r 效果。否则，将按以下顺序搜索标准 frei0r 路径：HOME/.frei0r-1/lib/，/usr/local/lib/frei0r-1/，/usr/lib/frei0r-1/。
- filter_params 一个用“|”分隔的参数列表，以传递给 frei0r 效果。

frei0r 效果参数可以是布尔值（其值为“y”或“n”），双精度型，颜色（指定为 R / G / B，其中 R，G 和 B 是介于 0.0 和 0.0 之间的浮点数）。手册的“颜色”部分中指定的颜色描述，或位置，位置（指定为 X / Y，其中 X 和 Y 为浮点数）和 / 或字符串。

参数的数量和类型取决于加载的效果。如果未指定效果参数，则设置默认值。

### 示例

No such filter: 'frei0r'

## fspp

> https://ffmpeg.org/ffmpeg-filters.html#fspp

应用快速简单的后处理。它是 spp 的更快版本。

它将（I）DCT 分为水平 / 垂直通道。与简单的后处理过滤器不同，其中一个对每个块执行一次，而不是对每个像素执行一次。这允许更高的速度。

### 参数

- quality 设置质量。此选项定义了平均级别数。它接受 4-5 范围内的整数。预设值为 4。
- qp 强制使用恒定的量化参数。可接受范围为 0-63 的整数。如果未设置，则过滤器将使用视频流中的 QP（如果有）。
- strength 设置过滤器强度。它接受介于 -15 到 32 之间的整数。较低的值表示更多的细节，但也有更多的伪影，而较高的值表示图像更平滑但也更模糊。默认值为 0- 最佳 PSNR。
- use_bframe_qp 如果设置为 1，则启用 B 帧中的 QP。由于 B 帧通常具有较大的 QP，因此使用此选项可能会导致闪烁。默认值为 0（未启用）。

### 示例

略

## gblur

> https://ffmpeg.org/ffmpeg-filters.html#gblur

应用高斯模糊滤镜。

### 参数

- sigma 设置水平 sigma，高斯模糊的标准偏差。默认值为 0.5。
- steps 设置高斯近似的步数。默认值为 1。
- planes 设置要过滤的通道。默认情况下，所有通道均被过滤。
- sigmaV 设置垂直 sigma，如果为负，则与 `sigma` 相同。默认值为 -1。

### 示例

```python
_ = input(src).gblur(sigma=0.45).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]gblur=sigma=0.45[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_gblur.mp4 -y -hide_banner
[0.4855s]
```

#### 对比

[视频对比链接]

## geq

> https://ffmpeg.org/ffmpeg-filters.html#geq

将通用方程式应用于每个像素。

### 参数

- lum_expr, lum 设置亮度表达式。
- cb_expr, cb 设置色度蓝色表达式。
- cr_expr, cr 设置色度红色表达式。
- alpha_expr, a 设置 alpha 表达式。
- red_expr, r 设置红色表达式。
- green_expr, g 设置绿色表达式。
- blue_expr, b 设置蓝色表达式。

颜色空间是根据指定的选项选择的。如果指定了 lum_expr，cb_expr 或 cr_expr 选项之一，则过滤器将自动选择 YCbCr 颜色空间。如果指定了 red_expr，green_expr 或 blue_expr 选项之一，它将选择 RGB 色彩空间。

如果未定义其中一个色度表达式，则它会落在另一个色度表达式上。如果未指定 alpha 表达式，它将计算为不透明值。如果未指定任何色度表达式，则它们将计算为亮度表达式。

表达式可用变量：

- N 过滤后的帧的序号，从 0 开始。
- X
- Y 当前样本的坐标。
- W
- H 图像的宽度和高度。
- SW
- SH 宽度和高度比例取决于当前过滤的通道。它是相应的亮度通道像素数与当前通道像素数之比。例如。对于 YUV 4:2:0，对于亮度通道，值是 1,1，对于色度通道，值是 0.5,0.5。
- T 当前帧的时间，以秒为单位。
- p(x,y) 返回当前通道位置 (x,y) 的像素值。
- lum(x,y) 返回亮度通道位置 (x,y) 的像素值。
- cb(x,y) 返回位于蓝差色度通道位置 (x,y) 的像素值。如果没有这样的通道则返回 0。
- cr(x,y) 返回红差色度通道位置 (x,y) 的像素值。如果没有这样的通道则返回 0。
- r(x,y)
- g(x,y)
- b(x,y) 返回红 / 绿 / 蓝组件位置 (x,y) 的像素值。如果没有这样的组件，则返回 0。
- alpha(x,y) 返回 alpha 通道位置 (x,y) 的像素值。如果没有这样的通道则返回 0。
- psum(x,y)
- lumsum(x,y)
- cbsum(x,y)
- crsum(x,y)
- rsum(x,y)
- gsum(x,y)
- bsum(x,y)
- alphasum(x,y) 从 (0,0) 到 (x,y) 的矩形内样本值的总和，这允许获得矩形内样本值的总和。请参阅不带 sum 后缀的函数。
- interpolation 设置一种插值方法: nearest/bilinear。默认 bilinear。

对于函数，如果 x 和 y 在该区域之外，则值将自动裁剪到较近的边缘。

请注意，此过滤器可以使用多个线程，在这种情况下，每个切片将具有其自己的表达式状态。如果由于表达式取决于以前的状态而只想使用一个表达式状态，则应将过滤器线程数限制为 1。

### 示例

#### 水平翻转

```python
_ = input(src).geq("p(W-X,Y)").output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=p(W-X\,Y)[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq1.mp4 -y -hide_banner
[1.1102s]
```

#### 对比

[视频对比链接]

#### 产生二维正弦波

```python
_ = input(src).geq("128 + 100*sin(2*(PI/100)*(cos(PI/3)*(X-50*T) + sin(PI/3)*Y))", 128, 128).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=128 + 100*sin(2*(PI/100)*(cos(PI/3)*(X-50*T) + sin(PI/3)*Y)):128:128[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq2.mp4 -y -hide_banner
[2.3361s]
```

#### 对比

[视频对比链接]

#### 产生一个奇特的神秘移动光

```python
_ = input(src).geq("128 + 100*sin(2*(PI/100)*(cos(PI/3)*(X-50*T) + sin(PI/3)*Y))", 128, 128).output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=random(1)/hypot(X-cos(N*0.07)*W/2-W/2\,Y-sin(N*0.09)*H/2-H/2)^2*1000000*sin(N*0.02):128:128[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq3.mp4 -y -hide_banner
[4.8099s]
```

#### 对比

[视频对比链接]

#### 生成一个快速浮雕效果

```python
_ = input(src).geq(lum_expr='(p(X,Y)+(256-p(X-4,Y-4)))/2').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=lum_expr=(p(X\,Y)+(256-p(X-4\,Y-4)))/2[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq4.mp4 -y -hide_banner
[3.4013s]
```

#### 对比

[视频对比链接]

#### 根据像素位置修改 RGB 分量

```python
_ = input(src).geq(r='X/W*r(X,Y)', g='(1-X/W)*g(X,Y)', b='(H-Y)/H*b(X,Y)').output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=b=(H-Y)/H*b(X\,Y):g=(1-X/W)*g(X\,Y):r=X/W*r(X\,Y)[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq5.mp4 -y -hide_banner
[2.4847s]
```

#### 对比

[视频对比链接]

#### 创建与输入大小相同的径向渐变

```python
_ = input(src).geq(lum="255*gauss((X/W-0.5)*3)*gauss((Y/H-0.5)*3)/gauss(0)/gauss(0)").output(dst).run()
```

```
ffmpeg -i testdata\media\0.mp4 -filter_complex "[0]geq=lum=255*gauss((X/W-0.5)*3)*gauss((Y/H-0.5)*3)/gauss(0)/gauss(0)[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_geq6.mp4 -y -hide_banner
[3.1773s]
```

#### 对比

[视频对比链接]

## gradfun

> https://ffmpeg.org/ffmpeg-filters.html#gradfun

修复有时被截断到8位色深的带状伪像，这些带状伪像有时会引入近乎平坦的区域。 插入应该到达带状伪像所在位置的渐变，并抖动它们。

它仅设计用于播放。 请勿在有损压缩之前使用它，因为压缩会丢失抖动并带回频段。

### 参数

- strength 滤镜将改变任何一个像素的最大数量。这也是检测几乎平坦区域的阈值。可接受的范围是 0.51 到 64； 默认值为 1.2。超出范围的值将被裁剪为有效范围。
- radius 要适合渐变的邻域。较大的半径可实现更平滑的渐变，但同时也会阻止滤镜修改细部区域附近的像素。可接受的值是 8-32 ； 默认值为 16。超出范围的值将被裁剪为有效范围。

### 示例

```python
_ = input(src).gradfun(3.5, 8).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]gradfun=3.5:8[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_gradfun.mp4 -y -hide_banner
[0.4002s]
```

#### 对比

[视频对比链接]

## graphmonitor

> https://ffmpeg.org/ffmpeg-filters.html#graphmonitor

显示各种过滤器统计信息。

使用此过滤器，可以调试完整的过滤器图。 尤其是用排队的帧填充链接的问题。

### 参数

- size, s 设置视频输出大小。默认值为 hd720。
- opacity, 0 设置视频不透明度。默认值为 0.9。允许范围是 0 到 1。
- mode, m 设置输出模式，可以 fulll 或 compact。在 compact 模式下，只有带有一些排队帧的过滤器才会显示统计信息。
- flags, f 设置标志，以启用在视频中显示哪些统计信息。
  - queue 显示每个链接中排队的帧数。
  - frame_count_in 显示从滤镜拍摄的帧数。
  - frame_count_out 显示从过滤器发出的帧数。
  - pts 显示当前过滤的帧点数。
  - time 显示当前过滤的帧时间。
  - timebase 显示过滤器链接的时基。
  - format 显示过滤器链接的使用格式。
  - size 如果过滤器链接使用了音频，则显示视频大小或音频通道数。
  - rate 如果过滤器链接使用音频，则显示视频帧率或采样率。
  - eof 显示链接输出状态。
- rate, r 设置输出流视频速率的上限，默认值为 25。这样可以保证输出视频帧速率不超过该值。

### 示例

略。

## greyedge

> https://ffmpeg.org/ffmpeg-filters.html#greyedge

颜色恒定变化滤波器，可通过灰度边缘算法估算场景照明并相应地校正场景颜色。

### 参数

- difford 应用于场景的区分顺序。必须在 [0,2] 范围内选择，默认值为 1。
- minknorm 用于计算 Minkowski 距离的 Minkowski 参数。必须在 [0,20] 范围内选择，默认值为 1。设置为 0 以获得最大值，而不是计算 Minkowski 距离。
- sigma 高斯模糊的标准偏差应用于场景。必须在 [0,1024.0] 范围内选择，默认值= 1。如果 difford 大于 0，则 floor（sigma * break_off_sigma（3））不能等于 0。

### 示例

```python
_ = input(src).greyedge(1, 5, 2).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]greyedge=1:5:2[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_greyedge.mp4 -y -hide_banner
[3.3097s]
```

#### 对比

[视频对比链接]

## haldclut

> https://ffmpeg.org/ffmpeg-filters.html#haldclut

将 Hald CLUT 应用于视频流。

第一个输入是要处理的视频流，第二个输入是 Hald CLUT。Hald CLUT 输入可以是简单的图片或完整的视频流。

### 参数

- shortest 最短输入终止时强制终止。 默认值为0。
- repeatlast 流结束后，继续应用最后一个 CLUT。值为 0 时，将在到达 CLUT 的最后一帧后禁用过滤器。默认值为 1。

### 示例

不懂，略。

## hflip

> https://ffmpeg.org/ffmpeg-filters.html#hflip

水平翻转输入视频。

### 参数

无。

### 示例

```python
_ = input(src).hflip().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hflip[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hflip.mp4 -y -hide_banner
[0.3542s]
```

#### 对比

[视频对比链接]

## histeq

> https://ffmpeg.org/ffmpeg-filters.html#histeq

该过滤器在每帧的基础上应用全局颜色直方图均衡。

它可用于校正像素强度压缩范围内的视频。 滤镜会重新分配像素强度，以使它们在强度范围内的分布相等。 可以将其视为“自动调整对比度滤镜”。 此过滤器仅在校正降级或捕获不良的源视频时有用。

### 参数

- strength 确定要应用的均衡量。随着强度降低，像素强度的分布越来越接近输入帧的分布。该值必须是 [0,1] 范围内的浮点数，默认为 0.200。
- intensity 设置可以产生的最大强度，并适当缩放输出值。强度应根据需要设置，然后可以根据需要限制强度，以免冲洗。该值必须是 [0,1] 范围内的浮点数，默认为 0.210。
- antibanding 设置防束缚水平。如果启用，滤镜将随机少量改变输出像素的亮度，以避免直方图出现条纹。可能的值是 none，weak 或 strong。默认为无。

### 示例

略。

## histogram

> https://ffmpeg.org/ffmpeg-filters.html#histogram

计算并绘制输入视频的颜色分布直方图。

所计算的直方图是图像中颜色分量分布的表示。

标准直方图显示图像中的颜色成分分布。显示每个颜色成分的颜色图。根据输入格式显示当前帧中 Y，U，V，A 或 R，G，B 分量的分布。在每个图的下方显示了一个颜色分量刻度表。

### 参数

- level_height
- scale_height
- display_mode
- levels_mode
- components
- fgopacity
- bgopacity

### 示例

```python
_ = input(src).histogram(level_height=250).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]histogram=level_height=250[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_histogram.mp4 -y -hide_banner
[0.4159s]
```

#### 对比

[视频对比链接]

## hqdn3d

> https://ffmpeg.org/ffmpeg-filters.html#hqdn3d

这是一个高精度 / 高质量的 3D 降噪滤波器。它的目的是减少图像噪点，产生平滑图像，并使静止图像真正静止。它应该增强可压缩性。

### 参数

- luma_spatial 一个非负浮点数，用于指定空间亮度强度。默认为 4.0。
- chroma_spatial 一个非负浮点数，用于指定空间色度强度。默认为 3.0 * luma_spatial / 4.0。
- luma_tmp 一个浮点数，它指定亮度时间强度。默认为 6.0 * luma_spatial / 4.0。
- chroma_tmp 一个浮点数，指定色度时间强度。默认为 luma_tmp * chroma_spatial / luma_spatial。

### 示例

略。

## hwdownload

> https://ffmpeg.org/ffmpeg-filters.html#hwdownload

将硬件帧下载到系统内存中。

输入必须为硬件帧，输出必须为非硬件格式。 并非所有格式都支持输出-可能需要在图形后立即插入一个附加格式过滤器，以获取受支持格式的输出。

### 参数

无。

### 示例

略。

## hwmap

> https://ffmpeg.org/ffmpeg-filters.html#hwmap

将硬件帧映射到系统内存或另一个设备。

该过滤器具有几种不同的操作模式。 使用哪种格式取决于输入和输出格式：

- 硬件帧输入，普通帧输出：将输入帧映射到系统内存，然后将其传递到输出。如果以后需要原始硬件帧（例如，在其上覆盖了其他内容），则可以在下一个模式下再次使用 hwmap 过滤器来检索它。
- 普通帧输入，硬件帧输出：如果输入实际上是一个软件映射的硬件帧，则取消映射 - 即返回原始硬件帧。否则，必须提供设备。在该设备上为输出创建新的硬件表面，然后将它们映射回输入端的软件格式，并将这些帧提供给前面的过滤器。然后，这将类似于 hwupload 过滤器，但是当输入已经采用兼容格式时，它可能能够避免其他副本。
- 硬件帧输入和输出：必须直接或使用 derive_device 选项为输出提供设备。输入和输出设备必须具有不同的类型并且兼容 - 确切的含义取决于系统，但是通常这意味着它们必须引用相同的基础硬件上下文（例如，引用相同的图形卡）。如果输入帧最初是在输出设备上创建的，则取消映射以检索原始帧。否则，将帧映射到输出设备 - 在输出上创建与输入中的帧相对应的新硬件帧。

### 参数

- mode 设置帧映射模式。可以是以下模式的组合（默认 read+write）：
  - read 映射的帧应该是可读的。
  - write 映射的帧应该是可写的。
  - overwrite 映射将始终覆盖整个帧。在某些情况下，这可能会提高性能，因为不需要加载帧的原始内容。
  - direct 映射不包含任何复制。在某些情况下，可能无法创建到帧副本的间接映射，或者无法进行直接映射，否则将具有意外的属性。 设置此标志可确保映射是直接的，并且如果不可能的话将失败。
- derive_device type 与其使用初始化时提供的设备，不如从输入帧所在的设备中派生类型类型的新设备。
- reverse 在硬件到硬件的映射中，反向映射-在接收器中创建帧并将其映射回源。 在某些情况下，如果需要在一个方向上进行映射，但是所使用的设备仅支持相反的方向，则这可能是必需的。此选项很危险-如果该过滤器的输出有任何其他限制，它可能会以不确定的方式破坏前面的过滤器。 在不完全了解其使用含义的情况下，请勿使用它。

### 示例

略。

## hwupload

> https://ffmpeg.org/ffmpeg-filters.html#hwupload

将系统内存帧上传到硬件上。

过滤器初始化时必须提供要上传的设备。如果使用 ffmpeg，请使用 -filter_hw_device 选项或 validate_device 选项选择适当的设备。输入和输出设备必须具有不同的类型并且兼容 - 确切的含义取决于系统，但是通常这意味着它们必须引用相同的基础硬件上下文（例如，引用相同的图形卡）。

### 参数

- derive_device type 与其使用初始化时提供的设备，不如从输入帧所在的设备中派生类型类型的新设备。

### 示例

略。

## hwupload_cuda

> https://ffmpeg.org/ffmpeg-filters.html#hwupload_cuda

将系统内存帧上传到 CUDA 设备。

### 参数

- device 要使用的 CUDA 设备的编号


### 示例

```python
_ = input(src).hwupload_cuda(0).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hwupload_cuda=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hwupload_cuda.mp4 -y -hide_banner
[0.5929s]
```

#### 对比

命令是成功的，但不知道有什么用。

## hqx

> https://ffmpeg.org/ffmpeg-filters.html#hqx

应用专为像素艺术设计的高质量放大滤镜。

### 参数

- n 设置缩放比例：hq2x 为 2，hq3x 为 3，hq4x 为 4。默认值为 3。

### 示例

```python
_ = input(src).hqx().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hqx[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hqx.mp4 -y -hide_banner
[1.6528s]
```

#### 对比

肉眼看不出明显区别。

## hstack

> https://ffmpeg.org/ffmpeg-filters.html#hstack

水平堆叠输入视频。

所有流必须具有相同的像素格式和相同的高度。

请注意，此过滤器比使用覆盖和填充过滤器创建相同的输出要快。

### 参数

- inputs 设置输入流的数量。预设值为 2。
- shortest 如果设置为 1，则在最短输入终止时强制输出终止。预设值为 0。

### 示例

```python
_ = vfilters.hstack(input(media_v0), input(media_v1), inputs=2, shortest=0).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -filter_complex "[0][1]hstack=inputs=2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hstack.mp4 -y -hide_banner
[0.5299s]
```

#### 对比

[视频对比链接]

#### 处理速度比较

以下三种方法结果相同：

```python
vtools.hstack_videos(dst, v1, v1)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0][1]hstack=inputs=2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\videos_hstack.mp4 -y -hide_banner
[14.1295s]
```

```python
vtools.compare_2_videos(v1, v1, dst)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0]pad=w=2*iw[tag0];[tag0][1]overlay=x=w[tag1]" -vcodec h264_nvenc -map [tag1] C:\Users\Admin\Videos\transform\videos_hstack.mp4 -y -hide_banner
[26.6111s]
```

```python
vtools.side_by_side_2_videos(v1, v1, dst)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0][1]framepack=format=sbs[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\videos_hstack.mp4 -y -hide_banner
[15.9902s]
```

确实此滤镜更快一些，之后都采用此滤镜进行水平并排比较视频的处理。

## hue

> https://ffmpeg.org/ffmpeg-filters.html#hue

修改输入的色相和/或饱和度。

### 参数

- h 将色相角指定为度数。它接受一个表达式，默认为“0”。
- s 在 [-10,10] 范围内指定饱和度。它接受一个表达式，默认为“1”。
- H 将色相角指定为弧度数。它接受一个表达式，默认为“0”。
- b 在 [-10,10] 范围内指定亮度。它接受一个表达式，默认为“0”。

h 和 H 是互斥的，不能同时指定。b，h，H 和 s 选项值是包含以下常量的表达式：

- n 输入帧的帧数从 0 开始
- pts 输入帧的表示时间戳记，以时基单位表示
- r 输入视频的帧速率，如果输入帧速率未知，则为 NAN
- t 以秒为单位的时间戳，如果输入的时间戳未知，则为 NAN
- tb 输入视频的时基

### 示例

#### 设置色相和饱和度

```python
_ = input(src).hue(h=90, s=1).output(dst).run()
# 等价
_ = input(src).hue(H="PI/2", s=1).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hue=h=90:s=1[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hue1.mp4 -y -hide_banner
[0.3754s]
```

#### 对比

[视频对比链接]

#### 旋转色调并使饱和度在 1 秒钟内在 0 和 2 之间摆动

```python
_ = input(src).hue(H="2*PI*t", s="sin(2*PI*t)+1").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hue=H=2*PI*t:s=sin(2*PI*t)+1[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hue2.mp4 -y -hide_banner
[0.4243s]
```

#### 对比

[视频对比链接]

#### 从 0 开始应用 3 秒的饱和淡入效果

```python
_ = input(src).hue(s="min(t/3,1)").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hue=s=min(t/3\,1)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hue3.mp4 -y -hide_banner
[0.4264s]
```

一般的淡入表达式可以写成：

```python
# _ = input(src).hue(s="min(0,max((t-START)/DURATION,1))").output(dst).run()
_ = input(src).hue(s="min(0,max((t-0)/3,1))").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hue=s=min(0\,max((t-0)/3\,1))[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hue3.mp4 -y -hide_banner
[0.3993s]
```

#### 对比

[视频对比链接]

#### 从 2 秒开始应用 2 秒的饱和淡出效果

```python
_ = input(src).hue(s="max(0, min(1, (4-t)/2))").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]hue=s=max(0\, min(1\, (4-t)/2))[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_hue4.mp4 -y -hide_banner
[0.3581s]
```

一般的淡出表达式可以写成：

```python
# _ = input(src).hue(s="max(0, min(1, (START+DURATION-t)/DURATION))").output(dst).run()
```

#### 对比

[视频对比链接]

## hysteresis

> https://ffmpeg.org/ffmpeg-filters.html#hysteresis

通过连接组件将第一流增长为第二流。 这使得构建更坚固的边缘掩模成为可能。

### 参数

- planes 设置哪些通道将作为位图处理，未处理的通道将从第一个流复制。 默认值为 0xf，将处理所有通道。
- threshold 设置用于过滤的阈值。 如果像素分量值高于此值，则会激活用于连接分量的过滤器算法。默认值是 0。

### 示例

不懂，略。

## identity

> https://ffmpeg.org/ffmpeg-filters.html#identity

获取两个输入视频之间的身份分数。

该过滤器可拍摄两个输入视频。

两个输入视频必须具有相同的分辨率和像素格式，此过滤器才能正常工作。 还假定两个输入具有相同数量的帧，将它们一一比较。

通过记录系统打印获得的每个组件，平均，最小和最大同一性得分。

过滤器将计算出的每个帧的身份分数存储在帧元数据中。

### 参数

无。

### 示例

不懂，略。

## idet

> https://ffmpeg.org/ffmpeg-filters.html#idet

检测视频隔行扫描类型。

该过滤器尝试检测输入帧是隔行，逐行，顶场还是底场优先。 它还将尝试检测在相邻帧之间重复的场（电视电影的标志）。

单帧检测在对每个帧进行分类时仅考虑紧邻的帧。 多帧检测合并了先前帧的分类历史。

过滤器将记录以下元数据值：

- single.current_frame 使用单帧检测检测到当前帧的类型。以下之一：“tff”（顶部字段优先），“bff”（底部字段优先），“progressive”（渐进）或“undefined”（不确定）
- single.tff 首先使用单帧检测将累积帧数检测为顶场。
- multiple.tff 首先使用多帧检测将累积帧数检测为顶场。
- single.bff 首先使用单帧检测检测为底场的累积帧数。
- multiple.current_frame 使用多帧检测检测到当前帧的类型。以下之一：“tff”（顶部字段优先），“bff”（底部字段优先），“progressive”（渐进）或“undefined”（不确定）
- multiple.bff 首先使用多帧检测将累积帧数检测为底场。
- single.progressive 使用单帧检测将累积帧检测为渐进帧。
- multiple.progressive 使用多帧检测将累积帧检测为渐进帧。
- single.undetermined 使用单帧检测无法分类的累计帧数。
- multiple.undetermined 无法使用多帧检测分类的累计帧数。
- repeated.current_frame 从最后一帧开始重复当前帧中的哪个字段。“neither”，“top” 或 “bottom” 之一。
- repeated.neither 没有重复字段的累计帧数。
- repeated.top 累积帧数，其中顶场从上一帧的顶场开始重复。
- repeated.bottom 累积帧数，其中下场从上一帧的下场开始重复。

### 参数

- intl_thres 设置隔行扫描阈值。
- prog_thres 设置渐进阈值。
- rep_thres 重复现场检测的阈值。
- half_life 给定帧对统计的贡献减半后的帧数（即其对分类的贡献仅为 0.5）。默认值为 0 表示所看到的所有帧将永远获得 1.0 的总权重。
- analyze_interlaced_flag 如果该值不为 0，则 idet 将使用指定的帧数来确定隔行标志是否正确，它将不计算未确定的帧。如果发现标志是正确的，则将不做任何进一步的计算就使用该标志，如果发现它是不正确的，则将不进行任何进一步的计算就将其清除。这样可以将 idet 滤波器作为一种低计算量的方法来清除隔行标志

### 示例

不懂，略。

## il

> https://ffmpeg.org/ffmpeg-filters.html#il

解交织或交织场。

该过滤器允许人们处理隔行扫描的图像场而无需对它们进行隔行扫描。 去交织将输入帧分为2个场（所谓的半图片）。 奇数行移动到输出图像的上半部分，偶数行移动到下半部分。 您可以独立处理（过滤）它们，然后重新交织它们。

### 参数

- luma_mode, l
- chroma_mode, c
- alpha_mode, a
  - ‘none’ 默认
  - ‘deinterleave, d’ 解交织场，将一个放置在另一个上方。
  - ‘interleave, i’ 交织字段。 反转去交织的效果。
- luma_swap, ls
- chroma_swap, cs
- alpha_swap, as 交换亮度/色度/ alpha字段。 交换偶数和奇数行。 预设值为 0。

### 示例

不懂，略。

## inflate

> https://ffmpeg.org/ffmpeg-filters.html#inflate

对视频应用膨胀效果。

该过滤器通过仅考虑高于像素的值，将像素替换为 local（3x3）平均值。

### 参数

- threshold0
- threshold1
- threshold2
- threshold3 限制每个通道的最大变化，默认值为 65535。如果为 0，则通道将保持不变。

### 示例

不懂，略。

## interlace

> https://ffmpeg.org/ffmpeg-filters.html#interlace

简单的隔行过滤器，可处理逐行内容。 这样可以将奇数帧的上（或下）行与偶数帧的下（或上）行交织，从而将帧速率减半，并保留了图像高度。

```
   Original        Original             New Frame
   Frame 'j'      Frame 'j+1'             (tff)
  ==========      ===========       ==================
    Line 0  -------------------->    Frame 'j' Line 0
    Line 1          Line 1  ---->   Frame 'j+1' Line 1
    Line 2 --------------------->    Frame 'j' Line 2
    Line 3          Line 3  ---->   Frame 'j+1' Line 3
     ...             ...                   ...
New Frame + 1 will be generated by Frame 'j+2' and Frame 'j+3' and so on
```

### 参数

- scan 这确定是从逐行帧的偶数（tff- 默认值）还是奇数（bff）行中获取隔行帧。
- lowpass 垂直低通滤波器，可避免 Twitter 隔行扫描并减少莫尔条纹。
  - ‘0, off’ 禁用垂直低通滤波器
  - ‘1, linear’ 启用线性过滤器（默认）
  - ‘2, complex’ 启用复杂过滤器。 这将略微减少 Twitter 和波纹，但更好地保留细节和主观清晰度

### 示例

不懂，略。

## kerndeint

> https://ffmpeg.org/ffmpeg-filters.html#kerndeint

通过应用自适应内核解交织来对输入视频进行解交织。 对视频的隔行扫描部分进行处理以产生逐行帧。

### 参数

- thresh 设置阈值，该阈值在确定是否必须处理像素线时会影响滤镜的容限。它必须是 [0,255] 范围内的整数，默认值为 10。值 0 将导致在每个像素上应用该过程。
- map 如果设置为 1，则将超出阈值的像素绘制为白色。默认值为 0。
- order 设置字段顺序。如果设置为 1，则交换字段，如果为 0，则保留字段。默认为 0。
- sharp 如果设置为 1，则启用其他锐化。默认值为 0。
- twoway 如果设置为 1，则启用双向锐化。默认值为 0。

### 示例

不懂，略。

## kirsch

> https://ffmpeg.org/ffmpeg-filters.html#kirsch

对输入视频流应用 kirsch 运算符。

### 参数

- planes 设置将要处理的通道，将复制未处理的通道。 默认值为 0xf，将处理所有通道。
- scale 设置值将与过滤结果相乘。
- delta 设置将被添加到过滤结果中的值。

### 示例

不懂，略。

## lagfun

> https://ffmpeg.org/ffmpeg-filters.html#lagfun

慢慢更新较暗的像素。

此滤镜使短时间的闪光看起来更长。

### 参数

- decay 设置衰减因子。默认值为 0.95。允许范围是 0 到 1。
- planes 设置要过滤的通道。默认为全部。允许范围是 0 到 15。

### 示例

不懂，略。

## lenscorrection

> https://ffmpeg.org/ffmpeg-filters.html#lenscorrection

校正径向镜片变形

该滤镜可用于校正由于使用广角镜而引起的径向变形，从而重新校正图像。为了找到正确的参数，可以使用一些可用的工具，例如，作为 opencv 的一部分或只是反复试验。要使用 opencv，请使用来自 opencv 源的校准样本（在 samples / cpp 下），并从所得矩阵中提取 k1 和 k2 系数。

注意，实际上，KDE 项目的开源工具 Krita 和 Digikam 中提供了相同的过滤器。

与也可以用来补偿镜头误差的晕影滤镜相比，此滤镜可以校正图像的失真，而晕影滤镜可以校正亮度分布，因此在某些情况下，您可能希望将两个滤镜一起使用，但必须注意顺序，即在镜片校正之前还是之后都要进行渐晕。

### 参数

- cx 图像焦点的相对 x 坐标，从而导致畸变的中心。该值的范围为 [0,1]，并表示为图像宽度的分数。默认值为 0.5。
- cy 图像焦点的相对 y 坐标，从而失真的中心。该值的范围为 [0,1]，并表示为图像高度的分数。默认值为 0.5。
- k1 二次校正项的系数。该值的范围为 [-1,1]。0 表示无校正。默认值为 0。
- k2 双二次校正项的系数。该值的范围为 [-1,1]。0 表示无校正。默认值为 0。
- i 设置插补类型。可以是最近的或双线性的。默认值是最近的。
- fc 指定未映射像素的颜色。默认黑色。

### 示例

不懂，略。

## lensfun

> https://ffmpeg.org/ffmpeg-filters.html#lensfun

通过 lensfun 库应用镜头校正。

lensfun 滤镜需要相机品牌，相机型号和镜头型号才能应用镜头校正。筛选器将加载 lensfun 数据库并对其进行查询，以在数据库中找到相应的相机和镜头条目。只要可以使用给定的选项找到这些条目，过滤器就可以对帧进行校正。请注意，不完整的字符串将导致滤镜选择与给定选项最匹配的滤镜，并且滤镜将输出所选的相机和镜头型号（记录为“信息”级）。您必须提供所需的品牌，相机型号和镜头型号。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## libvmaf

> https://ffmpeg.org/ffmpeg-filters.html#libvmaf


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## limiter

> https://ffmpeg.org/ffmpeg-filters.html#limiter

将像素分量值限制在指定范围 [min, max]。

### 参数

- min 默认为输入的最低允许值。
- max 默认为输入的最大允许值。
- planes 设置处理通道，默认全部。

### 示例

略。

## loop

> https://ffmpeg.org/ffmpeg-filters.html#loop

循环播放视频帧。

### 参数

- loop 设置循环数。将此值设置为 -1 将导致无限循环。默认值为 0。
- size 以帧数设置最大尺寸。默认值为 0。
- start 设置循环的第一帧。默认值为 0。

### 示例

```python
_ = input(src).loop(loop=-1, size=1, start=1).output(dst, duration=5).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]loop=loop=-1:size=1:start=1[tag0]" -t 5 -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_loop.mp4 -y -hide_banner
[0.4211s]
```

#### 对比

[视频对比链接]

## lut1d

> https://ffmpeg.org/ffmpeg-filters.html#lut1d


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## lut3d

> https://ffmpeg.org/ffmpeg-filters.html#lut3d


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## lumakey

> https://ffmpeg.org/ffmpeg-filters.html#lumakey

将某些亮度值转换为透明度。

### 参数

- threshold 设置将用作透明度基础的亮度。预设值为 0。
- tolerance 设置要键入的亮度值范围。默认值为 0.01。
- softness 设置柔软度范围。默认值为 0。使用此值可控制从零到完全透明的渐变。

### 示例

```python
_ = input(src).lumakey(threshold=0.01, tolerance=0.01).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]lumakey=threshold=0.01:tolerance=0.01[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_lumakey.mp4 -y -hide_banner
[0.3720s]
```

#### 对比

[视频对比链接]

## lut, lutrgb, lutyuv

> https://ffmpeg.org/ffmpeg-filters.html#lutyuv


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## lut2, tlut2

> https://ffmpeg.org/ffmpeg-filters.html#tlut2


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskedclamp

> https://ffmpeg.org/ffmpeg-filters.html#maskedclamp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskedmax

> https://ffmpeg.org/ffmpeg-filters.html#maskedmax


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskedmerge

> https://ffmpeg.org/ffmpeg-filters.html#maskedmerge


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskedmin

> https://ffmpeg.org/ffmpeg-filters.html#maskedmin


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskedthreshold

> https://ffmpeg.org/ffmpeg-filters.html#maskedthreshold


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## maskfun

> https://ffmpeg.org/ffmpeg-filters.html#maskfun


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## mcdeint

> https://ffmpeg.org/ffmpeg-filters.html#mcdeint


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## median

> https://ffmpeg.org/ffmpeg-filters.html#median


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## mergeplanes

> https://ffmpeg.org/ffmpeg-filters.html#mergeplanes

合并来自多个视频流的颜色通道分量。

滤镜最多可接收 4 个输入流，并将选定的输入通道合并到输出视频。

### 参数

- mapping 将输入设置为输出通道映射。默认值为 0。映射被指定为位图。应将其指定为十六进制数，格式为 0xAa [Bb [Cc [Dd]]]。“Aa”描述了输出流第一个通道的映射。“A”设置要使用的输入流的编号（从 0 到 3），“a”设置要使用的相应输入的通道编号（从 0 到 3）。其余映射相似，“Bb”描述输出流第二通道的映射，“Cc”描述输出流第三通道的映射，“Dd”描述输出流第四通道的映射。
- format 设置输出像素格式。默认值为 yuva444p。

### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## mestimate

> https://ffmpeg.org/ffmpeg-filters.html#mestimate

使用块匹配算法估计和导出运动矢量。 运动矢量存储在帧侧数据中，以供其他过滤器使用。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## midequalizer

> https://ffmpeg.org/ffmpeg-filters.html#midequalizer

使用两个视频流应用中途图像均衡效果。

中途图像均衡可将一对图像调整为具有相同的直方图，同时尽可能保持其动态。 这对于例如 匹配一对立体声相机的曝光。

该滤波器具有两个输入和一个输出，它们必须具有相同的像素格式，但大小可能不同。 滤波器的输出首先通过两个输入的中间直方图进行调整。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## minterpolate

> https://ffmpeg.org/ffmpeg-filters.html#minterpolate

使用运动插值将视频转换为指定的帧速率。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## mix

> https://ffmpeg.org/ffmpeg-filters.html#mix

将几个视频输入流混合到一个视频流中。

### 参数

- inputs 输入数量。如果未指定，则默认为 2。
- weights 指定每个输入视频流的权重作为顺序。每个砝码之间都用空格隔开。如果权重数量小于帧数，则最后指定的权重将用于所有剩余的未设置权重。
- scale 指定比例，如果设置，它将乘以每个权重的总和再乘以像素值，以得到最终的目标像素值。默认情况下，比例会自动缩放为权重之和。
- duration 指定如何确定流的结尾。
  - ‘ longest ’ 最长输入的持续时间。（默认）
  - ‘ shortest ’ 最短输入的持续时间。
  - ‘ first ’ 第一次输入的持续时间。

### 示例

```python
_ = vfilters.mix(input(media_v0), input(media_v1), input(media_v2),inputs=3).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -filter_complex "[0][1][2]mix=inputs=3[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_mix.mp4 -y -hide_banner
[0.9549s]
```

#### 对比

[视频对比链接]

## monochrome

> https://ffmpeg.org/ffmpeg-filters.html#monochrome

使用自定义滤色器将视频转换为灰色。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## mpdecimate

> https://ffmpeg.org/ffmpeg-filters.html#mpdecimate

丢弃与前一帧相差无几的帧，以降低帧速率。

此过滤器的主要用途是用于非常低比特率的编码（例如，通过拨号调制解调器进行流式传输），但从理论上讲，它可以用于修复反向电视连接不正确的电影。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## msad

> https://ffmpeg.org/ffmpeg-filters.html#msad

获取两个输入视频之间的 MSAD（绝对差的平均值）。

该过滤器可拍摄两个输入视频。

两个输入视频必须具有相同的分辨率和像素格式，此过滤器才能正常工作。还假定两个输入具有相同数量的帧，将它们一一比较。

通过测井系统打印获得的每组分，平均，最小和最大 MSAD。

过滤器将计算出的每个帧的 MSAD 存储在帧元数据中。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## negate

> https://ffmpeg.org/ffmpeg-filters.html#negate

对输入视频取反色。

### 参数

- negate_alpha 值为 1 时，它会否定 alpha 分量（如果存在）。预设值为 0。

### 示例

```python
_ = input(src).negate(negate_alpha=False).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]negate=negate_alpha=False[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_negate.mp4 -y -hide_banner
[0.4209s]
```

#### 对比

[视频对比链接]

## nlmeans

> https://ffmpeg.org/ffmpeg-filters.html#nlmeans

使用非局部均值算法对帧进行消噪。

通过寻找具有相似上下文的其他像素来调整每个像素。 通过比较它们周围大小为pxp的补丁来定义此上下文相似性。 在像素周围的rxr区域中搜索补丁。

请注意，研究区域定义了色块的中心，这意味着某些色块将由该研究区域之外的像素组成。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## nnedi

> https://ffmpeg.org/ffmpeg-filters.html#nnedi

使用神经网络边沿定向插值对视频进行去交织。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## noformat

> https://ffmpeg.org/ffmpeg-filters.html#noformat

强制 libavfilter 不要将任何指定的像素格式用于下一个过滤器的输入。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## noise

> https://ffmpeg.org/ffmpeg-filters.html#noise

在视频输入帧上添加噪点。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## normalize

> https://ffmpeg.org/ffmpeg-filters.html#normalize

标准化 RGB 视频（又名直方图拉伸，对比度拉伸）。

对于每帧的每个通道，滤波器都会计算输入范围并将其线性映射到用户指定的输出范围。输出范围默认为从纯黑色到纯白色的整个动态范围。

可以在输入范围上使用时间平滑，以减少当小的深色或明亮的物体进入或离开场景时引起的闪烁（亮度的快速变化）。这类似于摄像机上的自动曝光（自动增益控制），并且像摄像机一样，它可能会导致一段时间的视频过度曝光或曝光不足。

RGB 通道可以独立进行归一化，这可能会导致某些颜色偏移，或者可以将它们链接为单个通道，从而防止出现颜色偏移。链接归一化保留色调。独立归一化没有，因此可以用来消除某些偏色。独立和链接的归一化可以任意比例组合。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## null

> https://ffmpeg.org/ffmpeg-filters.html#null

不变地将视频源传递到输出。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ocr

> https://ffmpeg.org/ffmpeg-filters.html#ocr

光学字符识别。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ocv

> https://ffmpeg.org/ffmpeg-filters.html#ocv


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## oscilloscope

> https://ffmpeg.org/ffmpeg-filters.html#oscilloscope

2D视频示波器。

对测量空间冲动，阶跃响应，色度延迟等有用。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## overlay

> https://ffmpeg.org/ffmpeg-filters.html#overlay

将一个视频叠加在另一个视频上。它有两个输入，只有一个输出。 **第一个输入**是第二个输入叠加在其上的“主”视频。

### 参数

- x
- y 设置主视频上叠加视频的 x 和 y 坐标表达式。两个表达式的默认值为“0”。如果表达式无效，则将其设置为一个很大的值（这意味着该叠加层将不会显示在输出可见区域内）。
- eof_action
- eval 在计算 x 和 y 的表达式时设置。
  - ‘init’ 在过滤器初始化期间或处理命令时仅对表达式求值一次
  - ‘frame’ 计算每个传入帧的表达式
- shortest
- format 设置输出视频的格式。
  - ‘yuv420’
  - ‘yuv420p10’
  - ‘yuv422’
  - ‘yuv422p10’
  - ‘yuv444’
  - ‘rgb’
  - ‘gbrp’
  - ‘auto’
- repeatlast
- alpha 设置叠加视频的 alpha 格式，它可以是 straight 的或 premultiplied 的。 默认为 straight。

x 和 y 表达式可以包含以下参数：

- main_w, W
- main_h, H 主要输入宽度和高度。
- overlay_w, w
- overlay_h, h 叠加层输入的宽度和高度。
- x
- y x 和 y 的计算值。为每个新帧评估它们。
- hsub
- vsub 输出格式的水平和垂直色度子样本值。例如，对于像素格式“yuv422p”，hsub 为 2，vsub 为 1。
- n 输入帧的数量，从 0 开始
- pos 输入框在文件中的位置，如果未知，则为 NAN
- t 时间戳，以秒为单位。如果输入的时间戳未知，则为 NAN。

### 示例

#### 顶部与右边

```python
_ = vfilters.overlay(mv1, mv2, "main_w-overlay_w-50", "main_h-overlay_h-50").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -filter_complex "[0][1]overlay=x=main_w-overlay_w-50:y=main_h-overlay_h-50[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_overlay1.mp4 -y -hide_banner
[0.6054s]
```

#### 对比

[视频对比链接]

#### 添加图片水印

```python
_ = vfilters.overlay(mv1, logo, 10, "main_h-overlay_h-10").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -i testdata\i3.png -filter_complex "[1]scale=h=100:w=100[tag0];[0][tag0]overlay=x=10:y=main_h-overlay_h-10[tag1]" -vcodec h264_nvenc -map [tag1] C:\Users\Admin\Videos\transform\v0_overlay2.mp4 -y -hide_banner
[0.3607s]
```

#### 对比

[视频对比链接]

#### 添加多个图片水印

```python
_ = mv1.overlay(logos[0], 10, "H-h-10").overlay(logos[1], "W-w-10", "H-h-10").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -i testdata\i3.png -filter_complex "[1]scale=h=100:w=100[tag0];[tag0]split=2[tag1][tag2];[0][tag1]overlay=x=10:y=H-h-10[tag3];[tag3][tag2]overlay=x=W-w-10:y=H-h-10[tag4]" -vcodec h264_nvenc -map [tag4] C:\Users\Admin\Videos\transform\v0_overlay3.mp4 -y -hide_banner
[0.3933s]
```

#### 对比

[视频对比链接]

## overlay_cuda

> https://ffmpeg.org/ffmpeg-filters.html#overlay_cuda

同上，但只支持 CUDA 帧。

## owdenoise

> https://ffmpeg.org/ffmpeg-filters.html#owdenoise

Overcomplete Wavelet 降噪器。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pad

> https://ffmpeg.org/ffmpeg-filters.html#pad

将填充物添加到输入图像，并将原始输入放置在提供的 x，y 坐标处。

### 参数

- width, w
- height, h 为输出图像的大小指定一个表达式，其中添加了填充。 如果 width 或 height 的值为 0，则将相应的输入大小用于输出。宽度表达式可以引用由高度表达式设置的值，反之亦然。宽度和高度的默认值为 0。
- x
- y 指定偏移量，以相对于输出图像的顶部/左侧边界将输入图像放置在填充区域内。x 表达式可以引用 y 表达式设置的值，反之亦然。x 和 y 的默认值为 0。如果 x 或 y 的值为负数，则会对其进行更改，以使输入图像位于填充区域的中心。
- color 指定填充区域的颜色。默认黑色。
- eval 指定何时计算宽度，高度，x 和 y 表达式。
  - ‘init’ 在过滤器初始化期间或处理命令时，仅对表达式求值一次。默认。
  - ‘frame’ 计算每个传入帧的表达式。
- aspect 填充至指定分辨率。

width，height，x 和 y 选项的值是包含以下常量的表达式：
- in_w, iw
- in_h, ih 输入视频的宽度和高度。
- out_w, ow
- out_h, oh 输出的宽度和高度（填充区域的大小），由 width 和 height 表达式指定。
- x
- y 由 x 和 y 表达式指定的 x 和 y 偏移量；如果尚未指定，则为 NAN。
- a iw / ih
- sar 输入样本宽高比
- dar 输入显示宽高比 (iw / ih) * sar
- hsub
- vsub 水平和垂直色度子样本值。例如，对于像素格式“yuv422p”，hsub 为 2，vsub 为 1。

### 示例

```python
_ = input(src).pad("3/2*iw", "3/2*ih", "(ow-iw)/2", "(oh-ih)/2").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]pad=3/2*iw:3/2*ih:(ow-iw)/2:(oh-ih)/2[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_pad.mp4 -y -hide_banner
[0.4306s]
```

#### 对比

[视频对比链接]

## palettegen

> https://ffmpeg.org/ffmpeg-filters.html#palettegen

为整个视频流生成一个调色板。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## paletteuse

> https://ffmpeg.org/ffmpeg-filters.html#paletteuse

使用调色板对输入视频流进行下采样。

该过滤器有两个输入：一个视频流和一个调色板。 调色板必须是 256 像素的图像。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## perspective

> https://ffmpeg.org/ffmpeg-filters.html#perspective

纠正未垂直于屏幕录制的视频的透视图。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## phase

> https://ffmpeg.org/ffmpeg-filters.html#phase

将隔行视频延迟一个场时间，以便改变场序。

预期用途是将以相反场序拍摄的 PAL 电影固定为电影到视频的传输。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## photosensitivity

> https://ffmpeg.org/ffmpeg-filters.html#photosensitivity

减少视频中的各种闪烁，从而帮助癫痫病患者。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pixdesctest

> https://ffmpeg.org/ffmpeg-filters.html#pixdesctest

像素格式描述符测试过滤器，主要用于内部测试。 输出视频应等于输入视频。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pixscope

> https://ffmpeg.org/ffmpeg-filters.html#pixscope

显示颜色通道的样本值。 主要用于检查颜色和级别。 支持的最低分辨率为640x480。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pp

> https://ffmpeg.org/ffmpeg-filters.html#pp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pp7

> https://ffmpeg.org/ffmpeg-filters.html#pp7


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## premultiply

> https://ffmpeg.org/ffmpeg-filters.html#premultiply


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## prewitt

> https://ffmpeg.org/ffmpeg-filters.html#prewitt


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pseudocolor

> https://ffmpeg.org/ffmpeg-filters.html#pseudocolor


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## psnr

> https://ffmpeg.org/ffmpeg-filters.html#psnr


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## pullup

> https://ffmpeg.org/ffmpeg-filters.html#pullup


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## qp

> https://ffmpeg.org/ffmpeg-filters.html#qp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## random

> https://ffmpeg.org/ffmpeg-filters.html#random


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## readeia608

> https://ffmpeg.org/ffmpeg-filters.html#readeia608


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## readvitc

> https://ffmpeg.org/ffmpeg-filters.html#readvitc


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## remap

> https://ffmpeg.org/ffmpeg-filters.html#remap


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## removegrain

> https://ffmpeg.org/ffmpeg-filters.html#removegrain


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## removelogo

> https://ffmpeg.org/ffmpeg-filters.html#removelogo


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## repeatfields

> https://ffmpeg.org/ffmpeg-filters.html#repeatfields


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## reverse

> https://ffmpeg.org/ffmpeg-filters.html#reverse

反转视频片段。即倒放。

警告：此过滤器需要内存来缓冲整个片段，因此建议进行修剪。

### 参数

无。

### 示例

```python
_ = input(src).reverse().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i C:\Users\Admin\Videos\transform\v0_reverse.mp4 -filter_complex "[0][1]hstack=inputs=2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\contrast\v0_reverse_compare.mp4 -y -hide_banner
[0.4597s]
```

#### 对比

[视频对比链接]

## rgbashift

> https://ffmpeg.org/ffmpeg-filters.html#rgbashift


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## roberts

> https://ffmpeg.org/ffmpeg-filters.html#roberts


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## rotate

> https://ffmpeg.org/ffmpeg-filters.html#rotate

以弧度表示的任意角度旋转视频。

### 参数

- angle, a 设置用于顺时针旋转输入视频的角度的表达式，以弧度表示。负值将导致逆时针旋转。默认情况下，它设置为“0”。对每个帧评估该表达式。
- out_w, ow 设置输出宽度表达式，默认值为“iw”。在配置期间，该表达式仅被评估一次。
- out_h, oh 设置输出高度表达式，默认值为“ih”。在配置期间，该表达式仅被评估一次。
- bilinear 如果设置为 1，则启用双线性插值，值为 0 则将其禁用。预设值为 1。
- fillcolor, c 设置用于填充旋转图像未覆盖的输出区域的颜色。如果选择特殊值“none”，则不打印背景（例如，如果从未显示背景，则很有用）。默认值为“黑色”。

- 角度和输出大小的表达式可以包含以下常量和函数：
- n 输入帧的序号，从 0 开始。在过滤第一帧之前，始终为 NAN。
- t 输入帧的时间（以秒为单位），在配置过滤器时将其设置为 0。在过滤第一帧之前，始终为 NAN。
- hsub
- vsub 水平和垂直色度子样本值。例如，对于像素格式“yuv422p”，hsub 为 2，vsub 为 1。
- in_w, iw
- in_h, ih 输入视频的宽度和高度
- out_w, ow
- out_h, oh 输出的宽度和高度，即宽度和高度表达式指定的填充区域的大小
- rotw(a)
- roth(a) 完全包含以弧度旋转的输入视频所需的最小宽度 / 高度。

### 示例

```python
_ = input(src).rotate("PI/6").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]rotate=PI/6[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_rotate.mp4 -y -hide_banner
[0.4854s]
```

#### 对比

[视频对比链接]

## sab

> https://ffmpeg.org/ffmpeg-filters.html#sab


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## scale

> https://ffmpeg.org/ffmpeg-filters.html#scale

缩放输入视频的尺寸。

缩放过滤器通过更改输出样本的宽高比，强制输出显示宽高比与输入相同。

如果输入图像格式与下一个过滤器请求的格式不同，则比例过滤器会将输入转换为请求的格式。

### 参数

- width, w
- height, h 设置输出视频尺寸表达式。默认值为输入尺寸。如果 width 或 w 值为 0，则将输入宽度用于输出。如果 height 或 h 值为 0，则将输入高度用于输出。如果其中一个值中只有一个是 -n 且 n> = 1，则比例滤镜将使用一个值来保持输入图像的宽高比，该值是根据其他指定尺寸计算得出的。但是，此后，请确保计算出的尺寸可以被 n 整除，并在必要时调整该值。如果两个值均为 -n 且 n> = 1，则行为将与先前设置为 0 的两个值相同。
- eval 指定何时计算宽度，高度，x 和 y 表达式。
  - ‘init’ 在过滤器初始化期间或处理命令时，仅对表达式求值一次。默认。
  - ‘frame’ 计算每个传入帧的表达式。
- interl 设置隔行模式。
  - ‘1’ 强制隔行感知缩放。
  - ‘0’ 不要应用隔行缩放。默认。
  - ‘-1’ 根据源帧是否标记为隔行，选择隔行感知缩放。
- flags 设置缩放标志。
- param0, param1 设置缩放算法的输入参数。
- size, s 设置视频大小。
- in_color_matrix
- out_color_matrix 设置输入 / 输出 YCbCr 颜色空间类型。这允许自动检测的值被覆盖，并允许强制使用用于输出和编码器的特定值。如果未指定，则色彩空间类型取决于像素格式。
  - ‘auto’ 自动选择。
  - ‘bt709’ 
  - ‘fcc’
  - ‘bt601’
  - ‘bt470’
  - ‘smpte170m’
  - ‘bt2020’
- in_range
- out_range 设置输入/输出 YCbCr 采样范围。这允许自动检测的值被覆盖，并允许强制使用用于输出和编码器的特定值。如果未指定，则范围取决于像素格式。可能的值：
  - ‘auto/unknown’
  - ‘jpeg/full/pc’
  - ‘mpeg/limited/tv’
- force_original_aspect_ratio 如有必要，请启用或减少输出视频的宽度或高度，以保持原始的宽高比。可能的值：
  - ‘disable’ 按指定比例缩放视频并禁用此功能。
  - ‘decrease’ 如果需要，输出视频的尺寸将自动减小。
  - ‘increase’ 如果需要，输出视频的尺寸将自动增加。此选项的一个有用实例是，当您知道特定设备的最大允许分辨率时，可以使用该分辨率将输出视频限制为该分辨率，同时保持宽高比。例如，设备 A 允许 1280x720 的播放，而您的视频是 1920x800。使用此选项（将其设置为减少）并在命令行中指定 1280x720，则输出为 1280x533。请注意，这与为 w 或 h 指定 -1 有所不同，您仍然需要指定输出分辨率才能使此选项起作用。
- force_divisible_by 与 force_original_aspect_ratio 一起使用时，请确保输出尺寸（宽度和高度）都可被给定的整数整除。这与在 w 和 h 选项中使用 -n 相似。此选项遵循为 force_original_aspect_ratio 设置的值，相应地增加或减少分辨率。视频的宽高比可能会稍作修改。如果您需要使用 force_original_aspect_ratio 使视频适合或超过定义的分辨率，并且在宽度或高度可分割性方面有编码器限制，则此选项非常方便。

w 和 h 选项的值是包含以下常量的表达式：
- in_w, iw
- in_h, ih 输入视频的宽度和高度
- out_w, ow
- out_h, oh 输出的宽度和高度，即宽度和高度表达式指定的填充区域的大小
- a iw / ih
- sar 输入样本宽高比
- dar 输入显示宽高比 (iw / ih) * sar
- hsub
- vsub 水平和垂直色度子样本值。例如，对于像素格式“yuv422p”，hsub 为 2，vsub 为 1。
- ohsub
- ovsub 水平和垂直输出色度子样本值。例如，对于像素格式“yuv422p”，hsub 为 2，vsub 为 1。
- n 输入帧的（顺序）编号，从 0 开始。仅适用于 eval = frame。
- t 输入帧的显示时间戳记，以秒为单位。仅适用于 eval = frame。
- pos 帧在输入流中的位置（字节偏移），如果此信息不可用和 / 或无意义（例如，在合成视频的情况下），则为 NaN。仅适用于 eval = frame。

### 示例

```python
_ = input(src).scale("2*iw", "2*ih").output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]scale=h=2*ih:w=2*iw[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_scale.mp4 -y -hide_banner
[0.5439s]
```

#### 对比

[视频对比链接]

## scale_npp

> https://ffmpeg.org/ffmpeg-filters.html#scale_npp


### 参数

### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## scale2ref

> https://ffmpeg.org/ffmpeg-filters.html#scale2ref


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## scroll

> https://ffmpeg.org/ffmpeg-filters.html#scroll

以恒定速度水平和/或垂直滚动输入视频。

### 参数

- horizontal, h 设置水平滚动速度。默认值为 0。允许的范围是 -1 至 1。负值会更改滚动方向。
- vertical, v 设置垂直滚动速度。默认值为 0。允许的范围是 -1 至 1。负值会更改滚动方向。
- hpos 设置初始水平滚动位置。默认值为 0。允许的范围是 0 到 1。
- vpos 设置初始垂直滚动位置。默认值为 0。允许的范围是 0 到 1。

### 示例

```python
_ = input(src).scroll(h=0.01).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]scroll=h=0.01[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_scroll.mp4 -y -hide_banner
[0.5386s]
```

#### 对比

[视频对比链接]

## scdet

> https://ffmpeg.org/ffmpeg-filters.html#scdet


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## selectivecolor

> https://ffmpeg.org/ffmpeg-filters.html#selectivecolor


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## separatefields

> https://ffmpeg.org/ffmpeg-filters.html#separatefields


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## setdar, setsar

> https://ffmpeg.org/ffmpeg-filters.html#setdar_002c-setsar


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## setfield

> https://ffmpeg.org/ffmpeg-filters.html#setfield


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## setparams

> https://ffmpeg.org/ffmpeg-filters.html#setparams


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## shear

> https://ffmpeg.org/ffmpeg-filters.html#shear

将剪切变换应用于输入视频。

### 参数

- shx X 方向上的剪切因子。默认值为 0。允许的范围是 -2 到 2。
- shy Y 方向上的剪切因子。默认值为 0。允许的范围是 -2 到 2。
- fillcolor, c 设置用于填充转换后视频未覆盖的输出区域的颜色。默认值为“黑色”。
- interp 设置插补类型。可以是 bilinear 或 nearest。默认为双线性。

### 示例

No such filter: 'shear'

## showinfo

> https://ffmpeg.org/ffmpeg-filters.html#showinfo


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## showpalette

> https://ffmpeg.org/ffmpeg-filters.html#showpalette


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## shuffleframes

> https://ffmpeg.org/ffmpeg-filters.html#shuffleframes


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## shufflepixels

> https://ffmpeg.org/ffmpeg-filters.html#shufflepixels


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## shuffleplanes

> https://ffmpeg.org/ffmpeg-filters.html#shuffleplanes


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## signalstats

> https://ffmpeg.org/ffmpeg-filters.html#signalstats


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## signature

> https://ffmpeg.org/ffmpeg-filters.html#signature


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## smartblur

> https://ffmpeg.org/ffmpeg-filters.html#smartblur

使输入视频模糊而不影响轮廓。

### 参数

- luma_radius, lr 设置亮度半径。选项值必须是 [0.1,5.0] 范围内的浮点数，该浮点数指定用于模糊图像的高斯滤波器的方差（如果较大，则较慢）。默认值为 1.0。
- luma_strength, ls 设置亮度强度。选项值必须是在 [-1.0,1.0] 范围内配置浮点数的浮点数。[0.0,1.0] 中包含的值将使图像模糊，而 [-1.0,0.0] 中包含的值将使图像锐化。默认值为 1.0。
- luma_threshold, lt 设置亮度阈值作为系数，以确定像素是否应该模糊。选项值必须是 [-30,30] 范围内的整数。值为 0 将过滤所有图像，[0,30] 中包含的值将过滤平坦区域，[-30,0] 中包含的值将过滤边缘。预设值为 0。
- chroma_radius, cr 设置色度半径。选项值必须是 [0.1,5.0] 范围内的浮点数，该浮点数指定用于模糊图像的高斯滤波器的方差（如果较大，则较慢）。默认值为 luma_radius。
- chroma_strength, cs 设置色度强度。选项值必须是在 [-1.0,1.0] 范围内配置浮点数的浮点数。[0.0,1.0] 中包含的值将使图像模糊，而 [-1.0,0.0] 中包含的值将使图像锐化。默认值为 luma_strength。
- chroma_threshold, ct 设置用作系数的色度阈值，以确定是否应模糊像素。选项值必须是 [-30,30] 范围内的整数。值为 0 将过滤所有图像，[0,30] 中包含的值将过滤平坦区域，[-30,0] 中包含的值将过滤边缘。默认值为 luma_threshold。

如果未显式设置色度选项，则会设置相应的亮度值。

### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## sobel

> https://ffmpeg.org/ffmpeg-filters.html#sobel


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## spp

> https://ffmpeg.org/ffmpeg-filters.html#spp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## sr

> https://ffmpeg.org/ffmpeg-filters.html#sr

通过应用基于卷积神经网络的超分辨率方法之一来缩放输入。支持以下模型：

- Super-Resolution Convolutional Neural Network model (SRCNN). 
- Efficient Sub-Pixel Convolutional Neural Network model (ESPCN).

### 参数

- dnn_backend native/tensorflow
- model 设置模型文件的路径，以指定网络体系结构及其参数。请注意，不同的后端使用不同的文件格式。TensorFlow 和 native 后端只能按其格式加载文件。
- scale_factor 设置 SRCNN 模型的比例因子。允许值为 2、3 和 4。默认值为 2。SRCNN 模型必须使用比例因子，因为它接受使用具有适当比例因子的双三次放大来放大输入。

### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## ssim

> https://ffmpeg.org/ffmpeg-filters.html#ssim


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## stereo3d

> https://ffmpeg.org/ffmpeg-filters.html#stereo3d


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## streamselect, astreamselect

> https://ffmpeg.org/ffmpeg-filters.html#astreamselect


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## subtitles

> https://ffmpeg.org/ffmpeg-filters.html#subtitles


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## super2xsai

> https://ffmpeg.org/ffmpeg-filters.html#super2xsai


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## swaprect

> https://ffmpeg.org/ffmpeg-filters.html#swaprect


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## swapuv

> https://ffmpeg.org/ffmpeg-filters.html#swapuv


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tblend

> https://ffmpeg.org/ffmpeg-filters.html#tblend


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## telecine

> https://ffmpeg.org/ffmpeg-filters.html#telecine


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## thistogram

> https://ffmpeg.org/ffmpeg-filters.html#thistogram


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## threshold

> https://ffmpeg.org/ffmpeg-filters.html#threshold


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## thumbnail

> https://ffmpeg.org/ffmpeg-filters.html#thumbnail

在给定的连续帧序列中选择最具代表性的帧。

### 参数

- n 设置帧批量大小进行分析； 在一组 n 帧中，过滤器将选择其中一个，然后处理下一批 n 帧直到结束。默认值为 100。

由于过滤器会跟踪整个帧序列，因此较大的n值将导致较高的内存使用率，因此不建议使用较高的值。

### 示例

```python
_ = input(src).thumbnail(50).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]thumbnail=100[tag0]" -map [tag0] C:\Users\Admin\Videos\transform\v0_thumbnail_%d.png -y -hide_banner
[0.4287s]
```

#### 对比

[视频对比链接]

## tile

> https://ffmpeg.org/ffmpeg-filters.html#tile


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tinterlace

> https://ffmpeg.org/ffmpeg-filters.html#tinterlace


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tmedian

> https://ffmpeg.org/ffmpeg-filters.html#tmedian


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tmidequalizer

> https://ffmpeg.org/ffmpeg-filters.html#tmidequalizer


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tmix

> https://ffmpeg.org/ffmpeg-filters.html#tmix


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tonemap

> https://ffmpeg.org/ffmpeg-filters.html#tonemap


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## tpad

> https://ffmpeg.org/ffmpeg-filters.html#tpad


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## transpose

> https://ffmpeg.org/ffmpeg-filters.html#transpose


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## transpose_npp

> https://ffmpeg.org/ffmpeg-filters.html#transpose_npp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## trim

> https://ffmpeg.org/ffmpeg-filters.html#trim

修剪输入，以便输出包含输入的一个连续子部分。只作用于视频流。

### 参数

- start 指定保留部分的开始时间，即带有时间戳开始的帧将是输出中的第一帧。
- end 指定要删除的第一帧的时间，即紧接时间戳结束的那一帧之前的帧将是输出中的最后一帧。
- start_pts 这与开始相同，除了此选项以时基单位而不是秒设置开始时间戳。
- end_pts 这与结束相同，除了此选项以时基单位而不是秒设置结束时间戳记。
- duration 输出的最大持续时间（以秒为单位）。
- start_frame 应该传递到输出的第一帧的编号。
- end_frame 应该删除的第一帧的编号。

开始，结束和持续时间表示为持续时间规范。

> https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax

请注意，开始 / 结束选项和持续时间选项的前两组看帧时间戳，而 _frame 变体仅对通过过滤器的帧进行计数。另请注意，此过滤器不会修改时间戳。如果希望输出时间戳从零开始，请在调整过滤器之后插入 setpts 过滤器。

如果设置了多个开始或结束选项，则此过滤器将尽量保持贪婪并保留所有与至少一个指定约束匹配的帧。要仅保留一次与所有约束匹配的零件，请链接多个 trim 过滤器。

默认设置为保留所有输入。因此可以设置，例如只是将所有内容保留在指定时间之前的最终值。

### 示例

```python
_ = input(src).trim(1, 3).output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]trim=1:3[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_trim.mp4 -y -hide_banner
[0.4053s]
```

#### 对比

[视频对比链接]

## unpremultiply

> https://ffmpeg.org/ffmpeg-filters.html#unpremultiply


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## unsharp

> https://ffmpeg.org/ffmpeg-filters.html#unsharp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## untile

> https://ffmpeg.org/ffmpeg-filters.html#untile


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## uspp

> https://ffmpeg.org/ffmpeg-filters.html#uspp


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## v360

> https://ffmpeg.org/ffmpeg-filters.html#v360


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vaguedenoiser

> https://ffmpeg.org/ffmpeg-filters.html#vaguedenoiser


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vectorscope

> https://ffmpeg.org/ffmpeg-filters.html#vectorscope


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vidstabdetect

> https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vidstabtransform

> https://ffmpeg.org/ffmpeg-filters.html#vidstabtransform


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vflip

> https://ffmpeg.org/ffmpeg-filters.html#vflip

垂直翻转输入视频。

### 参数

无。

### 示例

```python
_ = input(src).vflip().output(dst).run()
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0]vflip[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_vflip.mp4 -y -hide_banner
[0.3931s]
```

#### 对比

[视频对比链接]

## vfrdet

> https://ffmpeg.org/ffmpeg-filters.html#vfrdet


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vibrance

> https://ffmpeg.org/ffmpeg-filters.html#vibrance


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vif

> https://ffmpeg.org/ffmpeg-filters.html#vif


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vignette

> https://ffmpeg.org/ffmpeg-filters.html#vignette

制作或反转自然渐晕效果。

### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vmafmotion

> https://ffmpeg.org/ffmpeg-filters.html#vmafmotion


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## vstack

> https://ffmpeg.org/ffmpeg-filters.html#vstack

垂直堆叠输入视频。

所有流必须具有相同的像素格式和相同的宽度。

请注意，此过滤器比使用覆盖和填充过滤器创建相同的输出要快。

### 参数

- inputs 设置输入流的数量。预设值为 2。
- shortest 如果设置为 1，则在最短输入终止时强制输出终止。预设值为 0。

### 示例

```python
vtools.vstack_videos(dst, v1, v1)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\v1.mp4 -filter_complex "[0][1]vstack=inputs=2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\videos_hstack.mp4 -y -hide_banner
[17.4009s]
```

#### 对比

[视频对比链接]

## w3fdif

> https://ffmpeg.org/ffmpeg-filters.html#w3fdif


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## waveform

> https://ffmpeg.org/ffmpeg-filters.html#waveform


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## weave, doubleweave

> https://ffmpeg.org/ffmpeg-filters.html#doubleweave


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## xbr

> https://ffmpeg.org/ffmpeg-filters.html#xbr


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## xfade

> https://ffmpeg.org/ffmpeg-filters.html#xfade

将交叉淡入淡出从一个输入视频流应用到另一输入视频流。 交叉渐变适用于指定的持续时间。

### 参数

- transition 指定转场
- duration 设置淡入淡出持续时间（以秒为单位）。默认持续时间为 1 秒。
- offset 设置相对于第一个输入流的淡入淡出开始时间（以秒为单位）。默认偏移量为 0。
- expr 为自定义过渡效果设置表达式。

### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## xmedian

> https://ffmpeg.org/ffmpeg-filters.html#xmedian


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## xstack

> https://ffmpeg.org/ffmpeg-filters.html#xstack

将视频输入堆叠到自定义布局中。所有流必须具有相同的像素格式。请注意，如果输入大小不同，则可能会出现间隙或重叠。

### 参数

- inputs 设置输入流的数量。预设值为 2。
- layout 指定输入的布局。此选项要求用户明确设置所需的布局配置。这将设置每个视频输入在输出中的位置。每个输入均以“|”分隔。第一个数字代表列，第二个数字代表行。数字从 0 开始，并以“_”分隔。可以选择使用 wX 和 hX，其中 X 是从中获取宽度或高度的视频输入。以“+”分隔时，可以使用多个值。在这种情况下，将值相加。请注意，如果输入大小不同，可能会出现间隙，因为并非所有输出视频帧都会被填充。同样，如果视频的位置没有为相邻视频的整个帧留出足够的空间，它们也可以彼此重叠。对于 2 个输入，默认布局设置为 0_0 | w0_0。在所有其他情况下，必须由用户设置布局。
- shortest 如果设置为 1，则在最短输入终止时强制输出终止。预设值为 0。
- fill 如果设置为有效颜色，则所有未使用的像素将被该颜色填充。默认情况下，填充设置为无，因此将其禁用。

### 示例

#### 2x2 四格布局

```
input1(0, 0)  | input3(w0, 0)
input2(0, h0) | input4(w0, h0)
```

```python
vtools.xstack_videos(
        media_v0, media_v1, media_v2, media_v0,
        dst=dst, layout="0_0|0_h0|w0_0|w0_h0",
)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0][1][2][3]xstack=inputs=4:layout=0_0|0_h0|w0_0|w0_h0:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_xstack.mp4 -y -hide_banner
[0.7751s]
```

#### 对比

[视频对比链接]

#### 1x4 四格布局

```
input1(0, 0)
input2(0, h0)
input3(0, h0+h1)
input4(0, h0+h1+h2)
```

```python
vtools.xstack_videos(
        media_v0, media_v1, media_v2, media_v0,
        dst=dst, layout="0_0|0_h0|0_h0+h1|0_h0+h1+h2",
)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0][1][2][3]xstack=inputs=4:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_xstack2.mp4 -y -hide_banner
[0.6386s]
```

#### 对比

[视频对比链接]

#### 3x3 四格布局

```
input1(0, 0)       | input4(w0, 0)      | input7(w0+w3, 0)
input2(0, h0)      | input5(w0, h0)     | input8(w0+w3, h0)
input3(0, h0+h1)   | input6(w0, h0+h1)  | input9(w0+w3, h0+h1)
```

```python
vtools.xstack_videos(
        media_v0, media_v1, media_v2,
        media_v1, media_v2, media_v0,
        media_v2, media_v0, media_v1,
        dst=dst, layout="0_0|0_h0|0_h0+h1|w0_0|w0_h0|w0_h0+h1|w0+w3_0|w0+w3_h0|w0+w3_h0+h1",
)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -filter_complex "[0][1][2][3][4][5][6][7][8]xstack=inputs=9:layout=0_0|0_h0|0_h0+h1|w0_0|w0_h0|w0_h0+h1|w0+w3_0|w0+w3_h0|w0+w3_h0+h1:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_xstack3.mp4 -y -hide_banner
[1.4246s]
```

#### 对比

[视频对比链接]

#### 4x4 四格布局

```
input1(0, 0)       | input5(w0, 0)       | input9 (w0+w4, 0)       | input13(w0+w4+w8, 0)
input2(0, h0)      | input6(w0, h0)      | input10(w0+w4, h0)      | input14(w0+w4+w8, h0)
input3(0, h0+h1)   | input7(w0, h0+h1)   | input11(w0+w4, h0+h1)   | input15(w0+w4+w8, h0+h1)
input4(0, h0+h1+h2)| input8(w0, h0+h1+h2)| input12(w0+w4, h0+h1+h2)| input16(w0+w4+w8, h0+h1+h2)
```

```python
vtools.xstack_videos(
        media_v0, media_v1, media_v2, media_v0,
        media_v1, media_v2, media_v0, media_v2,
        media_v1, media_v2, media_v0, media_v1,
        media_v1, media_v2, media_v2, media_v0,
        dst=dst, layout="0_0|0_h0|0_h0+h1|0_h0+h1+h2|w0_0|w0_h0|w0_h0+h1|w0_h0+"
                        "h1+h2|w0+w4_0|w0+w4_h0|w0+w4_h0+h1|w0+w4_h0+h1+h2|w0+w4"
                        "+w8_0|w0+w4+w8_h0|w0+w4+w8_h0+h1|w0+w4+w8_h0+h1+h2",
)
```

```
ffmpeg -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\1.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\2.mp4 -hwaccel cuda -vcodec h264_cuvid -i testdata\media\0.mp4 -filter_complex "[0][1][2][3][4][5][6][7][8][9][10][11][12][13][14][15]xstack=inputs=16:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2|w0_0|w0_h0|w0_h0+h1|w0_h0+h1+h2|w0+w4_0|w0+w4_h0|w0+w4_h0+h1|w0+w4_h0+h1+h2|w0+w4+w8_0|w0+w4+w8_h0|w0+w4+w8_h0+h1|w0+w4+w8_h0+h1+h2:shortest=0[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_xstack4.mp4 -y -hide_banner
```

#### 对比

[视频对比链接]

#### 2x2 四格布局

```

```

```python

```

```

```

#### 对比

[视频对比链接]

## yadif

> https://ffmpeg.org/ffmpeg-filters.html#yadif


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## yadif_cuda

> https://ffmpeg.org/ffmpeg-filters.html#yadif_cuda


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## yaepblur

> https://ffmpeg.org/ffmpeg-filters.html#yaepblur


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]

## zoompan

> https://ffmpeg.org/ffmpeg-filters.html#zoompan

缩放平移效果。

### 参数

- zoom, z 设置缩放表达式。范围是 1-10。默认值为 1。
- x
- y 设置 x 和 y 表达式。默认值为 0。
- d 以帧数设置持续时间表达式。设置单个输入图像将持续多少帧效果。
- s 设置输出图像的大小，默认为“hd720”。
- fps 设置输出帧频，默认为“25”。

每个表达式可以包含以下常量：

- in_w, iw
- in_h, ih 输入视频的宽度和高度
- out_w, ow
- out_h, oh 输出的宽度和高度，即宽度和高度表达式指定的填充区域的大小
- in 输入帧数
- on 输出帧数
- in_time, it 输入时间戳，以秒为单位。如果输入的时间戳未知，则为 NAN。
- out_time, time, ot 输出时间戳，以秒为单位。
- x
- y 根据当前输入框的“x”和“y”表达式最后计算的“x”和“y”位置。
- px
- py 上一个输入帧的最后一个输出帧的“x”和“y”，如果还没有这样的帧（第一个输入帧），则为 0。
- zoom 上一次从“z”表达式为当前输入帧计算的缩放
- pzoom 最近计算的上一个输入帧的最后一个输出帧的缩放
- duration 当前输入帧的输出帧数。根据每个输入帧的“d”表达式计算得出
- pduration 为上一个输入帧创建的输出帧数
- a iw / ih
- sar 输入样本宽高比
- dar 输入显示宽高比 (iw / ih) * sar

### 示例

```python
_ = input(i1).zoompan(z="min(zoom+0.0015,1.5)",
                       d=700, x="if(gte(zoom,1.5),x,x+1/a)",
                       y="if(gte(zoom,1.5),y,y+1)").output(dst).run()
```

```
ffmpeg -i testdata\i1.jpg -filter_complex "[0]zoompan=d=700:x=if(gte(zoom\,1.5)\,x\,x+1/a):y=if(gte(zoom\,1.5)\,y\,y+1):z=min(zoom+0.0015\,1.5)[tag0]" -vcodec h264_nvenc -map [tag0] C:\Users\Admin\Videos\transform\v0_zoompan.mp4 -y -hide_banner
[3.4039s]
```

#### 对比

[视频对比链接]

## zscale

> https://ffmpeg.org/ffmpeg-filters.html#zscale


### 参数


### 示例

```python

```

```

```

#### 对比

[视频对比链接]
