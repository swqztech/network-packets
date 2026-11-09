# -*- coding: utf-8 -*-
"""HTTP/1.x 请求解析（教学用，覆盖常见 GET）。"""

from __future__ import annotations

import re
from pathlib import Path


def load_hex(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return bytes.fromhex(re.sub(r"\s+", "", "".join(lines)))


def parse_http_request(data: bytes) -> dict:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError("样本不是 UTF-8/ASCII 文本 HTTP") from e

    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    if not lines:
        raise ValueError("空请求")

    start = lines[0].split(" ")
    if len(start) < 3:
        raise ValueError(f"起始行格式异常: {lines[0]!r}")

    method, path, version = start[0], start[1], start[2]
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"头字段异常: {line!r}")
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body.encode("utf-8") if body else b"",
        "raw_head_lines": lines,
    }
