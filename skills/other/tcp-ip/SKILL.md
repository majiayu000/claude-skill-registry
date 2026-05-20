---
name: tcp-ip
description: TCP/IP 网络诊断与排查
version: 1.0.0
author: terminal-skills
tags: [networking, tcp, ip, diagnosis]
---

# TCP/IP 网络诊断

## 概述
TCP/IP 协议栈相关的网络诊断、连通性测试、端口排查等技能。

## 连通性测试

```bash
# Ping 测试
ping -c 4 hostname
ping -i 0.2 hostname              # 间隔 0.2 秒

# 路由追踪
traceroute hostname
traceroute -n hostname            # 不解析域名
mtr hostname                      # 实时追踪

# 端口连通性
telnet hostname 80
nc -zv hostname 80
nc -zv hostname 80-100            # 端口范围
```

## 网络配置

```bash
# 查看网络接口
ip addr
ip link show
ifconfig                          # 传统命令

# 查看路由表
ip route
route -n
netstat -rn

# 查看 ARP 表
ip neigh
arp -a

# DNS 查询
nslookup hostname
dig hostname
dig +short hostname
host hostname
```

## 端口与连接

```bash
# 查看监听端口
ss -tlnp                          # TCP 监听
ss -ulnp                          # UDP 监听
netstat -tlnp

# 查看所有连接
ss -tanp
netstat -anp

# 查看特定端口
ss -tlnp | grep :80
lsof -i :80

# 连接统计
ss -s
netstat -s
```

## 抓包分析

```bash
# tcpdump 基础
tcpdump -i eth0
tcpdump -i any port 80
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 -w capture.pcap

# 常用过滤
tcpdump -i eth0 'tcp port 80'
tcpdump -i eth0 'host 10.0.0.1 and port 443'
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# 读取抓包文件
tcpdump -r capture.pcap
tcpdump -r capture.pcap -A        # 显示 ASCII
```

## 常见场景

### 场景 1：排查网络不通
```bash
# 1. 检查本地网络
ip addr
ip route

# 2. 测试网关连通性
ping gateway_ip

# 3. 测试目标连通性
ping target_ip
traceroute target_ip

# 4. 检查 DNS
nslookup target_hostname
```

### 场景 2：排查端口不通
```bash
# 1. 检查服务是否监听
ss -tlnp | grep :port

# 2. 检查防火墙
iptables -L -n
firewall-cmd --list-all

# 3. 从远程测试
nc -zv target_ip port
```

### 场景 3：排查连接超时
```bash
# 1. 检查网络延迟
ping -c 10 target

# 2. 检查路由
mtr target

# 3. 抓包分析
tcpdump -i eth0 host target -w debug.pcap
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 网络不通 | `ping`, `traceroute`, 检查路由 |
| DNS 解析失败 | `nslookup`, `dig`, 检查 /etc/resolv.conf |
| 端口不通 | `ss -tlnp`, 检查防火墙 |
| 连接超时 | `mtr`, `tcpdump` 抓包分析 |
| 连接被拒绝 | 检查服务状态、端口监听 |
