---
name: rust-resource
description: "智能指针与资源管理专家。处理 Box, Rc, Arc, Weak, RefCell, Cell, interior mutability, RAII, Drop, 堆分配, 引用计数, 智能指针"
globs: ["**/*.rs"]
---

# 智能指针与资源管理

## 核心问题

**这个资源应该用什么方式管理？**

选择正确的智能指针是 Rust 编程的核心决策之一。

---

## 选择决策树

```
需要共享数据吗？
    │
    ├─ 否 → 单 owner
    │   ├─ 需要堆分配？ → Box<T>
    │   └─ 栈上即可？ → 直接值类型
    │
    └─ 是 → 需要共享
          │
          ├─ 单线程？
          │   ├─ 可变？ → Rc<RefCell<T>>
          │   └─ 只读？ → Rc<T>
          │
          └─ 多线程？
                ├─ 可变？ → Arc<Mutex<T>> 或 Arc<RwLock<T>>
                └─ 只读？ → Arc<T>
```

---

## 智能指针对比

| 类型 | 所有权 | 线程安全 | 适用场景 |
|-----|-------|---------|---------|
| `Box<T>` | 单 owner | Yes | 堆分配、递归类型、trait object |
| `Rc<T>` | 共享 | No | 单线程共享、避免 clone |
| `Arc<T>` | 共享 | Yes | 多线程共享、只读数据 |
| `Weak<T>` | 弱引用 | - | 打破循环引用 |
| `RefCell<T>` | 单 owner | No | 运行时借用检查 |
| `Cell<T>` | 单 owner | No | Copy 类型的内部可变性 |

---

## 常见错误与解决方案

### Rc 循环引用泄漏

```rust
// ❌ 内存泄漏：两个 Rc 互相引用
struct Node {
    value: i32,
    next: Option<Rc<Node>>,
}

// ✅ 解决方案：使用 Weak 打破循环
struct Node {
    value: i32,
    next: Option<Weak<Node>>,
}
```

### RefCell panic

```rust
// ❌ 运行时 panic：双重可变借用
let cell = RefCell::new(vec![1, 2, 3]);
let mut_borrow = cell.borrow_mut();
let another_borrow = cell.borrow(); // panic!

// ✅ 解决方案：使用 try_borrow
if let Ok(mut_borrow) = cell.try_borrow_mut() {
    // 安全使用
}
```

### Arc 开销投诉

```rust
// ❌ 不必要的 Arc：单线程环境
let shared = Arc::new(data);

// ✅ 单线程用 Rc
let shared = Rc::new(data);

// ❌ 多线程不必要的原子操作
// 如果确定不需要跨线程共享，就不要用 Arc
```

---

## 内部可变性选择

```rust
// T 是 Copy 类型 → Cell
struct Counter {
    count: Cell<u32>,
}

// T 不是 Copy → RefCell
struct Container {
    items: RefCell<Vec<Item>>,
}

// 多线程 → Mutex 或 RwLock
struct SharedContainer {
    items: Mutex<Vec<Item>>,
}
```

---

## RAII 与 Drop

```rust
struct File {
    handle: std::fs::File,
}

impl Drop for File {
    fn drop(&mut self) {
        // 自动释放资源
        println!("File closed");
    }
}

// 使用 guard pattern 确保清理
struct Guard<'a> {
    resource: &'a Resource,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.resource.release();
    }
}
```

---

## 性能提示

| 场景 | 建议 |
|-----|------|
| 大量小对象 | `Rc::make_mut()` 避免 clone |
| 频繁读取 | `RwLock` 比 `Mutex` 更好 |
| 计数器 | 用 `AtomicU64` 而非 `Mutex<u64>` |
| 缓存 | 考虑 `moka` 或 `cached` crate |

---

## 何时不用智能指针

- 栈上数据足够 → 用值类型
- 借用即可满足 → 用引用 `&T`
- 生命周期简单 → 不要过度抽象

