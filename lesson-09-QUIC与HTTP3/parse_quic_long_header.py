#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from quic_lib import load_hex, parse_long_header_prefix


def main() -> None:
    path = Path(__file__).resolve().parent / "samples" / "quic_initial_long.hex"
    info = parse_long_header_prefix(load_hex(path))
    print("=== QUIC 长包头（前缀）===")
    for k, v in info.items():
        print(f"  {k}: {v}")
    print("\nUDP 载荷里如是；Wireshark: udp.port==443 and quic")
    print("对比第八课: 同一网站可能先有 TCP TLS，再切 UDP QUIC（Alt-Svc）。")


if __name__ == "__main__":
    main()
