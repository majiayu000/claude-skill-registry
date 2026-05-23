---
name: rust-error
description: "错误处理专家。处理 Result, Option, panic, anyhow, thiserror, 自定义错误, 错误传播等问题。触发词：Result, Error, panic, ?, unwrap, expect, anyhow, thiserror, error handling, 错误处理, 错误类型"
globs: ["**/*.rs"]
---

# Rust 错误处理

## 核心问题

**这个失败是预期的还是意外？**

- 预期的 → 用 `Result`
-  absence 正常 → 用 `Option`
- bug/不可恢复 → `panic!`

---

## Result vs Option

### Option 用于 "absence 是正常的"

```rust
// 查找操作，找不到是正常情况
fn find_user(id: u32) -> Option<User> {
    users.get(&id)
}

// 使用
let user = find_user(123);
if let Some(u) = user {
    println!("Found: {}", u.name);
}

// 或者用 ? 传播（但要包装成 Result）
let user = find_user(123).ok_or(UserNotFound)?;
```

### Result 用于 "可能失败"

```rust
// 文件可能不存在
fn read_file(path: &Path) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}

// 网络请求可能超时
fn fetch(url: &str) -> Result<Response, reqwest::Error> {
    reqwest::blocking::get(url)?
}
```

---

## 错误类型选择

### 库代码 → thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("invalid format: {0}")]
    InvalidFormat(String),
    
    #[error("missing field: {0}")]
    MissingField(&'static str),
    
    #[error("IO error: {source}")]
    Io {
        #[from]
        source: io::Error,
    },
}
```

### 应用代码 → anyhow

```rust
use anyhow::{Context, Result, bail};

fn process_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.json")
        .context("failed to read config file")?;
    
    let config: Config = serde_json::from_str(&content)
        .context("failed to parse config")?;
    
    Ok(config)
}
```

### 混合场景

库内部用 anyhow 快速开发，公共 API 用 thiserror。

---

## 错误传播最佳实践

```rust
// ✅ 好：明确区分错误类型
fn validate() -> Result<(), ValidationError> {
    if name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    Ok(())
}

// ✅ 好：传播时添加上下文
let config = File::open("config.json")
    .map_err(|e| ConfigError::with_context("config", e))?;

// ✅ 好：使用 ? 运算符
let data = read_file(&path)?;

// ❌ 差：unwrap() 在可能失败的操作上
let content = std::fs::read_to_string("config.json").unwrap();

// ❌ 差：静默忽略错误
let _ = some_fallible_function();
```

---

## 什么时候 panic

| 场景 | 示例 | 理由 |
|-----|------|-----|
| 不变量违反 | 配置文件验证失败 | 程序无法继续 |
| 初始化检查 | `EXPECTED_ENV.is_set()` | 配置问题需要修复 |
| 测试 | `assert_eq!` | 验证假设 |
| 不可恢复 | 连接意外断开 | 最好让程序崩溃 |

```rust
// ✅ 可接受：初始化检查
let home = std::env::var("HOME")
    .expect("HOME environment variable must be set");

// ✅ 可接受：测试断言
assert!(!users.is_empty(), "should have at least one user");

// ❌ 不可接受：用户输入验证失败
let num: i32 = input.parse().unwrap();
```

---

## 反模式

| 反模式 | 问题 | 正确做法 |
|-------|------|---------|
| `.unwrap()` 到处都是 | 生产环境 panic | `?` 或 `with_context()` |
| `Box<dyn Error>` | 丢失类型信息 | thiserror 枚举 |
| 静默忽略错误 | bug 隐藏 | 处理或传播 |
| 错误类型层次过深 | 过度设计 | 按需设计 |
| panic 用于流程控制 | 滥用 panic | 正常控制流 |

---

## 快速参考

| 场景 | 选择 | 工具 |
|-----|------|-----|
| 库返回自定义错误 | `Result<T, Enum>` | thiserror |
| 应用快速开发 | `Result<T, anyhow::Error>` | anyhow |
| absence 正常 | `Option<T>` | `None` / `Some(x)` |
| 预期 panic | `panic!` / `assert!` | 仅限特殊情况 |
| 错误转换 | `.map_err()` / `.with_context()` | 添加上下文 |

