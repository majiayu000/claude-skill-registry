---
name: rust-pin
description: "Pin 与自引用类型专家。处理 Pin, Unpin, self-referential, Future, async, Generator, Pinning projection 等问题。触发词：Pin, Unpin, self-referential, Future, async, Generator, 自引用, Pinning"
globs: ["**/*.rs"]
---

# Pin 与自引用

## 核心问题

**如何在异步或自引用结构中保证指针稳定性？**

Pin 确保某些类型在内存中不会移动。

---

## 什么时候需要 Pin

### 1. async/await 的 Future

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

struct MyFuture {
    state: State,
}

impl Future for MyFuture {
    type Output = ();
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        // 安全使用 this.state
        Poll::Ready(())
    }
}
```

### 2. 自引用结构

```rust
use std::pin::Pin;

struct Node {
    value: i32,
    parent: Option<Pin<Box<Node>>>,  // 自引用
}
```

---

## Pin 的四种使用方式

| 方式 | 场景 | 例子 |
|-----|------|-----|
| `Pin<&T>` | 借用，值不移动 | `Pin<&Foo>` |
| `Pin<&mut T>` | 可变借用 | `Pin<&mut Foo>` |
| `Pin<Box<T>>` | Box 包裹 | `Pin<Box<Foo>>` |
| `Pin<Arc<T>>` | Arc 包裹 | `Pin<Arc<Foo>>` |

---

## Unpin marker

```rust
// 类型可以实现 Unpin 表示它不介意被移动
struct MyType {
    data: Vec<u8>,
}

// Unpin 自动实现，大多数类型不需要手动实现
// 哪些类型没有实现 Unpin？
// - Future (async/await 生成的)
// - Generator
// - 手动用 !Unpin 标记的类型

struct NotUnpinType {
    // 包含自引用指针
    ptr: *const Self,
}

impl !Unpin for NotUnpinType {}
```

---

## Pinning Projection

```rust
struct Wrapper<T> {
    inner: T,
    extra: String,
}

impl<T> Pin for Wrapper<T> where T: Unpin {
    // projection 到 inner
    fn project(self: Pin<&mut Self>) -> Pin<&mut T> {
        // SAFETY: Wrapper is pinned, inner is inside it
        unsafe {
            &mut self.get_unchecked_mut().inner
        }
    }
}
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| 忘记 Pin | future 可能被移动 | 正确传递 Pin |
| projection 错误 | 借用规则违反 | unsafe get_unchecked_mut |
| 误用 Unpin | 跨 await 保持指针 | 理解 future 结构 |

---

## 什么时候不需要 Pin

- 同步代码，不涉及 future
- 数据结构不包含自引用
- 栈上的临时值
- 明确知道值不会被移动

---

## 使用场景速查

| 场景 | 需要 Pin 吗 |
|-----|-----------|
| `async {}` 块 | ✅ 需要 |
| `Box<dyn Future>` | ✅ 需要 |
| 互斥锁内的 Future | ✅ 需要 |
| 普通 Vec | ❌ 不需要 |
| 栈上变量 | ❌ 不需要 |
| 没有自引用的 struct | ❌ 不需要 |

