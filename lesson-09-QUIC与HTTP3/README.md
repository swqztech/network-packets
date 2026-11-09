# 第九课：QUIC 与 HTTP/3 入门

第八课路径：`TCP + TLS + HTTP/1.1`。  
越来越多站点用 **HTTP/3** = **HTTP 语义 + QUIC 传输**；QUIC 多半跑在 **UDP 443** 上（不再用 TCP 传 TLS）。

## 1. 和「老 HTTPS」比什么变了？

| | HTTPS 经典 | HTTP/3 |
|---|-----------|--------|
| 传输 | TCP（第三课） | **UDP** 上的 QUIC |
| 加密 | TLS 在 TCP 之上（第七课） | **集成在 QUIC** 里（1-RTT/0-RTT 握手） |
| 端口 | TCP 443 | 通常 **UDP 443** |
| 连接 | 四元组 + TCP 状态 | **Connection ID**，换网有时可保持 |
| 丢包 | TCP 重传可能阻塞整个连接 | 独立流（简化理解：多路更友好） |

**不变**：外面仍有 IP、以太网、ARP、NAT；DNS 仍常用来拿 A/AAAA。

## 2. QUIC 包头（长包头 · Initial，初识）

长包头第一个字节高位为 `1`；含 **版本号**、**目的/源 Connection ID**（便于 NAT 后仍认出连接）。

本课 `parse_quic_long_header.py` 解析样本前几字段（不解密内部 TLS 1.3）。

## 3. 浏览器怎么选 HTTP/3？

常先用 HTTP/2 或 HTTP/1.1，通过 **Alt-Svc** 头获知「同一主机支持 `h3`」，再改用 QUIC。抓包时可能先看到 **TCP TLS**，随后才出现 **UDP QUIC**。

## 4. Wireshark

- 需较新版本并启用 QUIC 解析。  
- 过滤器：`udp.port == 443 and quic`  
- 仍可能无法看到 HTTP 明文（加密与第七课类似）。

## 5. 本课代码

```bash
cd lesson-09-QUIC与HTTP3
python compare_stacks.py
python parse_quic_long_header.py
python alt_svc_probe.py
```

`alt_svc_probe.py` 用 **TCP HTTPS** 请求 `cloudflare.com`，打印响应头里是否含 `Alt-Svc`（需联网）。

## 6. 小测验

1. HTTP/3 默认基于 TCP 还是 UDP？  
2. 为何抓包里 QUIC 与 TCP 443 可能同时出现？  
3. ARP 对 QUIC 还重要吗？

<details>
<summary>参考答案</summary>

1. **UDP**（QUIC）。  
2. 首次访问或协商 Alt-Svc 时仍可能用 TCP HTTPS。  
3. 重要；仍以 **IP 下一跳 + MAC** 发送 UDP 帧（第六课）。

</details>
