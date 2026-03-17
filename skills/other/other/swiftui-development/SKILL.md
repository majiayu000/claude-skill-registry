---
name: swiftui-development
description: 专注于使用 modern SwiftUI 构建用户界面，涵盖 NavigationStack, Observation 框架和 SwiftData 集成。使用此技能编写 SwiftUI 视图文件、设计应用导航结构、处理动画和转场效果，或将 ViewModel 数据绑定到界面时使用。
---

# SwiftUI 开发技能

## 指令

使用此技能编写声明式、响应式的 UI 代码。始终遵循 iOS 人机交互指南 (HIG)。

## 此技能的功能

- **UI 构建**: 使用 View, Modifier, Layout 容器构建界面。
- **状态管理**: 使用 Observation 框架 (`@Observable`, `@State`, `@Environment`) 管理数据流。
- **导航**: 使用 `NavigationStack` 和 `navigationDestination` 处理路由。
- **预览**: 使用 `#Preview` 宏快速迭代 UI。
- **持久化集成**: 将 SwiftData (`@Query`) 无缝集成到视图中。

## 何时使用此技能

- 编写 `.swift` 视图文件时。
- 设计 App 的导航结构时。
- 处理动画和转场效果时。
- 将 ViewModel 的数据绑定到界面时。

## 示例

### 示例 1：基于 Observation 的 ViewModel 和 View

```swift
@Observable
class CounterModel {
    var count = 0
    
    func increment() {
        count += 1
    }
}

struct CounterView: View {
    @State private var model = CounterModel()
    
    var body: some View {
        VStack {
            Text("Count: \(model.count)")
                .font(.largeTitle)
            Button("Add") {
                model.increment()
            }
        }
    }
}

#Preview {
    CounterView()
}
```

### 示例 2：使用 NavigationStack 进行类型安全导航

```swift
enum Route: Hashable {
    case profile(id: String)
    case settings
}

struct ContentView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Go to Profile", value: Route.profile(id: "123"))
                NavigationLink("Settings", value: Route.settings)
            }
            .navigationDestination(for: Route.self) { route in
                switch route {
                case .profile(let id):
                    ProfileView(userId: id)
                case .settings:
                    SettingsView()
                }
            }
        }
    }
}
```

## 最佳实践

- **Single Source of Truth**: 始终保持单一数据源。
- **Environment**: 使用 `.environment()` 注入全局依赖或主题数据。
- **Avoid Massive Views**: 将复杂的视图拆分为小的组件视图 (`struct SubView: View`)。
- **State vs Binding**: 当视图拥有数据时使用 `@State`，当视图仅修改父视图数据时使用 `@Binding` (`@Bindable` for Observable)。
- **Computed Properties**: 使用计算属性来派生 UI 状态，而不是手动同步多个状态变量。

## 备注

- 对于 IOS 17+，`@Observable` 是首选。对于旧版本支持，可能需要退回到 `ObservableObject`，但应明确标注。
- 所有的 UI 更新必须在主线程执行（SwiftUI 通常会自动处理，但从后台任务回调时要注意）。
