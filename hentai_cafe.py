#!/usr/bin/env python

import sys
import zipfile
import requests
import logging

from lib_hentai import HentaiCafeKit, HentaiDownloadError
from lib_base import LOG_FMT_MESSAGE_ONLY, win32_ctrl_c

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FMT_MESSAGE_ONLY
)


if __name__ == '__main__':
    win32_ctrl_c()
    hc = HentaiCafeKit(5)
    uri = sys.argv[1]
    hc.save_entry_to_cbz(uri)
