# -*- coding: utf-8 -*-
"""第三课：TCP / UDP 头解析。"""

from __future__ import annotations

import re
import struct
from pathlib import Path


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


TCP_FLAGS = [
    (0x01, "FIN"),
    (0x02, "SYN"),
    (0x04, "RST"),
    (0x08, "PSH"),
    (0x10, "ACK"),
    (0x20, "URG"),
]


def flag_names(bits: int) -> str:
    names = [n for m, n in TCP_FLAGS if bits & m]
    return ",".join(names) if names else f"0x{bits:02x}"


def parse_tcp(data: bytes) -> dict:
    if len(data) < 20:
        raise ValueError("TCP 头至少 20 字节")
    src, dst, seq, ack, off_res, window, checksum, urgent = struct.unpack(
        "!HHIIHHHH", data[:20]
    )
    data_offset = (off_res >> 12) * 4
    flags = off_res & 0x3F
    if data_offset < 20 or len(data) < data_offset:
        raise ValueError("TCP 头长度非法")
    return {
        "src_port": src,
        "dst_port": dst,
        "seq": seq,
        "ack": ack,
        "header_len": data_offset,
        "flags": flag_names(flags),
        "window": window,
        "checksum": checksum,
        "payload": data[data_offset:],
    }


def parse_udp(data: bytes) -> dict:
    if len(data) < 8:
        raise ValueError("UDP 头 8 字节")
    src, dst, length, checksum = struct.unpack("!HHHH", data[:8])
    payload_len = max(0, length - 8)
    payload = data[8 : 8 + payload_len] if length else data[8:]
    return {
        "src_port": src,
        "dst_port": dst,
        "length": length,
        "checksum": checksum,
        "payload": payload,
    }
