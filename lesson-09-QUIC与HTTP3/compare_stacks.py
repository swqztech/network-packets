#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""并排对比经典 HTTPS 与 HTTP/3 协议栈。"""

ROWS = [
    ("应用", "HTTP/1.1 或 HTTP/2", "HTTP/3"),
    ("安全", "TLS 1.2/1.3 记录在 TCP 上", "TLS 1.3 集成在 QUIC 内"),
    ("传输", "TCP :443", "QUIC over UDP :443"),
    ("网络", "IPv4/IPv6", "相同"),
    ("链路", "以太网 + ARP", "相同"),
]


def main() -> None:
    print(f"{'层':<6} {'HTTPS 经典':<28} {'HTTP/3'}")
    print("-" * 64)
    for layer, classic, h3 in ROWS:
        print(f"{layer:<6} {classic:<28} {h3}")


if __name__ == "__main__":
    main()
