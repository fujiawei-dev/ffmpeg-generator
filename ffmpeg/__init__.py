'''
Date: 2021.02.25 14:34:07
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.25 09:25:13
'''
import subprocess

from pkgs import color

from ._ffmpeg import input, input_source, merge_outputs, output
from ._ffplay import ffplay_audio, ffplay_video, run_ffplay
from ._ffprobe import FFprobe, metadata, run_ffprobe
from ._utils import convert_kwargs_to_cmd_line_args
from .filters import afilters, avfilters, vfilters
from .nodes import FFmpegError
from .tools import atools, avtools, vtools

__all__ = [
    'FFmpeg',
    'FFmpegError',
    'FFprobe',
    'afilters',
    'atools',
    'avfilters',
    'avtools',
    'constants',
    'ffplay_audio',
    'ffplay_video',
    'input',
    'input_source',
    'merge_outputs',
    'metadata',
    'output',
    'run_ffmpeg',
    'run_ffplay',
    'run_ffprobe',
    'vfilters',
    'vtools',
]


def run_ffmpeg(option: str = None, stdout=None, check=True, **kwargs) -> subprocess.CompletedProcess:
    '''Run raw ffmpeg command.'''
    args = ['ffmpeg', '-hide_banner']

    if option:
        args.append(f'-{option}')

    args.extend(convert_kwargs_to_cmd_line_args(kwargs))

    return subprocess.run(args, stdout=stdout, encoding='utf-8', check=check)


def _findstr(option, str_: str = None):
    stdout = run_ffmpeg(option, stdout=subprocess.PIPE).stdout

    if str_ is None:
        print(stdout)
    else:
        print('\n'.join([line.replace(str_, color.sredf(str_))
                         for line in stdout.splitlines() if str_ in line]))


class FFmpeg(object):

    @staticmethod
    def cuda():
        FFmpeg.hwaccels()

        color.cyanln('Cuda Encoders:')
        FFmpeg.codecs(findstr='_nvenc')

        color.cyanln('Cuda Decoders:')
        FFmpeg.codecs(findstr='_cuvid')

    @staticmethod
    def version():
        run_ffmpeg('version')

    @staticmethod
    def formats(findstr: str = None):
        _findstr('formats', str_=findstr)

    @staticmethod
    def devices(findstr: str = None):
        _findstr('devices', str_=findstr)

    @staticmethod
    def codecs(findstr: str = None):
        '''
        Examples:
            FFmpeg.codecs(find='_cuvid')
            FFmpeg.codecs(find='_nvenc')
        '''
        _findstr('codecs', str_=findstr)

    @staticmethod
    def decoders(findstr: str = None):
        _findstr('decoders', str_=findstr)

    @staticmethod
    def encoders(findstr: str = None):
        _findstr('encoders', str_=findstr)

    @staticmethod
    def bsfs():
        run_ffmpeg('bsfs')

    @staticmethod
    def protocols(findstr: str = None):
        _findstr('protocols', str_=findstr)

    @staticmethod
    def filters(findstr: str = None):
        _findstr('filters', str_=findstr)

    @staticmethod
    def pix_fmts(findstr: str = None):
        _findstr('pix_fmts', str_=findstr)

    @staticmethod
    def layouts(findstr: str = None):
        _findstr('layouts', str_=findstr)

    @staticmethod
    def colors(findstr: str = None):
        _findstr('colors', str_=findstr)

    @staticmethod
    def hwaccels():
        run_ffmpeg('hwaccels')

    @staticmethod
    def help(filter: str):
        run_ffmpeg(help='filter=' + filter)

    @staticmethod
    def list_devices(f='dshow', i='dummy'):
        run_ffmpeg(check=False, list_devices=True, f=f, i=i)

    @staticmethod
    def list_options(f='dshow', i='dummy'):
        '''
        Examples:
            ffmpeg -list_options true -f dshow -i video='USB2.0 PC CAMERA'
            ffmpeg -list_options true -f dshow -i audio='麦克风 (2- USB2.0 MIC)'
        '''
        run_ffmpeg(check=False, list_options=True, f=f, i=i)
