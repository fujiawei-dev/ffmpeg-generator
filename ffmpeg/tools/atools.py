'''
Date: 2021.02-28 19:35:09
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 10:23:18
'''
import re
import subprocess
import sys
from typing import List

from .._ffmpeg import input
from ..constants import PCM_S16LE, S16LE

__all__ = [
    "convert_audio_to_raw_pcm",
    "detect_silence",
]


def convert_audio_to_raw_pcm(src) -> bytes:
    raw, _ = input(src).output("-", format=S16LE, acodec=PCM_S16LE,
                               ac=1, ar="16k").run(capture_stdout=True)
    return raw


def detect_silence(src, *, noise=-60, duration=2) -> List[List[float]]:
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
        return

    return list(zip(map(float, silence_start.findall(info)), map(float, silence_end.findall(info))))
