# 抓包时间线对照（第八课）

## 一次性实验

1. 选择正在使用的网卡，**Start**。
2. 终端运行：`python trace_https_visit.py`（目标默认 `example.com`）。
3. **Stop** 捕获，按下面顺序点过滤器（显示过滤器栏）。

## 推荐顺序

| 步骤 | 过滤器 | 预期 |
|------|--------|------|
| 1 | `dns.qry.name contains "example"` | UDP 53，查询名 |
| 2 | `arp` | 可能有 Who has 网关（视缓存而定） |
| 3 | `tcp.flags.syn == 1 && tcp.port == 443` | 第一次 SYN |
| 4 | `tls.handshake.type == 1` | ClientHello + SNI |
| 5 | `tls.handshake.type == 2` | ServerHello |
| 6 | `tcp.port == 443 && tls.record.content_type == 23` | 加密应用数据 |

## 统计视图

- **Statistics → Conversations → TCP**：看与 443 的字节数与时长。  
- 右键某包 → **Follow → TCP Stream**：整段流（TLS 期为乱码）。  
- 若配置了解密密钥（进阶），TLS 内可解出 HTTP；本课程不要求。

## 与脚本输出对齐

`trace_https_visit.py` 打印的 `[1/5]…[5/5]` 应能和上表 1～4/6 在时间上对应（ARP 可能不在本次触发）。
