'''
Date: 2021.02.25 15:02:34
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.05.10 12:33:20
'''
from pathlib import Path

from . import constants, settings
from ._node import Stream
from ._utils import (convert_kwargs_string, drop_empty_dict_values,
                     drop_empty_list_values)
from .expression import generate_resolution
from .nodes import (FilterableStream, InputNode, MergeOutputsNode, OutputNode,
                    OutputStream, filterable)

# http://ffmpeg.org/ffmpeg-all.html


def input(source, video_device: str = None, audio_device: str = None, format: str = None,
          pixel_format=None, fps: int = None, start_position: float = None, duration: float = None,
          to_position: float = None, start_position_eof: float = None, stream_loop: int = None,
          frame_rate: int = None, width: int = None, height: int = None, vcodec: str = None,
          hwaccel: str = None, enable_cuda=True, **kwargs) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg.html#Main-options"""

    if video_device:
        kwargs['source'] = "video=" + video_device
    elif audio_device:
        kwargs['source'] = "audio=" + audio_device
    elif source is None:
        raise ValueError("Must specify an input source")

    kwargs['source'] = str(source)

    if settings.CUDA_ENABLE and enable_cuda and \
            Path(source).suffix not in constants.IMAGE_FORMATS:
        hwaccel = "cuda"
        if vcodec not in constants.CUDA_ENCODERS:
            vcodec = settings.DEFAULT_DECODER

    kwargs = drop_empty_dict_values(kwargs, hwaccel=hwaccel, vcodec=vcodec,
                                    f=format, pix_fmt=pixel_format, ss=start_position,
                                    t=duration, to=to_position, sseof=start_position_eof,
                                    stream_loop=stream_loop, r=fps, framerate=frame_rate,
                                    s=generate_resolution(width, height))

    return InputNode(args=None, kwargs=kwargs).stream()


def input_source(source: str, color: str = None, level: int = None,
                 size: str = None, rate: int = None, sar: str = None,
                 duration: float = None, decimals: bool = None) -> FilterableStream:
    """https://ffmpeg.org/ffmpeg-filters.html#Video-Sources"""
    if source not in constants.VIDEO_SOURCES:
        raise ValueError("Here is currently available video sources: %s" % constants.VIDEO_SOURCES)

    args = convert_kwargs_string(color=color, level=level, size=size, rate=rate,
                                 sar=sar, duration=duration, decimals=decimals)

    if args:
        source = f"{source}={args}"

    return input(source, format="lavfi", enable_cuda=False)


@filterable()
def output(*streams_or_source, vn=False, an=False, ar=None, ab=None, ac=None,
           acodec=None, vcodec=None, codec: str = None, aq_scale=None, vq_scale=None,
           aspect=None, fps=None, format=None, pixel_format=None, video_bitrate=None,
           audio_bitrate=None, v_profile=None, preset=None, mov_flags=None,
           shortest=False, frame_size=None, v_frames: int = None, start_position: float = None,
           duration: float = None, video_filter: str = None, audio_filter: str = None,
           ignore_output=False, preview: bool = False, enable_cuda=True,
           args: list = None, **kwargs) -> OutputStream:
    if args is None:
        args = []

    args = drop_empty_list_values(args, vn=vn, an=an, shortest=shortest)

    if ignore_output:
        kwargs['source'] = "NUL" if constants.WINDOWS else "/dev/null"
        format = "null"

    if preview:
        kwargs['source'] = "preview"
        format = "sdl"

    streams_or_source = list(streams_or_source)
    if not kwargs.get('source'):
        if not isinstance(streams_or_source[-1], (str, Path)):
            raise ValueError("Must specify an output source")
        kwargs['source'] = str(streams_or_source.pop(-1))

    streams = streams_or_source

    if settings.CUDA_ENABLE and enable_cuda and not preview and \
            Path(kwargs['source']).suffix not in constants.IMAGE_FORMATS:
        if vcodec not in constants.CUDA_ENCODERS:
            vcodec = settings.DEFAULT_ENCODER

    # codec over acodec/vcodec
    if codec is not None:
        acodec = None
        vcodec = None

    if video_bitrate is not None:
        kwargs['b:v'] = video_bitrate

    if audio_bitrate is not None:
        kwargs['b:a'] = audio_bitrate

    if v_profile is not None:
        kwargs['profile:v'] = v_profile

    kwargs = drop_empty_dict_values(kwargs, r=fps, ss=start_position, t=duration,
                                    aspect=aspect, f=format, pix_fmt=pixel_format, ar=ar,
                                    ab=ab, ac=ac, codec=codec, acodec=acodec, vcodec=vcodec,
                                    aq=aq_scale, vq=vq_scale, s=frame_size, vframes=v_frames,
                                    preset=preset, movflags=mov_flags, vf=video_filter, af=audio_filter)

    return OutputNode(streams, args=args, kwargs=kwargs).stream()


def merge_outputs(*streams: Stream) -> OutputStream:
    """Include all given outputs in one ffmpeg command line."""
    return MergeOutputsNode(streams).stream()
