'''
Date: 2021.04.29 22:31
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.04.30 09:31:00
'''
import contextlib

from .layout import generate_gird_layout

__all__ = [
    'generate_gird_layout',
    'generate_resolution',
]


def generate_resolution(width, height) -> str:
    with contextlib.suppress(Exception):
        return f"{int(width)}x{int(height)}"
