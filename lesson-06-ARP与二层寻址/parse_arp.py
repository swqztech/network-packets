#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 ARP 请求/应答样本（含以太网头）。"""

from pathlib import Path

from arp_lib import load_hex, parse_arp, parse_ethernet


def show(name: str, path: Path) -> None:
    raw = load_hex(path)
    eth, rest, etype = parse_ethernet(raw)
    print(f"\n{'='*60}")
    print(name)
    print(f"{'='*60}")
    print("【链路层】")
    for k, v in eth.items():
        print(f"  {k}: {v}")
    if etype != 0x0806:
        print("  警告: 不是 ARP 帧")
        return
    arp = parse_arp(rest)
    print("【ARP】")
    for k, v in arp.items():
        print(f"  {k}: {v}")
    if "request" in arp["操作"]:
        print(f"\n  人话: {arp['发送方 IP']} 在问 —— 谁有 {arp['目标 IP']}？")
    else:
        print(
            f"\n  人话: {arp['发送方 IP']} 的 MAC 是 {arp['发送方 MAC']} "
            f"（单播告诉 {arp['目标 IP']}）"
        )


def main() -> None:
    base = Path(__file__).resolve().parent / "samples"
    print("ARP 只解决同一广播域里的 IP→MAC；跨网段不广播整个互联网。")
    show("ARP Request（广播）", base / "arp_request_frame.hex")
    show("ARP Reply（单播）", base / "arp_reply_frame.hex")


if __name__ == "__main__":
    main()
