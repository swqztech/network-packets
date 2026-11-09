#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""演示 IPv4 头校验和的计算，以及修改 TTL 后如何重算。"""

import struct
from pathlib import Path

from ipv4_lib import ipv4_checksum, load_hex, parse_ipv4_header


def main() -> None:
    path = Path(__file__).resolve().parent / "samples" / "ipv4_tcp.hex"
    raw = bytearray(load_hex(path))
    info = parse_ipv4_header(bytes(raw))

    print("=== 原始 IPv4 头（来自第一课同源样本）===")
    print(f"TTL = {info['ttl']}, 校验和 = 0x{info['checksum_stored']:04x}")

    # 正确的头：先清零校验和字段再算
    hdr = bytearray(raw[: info["ihl_bytes"]])
    hdr[10:12] = b"\x00\x00"
    calc = ipv4_checksum(bytes(hdr))
    hdr[10:12] = struct.pack("!H", calc)
    print(f"按算法重算并写回校验和 = 0x{calc:04x}")

    # 模拟路由器：TTL - 1
    print("\n=== 模拟路由器转发：TTL 减 1 ===")
    hdr[8] -= 1
    new_ttl = hdr[8]
    hdr[10:12] = b"\x00\x00"
    new_csum = ipv4_checksum(bytes(hdr))
    hdr[10:12] = struct.pack("!H", new_csum)
    print(f"新 TTL = {new_ttl}, 新校验和 = 0x{new_csum:04x}")
    print("（每跳都可能重复：改 TTL → 清零校验和字段 → 重算 → 写回）")


if __name__ == "__main__":
    main()
