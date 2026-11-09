# 第七课：TLS 在 TCP 里长什么样？

第四课：HTTP 是 **TCP 载荷里的明文**。  
**HTTPS = HTTP + TLS**：握手阶段载荷里仍是结构化但逐渐加密的数据；握手完成后，TCP 里大多是 **看不出语义的密文**（Wireshark 默认解不开）。

本课 **不解密**，只认识：

1. **TLS 记录**（Record）的边框  
2. **握手消息**的类型顺序  
3. 在 Wireshark 里用什么过滤器看「形状」

## 1. 仍是一根 TCP 连接

```
以太网 → IPv4(proto=6) → TCP:443 → [ TLS 记录 … TLS 记录 … ]
```

第三课的三次握手 **先完成**，再在同一个 TCP 流上发 **ClientHello**。

## 2. TLS 记录层（每条记录 5 字节头 + 载荷）

| 字节 | 含义 |
|------|------|
| 1 | **Content Type**：22=握手, 23=应用数据, 20=变更密码规范… |
| 2–3 | 版本（记录层常写 0x0301/0x0303，与真实协议版本不必完全一致） |
| 4–5 | **长度**（后面载荷字节数） |

握手载荷里再走一层：**握手类型**（1=ClientHello, 2=ServerHello, 11=Certificate…）。

`parse_tls_sample.py` 读样本十六进制，打印记录与 ClientHello。

## 3. 典型 HTTPS 握手（简化）

```
客户端                          服务端
  | ClientHello  (支持的套件、SNI 域名) |
  |---------------------------------->|
  |              ServerHello          |
  |              Certificate          |
  |              ServerHelloDone      |
  |<----------------------------------|
  | ClientKeyExchange                 |
  | ChangeCipherSpec                    |
  | Finished                          |
  |---------------------------------->|
  |              ChangeCipherSpec       |
  |              Finished               |
  |<----------------------------------|
  |==== 应用数据（加密的 HTTP）========>|
```

**SNI（Server Name Indication）** 常在 ClientHello 里以 **明文** 出现 → Wireshark 在未解密时仍可能看到 `example.com`。

## 4. Wireshark 提示

| 过滤器 | 用途 |
|--------|------|
| `tcp.port == 443` | 所有 TLS 流量 |
| `tls` | 解析 TLS 记录与握手 |
| `tls.handshake.type == 1` | ClientHello |
| `tls.handshake.type == 2` | ServerHello |
| `ssl.handshake.extensions_server_name` | 看谁访问了哪个域名 |

实验：抓包后访问 `https://example.com`，点第一个 ClientHello 展开 **Server Name**。

## 5. 本课代码

```bash
cd lesson-07-TLS与HTTPS形态
python parse_tls_sample.py
python tls_handshake_walkthrough.py
python tls_live_demo.py
```

`tls_live_demo.py` 用 Python 与真实站点完成 TLS（本机出站 TCP），打印 **协议版本与密码套件**；对照抓包时的 `tls` 过滤器。

## 6. 小测验

1. TLS 记录在 TCP 之上还是之下？  
2. Content Type `23` 通常表示什么阶段？  
3. 为什么第四课 `parse_http_payload.py` 对 HTTPS 站点往往不起作用？

<details>
<summary>参考答案</summary>

1. **之上**（对 TCP 载荷再封装）。  
2. **应用数据**（已加密的 HTTP 等）。  
3. HTTP 被 TLS 加密，TCP 载荷不再是明文 `GET /`。

</details>

## 下一课预告

第八课可做 **综合实验：从 DNS 到 TLS 的一条时间线**（脚本 checklist），或 **NAT 如何改地址端口**。
