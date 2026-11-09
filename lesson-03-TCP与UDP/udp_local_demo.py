#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本机 UDP：短生命周期服务端 + 客户端一发一收。
展示传输层「端口 + datagram」而无 TCP 握手。
"""

from __future__ import annotations

import socket
import struct
import threading
import time

HOST = "127.0.0.1"
PORT = 49876
MESSAGE = b"lesson-03-udp-datagram"


def checksum_udp_pseudo(header: bytes, payload: bytes) -> int:
    """仅教学：演示 UDP 校验和覆盖 伪首部 + UDP 头 + 载荷（IPv4）。"""
    src = socket.inet_aton(HOST)
    dst = src
    proto = 17
    udp_len = 8 + len(payload)
    pseudo = src + dst + struct.pack("!BBH", 0, proto, udp_len)
    body = header[:6] + b"\x00\x00" + payload  # 校验和字段置 0
    data = pseudo + body
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += data[i] << 8 | data[i + 1]
        while total > 0xFFFF:
            total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def server_ready() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.settimeout(3.0)
    try:
        data, addr = sock.recvfrom(2048)
        print(f"[服务端] 收到 {len(data)} 字节 来自 {addr}: {data.decode()}")
        sock.sendto(b"ACK:" + data, addr)
    finally:
        sock.close()


def main() -> None:
    t = threading.Thread(target=server_ready, daemon=True)
    t.start()
    time.sleep(0.1)

    payload = MESSAGE
    header = struct.pack("!HHHH", 54000, PORT, 8 + len(payload), 0)
    csum = checksum_udp_pseudo(header, payload)
    header = struct.pack("!HHHH", 54000, PORT, 8 + len(payload), csum)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.sendto(payload, (HOST, PORT))
        print(f"[客户端] 已发送 UDP 到 {HOST}:{PORT}，载荷={payload.decode()}")
        client.settimeout(2.0)
        reply, _ = client.recvfrom(2048)
        print(f"[客户端] 收到回复: {reply.decode()}")
        print(f"[教学] 自行组头的 UDP 校验和 = 0x{csum:04x}（真实栈在 sendto 时自动计算）")
    finally:
        client.close()
    t.join(timeout=5)


if __name__ == "__main__":
    main()
