#!/usr/bin/env python3
# encoding=utf8
import inspect
import re
from time import sleep
import win32clipboard

from .tricks import singleton, with_self_context

ILLEGAL_FS_CHARS = r'\/:*?"<>|'
ILLEGAL_FS_CHARS_LEN = len(ILLEGAL_FS_CHARS)
ILLEGAL_FS_CHARS_REGEX_PATTERN = re.compile(ILLEGAL_FS_CHARS)
ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE = r'⧹⧸꞉∗？″﹤﹥￨'
ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE_TABLE = str.maketrans(ILLEGAL_FS_CHARS, ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE)


@singleton
class Clipboard:
    _wcb = win32clipboard
    cf_dict = {n.lstrip('CF_'): m for n, m in inspect.getmembers(_wcb) if n.startswith('CF_')}

    def __init__(self):
        self.delay = 0

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        sleep(self.delay)
        self._wcb.OpenClipboard()

    def close(self):
        self._wcb.CloseClipboard()
        # sleep(self.delay)  # maybe not needed

    def valid_format(self, x: str or int):
        """get valid clipboard format ('CF_*')"""
        if isinstance(x, int):
            pass
        elif isinstance(x, str):
            x = x.upper()
            if not x.startswith('x_'):
                x = 'CF_' + x
            x = getattr(self._wcb, x)
        else:
            raise TypeError("'{}' is not str or int".format(x))
        return x

    @with_self_context
    def clear(self):
        return self._wcb.EmptyClipboard()

    @with_self_context
    def set(self, data, cf=_wcb.CF_UNICODETEXT):
        cf = self.valid_format(cf)
        return self._wcb.SetClipboardData(cf, data)

    @with_self_context
    def set_text(self, text):
        return self._wcb.SetClipboardText(text)

    @with_self_context
    def get(self, cf=_wcb.CF_UNICODETEXT):
        cf = self.valid_format(cf)
        if self._wcb.IsClipboardFormatAvailable(cf):
            data = self._wcb.GetClipboardData(cf)
        else:
            data = None
        return data

    def get_path(self) -> list:
        paths = self.get(self._wcb.CF_HDROP)
        if paths:
            return list(paths)
        else:
            return []

    @with_self_context
    def get_all(self) -> dict:
        d = {}
        for k, v in self.cf_dict.items():
            if self._wcb.IsClipboardFormatAvailable(v):
                d[k] = self._wcb.GetClipboardData(v)
        return d


clipboard = Clipboard()
