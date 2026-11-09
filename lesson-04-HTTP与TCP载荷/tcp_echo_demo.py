#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本机 TCP 回声：体验三次握手后，字节在连接上传输。
载荷仍是任意字节，不必是 HTTP。
"""

from __future__ import annotations

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 19091
PAYLOAD = (
    b"GET /demo HTTP/1.1\r\n"
    b"Host: localhost\r\n"
    b"\r\n"
    b"This text rides inside TCP segments."
)


def echo_server() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    srv.settimeout(5.0)
    conn, addr = srv.accept()
    with conn:
        print(f"[服务端] 连接来自 {addr}，等待字节流…")
        chunks: list[bytes] = []
        while True:
            part = conn.recv(4096)
            if not part:
                break
            chunks.append(part)
            conn.sendall(part)  # 回声
        data = b"".join(chunks)
        print(f"[服务端] 共收到 {len(data)} 字节，已原样回显")
    srv.close()


def main() -> None:
    t = threading.Thread(target=echo_server, daemon=True)
    t.start()
    time.sleep(0.15)

    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, PORT))
    cli.sendall(PAYLOAD)
    cli.shutdown(socket.SHUT_WR)

    received = bytearray()
    while True:
        block = cli.recv(4096)
        if not block:
            break
        received.extend(block)
    cli.close()

    print(f"[客户端] 发出 {len(PAYLOAD)} 字节")
    print(f"[客户端] 收回 {len(received)} 字节")
    print("--- 收回内容预览 ---")
    try:
        print(received.decode("utf-8"))
    except UnicodeDecodeError:
        print(received[:200])

    ok = received == PAYLOAD
    print(f"\n内容与发出一致: {ok}")
    t.join(timeout=6)


if __name__ == "__main__":
    main()
