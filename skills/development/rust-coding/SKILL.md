---
name: rust-coding
description: "Rust 编码规范专家。处理命名, 格式化, 注释, clippy, rustfmt, lint, 代码风格, 最佳实践, naming convention, 代码审查, P.NAM, G.FMT, 怎么命名, 代码规范"
globs: ["**/*.rs"]
---

# Rust 编码规范

## 核心问题

**什么样的 Rust 代码才是"惯用的"？**

遵循社区约定，让代码可读、可维护。

---

## 命名规范 (Rust 特有)

| 规则 | 正确 | 错误 |
|-----|------|------|
| 方法不用 `get_` 前缀 | `fn name(&self)` | `fn get_name(&self)` |
| 迭代器方法 | `iter()` / `iter_mut()` / `into_iter()` | `get_iter()` |
| 转换命名 | `as_` (廉价), `to_` (昂贵), `into_` (所有权) | 混用 |
| `static` 变量大写 | `static CONFIG: Config` | `static config: Config` |
| `const` 变量 | `const BUFFER_SIZE: usize = 1024` | 无限制 |

### 通用命名

```rust
// 变量和函数：snake_case
let max_connections = 100;
fn process_data() { ... }

// 类型和 trait：CamelCase
struct UserSession;
trait Cacheable {}

// 常量：SCREAMING_SAME_CASE
const MAX_CONNECTIONS: usize = 100;
static CONFIG:once_cell::sync::Lazy<Config> = ...
```

---

## 数据类型规范

| 规则 | 说明 | 示例 |
|-----|------|------|
| 用 newtype | 领域语义 | `struct Email(String)` |
| 用 slice 模式 | 模式匹配 | `if let [first, .., last] = slice` |
| 预分配 | 避免重新分配 | `Vec::with_capacity()`, `String::with_capacity()` |
| 避免 Vec 滥用 | 固定大小用数组 | `let arr: [u8; 256]` |

### 字符串

| 规则 | 说明 |
|-----|------|
| ASCII 数据用 `bytes()` | `s.bytes()` 优于 `s.chars()` |
| 可能修改时用 `Cow<str>` | 借用或拥有 |
| 用 `format!` 拼接 | 优于 `+` 操作符 |
| 避免嵌套 `contains()` | O(n*m) 复杂度 |

---

## 错误处理规范

| 规则 | 说明 |
|-----|------|
| 用 `?` 传播 | 不用 `try!()` 宏 |
| `expect()` 优于 `unwrap()` | 值确定时 |
| 用 `assert!` 检查不变量 | 函数入口处 |

```rust
// ✅ 好的错误处理
fn read_config() -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string("config.toml")
        .map_err(ConfigError::from)?;
    toml::from_str(&content)
        .map_err(ConfigError::parse)
}

// ❌ 避免
fn read_config() -> Config {
    std::fs::read_to_string("config.toml").unwrap()  // panic!
}
```

---

## 内存与生命周期

| 规则 | 说明 |
|-----|------|
| 生命周期命名有意义 | `'src`, `'ctx` 而非 `'a` |
| `RefCell` 用 `try_borrow` | 避免 panic |
| 用 shadowing 转换 | `let x = x.parse()?` |

---

## 并发规范

| 规则 | 说明 |
|-----|------|
| 确定锁顺序 | 防止死锁 |
| 原子类型用于原语 | 不用 `Mutex<bool>` |
| 谨慎选择内存序 | Relaxed/Acquire/Release/SeqCst |

---

## Async 规范

| 规则 | 说明 |
|-----|------|
| CPU-bound 用同步 | Async 适用于 I/O |
| 不要跨 await 持有锁 | 使用 scoped guard |

---

## 宏规范

| 规则 | 说明 |
|-----|------|
| 避免宏（除非必要） | 优先用函数/泛型 |
| 宏输入像 Rust | 可读性优先 |

---

## 废弃模式 → 推荐

| 废弃 | 推荐 | 版本 |
|-----|------|------|
| `lazy_static!` | `std::sync::OnceLock` | 1.70 |
| `once_cell::Lazy` | `std::sync::LazyLock` | 1.80 |
| `std::sync::mpsc` | `crossbeam::channel` | - |
| `std::sync::Mutex` | `parking_lot::Mutex` | - |
| `failure`/`error-chain` | `thiserror`/`anyhow` | - |
| `try!()` | `?` operator | 2018 |

---

## Clippy 规范

```toml
[package]
edition = "2024"
rust-version = "1.85"

[lints.rust]
unsafe_code = "warn"

[lints.clippy]
all = "warn"
pedantic = "warn"
```

### 常用 Clippy 规则

| Lint | 说明 |
|-----|------|
| `clippy::all` | 启用所有警告 |
| `clippy::pedantic` | 更严格的检查 |
| `clippy::unwrap_used` | 避免 unwrap |
| `clippy::expect_used` | 优先 expect |
| `clippy::clone_on_ref_ptr` | 避免 clone Arc |

---

## 格式化 (rustfmt)

```bash
# 使用默认配置即可
rustfmt src/lib.rs

# 检查格式
rustfmt --check src/lib.rs

# 配置文件 .rustfmt.toml
max_line_width = 100
tab_spaces = 4
edition = "2024"
```

---

## 文档规范

```rust
/// 模块文档
//! 本模块处理用户认证...

/// 结构体文档
/// 
/// # Examples
/// ```
/// let user = User::new("name");
/// ```
pub struct User { ... }

/// 方法文档
/// 
/// # Arguments
/// 
/// * `name` - 用户名
/// 
/// # Returns
/// 
/// 初始化后的用户实例
/// 
/// # Panics
/// 
/// 当用户名为空时 panic
pub fn new(name: &str) -> Self { ... }
```

---

## 快速参考

```
命名: snake_case (fn/var), CamelCase (type), SCREAMING_CASE (const)
格式: rustfmt (just use it)
文档: /// for public items, //! for module docs
Lint: #![warn(clippy::all)]
```

---

## 代码审查清单

- [ ] 命名符合 Rust 惯例
- [ ] 使用 `?` 而非 `unwrap()`
- [ ] 避免不必要的 `clone()`
- [ ] `unsafe` 块有 SAFETY 注释
- [ ] 公共 API 有文档注释
- [ ] 运行 `cargo clippy`
- [ ] 运行 `cargo fmt`
