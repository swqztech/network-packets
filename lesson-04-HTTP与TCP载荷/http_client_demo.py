#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""向 mini_http_server 发 HTTP GET 并打印响应。"""

import socket

HOST = "127.0.0.1"
PORT = 18080

REQUEST = (
    f"GET /hello?from=lesson-04 HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    f"User-Agent: network-packets/1.0\r\n"
    f"\r\n"
).encode("ascii")


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(REQUEST)
        data = sock.recv(65536)
    except (ConnectionRefusedError, TimeoutError):
        print("无法连接。请先运行: python mini_http_server.py")
        return
    finally:
        sock.close()

    print("=== 收到 TCP 载荷（HTTP 响应）===")
    print(data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
