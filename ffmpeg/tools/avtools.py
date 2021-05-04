'''
Date: 2021.02-25 20:50:07
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 10:24:18
'''
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union

from .. import constants
from .._ffmpeg import input, merge_outputs
from .._utils import seconds_to_string

__all__ = [
    "adjust_tempo",
    "concat_multiple_parts",
    "cut_into_multiple_parts",
    "merge_video_audio",
    "separate_audio_stream",
    "separate_video_stream",
]


def adjust_tempo(src: Union[str, Path], dst: Union[str, Path], *, vtempo: float = 2,
                 atempo: float = 2, acodec=None, vcodec=None, **kwargs):
    """Adjust audio and video playback speed.

    Args:
        vtempo: video current playback speed * vtempo, -1 mean no video
        atempo: audio current playback speed * atempo, -1 mean no audio
    """
    _input = input(src)

    v_input = _input.video.setpts(f"{1 / vtempo}*PTS")
    a_input = _input.audio.atempo(atempo)

    if vtempo == -1 and atempo == -1:
        raise ValueError("`vtempo` and `atempo` cannot all be -1")

    elif vtempo == -1:
        a_input.output(dst, acodec=acodec, **kwargs).run()
    elif atempo == -1:
        v_input.output(dst, vcodec=vcodec, **kwargs).run()
    else:
        v_input.output(a_input, dst, acodec=acodec, vcodec=vcodec, **kwargs).run()


def modify_metadata(src: Union[str, Path], dst: Union[str, Path], *,
                    metadata: Dict[str, Union[str, int]], specifier: Optional[str] = None):
    """Set a metadata key/value pair.

    An optional specifier may be given to set metadata on streams, chapters or programs.
    """
    if not metadata:
        raise ValueError("Provide at least one metadata %s" % metadata)

    specifier = "-metadata:" + specifier if specifier else "-metadata"

    args = []
    for k, v in metadata.items():
        args.extend([specifier, f"{k}={v}"])

    input(src).output(dst, vcodec=constants.COPY, acodec=constants.COPY, args=args).run()


def separate_video_stream(src: Union[str, Path], dst: Union[str, Path]):
    input(src).output(dst, an=True, vcodec="copy").run()


def separate_audio_stream(src: Union[str, Path], dst: Union[str, Path]):
    input(src).output(dst, vn=True, acodec="copy").run()


def convert_format(src: Union[str, Path], dst: Union[str, Path], *,
                   format=None, vcodec="copy", acodec="copy"):
    input(src).output(dst, format=format, acodec=acodec, vcodec=vcodec).run()


def cut_into_multiple_parts(src: Union[str, Path], dst: Union[str, Path],
                            *, durations: List[float], vcodec="libx264"):
    """Cut the video or audio into multiple parts.

    Example:
        avutils.cut_into_multiple_parts("video.mp4", [10, 10, 10, None])
        avutils.cut_into_multiple_parts("music.mp3", [-10, 10, -10, None])
    """
    if not isinstance(durations, (list, tuple)):
        raise ValueError

    if len(durations) < 2:
        raise ValueError(f'Expected at least 2 duration values; got {len(durations)}')

    outs = []
    raw = input(src)
    path = Path(src)
    start_position = 0

    for order, duration in enumerate(durations):
        # skip
        if duration is not None and duration < 0:
            start_position -= duration
            continue

        outs.append(raw.output(f"{dst / path.stem}_part{order}{path.suffix}",
                               acodec="copy", vcodec=vcodec,
                               start_position=seconds_to_string(start_position),
                               duration=duration))

        if duration is not None:
            start_position += duration

    merge_outputs(*outs).run()


def cut_one_part(src: Union[str, Path], dst: Union[str, Path], *, vcodec="libx264",
                 start: Union[str, int, float] = None, end: Union[str, int, float] = None,
                 duration: Union[int, float] = None, only_video=False, only_audio=False):
    '''Intercept a piece of audio or video from audio or video'''
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        end = start + duration if end == 0 or end < start else end

    av = input(src)
    a = av.audio.atrim(start=start, end=end, duration=duration)
    v = av.video.trim(start=start, end=end, duration=duration)

    if only_video:
        v.output(dst, vcodec=vcodec).run()
    elif only_audio:
        a.output(dst, vcodec=vcodec).run()
    else:
        v.output(a, dst, vcodec=vcodec).run()


def merge_video_audio(v_src: Union[str, Path], a_src: Union[str, Path],
                      dst: Union[str, Path], vcodec="copy", acodec="copy"):
    v_input = input(v_src).video
    a_input = input(a_src).audio
    v_input.output(a_input, dst, acodec=acodec, vcodec=vcodec).run()


def concat_multiple_parts(dst: Union[str, Path], *files: Union[str, Path],
                          vcodec="copy", acodec="copy"):
    concat = tempfile.mktemp()

    with open(concat, "w", encoding="utf-8") as fp:
        for file in files:
            fp.write("file '%s'\n" % Path(file).absolute().as_posix())

    # https://stackoverflow.com/questions/38996925/ffmpeg-concat-unsafe-file-name/56029574
    input(concat, format="concat", safe=0).output(dst, acodec=acodec, vcodec=vcodec).run()

    Path(concat).unlink(missing_ok=True)
