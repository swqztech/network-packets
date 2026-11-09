#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文字重演：发 IP 包前如何通过 ARP 拿到 MAC。"""

STEPS = [
    (
        "① 应用要连 93.184.216.34",
        "内核建 IP 包，目的 IP = 公网地址。",
    ),
    (
        "② 查路由表",
        "发现应走默认网关 192.168.1.1（下一跳）。",
    ),
    (
        "③ 查 ARP 缓存",
        "没有 192.168.1.1 → MAC 的条目，需要 ARP。",
    ),
    (
        "④ 发 ARP Request",
        "以太网目的 MAC = ff:ff:ff:ff:ff:ff；问 Who has 192.168.1.1?",
    ),
    (
        "⑤ 收到 ARP Reply",
        "网关单播回应：192.168.1.1 is at aa:bb:cc:dd:ee:ff。",
    ),
    (
        "⑥ 写缓存并发 IP 包",
        "以太网目的 MAC = 网关 MAC；IP 目的仍是 93.184.216.34。",
    ),
]


def main() -> None:
    print("第六课：把第二课的「路由」和第一课的「MAC」接起来\n")
    for title, detail in STEPS:
        print(title)
        print(f"  {detail}\n")
    print("对照: parse_arp.py 的样本即 ④⑤ 的报文形状。")
    print("Wireshark 过滤器: arp")


if __name__ == "__main__":
    main()
