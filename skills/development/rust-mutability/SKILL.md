---
name: rust-mutability
description: "可变性专家。处理 E0596, E0499, E0502, interior mutability, Cell, RefCell, Mutex, RwLock, borrow conflict, 可变性, 内部可变性, 借用冲突"
globs: ["**/*.rs"]
---

# 可变性

## 核心问题

**数据需要变化吗？谁来控制变化？**

可变性是程序状态改变的方式，需要谨慎设计。

---

## 可变性类型

| 类型 | 控制者 | 线程安全 | 使用场景 |
|-----|-------|---------|---------|
| `&mut T` | 外部调用者 | Yes | 标准可变借用 |
| `Cell<T>` | 内部 | No | Copy 类型的内部可变性 |
| `RefCell<T>` | 内部 | No | 非 Copy 类型的内部可变性 |
| `Mutex<T>` | 内部 | Yes | 多线程内部可变性 |
| `RwLock<T>` | 内部 | Yes | 多线程读写锁 |

---

## 借用规则

```
任何时刻只能有：
├─ 多个 &T（不可变借用）
└─ 或者一个 &mut T（可变借用）

两者不能同时存在
```

---

## 错误码速查

| 错误码 | 含义 | 不要说 | 要问 |
|-------|------|--------|------|
| E0596 | 无法获取可变引用 | "add mut" | 这个真的需要可变吗？ |
| E0499 | 多个可变借用冲突 | "split borrows" | 数据结构设计对吗？ |
| E0502 | 借用冲突 | "separate scopes" | 为什么需要同时借用？ |
| RefCell panic | 运行时借用错误 | "use try_borrow" | 运行时检查合适吗？ |

---

## 何时用内部可变性

```rust
// 情况1：从 &self 获取 &mut T
struct Config {
    counters: RefCell<HashMap<String, u32>>,
}

impl Config {
    fn increment(&self, key: &str) {
        // 从不可变引用获取可变引用
        let mut counters = self.counters.borrow_mut();
        *counters.entry(key.to_string()).or_insert(0) += 1;
    }
}

// 情况2：Copy 类型
struct State {
    count: Cell<u32>,
}

impl State {
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }
}
```

---

## 线程安全选择

```rust
// 简单计数器 → 原子类型
let counter = AtomicU64::new(0);

// 复杂数据 → Mutex 或 RwLock
let data = Mutex::new(HashMap::new());

// 读多写少 → RwLock
let data = RwLock::new(HashMap::new());
```

---

## 常见问题

### 借用冲突

```rust
// ❌ 借用冲突
let mut s = String::new();
let r1 = &s;
let r2 = &s;
let r3 = &mut s; // 冲突！

// ✅ 分开作用域
let mut s = String::new();
{
    let r1 = &s;
    // 使用 r1
}
let r3 = &mut s;
// 使用 r3
```

### RefCell panic

```rust
// ❌ 双重可变借用
let cell = RefCell::new(vec![]);
let mut_borrow = cell.borrow_mut();
let another = cell.borrow(); // panic!

// ✅ 用 try_borrow 避免 panic
if let Ok(mut_borrow) = cell.try_borrow_mut() {
    // 安全使用
}
```

---

## 设计建议

1. **变异是必要的吗？**
   - 也许可以返回新值
   - 也许可以 immutable 构造

2. **谁控制变异？**
   - 外部调用者 → `&mut T`
   - 内部逻辑 → 内部可变性
   - 并发访问 → 同步原语

3. **线程上下文？**
   - 单线程 → Cell/RefCell
   - 多线程 → Mutex/RwLock/Atomic

---

## 向上追踪

借用冲突持续时：

```
E0499/E0502 (借用冲突)
    ↑ 问：数据结构设计正确吗？
    ↑ 查 rust-type-driven：应该拆分数据吗？
    ↑ 查 rust-concurrency：涉及 async 吗？
```
