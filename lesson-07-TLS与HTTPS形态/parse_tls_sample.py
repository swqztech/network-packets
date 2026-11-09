#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析样本 TLS ClientHello 记录。"""

from pathlib import Path

from tls_record_lib import load_hex, parse_tls_record


def main() -> None:
    path = Path(__file__).resolve().parent / "samples" / "tls_client_hello.hex"
    data = load_hex(path)
    rec, _ = parse_tls_record(data, 0)

    print("=== TLS 记录 ===")
    print(f"  Content Type: {rec['content_type']} ({rec['content_name']})")
    print(f"  记录版本: {rec['record_version']}")
    print(f"  载荷长度: {rec['length']} 字节")
    print("\n=== 握手 ===")
    print(f"  类型: {rec.get('handshake_type')} ({rec.get('handshake_name')})")
    print(f"  握手体长度: {rec.get('handshake_length')}")
    if rec.get("sni_hostname"):
        print(f"  SNI 域名: {rec['sni_hostname']}")
    print("\n这在 TCP 443 的 PSH 段里；Wireshark: tls.handshake.type == 1")
    print("握手完成后 content_type=23 的 application_data 才是加密的 HTTP。")


if __name__ == "__main__":
    main()
