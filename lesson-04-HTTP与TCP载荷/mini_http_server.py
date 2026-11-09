#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""极简 HTTP/1.1 服务：演示 TCP 载荷即 HTTP 响应文本。"""

from __future__ import annotations

import socket

from http_parse_lib import parse_http_request

HOST = "127.0.0.1"
PORT = 18080


def build_response(body: str) -> bytes:
    body_bytes = body.encode("utf-8")
    head = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return head.encode("ascii") + body_bytes


def handle(conn: socket.socket, addr) -> None:
    buf = bytearray()
    while b"\r\n\r\n" not in buf and len(buf) < 65536:
        chunk = conn.recv(4096)
        if not chunk:
            break
        buf.extend(chunk)

    try:
        req = parse_http_request(bytes(buf))
        msg = (
            f"你好，这是 lesson-04。\n"
            f"你请求了: {req['method']} {req['path']}\n"
            f"Host 头: {req['headers'].get('host', '-')}\n"
        )
    except ValueError:
        msg = "收到无法解析的 HTTP 请求，但仍是 TCP 载荷里的字节。\n"

    conn.sendall(build_response(msg))
    conn.close()
    print(f"[HTTP] 已响应 {addr}")


def main() -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"监听 http://{HOST}:{PORT}/  （Ctrl+C 结束）")
    try:
        while True:
            conn, addr = srv.accept()
            handle(conn, addr)
    except KeyboardInterrupt:
        print("\n已停止")
    finally:
        srv.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
