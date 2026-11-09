#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用文字重演三次握手，序号与第三课样本一致。"""

CLIENT_PORT = 0xB24E
SERVER_PORT = 443
CLIENT_ISN = 0x8C4A2F10
SERVER_ISN = 0x12345678


def fmt(seq: int) -> str:
    return f"{seq} (0x{seq:08x})"


def main() -> None:
    print("场景: 客户端访问 93.184.216.34:443 (HTTPS)\n")
    steps = [
        (
            "① 客户端 → 服务端",
            f"SYN  {CLIENT_PORT} → {SERVER_PORT}",
            f"seq={fmt(CLIENT_ISN)}  ack=0  标志=SYN",
        ),
        (
            "② 服务端 → 客户端",
            f"SYN+ACK  {SERVER_PORT} → {CLIENT_PORT}",
            f"seq={fmt(SERVER_ISN)}  ack={fmt(CLIENT_ISN + 1)}  标志=SYN,ACK",
        ),
        (
            "③ 客户端 → 服务端",
            f"ACK  {CLIENT_PORT} → {SERVER_PORT}",
            f"seq={fmt(CLIENT_ISN + 1)}  ack={fmt(SERVER_ISN + 1)}  标志=ACK",
        ),
    ]
    for title, direction, detail in steps:
        print(title)
        print(f"  {direction}")
        print(f"  {detail}\n")

    print("此后 TCP 载荷里才会出现 TLS / HTTP；前两课学的 IP 头在整个过程中不变层职责。")
    print("运行 parse_transport.py 可对照样本 ①② 的十六进制。")


if __name__ == "__main__":
    main()
