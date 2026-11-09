#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一课可选演示：向本机发送一个 UDP 包。
观察：应用只提供「消息 + 端口」，操作系统负责封装 IP/UDP。
"""

import socket


def main() -> None:
    msg = b"Hello from lesson-01 (network packet)"
    port = 54321
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sent = sock.sendto(msg, ("127.0.0.1", port))
        print(f"已通过 UDP 发出 {sent} 字节 -> 127.0.0.1:{port}")
        print(f"载荷: {msg.decode()}")
        print("\n若没有程序在监听该端口，包会被本机丢弃，这仍然算一次「发包」。")
        print("可用 Wireshark 过滤: udp.port == 54321")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
