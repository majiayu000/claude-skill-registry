---
name: rust-anti-pattern
description: "Rust 反模式与常见错误。处理代码审查、clone、unwrap、String 用法、迭代器等问题。触发词：anti-pattern, common mistake, clone, unwrap, code review, 代码异味, 常见错误, 代码审查, refactor, 重构"
globs: ["**/*.rs"]
---

# Rust 反模式与常见错误

## 核心问题

**这个模式是否掩盖了设计问题？**

代码能跑不代表代码好。反模式是"能用但不该用"的模式。

---

## Top 5 新手常犯错误

| 排名 | 错误 | 正确做法 |
|-----|------|---------|
| 1 | 用 `.clone()` 躲避借用检查 | 使用引用 |
| 2 | 生产代码用 `.unwrap()` | 用 `?` 或 `with_context()` |
| 3 | 什么都是 `String` | 用 `&str`，必要时用 `Cow<str>` |
| 4 | 索引循环 | 用迭代器 `.iter()`, `.enumerate()` |
| 5 | 与生命周期对抗 | 重新设计数据结构 |

---

## 常见反模式

### 反模式 1：到处 clone

```rust
// ❌ 不好：躲避借用检查
fn process(user: User) {
    let name = user.name.clone();  // 为什么需要 clone？
    // ...
}

// ✅ 好：直接使用引用
fn process(user: &User) {
    let name = &user.name;  // 借用即可
}
```

**什么时候真的需要 clone：**
- 确实需要独立副本
- API 设计需要 owned 值
- 数据流向需要

### 反模式 2：生产代码用 unwrap

```rust
// ❌ 不好：可能 panic
let config = File::open("config.json").unwrap();

// ✅ 好：传播错误
let config = File::open("config.json")?;

// ✅ 好：带上下文
let config = File::open("config.json")
    .context("failed to open config")?;
```

### 反模式 3：String  everywhere

```rust
// ❌ 不好：不必要的分配
fn greet(name: String) {
    println!("Hello, {}", name);
}

// ✅ 好：借用即可
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// 确实需要 String 的场景：需要持有或修改
```

### 反模式 4：索引循环

```rust
// ❌ 不好：容易出错，效率低
for i in 0..items.len() {
    println!("{}: {}", i, items[i]);
}

// ✅ 好：直接迭代
for item in &items {
    println!("{}", item);
}

// ✅ 好：需要索引
for (i, item) in items.iter().enumerate() {
    println!("{}: {}", i, item);
}
```

### 反模式 5：过度 unsafe

```rust
// ❌ 不好：为了省事用 unsafe
unsafe {
    let ptr = data.as_mut_ptr();
    // ... 复杂的内存操作
}

// ✅ 好：寻找安全的抽象
let mut data: Vec<u8> = vec![0; size];
// Vec 已经处理了内存管理
```

---

## 代码异味速查

| 现象 | 暗示问题 | 重构方向 |
|-----|---------|---------|
| 很多 `.clone()` | 所有权不清晰 | 明确数据流 |
| 很多 `.unwrap()` | 错误处理缺失 | 添加 Result 处理 |
| 很多 `pub` 字段 | 封装被破坏 | 私有 + 访问器 |
| 深度嵌套 | 逻辑复杂 | 提取方法 |
| 函数过长 (>50行) | 职责过多 | 拆分职责 |
| 巨大的枚举 | 缺少抽象 | Trait + 类型 |

---

## 过时写法 → 现代写法

| 过时 | 现代 |
|-----|------|
| 索引循环 `.items[i]` | `.iter().enumerate()` |
| `collect::<Vec<_>>()` 然后再遍历 | 链式迭代器 |
| `lazy_static!` | `std::sync::OnceLock` |
| `mem::transmute` 转换 | `as` 或 `TryFrom` |
| 自定义链表 | `Vec` 或 `VecDeque` |
| 手动 unsafe cell | `Cell`, `RefCell` |

---

## 代码审查清单

- [ ] 没有无理由的 `.clone()`
- [ ] 库代码没有 `.unwrap()`
- [ ] 没有带不变式的 `pub` 字段
- [ ] 迭代器可用时不使用索引循环
- [ ] `&str` 够用时不使用 `String`
- [ ] 没有忽略 `#[must_use]` 警告
- [ ] `unsafe` 有 SAFETY 注释
- [ ] 没有巨型函数 (>50 行)

---

## 问自己这些问题

1. **这段代码在对抗 Rust 还是在配合 Rust？**
   - 对抗 → 重新设计
   - 配合 → 继续

2. **这个 clone 是必要的吗？**
   - 为了躲避借用 → 错误信号
   - 确实需要 → 保留

3. **这个 unwrap 会导致 panic 吗？**
   - 可能 → 用 `?`
   - 绝不会 → `expect("reason")`

4. **有更 idiomatic 的方式吗？**
   - 参考其他 Rust 代码
   - 查阅 std 库 API

