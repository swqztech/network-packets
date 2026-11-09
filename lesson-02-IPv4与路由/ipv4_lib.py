# -*- coding: utf-8 -*-
"""第二课共用：IPv4 解析与校验和。"""

from __future__ import annotations

import ipaddress
import re
import struct
from pathlib import Path


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def ipv4_checksum(header: bytes) -> int:
    """计算 IPv4 头校验和（16 位结果，未写入包头）。"""
    if len(header) % 2:
        header += b"\x00"
    total = 0
    for i in range(0, len(header), 2):
        word = header[i] << 8 | header[i + 1]
        total += word
        while total > 0xFFFF:
            total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def verify_ipv4_checksum(header: bytes) -> tuple[bool, int, int]:
    """验算；返回 (是否通过, 头内记录的校验和, 重算值)。"""
    stored = struct.unpack("!H", header[10:12])[0]
    hdr = bytearray(header)
    hdr[10:12] = b"\x00\x00"
    calc = ipv4_checksum(bytes(hdr))
    # 线上惯例：对整头再求和应为 0xFFFF
    hdr[10:12] = struct.pack("!H", stored)
    fold = 0
    h = bytearray(header)
    if len(h) % 2:
        h += b"\x00"
    for i in range(0, len(h), 2):
        fold += h[i] << 8 | h[i + 1]
        while fold > 0xFFFF:
            fold = (fold & 0xFFFF) + (fold >> 16)
    ok = fold == 0xFFFF
    return ok, stored, calc


def parse_ipv4_header(data: bytes) -> dict:
    if len(data) < 20:
        raise ValueError("IPv4 头至少 20 字节")
    ver_ihl = data[0]
    version = ver_ihl >> 4
    ihl = (ver_ihl & 0x0F) * 4
    fields = struct.unpack("!BBHHHBBH4s4s", data[:20])
    (
        _v,
        tos,
        total_len,
        ident,
        flags_frag,
        ttl,
        protocol,
        _csum,
        src,
        dst,
    ) = fields
    flags = (flags_frag >> 13) & 0x7
    frag_off = flags_frag & 0x1FFF
    df = bool(flags & 0x2)
    mf = bool(flags & 0x1)
    ok, stored_csum, calc_csum = verify_ipv4_checksum(data[:ihl])
    return {
        "version": version,
        "ihl_bytes": ihl,
        "tos": tos,
        "total_length": total_len,
        "identification": ident,
        "df": df,
        "mf": mf,
        "fragment_offset_bytes": frag_off * 8,
        "ttl": ttl,
        "protocol": protocol,
        "checksum_ok": ok,
        "checksum_stored": stored_csum,
        "checksum_recalc": calc_csum,
        "src": str(ipaddress.IPv4Address(src)),
        "dst": str(ipaddress.IPv4Address(dst)),
        "payload": data[ihl:],
    }
