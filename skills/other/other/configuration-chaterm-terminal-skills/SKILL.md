---
name: configuration
description: OpenClaw 配置管理
version: 1.0.0
author: terminal-skills
tags: [openclaw, configuration, settings, tuning]
---

# OpenClaw 配置管理

## 概述
OpenClaw 的核心配置、环境变量、性能调优和安全配置指南。

## 核心配置文件

### application.yml 结构
```yaml
# /opt/openclaw/conf/application.yml

server:
  port: 8080
  grpc:
    port: 9090
  servlet:
    context-path: /

spring:
  application:
    name: openclaw-server
  datasource:
    url: jdbc:mysql://localhost:3306/openclaw?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: openclaw
    password: your_password
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      idle-timeout: 300000
      connection-timeout: 30000
      max-lifetime: 1800000

  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    lettuce:
      pool:
        max-active: 16
        max-idle: 8
        min-idle: 2

openclaw:
  # 集群配置
  cluster:
    name: openclaw-cluster
    node-id: ${HOSTNAME:node-1}
    heartbeat-interval: 10000

  # 调度配置
  scheduler:
    thread-pool-size: 20
    max-retry-times: 3
    retry-interval: 30000
    task-timeout: 3600000

  # 执行器配置
  executor:
    max-concurrent-tasks: 100
    task-queue-size: 10000

  # 日志配置
  logging:
    level: INFO
    retention-days: 30
    max-file-size: 100MB
```

### Worker 配置
```yaml
# /opt/openclaw/conf/worker.yml

worker:
  # 服务端连接
  server:
    host: openclaw-server
    port: 9090

  # Worker 配置
  group: default
  name: ${HOSTNAME:worker-1}
  threads: 8
  max-tasks: 50

  # 心跳配置
  heartbeat:
    interval: 5000
    timeout: 30000

  # 任务配置
  task:
    temp-dir: /tmp/openclaw
    log-dir: /opt/openclaw/logs/tasks
    max-log-size: 10MB
```

## 环境变量配置

### Server 环境变量
```bash
# 数据库配置
export OPENCLAW_DB_HOST=localhost
export OPENCLAW_DB_PORT=3306
export OPENCLAW_DB_NAME=openclaw
export OPENCLAW_DB_USER=openclaw
export OPENCLAW_DB_PASSWORD=your_password

# Redis 配置
export OPENCLAW_REDIS_HOST=localhost
export OPENCLAW_REDIS_PORT=6379
export OPENCLAW_REDIS_PASSWORD=

# 服务配置
export OPENCLAW_PORT=8080
export OPENCLAW_GRPC_PORT=9090

# JVM 配置
export JAVA_OPTS="-Xms1g -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"

# 日志级别
export LOG_LEVEL=INFO
```

### Worker 环境变量
```bash
# Server 连接
export OPENCLAW_SERVER_HOST=openclaw-server
export OPENCLAW_SERVER_PORT=9090

# Worker 配置
export WORKER_GROUP=default
export WORKER_NAME=worker-1
export WORKER_THREADS=8

# 任务配置
export TASK_TEMP_DIR=/tmp/openclaw
export TASK_LOG_DIR=/opt/openclaw/logs/tasks
```

### Docker 环境变量传递
```bash
# docker-compose.yml 方式
docker-compose up -d

# 或直接传递
docker run -d \
  -e OPENCLAW_DB_HOST=mysql \
  -e OPENCLAW_DB_PASSWORD=password \
  -e JAVA_OPTS="-Xms1g -Xmx2g" \
  openclaw/openclaw-server:latest
```

## 数据库配置

### 连接池配置
```yaml
spring:
  datasource:
    hikari:
      # 最大连接数
      maximum-pool-size: 20
      # 最小空闲连接
      minimum-idle: 5
      # 空闲超时 (5分钟)
      idle-timeout: 300000
      # 连接超时 (30秒)
      connection-timeout: 30000
      # 连接最大生命周期 (30分钟)
      max-lifetime: 1800000
      # 连接池名称
      pool-name: OpenClawHikariPool
      # 连接测试查询
      connection-test-query: SELECT 1
```

### 多数据源配置
```yaml
spring:
  datasource:
    primary:
      url: jdbc:mysql://master:3306/openclaw
      username: openclaw
      password: password
    secondary:
      url: jdbc:mysql://slave:3306/openclaw
      username: openclaw
      password: password
      read-only: true
```

### 数据库优化参数
```sql
-- MySQL 推荐配置
SET GLOBAL innodb_buffer_pool_size = 1G;
SET GLOBAL innodb_log_file_size = 256M;
SET GLOBAL max_connections = 500;
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
SET GLOBAL sync_binlog = 0;
```

## Redis 配置

### 单机配置
```yaml
spring:
  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    timeout: 10000
    lettuce:
      pool:
        max-active: 16
        max-idle: 8
        min-idle: 2
        max-wait: 10000
```

### 集群配置
```yaml
spring:
  redis:
    cluster:
      nodes:
        - redis-node-1:6379
        - redis-node-2:6379
        - redis-node-3:6379
      max-redirects: 3
    lettuce:
      cluster:
        refresh:
          adaptive: true
          period: 30000
```

### 哨兵配置
```yaml
spring:
  redis:
    sentinel:
      master: mymaster
      nodes:
        - sentinel-1:26379
        - sentinel-2:26379
        - sentinel-3:26379
    password: redis_password
```

## 调度器配置

### 基础配置
```yaml
openclaw:
  scheduler:
    # 调度线程池大小
    thread-pool-size: 20

    # 任务重试配置
    max-retry-times: 3
    retry-interval: 30000

    # 任务超时 (1小时)
    task-timeout: 3600000

    # 任务队列
    queue-capacity: 10000

    # 调度策略
    strategy: ROUND_ROBIN  # ROUND_ROBIN, RANDOM, LEAST_LOAD, CONSISTENT_HASH
```

### 高级调度策略
```yaml
openclaw:
  scheduler:
    # 故障转移
    failover:
      enabled: true
      max-attempts: 3

    # 负载均衡
    load-balance:
      strategy: LEAST_LOAD
      weight-enabled: true

    # 任务分片
    sharding:
      enabled: true
      default-count: 10
```

## 执行器配置

### Worker 执行器
```yaml
openclaw:
  executor:
    # 并发任务数
    max-concurrent-tasks: 100

    # 任务队列大小
    task-queue-size: 10000

    # 线程池配置
    core-pool-size: 10
    max-pool-size: 50
    keep-alive-time: 60

    # 任务类型执行器
    handlers:
      shell:
        enabled: true
        timeout: 3600
      http:
        enabled: true
        timeout: 300
        max-connections: 100
      python:
        enabled: true
        interpreter: /usr/bin/python3
```

## 日志配置

### Logback 配置
```xml
<!-- /opt/openclaw/conf/logback-spring.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property name="LOG_PATH" value="/opt/openclaw/logs"/>
    <property name="LOG_PATTERN" value="%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n"/>

    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
        </encoder>
    </appender>

    <!-- 文件输出 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_PATH}/openclaw.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_PATH}/openclaw.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
        </encoder>
    </appender>

    <!-- 错误日志单独记录 -->
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_PATH}/error.log</file>
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>ERROR</level>
        </filter>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_PATH}/error.%d{yyyy-MM-dd}.log.gz</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
        <appender-ref ref="ERROR_FILE"/>
    </root>

    <!-- 特定包日志级别 -->
    <logger name="com.openclaw" level="DEBUG"/>
    <logger name="org.springframework" level="WARN"/>
    <logger name="org.hibernate" level="WARN"/>
</configuration>
```

## 安全配置

### 认证配置
```yaml
openclaw:
  security:
    # JWT 配置
    jwt:
      secret: your-secret-key-at-least-256-bits
      expiration: 86400000  # 24小时
      refresh-expiration: 604800000  # 7天

    # 密码策略
    password:
      min-length: 8
      require-uppercase: true
      require-lowercase: true
      require-digit: true
      require-special: false

    # 登录限制
    login:
      max-attempts: 5
      lock-duration: 1800000  # 30分钟
```

### HTTPS 配置
```yaml
server:
  ssl:
    enabled: true
    key-store: classpath:keystore.p12
    key-store-password: changeit
    key-store-type: PKCS12
    key-alias: openclaw
```

### CORS 配置
```yaml
openclaw:
  cors:
    allowed-origins:
      - http://localhost:3000
      - https://openclaw.example.com
    allowed-methods:
      - GET
      - POST
      - PUT
      - DELETE
    allowed-headers: "*"
    allow-credentials: true
    max-age: 3600
```

## 性能调优

### JVM 调优
```bash
# 生产环境推荐配置
JAVA_OPTS="-server \
  -Xms4g -Xmx4g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+ParallelRefProcEnabled \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/opt/openclaw/logs/heapdump.hprof \
  -Djava.net.preferIPv4Stack=true"
```

### 线程池调优
```yaml
openclaw:
  thread-pool:
    scheduler:
      core-size: 20
      max-size: 50
      queue-capacity: 1000
    executor:
      core-size: 50
      max-size: 200
      queue-capacity: 5000
    async:
      core-size: 10
      max-size: 30
      queue-capacity: 500
```

## 配置热更新

### 动态配置
```bash
# 通过 API 更新配置
curl -X PUT http://localhost:8080/api/admin/config \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "key": "scheduler.thread-pool-size",
    "value": "30"
  }'

# 查看当前配置
curl http://localhost:8080/api/admin/config \
  -H "Authorization: Bearer ${TOKEN}"

# 刷新配置
curl -X POST http://localhost:8080/api/admin/config/refresh \
  -H "Authorization: Bearer ${TOKEN}"
```

## 配置验证

### 检查配置
```bash
# 验证配置文件语法
/opt/openclaw/bin/openclaw-server.sh validate

# 测试数据库连接
/opt/openclaw/bin/openclaw-server.sh test-db

# 测试 Redis 连接
/opt/openclaw/bin/openclaw-server.sh test-redis

# 查看生效的配置
curl http://localhost:8080/api/admin/config/effective \
  -H "Authorization: Bearer ${TOKEN}"
```

## 常用配置模板

| 场景 | 关键配置 |
|------|----------|
| 开发环境 | `LOG_LEVEL=DEBUG`, 小内存配置 |
| 测试环境 | 中等资源配置，启用详细日志 |
| 生产环境 | 高可用配置，优化性能参数 |
| 高并发 | 增大线程池，连接池，队列大小 |
| 低延迟 | 减小心跳间隔，快速故障检测 |
