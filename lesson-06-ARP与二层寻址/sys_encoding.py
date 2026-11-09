# -*- coding: utf-8 -*-
"""Windows 控制台子进程输出编码（与第五课 run_ping 一致）。"""

import locale
import platform


def console_encoding() -> str:
    if "windows" in platform.system().lower():
        for name in ("gbk", locale.getpreferredencoding(False) or "", "cp936", "mbcs"):
            if name:
                return name
        return "gbk"
    return "utf-8"
