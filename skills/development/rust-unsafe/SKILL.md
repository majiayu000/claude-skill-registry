---
name: rust-unsafe
description: "不安全代码与 FFI 专家。处理 unsafe, raw pointer, FFI, extern, transmute, *mut, *const, union, #[repr(C)], libc, MaybeUninit, NonNull, SAFETY comment, soundness, undefined behavior, UB, 安全抽象, 裸指针, 外部函数接口, 内存布局, 未定义行为"
globs: ["**/*.rs"]
---

# 不安全代码与 FFI

## 核心问题

**什么时候可以用 unsafe，怎么用才安全？**

 unsafe 是必要的，但必须谨慎使用。

---

## 何时可以用 Unsafe

| 使用场景 | 示例 | 是否正当 |
|---------|-----|---------|
| FFI 调用 C | `extern "C" { fn libc_malloc(size: usize) -> *mut c_void; }` | ✅ |
| 实现底层抽象 | `Vec`, `Arc` 的内部实现 | ✅ |
| 性能优化（已测量） | 热点代码测出瓶颈 | ⚠️ 需验证 |
| 逃避借用检查 | 不知道为什么要用 | ❌ |

---

## SAFETY 注释要求

**每个 unsafe 块必须包含 SAFETY 注释：**

```rust
// SAFETY: ptr must be non-null and properly aligned.
// This function is only called after a null check.
unsafe { *ptr = value; }

/// # Safety
/// 
/// * `ptr` must be properly aligned and not null
/// * `ptr` must point to initialized memory of type T
/// * The memory must not be accessed after this function returns
pub unsafe fn write(ptr: *mut T, value: &T) { ... }
```

---

## 47 条 Unsafe 规则速查

### 通用原则 (3条)

| 规则 | 说明 |
|-----|------|
| G-01 | 不要用 unsafe 逃避编译器安全检查 |
| G-02 | 不要盲目为性能使用 unsafe |
| G-03 | 不要为类型/方法创建名为 "Unsafe" 的别名 |

### 内存布局 (6条)

| 规则 | 说明 |
|-----|------|
| M-01 | 为 struct/tuple/enum 选择合适的内存布局 |
| M-02 | 不要修改其他进程的内存变量 |
| M-03 | 不要让 String/Vec 自动释放其他进程的内存 |
| M-04 | 优先使用 C-API 或 Syscalls 的可重入版本 |
| M-05 | 用第三方 crate 处理位域 |
| M-06 | 用 `MaybeUninit<T>` 处理未初始化内存 |

### 原始指针 (6条)

| 规则 | 说明 |
|-----|------|
| P-01 | 不要跨线程共享原始指针 |
| P-02 | 优先使用 `NonNull<T>` 而非 `*mut T` |
| P-03 | 用 `PhantomData<T>` 标记方差和所有权 |
| P-04 | 不要解引用强制转换为对齐错误的类型 |
| P-05 | 不要手动将不可变指针转为可变指针 |
| P-06 | 用 `ptr::cast` 而非 `as` 做指针转换 |

### 联合 (2条)

| 规则 | 说明 |
|-----|------|
| U-01 | 除 C 互操作外避免使用 union |
| U-02 | 不要在不同生命周期使用 union 变体 |

### FFI (18条)

| 规则 | 说明 |
|-----|------|
| F-01 | 避免直接向 C 传递字符串 |
| F-02 | 仔细阅读 `std::ffi` 类型的文档 |
| F-03 | 为包装的 C 指针实现 Drop |
| F-04 | 处理跨越 FFI 边界的 panic |
| F-05 | 使用 `std` 或 `libc` 的可移植类型别名 |
| F-06 | 确保 C-ABI 字符串兼容性 |
| F-07 | 不要为传递给外部代码的类型实现 Drop |
| F-08 | 在 FFI 中正确处理错误 |
| F-09 | 安全包装中用引用而非原始指针 |
| F-10 | 导出函数必须线程安全 |
| F-11 | 小心 `repr(packed)` 字段的引用 |
| F-12 | 文档化 C 参数的不变式假设 |
| F-13 | 确保自定义类型的数据布局一致 |
| F-14 | FFI 中的类型应有稳定布局 |
| F-15 | 验证外部值的鲁棒性 |
| F-16 | 分离 C 闭包的数据和代码 |
| F-17 | 用不透明类型而非 `c_void` |
| F-18 | 避免向 C 传递 trait object |

### 安全抽象 (11条)

| 规则 | 说明 |
|-----|------|
| S-01 | 注意 panic 带来的内存安全问题 |
| S-02 | unsafe 代码作者必须验证安全不变量 |
| S-03 | 不要在公共 API 中暴露未初始化内存 |
| S-04 | 避免因 panic 导致的双重释放 |
| S-05 | 手动实现 Auto Traits 时考虑安全性 |
| S-06 | 不要在公共 API 中暴露原始指针 |
| S-07 | 为性能提供安全的替代方法 |
| S-08 | 从不可变参数返回可变引用是错误的 |
| S-09 | 在每个 unsafe 块前添加 SAFETY 注释 |
| S-10 | 为公共 unsafe 函数添加文档中的 Safety 节 |
| S-11 | 在 unsafe 函数中使用 `assert!` 而非 `debug_assert!` |

### I/O 安全 (1条)

| 规则 | 说明 |
|-----|------|
| I-01 | 使用原始句柄时确保 I/O 安全 |

---

## 常见错误与修复

| 错误 | 修复 |
|-----|------|
| 空指针解引用 | 解引用前检查 null |
| 使用后释放 | 确保生命周期有效性 |
| 数据竞争 | 添加同步 |
| 对齐违规 | 使用 `#[repr(C)]`，检查对齐 |
| 无效位模式 | 使用 `MaybeUninit` |
| 缺少 SAFETY 注释 | 添加注释 |

---

## 废弃模式

| 废弃 | 替代 |
|-----|------|
| `mem::uninitialized()` | `MaybeUninit<T>` |
| `mem::zeroed()` (引用类型) | `MaybeUninit<T>` |
| 原始指针运算 | `NonNull<T>`, `ptr::add` |
| `CString::new().unwrap().as_ptr()` | 先存储 `CString` |
| `static mut` | `AtomicT` 或 `Mutex` |
| 手动 extern | `bindgen` |

---

## FFI 工具

| 方向 | 工具 |
|-----|------|
| C → Rust | `bindgen` |
| Rust → C | `cbindgen` |
| Python | `PyO3` |
| Node.js | `napi-rs` |

---

## 调试工具

```bash
# Miri 检测未定义行为
cargo +nightly install miri
cargo miri test

# 内存问题检测
cargo install valgrind
valgrind ./target/release/my_program

# 竞态条件检测
cargo install helgrind
helgrind ./target/release/my_program
```
