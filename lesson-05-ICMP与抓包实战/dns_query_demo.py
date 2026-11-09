#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向系统解析器做一次 UDP DNS 查询（第三课端口 53）。
抓包时 Wireshark 过滤器: dns
"""

import socket


def main() -> None:
    host = "example.com"
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_UDP)
        addrs = sorted({item[4][0] for item in infos})
    except socket.gaierror as e:
        print(f"解析失败: {e}")
        return

    print(f"查询名称: {host}")
    print(f"系统解析结果: {', '.join(addrs)}")
    print("\n若此时正在抓包，在 Wireshark 中:")
    print("  过滤器: dns  或  udp.port == 53")
    print("  可看到 Standard query 与 A/AAAA 应答（UDP 载荷中的 DNS 格式）")


if __name__ == "__main__":
    main()
