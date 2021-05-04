'''
Date: 2021.03.01 13:25:12
LastEditors: Rustle Karl
LastEditTime: 2021.03.01 19:46:40
'''
import contextlib
import os
import shutil
import socket
import tempfile
from threading import Thread

from tqdm import tqdm

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
    import sys

    if sys.platform != "linux":
        raise OSError("Only supports Linux platform")

    with tqdm(total=total_frames, desc="Processing", unit="f") as bar:

        def handler(key, value):
            if key == "continueframe":
                bar.update(value)
            elif key == "progress" and value == "end":
                bar.update(bar.total - bar.n)

        with watch_progress(handler) as unix_sock:
            yield unix_sock
