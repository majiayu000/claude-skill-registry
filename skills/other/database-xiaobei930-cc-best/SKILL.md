---
name: database
description: "Database design, query optimization, migrations, and indexing. Use when designing schemas, writing queries, or managing migrations."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 数据库模式技能

> 关联 Agent: `architect` — 架构设计时加载数据库约束上下文

本技能提供数据库设计和操作的最佳实践，支持多数据库按需加载。

## 触发条件

- 设计数据库 Schema
- 编写数据库查询
- 优化查询性能
- 管理数据库迁移
- 配置索引

## 数据库专属模式

根据项目技术栈，加载对应的数据库专属文件：

| 数据库     | 加载文件      | 适用场景               |
| ---------- | ------------- | ---------------------- |
| PostgreSQL | `postgres.md` | 企业应用、复杂查询     |
| MySQL      | `mysql.md`    | Web 应用、读多写少     |
| Oracle     | `oracle.md`   | 大型企业、高并发 OLTP  |
| SQLite     | `sqlite.md`   | 嵌入式、移动端、本地化 |

**检测方式**: 根据连接字符串、ORM 配置或项目依赖确定数据库类型。

---

## 通用 Schema 设计

### 命名规范

```sql
-- 表名：小写下划线，复数形式
users, order_items, user_preferences

-- 列名：小写下划线
created_at, updated_at, user_id, is_active

-- 索引名：idx_表名_列名
idx_users_email, idx_orders_user_id_created_at

-- 外键名：fk_表名_关联表
fk_orders_users
```

### 必备字段

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,           -- 主键
    -- 业务字段...
    created_at TIMESTAMP NOT NULL,   -- 创建时间
    updated_at TIMESTAMP NOT NULL,   -- 更新时间
    deleted_at TIMESTAMP             -- 软删除
);
```

### 关系设计

| 关系类型 | 设计方式          | 示例                         |
| -------- | ----------------- | ---------------------------- |
| 一对多   | 子表添加外键      | orders.user_id → users       |
| 多对多   | 中间表 + 联合主键 | user_roles(user_id, role_id) |
| 一对一   | 子表主键 = 外键   | user_settings.user_id        |

---

## 通用索引策略

### 何时创建索引

- ✅ WHERE 条件频繁使用的列
- ✅ JOIN 关联的列
- ✅ ORDER BY / GROUP BY 的列
- ❌ 很少查询的列
- ❌ 值重复率高的列（如性别）
- ❌ 频繁更新的列

### 索引类型选择

| 查询模式            | 推荐索引      |
| ------------------- | ------------- |
| `WHERE col = value` | B-tree        |
| `WHERE col > value` | B-tree        |
| 全文搜索            | 全文索引      |
| JSON 字段查询       | GIN/JSON 索引 |
| 时序数据范围查询    | BRIN（PG）    |

### 复合索引原则

```sql
-- 规则：等值列在前，范围列在后
-- 查询：WHERE status = 'active' AND created_at > '2024-01-01'

-- ✅ 正确顺序
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- ❌ 错误顺序（范围列在前会导致后续列无法使用索引）
CREATE INDEX idx_orders_created_status ON orders(created_at, status);
```

---

## N+1 问题

### 问题示例

```
获取 100 个用户及其订单：
1 次查询获取用户 + 100 次查询获取每个用户的订单 = 101 次查询
```

### 解决方案

| 方案     | 方式            | 适用场景       |
| -------- | --------------- | -------------- |
| 预加载   | JOIN 或 IN 查询 | 数据量适中     |
| 批量加载 | 分批 IN 查询    | 大数据量       |
| 延迟加载 | 按需查询        | 不确定是否需要 |

---

## 分页优化

```sql
-- ❌ 大偏移量慢（OFFSET 10000 需要扫描 10000 行）
SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 10000;

-- ✅ 游标分页（直接定位）
SELECT * FROM posts WHERE id > 10000 ORDER BY id LIMIT 20;
```

---

## 事务原则

### ACID 特性

| 特性     | 含义               |
| -------- | ------------------ |
| A 原子性 | 全部成功或全部失败 |
| C 一致性 | 数据始终有效       |
| I 隔离性 | 事务互不干扰       |
| D 持久性 | 提交后永久保存     |

### 隔离级别

| 级别             | 脏读 | 不可重复读 | 幻读 | 性能 |
| ---------------- | ---- | ---------- | ---- | ---- |
| READ UNCOMMITTED | ✓    | ✓          | ✓    | 最高 |
| READ COMMITTED   | ✗    | ✓          | ✓    | 高   |
| REPEATABLE READ  | ✗    | ✗          | ✓    | 中   |
| SERIALIZABLE     | ✗    | ✗          | ✗    | 低   |

---

## 迁移管理

### 迁移原则

1. **版本控制** - 所有迁移文件纳入 Git
2. **只增不改** - 不修改已执行的迁移
3. **可回滚** - 每个 UP 对应 DOWN
4. **原子性** - 一个迁移只做一件事

### 常用 ORM 命令

```bash
# Prisma
npx prisma migrate dev --name add_column

# SQLAlchemy/Alembic
alembic revision --autogenerate -m "add column"
alembic upgrade head

# TypeORM
npm run typeorm migration:generate -- -n AddColumn
npm run typeorm migration:run
```

---

## 最佳实践清单

- [ ] 表名/列名统一命名规范
- [ ] 必备字段：id, created_at, updated_at
- [ ] 软删除而非物理删除
- [ ] 基于查询模式创建索引
- [ ] 避免 N+1 查询
- [ ] 大数据量使用游标分页
- [ ] 迁移文件纳入版本控制
- [ ] 合理配置连接池
- [ ] 使用 EXPLAIN 分析慢查询

---

## 数据库专属内容

详细的数据库专属实现请参考：

- **PostgreSQL**: [postgres.md](./postgres.md) - 数据类型、索引策略、RLS、性能诊断
- **MySQL**: [mysql.md](./mysql.md) - InnoDB 优化、索引策略、字符集
- **Oracle**: [oracle.md](./oracle.md) - 分区表、全局索引、PL/SQL
- **SQLite**: [sqlite.md](./sqlite.md) - WAL 模式、PRAGMA 优化、嵌入式场景

> **记住**: 数据库设计是系统的地基——索引、约束、迁移策略在上线前就要规划好。
