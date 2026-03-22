---
name: troubleshooting
description: OpenClaw 问题排查与诊断
version: 1.0.0
author: terminal-skills
tags: [openclaw, troubleshooting, debug, diagnosis, monitoring]
---

# OpenClaw 问题排查与诊断

## 概述
OpenClaw 常见问题的排查思路、诊断命令和解决方案。

## 健康检查

### 服务状态检查
```bash
# API 健康检查
curl -s http://localhost:8080/api/health | jq .

# 详细健康信息
curl -s http://localhost:8080/api/health/detail | jq .

# 组件状态
curl -s http://localhost:8080/api/status | jq .

# 返回示例
# {
#   "status": "UP",
#   "components": {
#     "db": { "status": "UP" },
#     "redis": { "status": "UP" },
#     "scheduler": { "status": "UP" },
#     "workers": { "status": "UP", "count": 3 }
#   }
# }
```

### 集群状态
```bash
# 集群信息
curl -s http://localhost:8080/api/cluster/info | jq .

# 节点列表
curl -s http://localhost:8080/api/cluster/nodes | jq .

# Worker 状态
curl -s http://localhost:8080/api/workers | jq .

# 检查 Worker 在线状态
curl -s http://localhost:8080/api/workers | jq '.[] | select(.status == "ONLINE")'
```

## 日志分析

### 日志位置
```bash
# Server 日志
tail -f /opt/openclaw/logs/openclaw-server.log
tail -f /opt/openclaw/logs/error.log

# Worker 日志
tail -f /opt/openclaw/logs/openclaw-worker.log

# 任务执行日志
ls -la /opt/openclaw/logs/tasks/

# Docker 方式查看
docker logs -f openclaw-server
docker logs -f openclaw-worker --tail 100
```

### 日志搜索
```bash
# 搜索错误日志
grep -i "error\|exception\|failed" /opt/openclaw/logs/openclaw-server.log

# 搜索特定任务日志
grep "taskId=12345" /opt/openclaw/logs/openclaw-server.log

# 搜索特定时间段
grep "2024-01-15 10:" /opt/openclaw/logs/openclaw-server.log

# 统计错误类型
grep -oP 'Exception: \K[^:]+' /opt/openclaw/logs/error.log | sort | uniq -c | sort -rn

# 实时监控错误
tail -f /opt/openclaw/logs/openclaw-server.log | grep -i --color "error\|exception"
```

### 日志级别调整
```bash
# 运行时调整日志级别
curl -X POST http://localhost:8080/api/admin/logging/level \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"logger": "com.openclaw.scheduler", "level": "DEBUG"}'

# 查看当前日志级别
curl http://localhost:8080/api/admin/logging/level \
  -H "Authorization: Bearer ${TOKEN}"
```

## 数据库问题排查

### 连接问题
```bash
# 测试数据库连接
mysql -h localhost -u openclaw -p -e "SELECT 1"

# 检查连接数
mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected'"
mysql -u root -p -e "SHOW PROCESSLIST"

# 检查连接池状态
curl -s http://localhost:8080/api/admin/datasource/pool | jq .

# 检查慢查询
mysql -u root -p -e "SHOW FULL PROCESSLIST" | grep -v Sleep
```

### 数据库性能
```bash
# 慢查询日志
tail -f /var/log/mysql/slow.log

# 检查锁等待
mysql -u root -p -e "
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
SELECT * FROM information_schema.INNODB_LOCKS;
"

# 检查表状态
mysql -u root -p openclaw -e "SHOW TABLE STATUS"

# 分析查询
mysql -u root -p openclaw -e "EXPLAIN SELECT * FROM task WHERE status = 'RUNNING'"
```

### 数据一致性检查
```bash
# 检查任务状态统计
mysql -u root -p openclaw -e "
SELECT status, COUNT(*) as count
FROM task
GROUP BY status
"

# 检查孤儿任务 (Worker 已下线)
mysql -u root -p openclaw -e "
SELECT t.* FROM task t
LEFT JOIN worker w ON t.worker_id = w.id
WHERE t.status = 'RUNNING' AND (w.id IS NULL OR w.status != 'ONLINE')
"
```

## Redis 问题排查

### 连接检查
```bash
# 测试 Redis 连接
redis-cli -h localhost -p 6379 ping

# 检查连接信息
redis-cli -h localhost -p 6379 info clients

# 检查内存使用
redis-cli -h localhost -p 6379 info memory

# 检查慢日志
redis-cli -h localhost -p 6379 slowlog get 10
```

### 缓存分析
```bash
# 查看 OpenClaw 相关 key
redis-cli -h localhost -p 6379 keys "openclaw:*"

# 检查特定 key
redis-cli -h localhost -p 6379 get "openclaw:task:12345"
redis-cli -h localhost -p 6379 hgetall "openclaw:worker:worker-1"

# 检查队列长度
redis-cli -h localhost -p 6379 llen "openclaw:task:queue:default"

# 内存分析
redis-cli -h localhost -p 6379 memory usage "openclaw:task:12345"
redis-cli -h localhost -p 6379 debug object "openclaw:task:12345"
```

## 任务执行问题

### 任务状态查询
```bash
# 查询任务详情
curl -s http://localhost:8080/api/tasks/12345 | jq .

# 查询任务执行记录
curl -s http://localhost:8080/api/tasks/12345/executions | jq .

# 查询失败任务
curl -s "http://localhost:8080/api/tasks?status=FAILED&limit=10" | jq .

# 查询超时任务
curl -s "http://localhost:8080/api/tasks?status=TIMEOUT&limit=10" | jq .
```

### 任务执行日志
```bash
# 获取任务执行日志
curl -s http://localhost:8080/api/tasks/12345/log | jq .

# 查看本地任务日志
cat /opt/openclaw/logs/tasks/12345.log

# 实时查看正在执行的任务日志
tail -f /opt/openclaw/logs/tasks/12345.log
```

### 常见任务问题

#### 任务一直 Pending
```bash
# 检查原因
# 1. 没有可用的 Worker
curl -s http://localhost:8080/api/workers | jq '.[] | select(.status == "ONLINE")'

# 2. Worker 负载已满
curl -s http://localhost:8080/api/workers | jq '.[] | {name, runningTasks, maxTasks}'

# 3. 任务队列阻塞
curl -s http://localhost:8080/api/admin/queue/status | jq .

# 4. 任务组没有匹配的 Worker
curl -s http://localhost:8080/api/tasks/12345 | jq '.group'
curl -s http://localhost:8080/api/workers | jq '.[] | select(.group == "specific-group")'
```

#### 任务执行超时
```bash
# 查看任务超时配置
curl -s http://localhost:8080/api/tasks/12345 | jq '.timeout'

# 检查任务实际执行时间
curl -s http://localhost:8080/api/tasks/12345/executions | jq '.[] | {startTime, endTime, duration}'

# 增加超时时间（如需要）
curl -X PUT http://localhost:8080/api/tasks/12345 \
  -H "Content-Type: application/json" \
  -d '{"timeout": 7200000}'
```

#### 任务执行失败
```bash
# 查看失败原因
curl -s http://localhost:8080/api/tasks/12345/executions | jq '.[-1] | {status, errorMessage, errorStack}'

# 查看重试记录
curl -s http://localhost:8080/api/tasks/12345/executions | jq '. | length'

# 手动重试任务
curl -X POST http://localhost:8080/api/tasks/12345/retry
```

## Worker 问题排查

### Worker 无法注册
```bash
# 检查 Worker 日志
tail -f /opt/openclaw/logs/openclaw-worker.log | grep -i "register\|connect"

# 检查网络连通性
telnet openclaw-server 9090
nc -zv openclaw-server 9090

# 检查 gRPC 服务
grpcurl -plaintext localhost:9090 list

# 检查 Server 端日志
grep "worker" /opt/openclaw/logs/openclaw-server.log | tail -50
```

### Worker 频繁离线
```bash
# 检查心跳配置
grep "heartbeat" /opt/openclaw/conf/worker.yml

# 检查网络延迟
ping -c 10 openclaw-server

# 检查系统资源
top -p $(pgrep -f openclaw-worker)
free -h
df -h

# 检查 JVM 状态
jstat -gc $(pgrep -f openclaw-worker)
```

### Worker 负载不均
```bash
# 查看各 Worker 负载
curl -s http://localhost:8080/api/workers | jq '.[] | {name, runningTasks, completedTasks}'

# 检查调度策略
curl -s http://localhost:8080/api/admin/config | jq '.scheduler.strategy'

# 检查 Worker 权重配置
curl -s http://localhost:8080/api/workers | jq '.[] | {name, weight}'
```

## 性能问题排查

### CPU 高
```bash
# 查看 Java 进程 CPU
top -H -p $(pgrep -f openclaw-server)

# 线程 dump
jstack $(pgrep -f openclaw-server) > thread_dump.txt

# 分析热点线程
jstack $(pgrep -f openclaw-server) | grep -A 30 "RUNNABLE"

# 查看线程池状态
curl -s http://localhost:8080/api/admin/threadpool | jq .
```

### 内存问题
```bash
# JVM 内存使用
jstat -gc $(pgrep -f openclaw-server) 1000

# Heap dump
jmap -dump:format=b,file=heapdump.hprof $(pgrep -f openclaw-server)

# 检查内存泄漏
jmap -histo $(pgrep -f openclaw-server) | head -30

# GC 日志分析
grep "GC" /opt/openclaw/logs/gc.log | tail -50
```

### 网络问题
```bash
# 检查连接数
ss -s
netstat -an | grep 8080 | wc -l

# 检查 TIME_WAIT
netstat -an | grep TIME_WAIT | wc -l

# 检查网络延迟
curl -o /dev/null -s -w "Connect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" http://localhost:8080/api/health
```

## 集群问题排查

### 主节点选举
```bash
# 查看当前主节点
curl -s http://localhost:8080/api/cluster/leader | jq .

# 检查选举日志
grep "leader\|election" /opt/openclaw/logs/openclaw-server.log

# 强制重新选举（谨慎使用）
curl -X POST http://localhost:8080/api/admin/cluster/reelect \
  -H "Authorization: Bearer ${TOKEN}"
```

### 节点同步
```bash
# 检查节点同步状态
curl -s http://localhost:8080/api/cluster/sync/status | jq .

# 手动触发同步
curl -X POST http://localhost:8080/api/admin/cluster/sync \
  -H "Authorization: Bearer ${TOKEN}"
```

## 诊断工具

### 内置诊断
```bash
# 运行诊断
curl -s http://localhost:8080/api/admin/diagnose | jq .

# 生成诊断报告
curl -s http://localhost:8080/api/admin/diagnose/report > diagnose_report.json

# 导出系统信息
curl -s http://localhost:8080/api/admin/system/info > system_info.json
```

### 指标监控
```bash
# Prometheus 指标
curl -s http://localhost:8080/actuator/prometheus

# 关键指标
curl -s http://localhost:8080/actuator/metrics/openclaw.task.completed
curl -s http://localhost:8080/actuator/metrics/openclaw.task.failed
curl -s http://localhost:8080/actuator/metrics/openclaw.worker.active
```

## 常见问题速查

| 问题现象 | 可能原因 | 排查命令 | 解决方案 |
|----------|----------|----------|----------|
| 服务无法启动 | 端口占用/配置错误 | `netstat -tlnp`, 查看启动日志 | 检查端口，修正配置 |
| 数据库连接失败 | 配置错误/网络问题 | `mysql -h host -u user -p` | 检查配置，网络 |
| Redis 连接失败 | 配置错误/服务未启动 | `redis-cli ping` | 检查配置，启动 Redis |
| Worker 注册失败 | 网络不通/配置错误 | `telnet server 9090` | 检查网络，配置 |
| 任务执行失败 | 脚本错误/超时 | 查看任务日志 | 修复脚本，调整超时 |
| 任务堆积 | Worker 不足/阻塞 | 查看队列状态 | 扩容 Worker |
| 内存溢出 | 内存配置过小 | `jstat -gc`, `jmap` | 增加内存配置 |
| 响应慢 | 数据库慢查询/GC | 慢查询日志，GC 日志 | SQL 优化，JVM 调优 |

## 问题上报

### 收集诊断信息
```bash
#!/bin/bash
# collect_diagnostic.sh - 收集诊断信息

DIAG_DIR="/tmp/openclaw_diag_$(date +%Y%m%d_%H%M%S)"
mkdir -p $DIAG_DIR

# 系统信息
uname -a > $DIAG_DIR/system_info.txt
free -h >> $DIAG_DIR/system_info.txt
df -h >> $DIAG_DIR/system_info.txt

# 服务状态
curl -s http://localhost:8080/api/health > $DIAG_DIR/health.json
curl -s http://localhost:8080/api/cluster/info > $DIAG_DIR/cluster.json

# 日志
tail -1000 /opt/openclaw/logs/openclaw-server.log > $DIAG_DIR/server.log
tail -1000 /opt/openclaw/logs/error.log > $DIAG_DIR/error.log

# 线程 dump
jstack $(pgrep -f openclaw-server) > $DIAG_DIR/thread_dump.txt 2>/dev/null

# 打包
tar -czf $DIAG_DIR.tar.gz -C /tmp $(basename $DIAG_DIR)
echo "诊断信息已保存: $DIAG_DIR.tar.gz"
```
