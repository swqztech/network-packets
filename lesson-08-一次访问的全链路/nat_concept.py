#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SNAT 表格式演示：理解家用路由器改写源地址/端口。"""

TABLE = [
    ("192.168.1.100", 52340, "93.184.216.34", 443),
    ("192.168.1.101", 52341, "93.184.216.34", 443),
]

PUBLIC_IP = "203.0.113.50"


def main() -> None:
    print("NAT 概念（出站 SNAT）\n")
    print("内网真实五元组 → 路由器翻译 → 公网可见五元组\n")
    print(f"{'内网 IP':<16} {'内网端口':<8} {'外网 IP':<16} {'外网端口':<8} 目的")
    print("-" * 70)
    for lip, lport, dip, dport in TABLE:
        map_port = 40000 + (lport % 1000)
        print(
            f"{lip:<16} {lport:<8} {PUBLIC_IP:<16} {map_port:<8} "
            f"{dip}:{dport}"
        )
    print(
        "\n回程包目的为 203.0.113.50:400xx 时，路由器查表还原为内网主机。"
    )
    print("抓包: 在 PC 网卡看到源 192.168.x；在运营商侧可能看到 203.0.113.50。")


if __name__ == "__main__":
    main()
