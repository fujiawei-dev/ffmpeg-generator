<!--
 * @Date: 2021.03.08T22:56:00+08:00
 * @Description: FFmpeg Audio/Video Sources
 * @LastEditors: Rustle Karl
 * @LastEditTime: 2021.05.10 12:09:41
-->

音频源/视频源是作为输入的参数，不能当成滤镜处理。

## buffer

> https://ffmpeg.org/ffmpeg-filters.html#buffer

缓冲视频帧，其可以作为滤镜链图的环节。

### 参数

- video_size 指定视频尺寸
- width 输入视频宽
- height 输入视频高
- pix_fmt 像素格式描述，可以是一个表征像素格式的号码或者名称
- time_base 指定时间戳时基
- frame_rate 指定帧率
- pixel_aspect, sar 输入视频的像素长宽比
- sws_param 指定一个可选参数用于在自动检测到输入视频大小或者格式变化时插入放缩滤镜。
- hw_frames_ctx 当使用硬件像素格式时，这应该是对描述输入帧的 AVHWFramesContext 的引用。

### 示例

不懂，不知道有什么用，略。

## cellauto

> https://ffmpeg.org/ffmpeg-filters.html#cellauto

创建由基本元胞自动机生成的模式。

细胞自动发送器的初始状态可以通过 `filename` 选项和 `pattern` 选项的模式来定义，如果不知道则是随机初始状态。每个新帧中的一个新行视频充满了下一代细胞自动发生器的结果。当 `scroll` 选项被指定时，整个帧会被滚动填充。

### 参数

- filename, f 用于读取细胞自动发生器初始状态的文件。在文件中第一行从行首开始每个非空字符被认为是活的细胞直到换行，更多行则被忽略
- pattern, p 用于定义细胞自动发生器初始状态，从指定字符串开始作为起始行每个非空字符作为一个细胞直到换行（或者字符串结束），更多的行被忽略
- rate, r 设置视频帧率，默认 25
- random_fill_ratio, ratio 设置初始随机填充率，是浮点数，范围 0-1，默认 `1/PHI` 此选项在指定了初始文件或模式时被忽略
- random_seed, seed 设置随机填充初始种子，必须是整数，范围 0-`UINT32_MAX`。不指定或显式指定为 -1，将尝试使用一个更好的随机种子
- rule 设置细胞自动发生规则，是 0-255 间数，默认 110
- size, s 设置输出视频尺寸，如果尺寸被设置，其宽必须匹配 `pattern` 字符串中最大行。如果 `filename` 和 `pattern` 都没有指定，则默认为 `320x518`
- scroll 如果为 1，向上滚出已经填满的行。如果为 0，到最后一行后，新行将覆盖第一行，默认为 1
- start_full, full 如果设置为 1，则需要完全填满后才输出第一帧，这时默认行为，设置为 0 则禁用
- stitch 如果设置为 1，左和右连接在一起，这是默认行为，为 0 则禁用

### 示例

```python

```

```

```

## coreimagesrc

> https://ffmpeg.org/ffmpeg-filters.html#coreimagesrc

### 参数



### 示例

- 从`pattern`读取初始化，输出为 200x400.cellauto=f=pattern:s=200x400
- 随机化输出初始化，宽200个细胞，填充率为2/3:cellauto=ratio=2/3:s=200x200
- 以规则18创建一个由单细胞开始，初始化宽度为100的源：cellauto=p=@:s=100x400:full=0:rule=18
- 指定一个详细的初始模式:cellauto=p='@@ @ @@':s=100x400:full=0:rule=18

```python

```

```

```

## gradients

> https://ffmpeg.org/ffmpeg-filters.html#gradients

### 参数


### 示例

```python

```

```

```

## mandelbrot

> https://ffmpeg.org/ffmpeg-filters.html#mandelbrot

生成一个曼德尔勃特（Mandelbrot）集合分形，它逐渐从点(start_x,start_y)放大

### 参数

- end_pts设置终端`pts`值，默认400.
- end_scale设置终端缩放值，必须是浮点数，默认0.3.
- inner设置内部着色模式，该算法用于绘制曼德布洛特分形内部区域.允许下面的值:black设置black模式. 
convergence设置时间收缩模式 
mincol设置基于点的颜色最接近的起源迭代 
period设置时间模式 默认为mincol.
- bailout设置bailout值，默认为10
- maxiter设置最大迭代执行的渲染算法，默认7189.
- outer设置外部着色模式，允许下面的值：iteration_count设置为迭代计算模式 
normalized_iteration_count设置为规范化的迭代计算模式 默认为normalized_iteration_count.
- rate, r设置帧率，可以是表达式和每秒帧数，默认为25
- size, s设置帧尺寸，语法同于`ffmpeg-utils`手册中的[视频尺寸](ffmpeg-doc-cn-07.md#视频尺寸分辨率)章节. 默认"640x480".
- start_scale设置初始化放大值，默认为3.0.
- start_x设置初始化点的x坐标，必须是-100 到100间的浮点数，默认为 -0.743643887037158704752191506114774.
- start_y设置初始化点的y坐标，必须是-100 到100间的浮点数，默认为-0.131825904205311970493132056385139. 

### 示例

```python

```

```

```

## mptestsrc

> https://ffmpeg.org/ffmpeg-filters.html#mptestsrc

生成各种测试模式，以作为MPlayer测试滤镜。生成视频是固定的256x256分辨率。

### 参数

- rate, r指定帧率，是默认每秒帧数数字。也可以以`frame_rate_num/frame_rate_den`格式设定整数和浮点数以及帧频短语都是有效值，默认25
- duration, d设置持续时间秒数，语法同于[持续时间](ffmpeg-doc-cn-07.md#持续时间)章节，如果不指定或者指定为负数，表示持续不断
- test, t设置测试项的数字或者名称，允许下面的值：dc_luma

这个源用于在特定编码功能测试支持下面选项：

dc_chroma
freq_luma
freq_chroma
amp_luma
amp_chroma
cbp
mv
ring1
ring2
all默认为"all",表示都要测试例如：	mptestsrc=t=dc_luma
将进行`dc_luma`测试

### 示例

```python

```

```

```

## frei0r_src

> https://ffmpeg.org/ffmpeg-filters.html#frei0r_src

提供一个frei0r源编译需要`frei0r`头以及配置项`--enable-frei0r`，接受如下参数：

### 参数

- size生成视频大小。语法同于`ffmpeg-utils`手册中的[视频尺寸](ffmpeg-doc-cn-07.md#视频尺寸分辨率)章节.
- framerate设置帧率，值为数字字符串，或者`num/den`形式字符串或者帧率短语
- filter_name这个名字frei0r源到负载。获得有关frei0r的更多信息以及如何设置参数,读取文档中的frei0r视频滤镜部分。
- filter_params由’|’分隔的参数列表传递给`frei0r`源例如：要产生一个200x200分辨率，帧率为10，产生一个frei0r源用作`partik0l`	frei0r_src=size=200x200:framerate=10:filter_name=partik0l:filter_params=1234 [overlay]; [in][overlay] overlay

### 示例

```python

```

```

```

## life

> https://ffmpeg.org/ffmpeg-filters.html#life

产生life模式这个源基于John Conway’s life游戏源输入一个网格、每个像素（代表细胞）可以有2个状态，活或者死。每个细胞有8个邻国水平、垂直或对角相邻。根据采用的规则发展网格,它指定邻居活细胞的数量会使细胞生存或出生，这里`rule`选项在下面介绍。这个源支持下面的选项：

### 参数

- filename, f设置读取初始化网格的文件。在文件中每个非空字符代表存活的细胞，换行结束一行。如果没有指定则随机生成
- rate, r设置视频帧率，默认25.
- random_fill_ratio, ratio设置随机初始化随机网格填充率，值为0-1的浮点数，默认为`1/PHI`，在设置了`filename`时忽略
- random_seed, seed设置随机种子，值为0 - `UINT32_MAX`如果设置为-1或者不设置，表示尽量用优化的种子
- rule设置规则规则可以是指定代码的形式"SNS/BNB"，这里`NS`和`NB`是0-8的数字序数，`NS`在一个存活细胞周围还存活的细胞数，`NB`指定周围要新生的细胞数，`s`和`b`分别是`S`和`B`的替代另外一个规则可以被描述为18位的整数。其中高段9位表示存活细胞周围存活细胞状态数，低段9位则为要新生的细胞状态数。例如数字6153=(12<<9)+9，表示细胞周围有12个存活细胞，新生为9的规则，其等效于"S23/B03".默认为"S23/B3",它是原始的Conway’s 游戏规则。如果它周围有2或者3个细胞将新生细胞，否则将死亡细胞
- size, s设置输出视频分辨率，语法同于`ffmpeg-utils`手册中的[视频尺寸](ffmpeg-doc-cn-07.md#视频尺寸分辨率)章节当`filename`被设定，则默认会采用输入文件的最大行宽。如果设置了这个值则需与输入文件相匹配。如果没有设置`filename`则默认为 "320x240" (用于随机初始化模式).
- stitch如果设置为1，则左右网格边和上下网格边缝合在一起（连续面），默认为1
- mold设置细胞分解速度。如果设置，则为死细胞将从 `death_color` 在`mold`步骤内转变为 `mold_color` 的速度。范围0-255。
- life_color设置存活的细胞颜色 (或新生) 
- death_color设置死亡细胞颜色。如果`mold`被设置，则为死亡后第一个颜色
- mold_color设置分解后颜色，作为绝对死亡或已被分解的细胞颜色前面3个颜色

### 示例

- 从模板读取一个网格，分辨率为300x300:life=f=pattern:s=300x300
- 填充率2/3的随机初始化，尺寸200x200, :life=ratio=2/3:s=200x200
- 指定一个规则的随机初始化和生成:life=rule=S14/B34
- 前面所有例子，且还伴有`mold`（分解）效果，在ffplay中播放:ffplay -f lavfi life=s=300x200:mold=10:r=60:ratio=0.1:death_color=#C83232:life_color=#00ff00,scale=1200:800:flags=16

```python

```

```

```

## allrgb, allyuv, color, haldclutsrc, nullsrc, pal75bars, pal100bars, rgbtestsrc, smptebars, smptehdbars, testsrc, testsrc2, yuvtestsrc

- `allrgb` 源返回所有 RGB 颜色且大小为 4096x4096 的帧
- `allyuv` 源返回所有 YUV 颜色且大小为 4096x4096 的帧
- `color` 源提供一致的颜色输入
- `haldclutsrc` 源提供哈尔德（Hald）CLUT 输入
- `nullsrc` 源返回未处理的视频帧，作为滤镜中可以忽略的输入数据
- `pal75bars` 源产生 75％的颜色级别生成颜色条图案
- `pal100bars` 源产生 100％的颜色级别生成颜色条图案
- `rgbtestsrc` 源产生 `RGB` 测试模板，用于检测对比 `RGB` 与 `BGR` 问题，可以看到一个红色、绿色和蓝色的从上到下条纹
- `smptebars` 源产生颜色条模板
- `smptehdbars` 源产生颜色条模板
- `testsrc` 源产生测试视频模板，显示颜色模板和滚动的梯形以及时间戳
- `testsrc2` 源产生测试视频模板，显示颜色模板和滚动的梯形以及时间戳
- `yuvtestsrc` 源生成一个YUV测试模式，从上到下看到 y, cb 和 cr 的条纹。

### 参数

- color, c 指定源颜色，仅作 `color` 源中有效
- level 指定 Hald CLUT 的层次。仅在 `haldclutsrc` 有效。`level` 中的 `N` 用于生成一个 `N * N * N` 像素为单位矩阵用于三维查找表。每个组件都是编码在 1 /(N * N) 范围内
- size, s 指定源视频尺寸。默认值为 `320x240`，这个选项在 `haldclutsrc` 中无效
- rate, r 设置帧率，默认为 25
- sar 设置样品长宽比（像素点长宽比）
- duration, d 设置源视频持续时间，不设置或者设置为负数，表示持续存在。
- decimals, n 设置屏幕时间戳的小数数字显示，仅在 `testsrc` 源有效显示的时间戳值将对应于原来的时间戳值乘以 `10 的 X 次方数 ` 的指定值。默认为 0。

### 示例

#### 用 FFplay 播放

```python
_ = run_ffplay("testsrc=size=400x300:rate=60", f="lavfi")
```

```
ffplay -hide_banner -f lavfi testsrc=size=900x400:rate=60
```

```python
_ = run_ffplay("allrgb", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("color=c=red@0.2:s=1600x900:r=10", f="lavfi")
_ = run_ffplay("haldclutsrc", f="lavfi")
_ = run_ffplay("pal75bars", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("allyuv", f="lavfi")
_ = run_ffplay("rgbtestsrc", f="lavfi")
_ = run_ffplay("smptebars", f="lavfi")
_ = run_ffplay("smptehdbars", f="lavfi")
_ = run_ffplay("testsrc=size=400x300:rate=60", f="lavfi")
_ = run_ffplay("testsrc2=s=1600x900", f="lavfi")
_ = run_ffplay("yuvtestsrc=s=1600x900", f="lavfi")
```

#### 用 FFmpeg 预览

预览的播放进行了加速。

```python
ffmpeg.input_source("testsrc", size="600x900", rate=60).output(preview=True).run()
```

```
ffmpeg -f lavfi -i testsrc=size=600x900:rate=60 -f sdl preview -y -hide_banner
```

## openclsrc

> https://ffmpeg.org/ffmpeg-filters.html#openclsrc


### 参数


### 示例

```python

```

```

```

## sierpinski

> https://ffmpeg.org/ffmpeg-filters.html#sierpinski

### 参数



### 示例

```python

```

```

```

## buffersink

> https://ffmpeg.org/ffmpeg-filters.html#buffersink

缓冲视频帧，可作为滤镜链图中有效的结束点。这个槽主要用于编程使用，特别是通过`libavfilter/buffersink.h`的接口或选择操作系统它接受指向`AVABufferSinkContext`结构的指针，用于定义传入缓冲区的格式，作为不透明参数传递给`avfilter_init_filter`以初始化。

### 参数


### 示例

```python

```

```

```

## nullsink

> https://ffmpeg.org/ffmpeg-filters.html#nullsink

Null（空）视频槽，绝对没有输入的视频。它主要用作模板以分析/调试工具。

### 参数


### 示例

```python

```

```

```
