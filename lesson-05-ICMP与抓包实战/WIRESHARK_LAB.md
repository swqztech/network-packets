# Wireshark 实验手册（第五课配套）

## 准备

1. 安装 [Wireshark](https://www.wireshark.org/)（Windows 安装时可选 Npcap）。
2. 以普通用户可抓包即可；有的环境需管理员。
3. 本仓库 Python 脚本用于「无抓包时」对照字段；与 Wireshark **同时用** 效果最好。

## 实验 A：ping = ICMP

1. 开始捕获（选正在使用的网卡，如 WLAN / 以太网）。
2. 显示过滤器输入：`icmp`。
3. 命令行：`ping -n 3 8.8.8.8`（Windows）或 `ping -c 3 8.8.8.8`（Linux/macOS）。
4. 点选一个 **Echo (ping) request**：
   - 展开 **Internet Protocol Version 4** → TTL、源/目的 IP。
   - 展开 **Internet Control Message Protocol** → Type `8`，Identifier / Sequence。
5. 紧接着的 **Echo (ping) reply** → Type `0`，对比数据是否相同。

## 实验 B：DNS + TCP（回顾第三、四课）

1. 清空过滤器，重新开始捕获。
2. 浏览器访问 **http://neverssl.com** 或 **http://example.com**（尽量用 HTTP 明文）。
3. 停止后：
   - 过滤器 `dns` → 找到 `Standard query` 的 A/AAAA 记录。
   - 记下解析 IP，过滤器：`ip.addr == <该IP> && tcp`。
4. 在 TCP 流中找：
   - `SYN` / `SYN,ACK` / `ACK`
   - `PSH,ACK` 承载 HTTP 的那几段 → Follow → TCP Stream 可看 GET（第四课）。

## 实验 C：同一页面 HTTPS

1. 访问 `https://example.com`。
2. `tcp.port == 443` → 仍能看到握手与加密集合，**看不到** GET 明文（第四课提示）。
3. 对比实验 B：应用层相同，Wireshark 里「能看到的文本」不同。

## 常用过滤器速查

```
icmp
dns
udp.port == 53
tcp.port == 80 || tcp.port == 443
tcp.flags.syn == 1
ip.addr == 192.168.1.1
http          # 仅明文 HTTP；HTTPS 默认无效
```

## 与本仓库脚本对照

| 脚本 | 对照 Wireshark 看什么 |
|------|------------------------|
| `parse_icmp.py` | ICMP 面板的 Type / Code / Identifier |
| `run_ping.py` | Statistics 里往返时间；包在 `icmp` 过滤器下 |
| `dns_query_demo.py` | `dns` 面板里的查询名与 A 记录 |
