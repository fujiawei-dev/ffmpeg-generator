'''
Date: 2021.03.06 23:06:21
LastEditors: Rustle Karl
LastEditTime: 2021.06.25 09:45:47
'''
import subprocess
from pathlib import Path

from pkgs import color

from ._utils import convert_kwargs_to_cmd_line_args, join_cmd_args_seq

__all__ = [
    "ffplay_audio",
    "ffplay_video",
    "run_ffplay",
]


def run_ffplay(source: str = None, print_cmd=True, **kwargs):
    """Run raw ffplay command."""
    args = ["ffplay", "-hide_banner"]

    _kwargs = {}
    for k, v in kwargs.items():
        if v is True:
            args.append(f"-{k}")
        elif v:
            _kwargs[k] = v

    args.extend(convert_kwargs_to_cmd_line_args(_kwargs, sort=False))

    if source is not None:
        args.append(Path(source).as_posix())

    if print_cmd:
        color.greenln(join_cmd_args_seq(args))

    return subprocess.Popen(args)


def ffplay_audio(source: str, f: str = None, channels: int = None, ar: int = None,
                 ss: float = None, t: float = None, loop: int = None, vf: str = None):
    """
    Examples:
        ffplay song.pcm -f s16le -channels 2 -ar 4
    '"""
    run_ffplay(source, f=f, channels=channels, ar=ar, ss=ss, t=t, loop=loop, vf=vf)


def ffplay_video(source: str, x: int = None, y: int = None, video_size: str = None,
                 pixel_format: str = None, fs: bool = False, an: bool = False,
                 vn: bool = False, sn: bool = False, f: str = None, s: str = None,
                 sync: str = None, ss: float = None, t: float = None, vf: str = None,
                 af: str = None, seek_interval: int = None, window_title=None,
                 show_mode=None, loop: int = None):
    """
    Examples:
        ffplay -f rawvideo -pixel_format yuv420p -s 480*480 texture.yuv
        ffplay -f rawvideo -pixel_format rgb24 -s 480*480 texture.rgb

        ffplay video.mp4 -sync audio
        ffplay video.mp4 -sync video
        ffplay video.mp4 -sync ext
    '"""
    run_ffplay(source, x=x, y=y, video_size=video_size, pixel_format=pixel_format,
               fs=fs, an=an, vn=vn, sn=sn, f=f, s=s, sync=sync, ss=ss, t=t, vf=vf,
               af=af, seek_interval=seek_interval, window_title=window_title,
               showmode=show_mode, loop=loop)
