---
name: rust-linear-type
description: "线性类型与资源管理专家。处理 Destructible, 资源清理, RAII, unique object, linear semantics, 线性语义, 资源所有权, 独占语义"
globs: ["**/*.rs"]
---

# 线性类型

## 核心问题

**如何保证资源不被泄漏或被重复释放？**

线性类型语义保证每个资源被精确使用一次。

---

## 线性类型 vs Rust 所有权

| 特性 | Rust 所有权 | 线性类型 |
|-----|------------|---------|
| 移动语义 | ✓ | ✓ |
| 复制语义 | 可选 | ✗ |
| 析构保证 | Drop | Destructible |
| 借用 | ✓ | ✗ 或受限 |
| 多重所有 | Rc/Arc | ✗ |

Rust 默认不是线性类型，但可以通过模式实现线性语义。

---

## Destructible Trait

```rust
// 线性类型的核心：Destructible 保证析构
use std::mem::ManuallyDrop;

struct LinearBuffer {
    ptr: *mut u8,
    size: usize,
}

impl Drop for LinearBuffer {
    fn drop(&mut self) {
        unsafe {
            std::alloc::dealloc(self.ptr, Layout::array::<u8>(self.size).unwrap());
        }
    }
}

// 防止双重释放
struct SafeLinearBuffer {
    inner: ManuallyDrop<LinearBuffer>,
}

impl Drop for SafeLinearBuffer {
    fn drop(&mut self) {
        // 确保只释放一次
        unsafe {
            ManuallyDrop::drop(&mut self.inner);
        }
    }
}
```

---

## 独占对象模式

```rust
// 确保对象只能被移动，不能被复制
#[derive(Copy, Clone)]
struct FileHandle(u32);

impl FileHandle {
    // 私有构造函数，防止外部直接创建
    fn from_raw(fd: u32) -> Self {
        Self(fd)
    }
}

// 包装为线性类型
struct LinearFile {
    fd: FileHandle,
}

impl LinearFile {
    pub fn open(path: &str) -> Result<Self, std::io::Error> {
        // 打开文件，返回线性文件句柄
        Ok(LinearFile {
            fd: FileHandle::from_raw(0), // 示例
        })
    }

    // consume() 方法消费 self，保证线性使用
    pub fn consume(self) -> FileHandle {
        self.fd
    }
}
```

---

## 资源令牌模式

```rust
// 线性资源令牌
struct ResourceToken<T> {
    resource: T,
    consumed: bool,
}

impl<T> ResourceToken<T> {
    pub fn new(resource: T) -> Self {
        Self {
            resource,
            consumed: false,
        }
    }

    // 消费令牌，返回资源
    pub fn consume(mut self) -> T {
        self.consumed = true;
        self.resource
    }

    // 检查是否已消费
    pub fn is_consumed(&self) -> bool {
        self.consumed
    }
}

// 使用示例
fn process_resource(token: ResourceToken<Vec<u8>>) -> Vec<u8> {
    // 在这里处理资源
    let data = token.consume(); // 消费后令牌失效
    data
}
```

---

## 交易式资源管理

```rust
// 两阶段提交模式
struct Transaction<T> {
    data: T,
    committed: bool,
}

impl<T> Transaction<T> {
    pub fn new(data: T) -> Self {
        Self {
            data,
            committed: false,
        }
    }

    pub fn commit(mut self) -> T {
        self.committed = true;
        self.data
    }

    // 回滚：丢弃资源
    pub fn rollback(self) {
        // 自动调用 Drop
    }
}

// 使用
fn example() -> Result<i32, ()> {
    let tx = Transaction::new(100);
    
    if condition {
        tx.commit(); // 提交，返回数据
    } else {
        tx.rollback(); // 回滚，丢弃
    }
}
```

---

## Unique 指针模式

```rust
// 类似 C++ unique_ptr 的线性指针
struct UniquePtr<T: Sized> {
    ptr: *mut T,
    _marker: std::marker::PhantomData<T>,
}

impl<T> UniquePtr<T> {
    pub fn new(data: T) -> Self {
        let ptr = Box::into_raw(Box::new(data));
        Self {
            ptr,
            _marker: std::marker::PhantomData,
        }
    }

    pub fn as_ref(&self) -> Option<&T> {
        if self.ptr.is_null() {
            None
        } else {
            Some(unsafe { &*self.ptr })
        }
    }

    // 消费自身，返回 Box
    pub fn into_box(self) -> Box<T> {
        unsafe {
            let ptr = self.ptr;
            std::mem::forget(self);
            Box::from_raw(ptr)
        }
    }
}

impl<T> Drop for UniquePtr<T> {
    fn drop(&mut self) {
        if !self.ptr.is_null() {
            unsafe {
                Box::from_raw(self.ptr);
            }
        }
    }
}
```

---

## Rust 中的线性语义场景

| 场景 | 线性保证 | 模式 |
|-----|---------|------|
| 文件句柄 | close 恰好一次 | RAII + Drop |
| 网络连接 | close 恰好一次 | RAII + Drop |
| 内存分配 | free 恰好一次 | RAII + Drop |
| 锁 | unlock 恰好一次 | RAII + Drop |
| 事务 | commit 或 rollback | 交易式资源管理 |
| FFI 资源 | release 恰好一次 | 资源令牌 |

---

## 避免的模式

| 反模式 | 问题 | 正确做法 |
|-------|------|---------|
| Clone 允许复制 | 破坏线性语义 | 使用 move 语义 |
| Rc/Arc 共享 | 多重所有 | 线性令牌 |
| 手动管理生命周期 | 容易出错 | RAII + Drop |
| 跳过 Drop | 资源泄漏 | 使用 scope API |

---

## 与其他技能关联

```
rust-linear-type
    │
    ├─► rust-resource → RAII 和 Drop 实现
    ├─► rust-ownership → 所有权模式
    └─► rust-unsafe → 底层资源操作
```

