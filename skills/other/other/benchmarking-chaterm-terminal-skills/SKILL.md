---
name: benchmarking
description: 性能基准测试
version: 1.0.0
author: terminal-skills
tags: [performance, benchmark, stress, load-test, sysbench]
---

# 性能基准测试

## 概述
压力测试、基准测试工具使用技能。

## sysbench

### 安装
```bash
# Debian/Ubuntu
apt install sysbench

# CentOS/RHEL
yum install sysbench
```

### CPU 测试
```bash
# 单线程
sysbench cpu run

# 多线程
sysbench cpu --threads=4 run

# 指定时间
sysbench cpu --threads=4 --time=60 run
```

### 内存测试
```bash
# 顺序读写
sysbench memory run

# 随机读写
sysbench memory --memory-access-mode=rnd run

# 指定大小
sysbench memory --memory-block-size=1M --memory-total-size=10G run
```

### 磁盘 IO 测试
```bash
# 准备测试文件
sysbench fileio --file-total-size=10G prepare

# 随机读写
sysbench fileio --file-total-size=10G --file-test-mode=rndrw run

# 顺序读
sysbench fileio --file-total-size=10G --file-test-mode=seqrd run

# 清理
sysbench fileio --file-total-size=10G cleanup
```

### MySQL 测试
```bash
# 准备数据
sysbench oltp_read_write --mysql-host=localhost --mysql-user=root \
    --mysql-password=pass --mysql-db=test --tables=10 --table-size=100000 prepare

# 运行测试
sysbench oltp_read_write --mysql-host=localhost --mysql-user=root \
    --mysql-password=pass --mysql-db=test --tables=10 --table-size=100000 \
    --threads=16 --time=60 run

# 清理
sysbench oltp_read_write --mysql-host=localhost --mysql-user=root \
    --mysql-password=pass --mysql-db=test cleanup
```

## fio 磁盘测试

### 基础测试
```bash
# 顺序读
fio --name=seqread --rw=read --bs=1M --size=1G --numjobs=1 --runtime=60

# 顺序写
fio --name=seqwrite --rw=write --bs=1M --size=1G --numjobs=1 --runtime=60

# 随机读
fio --name=randread --rw=randread --bs=4k --size=1G --numjobs=4 --runtime=60

# 随机写
fio --name=randwrite --rw=randwrite --bs=4k --size=1G --numjobs=4 --runtime=60

# 混合读写
fio --name=randrw --rw=randrw --bs=4k --size=1G --numjobs=4 --rwmixread=70 --runtime=60
```

### 配置文件
```ini
# test.fio
[global]
ioengine=libaio
direct=1
runtime=60
time_based

[seqread]
rw=read
bs=1M
size=1G

[randread]
rw=randread
bs=4k
size=1G
numjobs=4
```

```bash
fio test.fio
```

## HTTP 压测

### ab (Apache Bench)
```bash
# 基础测试
ab -n 1000 -c 100 http://localhost/

# 带 Keep-Alive
ab -n 1000 -c 100 -k http://localhost/

# POST 请求
ab -n 1000 -c 100 -p data.json -T application/json http://localhost/api
```

### wrk
```bash
# 基础测试
wrk -t4 -c100 -d30s http://localhost/

# 带脚本
wrk -t4 -c100 -d30s -s post.lua http://localhost/api
```

### hey
```bash
# 基础测试
hey -n 1000 -c 100 http://localhost/

# 指定时间
hey -z 30s -c 100 http://localhost/

# POST 请求
hey -n 1000 -c 100 -m POST -d '{"key":"value"}' http://localhost/api
```

## 网络测试

### iperf3
```bash
# 服务端
iperf3 -s

# 客户端
iperf3 -c server_ip

# UDP 测试
iperf3 -c server_ip -u -b 1G

# 双向测试
iperf3 -c server_ip -d

# 多线程
iperf3 -c server_ip -P 4
```

### netperf
```bash
# 服务端
netserver

# TCP 吞吐
netperf -H server_ip

# TCP 延迟
netperf -H server_ip -t TCP_RR
```

## 常见场景

### 场景 1：服务器基准测试
```bash
#!/bin/bash
echo "=== CPU 测试 ==="
sysbench cpu --threads=$(nproc) --time=30 run

echo "=== 内存测试 ==="
sysbench memory --threads=$(nproc) --time=30 run

echo "=== 磁盘测试 ==="
fio --name=test --rw=randrw --bs=4k --size=1G --runtime=30 --time_based
```

### 场景 2：数据库基准
```bash
#!/bin/bash
# MySQL OLTP 测试
sysbench oltp_read_write \
    --mysql-host=localhost \
    --mysql-user=root \
    --mysql-password=pass \
    --mysql-db=sbtest \
    --tables=10 \
    --table-size=100000 \
    --threads=16 \
    --time=300 \
    --report-interval=10 \
    run
```

## 结果解读

| 指标 | 说明 |
|------|------|
| TPS | 每秒事务数 |
| QPS | 每秒查询数 |
| IOPS | 每秒 IO 操作数 |
| 延迟 | 响应时间 |
| 吞吐量 | 数据传输速率 |

## 故障排查

```bash
# 检查系统负载
uptime
vmstat 1

# 检查 IO
iostat -x 1

# 检查网络
sar -n DEV 1
```
