---
name: efcore-data-access
description: EF Core 数据访问与性能最佳实践：查询形状、No-Tracking、投影、Split Query、N+1 规避、编译查询等。
---

# EF Core 数据访问

此 skill 用于编写“高可维护 + 高性能 + 可测试”的 EF Core 数据访问层。

## 何时使用此 Skill

- 新增/优化 EF Core 查询与仓储实现
- 出现 N+1、笛卡尔爆炸（cartesian explosion）、慢查询、内存膨胀
- 需要规范读取/写入边界、追踪策略（tracking/no-tracking）

## 核心最佳实践（含权威依据）

### 1) 只取需要的数据：投影（Select）优先

- 避免把大列/无关列一起取回导致网络与内存浪费。

### 2) 只读用 No-Tracking

- 读取场景优先 `AsNoTracking()`，减少 ChangeTracker 负担。

参考：ASP.NET Core Best Practices（Optimize data access and I/O）建议只读使用 no-tracking 查询。

### 3) 避免 JOIN 引发的 cartesian explosion：Split Query

- 多集合 Include 时考虑 `AsSplitQuery()`。
- 注意：Split Query 会带来多次 roundtrip，且在并发更新下可能导致不一致，需要在一致性要求高时用事务隔离级别缓解。

参考：EF Core 文档 Single vs. Split Queries（性能问题与权衡）。

### 4) 流式 vs 缓冲

- 大结果集尽量避免过早 `ToList/ToArray`，否则会不必要地缓冲并放大内存使用。

参考：EF Core Efficient Querying（Buffering and streaming）。

### 5) 高性能场景：Compiled Queries & Pooling

- 极高 QPS 场景可用编译查询减少查询树处理开销（先 benchmark）。
- 考虑使用 `DbContext Pooling` 减少上下文创建开销。

参考：EF Core Advanced Performance Topics（Compiled queries / DbContext pooling）。

### 6) 数据库端求值 (Database-side Evaluation)

- 确保 `.Where`, `.Select`, `.Sum` 等过滤与聚合逻辑在 LINQ to Entities 中正确转换，避免回流到客户端执行（Client Evaluation）。

### 7) 批量与流式处理

- 大规模查询必须配合 `.Skip(n).Take(m)` 进行分页。
- 只有在确认数据量极小或必须在内存中全量操作时才调用 `ToList()`；默认应保持 `IQueryable` 或使用 `IAsyncEnumerable`。

## 常见反模式

- 在循环里按 ID 单条查询（典型 N+1）
- Include 多个同级集合导航导致返回行数爆炸
- 读写混用 tracking，但又不保存，造成不必要的开销

## 使用示例（提示语模板）

- “请帮我找出这段 EF 查询的 N+1 风险，并改成一次性批量查询 + 合理投影。”
- “这个查询 Include 两个集合很慢：解释原因，并给出 AsSplitQuery 或重写投影的方案与权衡。”
