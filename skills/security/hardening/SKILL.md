---
name: hardening
description: 系统加固
version: 1.0.0
author: terminal-skills
tags: [security, hardening, cis, baseline, sysctl]
---

# 系统加固

## 概述
系统加固、基线配置、CIS 标准技能。

## SSH 加固

### 配置优化
```bash
# /etc/ssh/sshd_config
# 禁用 root 登录
PermitRootLogin no

# 禁用密码认证
PasswordAuthentication no
PubkeyAuthentication yes

# 限制用户
AllowUsers admin deploy
AllowGroups sshusers

# 修改端口
Port 2222

# 超时设置
ClientAliveInterval 300
ClientAliveCountMax 2

# 禁用空密码
PermitEmptyPasswords no

# 协议版本
Protocol 2

# 日志级别
LogLevel VERBOSE
```

### 应用配置
```bash
# 检查配置
sshd -t

# 重启服务
systemctl restart sshd
```

## 内核参数加固

### sysctl 配置
```bash
# /etc/sysctl.d/99-security.conf

# 禁用 IP 转发
net.ipv4.ip_forward = 0

# 禁用 ICMP 重定向
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# 启用 SYN Cookie
net.ipv4.tcp_syncookies = 1

# 忽略 ICMP 广播
net.ipv4.icmp_echo_ignore_broadcasts = 1

# 禁用源路由
net.ipv4.conf.all.accept_source_route = 0

# 启用反向路径过滤
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# 记录可疑包
net.ipv4.conf.all.log_martians = 1

# 禁用 IPv6（如不需要）
net.ipv6.conf.all.disable_ipv6 = 1
```

### 应用配置
```bash
sysctl -p /etc/sysctl.d/99-security.conf
```

## 用户安全

### 密码策略
```bash
# /etc/login.defs
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_MIN_LEN    12
PASS_WARN_AGE   14

# /etc/security/pwquality.conf
minlen = 12
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
```

### 账户锁定
```bash
# /etc/pam.d/common-auth (Debian)
auth required pam_tally2.so deny=5 unlock_time=900

# /etc/pam.d/system-auth (RHEL)
auth required pam_faillock.so preauth deny=5 unlock_time=900
auth required pam_faillock.so authfail deny=5 unlock_time=900
```

### 清理无用账户
```bash
# 锁定账户
usermod -L username
passwd -l username

# 禁用 shell
usermod -s /sbin/nologin username

# 查找无密码账户
awk -F: '($2 == "") {print $1}' /etc/shadow
```

## 文件权限

### 关键文件
```bash
# 设置权限
chmod 600 /etc/shadow
chmod 644 /etc/passwd
chmod 600 /etc/gshadow
chmod 644 /etc/group
chmod 700 /root
chmod 600 /boot/grub/grub.cfg

# 设置属性
chattr +i /etc/passwd
chattr +i /etc/shadow
```

### 查找问题文件
```bash
# 查找 SUID/SGID 文件
find / -perm /4000 -type f 2>/dev/null
find / -perm /2000 -type f 2>/dev/null

# 查找无主文件
find / -nouser -o -nogroup 2>/dev/null

# 查找全局可写文件
find / -perm -002 -type f 2>/dev/null
```

## 服务加固

### 禁用不必要服务
```bash
# 查看服务
systemctl list-unit-files --type=service

# 禁用服务
systemctl disable telnet
systemctl disable rsh
systemctl disable rlogin
systemctl disable vsftpd

# 停止服务
systemctl stop telnet
```

### 限制 cron
```bash
# 只允许特定用户
echo "root" > /etc/cron.allow
chmod 600 /etc/cron.allow
rm -f /etc/cron.deny
```

## 常见场景

### 场景 1：快速加固脚本
```bash
#!/bin/bash
echo "=== 系统加固 ==="

# SSH 加固
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# 内核参数
cat >> /etc/sysctl.d/99-security.conf << EOF
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.rp_filter = 1
EOF
sysctl -p /etc/sysctl.d/99-security.conf

# 文件权限
chmod 600 /etc/shadow
chmod 644 /etc/passwd

echo "加固完成"
```

### 场景 2：CIS 基线检查
```bash
#!/bin/bash
echo "=== CIS 基线检查 ==="

# 检查 SSH 配置
echo "SSH PermitRootLogin:"
grep "^PermitRootLogin" /etc/ssh/sshd_config

# 检查密码策略
echo "密码最大有效期:"
grep "^PASS_MAX_DAYS" /etc/login.defs

# 检查内核参数
echo "TCP SYN Cookie:"
sysctl net.ipv4.tcp_syncookies
```

## 加固检查清单

| 项目 | 检查内容 |
|------|----------|
| SSH | 禁用 root、密钥认证 |
| 密码 | 复杂度、有效期 |
| 内核 | sysctl 安全参数 |
| 服务 | 禁用不必要服务 |
| 权限 | 关键文件权限 |
| 日志 | 审计日志启用 |

## 故障排查

```bash
# SSH 无法登录
journalctl -u sshd -f
tail -f /var/log/auth.log

# 检查 PAM 配置
cat /etc/pam.d/sshd

# 检查 SELinux
getenforce
ausearch -m avc -ts recent
```
