---
name: rust-lifetime-complex
description: "高级生命周期专家。处理 HRTB, GAT, 'static 约束, dyn trait object, 泛型边界冲突等问题。触发词：lifetime, HRTB, GAT, 'static, dyn, trait object, one type is more general, 生命周期, 类型约束"
globs: ["**/*.rs"]
---

# 高级生命周期与类型系统

## 核心问题

**为什么这个类型转换就是编译不过？**

类型系统的边界往往出乎意料。

---

## HRTB + dyn Trait Object 冲突

### 问题代码

```rust
// ❌ HRTB 不能装进 dyn trait object
pub type ConnFn<T> =
    dyn for<'c> FnOnce(&'c mut PgConnection) -> BoxFuture<'c, T> + Send;

let f = Box::new(move |conn: &mut PgConnection| -> BoxFuture<'_, i64> {
    Box::pin(async { Ok(42) })
}) as Box<ConnFn<i64>>;  // ❌ "one type is more general than the other"
```

### 原因

- 闭包有**具体生命周期** `'_`
- `ConnFn<T>` 要求**任意生命周期** `for<'c>`
- 具体不能自动变成通用

### 解决：把 HRTB 留在函数边界

```rust
// ✅ HRTB 只在调用点使用泛型
impl Db {
    pub async fn with_conn<F, T, Fut>(&self, f: F) -> Result<T, DbError>
    where
        F: for<'c> FnOnce(&'c mut PgConnection) -> Fut + Send,
        Fut: Future<Output = Result<T, DbError>> + Send,
    {
        let mut conn = self.pool.acquire().await?;
        f(&mut conn).await
    }
}
```

### 使用

```rust
db.with_conn(|conn| async move {
    // 这里 'c 由调用时确定，不需要 dyn
    sqlx::query("...").fetch_all(conn).await
}).await
```

---

## GAT + dyn Trait Object

### 问题代码

```rust
// ❌ GAT 不能和 dyn Trait 一起用
trait ReportRepo: Send + Sync {
    type Row<'r>: RowView<'r>;  // ❌ GAT
}

let repo: Arc<dyn ReportRepo> = ...;  // ❌ 编译错误
```

### 错误信息

```
error[E0038]: the trait cannot be made into an object
because associated type `Row` has generic parameters
```

### 原因

- `dyn ReportRepo` 需要统一大小
- `Row<'r>` 对不同 `'r` 有不同大小
- 对象安全规则禁止

### 解决：分层架构

```rust
// 内部：GAT + 借用（高性能）
trait InternalRepo {
    type Row<'r>: RowView<'r>;
    async fn query<'c>(&'c self) -> Vec<Self::Row<'c>>;
}

// 外部：owned DTO（兼容 GraphQL）
pub trait PublicRepo: Send + Sync {
    async fn query(&self) -> Vec<ReportDto>;  // owned
}

// 适配层
impl PublicRepo for PgRepo {
    async fn query(&self) -> Vec<ReportDto> {
        let rows = self.internal.query().await;  // 借用内部
        rows.into_iter().map(|r| r.to_dto()).collect()
    }
}
```

### 架构图

```
GraphQL Layer (需要 'static)
         ↓
    PublicRepo Trait (owned)
         ↓
    Adapter (转换 borrowed → owned)
         ↓
    InternalRepo Trait (GAT, borrowed)
         ↓
    DB Implementation
```

---

## 'static 要求冲突

### 场景

```rust
// async-graphql 要求 schema 是 'static
// 但 repo 方法返回借用数据
async fn resolve(&self) -> Result<&'r Row<'r>> {
    // ❌ 'r 不能 outlive 'static
}
```

### 解决：owned 数据

```rust
// 不要在 API 层暴露借用
async fn resolve(&self) -> Result<ReportDto> {
    let row = self.repo.query().await?;  // owned
    Ok(row.to_dto())
}
```

### 何时例外

- 仅在 **非常短期** 的借用（如单次函数调用内）
- **完全控制** 所有者和借用的生命周期
- **性能收益显著** 且不可替代

---

## 常见冲突模式

| 模式 | 冲突原因 | 解决 |
|-----|---------|-----|
| HRTB → dyn | 具体 vs 通用 | 泛型函数替代 dyn |
| GAT → dyn | 大小不固定 | 分层设计 |
| 'static + 借用 | 生命周期矛盾 | owned 数据 |
| async + 生命周期 | 协程持有状态 | drop 借用或 owned |
| closure 捕获 + Send | 生命周期问题 | 克隆或 'static |

---

## 何时放弃借用

### 性能 vs 可维护性

```rust
// 性能收益 vs 复杂性
fn should_borrow() -> bool {
    // 大数据结构 → 借用
    // 高频访问 → 借用
    // 生命周期简单 → 借用
    
    // 复杂生命周期 → owned
    // API 边界 → owned
    // 异步上下文 → owned
}
```

### 经验法则

1. **API 层**：默认 owned
2. **内部实现**：按需借用
3. **性能热点**：考虑借用
4. **复杂度高时**：退回到 owned

---

## 调试技巧

### 编译器错误

| 错误 | 含义 |
|-----|------|
| "one type is more general" | 试图把具体转通用 |
| "lifetime may not live long enough" | 借用超出范围 |
| "cannot be made into an object" | GAT + dyn 不兼容 |
| "does not live long enough" | 借用被提前释放 |

### 方法

1. **最小化**：写出最小复现代码
2. **标注生命周期**：显式写出所有生命周期
3. **逐步简化**：去掉抽象，直面问题
4. **接受现实**：不是所有设计都能编译

