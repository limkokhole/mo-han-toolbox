#!/usr/bin/env python3
# encoding=utf8
import re

ILLEGAL_FS_CHARS = r'/'
ILLEGAL_FS_CHARS_LEN = len(ILLEGAL_FS_CHARS)
ILLEGAL_FS_CHARS_REGEX_PATTERN = re.compile(ILLEGAL_FS_CHARS)
ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE = r'⧸'
ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE_TABLE = str.maketrans(ILLEGAL_FS_CHARS, ILLEGAL_FS_CHARS_SUBSTITUTES_UNICODE)


class Clipboard:
    import pyperclip as _cb

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def set(self, data):
        self._cb.copy(data)

    def get(self):
        return self._cb.paste()


clipboard = Clipboard()
