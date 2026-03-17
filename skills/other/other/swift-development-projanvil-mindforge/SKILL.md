---
name: swift-development
description: 提供 Swift 6+ 核心语言开发能力，涵盖并发编程、宏、数据模型设计和业务逻辑实现。使用此技能编写 ViewModel、Service 或 Repository 层代码、定义数据模型、实现算法、编写单元测试，或修复并发警告和数据竞争时使用。
---

# Swift 6 开发技能

## 指令

当处理非 UI 的 Swift 代码、业务逻辑、算法或数据层时，请遵循本指南。你的目标是编写高性能、线程安全且富有表现力的 Swift 代码。

## 此技能的功能

- **并发编程**: 使用 Actors, async/await, Task, TaskGroup 编写安全并发代码。
- **类型安全**: 定义 Sendable 类型，使用 Typed Throws 精确处理错误。
- **测试**: 使用 Swift Testing 框架编写现代化的单元测试。
- **数据处理**: 编写 Codable 模型，进行 JSON 解析和网络请求封装。
- **宏的使用**: 使用或创建宏来减少样板代码。

## 何时使用此技能

- 编写 ViewModel, Service, Repository 层代码时。
- 定义数据模型 (structs, enums) 时。
- 实现算法或工具函数时。
- 编写单元测试时。
- 修复并发警告或数据竞争问题时。

## 示例

### 示例 1：定义安全的 Actor 服务

```swift
/// 一个线程安全的用户数据服务
actor UserService {
    private var cache: [String: User] = [:]
    
    // 使用 typed throws 明确错误类型
    func fetchUser(id: String) async throws(NetworkError) -> User {
        if let cached = cache[id] {
            return cached
        }
        
        // 模拟网络请求
        let user = try await NetworkClient.shared.get("/users/\(id)", as: User.self)
        cache[id] = user
        return user
    }
}
```

### 示例 2：使用 Swift Testing 进行测试

```swift
import Testing
@testable import MyApp

@Test("User parsing should succeed")
func userParsing() async throws {
    let json = """
    { "id": "1", "name": "Alice" }
    """.data(using: .utf8)!
    
    let user = try JSONDecoder().decode(User.self, from: json)
    
    #expect(user.name == "Alice")
    #expect(user.id == "1")
}
```

## 最佳实践

- **Conform to Sendable**: 任何在并发域之间传递的类型都应遵循 `Sendable` 协议。
- **Avoid Global Mutable State**: 避免使用全局变量，除非它们由 Actor 保护。
- **Implicitly Unwrapped Optionals**: 严禁使用强制解包操作符，除非在初始化器中确实无法避免（极少见）。
- **Use `let` over `var`**: 默认使用常量，仅在必要时使用变量。
- **Error Handling**: 优先使用 `throws` 和 `do-catch`，而不是返回 `Optional` 或 `Result` 类型（在 async 上下文中 throws 更自然）。

## 备注

- 始终留意编译器关于并发的警告（Strict Concurrency Checking）。
- 在处理跨 Actor 边界的闭包时，注意捕获列表 `[weak self]` 或 `[unowned self]` 的使用（但在 Task 中通常不需要 weak，除非为了打破循环引用）。
