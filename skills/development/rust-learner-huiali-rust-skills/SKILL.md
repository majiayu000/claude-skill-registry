---
name: rust-learner
description: "Rust 学习与生态追踪专家。处理新版本特性、crate 更新、最佳实践演进、RFC、每周新闻等问题。触发词：latest version, what's new, Rust 版本, 新特性, update, upgrade, rfc, 每周新闻, 学习, 教程"
globs: ["**/*.toml", "**/Cargo.lock"]
---

# Rust 学习与生态追踪

## 核心问题

**如何跟上 Rust 的发展节奏？**

Rust 每 6 周发布一个新版本，生态系统活跃。保持更新但不盲目追新。

---

## 版本更新策略

### 稳定版更新

```bash
# 检查当前版本
rustc --version

# 更新 Rust
rustup update stable

# 查看更新内容
rustup changelog stable
```

### 何时升级

| 场景 | 建议 |
|-----|------|
| 新项目 | 用最新稳定版 |
| 生产项目 | 跟随 6 周周期更新 |
| 库项目 | 考虑 MSRV 策略 |

### MSRV (Minimum Supported Rust Version)

```toml
[package]
rust-version = "1.70"  # 声明最低支持版本

[dependencies]
# 对 MSRV 敏感的依赖要谨慎
serde = { version = "1.0", default-features = false }
```

---

## 新特性学习路径

### 2024 Edition 重要特性

| 特性 | 稳定版本 | 实用度 |
|-----|---------|-------|
| `gen blocks` | nightly | ⭐ 实验性 |
| `async drop` | nightly | ⭐ 实验性 |
| `inline const` | 1.79+ | ⭐⭐ 生产可用 |
| `never type` 改进 | 1.82+ | ⭐⭐⭐ 常用 |

### 新手到进阶路线

```
基础 → 所有权、生命周期、借用检查
    ↓
中级 → 特征对象、泛型、闭包
    ↓
并发 → async/await、线程、通道
    ↓
高级 → unsafe、FFI、性能优化
    ↓
专家 → 宏、类型系统、设计模式
```

---

## 追踪信息源

### 官方渠道

| 渠道 | 内容 | 频率 |
|-----|------|-----|
| [This Week in Rust](https://this-week-in-rust.org/) | 周报、RFC、博客 | 每周 |
| [Rust Blog](https://blog.rust-lang.org/) | 重大发布、深度文章 | 不定期 |
| [Rust RFCs](https://github.com/rust-lang/rfcs) | 设计讨论 | 持续 |
| [Release Notes](https://github.com/rust-lang/rust/blob/master/RELEASES.md) | 版本变更 | 每 6 周 |

### 社区资源

| 资源 | 内容 |
|-----|------|
| [docs.rs](https://docs.rs/) | 文档搜索 |
| [crates.io](https://crates.io/) | 包搜索 |
| [lib.rs](https://lib.rs/) | 找替代 crate |
| [Rust Analyzer](https://rust-analyzer.github.io/) | IDE 插件 |

---

## 依赖更新管理

### 常规更新

```bash
# 检查可更新依赖
cargo outdated

# 更新次要版本
cargo update

# 强制更新所有
cargo update -Z direct-minimal-versions
```

### 安全审计

```bash
# 检查已知漏洞
cargo audit

# 检查依赖许可证
cargo deny check licenses
```

---

## 我的更新策略

### 每季度一次

- [ ] 升级到最新 stable
- [ ] 运行 `cargo outdated`
- [ ] 运行 `cargo audit`
- [ ] 检查依赖的 breaking changes
- [ ] 评估新特性是否值得采用

### 每年一次

- [ ] 考虑 edition 升级
- [ ] 重构使用旧模式代码
- [ ] 评估 MSRV 策略
- [ ] 更新开发工具链

---

## 学习资源推荐

### 入门

- [The Rust Programming Language](https://doc.rust-lang.org/book/) - 官方书
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) - 示例驱动

### 进阶

- [The Rust Reference](https://doc.rust-lang.org/reference/) - 语言参考
- [Rust Nomicon](https://doc.rust-lang.org/nomicon/) - unsafe 指南
- [Effective Rust](https://www.lurklurk.org/effective-rust/) - 最佳实践

### 实战

- [Exercism Rust Track](https://exercism.org/tracks/rust) - 练习题
- [Rust by Practice](https://practice.rs/) - 实践题目

