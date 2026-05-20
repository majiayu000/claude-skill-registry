---
name: tuning
description: 系统调优
version: 1.0.0
author: terminal-skills
tags: [performance, tuning, sysctl, kernel, optimization]
---

# 系统调优

## 概述
内核参数、文件系统、网络优化技能。

## 内核参数调优

### 内存管理
```bash
# /etc/sysctl.d/99-memory.conf

# 减少交换倾向
vm.swappiness = 10

# 脏页刷新
vm.dirty_ratio = 20
vm.dirty_background_ratio = 5

# 内存过量提交
vm.overcommit_memory = 1
vm.overcommit_ratio = 80

# 最大内存映射数
vm.max_map_count = 262144

# 应用
sysctl -p /etc/sysctl.d/99-memory.conf
```

### 网络调优
```bash
# /etc/sysctl.d/99-network.conf

# TCP 缓冲区
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# 连接队列
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_max_syn_backlog = 65535

# TIME_WAIT
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_tw_buckets = 65535

# 端口范围
net.ipv4.ip_local_port_range = 1024 65535

# Keep-Alive
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 3
```

### 文件系统
```bash
# /etc/sysctl.d/99-fs.conf

# 文件句柄
fs.file-max = 2097152
fs.nr_open = 2097152

# inotify
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 512
```

## 文件描述符限制

### ulimit 配置
```bash
# /etc/security/limits.conf
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535

root soft nofile 65535
root hard nofile 65535
```

### systemd 服务
```bash
# /etc/systemd/system/myapp.service.d/limits.conf
[Service]
LimitNOFILE=65535
LimitNPROC=65535
```

## 磁盘 IO 调优

### IO 调度器
```bash
# 查看当前调度器
cat /sys/block/sda/queue/scheduler

# 设置调度器
echo deadline > /sys/block/sda/queue/scheduler
echo noop > /sys/block/sda/queue/scheduler      # SSD
echo mq-deadline > /sys/block/nvme0n1/queue/scheduler

# 永久设置 (GRUB)
GRUB_CMDLINE_LINUX="elevator=deadline"
```

### 预读设置
```bash
# 查看预读
blockdev --getra /dev/sda

# 设置预读 (KB)
blockdev --setra 4096 /dev/sda
```

### 挂载选项
```bash
# /etc/fstab
# SSD 优化
/dev/sda1 /data ext4 defaults,noatime,nodiratime,discard 0 2

# 数据库优化
/dev/sdb1 /mysql ext4 defaults,noatime,barrier=0 0 2
```

## CPU 调优

### CPU 频率
```bash
# 查看调速器
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 设置性能模式
cpupower frequency-set -g performance

# 或直接设置
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### NUMA 优化
```bash
# 查看 NUMA 信息
numactl --hardware
numastat

# 绑定 NUMA 节点
numactl --cpunodebind=0 --membind=0 ./program

# 查看进程 NUMA 分布
numastat -p PID
```

### CPU 亲和性
```bash
# 查看亲和性
taskset -p PID

# 设置亲和性
taskset -c 0-3 ./program
taskset -pc 0-3 PID
```

## 常见场景

### 场景 1：Web 服务器优化
```bash
# /etc/sysctl.d/99-web.conf
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.core.netdev_max_backlog = 65535

# 文件描述符
fs.file-max = 2097152
```

### 场景 2：数据库服务器优化
```bash
# /etc/sysctl.d/99-database.conf
vm.swappiness = 1
vm.dirty_ratio = 40
vm.dirty_background_ratio = 10
vm.overcommit_memory = 1

# 大页内存
vm.nr_hugepages = 1024
```

### 场景 3：高并发优化
```bash
#!/bin/bash
# 一键优化脚本

# 网络
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sysctl -w net.ipv4.ip_local_port_range="1024 65535"

# 文件
sysctl -w fs.file-max=2097152

# 内存
sysctl -w vm.swappiness=10
```

## 调优检查

| 项目 | 检查命令 |
|------|----------|
| 文件限制 | ulimit -n |
| 网络参数 | sysctl -a \| grep net |
| 内存参数 | sysctl -a \| grep vm |
| IO 调度 | cat /sys/block/*/queue/scheduler |

## 故障排查

```bash
# 检查当前限制
cat /proc/PID/limits

# 检查打开文件数
ls /proc/PID/fd | wc -l
lsof -p PID | wc -l

# 检查网络连接
ss -s
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c
```
