---
name: firewall
description: 防火墙配置
version: 1.0.0
author: terminal-skills
tags: [security, firewall, iptables, firewalld, nftables, ufw]
---

# 防火墙配置

## 概述
iptables、firewalld、nftables、ufw 防火墙配置技能。

## iptables

### 基础命令
```bash
# 查看规则
iptables -L -n -v
iptables -L -n --line-numbers
iptables -t nat -L -n -v

# 清空规则
iptables -F
iptables -X
iptables -t nat -F

# 默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```

### 常用规则
```bash
# 允许回环
iptables -A INPUT -i lo -j ACCEPT

# 允许已建立连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允许 SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许 HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 允许特定 IP
iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# 允许网段
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 3306 -j ACCEPT

# 拒绝其他
iptables -A INPUT -j DROP
```

### 删除规则
```bash
# 按行号删除
iptables -D INPUT 3

# 按规则删除
iptables -D INPUT -p tcp --dport 80 -j ACCEPT
```

### NAT 配置
```bash
# 开启转发
echo 1 > /proc/sys/net/ipv4/ip_forward

# SNAT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT 端口转发
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to 192.168.1.10:80
iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 80 -j ACCEPT
```

### 保存规则
```bash
# Debian/Ubuntu
iptables-save > /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4

# CentOS/RHEL
service iptables save
```

## firewalld

### 基础命令
```bash
# 状态
systemctl status firewalld
firewall-cmd --state

# 重载
firewall-cmd --reload

# 查看区域
firewall-cmd --get-zones
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones
```

### 服务管理
```bash
# 查看服务
firewall-cmd --list-services
firewall-cmd --get-services

# 添加服务
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent

# 删除服务
firewall-cmd --remove-service=http --permanent
```

### 端口管理
```bash
# 查看端口
firewall-cmd --list-ports

# 添加端口
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --add-port=5000-5100/tcp --permanent

# 删除端口
firewall-cmd --remove-port=8080/tcp --permanent
```

### 富规则
```bash
# 允许特定 IP
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.100" accept' --permanent

# 允许网段访问端口
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="3306" protocol="tcp" accept' --permanent

# 拒绝 IP
firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.100" reject' --permanent
```

## ufw (Ubuntu)

### 基础命令
```bash
# 启用/禁用
ufw enable
ufw disable

# 状态
ufw status
ufw status verbose
ufw status numbered
```

### 规则管理
```bash
# 允许端口
ufw allow 22
ufw allow 80/tcp
ufw allow 443/tcp

# 允许服务
ufw allow ssh
ufw allow http

# 允许 IP
ufw allow from 192.168.1.100

# 允许网段到端口
ufw allow from 192.168.1.0/24 to any port 3306

# 拒绝
ufw deny 23

# 删除规则
ufw delete allow 80
ufw delete 3
```

### 默认策略
```bash
ufw default deny incoming
ufw default allow outgoing
```

## 常见场景

### 场景 1：Web 服务器
```bash
# iptables
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -j DROP

# firewalld
firewall-cmd --add-service=ssh --permanent
firewall-cmd --add-service=http --permanent
firewall-cmd --add-service=https --permanent
firewall-cmd --reload
```

### 场景 2：数据库服务器
```bash
# 只允许应用服务器访问
iptables -A INPUT -s 192.168.1.10 -p tcp --dport 3306 -j ACCEPT
iptables -A INPUT -s 192.168.1.11 -p tcp --dport 3306 -j ACCEPT
iptables -A INPUT -p tcp --dport 3306 -j DROP
```

### 场景 3：限速防护
```bash
# 限制 SSH 连接频率
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接被拒 | 检查规则顺序、默认策略 |
| 规则不生效 | 检查 --permanent、reload |
| NAT 不工作 | 检查 ip_forward、FORWARD 链 |

```bash
# 查看计数
iptables -L -n -v

# 日志
iptables -A INPUT -j LOG --log-prefix "IPT_DROP: "
tail -f /var/log/messages | grep IPT_DROP

# 连接跟踪
conntrack -L
```
