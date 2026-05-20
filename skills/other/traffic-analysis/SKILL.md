---
name: traffic-analysis
description: 流量分析与抓包
version: 1.0.0
author: terminal-skills
tags: [networking, tcpdump, wireshark, packet-capture, traffic]
---

# 流量分析与抓包

## 概述
tcpdump、Wireshark、流量分析与网络诊断技能。

## tcpdump

### 基础用法
```bash
# 监听所有接口
tcpdump -i any

# 指定接口
tcpdump -i eth0

# 详细输出
tcpdump -v
tcpdump -vv
tcpdump -vvv

# 显示 ASCII
tcpdump -A

# 显示十六进制
tcpdump -X
tcpdump -XX

# 不解析主机名
tcpdump -n

# 不解析端口名
tcpdump -nn
```

### 过滤表达式
```bash
# 主机过滤
tcpdump host 192.168.1.100
tcpdump src host 192.168.1.100
tcpdump dst host 192.168.1.100

# 网段过滤
tcpdump net 192.168.1.0/24

# 端口过滤
tcpdump port 80
tcpdump src port 80
tcpdump dst port 443
tcpdump portrange 8000-9000

# 协议过滤
tcpdump tcp
tcpdump udp
tcpdump icmp
tcpdump arp

# 组合过滤
tcpdump 'host 192.168.1.100 and port 80'
tcpdump 'src 192.168.1.100 and dst port 443'
tcpdump 'tcp and (port 80 or port 443)'
tcpdump 'not port 22'
```

### 保存与读取
```bash
# 保存到文件
tcpdump -w capture.pcap
tcpdump -w capture.pcap -c 1000    # 限制包数

# 读取文件
tcpdump -r capture.pcap
tcpdump -r capture.pcap -nn

# 轮转文件
tcpdump -w capture-%H%M%S.pcap -G 3600    # 每小时
tcpdump -w capture.pcap -C 100            # 每 100MB
```

### 高级过滤
```bash
# TCP 标志
tcpdump 'tcp[tcpflags] & tcp-syn != 0'
tcpdump 'tcp[tcpflags] & tcp-rst != 0'
tcpdump 'tcp[tcpflags] == tcp-syn'

# HTTP 请求
tcpdump -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# DNS 查询
tcpdump -i any 'udp port 53'

# 大包
tcpdump 'greater 1000'
tcpdump 'less 100'
```

## tshark (Wireshark CLI)

### 基础用法
```bash
# 安装
apt install tshark

# 监听
tshark -i eth0

# 指定过滤器
tshark -i eth0 -f "port 80"

# 显示过滤器
tshark -i eth0 -Y "http"
```

### 字段提取
```bash
# 提取特定字段
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# HTTP 请求
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# DNS 查询
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name
```

### 统计分析
```bash
# 协议统计
tshark -r capture.pcap -q -z io,phs

# 会话统计
tshark -r capture.pcap -q -z conv,tcp

# HTTP 统计
tshark -r capture.pcap -q -z http,tree

# 端点统计
tshark -r capture.pcap -q -z endpoints,ip
```

## ngrep

### 基础用法
```bash
# 安装
apt install ngrep

# 搜索内容
ngrep -q 'GET' port 80
ngrep -q 'password' port 80

# 指定接口
ngrep -d eth0 'pattern'

# 忽略大小写
ngrep -qi 'error'
```

## iftop / nethogs

### iftop
```bash
# 安装
apt install iftop

# 基础用法
iftop
iftop -i eth0

# 不解析主机名
iftop -n

# 显示端口
iftop -P

# 过滤
iftop -f "dst port 80"
```

### nethogs
```bash
# 安装
apt install nethogs

# 按进程显示
nethogs
nethogs eth0

# 刷新间隔
nethogs -d 2
```

## 常见场景

### 场景 1：HTTP 流量分析
```bash
# 抓取 HTTP 请求
tcpdump -i any -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# 提取 HTTP 头
tcpdump -i any -A 'tcp port 80' | grep -E "^(GET|POST|HTTP|Host:|Content-)"

# tshark 分析
tshark -i any -Y "http.request" -T fields -e http.host -e http.request.method -e http.request.uri
```

### 场景 2：DNS 问题排查
```bash
# 抓取 DNS
tcpdump -i any -nn port 53

# 详细 DNS 信息
tcpdump -i any -vvv port 53

# tshark DNS 分析
tshark -i any -Y "dns" -T fields -e dns.qry.name -e dns.a
```

### 场景 3：连接问题诊断
```bash
# TCP 握手
tcpdump -i any 'tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) != 0'

# 重传
tcpdump -i any 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack != 0'

# 连接重置
tcpdump -i any 'tcp[tcpflags] & tcp-rst != 0'
```

### 场景 4：带宽分析
```bash
# 实时带宽
iftop -i eth0 -P -n

# 按进程
nethogs eth0

# 统计流量
tcpdump -i eth0 -w - | pv > /dev/null
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 丢包 | 检查 tcpdump 统计、网卡队列 |
| 延迟高 | 分析 RTT、重传 |
| 连接失败 | 检查 SYN/RST 包 |
| 带宽占用 | 使用 iftop/nethogs |

```bash
# 查看丢包
tcpdump -i eth0 -w /dev/null 2>&1 | grep -i drop

# 网卡统计
ethtool -S eth0 | grep -i error
cat /proc/net/dev

# 连接状态
ss -s
netstat -s | grep -i retrans
```
