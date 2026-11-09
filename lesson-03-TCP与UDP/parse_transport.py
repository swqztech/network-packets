#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 TCP / UDP 样本并对比字段。"""

from pathlib import Path

from transport_lib import load_hex, parse_tcp, parse_udp

SAMPLES_TCP = [
    ("TCP · 客户端 SYN", "tcp_syn.hex"),
    ("TCP · 服务端 SYN+ACK", "tcp_synack.hex"),
]
SAMPLES_UDP = [("UDP · DNS 外形", "udp_dns_like.hex")]


def show_tcp(title: str, path: Path) -> None:
    info = parse_tcp(load_hex(path))
    print(f"\n=== {title} ===")
    print(f"  {info['src_port']} -> {info['dst_port']}")
    print(f"  seq={info['seq']}  ack={info['ack']}  标志={info['flags']}")
    print(f"  头长={info['header_len']}  窗口={info['window']}")
    print(f"  载荷: {len(info['payload'])} 字节")


def show_udp(title: str, path: Path) -> None:
    info = parse_udp(load_hex(path))
    print(f"\n=== {title} ===")
    print(f"  {info['src_port']} -> {info['dst_port']}")
    print(f"  UDP 长度字段={info['length']}  校验和=0x{info['checksum']:04x}")
    preview = info["payload"][:40]
    try:
        text = preview.decode("utf-8")
        print(f"  载荷预览: {text!r}")
    except UnicodeDecodeError:
        print(f"  载荷(hex): {preview.hex()}")


def main() -> None:
    base = Path(__file__).resolve().parent / "samples"
    print("传输层只管：端口 +（TCP 时）连接状态/序号；（UDP 时）一datagram 一包")
    for title, name in SAMPLES_TCP:
        show_tcp(title, base / name)
    for title, name in SAMPLES_UDP:
        show_udp(title, base / name)
    print("\n--- 对照 ---")
    print("SYN 只有 SYN 位；SYN+ACK 同时有 SYN 与 ACK，且 ack=对端 seq+1。")
    print("UDP 无序号/标志，一个 UDP 包即一次 delivery。")


if __name__ == "__main__":
    main()
