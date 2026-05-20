---
name: systemd
description: Systemd 服务管理
version: 1.0.0
author: terminal-skills
tags: [server, systemd, service, init, linux]
---

# Systemd 服务管理

## 概述
Systemd 服务单元编写、依赖管理、日志查看等技能。

## 服务管理

### 基础命令
```bash
# 启停服务
systemctl start service-name
systemctl stop service-name
systemctl restart service-name
systemctl reload service-name       # 重载配置（不中断服务）

# 开机启动
systemctl enable service-name
systemctl disable service-name
systemctl enable --now service-name # 启用并立即启动

# 查看状态
systemctl status service-name
systemctl is-active service-name
systemctl is-enabled service-name
systemctl is-failed service-name
```

### 服务列表
```bash
# 列出所有服务
systemctl list-units --type=service
systemctl list-units --type=service --state=running
systemctl list-units --type=service --state=failed

# 列出所有单元文件
systemctl list-unit-files --type=service

# 查看依赖
systemctl list-dependencies service-name
systemctl list-dependencies --reverse service-name
```

## 单元文件

### 文件位置
```bash
# 系统单元（包管理器安装）
/usr/lib/systemd/system/

# 管理员自定义
/etc/systemd/system/

# 运行时生成
/run/systemd/system/

# 优先级：/etc > /run > /usr/lib
```

### 基础服务单元
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Documentation=https://example.com/docs
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/start.sh
ExecStop=/opt/myapp/bin/stop.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 服务类型
```ini
# simple（默认）- 主进程即服务进程
Type=simple
ExecStart=/usr/bin/myapp

# forking - 传统守护进程
Type=forking
PIDFile=/var/run/myapp.pid
ExecStart=/usr/bin/myapp -d

# oneshot - 一次性任务
Type=oneshot
ExecStart=/usr/bin/backup.sh
RemainAfterExit=yes

# notify - 服务就绪通知
Type=notify
ExecStart=/usr/bin/myapp
```

### 环境变量
```ini
[Service]
# 直接设置
Environment="VAR1=value1" "VAR2=value2"

# 从文件加载
EnvironmentFile=/etc/myapp/env
EnvironmentFile=-/etc/myapp/env.local  # - 表示可选

# 传递给子进程
PassEnvironment=HOME USER
```

### 资源限制
```ini
[Service]
# 文件描述符
LimitNOFILE=65535

# 进程数
LimitNPROC=4096

# 内存限制
MemoryLimit=512M
MemoryMax=1G

# CPU 限制
CPUQuota=50%

# 超时设置
TimeoutStartSec=30
TimeoutStopSec=30
```

### 安全选项
```ini
[Service]
# 用户隔离
User=appuser
Group=appgroup
DynamicUser=yes

# 文件系统保护
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/myapp

# 网络隔离
PrivateNetwork=yes

# 能力限制
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
```

## 日志管理

### journalctl
```bash
# 查看服务日志
journalctl -u service-name
journalctl -u service-name -f       # 实时跟踪
journalctl -u service-name --since today
journalctl -u service-name --since "1 hour ago"
journalctl -u service-name -n 100   # 最后100行

# 按时间范围
journalctl --since "2024-01-01" --until "2024-01-02"

# 按优先级
journalctl -p err                   # 错误及以上
journalctl -p warning

# 输出格式
journalctl -u service-name -o json
journalctl -u service-name -o json-pretty

# 磁盘使用
journalctl --disk-usage
journalctl --vacuum-size=500M       # 清理到500M
journalctl --vacuum-time=7d         # 保留7天
```

## 定时器

### Timer 单元
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00           # 每天凌晨2点
Persistent=true                      # 错过的任务补执行

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

### 定时器管理
```bash
# 启用定时器
systemctl enable --now backup.timer

# 查看定时器
systemctl list-timers
systemctl list-timers --all
```

## 常见场景

### 场景 1：Node.js 应用
```ini
[Unit]
Description=Node.js Application
After=network.target

[Service]
Type=simple
User=node
WorkingDirectory=/opt/nodeapp
ExecStart=/usr/bin/node /opt/nodeapp/app.js
Restart=on-failure
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

### 场景 2：Java 应用
```ini
[Unit]
Description=Java Application
After=network.target

[Service]
Type=simple
User=java
ExecStart=/usr/bin/java -Xms512m -Xmx1024m -jar /opt/app/app.jar
SuccessExitStatus=143
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 场景 3：覆盖系统服务配置
```bash
# 创建覆盖目录
systemctl edit nginx

# 或手动创建
mkdir -p /etc/systemd/system/nginx.service.d/
cat > /etc/systemd/system/nginx.service.d/override.conf << EOF
[Service]
LimitNOFILE=65535
EOF

systemctl daemon-reload
systemctl restart nginx
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 服务启动失败 | `systemctl status`, `journalctl -u` |
| 依赖问题 | `systemctl list-dependencies` |
| 配置错误 | `systemd-analyze verify service.service` |
| 权限问题 | 检查 User/Group、文件权限 |
| 超时 | 调整 TimeoutStartSec |

```bash
# 重载配置
systemctl daemon-reload

# 分析启动时间
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain

# 验证单元文件
systemd-analyze verify /etc/systemd/system/myapp.service
```
