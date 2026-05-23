---
name: rust-macro
description: "宏与过程元编程专家。处理 macro_rules!, derive, proc-macro, 泛型宏、编译时计算等问题。触发词：macro, derive, proc-macro, macro_rules, 宏, 过程宏, 编译时计算"
globs: ["**/*.rs"]
---

# 宏与过程元编程

## 核心问题

**如何减少重复代码？什么时候用宏，什么时候用泛型？**

宏是编译时代码生成，泛型是运行时多态。

---

## 宏 vs 泛型

| 维度 | 宏 | 泛型 |
|-----|-----|-----|
| 灵活性 | 代码转换 | 类型抽象 |
| 编译开销 | 增量编译友好 | 单态化开销 |
| 错误信息 | 可能难懂 | 清晰 |
| 调试 | 调试宏展开代码 | 直接调试 |
| 使用场景 | 减少样板 | 通用算法 |

---

## declarative macros (macro_rules!)

### 基本结构

```rust
macro_rules! my_vec {
    () => {
        Vec::new()
    };
    ($($elem:expr),*) => {
        vec![$($elem),*]
    };
    ($elem:expr; $n:expr) => {
        vec![$elem; $n]
    };
}
```

### 重复模式

| 标记 | 含义 |
|-----|------|
| `$()` | 匹配零个或多个 |
| `$($x),*` | 以逗号分隔 |
| `$($x),+` | 至少一个 |
| `$x:ty` | 类型匹配 |
| `$x:expr` | 表达式匹配 |
| `$x:pat` | 模式匹配 |

---

## 派生宏 (derive macro)

### 实现简单 derive

```rust
use proc_macro::TokenStream;
#[proc_macro_derive(MyDerive)]
pub fn my_derive(input: TokenStream) -> TokenStream {
    let input = syn::parse_macro_input!(input as syn::DeriveInput);
    let name = &input.ident;
    
    let expanded = quote::quote! {
        impl MyDerive for #name {
            fn my_method(&self) -> String {
                format!("Hello from {}", stringify!(#name))
            }
        }
    };
    
    expanded.into()
}
```

### 使用

```rust
#[derive(MyDerive)]
struct MyStruct {
    field: i32,
}
```

---

## 函数式过程宏

```rust
#[proc_macro]
pub fn my_func_macro(input: TokenStream) -> TokenStream {
    // 转换输入
    let tokens = input.into_iter().collect::<Vec<_>>();
    // 生成代码
    quote::quote! { /* ... */ }.into()
}
```

---

## 调试宏

```bash
# 查看宏展开结果
cargo expand
cargo expand --test test_name
```

---

## 最佳实践

| 做法 | 原因 |
|-----|------|
| 先用泛型 | 泛型更安全、更易调试 |
| 宏保持简单 | 复杂宏难维护 |
| 文档化宏 | 用户需要理解展开行为 |
| 测试展开结果 | 确保正确性 |
| 用 cargo expand 调试 | 可视化宏展开 |

---

## 常用 crate

| crate | 用途 |
|-------|------|
| `syn` | 解析 Rust 代码 |
| `quote` | 生成 Rust 代码 |
| `proc-macro2` | Token 处理 |
| `derive-more` | 常用 derive 宏 |

