---
name: dns
description: DNS 配置与排查
version: 1.0.0
author: terminal-skills
tags: [networking, dns, bind, coredns, resolution]
---

# DNS 配置与排查

## 概述
DNS 配置、解析排查、BIND/CoreDNS 等技能。

## DNS 查询工具

### dig
```bash
# 基础查询
dig example.com
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
dig example.com ANY

# 简短输出
dig +short example.com

# 指定 DNS 服务器
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# 追踪解析过程
dig +trace example.com

# 反向解析
dig -x 8.8.8.8

# 查询特定记录
dig example.com SOA
dig example.com CNAME

# 禁用递归
dig +norecurse example.com
```

### nslookup
```bash
# 基础查询
nslookup example.com
nslookup example.com 8.8.8.8

# 查询特定类型
nslookup -type=mx example.com
nslookup -type=ns example.com
nslookup -type=txt example.com

# 反向解析
nslookup 8.8.8.8
```

### host
```bash
# 基础查询
host example.com
host -t mx example.com
host -t ns example.com

# 反向解析
host 8.8.8.8

# 详细输出
host -v example.com
```

## 本地 DNS 配置

### /etc/resolv.conf
```bash
# 查看配置
cat /etc/resolv.conf

# 配置示例
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com
options timeout:2 attempts:3

# 临时修改（可能被覆盖）
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

### /etc/hosts
```bash
# 查看
cat /etc/hosts

# 添加记录
echo "192.168.1.100 myserver.local" >> /etc/hosts

# 格式
127.0.0.1       localhost
192.168.1.100   myserver myserver.local
```

### systemd-resolved
```bash
# 查看状态
systemd-resolve --status
resolvectl status

# 查询
resolvectl query example.com

# 刷新缓存
systemd-resolve --flush-caches
resolvectl flush-caches

# 配置文件
/etc/systemd/resolved.conf
```

## BIND DNS 服务器

### 安装与管理
```bash
# 安装
apt install bind9 bind9utils          # Debian/Ubuntu
yum install bind bind-utils           # CentOS/RHEL

# 服务管理
systemctl start named
systemctl enable named
systemctl status named

# 检查配置
named-checkconf
named-checkzone example.com /etc/bind/zones/db.example.com
```

### 主配置
```bash
# /etc/bind/named.conf.options
options {
    directory "/var/cache/bind";
    
    forwarders {
        8.8.8.8;
        8.8.4.4;
    };
    
    dnssec-validation auto;
    
    listen-on { any; };
    listen-on-v6 { any; };
    
    allow-query { any; };
    allow-recursion { 192.168.0.0/16; 10.0.0.0/8; };
    
    recursion yes;
};
```

### 区域配置
```bash
# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/zones/db.example.com";
    allow-transfer { 192.168.1.2; };
};

zone "1.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.168.1";
};
```

### 区域文件
```bash
# /etc/bind/zones/db.example.com
$TTL    604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                        2024011501      ; Serial
                        604800          ; Refresh
                        86400           ; Retry
                        2419200         ; Expire
                        604800 )        ; Negative Cache TTL

; Name servers
@       IN      NS      ns1.example.com.
@       IN      NS      ns2.example.com.

; A records
@       IN      A       192.168.1.10
ns1     IN      A       192.168.1.1
ns2     IN      A       192.168.1.2
www     IN      A       192.168.1.10
mail    IN      A       192.168.1.20

; CNAME records
ftp     IN      CNAME   www.example.com.

; MX records
@       IN      MX      10 mail.example.com.
```

## CoreDNS

### 配置文件
```bash
# Corefile
.:53 {
    forward . 8.8.8.8 8.8.4.4
    cache 30
    log
    errors
}

example.com:53 {
    file /etc/coredns/db.example.com
    log
    errors
}
```

### Kubernetes CoreDNS
```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
            ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
            max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

## 常见场景

### 场景 1：DNS 解析排查
```bash
# 1. 检查本地配置
cat /etc/resolv.conf

# 2. 测试 DNS 服务器连通性
ping 8.8.8.8

# 3. 查询解析
dig example.com
dig @8.8.8.8 example.com

# 4. 追踪解析路径
dig +trace example.com

# 5. 检查 DNS 缓存
systemd-resolve --statistics
```

### 场景 2：清除 DNS 缓存
```bash
# systemd-resolved
systemd-resolve --flush-caches

# nscd
systemctl restart nscd

# dnsmasq
systemctl restart dnsmasq

# BIND
rndc flush

# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### 场景 3：测试 DNS 性能
```bash
# 使用 dig 测试响应时间
dig example.com | grep "Query time"

# 批量测试
for i in {1..10}; do
    dig +noall +stats example.com | grep "Query time"
done

# 使用 dnsperf
dnsperf -s 8.8.8.8 -d queries.txt
```

### 场景 4：配置内部 DNS
```bash
# 添加内部域名解析
# /etc/hosts
192.168.1.100   app.internal
192.168.1.101   db.internal

# 或配置 dnsmasq
# /etc/dnsmasq.conf
address=/internal/192.168.1.100
server=8.8.8.8
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 解析失败 | 检查 resolv.conf、DNS 服务器 |
| 解析慢 | 检查 DNS 服务器响应、网络延迟 |
| 缓存问题 | 清除本地缓存、检查 TTL |
| 记录不存在 | 检查区域文件、SOA 序列号 |

```bash
# 检查 DNS 端口
ss -ulnp | grep :53
netstat -ulnp | grep :53

# 测试 TCP/UDP
dig +tcp example.com
dig +notcp example.com

# 检查 BIND 日志
tail -f /var/log/named/query.log
journalctl -u named -f
```
