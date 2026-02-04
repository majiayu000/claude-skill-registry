---
name: ssh
description: SSH 管理与安全
version: 1.0.0
author: terminal-skills
tags: [server, ssh, security, key, tunnel]
---

# SSH 管理与安全

## 概述
SSH 密钥管理、跳板机配置、端口转发、安全加固等技能。

## 基础连接

### 连接命令
```bash
# 基础连接
ssh user@hostname
ssh -p 2222 user@hostname           # 指定端口

# 执行远程命令
ssh user@hostname "command"
ssh user@hostname 'ls -la && df -h'

# 详细输出（调试）
ssh -v user@hostname
ssh -vvv user@hostname              # 更详细
```

### 配置文件
```bash
# ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_rsa_myserver

Host dev-*
    User developer
    IdentityFile ~/.ssh/id_rsa_dev

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes

# 使用配置
ssh myserver
```

## 密钥管理

### 生成密钥
```bash
# 生成 RSA 密钥（推荐 4096 位）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 生成 Ed25519 密钥（推荐）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 指定文件名
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_work

# 修改密码
ssh-keygen -p -f ~/.ssh/id_rsa
```

### 部署公钥
```bash
# 方式1：ssh-copy-id
ssh-copy-id user@hostname
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname

# 方式2：手动复制
cat ~/.ssh/id_ed25519.pub | ssh user@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# 方式3：直接编辑
ssh user@hostname
echo "public_key_content" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### SSH Agent
```bash
# 启动 agent
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_rsa
ssh-add -l                          # 列出已添加的密钥

# 转发 agent（跳板机场景）
ssh -A user@jumphost
```

## 端口转发

### 本地转发
```bash
# 将本地端口转发到远程
ssh -L local_port:target_host:target_port user@ssh_server

# 示例：访问远程 MySQL
ssh -L 3306:localhost:3306 user@dbserver
mysql -h 127.0.0.1 -P 3306

# 示例：访问内网服务
ssh -L 8080:internal.server:80 user@jumphost
curl http://localhost:8080
```

### 远程转发
```bash
# 将远程端口转发到本地
ssh -R remote_port:local_host:local_port user@ssh_server

# 示例：暴露本地服务
ssh -R 8080:localhost:3000 user@public_server
# 现在可以通过 public_server:8080 访问本地 3000 端口
```

### 动态转发（SOCKS 代理）
```bash
# 创建 SOCKS5 代理
ssh -D 1080 user@ssh_server

# 使用代理
curl --socks5 localhost:1080 http://example.com
```

### 后台运行
```bash
# 后台运行隧道
ssh -fNL 3306:localhost:3306 user@server

# -f 后台运行
# -N 不执行远程命令
# -L 本地转发
```

## 跳板机配置

### ProxyJump（推荐）
```bash
# 命令行
ssh -J jumphost user@target

# 配置文件
Host target
    HostName 192.168.1.100
    User admin
    ProxyJump jumphost

Host jumphost
    HostName jump.example.com
    User jumper
```

### ProxyCommand
```bash
# 配置文件
Host target
    HostName 192.168.1.100
    User admin
    ProxyCommand ssh -W %h:%p jumphost
```

## 安全加固

### sshd_config 配置
```bash
# /etc/ssh/sshd_config

# 禁用密码登录
PasswordAuthentication no
ChallengeResponseAuthentication no

# 禁用 root 登录
PermitRootLogin no

# 限制用户
AllowUsers admin developer
AllowGroups sshusers

# 修改端口
Port 2222

# 限制登录尝试
MaxAuthTries 3
MaxSessions 5

# 空闲超时
ClientAliveInterval 300
ClientAliveCountMax 2

# 禁用不安全选项
X11Forwarding no
PermitEmptyPasswords no
```

### 应用配置
```bash
# 测试配置
sshd -t

# 重载配置
systemctl reload sshd
```

## 常见场景

### 场景 1：批量执行命令
```bash
# 使用 for 循环
for host in server1 server2 server3; do
    ssh $host "uptime"
done

# 使用 parallel-ssh
pssh -h hosts.txt -i "uptime"
```

### 场景 2：文件传输
```bash
# scp
scp file.txt user@host:/path/
scp -r dir/ user@host:/path/
scp user@host:/path/file.txt ./

# rsync over SSH
rsync -avz -e ssh source/ user@host:/dest/
```

### 场景 3：保持连接
```bash
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes

# 使用 autossh
autossh -M 0 -fN -L 3306:localhost:3306 user@server
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接超时 | 检查网络、防火墙、端口 |
| 权限被拒绝 | 检查密钥权限 (600)、authorized_keys |
| Host key 变更 | `ssh-keygen -R hostname` |
| Agent 转发失败 | 检查 `AllowAgentForwarding` |
| 连接断开 | 配置 `ServerAliveInterval` |

```bash
# 调试连接
ssh -vvv user@hostname

# 检查密钥权限
ls -la ~/.ssh/
# id_rsa: 600
# id_rsa.pub: 644
# authorized_keys: 600
# ~/.ssh: 700
```
