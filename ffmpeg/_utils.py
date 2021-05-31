'''
Date: 2021.02.25 14:34:07
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.05.04 23:37:10
'''
from typing import Dict, Iterable, List, Union

_backslash = '\\'
_empty_symbols = (None, '', [], {})  # exclude 0
_filter_symbols = {"-filter_complex", "-vf", "-af", "-lavfi"}


def drop_empty_dict_values(already: Dict, **kwargs) -> Dict:
    overlay = {k: v for k, v in kwargs.items() if v not in _empty_symbols}
    return {**already, **overlay}


def drop_empty_list_values(already: list, **kwargs) -> list:
    already = list(already)
    for k, v in kwargs.items():
        if v:
            already.append(f'-{k}')
    return already


def convert_kwargs_string(**kwargs):
    return ':'.join([f'{k}={v}' for k, v in kwargs.items() if v not in _empty_symbols])


def escape(text: str, chars: str) -> str:
    """Helper function to escape uncomfortable characters."""
    text = str(text)
    chars = list(set(chars))

    if _backslash in chars:
        chars.remove(_backslash)
        chars.insert(0, _backslash)

    for char in chars:
        text = text.replace(char, _backslash + char)

    return text


def convert_kwargs_to_cmd_line_args(kwargs: Dict, sort=True) -> List[str]:
    """Helper function to build command line arguments out of dict."""
    args = []
    keys = sorted(kwargs.keys()) if sort else kwargs.keys()

    for key in keys:
        v = kwargs[key]

        # list, tuple, map
        if isinstance(v, Iterable) and not isinstance(v, str):
            for value in v:
                args.append(f'-{key}')
                if value not in _empty_symbols:
                    args.append(f'{value}')
            continue

        args.append(f'-{key}')

        if v not in _empty_symbols:
            args.append(f'{v}')

    return args


def join_cmd_args_seq(args: List[str]) -> str:
    cmd_args_seq = list(args)

    for i in range(len(cmd_args_seq)):
        if cmd_args_seq[i] in _filter_symbols:
            cmd_args_seq[i + 1] = f'"{cmd_args_seq[i + 1]}"'
        elif ' ' in cmd_args_seq[i]:
            cmd_args_seq[i] = f'"{cmd_args_seq[i]}"'

    return " ".join(cmd_args_seq)


def string_to_seconds(clock: str) -> int:
    if isinstance(clock, (int, float)):
        return clock

    clock = [int(c) for c in clock.split(":")]
    if len(clock) == 0:
        hours, minutes, seconds = 0, 0, 0
    elif len(clock) == 1:
        hours, minutes, seconds = 0, 0, clock[0]
    elif len(clock) == 2:
        hours, minutes, seconds = 0, clock[0], clock[1]
    else:
        hours, minutes, seconds = clock[0], clock[1], clock[2]

    return hours * 60 * 60 + minutes * 60 + seconds


def seconds_to_string(seconds: Union[float, int, str]) -> str:
    if isinstance(seconds, str):
        return seconds

    hours = seconds // (60 * 60)
    minutes = seconds % (60 * 60) // 60
    seconds -= hours * 60 * 60 + minutes * 60
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.03f}"


if __name__ == "__main__":
    assert escape('a:b', ':') == 'a\:b'
    assert escape('a\\:b', ':\\') == 'a\\\\\\:b'
    assert (escape('a:b,c[d]e%{}f\'g\'h\\i', '\\\':,[]%') == 'a\\:b\\,c\\[d\\]e\\%{}f\\\'g\\\'h\\\\i')
    assert escape(123, ':\\') == '123'

    assert seconds_to_string(345.4246) == '00:05:45.425'
