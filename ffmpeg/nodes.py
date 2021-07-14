'''
Date: 2021.02.27 09:29:10
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.05.04 23:35:59
'''
from __future__ import annotations

import copy
import os
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path
from time import perf_counter
from typing import Dict, List, Tuple, Union

from pkgs import color

from ._dag import DagEdge, DagNode, topological_sort
from ._node import (Node, NodeTypes, Stream, format_input_stream_tag,
                    get_filters_spec, get_stream_spec_nodes, streamable)
from ._utils import convert_kwargs_to_cmd_line_args, escape, join_cmd_args_seq

__all__ = [
    'FFmpegError',
    'FilterableStream',
    'FilterNode',
    'GlobalNode',
    'InputNode',
    'MergeOutputsNode',
    'OutputNode',
    'OutputStream',
    'Stream',
    'filterable',
]


def filterable():
    return streamable(FilterableStream)


class FFmpegError(Exception):

    def __init__(self, executable, stdout, stderr):
        msg = [executable]

        if stdout:
            msg.append(stdout.decode('utf-8'))

        if stderr:
            msg.append(stderr.decode('utf-8'))

        super(FFmpegError, self).__init__(' '.join(msg))


class OutputStream(Stream):
    def __init__(self, upstream_node: Node, upstream_label: str, selector=None):
        super().__init__(upstream_node=upstream_node, upstream_label=upstream_label,
                         node_types=(OutputNode, GlobalNode, MergeOutputsNode), selector=selector)

    def with_global_args(self, *args: str) -> OutputStream:
        return GlobalNode(self, args=args).stream()

    def merge_outputs(self, *streams: Stream) -> OutputStream:
        """Add extra global command-line argument(s), e.g. ``-progress``."""
        return MergeOutputsNode([self, *streams]).stream()

    def get_output_args(self, overwrite=True, progress='') -> List[str]:
        nodes = get_stream_spec_nodes(self)
        sorted_nodes, outgoing_edge_graphs = topological_sort(nodes)

        type_nodes = defaultdict(list)
        for node in sorted_nodes:
            type_nodes[node.Type].append(node)

        stream_tag_graph = {(node, None): str(index)
                            for index, node in enumerate(type_nodes[NodeTypes.Input])}

        args = []
        for node in type_nodes[NodeTypes.Input]:
            args.extend(node.get_input_args())

        filters_spec = get_filters_spec(type_nodes[NodeTypes.Filter],
                                        stream_tag_graph, outgoing_edge_graphs)
        if filters_spec:
            args.extend(['-filter_complex', filters_spec])

        for node in type_nodes[NodeTypes.Output]:
            args.extend(node.get_output_args(stream_tag_graph))

        for node in type_nodes[NodeTypes.Global]:
            args.extend(node.get_global_args())

        if progress:
            args.extend(['-progress', 'unix://' + progress.replace('unix://', '', 1)])

        if overwrite:
            args.append('-y')

        args.append('-hide_banner')

        return args

    def compile(self, *, executable="ffmpeg", print_cmd=True, join_args=False,
                overwrite=True, progress='') -> Union[str, List[str]]:
        '''Build command-line for invoking ffmpeg.'''
        cmd_args_seq = [executable] + self.get_output_args(overwrite, progress)
        command = join_cmd_args_seq(cmd_args_seq)

        if print_cmd:
            color.greenln(command)

        if join_args:
            return command

        return cmd_args_seq

    def run_async(self, *, executable="ffmpeg", print_cmd=True, join_args=False,
                  pipe_stdin=False, pipe_stdout=True, pipe_stderr=True, quiet=False,
                  overwrite=True, progress='') -> subprocess.Popen:
        '''Asynchronously invoke ffmpeg for the supplied node graph.'''
        if shutil.which(executable) is None:
            raise FileNotFoundError(f"Can't find {executable} in $PATH or "
                                    f"current directory. Please specify a absolute path or "
                                    f"add {executable} into $PATH.")

        cmd_args_seq = self.compile(
                executable=executable,
                print_cmd=print_cmd,
                join_args=join_args,
                overwrite=overwrite,
                progress=progress,
        )

        stdin_stream = subprocess.PIPE if pipe_stdin else None
        stdout_stream = subprocess.PIPE if pipe_stdout else None
        stderr_stream = subprocess.PIPE if pipe_stderr else None

        return subprocess.Popen(
                cmd_args_seq,
                stdin=stdin_stream,
                stdout=stdout_stream if not quiet else subprocess.DEVNULL,
                stderr=stderr_stream if not quiet else subprocess.STDOUT,
        )

    def run(self, executable="ffmpeg", print_cmd=True, quiet=False,
            capture_stdout=True, capture_stderr=True, pipe_stdin=None,
            overwrite=True, progress='') -> Union[str, List[str]]:
        '''Invoke ffmpeg for the supplied node graph.'''
        start = perf_counter()
        process = self.run_async(
                executable=executable,
                print_cmd=print_cmd,
                quiet=quiet,
                pipe_stdin=pipe_stdin is not None,
                pipe_stdout=capture_stdout,
                pipe_stderr=capture_stderr,
                overwrite=overwrite,
                progress=progress,
        )

        stdout, stderr = process.communicate(pipe_stdin)
        if process.poll():
            raise FFmpegError('ffmpeg', stdout, stderr)

        end = perf_counter()
        if not progress:
            color.redln("[%2.4fs]\n" % (end - start))

        return stdout, stderr


class FilterableStream(Stream):

    def __init__(self, upstream_node: Node, upstream_label: str, selector=None):
        super().__init__(
                upstream_node=upstream_node,
                upstream_label=upstream_label,
                node_types=(InputNode, FilterNode),
                selector=selector,
        )

    def output(self, *streams_or_source, vn=False, an=False, ar=None, ab=None, ac=None,
               acodec=None, vcodec=None, codec: str = None, aq_scale=None, vq_scale=None,
               aspect=None, fps=None, format=None, pixel_format=None, video_bitrate=None,
               audio_bitrate=None, v_profile=None, preset=None, mov_flags=None,
               shortest=False, frame_size=None, v_frames: int = None, duration: Union[float, int, str] = None,
               start_position: Union[float, int, str] = None, video_filter: str = None,
               audio_filter: str = None, ignore_output=False, preview: bool = False,
               enable_cuda=True, args: list = None, **kwargs) -> OutputStream:
        raise NotImplementedError

    def filter(self, *args, **kwargs) -> FilterableStream:
        raise NotImplementedError

    # Custom Filters
    def gltransition(self, source: Union[str, Path] = None, offset: float = 1,
                     duration: float = 1) -> FilterableStream:
        raise NotImplementedError

    # Audio Filters
    def acompressor(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acompressor"""
        raise NotImplementedError

    def acontrast(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acontrast"""
        raise NotImplementedError

    def acopy(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acopy"""
        raise NotImplementedError

    def acrossfade(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acrossfade"""
        raise NotImplementedError

    def acrossover(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acrossover"""
        raise NotImplementedError

    def acrusher(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acrusher"""
        raise NotImplementedError

    def acue(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#acue"""
        raise NotImplementedError

    def adeclick(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#adeclick"""
        raise NotImplementedError

    def adeclip(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#adeclip"""
        raise NotImplementedError

    def adelay(self, delays: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#adelay"""
        raise NotImplementedError

    def adenorm(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#adenorm"""
        raise NotImplementedError

    def aintegral(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aintegral"""
        raise NotImplementedError

    def aecho(self, in_gain: int = 0.6, out_gain: int = 0.3, delays: str = "1000|1800",
              decays: str = "0.3|0.25") -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aecho"""
        raise NotImplementedError

    def aemphasis(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aemphasis"""
        raise NotImplementedError

    def aeval(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aeval"""
        raise NotImplementedError

    def aexciter(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aexciter"""
        raise NotImplementedError

    def afade(self, fadein: bool = False, fadeout: bool = False,
              start_sample: int = None, nb_samples: int = None,
              start_time: int = None, duration: int = None,
              curve: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afade"""
        raise NotImplementedError

    def afftdn(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afftdn"""
        raise NotImplementedError

    def afftfilt(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afftfilt"""
        raise NotImplementedError

    def afir(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afir"""
        raise NotImplementedError

    def aformat(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aformat"""
        raise NotImplementedError

    def afreqshift(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afreqshift"""
        raise NotImplementedError

    def agate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#agate"""
        raise NotImplementedError

    def aiir(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aiir"""
        raise NotImplementedError

    def alimiter(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#alimiter"""
        raise NotImplementedError

    def allpass(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#allpass"""
        raise NotImplementedError

    def aloop(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aloop"""
        raise NotImplementedError

    def amerge(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#amerge"""
        raise NotImplementedError

    def amix(self, inputs: int = None, duration: str = None,
             dropout_transition: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#amix"""
        raise NotImplementedError

    def amultiply(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#amultiply"""
        raise NotImplementedError

    def anequalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anequalizer"""
        raise NotImplementedError

    def anlmdn(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anlmdn"""
        raise NotImplementedError

    def anlms(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anlms"""
        raise NotImplementedError

    def anull(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anull"""
        raise NotImplementedError

    def apad(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#apad"""
        raise NotImplementedError

    def aphaser(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aphaser"""
        raise NotImplementedError

    def aphaseshift(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aphaseshift"""
        raise NotImplementedError

    def apulsator(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#apulsator"""
        raise NotImplementedError

    def aresample(self, inputs: int = None, duration: str = None,
                  dropout_transition: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aresample"""
        raise NotImplementedError

    def areverse(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#areverse"""
        raise NotImplementedError

    def arnndn(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#arnndn"""
        raise NotImplementedError

    def asetnsamples(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asetnsamples"""
        raise NotImplementedError

    def asetrate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asetrate"""
        raise NotImplementedError

    def ashowinfo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ashowinfo"""
        raise NotImplementedError

    def asoftclip(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asoftclip"""
        raise NotImplementedError

    def asr(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asr"""
        raise NotImplementedError

    def astats(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#astats"""
        raise NotImplementedError

    def asubboost(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asubboost"""
        raise NotImplementedError

    def asubcut(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asubcut"""
        raise NotImplementedError

    def asupercut(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asupercut"""
        raise NotImplementedError

    def asuperpass(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asuperpass"""
        raise NotImplementedError

    def asuperstop(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asuperstop"""
        raise NotImplementedError

    def atempo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#atempo"""
        raise NotImplementedError

    def atrim(self, start: float = None, end: float = None, start_pts: int = None,
              end_pts: int = None, duration: float = None, start_frame: int = None,
              end_frame: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#atrim"""
        raise NotImplementedError

    def axcorrelate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#axcorrelate"""
        raise NotImplementedError

    def bandpass(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bandpass"""
        raise NotImplementedError

    def bandreject(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bandreject"""
        raise NotImplementedError

    def lowshelf(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lowshelf"""
        raise NotImplementedError

    def biquad(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#biquad"""
        raise NotImplementedError

    def bs2b(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bs2b"""
        raise NotImplementedError

    def channelmap(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#channelmap"""
        raise NotImplementedError

    def channelsplit(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#channelsplit"""
        raise NotImplementedError

    def chorus(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#chorus"""
        raise NotImplementedError

    def compand(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#compand"""
        raise NotImplementedError

    def compensationdelay(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#compensationdelay"""
        raise NotImplementedError

    def crossfeed(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#crossfeed"""
        raise NotImplementedError

    def crystalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#crystalizer"""
        raise NotImplementedError

    def dcshift(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dcshift"""
        raise NotImplementedError

    def deesser(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deesser"""
        raise NotImplementedError

    def drmeter(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#drmeter"""
        raise NotImplementedError

    def dynaudnorm(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dynaudnorm"""
        raise NotImplementedError

    def earwax(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#earwax"""
        raise NotImplementedError

    def equalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#equalizer"""
        raise NotImplementedError

    def extrastereo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#extrastereo"""
        raise NotImplementedError

    def firequalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#firequalizer"""
        raise NotImplementedError

    def flanger(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#flanger"""
        raise NotImplementedError

    def haas(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#haas"""
        raise NotImplementedError

    def hdcd(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hdcd"""
        raise NotImplementedError

    def headphone(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#headphone"""
        raise NotImplementedError

    def highpass(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#highpass"""
        raise NotImplementedError

    def join(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#join"""
        raise NotImplementedError

    def ladspa(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ladspa"""
        raise NotImplementedError

    def loudnorm(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#loudnorm"""
        raise NotImplementedError

    def lowpass(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lowpass"""
        raise NotImplementedError

    def lv2(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lv2"""
        raise NotImplementedError

    def mcompand(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mcompand"""
        raise NotImplementedError

    def pan(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pan"""
        raise NotImplementedError

    def replaygain(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#replaygain"""
        raise NotImplementedError

    def resample(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#resample"""
        raise NotImplementedError

    def rubberband(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#rubberband"""
        raise NotImplementedError

    def sidechaincompress(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress"""
        raise NotImplementedError

    def sidechaingate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sidechaingate"""
        raise NotImplementedError

    def silencedetect(self, noise: float, duration: float) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#silencedetect"""
        raise NotImplementedError

    def silenceremove(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#silenceremove"""
        raise NotImplementedError

    def sofalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sofalizer"""
        raise NotImplementedError

    def speechnorm(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#speechnorm"""
        raise NotImplementedError

    def stereotools(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#stereotools"""
        raise NotImplementedError

    def stereowiden(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#stereowiden"""
        raise NotImplementedError

    def superequalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#superequalizer"""
        raise NotImplementedError

    def surround(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#surround"""
        raise NotImplementedError

    def highshelf(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#highshelf"""
        raise NotImplementedError

    def tremolo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tremolo"""
        raise NotImplementedError

    def vibrato(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vibrato"""
        raise NotImplementedError

    def volume(self, volume: Union[str, float], *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#volume"""
        raise NotImplementedError

    def volumedetect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#volumedetect"""
        raise NotImplementedError

    def abuffer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#abuffer"""
        raise NotImplementedError

    def aevalsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aevalsrc"""
        raise NotImplementedError

    def afirsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#afirsrc"""
        raise NotImplementedError

    def anullsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anullsrc"""
        raise NotImplementedError

    def flite(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#flite"""
        raise NotImplementedError

    def anoisesrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anoisesrc"""
        raise NotImplementedError

    def hilbert(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hilbert"""
        raise NotImplementedError

    def sinc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sinc"""
        raise NotImplementedError

    def sine(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sine"""
        raise NotImplementedError

    def abuffersink(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#abuffersink"""
        raise NotImplementedError

    def anullsink(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#anullsink"""
        raise NotImplementedError

    # Video Filters
    def addroi(self, x: int = None, y: int = None, w: int = None, h: int = None,
               qoffset: float = None, clear: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#addroi"""
        raise NotImplementedError

    def alphaextract(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#alphaextract"""
        raise NotImplementedError

    def alphamerge(self, *streams: Stream) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#alphamerge"""
        raise NotImplementedError

    def amplify(self, radius: int = None, factor: int = None, threshold: int = None,
                tolerance: int = None, low: int = None, high: int = None,
                planes: int = None, ) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#amplify"""
        raise NotImplementedError

    def ass(self, filename: Union[str, Path] = None, original_size: str = None,
            fontsdir: Union[str, Path] = None, alpha: int = None, charenc: str = None,
            stream_index: int = None, force_style: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ass"""
        raise NotImplementedError

    def atadenoise(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#atadenoise"""
        raise NotImplementedError

    def avgblur(self, x: int = None, y: int = None,
                planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#avgblur"""
        raise NotImplementedError

    def bbox(self, min_val: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bbox"""
        raise NotImplementedError

    def bilateral(self, s: float = None, r: float = None,
                  planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bilateral"""
        raise NotImplementedError

    def bitplanenoise(self, bitplane: int = None,
                      filter: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bitplanenoise"""
        raise NotImplementedError

    def blackdetect(self, d: float = None, pic_th: float = None,
                    pix_th: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#blackdetect"""
        raise NotImplementedError

    def blackframe(self, amount: float = None,
                   threshold: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#blackframe"""
        raise NotImplementedError

    def blend(self, all_mode: str = None, all_opacity: float = None,
              all_expr: str = None, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#blend"""
        raise NotImplementedError

    def bm3d(self, sigma: float = None, block: int = None, bstep: int = None,
             group: int = None, range: int = None, mstep: int = None, thmse: int = None,
             hdthr: int = None, estim: str = None, ref: bool = None,
             planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bm3d"""
        raise NotImplementedError

    def boxblur(self, luma_radius: int = None, luma_power: int = None,
                chroma_radius: int = None, chroma_power: int = None,
                alpha_radius: int = None, alpha_power: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#boxblur"""
        raise NotImplementedError

    def bwdif(self, mode: int = None, parity: int = None,
              deint: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#bwdif"""
        raise NotImplementedError

    def cas(self, strength: float = None, planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#cas"""
        raise NotImplementedError

    def chromahold(self, color: str = None, similarity: float = None,
                   blend: float = None, yuv: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#chromahold"""
        raise NotImplementedError

    def chromakey(self, color: str = None, similarity: float = None,
                  blend: float = None, yuv: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#chromakey"""
        raise NotImplementedError

    def chromanr(self, thres: int = None, sizew: int = None, sizeh: int = None,
                 stepw: int = None, steph: int = None, threy: int = None,
                 threu: int = None, threv: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#chromanr"""
        raise NotImplementedError

    def chromashift(self, cbh: int = None, cbv: int = None, crh: int = None,
                    crv: int = None, edge: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#chromashift"""
        raise NotImplementedError

    def ciescope(self, system: str = None, cie: str = None, gamuts: str = None,
                 size: int = None, intensity: float = None, contrast: float = None,
                 corrgamma: bool = None, showwhite: bool = None,
                 gamma: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ciescope"""
        raise NotImplementedError

    def codecview(self, mv: str = None, qp: str = None, mv_type: str = None,
                  frame_type: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#codecview"""
        raise NotImplementedError

    def colorbalance(self, rs: float = None, gs: float = None,
                     bs: float = None, rm: float = None, gm: float = None,
                     bm: float = None, rh: float = None, gh: float = None,
                     bh: float = None, pl: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorbalance"""
        raise NotImplementedError

    def colorcontrast(self, rc: float = None, gm: float = None, by: float = None,
                      rcw: float = None, gmw: float = None, byw: float = None,
                      pl: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorcontrast"""
        raise NotImplementedError

    def colorcorrect(self, rl: float = None, bl: float = None, rh: float = None,
                     bh: float = None, saturation: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorcorrect"""
        raise NotImplementedError

    def colorchannelmixer(self, rr: float = None, rg: float = None,
                          rb: float = None, ra: float = None, gr: float = None,
                          gg: float = None, gb: float = None, ga: float = None,
                          br: float = None, bg: float = None, ba: float = None,
                          ar: float = None, ag: float = None, ab: float = None,
                          aa: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer"""
        raise NotImplementedError

    def colorize(self, hue: int = None, saturation: float = None,
                 lightness: float = None, mix: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorize"""
        raise NotImplementedError

    def colorkey(self, color: str = None, similarity: float = None,
                 blend: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorkey"""
        raise NotImplementedError

    def colorhold(self, color: str = None, similarity: float = None,
                  blend: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorhold"""
        raise NotImplementedError

    def colorlevels(self, rimin: float = None, gimin: float = None,
                    bimin: float = None, aimin: float = None, rimax: float = None,
                    gimax: float = None, bimax: float = None, aimax: float = None,
                    romin: float = None, gomin: float = None, bomin: float = None,
                    aomin: float = None, romax: float = None, gomax: float = None,
                    bomax: float = None, aomax: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorlevels"""
        raise NotImplementedError

    def colormatrix(self, src: str, dst: str) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colormatrix"""
        raise NotImplementedError

    def colorspace(self, all: str = None, space: str = None, trc: str = None,
                   primaries: str = None, range: str = None, format: str = None,
                   fast: bool = None, dither: str = None, wpadapt: str = None,
                   iall: str = None, ispace: str = None, iprimaries: str = None,
                   itrc: str = None, irange: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorspace"""
        raise NotImplementedError

    def colortemperature(self, temperature: int = None, mix: float = None,
                         pl: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colortemperature"""
        raise NotImplementedError

    def convolution(self, m0: int = None, m1: int = None, m2: int = None, m3: int = None,
                    rdiv0: int = None, rdiv1: int = None, rdiv2: int = None, rdiv3: int = None,
                    bias0: int = None, bias1: int = None, bias2: int = None, bias3: int = None,
                    mode0: int = None, mode1: int = None, mode2: int = None,
                    mode3: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#convolution"""
        raise NotImplementedError

    def convolve(self, planes: int = None, impulse: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#convolve"""
        raise NotImplementedError

    def copy(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#copy"""
        raise NotImplementedError

    def coreimage(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#coreimage"""
        raise NotImplementedError

    def cover_rect(self, cover: Union[str, Path] = None,
                   mode: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#cover_rect"""
        raise NotImplementedError

    def crop(self, w: int = None, h: int = None, x: int = None, y: int = None,
             keep_aspect: bool = None, exact: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#crop"""
        raise NotImplementedError

    def cropdetect(self, limit: int = None, round: int = None,
                   reset_count: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#cropdetect"""
        raise NotImplementedError

    def cue(self, cue: int = None, preroll: int = None,
            buffer: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#cue"""
        raise NotImplementedError

    def curves(self, preset: str = None, master: str = None, red: str = None,
               green: str = None, blue: str = None, all: str = None,
               psfile: Union[str, Path] = None, plot: str = None) -> FilterableStream:
        """Apply color adjustments using curves.

        https://ffmpeg.org/ffmpeg-filters.html#curves"""
        raise NotImplementedError

    def datascope(self, size: str = None, x: int = None, y: int = None,
                  mode: str = None, axis: str = None, opacity: float = None,
                  format: str = None, components: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#datascope"""
        raise NotImplementedError

    def dblur(self, angle: int = None, radius: int = None,
              planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dblur"""
        raise NotImplementedError

    def dctdnoiz(self, sigma: float = None, overlap: int = None, expr: str = None,
                 n: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dctdnoiz"""
        raise NotImplementedError

    def deband(self, thr1: float = None, thr2: float = None, thr3: float = None,
               thr4: float = None, r: int = None, d: float = None, blur: bool = None,
               c: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deband"""
        raise NotImplementedError

    def deblock(self, filter: str = None, block: int = None, alpha: float = None,
                beta: float = None, gamma: float = None, delta: float = None,
                planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deblock"""
        raise NotImplementedError

    def decimate(self, cycle: int = None, dupthres: float = None,
                 scthresh: float = None, blockx: int = None, blocky: int = None,
                 ppsrc: int = None, chroma: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#decimate"""
        raise NotImplementedError

    def deconvolve(self, planes: int = None, impulse: str = None,
                   noise: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deconvolve"""
        raise NotImplementedError

    def dedot(self, m: str = None, lt: float = None, tl: float = None,
              tc: float = None, ct: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dedot"""
        raise NotImplementedError

    def deflate(self, threshold0: int = None, threshold1: int = None,
                threshold2: int = None, threshold3: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deflate"""
        raise NotImplementedError

    def deflicker(self, size: int = None, mode: str = None,
                  bypass: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deflicker"""
        raise NotImplementedError

    def dejudder(self, cycle: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dejudder"""
        raise NotImplementedError

    def delogo(self, x: int, y: int, w: int, h: int, band: int = None,
               show: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#delogo"""
        raise NotImplementedError

    def derain(self, filter_type: str = None, dnn_backend: str = None,
               mode: Union[str, Path] = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#derain"""
        raise NotImplementedError

    def deshake(self, x: int = None, y: int = None, w: int = None,
                h: int = None, rx: int = None, ry: int = None, edge: str = None,
                blocksize: int = None, contrast: int = None, search: str = None,
                filename: Union[str, Path] = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deshake"""
        raise NotImplementedError

    def despill(self, type: str = None, mix: str = None, expand: int = None,
                red: int = None, green: int = None, blue: int = None,
                brightness: int = None, alpha: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#despill"""
        raise NotImplementedError

    def detelecine(self, first_field: str = None, pattern: int = None,
                   start_frame: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#detelecine"""
        raise NotImplementedError

    def dilation(self, threshold0: int = None, threshold1: int = None,
                 threshold2: int = None, threshold3: int = None,
                 coordinates: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dilation"""
        raise NotImplementedError

    def displace(self, edge: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#displace"""
        raise NotImplementedError

    def dnn_processing(self, dnn_backend: str = None,
                       model: Union[str, Path] = None, input: str = None,
                       output: str = None, set_async: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dnn_processing"""
        raise NotImplementedError

    def drawbox(self, x: int = None, y: int = None, w: int = None,
                h: int = None, color: str = None, thickness: int = None,
                replace: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#drawbox"""
        raise NotImplementedError

    def drawgraph(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#drawgraph"""
        raise NotImplementedError

    def drawgrid(self, x: int = None, y: int = None, w: int = None,
                 h: int = None, color: str = None, thickness: int = None,
                 replace: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#drawgrid"""
        raise NotImplementedError

    def drawtext(self, text: str = None, x: int = 0, y: int = 0,
                 fontsize: int = 0, fontfile: Union[str, Path] = None,
                 fontcolor: str = None, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#drawtext"""
        raise NotImplementedError

    def edgedetect(self, low: float = None, high: float = None, mode: str = None,
                   planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#edgedetect"""
        raise NotImplementedError

    def elbg(self, codebook_length: int = None, nb_steps: int = None,
             seed: int = None, pal8: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#elbg"""
        raise NotImplementedError

    def entropy(self, mode: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#entropy"""
        raise NotImplementedError

    def epx(self, n: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#epx"""
        raise NotImplementedError

    def eq(self, contrast: float = None, brightness: float = None,
           saturation: float = None, gamma: float = None, gamma_r: float = None,
           gamma_g: float = None, gamma_b: float = None,
           gamma_weight: float = None, eval: str = None, ) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#eq"""
        raise NotImplementedError

    def erosion(self, threshold0: int = None, threshold1: int = None,
                threshold2: int = None, threshold3: int = None,
                coordinates: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#erosion"""
        raise NotImplementedError

    def estdif(self, mode: str = None, parity: str = None, deint: str = None,
               rslope: int = None, redge: int = None, interp: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#estdif"""
        raise NotImplementedError

    def exposure(self, exposure: float = None, black: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#exposure"""
        raise NotImplementedError

    def extractplanes(self, planes: str = None) -> List[FilterableStream]:
        """https://ffmpeg.org/ffmpeg-filters.html#extractplanes"""
        raise NotImplementedError

    def fade(self, t: str = None, start_frame: int = None, nb_frames: int = None,
             alpha: int = None, start_time: int = None, duration: int = None,
             color: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fade"""
        raise NotImplementedError

    def fftdnoiz(self, sigma: int = None, amount: int = None, block: int = None,
                 overlap: float = None, prev: int = None, next: int = None,
                 planes: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fftdnoiz"""
        raise NotImplementedError

    def fftfilt(self, dc_Y: int = None, dc_U: int = None, dc_V: int = None,
                weight_Y: str = None, weight_U: str = None, weight_V: str = None,
                eval: str = None, X: int = None, Y: int = None, W: int = None,
                H: int = None, N: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fftfilt"""
        raise NotImplementedError

    def field(self, t: Union[int, str] = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#field"""
        raise NotImplementedError

    def fieldhint(self, hint: Union[str, Path], mode: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fieldhint"""
        raise NotImplementedError

    def fieldmatch(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fieldmatch"""
        raise NotImplementedError

    def fieldorder(self, order: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fieldorder"""
        raise NotImplementedError

    def fifo(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fifo_002c-afifo"""
        raise NotImplementedError

    def afifo(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fifo_002c-afifo"""
        raise NotImplementedError

    def fillborders(self, left: int = None, right: int = None, top: int = None,
                    bottom: int = None, mode: str = None,
                    color: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fillborders"""
        raise NotImplementedError

    def find_rect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#find_rect"""
        raise NotImplementedError

    def floodfill(self, x: int = None, y: int = None, s0: str = None, s1: str = None,
                  s2: str = None, s3: str = None, d0: str = None, d1: str = None,
                  d2: str = None, d3: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#floodfill"""
        raise NotImplementedError

    def format(self, *pix_fmt: str) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#format"""
        raise NotImplementedError

    def fps(self, fps: int = None, start_time: int = None, round: str = None,
            eof_action: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fps"""
        raise NotImplementedError

    def framepack(self, *streams: Stream, format: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#framepack"""
        raise NotImplementedError

    def framerate(self, fps: int = None, interp_start: int = None, interp_end: int = None,
                  scene: int = None, flags: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#framerate"""
        raise NotImplementedError

    def framestep(self, step: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#framestep"""
        raise NotImplementedError

    def freezedetect(self, noise: Union[str, float], duration: int) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#freezedetect"""
        raise NotImplementedError

    def freezeframes(self, first: int = None, last: int = None,
                     replace: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#freezeframes"""
        raise NotImplementedError

    def frei0r(self, filter_name: str, filter_params: str) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#frei0r"""
        raise NotImplementedError

    def fspp(self, quality: int = None, qp: int = None, strength: int = None,
             use_bframe_qp: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#fspp"""
        raise NotImplementedError

    def gblur(self, sigma: float = None, steps: int = None, planes: int = None,
              sigma_v: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#gblur"""
        raise NotImplementedError

    def geq(self, lum_expr: str = None, cb_expr: str = None, cr_expr: str = None,
            alpha_expr: str = None, red_expr: str = None, green_expr: str = None,
            blue_expr: str = None, lum: str = None, cb: str = None, cr: str = None,
            r: str = None, g: str = None, b: str = None, a: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#geq"""
        raise NotImplementedError

    def gradfun(self, strength: float = None, radius: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#gradfun"""
        raise NotImplementedError

    def graphmonitor(self, size: str = None, opacity: float = None, mode: str = None,
                     flags: str = None, rate: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#graphmonitor"""
        raise NotImplementedError

    def greyedge(self, difford: float = None, minknorm: int = None,
                 sigma: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#greyedge"""
        raise NotImplementedError

    def haldclut(self, shortest: bool = None, repeatlast: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#haldclut"""
        raise NotImplementedError

    def hflip(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hflip"""
        raise NotImplementedError

    def histeq(self, strength: float = None, intensity: float = None,
               antibanding: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#histeq"""
        raise NotImplementedError

    def histogram(self, level_height: int = None, scale_height: int = None,
                  display_mode: str = None, levels_mode: str = None,
                  components: int = None, fgopacity: float = None,
                  bgopacity: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#histogram"""
        raise NotImplementedError

    def hqdn3d(self, luma_spatial: float = None, chroma_spatial: float = None,
               luma_tmp: float = None, chroma_tmp: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hqdn3d"""
        raise NotImplementedError

    def hwdownload(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hwdownload"""
        raise NotImplementedError

    def hwmap(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hwmap"""
        raise NotImplementedError

    def hwupload(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hwupload"""
        raise NotImplementedError

    def hwupload_cuda(self, device: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hwupload_cuda"""
        raise NotImplementedError

    def hqx(self, n: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hqx"""
        raise NotImplementedError

    def hstack(self, *streams: Stream, inputs: int = None,
               shortest: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hstack"""
        raise NotImplementedError

    def hue(self, h: Union[str, int] = None, s: Union[str, int] = None,
            H: Union[str, int] = None, b: Union[str, int] = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hue"""
        raise NotImplementedError

    def hysteresis(self, planes: int = None, threshold: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#hysteresis"""
        raise NotImplementedError

    def identity(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#identity"""
        raise NotImplementedError

    def idet(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#idet"""
        raise NotImplementedError

    def il(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#il"""
        raise NotImplementedError

    def inflate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#inflate"""
        raise NotImplementedError

    def interlace(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#interlace"""
        raise NotImplementedError

    def kerndeint(self, thresh: int = None, map: int = None, order: int = None,
                  sharp: int = None, twoway: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#kerndeint"""
        raise NotImplementedError

    def kirsch(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#kirsch"""
        raise NotImplementedError

    def lagfun(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lagfun"""
        raise NotImplementedError

    def lenscorrection(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lenscorrection"""
        raise NotImplementedError

    def lensfun(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lensfun"""
        raise NotImplementedError

    def libvmaf(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#libvmaf"""
        raise NotImplementedError

    def limiter(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#limiter"""
        raise NotImplementedError

    def loop(self, loop: int = None, size: int = None,
             start: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#loop"""
        raise NotImplementedError

    def lut1d(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lut1d"""
        raise NotImplementedError

    def lut3d(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lut3d"""
        raise NotImplementedError

    def lumakey(self, threshold: float = None, tolerance: float = None,
                softness: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lumakey"""
        raise NotImplementedError

    def lutyuv(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#lutyuv"""
        raise NotImplementedError

    def tlut2(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tlut2"""
        raise NotImplementedError

    def maskedclamp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskedclamp"""
        raise NotImplementedError

    def maskedmax(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskedmax"""
        raise NotImplementedError

    def maskedmerge(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskedmerge"""
        raise NotImplementedError

    def maskedmin(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskedmin"""
        raise NotImplementedError

    def maskedthreshold(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskedthreshold"""
        raise NotImplementedError

    def maskfun(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#maskfun"""
        raise NotImplementedError

    def mcdeint(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mcdeint"""
        raise NotImplementedError

    def median(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#median"""
        raise NotImplementedError

    def mergeplanes(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mergeplanes"""
        raise NotImplementedError

    def mestimate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mestimate"""
        raise NotImplementedError

    def midequalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#midequalizer"""
        raise NotImplementedError

    def minterpolate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#minterpolate"""
        raise NotImplementedError

    def mix(self, *streams: Stream, inputs: int = None, weights: str = None,
            scale: str = None, duration: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mix"""
        raise NotImplementedError

    def monochrome(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#monochrome"""
        raise NotImplementedError

    def mpdecimate(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mpdecimate"""
        raise NotImplementedError

    def negate(self, negate_alpha: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#negate"""
        raise NotImplementedError

    def nlmeans(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#nlmeans"""
        raise NotImplementedError

    def nnedi(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#nnedi"""
        raise NotImplementedError

    def noformat(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#noformat"""
        raise NotImplementedError

    def noise(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#noise"""
        raise NotImplementedError

    def normalize(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#normalize"""
        raise NotImplementedError

    def null(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#null"""
        raise NotImplementedError

    def ocr(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ocr"""
        raise NotImplementedError

    def ocv(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ocv"""
        raise NotImplementedError

    def oscilloscope(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#oscilloscope"""
        raise NotImplementedError

    def overlay(self, overlay_node: Node, x: Union[int, str] = 0, y: Union[int, str] = 0,
                eof_action: str = None, eval: str = None, shortest: bool = None,
                format: str = None, repeatlast: bool = None, alpha: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#overlay"""
        raise NotImplementedError

    def overlay_cuda(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#overlay_cuda"""
        raise NotImplementedError

    def owdenoise(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#owdenoise"""
        raise NotImplementedError

    def pad(self, w: Union[str, int] = None, h: Union[str, int] = None,
            x: Union[str, int] = None, y: Union[str, int] = None, color: str = None,
            eval: str = None, aspect: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pad"""
        raise NotImplementedError

    def palettegen(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#palettegen"""
        raise NotImplementedError

    def paletteuse(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#paletteuse"""
        raise NotImplementedError

    def perspective(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#perspective"""
        raise NotImplementedError

    def phase(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#phase"""
        raise NotImplementedError

    def photosensitivity(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#photosensitivity"""
        raise NotImplementedError

    def pixdesctest(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pixdesctest"""
        raise NotImplementedError

    def pixscope(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pixscope"""
        raise NotImplementedError

    def pp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pp"""
        raise NotImplementedError

    def pp7(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pp7"""
        raise NotImplementedError

    def premultiply(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#premultiply"""
        raise NotImplementedError

    def prewitt(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#prewitt"""
        raise NotImplementedError

    def pseudocolor(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pseudocolor"""
        raise NotImplementedError

    def psnr(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#psnr"""
        raise NotImplementedError

    def pullup(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pullup"""
        raise NotImplementedError

    def qp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#qp"""
        raise NotImplementedError

    def random(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#random"""
        raise NotImplementedError

    def readeia608(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#readeia608"""
        raise NotImplementedError

    def readvitc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#readvitc"""
        raise NotImplementedError

    def remap(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#remap"""
        raise NotImplementedError

    def removegrain(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#removegrain"""
        raise NotImplementedError

    def removelogo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#removelogo"""
        raise NotImplementedError

    def repeatfields(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#repeatfields"""
        raise NotImplementedError

    def reverse(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#reverse"""
        raise NotImplementedError

    def rgbashift(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#rgbashift"""
        raise NotImplementedError

    def roberts(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#roberts"""
        raise NotImplementedError

    def rotate(self, angle: str = None, ow: str = None, oh: str = None,
               bilinear: bool = None, fillcolor: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#rotate"""
        raise NotImplementedError

    def sab(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sab"""
        raise NotImplementedError

    def scale(self, w: int = -1, h: int = -1, eval: str = None, interl: int = None,
              flags: str = None, size: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#scale"""
        raise NotImplementedError

    def scale_npp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#scale_npp"""
        raise NotImplementedError

    def scale2ref(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#scale2ref"""
        raise NotImplementedError

    def scroll(self, h: float = None, v: float = None, hpos: float = None,
               vpos: float = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#scroll"""
        raise NotImplementedError

    def scdet(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#scdet"""
        raise NotImplementedError

    def selectivecolor(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#selectivecolor"""
        raise NotImplementedError

    def separatefields(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#separatefields"""
        raise NotImplementedError

    def setsar(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#setsar"""
        raise NotImplementedError

    def setfield(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#setfield"""
        raise NotImplementedError

    def setparams(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#setparams"""
        raise NotImplementedError

    def shear(self, shx: float = None, shy: float = None, fillcolor: str = None,
              interp: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#shear"""
        raise NotImplementedError

    def showinfo(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showinfo"""
        raise NotImplementedError

    def showpalette(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showpalette"""
        raise NotImplementedError

    def shuffleframes(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#shuffleframes"""
        raise NotImplementedError

    def shufflepixels(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#shufflepixels"""
        raise NotImplementedError

    def shuffleplanes(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#shuffleplanes"""
        raise NotImplementedError

    def signalstats(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#signalstats"""
        raise NotImplementedError

    def signature(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#signature"""
        raise NotImplementedError

    def smartblur(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#smartblur"""
        raise NotImplementedError

    def sobel(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sobel"""
        raise NotImplementedError

    def spp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#spp"""
        raise NotImplementedError

    def sr(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sr"""
        raise NotImplementedError

    def ssim(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ssim"""
        raise NotImplementedError

    def stereo3d(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#stereo3d"""
        raise NotImplementedError

    def astreamselect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#astreamselect"""
        raise NotImplementedError

    def subtitles(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#subtitles"""
        raise NotImplementedError

    def super2xsai(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#super2xsai"""
        raise NotImplementedError

    def swaprect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#swaprect"""
        raise NotImplementedError

    def swapuv(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#swapuv"""
        raise NotImplementedError

    def tblend(self, all_mode: str = None, all_opacity: float = None,
               all_expr: str = None, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tblend"""
        raise NotImplementedError

    def telecine(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#telecine"""
        raise NotImplementedError

    def thistogram(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#thistogram"""
        raise NotImplementedError

    def threshold(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#threshold"""
        raise NotImplementedError

    def thumbnail(self, n: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#thumbnail"""
        raise NotImplementedError

    def tile(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tile"""
        raise NotImplementedError

    def tinterlace(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tinterlace"""
        raise NotImplementedError

    def tmedian(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tmedian"""
        raise NotImplementedError

    def tmidequalizer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tmidequalizer"""
        raise NotImplementedError

    def tmix(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tmix"""
        raise NotImplementedError

    def tonemap(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tonemap"""
        raise NotImplementedError

    def tpad(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tpad"""
        raise NotImplementedError

    def transpose(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#transpose"""
        raise NotImplementedError

    def transpose_npp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#transpose_npp"""
        raise NotImplementedError

    def trim(self, start: float = None, end: float = None, start_pts: int = None,
             end_pts: int = None, duration: float = None, start_frame: int = None,
             end_frame: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#trim"""
        raise NotImplementedError

    def unpremultiply(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#unpremultiply"""
        raise NotImplementedError

    def unsharp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#unsharp"""
        raise NotImplementedError

    def untile(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#untile"""
        raise NotImplementedError

    def uspp(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#uspp"""
        raise NotImplementedError

    def v360(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#v360"""
        raise NotImplementedError

    def vaguedenoiser(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vaguedenoiser"""
        raise NotImplementedError

    def vectorscope(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vectorscope"""
        raise NotImplementedError

    def vidstabdetect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect"""
        raise NotImplementedError

    def vidstabtransform(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vidstabtransform"""
        raise NotImplementedError

    def vflip(self) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vflip"""
        raise NotImplementedError

    def vfrdet(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vfrdet"""
        raise NotImplementedError

    def vibrance(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vibrance"""
        raise NotImplementedError

    def vif(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vif"""
        raise NotImplementedError

    def vignette(self, angle="PI/5", *args, **kwargs) -> FilterableStream:
        """Make or reverse a natural vignetting effect.

        https://ffmpeg.org/ffmpeg-filters.html#vignette
        """
        raise NotImplementedError

    def vmafmotion(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vmafmotion"""
        raise NotImplementedError

    def vstack(self, *streams: Stream, inputs: int = None,
               shortest: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#vstack"""
        raise NotImplementedError

    def w3fdif(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#w3fdif"""
        raise NotImplementedError

    def waveform(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#waveform"""
        raise NotImplementedError

    def doubleweave(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#doubleweave"""
        raise NotImplementedError

    def xbr(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#xbr"""
        raise NotImplementedError

    def xfade(self, transition: str = None, duration: float = None,
              offset: float = None, expr: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#xfade"""
        raise NotImplementedError

    def xmedian(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#xmedian"""
        raise NotImplementedError

    def xstack(self, *streams: Stream, inputs: int = None, layout: str = None,
               shortest: int = None, fill: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#xstack"""
        raise NotImplementedError

    def yadif(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#yadif"""
        raise NotImplementedError

    def yadif_cuda(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#yadif_cuda"""
        raise NotImplementedError

    def yaepblur(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#yaepblur"""
        raise NotImplementedError

    def zoompan(self, z: int = None, zoom: int = None, x: Union[str, int] = None,
                y: Union[str, int] = None, d: int = None, s: str = None,
                fps: int = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#zoompan"""
        raise NotImplementedError

    def zscale(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#zscale"""
        raise NotImplementedError

    # OpenCL Video Filters
    def avgblur_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#avgblur_opencl"""
        raise NotImplementedError

    def boxblur_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#boxblur_opencl"""
        raise NotImplementedError

    def colorkey_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#colorkey_opencl"""
        raise NotImplementedError

    def convolution_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#convolution_opencl"""
        raise NotImplementedError

    def erosion_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#erosion_opencl"""
        raise NotImplementedError

    def deshake_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#deshake_opencl"""
        raise NotImplementedError

    def dilation_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#dilation_opencl"""
        raise NotImplementedError

    def nlmeans_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#nlmeans_opencl"""
        raise NotImplementedError

    def overlay_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#overlay_opencl"""
        raise NotImplementedError

    def pad_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#pad_opencl"""
        raise NotImplementedError

    def prewitt_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#prewitt_opencl"""
        raise NotImplementedError

    def program_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#program_opencl"""
        raise NotImplementedError

    def roberts_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#roberts_opencl"""
        raise NotImplementedError

    def sobel_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sobel_opencl"""
        raise NotImplementedError

    def tonemap_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tonemap_opencl"""
        raise NotImplementedError

    def unsharp_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#unsharp_opencl"""
        raise NotImplementedError

    def xfade_opencl(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#xfade_opencl"""
        raise NotImplementedError

    def tonemap_vaapi(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#tonemap_vaapi"""
        raise NotImplementedError

    # Video Sources
    def buffer(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#buffer"""
        raise NotImplementedError

    def cellauto(self, f: Union[str, Path] = None, p: str = None, r: int = None,
                 ratio: float = None, seed: int = None, rule: int = None, s: str = None,
                 scroll: bool = None, full: bool = None, stitch: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#cellauto"""
        raise NotImplementedError

    def coreimagesrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#coreimagesrc"""
        raise NotImplementedError

    def gradients(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#gradients"""
        raise NotImplementedError

    def mandelbrot(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mandelbrot"""
        raise NotImplementedError

    def mptestsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#mptestsrc"""
        raise NotImplementedError

    def frei0r_src(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#frei0r_src"""
        raise NotImplementedError

    def life(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#life"""
        raise NotImplementedError

    def yuvtestsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#yuvtestsrc"""
        raise NotImplementedError

    def openclsrc(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#openclsrc"""
        raise NotImplementedError

    def sierpinski(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#sierpinski"""
        raise NotImplementedError

    def buffersink(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#buffersink"""
        raise NotImplementedError

    def nullsink(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#nullsink"""
        raise NotImplementedError

    def abitscope(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#abitscope"""
        raise NotImplementedError

    def adrawgraph(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#adrawgraph"""
        raise NotImplementedError

    def agraphmonitor(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#agraphmonitor"""
        raise NotImplementedError

    def ahistogram(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ahistogram"""
        raise NotImplementedError

    def aphasemeter(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aphasemeter"""
        raise NotImplementedError

    def avectorscope(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#avectorscope"""
        raise NotImplementedError

    def abench(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#abench"""
        raise NotImplementedError

    def concat(self, *streams: Stream, n: int = None, v: int = None, a: int = None,
               unsafe: bool = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#concat"""
        raise NotImplementedError

    def ebur128(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ebur128"""
        raise NotImplementedError

    def ainterleave(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ainterleave"""
        raise NotImplementedError

    def ametadata(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#ametadata"""
        raise NotImplementedError

    def aperms(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aperms"""
        raise NotImplementedError

    def arealtime(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#arealtime"""
        raise NotImplementedError

    def aselect(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#aselect"""
        raise NotImplementedError

    def asendcmd(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asendcmd"""
        raise NotImplementedError

    def setpts(self, expr: str = "PTS-STARTPTS") -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#setpts"""
        raise NotImplementedError

    def asetpts(self, expr: str = "PTS-STARTPTS") -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asetpts"""
        raise NotImplementedError

    def setrange(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#setrange"""
        raise NotImplementedError

    def asettb(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asettb"""
        raise NotImplementedError

    def showcqt(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showcqt"""
        raise NotImplementedError

    def showfreqs(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showfreqs"""
        raise NotImplementedError

    def showspatial(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showspatial"""
        raise NotImplementedError

    def showspectrum(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showspectrum"""
        raise NotImplementedError

    def showspectrumpic(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showspectrumpic"""
        raise NotImplementedError

    def showvolume(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showvolume"""
        raise NotImplementedError

    def showwaves(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showwaves"""
        raise NotImplementedError

    def showwavespic(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#showwavespic"""
        raise NotImplementedError

    def asidedata(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asidedata"""
        raise NotImplementedError

    def spectrumsynth(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#spectrumsynth"""
        raise NotImplementedError

    def asplit(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#asplit"""
        raise NotImplementedError

    def azmq(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#azmq"""
        raise NotImplementedError

    def amovie(self, *args, **kwargs) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#amovie"""
        raise NotImplementedError

    def movie(self, filename: Union[str, Path] = None, format_name: str = None,
              seek_point: float = None, streams: str = None, stream_index: int = None,
              loop: int = None, discontinuity: str = None) -> FilterableStream:
        """https://ffmpeg.org/ffmpeg-filters.html#movie"""
        raise NotImplementedError

    # TODO
    def split(self) -> List[FilterableStream]:
        raise NotImplementedError

    def select(self, expr: str) -> FilterableStream:
        raise NotImplementedError


class InputNode(Node):

    def __init__(self, args=None, kwargs=None):
        super().__init__(NodeTypes.Input, None, {}, FilterableStream,
                         node_type=NodeTypes.Input, args=args, kwargs=kwargs)

        self._source = kwargs.get('source')
        if not self._source:
            raise ValueError(f'Unsupported: {self}')

    def get_input_args(self) -> List[str]:
        kwargs = copy.copy(self._kwargs)
        source = kwargs.pop('source')
        return convert_kwargs_to_cmd_line_args(kwargs) + ['-i', source]

    @property
    def source(self) -> str:
        return self._source

    @property
    def brief(self) -> str:
        return os.path.basename(self.source)


class OutputNode(Node):

    def __init__(self, streams: List[Stream], args=None, kwargs=None):
        super().__init__(NodeTypes.Output, streams, FilterableStream, OutputStream,
                         min_inputs=1, node_type=NodeTypes.Output,
                         args=args, kwargs=kwargs)

        self._source = kwargs.get('source')
        if not self._source:
            raise ValueError(f'Unsupported: {self}')

    def get_output_args(self, stream_tag_graph: Dict[Tuple[DagNode, str], str]) -> List[str]:
        if len(self.incoming_edges) == 0:
            raise ValueError(f'{self} has no mapped streams')

        args = copy.copy(self._args)
        kwargs = copy.copy(self._kwargs)

        source = kwargs.pop('source')

        for edge in self.incoming_edges:
            stream_tag = format_input_stream_tag(stream_tag_graph, edge, is_final=True)
            if stream_tag != '0' or len(self.incoming_edges) > 1:
                args += ['-map', stream_tag]

        return convert_kwargs_to_cmd_line_args(kwargs) + args + [source]

    @property
    def source(self) -> str:
        return self._source

    @property
    def brief(self) -> str:
        return os.path.basename(self.source)


class FilterNode(Node):

    def __init__(self, streams: List[Stream], label: str, min_inputs=1,
                 max_inputs=1, args=None, kwargs=None):
        super().__init__(label, streams, FilterableStream, FilterableStream,
                         min_inputs=min_inputs, max_inputs=max_inputs,
                         node_type=NodeTypes.Filter, args=args, kwargs=kwargs)

    def get_filter_spec(self, outgoing_edges: Tuple[DagEdge] = None) -> str:
        args = self._args or []
        kwargs = self._kwargs or {}

        if self.Label in {'split', 'asplit'} and outgoing_edges:
            args = [str(len(outgoing_edges))]
        else:
            args = [escape(x, '\\\'=:') for x in args]

        kwargs = {escape(k, '\\\'=:'): escape(v, '\\\'=:') for k, v in kwargs.items()}

        args.extend([f'{key}={kwargs[key]}' for key in sorted(kwargs)])
        if args:
            params = escape(self.Label, '\\\'=:') + '=' + ':'.join(args)
        else:
            params = escape(self.Label, '\\\'=:')

        return escape(params, '\\\'[],;')


class GlobalNode(Node):

    def __init__(self, stream: Stream, args=None, kwargs=None):
        super().__init__(stream.Label, stream, OutputStream, OutputStream,
                         min_inputs=1, max_inputs=1, node_type=NodeTypes.Global,
                         args=args, kwargs=kwargs)

    def get_global_args(self) -> List[str]:
        return list(self._args)


class MergeOutputsNode(Node):

    def __init__(self, streams: List[Stream]):
        super().__init__(None, streams, OutputStream, OutputStream,
                         min_inputs=1, node_type='merge_outputs')
