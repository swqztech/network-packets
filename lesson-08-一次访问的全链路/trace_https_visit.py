#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一次 HTTPS 访问 narrated：DNS →（ARP 提示）→ TCP/TLS → GET。
边跑边对照 WIRESHARK_TIMELINE.md。
"""

from __future__ import annotations

import socket
import ssl
import sys

HOST = "example.com"
PORT = 443


def step_dns(name: str) -> list[str]:
    print("[1/5] DNS（课时 05）")
    print(f"      查询: {name}")
    infos = socket.getaddrinfo(name, None, type=socket.SOCK_STREAM)
    ips = []
    for fam, _, _, _, addr in infos:
        if fam == socket.AF_INET:
            ips.append(addr[0])
    ips = list(dict.fromkeys(ips))
    print(f"      结果 IPv4: {', '.join(ips) or '(无)'}")
    print("      Wireshark: dns.qry.name contains", repr(name.split('.')[0]))
    return ips


def step_arp_hint() -> None:
    print("\n[2/5] ARP（课时 06）")
    print("      若网关 MAC 不在缓存，会先 arp 广播 Who has 网关 IP")
    print("      本脚本不主动发包；可另开: arp -a 看 192.168.1.1 一类条目")
    print("      Wireshark: arp")


def step_tls_http(name: str, connect_ip: str | None) -> int:
    print("\n[3/5] TCP 三次握手（课时 03）→ 端口", PORT)
    print("[4/5] TLS 握手（课时 07）")
    print("[5/5] HTTP GET（课时 04，在 TLS 内）")

    ctx = ssl.create_default_context()
    target = connect_ip or name
    print(f"      connect → {target}:{PORT} (SNI={name})")
    try:
        with socket.create_connection((target, PORT), timeout=10) as raw:
            with ctx.wrap_socket(raw, server_hostname=name) as tls:
                print(f"      TLS: {tls.version()}  套件: {tls.cipher()[0]}")
                req = (
                    f"GET / HTTP/1.1\r\nHost: {name}\r\nConnection: close\r\n\r\n"
                ).encode("ascii")
                tls.sendall(req)
                buf = bytearray()
                while True:
                    chunk = tls.recv(8192)
                    if not chunk:
                        break
                    buf.extend(chunk)
    except OSError as e:
        print(f"      失败: {e}")
        return 1

    status = buf.split(b"\r\n", 1)[0].decode("latin-1", errors="replace")
    print(f"      响应起始: {status}")
    print(f"      共 {len(buf)} 字节（进程内已解密；抓包仍为 TLS 密文）")
    print("\n--- 抓包对齐 ---")
    print("      tcp.flags.syn==1 && tcp.port==443")
    print("      tls.handshake.type == 1  # ClientHello")
    return 0


def main() -> int:
    print("=" * 56)
    print(f"全链路演示: https://{HOST}/")
    print("建议: Wireshark 先开始捕获再运行本脚本")
    print("=" * 56 + "\n")

    try:
        ips = step_dns(HOST)
    except socket.gaierror as e:
        print(f"DNS 失败: {e}")
        return 1

    step_arp_hint()
    ip = ips[0] if ips else None
    return step_tls_http(HOST, ip)


if __name__ == "__main__":
    raise SystemExit(main())
