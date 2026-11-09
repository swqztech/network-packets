#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 ICMP Echo 请求/应答样本。"""

from pathlib import Path

from icmp_lib import load_hex, parse_icmp


def show(name: str, path: Path) -> None:
    info = parse_icmp(load_hex(path))
    ok = info["checksum"] == info["checksum_recalc"]
    print(f"\n=== {name} ===")
    print(f"  类型: {info['type']} ({info['type_name']})  代码: {info['code']}")
    print(
        f"  校验和: 0x{info['checksum']:04x} "
        f"(重算 0x{info['checksum_recalc']:04x}, {'通过' if ok else '失败'})"
    )
    print(f"  标识符: 0x{info['identifier']:04x}  序号: {info['sequence']}")
    try:
        print(f"  数据: {info['payload'].decode('ascii')!r}")
    except UnicodeDecodeError:
        print(f"  数据(hex): {info['payload'].hex()}")


def main() -> None:
    base = Path(__file__).resolve().parent / "samples"
    print("ICMP 装在 IP 协议号=1 的载荷里，没有端口号。")
    show("Echo Request (ping 发出)", base / "icmp_echo_request.hex")
    show("Echo Reply (ping 收回)", base / "icmp_echo_reply.hex")
    print("\n--- 对照 Wireshark ---")
    print("展开 ICMP 面板时，字段应与本输出一致。")


if __name__ == "__main__":
    main()
