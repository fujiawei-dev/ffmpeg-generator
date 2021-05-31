'''
Date: 2021.03.01 19:46:08
LastEditors: Rustle Karl
LastEditTime: 2021.05.24 07:34:01
'''
import os
from pathlib import Path
from typing import Union

import numpy as np

from .. import vfilters
from .._ffmpeg import input
from .._ffprobe import FFprobe
from ..constants import PIPE, RAW_VIDEO, RGB24

__all__ = [
    "assemble_video_from_images",
    "compare_2_videos",
    "convert_video_to_np_array",
    "generate_video_thumbnail",
    "hstack_videos",
    "read_frame_as_jpeg",
    "side_by_side_2_videos",
    "timed_video_screenshot",
    "video_add_image_watermark",
    "video_add_text_watermark",
    "vstack_videos",
]


# TODO
def capture_x11_screen(dst: Union[str, Path], *, screen: str = None,
                       duration: int = 3, frame_rate: int = 25):
    screen = os.environ["DISPLAY"] if screen is None else screen

    input(screen, duration=duration, format="x11grab",
          video_size="cif", framerate=frame_rate).output(dst).run()


def capture_video_key_frame(src: Union[str, Path], dst: Union[str, Path]):
    if not os.path.isdir(dst):
        dst = os.path.dirname(dst)

    input(src).output(os.path.join(dst, Path(src).stem + "_key_frame_%d.png"),
                      video_filter="select='eq(pict_type,PICT_TYPE_I)'", vsync="vfr").run()


def timed_video_screenshot(src: Union[str, Path], dst: Union[str, Path], interval=3):
    os.makedirs(dst, exist_ok=True)
    input(src).output(os.path.join(dst, Path(src).stem + "_screenshot_%d.png"),
                      video_filter=f"fps=1/{interval}").run()


def flip_mirror_video(src: Union[str, Path], dst: Union[str, Path], *,
                      horizontal=True, keep_audio=True, hwaccel: str = None,
                      output_vcodec: str = None, **output_kwargs):
    input_v = input(src, hwaccel=hwaccel)

    if horizontal:
        stream = input_v.pad(w="2*iw").overlay(input_v.hflip(), x="w")
    else:
        stream = input_v.pad(h="2*ih").overlay(input_v.vflip(), y="h")

    if keep_audio:
        stream.output(input_v.audio, dst, acodec="copy",
                      vcodec=output_vcodec, **output_kwargs).run()
    else:
        stream.output(dst, vcodec=output_vcodec, **output_kwargs).run()


def compare_2_videos(v1: Union[str, Path], v2: Union[str, Path],
                     dst: Union[str, Path], horizontal=True):
    if horizontal:
        hstack_videos(dst, v1, v2)  # Fastest
        # input(v1).pad(w="2*iw").overlay(input(v2), x="w").output(dst).run()
    else:
        vstack_videos(dst, v1, v2)  # Fastest
        # side_by_side_2_videos(v1, v2, dst, False) # Fast
        # input(v1).pad(h="2*ih").overlay(input(v2), y="h").output(dst).run() # Slowest


def side_by_side_2_videos(v1: Union[str, Path], v2: Union[str, Path],
                          dst: Union[str, Path], horizontal=True):
    vfilters.framepack(input(v1), input(v2), format="sbs" if horizontal else "tab").output(dst).run()


def hstack_videos(dst: Union[str, Path], *videos: Union[str, Path]):
    vfilters.hstack(*list(map(input, videos)), inputs=len(videos), shortest=0).output(dst).run()


def vstack_videos(dst: Union[str, Path], *videos: Union[str, Path]):
    vfilters.vstack(*list(map(input, videos)), inputs=len(videos), shortest=0).output(dst).run()


def xstack_videos(*videos: Union[str, Path], dst: Union[str, Path], layout: str, fill: str = None):
    vfilters.xstack(*list(map(input, videos)), inputs=len(videos),
                    layout=layout, shortest=0, fill=fill).output(dst).run()


def concat_2_videos_with_gltransition(dst: Union[str, Path], *videos: Union[str, Path],
                                      offset: float = 0, duration: float = 0, source: Union[str, Path] = None):
    if len(videos) < 2:
        raise ValueError(f'Expected at least 2 videos; got {len(videos)}')

    in1, in2 = input(videos[0]), input(videos[1])
    vfilters.gltransition(in1, in2, offset=offset, duration=duration,
                          source=source).output(dst).run()


def concat_2_videos_with_xfade(dst: Union[str, Path], *videos: Union[str, Path],
                               transition: str = None, duration: float = None,
                               offset: float = None, expr: str = None,
                               hwaccel: str = None, output_vcodec: str = None):
    if len(videos) < 2:
        raise ValueError(f'Expected at least 2 videos; got {len(videos)}')

    in1, in2 = input(videos[0], hwaccel=hwaccel), input(videos[1], hwaccel=hwaccel)
    vfilters.xfade(in1, in2, transition=transition, duration=duration, offset=offset, expr=expr). \
        output(dst, vcodec=output_vcodec).run()


def video_add_image_watermark(v_src: Union[str, Path], i_src: Union[str, Path],
                              dst: Union[str, Path], *, w: int = 0, h: int = 0,
                              x: int = 0, y: int = 0, _eval='init', ):
    v_input = input(v_src)
    i_input = input(i_src).scale(w, h)
    v_input.overlay(i_input, x=x, y=y, eval=_eval).output(v_input.audio, dst, acodec="copy").run()


def video_add_text_watermark(v_src, dst, *, text: str, x: int = 0, y: int = 0,
                             fontsize: int = 24, fontfile: Union[str, Path] = None,
                             keep_audio=True):
    v_input = input(v_src)
    stream = v_input.drawtext(text=text, x=x, y=y, fontsize=fontsize, fontfile=fontfile)

    if keep_audio:
        stream.output(v_input.audio, dst, acodec="copy").run()
    else:
        stream.output(dst).run()


def video_add_ass_subtitle(v_src, s_src=None, dst=None, keep_audio=True):
    if not s_src:
        s_src = Path(v_src).with_suffix('.ass')
        assert s_src.exists()

    if not dst:
        path = Path(v_src)
        dst = path.with_name(path.stem + '_video_ass.mp4')

    v_input = input(v_src)
    stream = v_input.ass(filename=str(s_src))

    if keep_audio:
        stream.output(v_input.audio, dst, acodec="copy").run()
    else:
        stream.output(dst).run()


def assemble_video_from_images(glob_pattern, dst, *, pattern_type="glob", frame_rate=25):
    # https://stackoverflow.com/questions/31201164/ffmpeg-error-pattern-type-glob-was-selected-but-globbing-is-not-support-ed-by
    if pattern_type:
        input(glob_pattern, frame_rate=frame_rate, pattern_type=pattern_type).output(dst).run()
    else:
        input(glob_pattern, frame_rate=frame_rate).output(dst).run()


def convert_video_to_np_array(src, *, width=0, height=0) -> np.ndarray:
    width_, height_ = FFprobe(src).video_scale
    stdout, _ = input(src, enable_cuda=False). \
        output(PIPE, format=RAW_VIDEO, pixel_format=RGB24, enable_cuda=False).run()
    return np.frombuffer(stdout, np.uint8).reshape([-1, height or height_, width or width_, 3])


def read_frame_as_jpeg(src, frame=1) -> bytes:
    raw, _ = input(src, enable_cuda=False).select(f"gte(n, {frame})"). \
        output(PIPE, vframes=1, format='image2', vcodec='mjpeg', enable_cuda=False). \
        run(capture_stdout=True)
    return raw


def generate_video_thumbnail(src, dst, *, start_position=1, width=-1, height=-1):
    input(src, start_position=start_position).scale(width, height).output(dst, vframes=1).run()
