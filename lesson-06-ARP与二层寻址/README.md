# 第六课：ARP —— IP 怎么找到 MAC？

第一课：同一网段用 **MAC** 送帧。第二课：**目的 IP** 决定往哪转发。  
若下一跳 IP 就在本网段，必须知道「这个 IP 对应哪块网卡的 MAC」——**ARP（Address Resolution Protocol）** 干的就是这件事。

## 1. 什么时候需要 ARP？

```
你要发 IP 包给 192.168.1.1（通常是网关）
  → 路由表说：走本网段，直接二层投递
  → 但以太网头要写「目的 MAC」
  → 若缓存里没有，先发 ARP 问：谁有 192.168.1.1？
```

- **跨路由器** 的远目标：先 ARP **默认网关**，IP 包头里的目的地址仍是最终网站 IP，**目的 MAC 往往是网关的 MAC**（第一课/第二课的衔接点）。

## 2. ARP 包长什么样？

挂在以太网类型 **0x0806** 后面（不是 0x0800 IPv4）：

| 字段 | 含义 |
|------|------|
| 硬件类型 | 1 = 以太网 |
| 协议类型 | 0x0800 = IPv4 |
| 操作码 | **1 请求**、**2 应答** |
| 发送方 MAC / IP | 问的人 |
| 目标 MAC / IP | 被问的人（请求里 MAC 常为全 0） |

**请求**常 **广播**（`ff:ff:ff:ff:ff:ff`）；**应答**单播给询问者。

`parse_arp.py` 会解析本课样本。

## 3. ARP 缓存

系统把「IP → MAC」记在 **ARP 表** 里，过一阵会过期，以免网卡换了人不知道。

运行 `show_arp_table.py` 查看当前缓存（Windows：`arp -a`）。

## 4. Wireshark 怎么看？

```
arp
```

访问本网段设备或刚 ping 网关时，常能看到 **Who has … ? Tell …** 与 **… is at …**。

与第五课组合练习：先 `icmp` ping 本网段 IP，再 `arp` 看解析过程。

## 5. 本课代码

```bash
cd lesson-06-ARP与二层寻址
python parse_arp.py
python arp_walkthrough.py
python show_arp_table.py
```

`arp_walkthrough.py` 用文字重演「要发 IP 包 → 查 ARP 缓存未命中 → 广播请求 → 单播应答 → 写入缓存 → 封装以太网帧」。

## 6. IPv6 呢？

IPv6 用 **NDP（邻居发现）** 取代 ARP，挂在 ICMPv6 上；思路仍是「IP → 链路层地址」，本课先吃透 ARP 即可。

## 7. 小测验

1. ARP 在以太网里的类型字段值是？  
2. 发往公网 IP 的帧，目的 MAC 通常是谁？  
3. ARP 应答是广播还是单播？

<details>
<summary>参考答案</summary>

1. `0x0806`。  
2. 默认**网关**的 MAC（下一跳），不是公网 IP 对应的 MAC。  
3. **单播**给当初发问的那台主机。

</details>

## 下一课预告

第七课：**TLS 握手在 TCP 流里长什么样**（只看长度与方向，不解密），与第四课 HTTPS 衔接。
