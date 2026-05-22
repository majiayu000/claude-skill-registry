---
name: rust-const
description: "Const generics 与编译时计算专家。处理 const泛型、类型级计算、编译时求值、MaybeUninit 数组等问题。触发词：const, generics, compile-time, MaybeUninit, 类型级计算, 编译时"
globs: ["**/*.rs"]
---

# Const Generics 与编译时计算

## 核心问题

**哪些计算可以在编译时完成？**

Rust 的 const fn 让你在编译时运行代码。

---

## 基本 const 泛型

```rust
struct Array<T, const N: usize> {
    data: [T; N],
}

let arr: Array<i32, 5> = Array { data: [0; 5] };
```

### 数组初始化

```rust
// 栈上固定大小数组
let arr: [i32; 100] = [0; 100];

// MaybeUninit 用于未初始化内存
use std::mem::MaybeUninit;
let mut arr: [MaybeUninit<i32>; 100] = [MaybeUninit::uninit(); 100];

// 初始化后使用
unsafe {
    let arr: [i32; 100] = arr.map(|x| x.assume_init());
}
```

---

## Const Fn

```rust
const fn double(x: i32) -> i32 {
    x * 2
}

const VAL: i32 = double(5);  // 编译时计算

// 编译时检查
const fn checked_div(a: i32, b: i32) -> i32 {
    assert!(b != 0, "division by zero");
    a / b
}
```

### 当前限制

```rust
// 有些操作 const fn 还不能做
const fn heap_alloc() -> Vec<i32> {
    Vec::new()  // ❌ 还不支持
}

const fn dynamic_size(n: usize) -> [i32; n] {
    // ❌ 数组大小必须是 const
    [0; n]
}
```

---

## 编译时检查模式

```rust
// 数组长度检查
const fn assert_len<T>(slice: &[T], len: usize) {
    assert!(slice.len() == len);
}

// 使用
const _: () = assert_len(&[1, 2, 3], 3);  // 编译时断言

// 类型级状态机
struct StateMachine<S: State> {
    data: Vec<u8>,
    _phantom: std::marker::PhantomData<S>,
}

trait State {}
struct Initial;
struct Processing;
struct Done;

impl StateMachine<Initial> {
    fn start(self) -> StateMachine<Processing> {
        StateMachine {
            data: vec![],
            _phantom: std::marker::PhantomData,
        }
    }
}
```

---

## 常用模式

| 模式 | 用途 | 示例 |
|-----|------|-----|
| 数组类型 | 固定大小集合 | `[T; N]` |
| 缓冲区大小 | 避免动态分配 | `const SIZE: usize = 1024` |
| 编译时检查 | 提前发现问题 | `assert!` in const fn |
| 类型状态 | 状态机 | `StateMachine<S>` |

---

## MaybeUninit 使用

```rust
// 安全初始化模式
fn init_array<T: Default + Copy>(len: usize) -> Vec<T> {
    let mut vec = Vec::with_capacity(len);
    for _ in 0..len {
        unsafe {
            vec.as_mut_ptr().write(T::default());
        }
    }
    unsafe {
        vec.set_len(len);
    }
    vec
}

// 大数组：栈可能溢出
fn big_array_on_heap() -> Box<[u8; 1024 * 1024]> {
    Box::new([0; 1024 * 1024])
}
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| 栈溢出 | 大数组在栈上 | 用 Box 或 Vec |
| 数组大小不匹配 | const 泛型值错误 | 检查常量值 |
| const fn 不支持 | 语言限制 | 用 runtime 或 nightly |
| MaybeUninit 未初始化 | UB | 正确使用 assume_init |

