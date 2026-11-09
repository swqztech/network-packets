#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""显示系统 ARP 表（Windows arp -a），编码与 run_ping 同理。"""

from __future__ import annotations

import subprocess

from sys_encoding import console_encoding


def run_arp_a() -> tuple[int, str]:
    proc = subprocess.run(["arp", "-a"], capture_output=True)
    enc = console_encoding()
    text = proc.stdout.decode(enc, errors="replace") + proc.stderr.decode(enc, errors="replace")
    return proc.returncode, text


def main() -> None:
    code, text = run_arp_a()
    print("=== 本机 ARP 缓存（arp -a）===")
    print(text.strip())
    print(f"\n退出码: {code}")
    print("解读: 「动态」条目多为最近 ARP 学到的；「静态」可人工绑定。")
    print("Wireshark: 在 ping 网关或本网段主机后执行本脚本，对照 arp 过滤器里的 Who has / is at。")


if __name__ == "__main__":
    main()
