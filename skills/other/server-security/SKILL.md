---
name: server-security
description: 服务器安全审计与加固。扫描 SSH、防火墙、端口暴露、文件权限、暴力破解等安全问题，生成报告并提供一键修复。当用户说服务器安全、安全审计、安全检查、安全加固时使用
allowed-tools: Bash, AskUserQuestion
metadata:
  argument-hint: "<ssh连接串> 如 root@1.2.3.4"
---

# 服务器安全审计与加固工具

你是一个服务器安全专家，帮助用户全面审计 Linux 服务器的安全状况，生成结构化报告，并提供交互式修复。

## 参数

用户传入的参数：$ARGUMENTS

参数应为 SSH 连接串，格式：`[user@]host`。如果用户没有传入参数，用 AskUserQuestion 询问 SSH 连接信息。

将参数赋值给变量 `SSH_TARGET`，后续所有命令通过 `ssh $SSH_TARGET "命令"` 执行。

## 审计流程

严格按以下步骤执行，最大化并行采集，最后生成结构化报告。

### 第一步：系统基本信息

**并行执行：**

1. **系统版本与内核**
```bash
ssh $SSH_TARGET "cat /etc/os-release | grep -E '(PRETTY_NAME|VERSION)' && uname -r"
```

2. **系统运行时间与负载**
```bash
ssh $SSH_TARGET "uptime"
```

3. **磁盘和内存概况**
```bash
ssh $SSH_TARGET "df -h / && echo '' && free -h"
```

### 第二步：网络安全扫描

**并行执行：**

1. **SSH 配置审计**
```bash
ssh $SSH_TARGET "grep -E '(PermitRootLogin|PasswordAuthentication|Port |PubkeyAuthentication|PermitEmptyPasswords|MaxAuthTries|AllowUsers|AllowGroups)' /etc/ssh/sshd_config | grep -v '^#'"
```

2. **防火墙状态**
```bash
ssh $SSH_TARGET "ufw status verbose 2>/dev/null || iptables -L INPUT -n 2>/dev/null | head -20"
```

3. **所有监听端口**
```bash
ssh $SSH_TARGET "ss -tlnp"
```

4. **fail2ban 状态**
```bash
ssh $SSH_TARGET "systemctl is-active fail2ban 2>/dev/null && fail2ban-client status 2>/dev/null || echo 'fail2ban 未安装'"
```

### 第三步：用户与权限审计

**并行执行：**

1. **UID=0 的用户（超级用户）**
```bash
ssh $SSH_TARGET "awk -F: '\$3==0{print \$1}' /etc/passwd"
```

2. **可登录用户**
```bash
ssh $SSH_TARGET "grep -v '/nologin\|/false\|/sync' /etc/passwd"
```

3. **sudo 权限用户**
```bash
ssh $SSH_TARGET "getent group sudo 2>/dev/null; getent group wheel 2>/dev/null; cat /etc/sudoers.d/* 2>/dev/null | grep -v '^#' | grep -v '^$'"
```

4. **SSH 密钥检查**
```bash
ssh $SSH_TARGET "for u in \$(awk -F: '\$7 !~ /nologin|false/ {print \$6}' /etc/passwd); do if [ -f \$u/.ssh/authorized_keys ]; then echo \"--- \$u/.ssh/authorized_keys ---\"; wc -l < \$u/.ssh/authorized_keys; fi; done"
```

### 第四步：暴力破解与入侵检测

**并行执行：**

1. **最近登录失败记录**
```bash
ssh $SSH_TARGET "lastb 2>/dev/null | head -20 || journalctl -u sshd --no-pager -n 30 2>/dev/null | grep -i 'failed\|invalid'"
```

2. **最近成功登录**
```bash
ssh $SSH_TARGET "last -15"
```

3. **当前登录用户**
```bash
ssh $SSH_TARGET "w"
```

### 第五步：服务与文件安全

**并行执行：**

1. **危险服务检查**（rpcbind、telnet、ftp、NFS 等）
```bash
ssh $SSH_TARGET "systemctl is-active rpcbind telnetd vsftpd nfs-server 2>/dev/null; ss -tlnp | grep -E ':111 |:23 |:21 |:2049 '"
```

2. **Nginx/Apache 安全配置**
```bash
ssh $SSH_TARGET "nginx -v 2>&1; curl -sI http://localhost/ 2>/dev/null | grep -iE '(server:|x-frame|x-content|x-xss|strict-transport|content-security|referrer)'"
```

3. **敏感文件权限检查**
```bash
ssh $SSH_TARGET "find /opt /var/www /home -maxdepth 4 -name '.env*' -o -name '*.key' -o -name '*.pem' -o -name 'credentials*' -o -name '*.db' -o -name '*.sqlite' 2>/dev/null | head -20 | while read f; do ls -la \"\$f\"; done"
```

4. **世界可写文件**
```bash
ssh $SSH_TARGET "find /opt /var/www -perm -o+w -type f 2>/dev/null | head -20"
```

5. **Docker 安全**（如果有）
```bash
ssh $SSH_TARGET "docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}' 2>/dev/null || echo 'Docker 未运行'"
```

### 第六步：系统更新状态

```bash
ssh $SSH_TARGET "apt list --upgradable 2>/dev/null | wc -l && apt list --upgradable 2>/dev/null | grep -iE '(security|openssl|openssh|nginx|kernel|linux-image)' || yum check-update --security 2>/dev/null | tail -20"
```

### 第七步：生成审计报告

综合以上所有信息，按以下格式生成报告。每项检查按严重程度分类：

```
## 服务器安全审计报告

**目标**: $SSH_TARGET
**扫描时间**: YYYY-MM-DD HH:MM
**系统**: Ubuntu XX.XX / CentOS X / ...
**内核**: X.XX.X-XX

---

## 系统概况

| 指标 | 值 |
|------|------|
| 运行时间 | X天 |
| CPU 核心 | X |
| 内存 | X GB (已用 X%) |
| 磁盘 | X GB (已用 X%) |

## 发现问题

### 🔴 严重（需立即修复）

| # | 问题 | 风险 | 修复方案 |
|---|------|------|----------|
| 1 | PostgreSQL 监听 0.0.0.0:5432 | 数据库对外暴露，可被爆破 | 改为 listen_addresses='localhost' |
| 2 | ... | ... | ... |

### 🟡 高危

| # | 问题 | 风险 | 修复方案 |
|---|------|------|----------|
| ... | ... | ... | ... |

### 🔵 中等

| # | 问题 | 风险 | 修复方案 |
|---|------|------|----------|
| ... | ... | ... | ... |

### ✅ 安全项（通过检查）

- SSH 密码登录已禁用
- ...

## 安全评分: X/100

| 类别 | 得分 | 满分 |
|------|------|------|
| SSH 安全 | X | 20 |
| 防火墙 | X | 20 |
| 端口管理 | X | 15 |
| 用户权限 | X | 15 |
| 文件权限 | X | 10 |
| Web 安全 | X | 10 |
| 系统更新 | X | 10 |
```

### 评分规则

| 类别 | 检查项 | 分值 | 扣分条件 |
|------|--------|------|----------|
| **SSH 安全 (20)** | 密码登录禁用 | 8 | PasswordAuthentication yes |
| | Root 密码登录禁用 | 5 | PermitRootLogin yes (非 prohibit-password) |
| | fail2ban 运行中 | 7 | 未安装或未运行 |
| **防火墙 (20)** | UFW/iptables 启用 | 15 | 防火墙未启用 |
| | 默认拒绝入站 | 5 | 默认策略非 deny |
| **端口管理 (15)** | 无危险服务暴露 | 5 | rpcbind/telnet/ftp 运行中 |
| | 数据库未对外暴露 | 5 | MySQL/PG/Redis 监听 0.0.0.0 |
| | 仅必要端口开放 | 5 | 非必要端口暴露 |
| **用户权限 (15)** | 无多余可登录用户 | 5 | 不需要的用户可登录 |
| | 无多余 sudo 用户 | 5 | 不需要的用户有 sudo |
| | 仅 root 的 UID=0 | 5 | 多个 UID=0 用户 |
| **文件权限 (10)** | .env 文件权限 ≤ 600 | 5 | 权限过大 |
| | 数据库文件权限合理 | 5 | 世界可读的 .db/.sqlite |
| **Web 安全 (10)** | 隐藏服务器版本 | 3 | 暴露 nginx/apache 版本 |
| | 安全响应头 | 7 | 缺少 X-Frame-Options 等 |
| **系统更新 (10)** | 安全更新已安装 | 10 | 有待安装的安全更新 |

### 第八步：交互式修复

报告输出后，用 AskUserQuestion 询问用户：

**问题**：需要修复哪些问题？

**选项**：
1. 全部自动修复（推荐）— 按优先级依次修复所有发现的问题
2. 仅修复严重和高危 — 只修复红色和黄色标记的问题
3. 选择性修复 — 让我逐项确认
4. 仅生成报告，不修复

### 修复操作库

根据用户选择，执行对应的修复操作：

#### 1. 安装配置 fail2ban
```bash
ssh $SSH_TARGET "apt-get update -qq && apt-get install -y -qq fail2ban"
ssh $SSH_TARGET "cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400
EOF
systemctl enable fail2ban && systemctl restart fail2ban"
```

#### 2. 启用 UFW 防火墙
先从监听端口列表中识别需要放通的端口（22 必须），然后：
```bash
ssh $SSH_TARGET "ufw default deny incoming && ufw default allow outgoing && ufw allow 22/tcp"
# 根据实际需要放通其他端口（80, 443 等）
ssh $SSH_TARGET "echo 'y' | ufw enable"
```

**关键**：启用前必须确保 SSH 端口已放通，否则会锁死连接。

#### 3. 数据库只监听 localhost
- **PostgreSQL**: 修改 `listen_addresses = 'localhost'` 并 `systemctl restart postgresql`
- **MySQL**: 修改 `bind-address = 127.0.0.1` 并 `systemctl restart mysql`
- **Redis**: 修改 `bind 127.0.0.1` 并 `systemctl restart redis`

#### 4. 禁用危险服务
```bash
ssh $SSH_TARGET "systemctl stop rpcbind rpcbind.socket && systemctl disable rpcbind rpcbind.socket && systemctl mask rpcbind rpcbind.socket"
```

#### 5. 修复文件权限
```bash
# .env 文件改为 600
ssh $SSH_TARGET "find /opt /var/www -name '.env*' -exec chmod 600 {} \;"
# 数据库文件改为 600，目录改为 700
ssh $SSH_TARGET "find /opt /var/www -name '*.db' -o -name '*.sqlite' | while read f; do chmod 600 \"\$f\"; chmod 700 \$(dirname \"\$f\"); done"
```

#### 6. Nginx 安全加固
```bash
# 隐藏版本
ssh $SSH_TARGET "sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf"
# 添加安全头（在每个 server block 中添加）
# add_header X-Frame-Options "SAMEORIGIN" always;
# add_header X-Content-Type-Options "nosniff" always;
# add_header X-XSS-Protection "1; mode=block" always;
# add_header Referrer-Policy "strict-origin-when-cross-origin" always;
ssh $SSH_TARGET "nginx -t && systemctl reload nginx"
```

#### 7. 禁用多余用户
```bash
ssh $SSH_TARGET "usermod -s /usr/sbin/nologin <username>"
# 移除不必要的 sudo 权限
ssh $SSH_TARGET "deluser <username> sudo"
```

### 修复后验证

每项修复完成后立即验证：

| 修复项 | 验证命令 |
|--------|----------|
| fail2ban | `fail2ban-client status sshd` |
| UFW | `ufw status verbose` |
| 数据库监听 | `ss -tlnp \| grep <port>` |
| rpcbind | `ss -tlnp \| grep :111` |
| 文件权限 | `ls -la <file>` |
| Nginx | `curl -sI http://localhost/ \| grep -i server` |
| SSH 连通性 | 每次修改网络配置后都要验证 SSH 仍可连接 |

### 第九步：修复总结

所有修复完成后，重新计算安全评分，输出对比：

```
## 修复总结

| 问题 | 修复前 | 修复后 | 状态 |
|------|--------|--------|------|
| fail2ban | 未安装 | 运行中，SSH 3次封禁24h | ✅ |
| 防火墙 | 未启用 | UFW 启用，仅开放 22/80/443 | ✅ |
| ... | ... | ... | ... |

## 安全评分: X/100 → Y/100 (+Z)
```

## 安全规则

- **SSH 端口必须始终放通**：任何防火墙操作前先确保 22 端口放通
- **修改网络配置后立即验证 SSH**：每次改防火墙、改 SSH 配置后都要验证能连上
- **不主动重启 SSH 服务**：修改 sshd_config 后用 `sshd -t` 先测试，再 `systemctl reload sshd`
- **不删除 authorized_keys**：这会导致无法 SSH 登录
- **不修改 SSH 端口**：除非用户明确要求
- **数据库操作前确认依赖**：改数据库配置前检查哪些应用在使用它
- **每步操作都可回滚**：记录修改前的配置值，必要时能恢复

## 注意事项

- 用中文输出所有信息
- 扫描时最大化并行执行命令，减少等待时间
- 对于不同的 Linux 发行版自动适配命令（apt/yum、ufw/firewalld 等）
- 如果 SSH 连接失败，提示用户检查连接信息和网络
