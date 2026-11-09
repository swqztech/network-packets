# -*- coding: utf-8 -*-
"""ICMP 解析（Echo 为主）。"""

from __future__ import annotations

import re
import struct
from pathlib import Path

ICMP_TYPES = {
    0: "Echo Reply",
    3: "Destination Unreachable",
    8: "Echo Request",
    11: "Time Exceeded",
}


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def icmp_checksum(body: bytes) -> int:
    if len(body) % 2:
        body += b"\x00"
    total = 0
    for i in range(0, len(body), 2):
        total += body[i] << 8 | body[i + 1]
        while total > 0xFFFF:
            total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def parse_icmp(data: bytes) -> dict:
    if len(data) < 8:
        raise ValueError("ICMP 至少 8 字节")
    typ, code, csum, ident, seq = struct.unpack("!BBHHH", data[:8])
    payload = data[8:]
    calc = icmp_checksum(data[:2] + b"\x00\x00" + data[4:]) if len(data) >= 4 else 0
    return {
        "type": typ,
        "type_name": ICMP_TYPES.get(typ, f"类型 {typ}"),
        "code": code,
        "checksum": csum,
        "checksum_recalc": calc,
        "identifier": ident,
        "sequence": seq,
        "payload": payload,
    }
