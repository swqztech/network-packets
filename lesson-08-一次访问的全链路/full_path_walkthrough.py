#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打印全链路各阶段与对应课时（不联网）。"""

PHASES = [
    ("DNS", "05", "域名 → IP，常为 UDP/53", "dns"),
    ("ARP", "06", "下一跳 IP → MAC", "arp"),
    ("路由/TTL", "02", "每跳减 TTL", "ip"),
    ("TCP", "03", "三次握手，端口 443", "tcp.port==443"),
    ("TLS", "07", "ClientHello、证书、Finished", "tls"),
    ("HTTP", "04", "GET/200；HTTPS 时在 TLS 内", "tls or http"),
    ("ICMP", "05", "旁路诊断 ping，非必选", "icmp"),
]


def main() -> None:
    print("第八课：访问 https://example.com 的典型阶段\n")
    print(f"{'阶段':<8} {'课时':^4}  说明".ljust(50))
    print("-" * 58)
    for name, lesson, desc, flt in PHASES:
        print(f"{name:<8}  {lesson}   {desc}")
        print(f"         过滤器: {flt}\n")
    print("运行 trace_https_visit.py 在本机执行 DNS+TCP+TLS+GET。")


if __name__ == "__main__":
    main()
