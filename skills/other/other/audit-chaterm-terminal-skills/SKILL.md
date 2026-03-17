---
name: audit
description: 安全审计
version: 1.0.0
author: terminal-skills
tags: [security, audit, auditd, logging, compliance, vulnerability]
---

# 安全审计

## 概述
安全审计、漏洞扫描、合规检查技能。

## auditd 审计系统

### 安装与管理
```bash
# 安装
apt install auditd audispd-plugins      # Debian/Ubuntu
yum install audit                        # CentOS/RHEL

# 服务管理
systemctl start auditd
systemctl enable auditd
systemctl status auditd
```

### 审计规则
```bash
# 查看规则
auditctl -l

# 添加规则 - 监控文件
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -w /etc/sudoers -p wa -k sudoers_changes

# 监控目录
auditctl -w /etc/ssh/ -p wa -k ssh_config

# 监控系统调用
auditctl -a always,exit -F arch=b64 -S execve -k command_exec

# 监控用户操作
auditctl -a always,exit -F arch=b64 -S open -F auid>=1000 -k user_file_access
```

### 永久规则
```bash
# /etc/audit/rules.d/audit.rules
-w /etc/passwd -p wa -k passwd_changes
-w /etc/shadow -p wa -k shadow_changes
-w /etc/sudoers -p wa -k sudoers_changes
-w /var/log/lastlog -p wa -k logins
-a always,exit -F arch=b64 -S execve -k commands

# 重载规则
augenrules --load
```

### 查看日志
```bash
# 搜索审计日志
ausearch -k passwd_changes
ausearch -k commands -ts today
ausearch -ua root -ts recent

# 生成报告
aureport
aureport --summary
aureport --login
aureport --file
aureport --executable
```

## 日志审计

### 系统日志
```bash
# 查看认证日志
tail -f /var/log/auth.log          # Debian/Ubuntu
tail -f /var/log/secure            # CentOS/RHEL

# 查看登录记录
last
lastb                               # 失败登录
lastlog

# journalctl
journalctl -u sshd
journalctl --since "1 hour ago"
journalctl -p err
```

### 日志分析
```bash
# 统计 SSH 登录失败
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# 统计 sudo 使用
grep "sudo:" /var/log/auth.log | tail -20

# 查找异常登录
grep "Accepted" /var/log/auth.log | grep -v "192.168"
```

## 漏洞扫描

### Lynis
```bash
# 安装
apt install lynis

# 系统审计
lynis audit system

# 查看报告
cat /var/log/lynis-report.dat
```

### OpenSCAP
```bash
# 安装
yum install openscap-scanner scap-security-guide

# 扫描
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_standard \
    --results results.xml \
    /usr/share/xml/scap/ssg/content/ssg-centos7-ds.xml

# 生成报告
oscap xccdf generate report results.xml > report.html
```

### Nmap 扫描
```bash
# 端口扫描
nmap -sV -sC target.com

# 漏洞扫描
nmap --script vuln target.com

# 全面扫描
nmap -A -T4 target.com
```

## 文件完整性

### AIDE
```bash
# 安装
apt install aide

# 初始化数据库
aide --init
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# 检查变更
aide --check

# 更新数据库
aide --update
```

### Tripwire
```bash
# 初始化
tripwire --init

# 检查
tripwire --check

# 更新策略
tripwire --update-policy
```

## 常见场景

### 场景 1：监控特权操作
```bash
# /etc/audit/rules.d/privileged.rules
# 监控 sudo
-w /usr/bin/sudo -p x -k privileged_sudo
-w /etc/sudoers -p wa -k sudoers_edit

# 监控用户管理
-w /usr/sbin/useradd -p x -k user_add
-w /usr/sbin/userdel -p x -k user_del
-w /usr/sbin/usermod -p x -k user_mod

# 监控网络配置
-w /etc/hosts -p wa -k hosts_edit
-w /etc/network/ -p wa -k network_config
```

### 场景 2：合规检查脚本
```bash
#!/bin/bash
echo "=== 安全合规检查 ==="

# 检查空密码账户
echo "空密码账户:"
awk -F: '($2 == "") {print $1}' /etc/shadow

# 检查 UID 为 0 的账户
echo "UID=0 账户:"
awk -F: '($3 == 0) {print $1}' /etc/passwd

# 检查 SSH 配置
echo "SSH 配置:"
grep -E "^(PermitRootLogin|PasswordAuthentication)" /etc/ssh/sshd_config

# 检查开放端口
echo "监听端口:"
ss -tlnp
```

### 场景 3：登录告警
```bash
#!/bin/bash
# /etc/profile.d/login-alert.sh
if [ -n "$SSH_CLIENT" ]; then
    IP=$(echo $SSH_CLIENT | awk '{print $1}')
    echo "SSH 登录告警: 用户 $USER 从 $IP 登录 $(hostname)" | \
        mail -s "SSH Login Alert" admin@example.com
fi
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 审计日志过大 | 配置日志轮转、过滤规则 |
| 性能影响 | 减少审计规则、优化过滤 |
| 规则不生效 | 检查语法、重载规则 |

```bash
# 检查 auditd 状态
auditctl -s

# 查看丢失事件
aureport --summary | grep lost

# 日志轮转配置
# /etc/audit/auditd.conf
max_log_file = 50
num_logs = 5
max_log_file_action = ROTATE
```
