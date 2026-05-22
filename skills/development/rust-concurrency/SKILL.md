---
name: rust-concurrency
description: "并发与异步专家。处理 Send, Sync, thread, async, await, tokio, channel, Mutex, deadlock, race condition, 并发, 异步, 死锁等问题。触发词：thread, spawn, channel, mpsc, Mutex, RwLock, Atomic, async, await, Future, tokio, deadlock, race condition"
globs: ["**/*.rs"]
---

# 并发与异步专家

## 核心问题

**数据如何在线程间安全传递？**

这是并发的本质。Rust 的类型系统在这里发挥最大威力。

---

## 并发 vs 异步

| 维度 | 并发 (thread) | 异步 (async) |
|-----|--------------|-------------|
| 内存 | 每个线程有独立栈 | 单线程复用 |
| 阻塞 | 阻塞 OS 线程 | 不阻塞，yield |
| 适用 | CPU 密集型 | I/O 密集型 |
| 复杂度 | 简单直接 | 需要运行时 |

---

## Send/Sync 快速判断

### Send - 可以在线程间转移所有权

```
基本类型 → 自动 Send
包含引用 → 自动 Send
Raw pointer → 非 Send
Rc → 非 Send（引用计数非原子）
```

### Sync - 可以在线程间共享引用

```
&T where T: Sync → 自动 Sync
RefCell → 非 Sync（运行时检查非线程安全）
MutexGuard → 非 Sync（未实现）
```

---

## 常见模式

### 1. 共享可变状态

```rust
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = std::thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}
```

### 2. 消息传递

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send("hello").unwrap();
});

println!("{}", rx.recv().unwrap());
```

### 3. 异步运行时

```rust
use tokio;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // 异步任务
    });
    
    handle.await.unwrap();
}
```

---

## 常见错误与解决

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| E0277 Send not satisfied | 包含非 Send 类型 | 检查所有字段 |
| E0277 Sync not satisfied | 共享引用类型非 Sync | 用 Mutex/RwLock 包装 |
| Deadlock | 锁顺序不一致 | 统一加锁顺序 |
| MutexGuard across await | 锁持有时挂起 | 缩小锁的作用域 |

---

## 性能考量

- 锁的粒度要细（锁住必要部分，不是整个数据结构）
- 读写锁适合读多写少场景
- 原子操作比锁更轻量，但只适合简单操作
- 消息传递避免共享状态，但有复制开销

