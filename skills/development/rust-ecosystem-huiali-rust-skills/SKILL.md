---
name: rust-ecosystem
description: "Rust 生态专家。处理 crate 选择、库推荐、框架对比、async runtime 选择、序列化库、web 框架等。触发词：crate, library, framework, ecosystem, async runtime, tokio, async-std, serde, reqwest, axum, 库, 框架, 生态"
globs: ["**/Cargo.toml"]
---

# Rust 生态

## 核心问题

**用什么 crate 解决当前问题？**

选择正确的库是高效 Rust 开发的关键。

---

## 异步 Runtime

| Runtime | 特点 | 适用场景 |
|---------|------|---------|
| **tokio** | 最流行、功能全 | 通用异步应用 |
| **async-std** | 类似 std API | 偏好 std 风格 |
| **actix** | 高性能 | 高性能 Web 服务 |
| **async-executors** | 统一接口 | 需要切换 runtime |

```toml
# Web 服务
tokio = { version = "1", features = ["full"] }
axum = "0.7"

# 轻量级
async-std = "1"
```

---

## Web 框架

| 框架 | 特点 | 性能 |
|-----|------|------|
| **axum** | Tower 中间件、类型安全 | 高 |
| **actix-web** | 最高性能 | 最高 |
| **rocket** | 开发者友好 | 中 |
| **warp** | 组合式、Filter | 高 |

---

## 序列化

| 库 | 特点 | 性能 |
|-----|------|------|
| **serde** | 标准选择 | 高 |
| **bincode** | 二进制、紧凑 | 最高 |
| ** postcard** | 无 std、嵌入式 | 高 |
| **ron** | 可读性好 | 中 |

```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

// JSON
let json = serde_json::to_string(&user)?;

// 二进制
let bytes = bincode::serialize(&user)?;
```

---

## HTTP 客户端

| 库 | 特点 |
|-----|------|
| **reqwest** | 最流行、易用 |
| **ureq** | 同步、简单 |
| **surf** | 异步、modern |

```rust
// reqwest
let response = reqwest::Client::new()
    .post("https://api.example.com")
    .json(&payload)
    .send()
    .await?;
```

---

## 数据库

| 类型 | 库 |
|-----|------|
| ORM | **sqlx**, diesel, sea-orm |
| Raw SQL | **sqlx**, tokio-postgres |
| NoSQL | mongodb, redis |
| 连接池 | **sqlx**, deadpool, r2d2 |

---

## 并发与并行

| 场景 | 推荐 |
|-----|------|
| 数据并行 | **rayon** |
| 工作窃取 | **crossbeam**, tokio |
| 通道 | **tokio::sync**, crossbeam, flume |
| 原子类型 | **std::sync::atomic** |

---

## 错误处理

| 库 | 用途 |
|-----|------|
| **thiserror** | 库错误类型 |
| **anyhow** | 应用错误传播 |
| **snafu** | 结构化错误 |

---

## 常用工具库

| 场景 | 库 |
|-----|------|
| 命令行 | **clap** (v4), structopt |
| 日志 | **tracing**, log |
| 配置 | **config**, dotenvy |
| 测试 | **tempfile**, rstest |
| 时间 | **chrono**, time |

---

## Crate 选择原则

1. **活跃维护**：看 GitHub 活跃度、最近更新
2. **下载量**：crates.io 下载量参考
3. **MSRV**：最小支持 Rust 版本
4. **依赖**：依赖数量和安全性
5. **文档**：完整文档和示例
6. **License**：MIT/Apache2 兼容性

---

## 废弃模式 → 推荐

| 废弃 | 推荐 | 原因 |
|-----|------|------|
| `lazy_static` | `std::sync::OnceLock` | std 内置 |
| `rand::thread_rng` | `rand::rng()` | 新 API |
| `failure` | `thiserror` + `anyhow` | 更流行 |
| `serde_derive` | `serde` | 统一导入 |
| `parking_lot::Mutex` | std::sync::Mutex | 足够快，稳定性优先 |

---

## 验证 Crate

```bash
# 检查安全性
cargo audit

# 检查许可证
cargo deny check

# 检查依赖
cargo tree -i serde
```

---

## 快速参考

| 场景 | 推荐 Crate |
|-----|-----------|
| Web 服务 | axum + tokio + sqlx |
| CLI 工具 | clap + anyhow |
| 序列化 | serde + (json/bincode) |
| 并行计算 | rayon |
| 配置管理 | config + dotenvy |
| 日志追踪 | tracing |
| 测试 | tempfile + proptest |
| 日期时间 | chrono |

