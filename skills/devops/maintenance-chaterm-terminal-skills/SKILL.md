---
name: maintenance
description: OpenClaw 运维与故障修复
version: 1.0.0
author: terminal-skills
tags: [openclaw, maintenance, ops, repair, backup, recovery]
---

# OpenClaw 运维与故障修复

## 概述
OpenClaw 日常运维操作、备份恢复、故障修复和高可用管理指南。

## 日常运维

### 服务管理
```bash
# Systemd 方式
systemctl start openclaw-server
systemctl stop openclaw-server
systemctl restart openclaw-server
systemctl status openclaw-server

# 脚本方式
/opt/openclaw/bin/openclaw-server.sh start
/opt/openclaw/bin/openclaw-server.sh stop
/opt/openclaw/bin/openclaw-server.sh restart
/opt/openclaw/bin/openclaw-server.sh status

# Docker 方式
docker-compose start
docker-compose stop
docker-compose restart
docker-compose ps

# Kubernetes 方式
kubectl rollout restart deployment/openclaw-server -n openclaw
kubectl scale deployment/openclaw-worker --replicas=5 -n openclaw
```

### 健康检查
```bash
# 服务健康检查
curl -s http://localhost:8080/api/health | jq .

# 集群健康检查
curl -s http://localhost:8080/api/cluster/health | jq .

# 自动化健康检查脚本
#!/bin/bash
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/health)
if [ "$HEALTH" != "200" ]; then
    echo "OpenClaw 服务异常，状态码: $HEALTH"
    # 发送告警
    curl -X POST https://webhook.example.com/alert \
      -H "Content-Type: application/json" \
      -d '{"message": "OpenClaw 服务异常"}'
fi
```

### 日志管理
```bash
# 日志轮转配置
cat > /etc/logrotate.d/openclaw << 'EOF'
/opt/openclaw/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 openclaw openclaw
    postrotate
        systemctl reload openclaw-server > /dev/null 2>&1 || true
    endscript
}
EOF

# 手动清理日志
find /opt/openclaw/logs -name "*.log.*" -mtime +30 -delete
find /opt/openclaw/logs/tasks -name "*.log" -mtime +7 -delete

# 日志归档
tar -czf /backup/openclaw-logs-$(date +%Y%m%d).tar.gz /opt/openclaw/logs/
```

## 备份与恢复

### 数据库备份
```bash
# 全量备份
mysqldump -h localhost -u openclaw -p \
  --single-transaction \
  --routines \
  --triggers \
  openclaw > /backup/openclaw_$(date +%Y%m%d_%H%M%S).sql

# 压缩备份
mysqldump -h localhost -u openclaw -p openclaw | gzip > /backup/openclaw_$(date +%Y%m%d).sql.gz

# 定时备份脚本
#!/bin/bash
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

mysqldump -h localhost -u openclaw -p$MYSQL_PASSWORD \
  --single-transaction \
  openclaw | gzip > $BACKUP_DIR/openclaw_$DATE.sql.gz

# 清理 7 天前的备份
find $BACKUP_DIR -name "openclaw_*.sql.gz" -mtime +7 -delete

echo "备份完成: $BACKUP_DIR/openclaw_$DATE.sql.gz"
```

### 数据库恢复
```bash
# 停止服务
systemctl stop openclaw-server

# 恢复数据库
gunzip < /backup/openclaw_20240115.sql.gz | mysql -h localhost -u openclaw -p openclaw

# 或直接恢复
mysql -h localhost -u openclaw -p openclaw < /backup/openclaw_20240115.sql

# 启动服务
systemctl start openclaw-server
```

### 配置备份
```bash
# 备份配置文件
tar -czf /backup/openclaw-config-$(date +%Y%m%d).tar.gz \
  /opt/openclaw/conf/ \
  /etc/systemd/system/openclaw*.service

# Docker 配置备份
tar -czf /backup/openclaw-docker-config-$(date +%Y%m%d).tar.gz \
  /opt/openclaw/docker-compose.yml \
  /opt/openclaw/.env \
  /opt/openclaw/config/
```

### 完整备份
```bash
#!/bin/bash
# full_backup.sh - 完整备份脚本

BACKUP_DIR="/backup/openclaw/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

echo "开始备份..."

# 1. 备份数据库
echo "备份数据库..."
mysqldump -h localhost -u openclaw -p$DB_PASSWORD \
  --single-transaction openclaw | gzip > $BACKUP_DIR/database.sql.gz

# 2. 备份配置
echo "备份配置文件..."
tar -czf $BACKUP_DIR/config.tar.gz /opt/openclaw/conf/

# 3. 备份 Redis (如需要)
echo "备份 Redis..."
redis-cli -h localhost BGSAVE
sleep 5
cp /var/lib/redis/dump.rdb $BACKUP_DIR/redis.rdb

# 4. 生成备份清单
echo "生成备份清单..."
cat > $BACKUP_DIR/manifest.txt << EOF
备份时间: $(date)
数据库: database.sql.gz
配置: config.tar.gz
Redis: redis.rdb
OpenClaw 版本: $(curl -s http://localhost:8080/api/version | jq -r .version)
EOF

echo "备份完成: $BACKUP_DIR"
```

## 故障修复

### 服务无法启动

#### 端口占用
```bash
# 检查端口占用
netstat -tlnp | grep -E "8080|9090"
lsof -i :8080

# 杀死占用进程
kill -9 $(lsof -t -i :8080)

# 或修改配置使用其他端口
vim /opt/openclaw/conf/application.yml
# 修改 server.port
```

#### 配置错误
```bash
# 检查配置语法
/opt/openclaw/bin/openclaw-server.sh validate

# 查看启动日志
tail -100 /opt/openclaw/logs/openclaw-server.log

# 常见配置问题
# 1. YAML 格式错误 - 检查缩进
# 2. 数据库连接字符串错误
# 3. 环境变量未设置
```

#### 权限问题
```bash
# 修复目录权限
chown -R openclaw:openclaw /opt/openclaw
chmod 755 /opt/openclaw/bin/*.sh
chmod 644 /opt/openclaw/conf/*.yml

# 修复日志目录权限
chown -R openclaw:openclaw /opt/openclaw/logs
chmod 755 /opt/openclaw/logs
```

### 数据库问题修复

#### 连接失败
```bash
# 测试连接
mysql -h localhost -u openclaw -p -e "SELECT 1"

# 重置密码
mysql -u root -p << 'EOF'
ALTER USER 'openclaw'@'%' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
EOF

# 检查用户权限
mysql -u root -p -e "SHOW GRANTS FOR 'openclaw'@'%'"

# 修复权限
mysql -u root -p << 'EOF'
GRANT ALL PRIVILEGES ON openclaw.* TO 'openclaw'@'%';
FLUSH PRIVILEGES;
EOF
```

#### 表损坏修复
```bash
# 检查表状态
mysqlcheck -u root -p --check openclaw

# 修复表
mysqlcheck -u root -p --repair openclaw

# 修复特定表
mysqlcheck -u root -p --repair openclaw task
mysqlcheck -u root -p --repair openclaw execution
```

#### 数据不一致修复
```bash
# 清理僵尸任务（长时间 RUNNING 但 Worker 已下线）
mysql -u root -p openclaw << 'EOF'
UPDATE task SET status = 'FAILED',
  error_message = 'Worker offline - auto recovered'
WHERE status = 'RUNNING'
  AND worker_id NOT IN (SELECT id FROM worker WHERE status = 'ONLINE')
  AND update_time < DATE_SUB(NOW(), INTERVAL 1 HOUR);
EOF

# 重置卡住的调度任务
mysql -u root -p openclaw << 'EOF'
UPDATE task SET status = 'PENDING', worker_id = NULL
WHERE status = 'ASSIGNED'
  AND update_time < DATE_SUB(NOW(), INTERVAL 10 MINUTE);
EOF
```

### Redis 问题修复

#### 连接问题
```bash
# 测试连接
redis-cli -h localhost ping

# 重启 Redis
systemctl restart redis

# 检查 Redis 日志
tail -100 /var/log/redis/redis-server.log
```

#### 内存问题
```bash
# 检查内存使用
redis-cli info memory

# 清理过期 key
redis-cli --scan --pattern "openclaw:task:log:*" | xargs redis-cli del

# 设置内存策略
redis-cli config set maxmemory 2gb
redis-cli config set maxmemory-policy allkeys-lru
```

#### 数据恢复
```bash
# 从 RDB 恢复
systemctl stop redis
cp /backup/redis.rdb /var/lib/redis/dump.rdb
chown redis:redis /var/lib/redis/dump.rdb
systemctl start redis

# 验证恢复
redis-cli info keyspace
```

### Worker 故障修复

#### Worker 无法注册
```bash
# 检查网络连接
telnet openclaw-server 9090
nc -zv openclaw-server 9090

# 检查防火墙
iptables -L -n | grep 9090
firewall-cmd --list-ports

# 开放端口
firewall-cmd --add-port=9090/tcp --permanent
firewall-cmd --reload

# 检查 Worker 配置
grep -E "server|host|port" /opt/openclaw/conf/worker.yml
```

#### Worker 频繁离线
```bash
# 调整心跳配置
vim /opt/openclaw/conf/worker.yml
# 增加心跳间隔和超时时间
# heartbeat:
#   interval: 10000
#   timeout: 60000

# 检查系统资源
top -p $(pgrep -f openclaw-worker)
free -h

# 检查网络稳定性
ping -c 100 openclaw-server | tail -5
```

#### Worker 任务堆积
```bash
# 查看 Worker 负载
curl -s http://localhost:8080/api/workers | jq '.[] | {name, runningTasks, maxTasks}'

# 增加 Worker 线程数
vim /opt/openclaw/conf/worker.yml
# threads: 16

# 或扩容 Worker
docker-compose up -d --scale openclaw-worker=5
```

### 任务故障修复

#### 批量重试失败任务
```bash
# API 方式重试
curl -X POST http://localhost:8080/api/tasks/batch-retry \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"status": "FAILED", "startTime": "2024-01-15T00:00:00", "endTime": "2024-01-15T23:59:59"}'

# 数据库方式重置
mysql -u root -p openclaw << 'EOF'
UPDATE task SET status = 'PENDING', retry_count = 0, worker_id = NULL
WHERE status = 'FAILED'
  AND create_time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 23:59:59';
EOF
```

#### 清理过期任务
```bash
# 清理历史执行记录
mysql -u root -p openclaw << 'EOF'
DELETE FROM execution
WHERE create_time < DATE_SUB(NOW(), INTERVAL 30 DAY);
EOF

# 清理已完成任务日志
find /opt/openclaw/logs/tasks -name "*.log" -mtime +7 -delete
```

#### 终止卡住的任务
```bash
# API 方式终止
curl -X POST http://localhost:8080/api/tasks/12345/kill \
  -H "Authorization: Bearer ${TOKEN}"

# 批量终止
curl -X POST http://localhost:8080/api/tasks/batch-kill \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"taskIds": ["12345", "12346", "12347"]}'
```

## 高可用运维

### 主备切换
```bash
# 查看当前主节点
curl -s http://localhost:8080/api/cluster/leader | jq .

# 手动切换主节点（计划维护）
curl -X POST http://localhost:8080/api/admin/cluster/transfer-leader \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"targetNode": "node-2"}'

# 检查切换结果
curl -s http://localhost:8080/api/cluster/leader | jq .
```

### 节点上下线
```bash
# 优雅下线节点（不接收新任务，等待当前任务完成）
curl -X POST http://localhost:8080/api/admin/nodes/node-1/drain \
  -H "Authorization: Bearer ${TOKEN}"

# 检查节点状态
curl -s http://localhost:8080/api/admin/nodes/node-1/status | jq .

# 节点上线
curl -X POST http://localhost:8080/api/admin/nodes/node-1/resume \
  -H "Authorization: Bearer ${TOKEN}"
```

### 滚动升级
```bash
# Kubernetes 滚动升级
kubectl set image deployment/openclaw-server \
  openclaw-server=openclaw/openclaw-server:v2.0.0 -n openclaw

kubectl rollout status deployment/openclaw-server -n openclaw

# Docker Compose 滚动升级
docker-compose pull
docker-compose up -d --no-deps openclaw-worker
docker-compose up -d --no-deps openclaw-server

# 验证升级
curl -s http://localhost:8080/api/version | jq .
```

## 监控告警

### Prometheus 监控配置
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'openclaw'
    static_configs:
      - targets: ['openclaw-server:8080']
    metrics_path: '/actuator/prometheus'
```

### 告警规则
```yaml
# alerting_rules.yml
groups:
  - name: openclaw
    rules:
      - alert: OpenClawServerDown
        expr: up{job="openclaw"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "OpenClaw Server 宕机"

      - alert: OpenClawWorkerOffline
        expr: openclaw_worker_online_total < 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "所有 Worker 离线"

      - alert: OpenClawTaskQueueHigh
        expr: openclaw_task_queue_size > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "任务队列堆积"

      - alert: OpenClawTaskFailRateHigh
        expr: rate(openclaw_task_failed_total[5m]) / rate(openclaw_task_completed_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "任务失败率过高"
```

## 运维脚本

### 一键健康检查
```bash
#!/bin/bash
# health_check.sh

echo "=== OpenClaw 健康检查 ==="
echo "时间: $(date)"
echo ""

# 服务状态
echo "1. 服务状态"
systemctl is-active openclaw-server && echo "Server: 运行中" || echo "Server: 已停止"
systemctl is-active openclaw-worker && echo "Worker: 运行中" || echo "Worker: 已停止"
echo ""

# API 健康
echo "2. API 健康"
curl -s http://localhost:8080/api/health | jq .
echo ""

# 数据库连接
echo "3. 数据库连接"
mysql -u openclaw -p$DB_PASSWORD -e "SELECT 1" > /dev/null 2>&1 && echo "MySQL: 正常" || echo "MySQL: 异常"
echo ""

# Redis 连接
echo "4. Redis 连接"
redis-cli ping > /dev/null 2>&1 && echo "Redis: 正常" || echo "Redis: 异常"
echo ""

# 磁盘空间
echo "5. 磁盘空间"
df -h /opt/openclaw
echo ""

# 内存使用
echo "6. 内存使用"
free -h
echo ""

echo "=== 检查完成 ==="
```

## 运维检查清单

| 检查项 | 频率 | 命令/操作 |
|--------|------|-----------|
| 服务状态 | 每分钟 | 健康检查 API |
| 日志错误 | 每小时 | 检查 error.log |
| 磁盘空间 | 每天 | `df -h` |
| 数据库备份 | 每天 | 备份脚本 |
| 日志清理 | 每周 | 日志轮转 |
| 配置备份 | 每周 | 配置备份脚本 |
| 安全更新 | 每月 | 版本检查和升级 |
| 性能分析 | 每月 | 监控指标分析 |
