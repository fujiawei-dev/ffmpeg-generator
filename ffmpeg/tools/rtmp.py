'''
Date: 2021.03.05 09:36:19
LastEditors: Rustle Karl
LastEditTime: 2021.03.05 12:26:09
'''
from pathlib import Path
from typing import Union

from .. import FFprobe
from .._ffmpeg import input


def start_one_stream_loop(src: Union[str, Path], *, loop: int = -1, codec="copy",
                          vcodec="copy", acodec="copy", format="mpegts",
                          source_url: str = "udp://localhost:10240"):
    input(src, stream_loop=loop, re=None) \
        .output(source_url, codec=codec, vcodec=vcodec,
                acodec=acodec, format=format). \
        run(capture_stdout=False, capture_stderr=False)


def detect_source_stream(source_url: str, timeout: int = 3) -> dict:
    return FFprobe(source_url, timeout=timeout).metadata
