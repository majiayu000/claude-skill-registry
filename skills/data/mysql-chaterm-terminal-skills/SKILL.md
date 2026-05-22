---
name: mysql
description: MySQL 数据库管理与运维
version: 1.0.0
author: terminal-skills
tags: [database, mysql, mariadb, sql]
---

# MySQL 数据库管理

## 概述
MySQL/MariaDB 数据库的日常管理、备份恢复、性能调优等运维技能。

## 连接管理

```bash
# 本地连接
mysql -u root -p

# 远程连接
mysql -h hostname -P 3306 -u user -p database

# 执行 SQL 文件
mysql -u user -p database < script.sql

# 执行单条命令
mysql -u user -p -e "SHOW DATABASES;"
```

## 用户与权限

```sql
-- 查看用户
SELECT user, host FROM mysql.user;

-- 创建用户
CREATE USER 'username'@'%' IDENTIFIED BY 'password';

-- 授权
GRANT ALL PRIVILEGES ON database.* TO 'username'@'%';
GRANT SELECT, INSERT ON database.table TO 'username'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 查看权限
SHOW GRANTS FOR 'username'@'%';
```

## 数据库操作

```sql
-- 数据库管理
SHOW DATABASES;
CREATE DATABASE dbname CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
DROP DATABASE dbname;
USE dbname;

-- 表管理
SHOW TABLES;
DESCRIBE tablename;
SHOW CREATE TABLE tablename;
```

## 备份与恢复

### mysqldump 备份
```bash
# 备份单个数据库
mysqldump -u root -p database > backup.sql

# 备份所有数据库
mysqldump -u root -p --all-databases > all_backup.sql

# 备份表结构
mysqldump -u root -p --no-data database > schema.sql

# 压缩备份
mysqldump -u root -p database | gzip > backup.sql.gz
```

### 恢复
```bash
# 恢复数据库
mysql -u root -p database < backup.sql

# 从压缩文件恢复
gunzip < backup.sql.gz | mysql -u root -p database
```

## 性能监控

```sql
-- 查看进程
SHOW PROCESSLIST;
SHOW FULL PROCESSLIST;

-- 查看状态
SHOW STATUS;
SHOW GLOBAL STATUS LIKE 'Threads%';
SHOW GLOBAL STATUS LIKE 'Connections';

-- 查看变量
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE '%buffer%';

-- 慢查询
SHOW VARIABLES LIKE 'slow_query%';
SHOW GLOBAL STATUS LIKE 'Slow_queries';
```

## 常见场景

### 场景 1：排查慢查询
```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- 查看慢查询日志位置
SHOW VARIABLES LIKE 'slow_query_log_file';

-- 分析执行计划
EXPLAIN SELECT * FROM table WHERE condition;
EXPLAIN ANALYZE SELECT * FROM table WHERE condition;
```

### 场景 2：锁问题排查
```sql
-- 查看锁等待
SHOW ENGINE INNODB STATUS\G

-- 查看当前锁
SELECT * FROM information_schema.INNODB_LOCKS;
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- 查看事务
SELECT * FROM information_schema.INNODB_TRX;
```

### 场景 3：主从复制状态
```sql
-- 主库状态
SHOW MASTER STATUS;

-- 从库状态
SHOW SLAVE STATUS\G

-- 关键指标
-- Slave_IO_Running: Yes
-- Slave_SQL_Running: Yes
-- Seconds_Behind_Master: 0
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接数过多 | `SHOW PROCESSLIST`, 检查 max_connections |
| 查询慢 | `EXPLAIN`, 检查索引 |
| 锁等待 | `SHOW ENGINE INNODB STATUS` |
| 复制延迟 | `SHOW SLAVE STATUS`, 检查网络和负载 |
| 磁盘满 | 检查 binlog, 清理旧日志 |
