---
name: redis
description: Redis 数据库管理
version: 1.0.0
author: terminal-skills
tags: [database, redis, cache, nosql, key-value]
---

# Redis 数据库管理

## 概述
Redis 命令、持久化、集群配置等技能。

## 连接管理

```bash
# 本地连接
redis-cli

# 远程连接
redis-cli -h hostname -p 6379
redis-cli -h hostname -p 6379 -a password

# 连接并选择数据库
redis-cli -n 1

# 执行单条命令
redis-cli ping
redis-cli get key

# 集群连接
redis-cli -c -h hostname -p 6379
```

## 基础命令

### 键操作
```bash
# 查看键
KEYS *                              # 所有键（生产慎用）
KEYS user:*                         # 匹配模式
SCAN 0 MATCH user:* COUNT 100       # 安全遍历

# 键信息
EXISTS key
TYPE key
TTL key                             # 剩余过期时间
PTTL key                            # 毫秒

# 键操作
DEL key
EXPIRE key 3600                     # 设置过期时间
PERSIST key                         # 移除过期时间
RENAME key newkey
```

### 字符串
```bash
SET key value
SET key value EX 3600               # 带过期时间
SETNX key value                     # 不存在时设置
GET key
MSET key1 val1 key2 val2
MGET key1 key2
INCR counter
INCRBY counter 10
DECR counter
APPEND key " suffix"
STRLEN key
```

### 哈希
```bash
HSET user:1 name "John" age 30
HGET user:1 name
HMSET user:1 name "John" age 30
HMGET user:1 name age
HGETALL user:1
HDEL user:1 age
HEXISTS user:1 name
HKEYS user:1
HVALS user:1
HINCRBY user:1 age 1
```

### 列表
```bash
LPUSH list value                    # 左侧插入
RPUSH list value                    # 右侧插入
LPOP list
RPOP list
LRANGE list 0 -1                    # 获取所有
LLEN list
LINDEX list 0
LSET list 0 newvalue
LTRIM list 0 99                     # 保留前100个
BLPOP list 10                       # 阻塞弹出
```

### 集合
```bash
SADD set member1 member2
SREM set member1
SMEMBERS set
SISMEMBER set member
SCARD set                           # 元素数量
SINTER set1 set2                    # 交集
SUNION set1 set2                    # 并集
SDIFF set1 set2                     # 差集
SRANDMEMBER set 3                   # 随机获取
```

### 有序集合
```bash
ZADD zset 100 member1 200 member2
ZREM zset member1
ZRANGE zset 0 -1                    # 按分数升序
ZRANGE zset 0 -1 WITHSCORES
ZREVRANGE zset 0 -1                 # 按分数降序
ZRANK zset member                   # 排名
ZSCORE zset member                  # 分数
ZCOUNT zset 100 200                 # 分数范围内数量
ZINCRBY zset 10 member
```

## 持久化

### RDB 快照
```bash
# 手动触发
SAVE                                # 阻塞
BGSAVE                              # 后台

# 配置 redis.conf
save 900 1                          # 900秒内1次修改
save 300 10                         # 300秒内10次修改
save 60 10000                       # 60秒内10000次修改

dbfilename dump.rdb
dir /var/lib/redis
```

### AOF 日志
```bash
# 配置 redis.conf
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec                # always/everysec/no

# AOF 重写
BGREWRITEAOF

# 自动重写配置
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

## 主从复制

```bash
# 从节点配置
REPLICAOF master_host master_port
REPLICAOF NO ONE                    # 取消复制

# 查看复制状态
INFO replication

# redis.conf 配置
replicaof master_host master_port
masterauth master_password
replica-read-only yes
```

## 集群管理

```bash
# 创建集群
redis-cli --cluster create \
    node1:6379 node2:6379 node3:6379 \
    node4:6379 node5:6379 node6:6379 \
    --cluster-replicas 1

# 集群信息
redis-cli -c cluster info
redis-cli -c cluster nodes

# 添加节点
redis-cli --cluster add-node new_node:6379 existing_node:6379

# 重新分片
redis-cli --cluster reshard node:6379

# 检查集群
redis-cli --cluster check node:6379
```

## 性能监控

```bash
# 服务器信息
INFO
INFO memory
INFO replication
INFO stats
INFO clients

# 实时监控
MONITOR                             # 实时命令（调试用）

# 慢查询
SLOWLOG GET 10
SLOWLOG LEN
SLOWLOG RESET

# 配置慢查询
CONFIG SET slowlog-log-slower-than 10000
CONFIG SET slowlog-max-len 128

# 内存分析
MEMORY USAGE key
MEMORY DOCTOR
DEBUG OBJECT key

# 客户端列表
CLIENT LIST
CLIENT KILL ID client_id
```

## 常见场景

### 场景 1：分布式锁
```bash
# 加锁
SET lock:resource unique_value NX EX 30

# 解锁（Lua 脚本保证原子性）
EVAL "if redis.call('get',KEYS[1]) == ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end" 1 lock:resource unique_value
```

### 场景 2：限流
```bash
# 滑动窗口限流
MULTI
ZADD rate_limit:user:1 timestamp timestamp
ZREMRANGEBYSCORE rate_limit:user:1 0 (timestamp-60000)
ZCARD rate_limit:user:1
EXPIRE rate_limit:user:1 60
EXEC
```

### 场景 3：缓存穿透防护
```bash
# 布隆过滤器（需要 RedisBloom 模块）
BF.ADD filter key
BF.EXISTS filter key

# 空值缓存
SET key "" EX 60                    # 缓存空值
```

### 场景 4：批量删除
```bash
# 使用 SCAN + DEL
redis-cli --scan --pattern "prefix:*" | xargs redis-cli DEL

# 使用 UNLINK（异步删除）
UNLINK key1 key2 key3
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 内存不足 | `INFO memory`, `MEMORY DOCTOR` |
| 连接数过多 | `INFO clients`, `CLIENT LIST` |
| 响应慢 | `SLOWLOG GET`, 检查大 key |
| 主从延迟 | `INFO replication` |
| 集群故障 | `CLUSTER INFO`, `CLUSTER NODES` |

```bash
# 查找大 key
redis-cli --bigkeys

# 内存分析
redis-cli --memkeys

# 延迟测试
redis-cli --latency
redis-cli --latency-history
```
