#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTPS 握手阶段与 TCP 流方向（文字）。"""

STEPS = [
    ("TCP", "SYN → SYN,ACK → ACK（第三课）"),
    ("TLS", "ClientHello：明文，常含 SNI"),
    ("TLS", "ServerHello + Certificate + …"),
    ("TLS", "客户端 Finished；双方 ChangeCipherSpec"),
    ("TLS", "Application Data：加密，Wireshark 默认无 HTTP 树"),
    ("HTTP", "逻辑上仍是 GET/200，但在 TLS 里面"),
]


def main() -> None:
    print("第七课：HTTPS = TCP + TLS + HTTP\n")
    for layer, detail in STEPS:
        print(f"  [{layer:4}] {detail}")
    print("\n过滤器: tcp.port == 443 与 tls 组合使用。")


if __name__ == "__main__":
    main()
