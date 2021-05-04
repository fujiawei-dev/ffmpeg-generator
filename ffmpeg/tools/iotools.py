'''
Date: 2021.03.06 17:33:38
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 10:24:34
'''
import signal
from pathlib import Path
from typing import Union

import psutil

from .._ffmpeg import input
from ..constants import LINUX, WINDOWS


def record_screen_windows(dst: Union[str, Path], *, area="desktop", duration=None,
                          frame_rate=30, offset_x=0, offset_y=0, video_size="vga",
                          output_vcodec="libx264", output_acodec="libfaac",
                          output_format="flv", run=True, **output_kwargs):
    """https://ffmpeg.org/ffmpeg-all.html#gdigrab"""
    command = input(area, format="gdigrab", frame_rate=frame_rate, offset_x=offset_x,
                    offset_y=offset_y, video_size=video_size, duration=duration). \
        output(dst, vcodec=output_vcodec, acodec=output_acodec,
               format=output_format, **output_kwargs)
    if run:
        command.run(capture_stdout=False, capture_stderr=False)
    else:
        return command


class ScreenRecorder(object):

    def __init__(self, dst: Union[str, Path], *, area="desktop",
                 frame_rate=30, offset_x=0, offset_y=0, video_size="vga",
                 duration=None, output_vcodec="libx264", output_acodec="libfaac",
                 output_format="flv", **output_kwargs):

        if WINDOWS:
            self.command = record_screen_windows(
                    dst, area=area, frame_rate=frame_rate, duration=duration,
                    offset_x=offset_x, offset_y=offset_y, video_size=video_size,
                    output_vcodec=output_vcodec, output_acodec=output_acodec,
                    output_format=output_format, run=False, **output_kwargs
            )
        elif LINUX:
            raise NotImplementedError
        else:
            raise NotImplementedError

        self.proc: psutil.Process = None
        self.paused = False

    def start(self):
        if self.proc is None:
            _proc = self.command.run_async(quiet=True)
            self.proc = psutil.Process(_proc.pid)
        elif self.paused:
            self.proc.resume()
            self.paused = False

    def pause(self):
        if self.proc is None or self.paused:
            return
        else:
            self.proc.suspend()
            self.paused = True

    def resume(self):
        self.start()

    def stop(self):
        if self.proc is None:
            return

        self.proc.send_signal(signal.CTRL_C_EVENT)
