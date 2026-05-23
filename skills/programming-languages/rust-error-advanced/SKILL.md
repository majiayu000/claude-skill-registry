---
name: rust-error-advanced
description: "深入错误处理专家。处理 Result vs Option, thiserror, anyhow, error context, library vs application errors, 错误处理, Result 用法, 什么时候用 panic"
globs: ["**/*.rs"]
---

# 深入错误处理

## 核心问题

**这个失败是预期的还是 bug？**

错误处理策略决定代码的健壮性。

---

## Result vs Option vs panic

| 类型 | 何时使用 | 示例 |
|-----|---------|-----|
| `Result<T, E>` | 预期会失败的操作 | 文件读取、网络请求 |
| `Option<T>` | absence 正常 | 查找、可能为空的值 |
| `panic!` | bug 或不变式违规 | 程序逻辑错误、不可恢复错误 |
| `unreachable!()` | 理论上不会执行到的代码 | 匹配穷举 |

---

## 错误处理决策

```
失败是预期的吗？
    │
    ├─ 是 → 这是库代码？
    │   ├─ 是 → thiserror（类型化错误）
    │   └─ 否 → anyhow（易用性）
    │
    ├─ 否，absence 正常？
    │   └─ Option<T>
    │
    └─ 否，bug 或不变式违规
        └─ panic!, assert!
```

---

## thiserror（库代码）

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("validation failed: {0}")]
    Validation(String),
    
    #[error("IO error: {source}")]
    Io {
        #[from]
        source: std::io::Error,
    },
    
    #[error("not found: {entity}:{id}")]
    NotFound {
        entity: String,
        id: u64,
    },
}

// 使用 ? 传播
fn read_config() -> Result<Config, MyError> {
    let content = std::fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}
```

---

## anyhow（应用代码）

```rust
use anyhow::{Context, Result, bail};

fn process_user(id: u64) -> Result<User> {
    let user = db.find_user(id)
        .with_context(|| format!("failed to find user {}", id))?;
    
    if !user.is_active {
        bail!("user {} is not active", id);
    }
    
    Ok(user)
}

// 组合多个错误源
fn complex_operation() -> Result<()> {
    let a = operation_a().context("operation A failed")?;
    let b = operation_b().context("operation B failed")?;
    Ok(())
}
```

---

## 错误设计原则

| 场景 | 建议 |
|-----|------|
| 库代码 | thiserror，精确的错误类型 |
| 应用代码 | anyhow，易于传播和添加上下文 |
| 库依赖库 | 传递第三方错误（`#[from]`） |
| 需要错误码 | 枚举变体 |
| 需要错误链 | `context()` + `with_context()` |

---

## 常见反模式

| 反模式 | 问题 | 解决 |
|-------|------|-----|
| 处处 `unwrap()` | 库中 panic | 用 `?` |
| `Box<dyn Error>` | 丢失类型信息 | thiserror 变体 |
| 丢失上下文 | 调试困难 | `.context()` |
| 错误变体过多 | 过度设计 | 简化或合并 |

---

## panic 使用场景

```rust
// 1. 不变量验证（公开 API）
pub fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        panic!("division by zero");  // 公开 API，确保调用者不传入 0
    }
    a / b
}

// 2. 不可恢复错误
fn start_engine() {
    let config = load_critical_config();
    if config.is_corrupted() {
        panic!("cannot start without valid config");
    }
}

// 3. 匹配穷举（理论上的永远执行不到）
fn process_status(status: Status) {
    match status {
        Status::Running => { /* ... */ }
        Status::Stopped => { /* ... */ }
        // 未来可能添加新状态
        // _ => unreachable!("unknown status: {:?}", status),
    }
}

// 4. 内部不变量
assert!(!queue.is_empty(), "queue should never be empty here");
```

---

## 错误链

```rust
// 使用 map_err 转换错误
fn high_level() -> Result<()> {
    low_level()
        .map_err(|e| MyError::from_low_level(e, "high level operation failed"))
}

// 使用 with_context 添加调用链信息
fn middle_layer() -> Result<()> {
    low_level()
        .with_context(|| format!("while processing request {}", request_id))?;
    Ok(())
}
```

---

## 最佳实践

1. **库代码**：精确的错误类型（thiserror）
2. **应用代码**：易用性优先（anyhow）
3. **传播错误**：用 `?` 而非 `unwrap()`
4. **添加上下文**：使用 `.context()` 或 `with_context()`
5. **保留错误源**：用 `#[from]` 保留底层错误
6. **区分 panic 场景**：bug 用 panic，预期失败用 Result

