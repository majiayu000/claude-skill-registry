---
name: profiling
description: 性能分析
version: 1.0.0
author: terminal-skills
tags: [performance, profiling, perf, flamegraph, strace, cpu]
---

# 性能分析

## 概述
CPU/内存分析、火焰图、追踪技能。

## perf 工具

### 基础命令
```bash
# 安装
apt install linux-tools-common linux-tools-$(uname -r)

# CPU 采样
perf record -g -p PID
perf record -g -a -- sleep 30

# 查看报告
perf report
perf report --stdio

# 实时统计
perf top
perf top -p PID

# 统计事件
perf stat command
perf stat -p PID sleep 10
```

### 常用事件
```bash
# CPU 周期
perf record -e cycles -p PID

# 缓存未命中
perf record -e cache-misses -p PID

# 上下文切换
perf record -e context-switches -p PID

# 列出可用事件
perf list
```

### 火焰图
```bash
# 采集数据
perf record -F 99 -g -p PID -- sleep 30

# 生成火焰图
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg

# 或使用 FlameGraph 工具
git clone https://github.com/brendangregg/FlameGraph
perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > out.svg
```

## strace 追踪

### 基础用法
```bash
# 追踪进程
strace -p PID

# 追踪命令
strace command

# 统计系统调用
strace -c command
strace -c -p PID

# 追踪特定调用
strace -e open,read,write command
strace -e trace=network command
strace -e trace=file command
```

### 高级选项
```bash
# 显示时间戳
strace -t command
strace -tt command      # 微秒

# 显示耗时
strace -T command

# 跟踪子进程
strace -f command

# 输出到文件
strace -o trace.log command
```

## ltrace 库调用

```bash
# 追踪库调用
ltrace command
ltrace -p PID

# 统计
ltrace -c command

# 特定库
ltrace -l libc.so.6 command
```

## 内存分析

### valgrind
```bash
# 内存泄漏检测
valgrind --leak-check=full ./program

# 内存错误
valgrind --tool=memcheck ./program

# 缓存分析
valgrind --tool=cachegrind ./program

# 调用图
valgrind --tool=callgrind ./program
kcachegrind callgrind.out.*
```

### pmap
```bash
# 查看进程内存映射
pmap PID
pmap -x PID

# 详细信息
pmap -XX PID
```

### smem
```bash
# 内存使用统计
smem
smem -u          # 按用户
smem -p          # 按进程
smem -k          # 人类可读
```

## 系统分析

### vmstat
```bash
# 每秒刷新
vmstat 1

# 输出说明
# r: 运行队列
# b: 阻塞进程
# si/so: 交换
# bi/bo: 块 IO
# us/sy/id/wa: CPU 使用
```

### iostat
```bash
# 磁盘统计
iostat -x 1

# 输出说明
# %util: 设备利用率
# await: 平均等待时间
# r/s, w/s: 读写 IOPS
```

### pidstat
```bash
# CPU 使用
pidstat -u 1

# 内存使用
pidstat -r 1

# IO 使用
pidstat -d 1

# 特定进程
pidstat -p PID 1
```

## 常见场景

### 场景 1：CPU 热点分析
```bash
#!/bin/bash
PID=$1

# 采集 30 秒
perf record -F 99 -g -p $PID -- sleep 30

# 生成报告
perf report --stdio > cpu_report.txt

# 生成火焰图
perf script | stackcollapse-perf.pl | flamegraph.pl > cpu_flame.svg
```

### 场景 2：IO 延迟分析
```bash
#!/bin/bash
# 使用 biolatency (bcc-tools)
biolatency 10 1

# 或使用 iostat
iostat -x 1 10
```

### 场景 3：系统调用分析
```bash
#!/bin/bash
PID=$1

# 统计系统调用
strace -c -p $PID -o syscall_stat.txt &
sleep 60
kill %1

cat syscall_stat.txt
```

## 工具对比

| 工具 | 用途 | 开销 |
|------|------|------|
| perf | CPU 分析 | 低 |
| strace | 系统调用 | 高 |
| valgrind | 内存分析 | 很高 |
| pidstat | 进程统计 | 低 |

## 故障排查

```bash
# perf 权限问题
echo 0 > /proc/sys/kernel/perf_event_paranoid

# 符号缺失
apt install linux-tools-$(uname -r)-dbgsym

# strace 附加失败
echo 0 > /proc/sys/kernel/yama/ptrace_scope
```
