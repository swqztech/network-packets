#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
与真实站点建立 TLS（出站 TCP 443）。
抓包时可同时看：先 tcp 握手，再 tls ClientHello。
"""

from __future__ import annotations

import socket
import ssl
import sys

HOST = "example.com"
PORT = 443


def main() -> int:
    print(f"连接 TLS: {HOST}:{PORT}")
    print("（若同步 Wireshark 抓包：tcp.port==443 and tls）\n")
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((HOST, PORT), timeout=8) as raw:
            with ctx.wrap_socket(raw, server_hostname=HOST) as tls:
                print(f"  协商 TLS 版本: {tls.version()}")
                print(f"  选定密码套件: {tls.cipher()[0]}")
                tls.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
                chunks = []
                while True:
                    part = tls.recv(4096)
                    if not part:
                        break
                    chunks.append(part)
                body = b"".join(chunks)
    except (socket.timeout, ssl.SSLError, OSError) as e:
        print(f"连接失败: {e}")
        return 1

    print(f"  收到 {len(body)} 字节应用数据（已解密，仅本进程可见）")
    head = body.split(b"\r\n\r\n", 1)[0].decode("latin-1", errors="replace")
    print("  响应起始行:")
    for line in head.split("\r\n")[:3]:
        print(f"    {line}")
    print("\n对比: 线上抓包看到的是 TLS 密文，不是上面这些明文行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
