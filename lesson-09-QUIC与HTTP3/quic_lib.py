# -*- coding: utf-8 -*-
"""QUIC 长包头前缀解析（教学子集）。"""

from __future__ import annotations

import re
from pathlib import Path

LONG_TYPES = {
    0x0: "Initial",
    0x1: "0-RTT",
    0x2: "Handshake",
    0x3: "Retry",
}


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def parse_long_header_prefix(data: bytes) -> dict:
    if not data:
        raise ValueError("空数据")
    first = data[0]
    if first & 0x80 == 0:
        raise ValueError("样本应为 QUIC 长包头（首字节最高位=1）")
    fixed = bool(first & 0x40)
    pkt_type = (first & 0x30) >> 4
    if len(data) < 7:
        raise ValueError("不足以读取版本与 DCID 长度")
    version = int.from_bytes(data[1:5], "big")
    dcid_len = data[5]
    if len(data) < 6 + dcid_len:
        raise ValueError("DCID 长度超出缓冲区")
    dcid = data[6 : 6 + dcid_len]
    pos = 6 + dcid_len
    if len(data) <= pos:
        raise ValueError("缺少 SCID 长度")
    scid_len = data[pos]
    pos += 1
    if len(data) < pos + scid_len:
        raise ValueError("SCID 长度超出缓冲区")
    scid = data[pos : pos + scid_len]
    pos += scid_len
    return {
        "form": "long",
        "fixed_bit": fixed,
        "type": LONG_TYPES.get(pkt_type, f"unknown_{pkt_type}"),
        "version_hex": f"0x{version:08x}",
        "dcid_len": dcid_len,
        "dcid_hex": dcid.hex(),
        "scid_len": scid_len,
        "scid_hex": scid.hex(),
        "remaining_bytes": len(data) - pos,
    }
