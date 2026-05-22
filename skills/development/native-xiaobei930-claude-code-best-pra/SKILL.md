---
name: native
description: "Native app development strategies including iOS/macOS (Apple platforms). Use when developing native mobile or desktop applications. Future: android."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 原生应用开发

本技能提供原生应用开发的策略选择指南，整合各平台特定的开发模式。

## 子文件

- [ios.md](ios.md) - iOS/macOS 开发指南
- [swift-concurrency.md](swift-concurrency.md) - Swift 并发编程
- [swiftui-performance.md](swiftui-performance.md) - SwiftUI 性能优化

## 原生 vs 跨平台

| 维度     | 原生开发   | 跨平台 (Flutter/RN) |
| -------- | ---------- | ------------------- |
| 性能     | 最佳       | 接近原生            |
| 平台特性 | 完全支持   | 部分支持            |
| 开发成本 | 各平台独立 | 一套代码            |
| 维护成本 | 较高       | 较低                |
| 用户体验 | 最佳       | 良好                |

**选择原生开发的场景**：

- 性能敏感应用（游戏、视频）
- 深度平台集成（系统 API、硬件）
- 追求极致用户体验
- 团队有平台专业知识

## 平台概览

### Apple 平台（iOS/macOS）

**覆盖范围**：iOS/iPadOS、macOS、watchOS/tvOS

**技术栈**：Swift 6.x、SwiftUI / UIKit、Xcode

详细指南参阅 `ios.md`

### Android（未来）

**覆盖范围**：Android 手机/平板、Wear OS、Android TV

**技术栈**：Kotlin、Jetpack Compose / View、Android Studio

## 通用最佳实践

### 架构模式

| 模式               | iOS                   | Android             |
| ------------------ | --------------------- | ------------------- |
| MVVM               | SwiftUI + @Observable | Compose + ViewModel |
| Clean Architecture | 分层 + 协议           | 分层 + 接口         |
| 依赖注入           | Swift DI              | Hilt/Koin           |

### 性能优化

1. **启动优化** - 延迟加载、预加载
2. **内存管理** - 避免循环引用、及时释放
3. **UI 流畅** - 主线程保持响应、异步处理
4. **电量优化** - 减少后台任务、优化网络请求

### 测试策略

| 层级     | 覆盖内容            |
| -------- | ------------------- |
| 单元测试 | 业务逻辑、ViewModel |
| 集成测试 | 网络层、数据层      |
| UI 测试  | 关键用户流程        |

---

**记住**：原生开发追求的是最佳的平台体验，选择原生意味着要深入理解平台特性。
