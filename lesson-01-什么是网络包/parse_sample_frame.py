#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一课演示：从十六进制样本解析 以太网 + IPv4 + TCP 头。
不依赖第三方库，便于对照 README 里的分层图。
"""

from __future__ import annotations

import ipaddress
import re
import struct
import sys
from pathlib import Path


def load_hex_payload(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    # 去掉注释行
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    hex_str = re.sub(r"\s+", "", "".join(lines))
    return bytes.fromhex(hex_str)


def mac_fmt(b: bytes) -> str:
    return ":".join(f"{x:02x}" for x in b)


def parse_ethernet(data: bytes) -> tuple[dict, bytes]:
    if len(data) < 14:
        raise ValueError("以太网头至少 14 字节")
    dest, src, ethertype = data[:6], data[6:12], data[12:14]
    etype = struct.unpack("!H", ethertype)[0]
    info = {
        "目的 MAC": mac_fmt(dest),
        "源 MAC": mac_fmt(src),
        "类型": f"0x{etype:04x}" + (" (IPv4)" if etype == 0x0800 else ""),
    }
    return info, data[14:]


def parse_ipv4(data: bytes) -> tuple[dict, bytes]:
    if len(data) < 20:
        raise ValueError("IPv4 头至少 20 字节")
    ver_ihl = data[0]
    version = ver_ihl >> 4
    ihl = (ver_ihl & 0x0F) * 4
    if version != 4:
        raise ValueError(f"样本不是 IPv4 (version={version})")
    if len(data) < ihl:
        raise ValueError("IPv4 头长度不足")
    (
        _ver_ihl,
        dscp_ecn,
        total_len,
        ident,
        flags_frag,
        ttl,
        protocol,
        checksum,
        src,
        dst,
    ) = struct.unpack("!BBHHHBBH4s4s", data[:20])
    flags = (flags_frag >> 13) & 0x7
    frag_off = flags_frag & 0x1FFF
    proto_name = {6: "TCP", 17: "UDP"}.get(protocol, str(protocol))
    info = {
        "版本": version,
        "头长(字节)": ihl,
        "总长度(字节)": total_len,
        "TTL": ttl,
        "协议": f"{protocol} ({proto_name})",
        "源 IP": str(ipaddress.IPv4Address(src)),
        "目的 IP": str(ipaddress.IPv4Address(dst)),
        "标志/片偏移": f"flags={flags:#x}, offset={frag_off}",
    }
    return info, data[ihl:]


def parse_tcp(data: bytes) -> tuple[dict, bytes]:
    if len(data) < 20:
        raise ValueError("TCP 头至少 20 字节")
    src_port, dst_port, seq, ack, off_res_flags, window, checksum, urgent = struct.unpack(
        "!HHIIHHHH", data[:20]
    )
    data_offset = (off_res_flags >> 12) * 4
    flags = off_res_flags & 0x3F
    flag_bits = []
    names = [(0x02, "SYN"), (0x10, "ACK"), (0x01, "FIN"), (0x04, "RST"), (0x08, "PSH")]
    for mask, name in names:
        if flags & mask:
            flag_bits.append(name)
    info = {
        "源端口": src_port,
        "目的端口": dst_port,
        "序号": seq,
        "确认号": ack,
        "头长(字节)": data_offset,
        "标志": ",".join(flag_bits) or f"0x{flags:02x}",
        "窗口": window,
    }
    payload = data[data_offset:]
    return info, payload


def print_section(title: str, fields: dict) -> None:
    print(f"\n=== {title} ===")
    for k, v in fields.items():
        print(f"  {k}: {v}")


def main() -> int:
    base = Path(__file__).resolve().parent
    sample = base / "sample_frame.hex"
    if not sample.exists():
        print(f"找不到样本文件: {sample}", file=sys.stderr)
        return 1

    raw = load_hex_payload(sample)
    print(f"样本总长度: {len(raw)} 字节")
    print("（由下往上读：先看链路层，再看网络层、传输层）")

    eth, rest = parse_ethernet(raw)
    print_section("链路层 · 以太网", eth)

    ip_info, rest = parse_ipv4(rest)
    print_section("网络层 · IPv4", ip_info)

    tcp_info, payload = parse_tcp(rest)
    print_section("传输层 · TCP", tcp_info)

    if payload:
        print(f"\n载荷: {len(payload)} 字节")
        try:
            print("  内容预览:", payload[:64].decode("utf-8", errors="replace"))
        except Exception:
            print("  (二进制，未解码)")
    else:
        print("\n载荷: 无（纯 SYN，常见）")

    print("\n--- 小结 ---")
    print("同一串字节，不同层「只读自己的头」。路由器主要看 IPv4；")
    print("目的主机的内核根据「协议=TCP」把剩余部分交给 TCP，再按端口交给应用。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
