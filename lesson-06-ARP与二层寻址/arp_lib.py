# -*- coding: utf-8 -*-
"""以太网 + ARP 解析。"""

from __future__ import annotations

import ipaddress
import re
import struct
from pathlib import Path

ARP_OP = {1: "request", 2: "reply"}


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def mac_fmt(b: bytes) -> str:
    return ":".join(f"{x:02x}" for x in b)


def parse_ethernet(data: bytes) -> tuple[dict, bytes]:
    if len(data) < 14:
        raise ValueError("以太网头不足 14 字节")
    dest, src, etype_b = data[:6], data[6:12], data[12:14]
    etype = struct.unpack("!H", etype_b)[0]
    names = {0x0800: "IPv4", 0x0806: "ARP"}
    return {
        "目的 MAC": mac_fmt(dest),
        "源 MAC": mac_fmt(src),
        "类型": f"0x{etype:04x} ({names.get(etype, '其他')})",
    }, data[14:], etype


def parse_arp(payload: bytes) -> dict:
    if len(payload) < 28:
        raise ValueError("ARP 包至少 28 字节（IPv4/以太网）")
    (
        hwtype,
        protype,
        hwlen,
        plen,
        opcode,
        sha,
        spa,
        tha,
        tpa,
    ) = struct.unpack("!HHBBH6s4s6s4s", payload[:28])
    return {
        "硬件类型": hwtype,
        "协议类型": f"0x{protype:04x}",
        "操作": f"{opcode} ({ARP_OP.get(opcode, '?')})",
        "发送方 MAC": mac_fmt(sha),
        "发送方 IP": str(ipaddress.IPv4Address(spa)),
        "目标 MAC": mac_fmt(tha),
        "目标 IP": str(ipaddress.IPv4Address(tpa)),
    }
