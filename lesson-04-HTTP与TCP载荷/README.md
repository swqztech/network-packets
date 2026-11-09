# 第四课：HTTP 在 TCP 里长什么样？

前三课：以太网 → IP → TCP。**应用数据**就在 TCP 的 **载荷（payload）** 里。本课以 **HTTP/1.1** 为例：握手完成后，线上传的「网页请求」本质是 **一段 ASCII 文本**。

## 1. 从分层再看一眼

```
[ HTTP 文本：GET / ... ]
        ↑ TCP 把它切成段，加 Seq/Ack（第三课）
        ↑ IP 套上地址（第二课）
        ↑ 以太网套上 MAC（第一课）
```

浏览器不会把「每个字」单独发一个 IP 包；内核会把你的 HTTP 字节 **分段** 进多个 TCP 段，对应用仍表现为 **连续字节流**。

## 2. HTTP/1.1 请求骨架

```http
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: learn/1.0\r\n
Accept: */*\r\n
\r\n
```

| 部分 | 说明 |
|------|------|
| 起始行 | `方法 路径 版本` |
| 头字段 | 多行 `名字: 值`，以 `\r\n` 结尾 |
| 空行 | 单独的 `\r\n` 表示头结束 |
| 主体 | GET 常无 body；POST 可有，需 `Content-Length` 或 chunked |

响应类似：`HTTP/1.1 200 OK\r\n...`

Wireshark 里展开 **Hypertext Transfer Protocol**，看到的正是 TCP 载荷按 HTTP 语法解析的结果。

## 3. 本课代码

| 脚本 | 作用 |
|------|------|
| `parse_http_payload.py` | 读十六进制样本，解析 **方法、路径、Host、头列表** |
| `tcp_echo_demo.py` | 本机 **TCP 回声**：先握手，再发一串字节原样回显（理解「流」） |
| `mini_http_server.py` | 本机极简 HTTP：浏览器或 `http_client_demo.py` 可访问 |

## 4. 怎么运行

```bash
cd lesson-04-HTTP与TCP载荷
python parse_http_payload.py
python tcp_echo_demo.py
python mini_http_server.py
# 另开终端：
python http_client_demo.py
```

`mini_http_server.py` 默认 `http://127.0.0.1:18080/` 。

## 5. 小测验

1. HTTP 头与 body 之间用什么分隔？  
2. HTTPS 的 TLS 记录在哪个层的载荷里？  
3. 为什么抓包里有时一个 HTTP 请求对应多个 TCP 段？

<details>
<summary>参考答案</summary>

1. 空行（`\r\n\r\n`）。  
2. 仍在 **TCP 载荷** 里（TLS 介于 HTTP 与 TCP 之间，对 IP 仍是 TCP 协议号 6）。  
3. TCP 按 MSS/缓冲区拆分；HTTP 是逻辑报文，物理上可多段传输。

</details>

## 下一课预告

第五课可做 **抓包实战清单**（Wireshark 过滤表达式、跟一次 DNS+TCP+HTTP），或 **ICMP / ping 与第二课 TTL** 串联。
