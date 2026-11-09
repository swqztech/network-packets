# -*- coding: utf-8 -*-
"""TLS 记录与握手头解析（教学子集，不解密）。"""

from __future__ import annotations

import re
import struct
from pathlib import Path

CONTENT_TYPES = {
    20: "change_cipher_spec",
    21: "alert",
    22: "handshake",
    23: "application_data",
}

HANDSHAKE_TYPES = {
    1: "client_hello",
    2: "server_hello",
    11: "certificate",
    14: "server_hello_done",
    16: "client_key_exchange",
    20: "finished",
}


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def parse_tls_record(data: bytes, offset: int = 0) -> tuple[dict, int]:
    if len(data) - offset < 5:
        raise ValueError("不足 5 字节 TLS 记录头")
    ctype, ver_major, ver_minor, length = struct.unpack("!BBBH", data[offset : offset + 5])
    version = f"{ver_major}.{ver_minor}"
    end = offset + 5 + length
    if len(data) < end:
        raise ValueError(f"记录声称长度 {length}，但缓冲区不足")
    payload = data[offset + 5 : end]
    info: dict = {
        "content_type": ctype,
        "content_name": CONTENT_TYPES.get(ctype, f"type_{ctype}"),
        "record_version": version,
        "length": length,
        "payload": payload,
    }
    if ctype == 22 and len(payload) >= 4:
        htype = payload[0]
        hlen = int.from_bytes(payload[1:4], "big")
        info["handshake_type"] = htype
        info["handshake_name"] = HANDSHAKE_TYPES.get(htype, f"hs_{htype}")
        info["handshake_length"] = hlen
        if htype == 1 and len(payload) >= 34:
            # ClientHello: 跳过 handshake 头 + client_version(2) + random(32)
            body = payload[4:]
            if len(body) >= 34:
                sess = body[34]
                pos = 35 + sess
                if len(body) > pos + 1:
                    cs_len = struct.unpack("!H", body[pos : pos + 2])[0]
                    pos += 2 + cs_len + 1  # 压缩方法
                    if len(body) > pos + 1:
                        ext_len = struct.unpack("!H", body[pos : pos + 2])[0]
                        info["extensions_total_len"] = ext_len
                        info["sni_hostname"] = _extract_sni(body[pos + 2 : pos + 2 + ext_len])
    return info, end


def _extract_sni(ext_block: bytes) -> str | None:
    """从扩展区粗略查找 type=0 server_name（不保证覆盖所有格式）。"""
    i = 0
    while i + 4 <= len(ext_block):
        etype, elen = struct.unpack("!HH", ext_block[i : i + 4])
        i += 4
        val = ext_block[i : i + elen]
        i += elen
        if etype != 0:  # server_name
            continue
        if len(val) < 5:
            continue
        # server_name_list: list_len(2), name_type(1), host_len(2), host
        name_len = struct.unpack("!H", val[3:5])[0]
        start = 5
        if len(val) >= start + name_len:
            try:
                return val[start : start + name_len].decode("ascii")
            except UnicodeDecodeError:
                return None
    return None
