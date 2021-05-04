'''
Date: 2021.02-25 14:34:07
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 13:31:36
'''
import contextlib
from typing import List

from .._utils import drop_empty_dict_values
from ..nodes import filterable, FilterableStream, FilterNode, Stream

# https://ffmpeg.org/ffmpeg-filters.html

__all__ = [
    'concat',
    'filter',
    'filter_multi_output',
]


@filterable()
def filter_multi_output(stream_spec, label: str, *args, **kwargs) -> FilterNode:
    max_inputs, min_inputs = 1, 1

    with contextlib.suppress(KeyError):
        max_inputs = kwargs.pop("max_inputs")

    with contextlib.suppress(KeyError):
        min_inputs = kwargs.pop("min_inputs")

    return FilterNode(
            streams=stream_spec,
            label=label,
            min_inputs=min_inputs,
            max_inputs=max_inputs,
            args=args,
            kwargs=drop_empty_dict_values({}, **kwargs),
    )


@filterable()
def filter(stream, label: str, *args, **kwargs) -> FilterableStream:
    return filter_multi_output(stream, label, *args, **kwargs).stream()


"""Multimedia Filters

https://ffmpeg.org/ffmpeg-filters.html#Multimedia-Filters
"""


@filterable()
def abitscope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#abitscope"""
    return filter(stream, abitscope.__name__, *args, **kwargs)


@filterable()
def adrawgraph(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#adrawgraph"""
    return filter(stream, adrawgraph.__name__, *args, **kwargs)


@filterable()
def agraphmonitor(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#agraphmonitor"""
    return filter(stream, agraphmonitor.__name__, *args, **kwargs)


@filterable()
def ahistogram(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ahistogram"""
    return filter(stream, ahistogram.__name__, *args, **kwargs)


@filterable()
def aphasemeter(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aphasemeter"""
    return filter(stream, aphasemeter.__name__, *args, **kwargs)


@filterable()
def avectorscope(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#avectorscope"""
    return filter(stream, avectorscope.__name__, *args, **kwargs)


@filterable()
def abench(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#abench"""
    return filter(stream, abench.__name__, *args, **kwargs)


@filterable()
def concat(*streams: Stream, v: int = None, a: int = None, n: int = None,
           unsafe: bool = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#concat"""
    stream_count = 0

    if isinstance(v, int):
        stream_count += v

    if isinstance(a, int):
        stream_count += a

    if stream_count == 0:
        stream_count = 1

    if len(streams) % stream_count != 0:
        raise ValueError(f'Expected concat input streams to have length multiple '
                         f'of {stream_count} (v={v}, a={a}); got {len(streams)}')

    return filter(streams, concat.__name__, min_inputs=2, max_inputs=None, n=n or len(streams) // stream_count, v=v,
                  a=a, unsafe=unsafe)


@filterable()
def ebur128(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ebur128"""
    return filter(stream, ebur128.__name__, *args, **kwargs)


@filterable()
def ainterleave(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ainterleave"""
    return filter(stream, ainterleave.__name__, *args, **kwargs)


@filterable()
def ametadata(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#ametadata"""
    return filter(stream, ametadata.__name__, *args, **kwargs)


@filterable()
def aperms(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aperms"""
    return filter(stream, aperms.__name__, *args, **kwargs)


@filterable()
def arealtime(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#arealtime"""
    return filter(stream, arealtime.__name__, *args, **kwargs)


@filterable()
def aselect(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#aselect"""
    return filter(stream, aselect.__name__, *args, **kwargs)


@filterable()
def asendcmd(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asendcmd"""
    return filter(stream, asendcmd.__name__, *args, **kwargs)


@filterable()
def setpts(stream: Stream, expr: str = "PTS-STARTPTS") -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#setpts"""
    return filter(stream, setpts.__name__, expr)


@filterable()
def asetpts(stream: Stream, expr: str = "PTS-STARTPTS") -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asetpts"""
    return filter(stream, asetpts.__name__, expr)


@filterable()
def setrange(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#setrange"""
    return filter(stream, setrange.__name__, *args, **kwargs)


@filterable()
def asettb(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asettb"""
    return filter(stream, asettb.__name__, *args, **kwargs)


@filterable()
def select(stream: Stream, expr: str) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#select"""
    return filter(stream, select.__name__, expr)


@filterable()
def showcqt(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showcqt"""
    return filter(stream, showcqt.__name__, *args, **kwargs)


@filterable()
def showfreqs(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showfreqs"""
    return filter(stream, showfreqs.__name__, *args, **kwargs)


@filterable()
def showspatial(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showspatial"""
    return filter(stream, showspatial.__name__, *args, **kwargs)


@filterable()
def showspectrum(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showspectrum"""
    return filter(stream, showspectrum.__name__, *args, **kwargs)


@filterable()
def showspectrumpic(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showspectrumpic"""
    return filter(stream, showspectrumpic.__name__, *args, **kwargs)


@filterable()
def showvolume(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showvolume"""
    return filter(stream, showvolume.__name__, *args, **kwargs)


@filterable()
def showwaves(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showwaves"""
    return filter(stream, showwaves.__name__, *args, **kwargs)


@filterable()
def showwavespic(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#showwavespic"""
    return filter(stream, showwavespic.__name__, *args, **kwargs)


@filterable()
def sidedata(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asidedata"""
    return filter(stream, sidedata.__name__, *args, **kwargs)


@filterable()
def asidedata(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#asidedata"""
    return filter(stream, asidedata.__name__, *args, **kwargs)


@filterable()
def spectrumsynth(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#spectrumsynth"""
    return filter(stream, spectrumsynth.__name__, *args, **kwargs)


@filterable()
def split(stream: Stream) -> List[FilterableStream]:
    """https://ffmpeg.org/ffmpeg-filters.html#asplit"""
    return FilterNode(stream, split.__name__)


@filterable()
def asplit(stream: Stream) -> List[FilterableStream]:
    """https://ffmpeg.org/ffmpeg-filters.html#asplit"""
    return FilterNode(stream, asplit.__name__)


@filterable()
def zmq(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#azmq"""
    return filter(stream, zmq.__name__, *args, **kwargs)


@filterable()
def azmq(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#azmq"""
    return filter(stream, azmq.__name__, *args, **kwargs)


"""Multimedia Sources

https://ffmpeg.org/ffmpeg-filters.html#Multimedia-Sources
"""


@filterable()
def amovie(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#amovie"""
    return filter(stream, amovie.__name__, *args, **kwargs)


@filterable()
def movie(stream: Stream, *args, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#movie"""
    return filter(stream, movie.__name__, *args, **kwargs)
