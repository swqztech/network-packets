#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调用系统 ping，帮助对照第五课与 Wireshark 过滤器 icmp。"""

from __future__ import annotations

import locale
import platform
import re
import subprocess

TARGETS = ["127.0.0.1", "1.1.1.1"]


def ping_output_encoding() -> str:
    """Windows 的 ping/cmd 输出多为系统 OEM/ANSI 编码（中文环境常为 GBK），不是 UTF-8。"""
    if "windows" in platform.system().lower():
        for name in ("gbk", locale.getpreferredencoding(False) or "", "cp936", "mbcs"):
            if name:
                return name
        return "gbk"
    return "utf-8"


def ping_once(host: str) -> tuple[int, str]:
    system = platform.system().lower()
    if "windows" in system:
        cmd = ["ping", "-n", "1", "-w", "2000", host]
    else:
        cmd = ["ping", "-c", "1", "-W", "2", host]
    proc = subprocess.run(cmd, capture_output=True)
    enc = ping_output_encoding()
    text = proc.stdout.decode(enc, errors="replace") + proc.stderr.decode(enc, errors="replace")
    return proc.returncode, text


def summarize(host: str, code: int, text: str) -> None:
    print(f"\n{'='*50}")
    print(f"目标: {host}  (退出码 {code})")
    print("--- 系统 ping 输出（节选）---")
    for line in text.strip().splitlines()[:12]:
        print(line)

    if "windows" in platform.system().lower():
        # 中文：时间=172ms、时间<1ms；英文：time=172ms
        m = (
            re.search(r"时间[=<]?(\d+)ms", text)
            or re.search(r"time[=<]?(\d+)ms", text, re.I)
        )
    else:
        m = re.search(r"time=(\d+\.?\d*)\s*ms", text, re.I)
    if m:
        print(f"\n解读: 收到 ICMP Echo Reply，往返约 {m.group(1)} ms")
    elif code != 0:
        print("\n解读: 未收到应答（超时、禁 ping 或路由不可达），Wireshark 里可能只有 Request")
    print("Wireshark 过滤器建议: icmp and ip.addr ==", host)


def main() -> int:
    print("第五课: ping 触发 ICMP Echo Request/Reply")
    print("可在抓包时用显示过滤器 icmp 对照。")
    for host in TARGETS:
        code, text = ping_once(host)
        summarize(host, code, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
