---
name: supabase-postgres-best-practices
description: "Supabase 出品的 Postgres 性能优化与最佳实践。在编写、评审或优化 Postgres 查询、表结构设计或数据库配置时使用。"
license: MIT
---

# Supabase Postgres 最佳实践

面向 Postgres 的性能优化指南，由 Supabase 维护。包含 8 大类规则，按影响程度排序，用于指导自动化查询优化与表结构设计。

## 何时使用

在以下场景参考本指南：
- 编写 SQL 查询或设计表结构
- 实现索引或查询优化
- 排查数据库性能问题
- 配置连接池或扩展
- 利用 Postgres 特有功能做优化
- 使用行级安全（RLS）

## 规则类别与优先级

| 优先级 | 类别 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | 查询性能 | 关键 | `query-` |
| 2 | 连接管理 | 关键 | `conn-` |
| 3 | 安全与 RLS | 关键 | `security-` |
| 4 | 表结构设计 | 高 | `schema-` |
| 5 | 并发与锁 | 中高 | `lock-` |
| 6 | 数据访问模式 | 中 | `data-` |
| 7 | 监控与诊断 | 低中 | `monitor-` |
| 8 | 高级特性 | 低 | `advanced-` |

## 使用方式

阅读单条规则文件获取说明与 SQL 示例：

```
rules/query-missing-indexes.md
rules/query-partial-indexes.md
rules/_sections.md
```

每条规则包含：为何重要、错误 SQL 示例、正确 SQL 示例、可选的 EXPLAIN 输出或指标、补充说明与参考、以及适用时的 Supabase 说明。

完整展开版见 `rules/` 目录下各 .md 规则文件。
