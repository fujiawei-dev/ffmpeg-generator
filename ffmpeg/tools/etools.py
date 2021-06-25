'''
Date: 2021.06.25 8:54
Description : Additional, experimental, non-essential features
LastEditors: Rustle Karl
LastEditTime: 2021.06.25 09:24:48
'''
import contextlib
import os
import shutil
import signal
import socket
import tempfile
from pathlib import Path
from threading import Thread
from typing import Union

from .._dag import get_outgoing_edges, topological_sort
from .._ffmpeg import input
from .._node import get_stream_spec_nodes, streamable
from ..constants import LINUX, WINDOWS
from ..nodes import FilterNode, InputNode, OutputNode

try:
    import psutil
except ImportError as e:
    psutil = e

__all__ = [
    'ScreenRecorder',  # Record screen content
    'show_progress',  # Show progress bar
    'view',  # Draw a topology graph
]


# --------------------- Draw a topology graph ---------------------

@streamable()
def view(stream_spec, save_path=None, detail=False, show_labels=True, pipe=False):
    import graphviz

    if pipe and save_path is not None:
        raise ValueError("Can't specify both `source` and `pipe`")
    elif not pipe and save_path is None:
        save_path = tempfile.mktemp()

    nodes = get_stream_spec_nodes(stream_spec)
    sorted_nodes, outgoing_edge_graphs = topological_sort(nodes)
    graph = graphviz.Digraph(format='png')
    graph.attr(rankdir='LR')

    for node in sorted_nodes:
        if isinstance(node, InputNode):
            color = '#99CC00'
        elif isinstance(node, OutputNode):
            color = '#99CCFF'
        elif isinstance(node, FilterNode):
            color = '#FFCC00'
        else:
            color = None

        if detail:
            label = node.detail
        else:
            label = node.brief

        graph.node(str(hash(node)), label, shape='box', style='filled', fillcolor=color)
        outgoing_edge_graph = outgoing_edge_graphs.get(node, {})

        for edge in get_outgoing_edges(node, outgoing_edge_graph):
            kwargs = {}
            upstream_label = edge.UpstreamLabel
            downstream_label = edge.DownstreamLabel
            selector = edge.Selector
            if show_labels and (upstream_label or downstream_label or selector):
                if upstream_label is None:
                    upstream_label = ''
                if selector is not None:
                    upstream_label += ":" + selector
                if downstream_label is None:
                    downstream_label = ''
                if upstream_label != '' and downstream_label != '':
                    middle = ' {} '.format('\u2192')  # Right Arrow
                else:
                    middle = ''
                kwargs['label'] = '{}  {}  {}'.format(upstream_label, middle, downstream_label)

            upstream_node_id = str(hash(edge.UpstreamNode))
            downstream_node_id = str(hash(edge.DownstreamNode))
            graph.edge(upstream_node_id, downstream_node_id, **kwargs)

    if pipe:
        return graph.pipe()

    graph.view(save_path, cleanup=True)

    return stream_spec


# -------------------- Record screen content --------------------

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

        if isinstance(psutil, Exception):
            raise psutil

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


# ---------------------- Show progress bar ----------------------

"""
Process video and report and show progress bar.

This is an example of using the ffmpeg `-progress` option with a
unix-domain socket to report progress in the form of a progress bar.

The video processing simply consists of converting the video to
sepia colors, but the same pattern can be applied to other use cases.
"""


@contextlib.contextmanager
def open_temporary_directory() -> str:
    temporary_directory = tempfile.mkdtemp()
    try:
        yield temporary_directory
    finally:
        shutil.rmtree(temporary_directory)


def accept(s: socket.socket, handler):
    """Read progress events from a unix-domain socket."""
    conn, _ = s.accept()

    buffer = b""
    previous = 0

    while more := conn.recv(16):
        buffer += more
        lines = buffer.splitlines()

        for line in lines[:-1]:
            parts = line.decode().split("=")
            if len(parts) < 2:
                continue

            k, v = parts[:2]
            if v == "continueframe":
                k = v
                frame = int(parts[2])
                v = frame - previous
                previous = frame

            handler(k, v)

        buffer = lines[-1]

    conn.close()


@contextlib.contextmanager
def watch_progress(handler):
    """Context manager for creating a unix-domain socket and listen for
    ffmpeg progress events.

    The socket domain is yielded from the context manager and the
    socket is closed when the context manager is exited.

    Args:
        handler: a function to be called when progress events are
            received; receives a ``key`` argument and ``value`` argument.
    """
    with open_temporary_directory() as temporary_d:
        unix_sock = os.path.join(temporary_d, "sock")
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        with contextlib.closing(s):
            s.bind(unix_sock)
            s.listen(1)
            Thread(target=accept, args=(s, handler)).start()

            yield unix_sock


@contextlib.contextmanager
def show_progress(total_frames):
    """Create a unix-domain socket to watch progress and
    render tqdm progress bar."""
    from tqdm import tqdm

    if not LINUX:
        raise OSError("Only supports Linux platform")

    with tqdm(total=total_frames, desc="Processing", unit="f") as bar:

        def handler(key, value):
            if key == "continueframe":
                bar.update(value)
            elif key == "progress" and value == "end":
                bar.update(bar.total - bar.n)

        with watch_progress(handler) as unix_sock:
            yield unix_sock
