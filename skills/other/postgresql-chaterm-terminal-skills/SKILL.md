---
name: postgresql
description: PostgreSQL 数据库管理
version: 1.0.0
author: terminal-skills
tags: [database, postgresql, postgres, sql]
---

# PostgreSQL 数据库管理

## 概述
PostgreSQL 数据库管理、扩展使用、查询优化等技能。

## 连接管理

```bash
# 本地连接
psql -U postgres
psql -U username -d database

# 远程连接
psql -h hostname -p 5432 -U username -d database

# 执行 SQL 文件
psql -U username -d database -f script.sql

# 执行单条命令
psql -U username -d database -c "SELECT version();"
```

### psql 常用命令
```sql
\l              -- 列出数据库
\c dbname       -- 切换数据库
\dt             -- 列出表
\d tablename    -- 表结构
\du             -- 列出用户
\dn             -- 列出 schema
\df             -- 列出函数
\di             -- 列出索引
\q              -- 退出
\?              -- 帮助
\timing         -- 显示执行时间
\x              -- 扩展显示模式
```

## 用户与权限

```sql
-- 创建用户
CREATE USER username WITH PASSWORD 'password';
CREATE ROLE username WITH LOGIN PASSWORD 'password';

-- 创建超级用户
CREATE USER admin WITH SUPERUSER PASSWORD 'password';

-- 授权
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO username;
GRANT USAGE ON SCHEMA schema_name TO username;

-- 设置默认权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT ON TABLES TO readonly_user;

-- 查看权限
\du username
SELECT * FROM information_schema.role_table_grants WHERE grantee = 'username';

-- 修改密码
ALTER USER username WITH PASSWORD 'newpassword';
```

## 数据库操作

```sql
-- 创建数据库
CREATE DATABASE dbname;
CREATE DATABASE dbname OWNER username ENCODING 'UTF8';

-- 删除数据库
DROP DATABASE dbname;

-- 查看数据库大小
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) 
FROM pg_database ORDER BY pg_database_size(pg_database.datname) DESC;

-- 查看表大小
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) 
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;
```

## 备份与恢复

### pg_dump
```bash
# 备份单个数据库
pg_dump -U username dbname > backup.sql
pg_dump -U username -Fc dbname > backup.dump    # 自定义格式

# 备份所有数据库
pg_dumpall -U postgres > all_backup.sql

# 只备份结构
pg_dump -U username --schema-only dbname > schema.sql

# 只备份数据
pg_dump -U username --data-only dbname > data.sql

# 备份特定表
pg_dump -U username -t tablename dbname > table.sql

# 并行备份（大数据库）
pg_dump -U username -Fd -j 4 dbname -f backup_dir/
```

### 恢复
```bash
# 恢复 SQL 格式
psql -U username -d dbname < backup.sql

# 恢复自定义格式
pg_restore -U username -d dbname backup.dump

# 并行恢复
pg_restore -U username -d dbname -j 4 backup_dir/

# 恢复到新数据库
createdb -U postgres newdb
pg_restore -U postgres -d newdb backup.dump
```

## 性能监控

```sql
-- 当前连接
SELECT * FROM pg_stat_activity;
SELECT pid, usename, application_name, state, query 
FROM pg_stat_activity WHERE state != 'idle';

-- 终止连接
SELECT pg_terminate_backend(pid);

-- 锁信息
SELECT * FROM pg_locks WHERE NOT granted;

-- 查看锁等待
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.usename AS blocked_user,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 表统计
SELECT relname, seq_scan, idx_scan, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables;

-- 索引使用情况
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes;
```

## 查询优化

```sql
-- 执行计划
EXPLAIN SELECT * FROM table WHERE condition;
EXPLAIN ANALYZE SELECT * FROM table WHERE condition;
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM table;

-- 更新统计信息
ANALYZE tablename;
ANALYZE;

-- 重建索引
REINDEX TABLE tablename;
REINDEX DATABASE dbname;

-- VACUUM
VACUUM tablename;
VACUUM FULL tablename;              -- 回收空间
VACUUM ANALYZE tablename;           -- 同时更新统计
```

## 常见场景

### 场景 1：主从复制状态
```sql
-- 主库
SELECT * FROM pg_stat_replication;

-- 从库
SELECT * FROM pg_stat_wal_receiver;

-- 复制延迟
SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::INT AS lag_seconds;
```

### 场景 2：慢查询分析
```sql
-- 启用 pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- 查看慢查询
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC LIMIT 10;

-- 重置统计
SELECT pg_stat_statements_reset();
```

### 场景 3：表维护
```sql
-- 查看表膨胀
SELECT schemaname, relname, n_dead_tup, n_live_tup,
       round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- 清理膨胀
VACUUM FULL tablename;
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接数过多 | `pg_stat_activity`, 检查 max_connections |
| 查询慢 | `EXPLAIN ANALYZE`, 检查索引 |
| 锁等待 | `pg_locks`, `pg_stat_activity` |
| 磁盘满 | 检查 WAL、清理旧数据 |
| 复制延迟 | `pg_stat_replication` |
