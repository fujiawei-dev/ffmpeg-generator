'''
Date: 2021.02-25 20:50:07
LastEditors: Rustle Karl
LastEditTime: 2021.05.04 23:34:46
'''
import tempfile
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

from .. import FFprobe, constants
from .._ffmpeg import input, merge_outputs, output
from .._utils import seconds_to_string, string_to_seconds

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
    input(src, enable_cuda=False).output(dst, an=True, enable_cuda=False, vcodec="copy").run()


def separate_audio_stream(src: Union[str, Path], dst: Union[str, Path], pcm_format=False):
    if pcm_format:
        kwargs = dict(format=constants.S16LE, acodec=constants.PCM_S16LE, ac=1, ar="16k")
    else:
        kwargs = dict(acodec=constants.COPY)

    input(src, enable_cuda=False).output(dst, vn=True, enable_cuda=False, **kwargs).run()


def convert_format(src: Union[str, Path], dst: Union[str, Path], *,
                   format=None, vcodec="copy", acodec="copy", enable_cuda=True):
    if vcodec == constants.COPY:
        enable_cuda = False

    input(src, enable_cuda=enable_cuda). \
        output(dst, format=format, acodec=acodec,
               vcodec=vcodec, enable_cuda=enable_cuda).run()


def cut_into_multiple_parts(src: Union[str, Path], dst: Union[str, Path],
                            *, durations: List[Union[float, int, str]], vcodec="libx264",
                            enable_cuda=True, overwrite=True, accumulative=False):
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
    path = Path(src)
    start_position = 0
    raw = input(src, enable_cuda=enable_cuda)

    for order, duration in enumerate(durations):
        # skip negative value
        if isinstance(duration, (int, float)) and duration < 0:
            start_position -= duration
            continue

        if isinstance(duration, str):
            duration = string_to_seconds(duration)

        if isinstance(duration, (int, float)) and accumulative:
            duration -= start_position

        outs.append(raw.output(f"{dst / path.stem}_{order}{path.suffix}",
                               acodec="copy", vcodec=vcodec, enable_cuda=enable_cuda,
                               start_position=seconds_to_string(start_position), duration=duration))

        if duration is not None:
            start_position += duration

    merge_outputs(*outs).run(overwrite=overwrite)


class TrimPair(NamedTuple):
    Start: Union[str, int, float]
    End: Union[str, int, float]
    IsDuration: bool = False


def cut_into_multiple_parts_v2(src: Union[str, Path], dst: Union[str, Path],
                               *, start_duration_pairs: List[TrimPair], vcodec="libx264",
                               enable_cuda=True, overwrite=True):
    outs = []
    path = Path(src)
    raw = input(src, enable_cuda=enable_cuda)

    for order, pair in enumerate(start_duration_pairs):
        start_position = string_to_seconds(pair.Start)
        end_position = string_to_seconds(pair.End)

        if not pair.IsDuration and end_position > start_position:
            duration = end_position - start_position
        else:
            duration = end_position

        outs.append(raw.output(f"{dst / path.stem}_{order}{path.suffix}",
                               acodec="copy", vcodec=vcodec, enable_cuda=enable_cuda,
                               start_position=start_position, duration=duration))

    merge_outputs(*outs).run(overwrite=overwrite)


def cut_one_part(src: Union[str, Path], dst: Union[str, Path], *, vcodec="libx264",
                 enable_cuda=True, overwrite=True, start: Union[str, int, float] = None,
                 end: Union[str, int, float] = None, duration: Union[int, float] = None,
                 only_video=False, only_audio=False):
    '''Intercept a piece of audio or video from audio or video.
    Slower than `cut_into_multiple_parts`.'''
    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
        end = start + duration if end == 0 or end < start else end

    av = input(src, enable_cuda=enable_cuda)
    a = av.audio.atrim(start=start, end=end, duration=duration).asetpts("PTS-STARTPTS")
    v = av.video.trim(start=start, end=end, duration=duration).setpts("PTS-STARTPTS")

    streams = [v, a]
    if only_video:
        streams = [v]
    elif only_audio:
        streams = [a]

    output(*streams, dst, vcodec=vcodec, enable_cuda=enable_cuda). \
        run(overwrite=overwrite)


def merge_video_audio(v_src: Union[str, Path], a_src: Union[str, Path],
                      dst: Union[str, Path], vcodec="copy", acodec="copy"):
    v_input = input(v_src).video
    a_input = input(a_src).audio
    v_input.output(a_input, dst, acodec=acodec, vcodec=vcodec).run()


def concat_multiple_parts(dst: Union[str, Path], *files: Union[str, Path],
                          vcodec="copy", acodec="copy"):
    '''Splicing video or audio clips.'''
    concat = tempfile.mktemp()

    with open(concat, "w", encoding="utf-8") as fp:
        for file in files:
            fp.write("file '%s'\n" % Path(file).absolute().as_posix())

    # https://stackoverflow.com/questions/38996925/ffmpeg-concat-unsafe-file-name/56029574
    input(concat, format="concat", safe=0).output(dst, acodec=acodec, vcodec=vcodec).run()

    Path(concat).unlink(missing_ok=True)


def start_one_stream_loop(src: Union[str, Path], *, loop: int = -1, codec="copy",
                          vcodec="copy", acodec="copy", format="mpegts",
                          source_url: str = "udp://localhost:10240"):
    '''Push a video stream in a loop forever.'''
    input(src, stream_loop=loop, re=None) \
        .output(source_url, codec=codec, vcodec=vcodec,
                acodec=acodec, format=format). \
        run(capture_stdout=False, capture_stderr=False)


def detect_source_stream(source_url: str, timeout: int = 3) -> dict:
    '''Detect whether is a stream source.'''
    return FFprobe(source_url, timeout=timeout).metadata
