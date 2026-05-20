---
name: troubleshooting
description: 性能问题排查
version: 1.0.0
author: terminal-skills
tags: [performance, troubleshooting, bottleneck, diagnosis]
---

# 性能问题排查

## 概述
性能瓶颈定位、资源争用分析技能。

## 快速诊断

### USE 方法
```bash
# Utilization, Saturation, Errors

# CPU
# 利用率
mpstat -P ALL 1
# 饱和度
vmstat 1 | awk '{print $1}'    # 运行队列
# 错误
dmesg | grep -i "cpu"

# 内存
# 利用率
free -m
# 饱和度
vmstat 1 | awk '{print $7,$8}' # si/so
# 错误
dmesg | grep -i "oom"

# 磁盘
# 利用率
iostat -x 1 | awk '{print $NF}'  # %util
# 饱和度
iostat -x 1 | awk '{print $10}'  # avgqu-sz
# 错误
dmesg | grep -i "error"

# 网络
# 利用率
sar -n DEV 1
# 饱和度
netstat -s | grep -i "overflow"
# 错误
ip -s link
```

### 60 秒诊断
```bash
# 1. 系统负载
uptime

# 2. 内核消息
dmesg | tail

# 3. 系统统计
vmstat 1 5

# 4. CPU 统计
mpstat -P ALL 1 5

# 5. 进程 CPU
pidstat 1 5

# 6. 磁盘 IO
iostat -xz 1 5

# 7. 内存使用
free -m

# 8. 网络统计
sar -n DEV 1 5

# 9. TCP 统计
sar -n TCP,ETCP 1 5

# 10. 进程列表
top -bn1 | head -20
```

## CPU 问题排查

### 高 CPU 使用
```bash
# 找出高 CPU 进程
top -c
ps aux --sort=-%cpu | head

# 查看进程线程
top -H -p PID
ps -T -p PID

# CPU 分析
perf top -p PID
perf record -g -p PID -- sleep 30
perf report
```

### CPU 等待
```bash
# 查看 iowait
vmstat 1
iostat -x 1

# 找出 IO 进程
iotop
pidstat -d 1
```

### 上下文切换
```bash
# 系统级
vmstat 1 | awk '{print $12,$13}'

# 进程级
pidstat -w 1
pidstat -wt -p PID 1
```

## 内存问题排查

### 内存不足
```bash
# 查看内存使用
free -m
cat /proc/meminfo

# 查看进程内存
ps aux --sort=-%mem | head
smem -rs pss

# 查看缓存
slabtop
cat /proc/slabinfo
```

### 内存泄漏
```bash
# 监控进程内存
while true; do
    ps -o pid,vsz,rss,comm -p PID
    sleep 60
done

# 使用 valgrind
valgrind --leak-check=full ./program
```

### OOM 分析
```bash
# 查看 OOM 日志
dmesg | grep -i "oom"
journalctl -k | grep -i "oom"

# 查看 OOM 分数
cat /proc/PID/oom_score
cat /proc/PID/oom_score_adj
```

## 磁盘 IO 问题

### IO 瓶颈
```bash
# 查看 IO 统计
iostat -x 1

# 关键指标
# %util > 80%: 设备繁忙
# await > 10ms: 延迟高
# avgqu-sz > 1: 队列积压

# 找出 IO 进程
iotop -o
pidstat -d 1
```

### 磁盘空间
```bash
# 查看空间
df -h
df -i    # inode

# 找大文件
du -sh /* | sort -rh | head
find / -type f -size +100M

# 找已删除但占用空间的文件
lsof | grep deleted
```

## 网络问题排查

### 连接问题
```bash
# 查看连接状态
ss -s
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c

# TIME_WAIT 过多
ss -tan state time-wait | wc -l

# 连接队列溢出
netstat -s | grep -i "overflow"
ss -ltn
```

### 带宽问题
```bash
# 查看流量
iftop
nethogs
sar -n DEV 1

# 查看连接带宽
ss -ti
```

### 延迟问题
```bash
# 网络延迟
ping target
mtr target

# TCP 延迟
ss -ti | grep rtt
```

## 常见场景

### 场景 1：系统变慢排查
```bash
#!/bin/bash
echo "=== 系统负载 ==="
uptime

echo "=== CPU 使用 ==="
mpstat 1 3

echo "=== 内存使用 ==="
free -m

echo "=== 磁盘 IO ==="
iostat -x 1 3

echo "=== 高 CPU 进程 ==="
ps aux --sort=-%cpu | head -5

echo "=== 高内存进程 ==="
ps aux --sort=-%mem | head -5
```

### 场景 2：应用响应慢
```bash
#!/bin/bash
PID=$1

echo "=== 进程状态 ==="
ps -p $PID -o pid,stat,pcpu,pmem,cmd

echo "=== 线程状态 ==="
ps -T -p $PID

echo "=== 打开文件 ==="
lsof -p $PID | wc -l

echo "=== 网络连接 ==="
ss -tnp | grep $PID | wc -l

echo "=== 系统调用 ==="
strace -c -p $PID -o /tmp/strace.out &
sleep 10
kill %1
cat /tmp/strace.out
```

## 排查清单

| 症状 | 检查项 |
|------|--------|
| 系统慢 | load、CPU、内存、IO |
| 响应慢 | 网络、磁盘、锁 |
| 内存高 | 泄漏、缓存、交换 |
| IO 高 | 进程、队列、设备 |

## 常用工具

```bash
# 综合工具
htop, atop, glances, nmon

# CPU
top, mpstat, perf, pidstat

# 内存
free, vmstat, smem, pmap

# 磁盘
iostat, iotop, blktrace

# 网络
ss, netstat, iftop, tcpdump
```
