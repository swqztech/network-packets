#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简「最长前缀匹配」+ TTL 递减，帮助理解路由转发与 TTL。
不模拟 MAC，只玩 IP 层决策。
"""

from __future__ import annotations

import ipaddress


# 路由表项：(前缀, 下一跳名称)
ROUTES = [
    (ipaddress.ip_network("10.0.0.0/8"), "网关-内网"),
    (ipaddress.ip_network("93.184.216.0/24"), "对等-运营商"),
    (ipaddress.ip_network("0.0.0.0/0"), "默认-上游"),
]

HOPS = ["本机", "路由器 R1", "路由器 R2", "路由器 R3", "目的网相邻路由器"]


def lookup(dst: ipaddress.IPv4Address) -> str:
    best: tuple[int, str] | None = None
    for net, nh in ROUTES:
        if dst in net:
            plen = net.prefixlen
            if best is None or plen > best[0]:
                best = (plen, nh)
    return best[1] if best else "丢弃(无路由)"


def simulate(dst_ip: str, start_ttl: int = 64) -> None:
    dst = ipaddress.IPv4Address(dst_ip)
    ttl = start_ttl
    print(f"目的 IP: {dst}")
    print(f"初始 TTL: {ttl}")
    print(f"查表结果: {lookup(dst)}\n")

    for hop in HOPS:
        if ttl <= 0:
            print(f"[{hop}] TTL 已为 0，包丢弃（可发 ICMP Time Exceeded）")
            break
        nh = lookup(dst) if hop != HOPS[-1] else "交付主机"
        print(f"[{hop}] 转发前 TTL={ttl} → 查表 → 下一跳: {nh}")
        ttl -= 1
        if hop == HOPS[-1]:
            print(f"[{hop}] TTL={ttl}，交付给内核网络栈")
            break


def main() -> None:
    print("--- 访问公网示例（example.com 常用网段）---\n")
    simulate("93.184.216.34")
    print("\n--- 访问私网地址 ---\n")
    simulate("10.20.30.40", start_ttl=32)


if __name__ == "__main__":
    main()
