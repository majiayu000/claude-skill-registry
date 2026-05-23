---
name: rust-skill-index
description: "Rust 技能索引。提供所有技能的快速导航和查询入口。触发词：skill, index, 技能, 索引, 目录"
---

# Rust 技能索引

> **当前共 35 个技能**，完整内容请参见根目录 `SKILL.md`

---

## 快速导航

| 类别 | 技能数量 | 用途 |
|-----|---------|-----|
| 核心技能 | 7 | 日常开发必备 |
| 进阶技能 | 10 | 深入理解 Rust |
| 专家技能 | 18 | 疑难杂症专项 |
| **总计** | **35** | |

---

## 核心技能（必学）

| 技能 | 文件 | 描述 |
|-----|------|------|
| **rust-skill** | `rust-skill/SKILL.md` | Rust 编程总览与核心概念 |
| **rust-ownership** | `rust-ownership/SKILL.md` | 所有权与生命周期 |
| **rust-mutability** | `rust-mutability/SKILL.md` | 可变性深入 |
| **rust-concurrency** | `rust-concurrency/SKILL.md` | 并发编程基础 |
| **rust-error** | `rust-error/SKILL.md` | 错误处理基础 |
| **rust-error-advanced** | `rust-error-advanced/SKILL.md` | 深入错误处理 |
| **rust-coding** | `rust-coding/SKILL.md` | 编码规范与最佳实践 |

---

## 进阶技能

| 技能 | 文件 | 描述 |
|-----|------|------|
| **rust-unsafe** | `rust-unsafe/SKILL.md` | unsafe Rust |
| **rust-anti-pattern** | `rust-anti-pattern/SKILL.md` | 反模式识别与避免 |
| **rust-performance** | `rust-performance/SKILL.md` | 性能优化（含高级优化） |
| **rust-web** | `rust-web/SKILL.md` | Web 开发指南 |
| **rust-learner** | `rust-learner/SKILL.md` | 学习路径与资源 |
| **rust-ecosystem** | `rust-ecosystem/SKILL.md` | Rust 生态与 crate 选择 |
| **rust-cache** | `rust-cache/SKILL.md` | Redis 缓存管理 |
| **rust-auth** | `rust-auth/SKILL.md` | JWT 与 API Key 认证 |
| **rust-middleware** | `rust-middleware/SKILL.md` | 中间件模式 |
| **rust-xacml** | `rust-xacml/SKILL.md` | 策略引擎与 RBAC |

---

## 专家技能

| 技能 | 文件 | 描述 |
|-----|------|------|
| **rust-ffi** | `rust-ffi/SKILL.md` | FFI 与 C/C++ 互操作（含 C++ 异常） |
| **rust-pin** | `rust-pin/SKILL.md` | Pin 与 Unpin 深入理解 |
| **rust-macro** | `rust-macro/SKILL.md` | 宏编程深入 |
| **rust-async** | `rust-async/SKILL.md` | async/await 深入 |
| **rust-async-pattern** | `rust-async-pattern/SKILL.md` | 异步设计模式 |
| **rust-const** | `rust-const/SKILL.md` | const fn 与编译期计算 |
| **rust-embedded** | `rust-embedded/SKILL.md` | 嵌入式开发（含 WASM/RISC-V） |
| **rust-lifetime-complex** | `rust-lifetime-complex/SKILL.md` | 复杂生命周期场景 |
| **rust-linear-type** | `rust-linear-type/SKILL.md` | 线性类型与资源管理 |
| **rust-coroutine** | `rust-coroutine/SKILL.md` | 协程与绿色线程 |
| **rust-ebpf** | `rust-ebpf/SKILL.md` | eBPF 与内核编程 |
| **rust-gpu** | `rust-gpu/SKILL.md` | GPU 内存与计算 |
| **rust-skill-index** | `rust-skill-index/SKILL.md` | 技能索引（本文件） |

---

## 技能分类

### 按难度

```
入门级：rust-skill, rust-ownership, rust-concurrency, rust-error
进阶级：rust-mutability, rust-unsafe, rust-coding, rust-performance
高级：rust-async, rust-pin, rust-macro, rust-ffi, rust-embedded
专家级：rust-ebpf, rust-gpu, rust-coroutine, rust-linear-type
```

### 按领域

```
系统编程：rust-unsafe, rust-ffi, rust-embedded, rust-ebpf, rust-gpu
Web 开发：rust-web, rust-async, rust-middleware, rust-auth, rust-xacml
并发编程：rust-concurrency, rust-async, rust-coroutine
性能优化：rust-performance, rust-embedded
类型系统：rust-ownership, rust-pin, rust-macro, rust-const, rust-lifetime-complex
错误处理：rust-error, rust-error-advanced
基础设施：rust-cache, rust-auth, rust-middleware, rust-xacml
```

---

## 问题速查

遇到问题时的技能选择：

| 问题类型 | 推荐技能 |
|---------|---------|
| 所有权/生命周期错误 | rust-ownership |
| 借用冲突/可变性 | rust-mutability |
| Send/Sync 错误 | rust-concurrency |
| 错误处理策略 | rust-error / rust-error-advanced |
| 异步代码问题 | rust-async |
| unsafe 代码审查 | rust-unsafe |
| FFI 与 C++ 互操作 | rust-ffi |
| 性能优化 | rust-performance |
| no_std 开发 | rust-embedded |
| eBPF 内核编程 | rust-ebpf |
| GPU 计算 | rust-gpu |
| 协程实现 | rust-coroutine |
| 线性类型语义 | rust-linear-type |
| crate 选择 | rust-ecosystem |
| 代码风格 | rust-coding |
| 缓存策略 | rust-cache |
| 认证授权 | rust-auth |
| Web 中间件 | rust-middleware |
| 策略引擎 | rust-xacml |
