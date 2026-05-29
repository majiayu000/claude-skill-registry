---
name: rust-zero-cost
description: "零成本抽象与泛型专家。处理泛型, trait, monomorphization, static dispatch, dynamic dispatch, impl Trait, dyn Trait, 泛型, 特征, 单态化, 零成本抽象"
globs: ["**/*.rs"]
---

# 零成本抽象与泛型

## 核心问题

**需要编译时多态还是运行时多态？**

选择正确的抽象层次直接影响性能。

---

## 泛型 vs Trait Object

| 特性 | 泛型 (static dispatch) | trait object (dynamic dispatch) |
|-----|----------------------|--------------------------------|
| 性能 | 零开销 | vtable 查找 |
| 代码大小 | 可能膨胀 | 更小 |
| 编译时间 | 更长 | 更短 |
| 灵活性 | 类型必须已知 | 运行时决定 |
| 异构集合 | 不支持 | `Vec<Box<dyn Trait>>` |

---

## 何时用泛型

```rust
// 类型在编译时已知
fn process<T: Processor>(item: T) {
    item.process();
}

// 返回同一类型
fn create_processor() -> impl Processor {
    // 返回具体类型
}

// 多个类型参数
fn combine<A: Display, B: Display>(a: A, b: B) -> String {
    format!("{} and {}", a, b)
}
```

---

## 何时用 trait object

```rust
// 运行时决定类型
trait Plugin {
    fn run(&self);
}

struct PluginManager {
    plugins: Vec<Box<dyn Plugin>>,
}

// 异构集合
let handlers: Vec<Box<dyn Handler>> = vec![
    Box::new(HttpHandler),
    Box::new(GrpcHandler),
];
```

---

## 对象安全规则

```rust
// ❌ 不是对象安全的
trait Bad {
    fn create(&self) -> Self;  // 返回 Self
    fn method(&self, x: Self);  // 参数有 Self
}

// ✅ 对象安全
trait Good {
    fn name(&self) -> &str;
}
```

---

## impl Trait vs dyn Trait

```rust
// impl Trait：返回具体类型（静态分发）
fn create_processor() -> impl Processor {
    HttpProcessor
}

// dyn Trait：返回 trait object（动态分发）
fn create_processor() -> Box<dyn Processor> {
    Box::new(HttpProcessor)
}
```

---

## 性能影响

```rust
// 泛型：每个类型生成一份代码
fn process<T: Trait>(item: T) {
    item.method();
}
// 编译后：
// fn process_Http(item: Http) { ... }
// fn process_Ftp(item: Ftp) { ... }

// trait object：单一路径
fn process(item: &dyn Trait) {
    item.method();  // 通过 vtable 调用
}
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|-----|------|-----|
| E0277 | 缺少 trait bound | 添加 `T: Trait` |
| E0038 | trait object 不安全 | 检查对象安全规则 |
| E0308 | 类型不匹配 | 统一类型或用泛型 |
| E0599 | 未找到实现 | 实现 trait 或检查约束 |

---

## 优化策略

1. **热点代码用泛型** - 消除动态分发开销
2. **插件系统用 dyn** - 灵活性优先
3. **小集合用泛型** - 避免 Box 分配
4. **大集合用 dyn** - 减少代码膨胀

