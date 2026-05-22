---
name: swiftui-development
description: Specialized in building user interfaces using modern SwiftUI, covering NavigationStack, Observation framework, and SwiftData integration. Use this skill when writing SwiftUI view files, designing app navigation, handling animations and transitions, or binding ViewModel data to the interface.
---

# SwiftUI Development Skill

## Instructions

Use this skill to write declarative, reactive UI code. Always adhere to the iOS Human Interface Guidelines (HIG).

## What This Skill Does

- **UI Construction**: Build interfaces using Views, Modifiers, and Layout containers.
- **State Management**: Manage data flow using the Observation framework (`@Observable`, `@State`, `@Environment`).
- **Navigation**: Handle routing using `NavigationStack` and `navigationDestination`.
- **Previews**: Rapidly iterate on UI using the `#Preview` macro.
- **Persistence Integration**: Seamlessly integrate SwiftData (`@Query`) into views.

## When to Use This Skill

- When writing `.swift` view files.
- When designing the App's navigation structure.
- When handling animations and transitions.
- When binding ViewModel data to the interface.

## Examples

### Example 1: Observation-based ViewModel and View

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

### Example 2: Type-Safe Navigation with NavigationStack

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

## Best Practices

- **Single Source of Truth**: Always maintain a single source of truth for your data.
- **Environment**: Use `.environment()` to inject global dependencies or theme data.
- **Avoid Massive Views**: Break down complex views into smaller component views (`struct SubView: View`).
- **State vs Binding**: Use `@State` when the view owns the data, and `@Binding` (`@Bindable` for Observables) when it modifies parent data.
- **Computed Properties**: Use computed properties to derive UI state instead of manually syncing multiple state variables.

## Notes

- For iOS 17+, `@Observable` is preferred. For legacy support, fallback to `ObservableObject` may be needed, but strictly mark it.
- All UI updates must be performed on the main thread (SwiftUI generally handles this, but be careful with callbacks from background tasks).
