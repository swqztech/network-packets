# 第五课：ICMP、ping 与抓包实战

第二课讲过 **TTL** 每跳减 1；到了 0 时路由器会丢弃并发 **ICMP Time Exceeded**——`tracert`/`traceroute` 靠的是另一类 ICMP。本课先搞清最常见的 **Echo（ping）**，再给一份 **Wireshark 跟包清单**，把前四课串成一条线。

## 1. ICMP 在哪一层？

ICMP 不是「第四层传输」，通常归类为 **IP 的伴随协议**：

- IPv4 头里 `protocol = 1` 表示里面是 **ICMP**
- ICMP 自己的头 + 载荷，再套在 IP 包里（无 TCP/UDP 端口）

```
[以太网][ IPv4  proto=1 ][ ICMP 头 ][ 可选数据 ]
```

| type (类型) | 常见含义 |
|-------------|----------|
| 0 | Echo Reply（ping 回声） |
| 8 | Echo Request（ping 请求） |
| 3 | Destination Unreachable |
| 11 | Time Exceeded（TTL 用尽，traceroute 用） |

## 2. Echo / ping 在干什么？

**ping** 发 type **8**（Echo Request），目标若可达且允许 ICMP，则回 type **0**（Echo Reply），**回包里 TTL 由对方系统决定**，载荷常常把请求里的数据原样捎回。

```
你:  Echo Request  id=?, seq=1, data="abc..."
对方: Echo Reply    id=?, seq=1, data="abc..."
```

RTT（往返时延）= 本机从发到收的时间差；**丢包** = 超时没等到 Reply。

本机跑 `run_ping.py` 会调用系统 `ping` 并解读输出；`parse_icmp.py` 用十六进制样本拆 ICMP 字段（不依赖管理员权限）。

## 3. 与 TTL 的关系

- **路径上**：每个路由器转发 IP 包时 **TTL−1**（第二课）。
- **ping 成功**：说明往返路径上的节点至少把 Echo 送到了目标并带回答复。
- **traceroute 思想**：发 TTL=1,2,3…，在第 n 跳收到 **Time Exceeded** 就知道第 n 台路由器地址（细节因 OS/工具而异）。

## 4. Wireshark 实战清单（跟一次「打开网页」）

在网卡上抓包时（选正在上网的那块网卡），建议按阶段过滤：

| 阶段 | 显示过滤器（Wireshark） | 你在找什么 |
|------|-------------------------|------------|
| DNS | `dns` 或 `udp.port == 53` | UDP 53 上的查询/响应（第三课） |
| 建连 | `tcp.flags.syn == 1 && tcp.flags.ack == 0` | 第一次 SYN（第三课） |
| 传输 | `tcp.port == 443` | TLS 密文仍在 **TCP 载荷**（第四课） |
| 旁路 | `icmp` | ping、不可达等 |
| 综合 | `ip.addr == 目标IP` | 某主机的所有 IP 流量 |

**操作步骤建议：**

1. 开始捕获 → 浏览器访问 `http://example.com`（明文 HTTP 便于看第四课；HTTPS 只能看到 TLS 握手形状）。  
2. 停止 → 先 `dns`，点开一个 **Query**，看 UDP 里问的是什么名字。  
3. 用解析出的 A 记录 IP 过滤：`ip.addr == x.x.x.x`。  
4. 找 **TCP 三次握手**（SYN → SYN,ACK → ACK）。  
5. 展开 **IPv4**，对照第二课：TTL、DF、校验和。  
6. 另开终端 `ping` 同一 IP，过滤器改 `icmp`，对照本课样本。

详细可复制过滤器见 `WIRESHARK_LAB.md`。

## 5. 本课代码

```bash
cd lesson-05-ICMP与抓包实战
python parse_icmp.py
python run_ping.py
python dns_query_demo.py
```

`dns_query_demo.py` 向系统解析器发一次 UDP DNS 查询（需联网）；控制台会提示你在 Wireshark 里用 `dns` 过滤对照。

## 6. 小测验

1. ping 使用的 ICMP 类型号分别是？（请求 / 应答）  
2. IPv4 协议字段值为 1 表示什么？  
3. 为什么在 Wireshark 里看 HTTPS 网站时常看不到 `GET /` 明文？

<details>
<summary>参考答案</summary>

1. 8 / 0。  
2. ICMP。  
3. TLS 在 TCP 之上加密，HTTP 在 TLS 里面。

</details>

## 下一课预告

第六课可走 **ARP（IP 如何找到 MAC）**，或 **TLS 握手在 TCP 流里占哪几段**（不解密只看形状）。
