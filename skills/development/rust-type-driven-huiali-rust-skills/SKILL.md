---
name: rust-type-driven
description: "类型驱动设计专家。处理 newtype, type state, PhantomData, marker trait, builder pattern, 类型状态, 新类型模式, 编译时验证, sealed trait, ZST"
globs: ["**/*.rs"]
---

# 类型驱动设计

## 核心问题

**如何让编译器在编译期捕获更多错误？**

类型设计得好，运行时错误就少。

---

## 类型设计模式

### Newtype 模式

```rust
// ❌ 原始类型容易被混淆
struct UserId(u64);
struct OrderId(u64);

// ✅ 类型安全：无法混用
fn get_user(user_id: UserId) { ... }
fn get_order(order_id: OrderId) { ... }

// 编译器会阻止：
// get_order(user_id);  // 编译错误！
```

### 类型状态模式 (Type State)

```rust
// 用类型编码状态
struct Disconnected;
struct Connecting;
struct Connected;

struct Connection<State = Disconnected> {
    socket: TcpSocket,
    _state: PhantomData<State>,
}

impl Connection<Disconnected> {
    fn connect(self) -> Connection<Connecting> {
        // ...
        Connection { socket: self.socket, _state: PhantomData }
    }
}

impl Connection<Connected> {
    fn send(&mut self, data: &[u8]) {
        // 只有 Connected 状态可以发送
    }
}
```

### PhantomData

```rust
// 用 PhantomData 标记所有权和方差
struct MyIterator<'a, T> {
    _marker: PhantomData<&'a T>,
}

// 告诉编译器：我们借用了一个 T 的生命周期
```

---

## 让无效状态不可表示

```rust
// ❌ 容易创建无效状态
struct User {
    name: String,
    email: Option<String>,  // 可能为空
    age: u32,
}

// ✅ email 不可能为空
struct User {
    name: String,
    email: Email,  // 类型保证有效
    age: u32,
}

struct Email(String);

impl Email {
    fn new(s: &str) -> Option<Self> {
        if s.contains('@') {
            Some(Email(s.to_string()))
        } else {
            None
        }
    }
}
```

---

## Builder 模式

```rust
struct ConfigBuilder {
    host: String,
    port: u16,
    timeout: u64,
    retries: u32,
}

impl ConfigBuilder {
    fn new() -> Self {
        Self {
            host: "localhost".to_string(),
            port: 8080,
            timeout: 30,
            retries: 3,
        }
    }

    fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }

    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    fn build(self) -> Config {
        // 可以在这里做最终验证
        Config {
            host: self.host,
            port: self.port,
        }
    }
}
```

---

## Marker Trait

```rust
// 用 marker trait 标记能力
trait Sendable: Send + 'static {}

// 或用 marker 做类型约束
struct Cache<T: Cacheable> {
    data: T,
}

trait Cacheable: Send + Sync {}
```

---

## Zero-Sized Types (ZST)

```rust
// 用 ZST 做标记
struct DebugOnly;
struct Always;

// 只在 debug 模式执行的代码
struct DebugLogger<Mode = Always> {
    _marker: PhantomData<Mode>,
}

impl DebugLogger<DebugOnly> {
    fn log(&self, msg: &str) {
        println!("[DEBUG] {}", msg);
    }
}
```

---

## 常见反模式

| 反模式 | 问题 | 改进 |
|-------|------|-----|
| `is_valid` 标志 | 运行时检查 | 用类型编码状态 |
| 大量 `Option` | 可能为空 | 重新设计类型 |
| 原始类型 everywhere | 类型混淆 | Newtype |
| 验证在运行时 | 延迟错误发现 | 构造函数验证 |
| 布尔参数 | 含义不清 | 用枚举或 builder |

---

## 验证时机

| 验证类型 | 最佳时机 | 示例 |
|---------|---------|-----|
| 范围验证 | 构造时 | `Email::new()` 返回 `Option` |
| 状态转换 | 类型边界 | `Connection<Connected>` |
| 引用有效性 | 生命周期 | `&'a T` |
| 线程安全 | `Send + Sync` | 编译器检查 |

