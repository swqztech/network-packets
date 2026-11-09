#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经 TCP HTTPS 探测 Alt-Svc（网站告知客户端可用 HTTP/3）。
仍是第八课路径；只是读响应头，不解 QUIC。
"""

import socket
import ssl

HOST = "cloudflare.com"
PORT = 443


def main() -> None:
    ctx = ssl.create_default_context()
    req = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n".encode()
    with socket.create_connection((HOST, PORT), timeout=10) as raw:
        with ctx.wrap_socket(raw, server_hostname=HOST) as tls:
            tls.sendall(req)
            data = tls.recv(65536)
    head = data.split(b"\r\n\r\n", 1)[0].decode("latin-1", errors="replace")
    print(f"=== {HOST} 响应头（节选）===\n")
    alt = [ln for ln in head.split("\r\n") if ln.lower().startswith("alt-svc")]
    for ln in head.split("\r\n")[:15]:
        print(ln)
    print("\n--- Alt-Svc（若有）---")
    if alt:
        for ln in alt:
            print(ln)
        print("\n含义: 浏览器可据此尝试 UDP/QUIC 访问 HTTP/3。")
    else:
        print("(本响应未含 Alt-Svc，不代表站点永远不用 HTTP/3)")
    print("抓包: 之后可能出现 udp.port==443 and quic")


if __name__ == "__main__":
    main()
