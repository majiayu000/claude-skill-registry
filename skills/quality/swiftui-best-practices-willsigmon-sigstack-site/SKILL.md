---
name: SwiftUI Best Practices Enforcer
description: Audit and fix SwiftUI anti-patterns in Leavn - @State in wrong places, heavy View body computation, missing @MainActor, improper property wrappers
allowed-tools: Read, Edit, Grep
---

# SwiftUI Best Practices Enforcer

Fix SwiftUI anti-patterns:

1. **@State for ViewModels**: Move to ViewModel property
2. **Heavy View body**: Extract to ViewModel computed property
3. **Missing @MainActor**: Add to ViewModels
4. **Property wrapper mistakes**:
   - @Observable → @State or @Bindable
   - ObservableObject → @StateObject or @ObservedObject

5. **Leavn patterns**:
   - ViewModels: @Observable + @MainActor
   - Services: Protocol-based, injected via DIContainer
   - State: In ViewModel, not View
   - Bindings: Use @Bindable for @Observable types

Use when: SwiftUI issues, performance problems, architecture violations
