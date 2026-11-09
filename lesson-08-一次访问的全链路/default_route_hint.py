#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Windows: 显示默认路由（课时 02），便于联想 ARP 的下一跳。"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# 复用第六课编码
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lesson-06-ARP与二层寻址"))
from sys_encoding import console_encoding  # noqa: E402


def main() -> None:
    proc = subprocess.run(["route", "print", "0.0.0.0"], capture_output=True)
    text = proc.stdout.decode(console_encoding(), errors="replace")
    print("=== 默认路由（route print 0.0.0.0 节选）===\n")
    print(text)
    m = re.search(r"0\.0\.0\.0\s+0\.0\.0\.0\s+(\d+\.\d+\.\d+\.\d+)", text)
    if m:
        gw = m.group(1)
        print(f"\n下一跳网关常为: {gw}")
        print("ARP 通常会解析该 IP 的 MAC（课时 06）。")


if __name__ == "__main__":
    main()
