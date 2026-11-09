#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 TCP 载荷里的 HTTP GET 拆开给人看。"""

from pathlib import Path

from http_parse_lib import load_hex, parse_http_request


def main() -> None:
    path = Path(__file__).resolve().parent / "samples" / "http_get.hex"
    payload = load_hex(path)

    print("=== 原始载荷（逻辑上在 TCP 字节流里）===")
    print(payload.decode("ascii"))
    print("---")

    req = parse_http_request(payload)
    print(f"方法: {req['method']}")
    print(f"路径: {req['path']}")
    print(f"版本: {req['version']}")
    print(f"Host: {req['headers'].get('host', '(无)')}")
    print("头字段:")
    for k, v in req["headers"].items():
        print(f"  {k}: {v}")
    print(f"body 长度: {len(req['body'])} 字节")
    print("\n提示: 真实 HTTPS 里这段会先被 TLS 加密，Wireshark 里默认看不到明文 HTTP。")


if __name__ == "__main__":
    main()
