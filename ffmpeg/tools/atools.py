'''
Date: 2021.02-28 19:35:09
LastEditors: Rustle Karl
LastEditTime: 2021.05.24 07:33:35
'''
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Union

from .._ffmpeg import input
from ..constants import PCM_S16LE, S16LE

__all__ = [
    "convert_audio_to_raw_pcm",
    "detect_silence",
]


def convert_audio_to_raw_pcm(src: Union[str, Path], dst: Union[str, Path] = None) -> bytes:
    raw, _ = input(src, enable_cuda=False). \
        output(dst or "-", format=S16LE, acodec=PCM_S16LE,
               ac=1, ar="16k", enable_cuda=False). \
        run(capture_stdout=dst is None)

    return raw


def detect_silence(src, *, noise=-60, duration=2) -> List[Tuple[float, float]]:
    """Detect silence in an audio stream.

    This filter logs a message when it detects that the input audio volume is less or
    equal to a noise tolerance value for a duration greater or equal to the minimum
    detected noise duration.

    Args:
        noise, n: Set noise tolerance. Can be specified in dB (in case "dB" is appended to the
        specified value) or amplitude ratio. Default is -60dB, or 0.001.
        duration, d: Set silence duration until notification (default is 2 seconds).
    """
    silence_start = re.compile(r'silence_start: ([0-9]+\.?[0-9]*)')
    silence_end = re.compile(r'silence_end: ([0-9]+\.?[0-9]*)')

    args = input(src).silencedetect(noise, duration).output("-", format="null").compile()
    process = subprocess.Popen(args, stderr=subprocess.PIPE)

    info = process.communicate()[1].decode("utf-8")
    if process.returncode != 0:
        sys.stderr.write(info)
        return []

    return list(zip(map(float, silence_start.findall(info)), map(float, silence_end.findall(info))))
