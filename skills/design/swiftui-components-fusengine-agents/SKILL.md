---
name: swiftui-components
description: Build production SwiftUI views, custom components, layouts, and view modifiers. Use when creating iOS/macOS UI components, implementing responsive layouts, building custom modifiers, or designing reusable view hierarchies with @ViewBuilder.
user-invocable: false
---

# SwiftUI Components & Views

## Core Principles

1. **Small, focused views** - Extract subviews at 30+ lines
2. **Composition over inheritance** - Use ViewBuilder and modifiers
3. **Preview-driven development** - Always include #Preview

## View Structure Pattern

```swift
struct FeatureView: View {
    // MARK: - State
    @State private var isLoading = false

    // MARK: - Environment
    @Environment(\.dismiss) private var dismiss

    // MARK: - Body
    var body: some View {
        content
            .navigationTitle("Feature")
            .toolbar { toolbarContent }
    }

    // MARK: - Subviews
    @ViewBuilder
    private var content: some View {
        if isLoading {
            ProgressView()
        } else {
            mainContent
        }
    }
}
```

## Custom Modifiers

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 4)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}
```

## Responsive Layouts

```swift
struct AdaptiveGrid: View {
    @Environment(\.horizontalSizeClass) var sizeClass

    var columns: [GridItem] {
        Array(repeating: GridItem(.flexible(), spacing: 16),
              count: sizeClass == .compact ? 2 : 4)
    }

    var body: some View {
        LazyVGrid(columns: columns, spacing: 16) {
            ForEach(items) { ItemCard(item: $0) }
        }
    }
}
```

## Best Practices

- Use `@ViewBuilder` for conditional content
- Prefer `some View` return type
- Extract magic numbers to constants
- Use semantic colors: `.primary`, `.secondary`
- Add `.accessibilityLabel()` to icons
