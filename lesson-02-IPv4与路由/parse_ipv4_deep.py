#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析多个 IPv4 样本，重点展示 TTL、分片标志、校验和。"""

from pathlib import Path

from ipv4_lib import load_hex, parse_ipv4_header

PROTO = {1: "ICMP", 6: "TCP", 17: "UDP"}


def describe(name: str, path: Path) -> None:
    raw = load_hex(path)
    info = parse_ipv4_header(raw)
    print(f"\n{'='*60}")
    print(f"样本: {name}")
    print(f"{'='*60}")
    print(f"  源 IP / 目的 IP: {info['src']} -> {info['dst']}")
    print(f"  总长度: {info['total_length']}  头长: {info['ihl_bytes']}  TTL: {info['ttl']}")
    print(f"  协议: {info['protocol']} ({PROTO.get(info['protocol'], '?')})")
    print(f"  标识 ID: 0x{info['identification']:04x}")
    print(
        f"  分片: DF={info['df']}, MF={info['mf']}, "
        f"偏移={info['fragment_offset_bytes']} 字节"
    )
    csum_status = "通过" if info["checksum_ok"] else "失败(教学样本可能故意未填)"
    print(
        f"  头校验和: 0x{info['checksum_stored']:04x} "
        f"(重算 0x{info['checksum_recalc']:04x}, {csum_status})"
    )
    print(f"  载荷长度: {len(info['payload'])} 字节")


def main() -> None:
    base = Path(__file__).resolve().parent / "samples"
    describe("典型 TCP 之上", base / "ipv4_tcp.hex")
    describe("带 MF 的分片示意", base / "ipv4_fragment.hex")
    print("\n--- 提示 ---")
    print("真实抓包里 DF 经常为 1；本课第二个样本为演示 MF/Offset 字段而合成。")


if __name__ == "__main__":
    main()
