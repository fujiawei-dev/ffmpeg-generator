'''
Date: 2021.02-25 14:34:07
LastEditors: Rustle Karl
LastEditTime: 2021.06.18 17:21:29
'''
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Union

from ._utils import convert_kwargs_to_cmd_line_args, drop_empty_list_values
from .constants import JSON_FORMAT
from .nodes import FFmpegError

__all__ = [
    'FFprobe',
    'metadata',
    'run_ffprobe',
]


def run_ffprobe(source, *args: List, **kwargs: Dict):
    '''https://ffmpeg.org/ffprobe-all.html'''
    args = ['ffprobe', '-hide_banner'] + list(args) + convert_kwargs_to_cmd_line_args(kwargs) + [source]

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise FFmpegError('ffprobe', stdout, stderr)

    if kwargs.get('print_format') == JSON_FORMAT:
        return json.loads(stdout)

    return stderr


def metadata(filepath, show_format=False, show_streams=False, show_frames=False,
             show_packets=False, show_programs=False, print_format=None,
             timeout: float = None, **kwargs) -> Union[dict, str]:
    if timeout:
        kwargs['timeout'] = timeout * 1000 * 1000  # s

    if print_format == JSON_FORMAT:
        kwargs['print_format'] = JSON_FORMAT
        show_streams = True

    args = drop_empty_list_values([], show_format=show_format,
                                  show_streams=show_streams, show_frames=show_frames,
                                  show_packets=show_packets, show_programs=show_programs)

    return run_ffprobe(filepath, *args, **kwargs)


class FFprobe(object):

    def __init__(self, source: Union[str, Path], show_format=False,
                 show_streams=True, show_frames=False, show_packets=False,
                 show_programs=False, print_format='json', timeout: float = None, **kwargs):
        self._source = source
        self._metadata = metadata(source, show_format=show_format,
                                  show_streams=show_streams, show_frames=show_frames,
                                  show_packets=show_packets, show_programs=show_programs,
                                  print_format=print_format, timeout=timeout, **kwargs)
        self._streams = self._metadata.get('streams', [])

        if len(self._streams) == 0:
            raise ValueError('This media file does not contain any streams.')

        for stream in self._streams:
            codec_type = stream.get('codec_type')
            if codec_type == 'video':
                self.__video = stream
            elif codec_type == 'audio':
                self.__audio = stream

    @property
    def source(self):
        return self._source

    @property
    def metadata(self):
        return self._metadata

    @property
    def streams(self):
        return self._streams

    @property
    def video(self):
        return self.__video or {}

    @property
    def video_duration(self) -> float:
        return float(self.video.get('duration')) or 0

    @property
    def video_scale(self) -> List[int]:
        return self.video.get('width') or 0, self.video.get('height') or 0

    @property
    def video_frame_rate(self) -> float:
        return eval(self.video.get('r_frame_rate', 30))

    @property
    def video_total_frames(self) -> int:
        '''video_total_frames is the number of frames as indicated
        in the file metadata - this may not always be accurate.'''
        return int(self.video.get('nb_frames')) or \
               int(self.video.get('nb_read_frames')) or \
               int(self.video_frame_rate * self.video_duration) or 0

    @property
    def video_tags(self) -> dict:
        return self.video.get('tags', {})

    @property
    def video_codec(self) -> str:
        return self.video_tags.get('ENCODER') or \
               self.video.get('codec_long_name') or \
               self.video.get('codec_name')

    @property
    def audio(self):
        return self.__audio or {}

    @property
    def audio_duration(self) -> float:
        return float(self.audio.get('duration')) or 0

    def __str__(self):
        return '<FFprobe(%s)>' % self.source

    def __dict__(self):
        return self.metadata
