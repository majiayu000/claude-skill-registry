---
name: sql-optimization
description: SQL 优化与调优
version: 1.0.0
author: terminal-skills
tags: [database, sql, optimization, performance, index]
---

# SQL 优化与调优

## 概述
慢查询分析、执行计划、索引优化等通用 SQL 优化技能。

## 执行计划分析

### MySQL EXPLAIN
```sql
-- 基础执行计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 详细执行计划
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- JSON 格式
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';

-- 关键字段解读
-- type: 访问类型 (system > const > eq_ref > ref > range > index > ALL)
-- key: 使用的索引
-- rows: 预估扫描行数
-- Extra: 额外信息 (Using index, Using filesort, Using temporary)
```

### PostgreSQL EXPLAIN
```sql
-- 基础执行计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 实际执行
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- 详细信息
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM users WHERE email = 'test@example.com';

-- 关键指标
-- Seq Scan: 全表扫描
-- Index Scan: 索引扫描
-- Bitmap Index Scan: 位图索引扫描
-- actual time: 实际执行时间
-- rows: 实际返回行数
```

## 索引优化

### 索引设计原则
```sql
-- 1. 选择性高的列优先
-- 选择性 = 不同值数量 / 总行数
SELECT COUNT(DISTINCT column) / COUNT(*) AS selectivity FROM table;

-- 2. 复合索引列顺序
-- 遵循最左前缀原则
-- 将选择性高的列放前面
CREATE INDEX idx_user ON users(status, created_at, name);

-- 3. 覆盖索引
-- 索引包含查询所需的所有列
CREATE INDEX idx_covering ON orders(user_id, status, amount);
SELECT user_id, status, amount FROM orders WHERE user_id = 1;

-- 4. 前缀索引（长字符串）
CREATE INDEX idx_email ON users(email(20));
```

### 索引使用检查
```sql
-- MySQL: 查看索引使用情况
SELECT * FROM sys.schema_index_statistics WHERE table_schema = 'mydb';

-- MySQL: 未使用的索引
SELECT * FROM sys.schema_unused_indexes WHERE object_schema = 'mydb';

-- PostgreSQL: 索引使用统计
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan;
```

### 索引失效场景
```sql
-- 1. 函数操作
-- 错误
SELECT * FROM users WHERE YEAR(created_at) = 2024;
-- 正确
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- 2. 隐式类型转换
-- 错误 (phone 是 varchar)
SELECT * FROM users WHERE phone = 13800138000;
-- 正确
SELECT * FROM users WHERE phone = '13800138000';

-- 3. LIKE 前缀通配符
-- 错误
SELECT * FROM users WHERE name LIKE '%john%';
-- 正确
SELECT * FROM users WHERE name LIKE 'john%';

-- 4. OR 条件
-- 可能不走索引
SELECT * FROM users WHERE status = 1 OR name = 'john';
-- 改写为 UNION
SELECT * FROM users WHERE status = 1
UNION
SELECT * FROM users WHERE name = 'john';

-- 5. NOT IN / NOT EXISTS
-- 尽量避免，改用 LEFT JOIN
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders);
-- 改写
SELECT u.* FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.id IS NULL;
```

## 查询优化

### SELECT 优化
```sql
-- 1. 只查询需要的列
-- 错误
SELECT * FROM users;
-- 正确
SELECT id, name, email FROM users;

-- 2. 避免 SELECT DISTINCT（考虑是否真的需要）
-- 检查是否有重复数据的根本原因

-- 3. 使用 LIMIT
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;

-- 4. 分页优化
-- 错误（大偏移量性能差）
SELECT * FROM users LIMIT 10000, 20;
-- 正确（使用游标分页）
SELECT * FROM users WHERE id > 10000 ORDER BY id LIMIT 20;
```

### JOIN 优化
```sql
-- 1. 小表驱动大表
-- 确保 JOIN 顺序合理

-- 2. 确保 JOIN 列有索引
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id  -- user_id 需要索引
WHERE u.status = 1;

-- 3. 避免过多 JOIN
-- 超过 3-4 个表的 JOIN 考虑拆分查询

-- 4. 使用 STRAIGHT_JOIN 强制顺序（MySQL）
SELECT STRAIGHT_JOIN u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id;
```

### 子查询优化
```sql
-- 1. 将子查询改为 JOIN
-- 错误
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);
-- 正确
SELECT DISTINCT u.* FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100;

-- 2. EXISTS 替代 IN（大数据集）
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.amount > 100
);
```

## 慢查询分析

### MySQL 慢查询
```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- 查看配置
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- 分析慢查询日志
-- mysqldumpslow -s t -t 10 /var/log/mysql/slow.log
```

### PostgreSQL 慢查询
```sql
-- 配置 postgresql.conf
-- log_min_duration_statement = 1000  # 记录超过1秒的查询

-- 使用 pg_stat_statements
CREATE EXTENSION pg_stat_statements;

SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

## 常见场景

### 场景 1：大表分页
```sql
-- 使用延迟关联
SELECT u.* FROM users u
JOIN (SELECT id FROM users ORDER BY created_at DESC LIMIT 10000, 20) t
ON u.id = t.id;

-- 使用游标分页
SELECT * FROM users
WHERE id > last_seen_id
ORDER BY id
LIMIT 20;
```

### 场景 2：批量更新
```sql
-- 分批更新，避免长事务
-- 每次更新 1000 条
UPDATE users SET status = 1 WHERE id BETWEEN 1 AND 1000;
UPDATE users SET status = 1 WHERE id BETWEEN 1001 AND 2000;
-- ...

-- 或使用存储过程循环
```

### 场景 3：统计查询优化
```sql
-- 使用汇总表
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY,
    total_orders INT,
    total_amount DECIMAL(10,2)
);

-- 定时任务更新汇总表
INSERT INTO daily_stats
SELECT DATE(created_at), COUNT(*), SUM(amount)
FROM orders
WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY
GROUP BY DATE(created_at)
ON DUPLICATE KEY UPDATE
    total_orders = VALUES(total_orders),
    total_amount = VALUES(total_amount);
```

### 场景 4：锁优化
```sql
-- 减少锁范围
-- 错误：锁定整个表
SELECT * FROM users FOR UPDATE;

-- 正确：只锁定需要的行
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- 使用乐观锁
UPDATE users SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 5;
```

## 优化检查清单

| 检查项 | 说明 |
|--------|------|
| 执行计划 | 是否全表扫描、是否使用索引 |
| 索引设计 | 选择性、覆盖索引、复合索引顺序 |
| 查询改写 | 避免 SELECT *、优化子查询 |
| 分页方式 | 大偏移量使用游标分页 |
| 批量操作 | 分批处理、避免长事务 |
| 锁粒度 | 减少锁范围、使用乐观锁 |
