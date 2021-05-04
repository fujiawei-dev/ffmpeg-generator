'''
Date: 2021.03.03 08:17:05
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 13:31:29
'''
from pathlib import Path
from typing import Union

from .avfilters import filter
from .._utils import drop_empty_dict_values
from ..constants import LINUX
from ..nodes import filterable, FilterableStream, FilterNode, Stream

__all__ = [
    "gltransition",
    "overlay",
]

"""OpenGL Filters"""


@filterable()
def gltransition(*streams: Stream, source: Union[str, Path] = None,
                 offset: float = 0, duration: float = 0) -> FilterableStream:
    """Combine two videos with transition effects.

    Args:
        source: Transition effect source file.
        offset: Specify the transition effect to start at offset seconds of the first video.
        duration: Duration of transition effect.
    """
    if not LINUX:
        raise NotImplementedError('Only supports Linux system, and FFmpeg must be recompiled')

    return FilterNode(streams, gltransition.__name__, max_inputs=2,
                      kwargs=drop_empty_dict_values({}, source=source, offset=offset, duration=duration)).stream()


"""Video Filters

https://ffmpeg.org/ffmpeg-filters.html#Video-Filters
"""


@filterable()
def addroi(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#addroi"""
    return filter(stream, addroi.__name__, *args, **kwargs)


@filterable()
def alphaextract(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#alphaextract"""
    return filter(stream, alphaextract.__name__, *args, **kwargs)


@filterable()
def alphamerge(*streams: Stream) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#alphamerge"""
    return filter(streams, alphamerge.__name__, max_inputs=2)


@filterable()
def amplify(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#amplify"""
    return filter(stream, amplify.__name__, *args, **kwargs)


@filterable()
def ass(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ass"""
    return filter(stream, ass.__name__, *args, **kwargs)


@filterable()
def atadenoise(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#atadenoise"""
    return filter(stream, atadenoise.__name__, *args, **kwargs)


@filterable()
def avgblur(stream: Stream, x: int = None, y: int = None,
            planes: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#avgblur"""
    return filter(stream, avgblur.__name__, sizeX=x, sizeY=y, planes=planes)


@filterable()
def bbox(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bbox"""
    return filter(stream, bbox.__name__, *args, **kwargs)


@filterable()
def bilateral(stream: Stream, s: float = None, r: float = None,
              planes: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bilateral"""
    return filter(stream, bilateral.__name__, sigmaS=s, sigmaR=r, planes=planes)


@filterable()
def bitplanenoise(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bitplanenoise"""
    return filter(stream, bitplanenoise.__name__, *args, **kwargs)


@filterable()
def blackdetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#blackdetect"""
    return filter(stream, blackdetect.__name__, *args, **kwargs)


@filterable()
def blackframe(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#blackframe"""
    return filter(stream, blackframe.__name__, *args, **kwargs)


@filterable()
def blend(*stream: Stream, all_mode: str = None, all_opacity: float = None,
          all_expr: str = None, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#blend"""
    return filter(stream, blend.__name__, max_inputs=2, all_mode=all_mode, all_opacity=all_opacity, all_expr=all_expr,
                  **kwargs)


@filterable()
def bm3d(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bm3d"""
    return filter(stream, bm3d.__name__, *args, **kwargs)


@filterable()
def boxblur(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#boxblur"""
    return filter(stream, boxblur.__name__, *args, **kwargs)


@filterable()
def bwdif(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#bwdif"""
    return filter(stream, bwdif.__name__, *args, **kwargs)


@filterable()
def cas(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#cas"""
    return filter(stream, cas.__name__, *args, **kwargs)


@filterable()
def chromahold(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#chromahold"""
    return filter(stream, chromahold.__name__, *args, **kwargs)


@filterable()
def chromakey(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#chromakey"""
    return filter(stream, chromakey.__name__, *args, **kwargs)


@filterable()
def chromanr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#chromanr"""
    return filter(stream, chromanr.__name__, *args, **kwargs)


@filterable()
def chromashift(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#chromashift"""
    return filter(stream, chromashift.__name__, *args, **kwargs)


@filterable()
def ciescope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ciescope"""
    return filter(stream, ciescope.__name__, *args, **kwargs)


@filterable()
def codecview(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#codecview"""
    return filter(stream, codecview.__name__, *args, **kwargs)


@filterable()
def colorbalance(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorbalance"""
    return filter(stream, colorbalance.__name__, *args, **kwargs)


@filterable()
def colorcontrast(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorcontrast"""
    return filter(stream, colorcontrast.__name__, *args, **kwargs)


@filterable()
def colorcorrect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorcorrect"""
    return filter(stream, colorcorrect.__name__, *args, **kwargs)


@filterable()
def colorchannelmixer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer"""
    return filter(stream, colorchannelmixer.__name__, *args, **kwargs)


@filterable()
def colorize(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorize"""
    return filter(stream, colorize.__name__, *args, **kwargs)


@filterable()
def colorkey(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorkey"""
    return filter(stream, colorkey.__name__, *args, **kwargs)


@filterable()
def colorhold(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorhold"""
    return filter(stream, colorhold.__name__, *args, **kwargs)


@filterable()
def colorlevels(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorlevels"""
    return filter(stream, colorlevels.__name__, *args, **kwargs)


@filterable()
def colormatrix(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colormatrix"""
    return filter(stream, colormatrix.__name__, *args, **kwargs)


@filterable()
def colorspace(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorspace"""
    return filter(stream, colorspace.__name__, *args, **kwargs)


@filterable()
def colortemperature(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colortemperature"""
    return filter(stream, colortemperature.__name__, *args, **kwargs)


@filterable()
def convolution(stream: Stream, m0: int = None, m1: int = None, m2: int = None,
                m3: int = None, rdiv0: int = None, rdiv1: int = None, rdiv2: int = None,
                rdiv3: int = None, bias0: int = None, bias1: int = None, bias2: int = None,
                bias3: int = None, mode0: int = None, mode1: int = None,
                mode2: int = None, mode3: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#convolution"""

    kwargs = {
        "0m": m0, "1m": m1, "2m": m2, "3m": m3,
        "0rdiv": rdiv0, "1rdiv": rdiv1, "2rdiv": rdiv2, "3rdiv": rdiv3,
        "0bias": bias0, "1bias": bias1, "2bias": bias2, "3bias": bias3,
        "0mode": mode0, "1mode": mode1, "2mode": mode2, "3mode": mode3
    }

    return filter(stream, convolution.__name__, **kwargs)


@filterable()
def convolve(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#convolve"""
    return filter(stream, convolve.__name__, *args, **kwargs)


@filterable()
def copy(stream: Stream) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#copy"""
    return filter(stream, copy.__name__)


@filterable()
def coreimage(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#coreimage"""
    return filter(stream, coreimage.__name__, *args, **kwargs)


@filterable()
def cover_rect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#cover_rect"""
    return filter(stream, cover_rect.__name__, *args, **kwargs)


@filterable()
def crop(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#crop"""
    return filter(stream, crop.__name__, *args, **kwargs)


@filterable()
def cropdetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#cropdetect"""
    return filter(stream, cropdetect.__name__, *args, **kwargs)


@filterable()
def cue(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#cue"""
    return filter(stream, cue.__name__, *args, **kwargs)


@filterable()
def curves(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#curves"""
    return filter(stream, curves.__name__, *args, **kwargs)


@filterable()
def datascope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#datascope"""
    return filter(stream, datascope.__name__, *args, **kwargs)


@filterable()
def dblur(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dblur"""
    return filter(stream, dblur.__name__, *args, **kwargs)


@filterable()
def dctdnoiz(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dctdnoiz"""
    return filter(stream, dctdnoiz.__name__, *args, **kwargs)


@filterable()
def deband(stream: Stream, thr1: float = None, thr2: float = None,
           thr3: float = None, thr4: float = None, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deband"""
    kwargs.update({
        "1thr": thr1, "2thr": thr2,
        "3thr": thr3, "4thr": thr4,
    })

    return filter(stream, deband.__name__, **kwargs)


@filterable()
def deblock(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deblock"""
    return filter(stream, deblock.__name__, *args, **kwargs)


@filterable()
def decimate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#decimate"""
    return filter(stream, decimate.__name__, *args, **kwargs)


@filterable()
def deconvolve(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deconvolve"""
    return filter(stream, deconvolve.__name__, *args, **kwargs)


@filterable()
def dedot(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dedot"""
    return filter(stream, dedot.__name__, *args, **kwargs)


@filterable()
def deflate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deflate"""
    return filter(stream, deflate.__name__, *args, **kwargs)


@filterable()
def deflicker(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deflicker"""
    return filter(stream, deflicker.__name__, *args, **kwargs)


@filterable()
def dejudder(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dejudder"""
    return filter(stream, dejudder.__name__, *args, **kwargs)


@filterable()
def delogo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#delogo"""
    return filter(stream, delogo.__name__, *args, **kwargs)


@filterable()
def derain(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#derain"""
    return filter(stream, derain.__name__, *args, **kwargs)


@filterable()
def deshake(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deshake"""
    return filter(stream, deshake.__name__, *args, **kwargs)


@filterable()
def despill(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#despill"""
    return filter(stream, despill.__name__, *args, **kwargs)


@filterable()
def detelecine(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#detelecine"""
    return filter(stream, detelecine.__name__, *args, **kwargs)


@filterable()
def dilation(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dilation"""
    return filter(stream, dilation.__name__, *args, **kwargs)


@filterable()
def displace(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#displace"""
    return filter(stream, displace.__name__, *args, **kwargs)


@filterable()
def dnn_processing(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dnn_processing"""
    if kwargs.get("set_async"):
        kwargs["async"] = kwargs.pop("set_async")
    return filter(stream, dnn_processing.__name__, *args, **kwargs)


@filterable()
def drawbox(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#drawbox"""
    return filter(stream, drawbox.__name__, *args, **kwargs)


@filterable()
def drawgraph(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#drawgraph"""
    return filter(stream, drawgraph.__name__, *args, **kwargs)


@filterable()
def drawgrid(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#drawgrid"""
    return filter(stream, drawgrid.__name__, *args, **kwargs)


@filterable()
def drawtext(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#drawtext"""
    return filter(stream, drawtext.__name__, *args, **kwargs)


@filterable()
def edgedetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#edgedetect"""
    return filter(stream, edgedetect.__name__, *args, **kwargs)


@filterable()
def elbg(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#elbg"""
    return filter(stream, elbg.__name__, *args, **kwargs)


@filterable()
def entropy(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#entropy"""
    return filter(stream, entropy.__name__, *args, **kwargs)


@filterable()
def epx(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#epx"""
    return filter(stream, epx.__name__, *args, **kwargs)


@filterable()
def eq(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#eq"""
    return filter(stream, eq.__name__, *args, **kwargs)


@filterable()
def erosion(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#erosion"""
    return filter(stream, erosion.__name__, *args, **kwargs)


@filterable()
def estdif(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#estdif"""
    return filter(stream, estdif.__name__, *args, **kwargs)


@filterable()
def exposure(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#exposure"""
    return filter(stream, exposure.__name__, *args, **kwargs)


@filterable()
def extractplanes(stream: Stream, planes: str = None) -> FilterNode:
    """https://ffmpeg.org/ffmpeg-filters.html#extractplanes"""
    return FilterNode(stream, extractplanes.__name__, args=[planes])


@filterable()
def fade(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fade"""
    return filter(stream, fade.__name__, *args, **kwargs)


@filterable()
def fftdnoiz(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fftdnoiz"""
    return filter(stream, fftdnoiz.__name__, *args, **kwargs)


@filterable()
def fftfilt(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fftfilt"""
    return filter(stream, fftfilt.__name__, *args, **kwargs)


@filterable()
def field(stream: Stream, t: Union[int, str] = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#field"""
    return filter(stream, field.__name__, type=t)


@filterable()
def fieldhint(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fieldhint"""
    return filter(stream, fieldhint.__name__, *args, **kwargs)


@filterable()
def fieldmatch(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fieldmatch"""
    return filter(stream, fieldmatch.__name__, *args, **kwargs)


@filterable()
def fieldorder(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fieldorder"""
    return filter(stream, fieldorder.__name__, *args, **kwargs)


@filterable()
def afifo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#afifo"""
    return filter(stream, afifo.__name__, *args, **kwargs)


@filterable()
def fillborders(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fillborders"""
    return filter(stream, fillborders.__name__, *args, **kwargs)


@filterable()
def find_rect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#find_rect"""
    return filter(stream, find_rect.__name__, *args, **kwargs)


@filterable()
def floodfill(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#floodfill"""
    return filter(stream, floodfill.__name__, *args, **kwargs)


@filterable()
def format(stream: Stream, *pix_fmts: str) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#format"""
    return filter(stream, format.__name__, pix_fmts="|".join(pix_fmts) or None)


@filterable()
def fps(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fps"""
    return filter(stream, fps.__name__, *args, **kwargs)


@filterable()
def framepack(*streams: Stream, format: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#framepack"""
    return filter(streams, framepack.__name__, max_inputs=2, format=format)


@filterable()
def framerate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#framerate"""
    return filter(stream, framerate.__name__, *args, **kwargs)


@filterable()
def framestep(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#framestep"""
    return filter(stream, framestep.__name__, *args, **kwargs)


@filterable()
def freezedetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#freezedetect"""
    return filter(stream, freezedetect.__name__, *args, **kwargs)


@filterable()
def freezeframes(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#freezeframes"""
    return filter(stream, freezeframes.__name__, *args, **kwargs)


@filterable()
def frei0r(stream: Stream, filter_name: str, filter_params: str) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#frei0r"""
    return filter(stream, frei0r.__name__, filter_name, filter_params)


@filterable()
def fspp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#fspp"""
    return filter(stream, fspp.__name__, *args, **kwargs)


@filterable()
def gblur(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#gblur"""
    return filter(stream, gblur.__name__, *args, **kwargs)


@filterable()
def geq(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#geq"""
    try:
        kwargs["sigmaV"] = kwargs.pop("sigma_v")
    except KeyError:
        pass

    return filter(stream, geq.__name__, *args, **kwargs)


@filterable()
def gradfun(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#gradfun"""
    return filter(stream, gradfun.__name__, *args, **kwargs)


@filterable()
def graphmonitor(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#graphmonitor"""
    return filter(stream, graphmonitor.__name__, *args, **kwargs)


@filterable()
def greyedge(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#greyedge"""
    return filter(stream, greyedge.__name__, *args, **kwargs)


@filterable()
def haldclut(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#haldclut"""
    return filter(stream, haldclut.__name__, *args, **kwargs)


@filterable()
def hflip(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hflip"""
    return filter(stream, hflip.__name__, *args, **kwargs)


@filterable()
def histeq(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#histeq"""
    return filter(stream, histeq.__name__, *args, **kwargs)


@filterable()
def histogram(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#histogram"""
    return filter(stream, histogram.__name__, *args, **kwargs)


@filterable()
def hqdn3d(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hqdn3d"""
    return filter(stream, hqdn3d.__name__, *args, **kwargs)


@filterable()
def hwdownload(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hwdownload"""
    return filter(stream, hwdownload.__name__, *args, **kwargs)


@filterable()
def hwmap(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hwmap"""
    return filter(stream, hwmap.__name__, *args, **kwargs)


@filterable()
def hwupload(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hwupload"""
    return filter(stream, hwupload.__name__, *args, **kwargs)


@filterable()
def hwupload_cuda(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hwupload_cuda"""
    return filter(stream, hwupload_cuda.__name__, *args, **kwargs)


@filterable()
def hqx(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hqx"""
    return filter(stream, hqx.__name__, *args, **kwargs)


@filterable()
def hstack(*streams: Stream, inputs: int = None,
           shortest: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hstack"""
    return filter(streams, hstack.__name__, inputs=inputs or len(streams), shortest=shortest, min_inputs=2)


@filterable()
def hue(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hue"""
    return filter(stream, hue.__name__, *args, **kwargs)


@filterable()
def hysteresis(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#hysteresis"""
    return filter(stream, hysteresis.__name__, *args, **kwargs)


@filterable()
def identity(*stream: Stream) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#identity"""
    return filter(stream, identity.__name__, min_inputs=2)


@filterable()
def idet(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#idet"""
    return filter(stream, idet.__name__, *args, **kwargs)


@filterable()
def il(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#il"""
    return filter(stream, il.__name__, *args, **kwargs)


@filterable()
def inflate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#inflate"""
    return filter(stream, inflate.__name__, *args, **kwargs)


@filterable()
def interlace(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#interlace"""
    return filter(stream, interlace.__name__, *args, **kwargs)


@filterable()
def kerndeint(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#kerndeint"""
    return filter(stream, kerndeint.__name__, *args, **kwargs)


@filterable()
def kirsch(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#kirsch"""
    return filter(stream, kirsch.__name__, *args, **kwargs)


@filterable()
def lagfun(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lagfun"""
    return filter(stream, lagfun.__name__, *args, **kwargs)


@filterable()
def lenscorrection(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lenscorrection"""
    return filter(stream, lenscorrection.__name__, *args, **kwargs)


@filterable()
def lensfun(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lensfun"""
    return filter(stream, lensfun.__name__, *args, **kwargs)


@filterable()
def libvmaf(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#libvmaf"""
    return filter(stream, libvmaf.__name__, *args, **kwargs)


@filterable()
def limiter(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#limiter"""
    return filter(stream, limiter.__name__, *args, **kwargs)


@filterable()
def loop(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#loop"""
    return filter(stream, loop.__name__, *args, **kwargs)


@filterable()
def lut1d(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lut1d"""
    return filter(stream, lut1d.__name__, *args, **kwargs)


@filterable()
def lut3d(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lut3d"""
    return filter(stream, lut3d.__name__, *args, **kwargs)


@filterable()
def lumakey(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lumakey"""
    return filter(stream, lumakey.__name__, *args, **kwargs)


@filterable()
def lutyuv(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#lutyuv"""
    return filter(stream, lutyuv.__name__, *args, **kwargs)


@filterable()
def tlut2(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tlut2"""
    return filter(stream, tlut2.__name__, *args, **kwargs)


@filterable()
def maskedclamp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskedclamp"""
    return filter(stream, maskedclamp.__name__, *args, **kwargs)


@filterable()
def maskedmax(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskedmax"""
    return filter(stream, maskedmax.__name__, *args, **kwargs)


@filterable()
def maskedmerge(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskedmerge"""
    return filter(stream, maskedmerge.__name__, *args, **kwargs)


@filterable()
def maskedmin(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskedmin"""
    return filter(stream, maskedmin.__name__, *args, **kwargs)


@filterable()
def maskedthreshold(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskedthreshold"""
    return filter(stream, maskedthreshold.__name__, *args, **kwargs)


@filterable()
def maskfun(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#maskfun"""
    return filter(stream, maskfun.__name__, *args, **kwargs)


@filterable()
def mcdeint(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mcdeint"""
    return filter(stream, mcdeint.__name__, *args, **kwargs)


@filterable()
def median(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#median"""
    return filter(stream, median.__name__, *args, **kwargs)


@filterable()
def mergeplanes(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mergeplanes"""
    return filter(stream, mergeplanes.__name__, *args, **kwargs)


@filterable()
def mestimate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mestimate"""
    return filter(stream, mestimate.__name__, *args, **kwargs)


@filterable()
def midequalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#midequalizer"""
    return filter(stream, midequalizer.__name__, *args, **kwargs)


@filterable()
def minterpolate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#minterpolate"""
    return filter(stream, minterpolate.__name__, *args, **kwargs)


@filterable()
def mix(*streams: Stream, inputs: int = None, weights: str = None,
        scale: str = None, duration: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mix"""
    return filter(streams, mix.__name__, min_inputs=2, inputs=inputs, weights=weights, scale=scale, duration=duration)


@filterable()
def monochrome(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#monochrome"""
    return filter(stream, monochrome.__name__, *args, **kwargs)


@filterable()
def mpdecimate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mpdecimate"""
    return filter(stream, mpdecimate.__name__, *args, **kwargs)


@filterable()
def negate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#negate"""
    return filter(stream, negate.__name__, *args, **kwargs)


@filterable()
def nlmeans(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#nlmeans"""
    return filter(stream, nlmeans.__name__, *args, **kwargs)


@filterable()
def nnedi(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#nnedi"""
    return filter(stream, nnedi.__name__, *args, **kwargs)


@filterable()
def noformat(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#noformat"""
    return filter(stream, noformat.__name__, *args, **kwargs)


@filterable()
def noise(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#noise"""
    return filter(stream, noise.__name__, *args, **kwargs)


@filterable()
def normalize(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#normalize"""
    return filter(stream, normalize.__name__, *args, **kwargs)


@filterable()
def null(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#null"""
    return filter(stream, null.__name__, *args, **kwargs)


@filterable()
def ocr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ocr"""
    return filter(stream, ocr.__name__, *args, **kwargs)


@filterable()
def ocv(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ocv"""
    return filter(stream, ocv.__name__, *args, **kwargs)


@filterable()
def oscilloscope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#oscilloscope"""
    return filter(stream, oscilloscope.__name__, *args, **kwargs)


@filterable()
def overlay(main_node, overlay_node, x: Union[int, str] = 0, y: Union[int, str] = 0,
            eof_action: str = None, eval: str = None, shortest: bool = None,
            format: str = None, repeatlast: bool = None, alpha: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#overlay"""
    return filter([main_node, overlay_node], overlay.__name__, min_inputs=2, max_inputs=2, x=x, y=y,
                  eof_action=eof_action, eval=eval, shortest=shortest, format=format, repeatlast=repeatlast,
                  alpha=alpha)


@filterable()
def overlay_cuda(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#overlay_cuda"""
    return filter(stream, overlay_cuda.__name__, *args, **kwargs)


@filterable()
def owdenoise(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#owdenoise"""
    return filter(stream, owdenoise.__name__, *args, **kwargs)


@filterable()
def pad(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pad"""
    return filter(stream, pad.__name__, *args, **kwargs)


@filterable()
def palettegen(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#palettegen"""
    return filter(stream, palettegen.__name__, *args, **kwargs)


@filterable()
def paletteuse(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#paletteuse"""
    return filter(stream, paletteuse.__name__, *args, **kwargs)


@filterable()
def perspective(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#perspective"""
    return filter(stream, perspective.__name__, *args, **kwargs)


@filterable()
def phase(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#phase"""
    return filter(stream, phase.__name__, *args, **kwargs)


@filterable()
def photosensitivity(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#photosensitivity"""
    return filter(stream, photosensitivity.__name__, *args, **kwargs)


@filterable()
def pixdesctest(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pixdesctest"""
    return filter(stream, pixdesctest.__name__, *args, **kwargs)


@filterable()
def pixscope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pixscope"""
    return filter(stream, pixscope.__name__, *args, **kwargs)


@filterable()
def pp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pp"""
    return filter(stream, pp.__name__, *args, **kwargs)


@filterable()
def pp7(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pp7"""
    return filter(stream, pp7.__name__, *args, **kwargs)


@filterable()
def premultiply(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#premultiply"""
    return filter(stream, premultiply.__name__, *args, **kwargs)


@filterable()
def prewitt(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#prewitt"""
    return filter(stream, prewitt.__name__, *args, **kwargs)


@filterable()
def pseudocolor(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pseudocolor"""
    return filter(stream, pseudocolor.__name__, *args, **kwargs)


@filterable()
def psnr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#psnr"""
    return filter(stream, psnr.__name__, *args, **kwargs)


@filterable()
def pullup(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pullup"""
    return filter(stream, pullup.__name__, *args, **kwargs)


@filterable()
def qp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#qp"""
    return filter(stream, qp.__name__, *args, **kwargs)


@filterable()
def random(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#random"""
    return filter(stream, random.__name__, *args, **kwargs)


@filterable()
def readeia608(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#readeia608"""
    return filter(stream, readeia608.__name__, *args, **kwargs)


@filterable()
def readvitc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#readvitc"""
    return filter(stream, readvitc.__name__, *args, **kwargs)


@filterable()
def remap(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#remap"""
    return filter(stream, remap.__name__, *args, **kwargs)


@filterable()
def removegrain(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#removegrain"""
    return filter(stream, removegrain.__name__, *args, **kwargs)


@filterable()
def removelogo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#removelogo"""
    return filter(stream, removelogo.__name__, *args, **kwargs)


@filterable()
def repeatfields(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#repeatfields"""
    return filter(stream, repeatfields.__name__, *args, **kwargs)


@filterable()
def reverse(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#reverse"""
    return filter(stream, reverse.__name__, *args, **kwargs)


@filterable()
def rgbashift(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#rgbashift"""
    return filter(stream, rgbashift.__name__, *args, **kwargs)


@filterable()
def roberts(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#roberts"""
    return filter(stream, roberts.__name__, *args, **kwargs)


@filterable()
def rotate(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#rotate"""
    return filter(stream, rotate.__name__, *args, **kwargs)


@filterable()
def sab(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sab"""
    return filter(stream, sab.__name__, *args, **kwargs)


@filterable()
def scale(stream: Stream, *args, **kwargs) -> FilterableStream:
    return filter(stream, scale.__name__, *args, **kwargs)


@filterable()
def scale_npp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#scale_npp"""
    return filter(stream, scale_npp.__name__, *args, **kwargs)


@filterable()
def scale2ref(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#scale2ref"""
    return filter(stream, scale2ref.__name__, *args, **kwargs)


@filterable()
def scroll(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#scroll"""
    return filter(stream, scroll.__name__, *args, **kwargs)


@filterable()
def scdet(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#scdet"""
    return filter(stream, scdet.__name__, *args, **kwargs)


@filterable()
def selectivecolor(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#selectivecolor"""
    return filter(stream, selectivecolor.__name__, *args, **kwargs)


@filterable()
def separatefields(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#separatefields"""
    return filter(stream, separatefields.__name__, *args, **kwargs)


@filterable()
def setsar(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#setsar"""
    return filter(stream, setsar.__name__, *args, **kwargs)


@filterable()
def setfield(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#setfield"""
    return filter(stream, setfield.__name__, *args, **kwargs)


@filterable()
def setparams(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#setparams"""
    return filter(stream, setparams.__name__, *args, **kwargs)


@filterable()
def shear(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#shear"""
    return filter(stream, shear.__name__, *args, **kwargs)


@filterable()
def showinfo(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showinfo"""
    return filter(stream, showinfo.__name__, *args, **kwargs)


@filterable()
def showpalette(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showpalette"""
    return filter(stream, showpalette.__name__, *args, **kwargs)


@filterable()
def shuffleframes(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#shuffleframes"""
    return filter(stream, shuffleframes.__name__, *args, **kwargs)


@filterable()
def shufflepixels(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#shufflepixels"""
    return filter(stream, shufflepixels.__name__, *args, **kwargs)


@filterable()
def shuffleplanes(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#shuffleplanes"""
    return filter(stream, shuffleplanes.__name__, *args, **kwargs)


@filterable()
def signalstats(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#signalstats"""
    return filter(stream, signalstats.__name__, *args, **kwargs)


@filterable()
def signature(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#signature"""
    return filter(stream, signature.__name__, *args, **kwargs)


@filterable()
def smartblur(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#smartblur"""
    return filter(stream, smartblur.__name__, *args, **kwargs)


@filterable()
def sobel(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sobel"""
    return filter(stream, sobel.__name__, *args, **kwargs)


@filterable()
def spp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#spp"""
    return filter(stream, spp.__name__, *args, **kwargs)


@filterable()
def sr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sr"""
    return filter(stream, sr.__name__, *args, **kwargs)


@filterable()
def ssim(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ssim"""
    return filter(stream, ssim.__name__, *args, **kwargs)


@filterable()
def stereo3d(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#stereo3d"""
    return filter(stream, stereo3d.__name__, *args, **kwargs)


@filterable()
def astreamselect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#astreamselect"""
    return filter(stream, astreamselect.__name__, *args, **kwargs)


@filterable()
def subtitles(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#subtitles"""
    return filter(stream, subtitles.__name__, *args, **kwargs)


@filterable()
def super2xsai(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#super2xsai"""
    return filter(stream, super2xsai.__name__, *args, **kwargs)


@filterable()
def swaprect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#swaprect"""
    return filter(stream, swaprect.__name__, *args, **kwargs)


@filterable()
def swapuv(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#swapuv"""
    return filter(stream, swapuv.__name__, *args, **kwargs)


@filterable()
def tblend(stream: Stream, all_mode: str = None, all_opacity: float = None,
           all_expr: str = None, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tblend"""
    return filter(stream, tblend.__name__, all_mode=all_mode, all_opacity=all_opacity, all_expr=all_expr, **kwargs)


@filterable()
def telecine(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#telecine"""
    return filter(stream, telecine.__name__, *args, **kwargs)


@filterable()
def thistogram(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#thistogram"""
    return filter(stream, thistogram.__name__, *args, **kwargs)


@filterable()
def threshold(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#threshold"""
    return filter(stream, threshold.__name__, *args, **kwargs)


@filterable()
def thumbnail(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#thumbnail"""
    return filter(stream, thumbnail.__name__, *args, **kwargs)


@filterable()
def tile(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tile"""
    return filter(stream, tile.__name__, *args, **kwargs)


@filterable()
def tinterlace(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tinterlace"""
    return filter(stream, tinterlace.__name__, *args, **kwargs)


@filterable()
def tmedian(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tmedian"""
    return filter(stream, tmedian.__name__, *args, **kwargs)


@filterable()
def tmidequalizer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tmidequalizer"""
    return filter(stream, tmidequalizer.__name__, *args, **kwargs)


@filterable()
def tmix(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tmix"""
    return filter(stream, tmix.__name__, *args, **kwargs)


@filterable()
def tonemap(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tonemap"""
    return filter(stream, tonemap.__name__, *args, **kwargs)


@filterable()
def tpad(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tpad"""
    return filter(stream, tpad.__name__, *args, **kwargs)


@filterable()
def transpose(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#transpose"""
    return filter(stream, transpose.__name__, *args, **kwargs)


@filterable()
def transpose_npp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#transpose_npp"""
    return filter(stream, transpose_npp.__name__, *args, **kwargs)


@filterable()
def trim(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#trim"""
    return filter(stream, trim.__name__, *args, **kwargs)


@filterable()
def unpremultiply(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#unpremultiply"""
    return filter(stream, unpremultiply.__name__, *args, **kwargs)


@filterable()
def unsharp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#unsharp"""
    return filter(stream, unsharp.__name__, *args, **kwargs)


@filterable()
def untile(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#untile"""
    return filter(stream, untile.__name__, *args, **kwargs)


@filterable()
def uspp(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#uspp"""
    return filter(stream, uspp.__name__, *args, **kwargs)


@filterable()
def v360(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#v360"""
    return filter(stream, v360.__name__, *args, **kwargs)


@filterable()
def vaguedenoiser(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vaguedenoiser"""
    return filter(stream, vaguedenoiser.__name__, *args, **kwargs)


@filterable()
def vectorscope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vectorscope"""
    return filter(stream, vectorscope.__name__, *args, **kwargs)


@filterable()
def vidstabdetect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect"""
    return filter(stream, vidstabdetect.__name__, *args, **kwargs)


@filterable()
def vidstabtransform(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vidstabtransform"""
    return filter(stream, vidstabtransform.__name__, *args, **kwargs)


@filterable()
def vflip(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vflip"""
    return filter(stream, vflip.__name__, *args, **kwargs)


@filterable()
def vfrdet(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vfrdet"""
    return filter(stream, vfrdet.__name__, *args, **kwargs)


@filterable()
def vibrance(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vibrance"""
    return filter(stream, vibrance.__name__, *args, **kwargs)


@filterable()
def vif(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vif"""
    return filter(stream, vif.__name__, *args, **kwargs)


@filterable()
def vignette(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vignette"""
    return filter(stream, vignette.__name__, *args, **kwargs)


@filterable()
def vmafmotion(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vmafmotion"""
    return filter(stream, vmafmotion.__name__, *args, **kwargs)


@filterable()
def vstack(*streams: Stream, inputs: int = None,
           shortest: int = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#vstack"""
    return filter(streams, vstack.__name__, inputs=inputs or len(streams), shortest=shortest, min_inputs=2)


@filterable()
def w3fdif(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#w3fdif"""
    return filter(stream, w3fdif.__name__, *args, **kwargs)


@filterable()
def waveform(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#waveform"""
    return filter(stream, waveform.__name__, *args, **kwargs)


@filterable()
def doubleweave(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#doubleweave"""
    return filter(stream, doubleweave.__name__, *args, **kwargs)


@filterable()
def xbr(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#xbr"""
    return filter(stream, xbr.__name__, *args, **kwargs)


@filterable()
def xfade(*stream: Stream, transition: str = None, duration: float = None,
          offset: float = None, expr: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#xfade"""
    return filter(stream, xfade.__name__, max_inputs=2, transition=transition, duration=duration, offset=offset,
                  expr=expr)


@filterable()
def xmedian(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#xmedian"""
    return filter(stream, xmedian.__name__, *args, **kwargs)


@filterable()
def xstack(*streams: Stream, inputs: int = None, layout: str = None,
           shortest: int = None, fill: str = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#xstack"""
    return filter(streams, xstack.__name__, inputs=inputs or len(streams), layout=layout, shortest=shortest, fill=fill,
                  min_inputs=2)


@filterable()
def yadif(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#yadif"""
    return filter(stream, yadif.__name__, *args, **kwargs)


@filterable()
def yadif_cuda(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#yadif_cuda"""
    return filter(stream, yadif_cuda.__name__, *args, **kwargs)


@filterable()
def yaepblur(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#yaepblur"""
    return filter(stream, yaepblur.__name__, *args, **kwargs)


@filterable()
def zoompan(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#zoompan"""
    return filter(stream, zoompan.__name__, *args, **kwargs)


@filterable()
def zscale(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#zscale"""
    return filter(stream, zscale.__name__, *args, **kwargs)


"""OpenCL Video Filters

https://ffmpeg.org/ffmpeg-filters.html#OpenCL-Video-Filters
"""


@filterable()
def avgblur_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#avgblur_opencl"""
    return filter(stream, avgblur_opencl.__name__, *args, **kwargs)


@filterable()
def boxblur_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#boxblur_opencl"""
    return filter(stream, boxblur_opencl.__name__, *args, **kwargs)


@filterable()
def colorkey_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#colorkey_opencl"""
    return filter(stream, colorkey_opencl.__name__, *args, **kwargs)


@filterable()
def convolution_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#convolution_opencl"""
    return filter(stream, convolution_opencl.__name__, *args, **kwargs)


@filterable()
def erosion_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#erosion_opencl"""
    return filter(stream, erosion_opencl.__name__, *args, **kwargs)


@filterable()
def deshake_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#deshake_opencl"""
    return filter(stream, deshake_opencl.__name__, *args, **kwargs)


@filterable()
def dilation_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#dilation_opencl"""
    return filter(stream, dilation_opencl.__name__, *args, **kwargs)


@filterable()
def nlmeans_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#nlmeans_opencl"""
    return filter(stream, nlmeans_opencl.__name__, *args, **kwargs)


@filterable()
def overlay_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#overlay_opencl"""
    return filter(stream, overlay_opencl.__name__, *args, **kwargs)


@filterable()
def pad_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#pad_opencl"""
    return filter(stream, pad_opencl.__name__, *args, **kwargs)


@filterable()
def prewitt_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#prewitt_opencl"""
    return filter(stream, prewitt_opencl.__name__, *args, **kwargs)


@filterable()
def program_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#program_opencl"""
    return filter(stream, program_opencl.__name__, *args, **kwargs)


@filterable()
def roberts_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#roberts_opencl"""
    return filter(stream, roberts_opencl.__name__, *args, **kwargs)


@filterable()
def sobel_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sobel_opencl"""
    return filter(stream, sobel_opencl.__name__, *args, **kwargs)


@filterable()
def tonemap_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tonemap_opencl"""
    return filter(stream, tonemap_opencl.__name__, *args, **kwargs)


@filterable()
def unsharp_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#unsharp_opencl"""
    return filter(stream, unsharp_opencl.__name__, *args, **kwargs)


@filterable()
def xfade_opencl(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#xfade_005fopencl"""
    return filter(stream, xfade_opencl.__name__, *args, **kwargs)


"""VAAPI Video Filters

https://ffmpeg.org/ffmpeg-filters.html#VAAPI-Video-Filters
"""


@filterable()
def tonemap_vaapi(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#tonemap_vaapi"""
    return filter(stream, tonemap_vaapi.__name__, *args, **kwargs)


"""Video Sources

https://ffmpeg.org/ffmpeg-filters.html#Video-Sources
"""


@filterable()
def buffer(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#buffer"""
    return filter(stream, buffer.__name__, *args, **kwargs)


@filterable()
def cellauto(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#cellauto"""
    return filter(stream, cellauto.__name__, *args, **kwargs)


@filterable()
def coreimagesrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#coreimagesrc"""
    return filter(stream, coreimagesrc.__name__, *args, **kwargs)


@filterable()
def gradients(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#gradients"""
    return filter(stream, gradients.__name__, *args, **kwargs)


@filterable()
def mandelbrot(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mandelbrot"""
    return filter(stream, mandelbrot.__name__, *args, **kwargs)


@filterable()
def mptestsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#mptestsrc"""
    return filter(stream, mptestsrc.__name__, *args, **kwargs)


@filterable()
def frei0r_src(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#frei0r_src"""
    return filter(stream, frei0r_src.__name__, *args, **kwargs)


@filterable()
def life(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#life"""
    return filter(stream, life.__name__, *args, **kwargs)


@filterable()
def yuvtestsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#yuvtestsrc"""
    return filter(stream, yuvtestsrc.__name__, *args, **kwargs)


@filterable()
def openclsrc(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#openclsrc"""
    return filter(stream, openclsrc.__name__, *args, **kwargs)


@filterable()
def sierpinski(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#sierpinski"""
    return filter(stream, sierpinski.__name__, *args, **kwargs)


"""Video Sinks

https://ffmpeg.org/ffmpeg-filters.html#Video-Sinks
"""


@filterable()
def buffersink(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#buffersink"""
    return filter(stream, buffersink.__name__, *args, **kwargs)


@filterable()
def nullsink(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#nullsink"""
    return filter(stream, nullsink.__name__, *args, **kwargs)
