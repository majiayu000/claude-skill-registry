---
name: swiftui-patterns
description: "Build SwiftUI views with modern MV architecture, state management, and view composition patterns. Covers @Observable ownership rules, @State/@Bindable/@Environment wiring, view decomposition, custom ViewModifiers, environment values, async data loading with .task, iOS 26+ APIs, Writing Tools, and performance guidelines. Use when structuring a SwiftUI app, managing state with @Observable, composing view hierarchies, or applying SwiftUI best practices."
---

# SwiftUI Patterns

Modern SwiftUI patterns targeting iOS 26+ with Swift 6.2. Covers architecture, state management, view composition, environment wiring, async loading, design polish, and platform/share integration. Navigation and layout patterns live in dedicated sibling skills. Patterns are backward-compatible to iOS 17 unless noted.

## Contents

- [Architecture: Model-View (MV) Pattern](#architecture-model-view-mv-pattern)
- [State Management](#state-management)
- [View Ordering Convention](#view-ordering-convention)
- [View Composition](#view-composition)
- [Environment](#environment)
- [Async Data Loading](#async-data-loading)
- [iOS 26+ New APIs](#ios-26-new-apis)
- [Performance Guidelines](#performance-guidelines)
- [HIG Alignment](#hig-alignment)
- [Writing Tools (iOS 18+)](#writing-tools-ios-18)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

**Scope boundary:** This skill covers architecture, state ownership, composition, environment wiring, async loading, and related SwiftUI app structure patterns. Detailed navigation patterns are covered in the `swiftui-navigation` skill, including `NavigationStack`, `NavigationSplitView`, sheets, tabs, and deep-linking patterns. Detailed layout, container, and component patterns are covered in the `swiftui-layout-components` skill, including stacks, grids, lists, scroll view patterns, forms, controls, search UI with `.searchable`, overlays, and related layout components.

## Architecture: Model-View (MV) Pattern

Default to MV -- views are lightweight state expressions; models and services own business logic. Do not introduce view models unless the existing code already uses them.

**Core principles:**
- Favor `@State`, `@Environment`, `@Query`, `.task`, and `.onChange` for orchestration
- Inject services and shared models via `@Environment`; keep views small and composable
- Split large views into smaller subviews rather than introducing a view model
- Test models, services, and business logic; keep views simple and declarative

```swift
struct FeedView: View {
    @Environment(FeedClient.self) private var client

    enum ViewState {
        case loading, error(String), loaded([Post])
    }

    @State private var viewState: ViewState = .loading

    var body: some View {
        List {
            switch viewState {
            case .loading:
                ProgressView()
            case .error(let message):
                ContentUnavailableView("Error", systemImage: "exclamationmark.triangle",
                                       description: Text(message))
            case .loaded(let posts):
                ForEach(posts) { post in
                    PostRow(post: post)
                }
            }
        }
        .task { await loadFeed() }
        .refreshable { await loadFeed() }
    }

    private func loadFeed() async {
        do {
            let posts = try await client.getFeed()
            viewState = .loaded(posts)
        } catch {
            viewState = .error(error.localizedDescription)
        }
    }
}
```

For MV pattern rationale, app wiring, and lightweight client examples, see `references/architecture-patterns.md`.

## State Management

### @Observable Ownership Rules

**Important:** Always annotate `@Observable` view model classes with `@MainActor` to ensure UI-bound state is updated on the main thread. Required for Swift 6 concurrency safety.

| Wrapper | When to Use |
|---------|-------------|
| `@State` | View owns the object or value. Creates and manages lifecycle. |
| `let` | View receives an `@Observable` object. Read-only observation -- no wrapper needed. |
| `@Bindable` | View receives an `@Observable` object and needs two-way bindings (`$property`). |
| `@Environment(Type.self)` | Access shared `@Observable` object from environment. |
| `@State` (value types) | View-local simple state: toggles, counters, text field values. Always `private`. |
| `@Binding` | Two-way connection to parent's `@State` or `@Bindable` property. |

### Ownership Pattern

```swift
// @Observable view model -- always @MainActor
@MainActor
@Observable final class ItemStore {
    var title = ""
    var items: [Item] = []
}

// View that OWNS the model
struct ParentView: View {
    @State var viewModel = ItemStore()

    var body: some View {
        ChildView(store: viewModel)
            .environment(viewModel)
    }
}

// View that READS (no wrapper needed for @Observable)
struct ChildView: View {
    let store: ItemStore

    var body: some View { Text(store.title) }
}

// View that BINDS (needs two-way access)
struct EditView: View {
    @Bindable var store: ItemStore

    var body: some View {
        TextField("Title", text: $store.title)
    }
}

// View that reads from ENVIRONMENT
struct DeepView: View {
    @Environment(ItemStore.self) var store

    var body: some View {
        @Bindable var s = store
        TextField("Title", text: $s.title)
    }
}
```

**Granular tracking:** SwiftUI only re-renders views that read properties that changed. If a view reads `items` but not `isLoading`, changing `isLoading` does not trigger a re-render. This is a major performance advantage over `ObservableObject`.

### Legacy ObservableObject

Only use if supporting iOS 16 or earlier. `@StateObject` → `@State`, `@ObservedObject` → `let`, `@EnvironmentObject` → `@Environment(Type.self)`.

## View Ordering Convention

Order members top to bottom: 1) `@Environment` 2) `let` properties 3) `@State` / stored properties 4) computed `var` 5) `init` 6) `body` 7) view builders / helpers 8) async functions

## View Composition

### Extract Subviews

Break views into focused subviews. Each should have a single responsibility.

```swift
var body: some View {
    VStack {
        HeaderSection(title: title, isPinned: isPinned)
        DetailsSection(details: details)
        ActionsSection(onSave: onSave, onCancel: onCancel)
    }
}
```

### Computed View Properties

Keep related subviews as computed properties in the same file; extract to a standalone `View` struct when reuse is intended or the subview carries its own state.

```swift
var body: some View {
    List {
        header
        filters
        results
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}
```

### ViewBuilder Functions

For conditional logic that does not warrant a separate struct:

```swift
@ViewBuilder
private func statusBadge(for status: Status) -> some View {
    switch status {
    case .active: Text("Active").foregroundStyle(.green)
    case .inactive: Text("Inactive").foregroundStyle(.secondary)
    }
}
```

### Custom View Modifiers

Extract repeated styling into `ViewModifier`:

```swift
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 2)
    }
}
extension View { func cardStyle() -> some View { modifier(CardStyle()) } }
```

### Stable View Tree

Avoid top-level conditional view swapping. Prefer a single stable base view with conditions inside sections or modifiers. When a view file exceeds ~300 lines, split with extensions and `// MARK: -` comments.

## Environment

### Custom Environment Values

```swift
private struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .default
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// Usage
.environment(\.theme, customTheme)
@Environment(\.theme) var theme
```

### Common Built-in Environment Values

```swift
@Environment(\.dismiss) var dismiss
@Environment(\.colorScheme) var colorScheme
@Environment(\.dynamicTypeSize) var dynamicTypeSize
@Environment(\.horizontalSizeClass) var sizeClass
@Environment(\.isSearching) var isSearching
@Environment(\.openURL) var openURL
@Environment(\.modelContext) var modelContext
```

## Async Data Loading

Always use `.task` -- it cancels automatically on view disappear:

```swift
struct ItemListView: View {
    @State var store = ItemStore()

    var body: some View {
        List(store.items) { item in
            ItemRow(item: item)
        }
        .task { await store.load() }
        .refreshable { await store.refresh() }
    }
}
```

Use `.task(id:)` to re-run when a dependency changes:

```swift
.task(id: searchText) {
    guard !searchText.isEmpty else { return }
    await search(query: searchText)
}
```

Never create manual `Task` in `onAppear` unless you need to store a reference for cancellation. Exception: `Task {}` is acceptable in synchronous action closures (e.g., Button actions) for immediate state updates before async work.

## iOS 26+ New APIs

- **`.scrollEdgeEffectStyle(.soft, for: .top)`** -- fading edge effect on scroll edges
- **`.backgroundExtensionEffect()`** -- mirror/blur at safe area edges
- **`@Animatable`** macro -- synthesizes `AnimatableData` conformance automatically (see `swiftui-animation` skill)
- **`TextEditor`** -- now accepts `AttributedString` for rich text

## Performance Guidelines

- **Lazy stacks/grids:** Use `LazyVStack`, `LazyHStack`, `LazyVGrid`, `LazyHGrid` for large collections. Regular stacks render all children immediately.
- **Stable IDs:** All items in `List`/`ForEach` must conform to `Identifiable` with stable IDs. Never use array indices.
- **Avoid body recomputation:** Move filtering and sorting to computed properties or the model, not inline in `body`.
- **Equatable views:** For complex views that re-render unnecessarily, conform to `Equatable`.

## HIG Alignment

Follow Apple Human Interface Guidelines for layout, typography, color, and accessibility. Key rules:

- Use semantic colors (`Color.primary`, `.secondary`, `Color(uiColor: .systemBackground)`) for automatic light/dark mode
- Use system font styles (`.title`, `.headline`, `.body`, `.caption`) for Dynamic Type support
- Use `ContentUnavailableView` for empty and error states
- Support adaptive layouts via `horizontalSizeClass`
- Provide VoiceOver labels (`.accessibilityLabel`) and support Dynamic Type accessibility sizes by switching layout orientation

See `references/design-polish.md` for HIG, theming, haptics, focus, transitions, and loading patterns.

## Writing Tools (iOS 18+)

Control the Apple Intelligence Writing Tools experience on text views with `.writingToolsBehavior(_:)`.

| Level | Effect | When to use |
|-------|--------|-------------|
| `.complete` | Full inline rewriting (proofread, rewrite, transform) | Notes, email, documents |
| `.limited` | Overlay panel only — original text untouched | Code editors, validated forms |
| `.disabled` | Writing Tools hidden entirely | Passwords, search bars |
| `.automatic` | System chooses based on context (default) | Most views |

```swift
TextEditor(text: $body)
    .writingToolsBehavior(.complete)
TextField("Search…", text: $query)
    .writingToolsBehavior(.disabled)
```

**Detecting active sessions:** Read `isWritingToolsActive` on `UITextView` (UIKit) to defer validation or suspend undo grouping until a rewrite finishes.

> **Docs:** [WritingToolsBehavior](https://sosumi.ai/documentation/swiftui/writingtoolsbehavior) · [writingToolsBehavior(_:)](https://sosumi.ai/documentation/swiftui/view/writingtoolsbehavior(_:))

## Common Mistakes

1. Using `@ObservedObject` to create objects -- use `@StateObject` (legacy) or `@State` (modern)
2. Heavy computation in view `body` -- move to model or computed property
3. Not using `.task` for async work -- manual `Task` in `onAppear` leaks if not cancelled
4. Array indices as `ForEach` IDs -- causes incorrect diffing and UI bugs
5. Forgetting `@Bindable` -- `$property` syntax on `@Observable` requires `@Bindable`
6. Over-using `@State` -- only for view-local state; shared state belongs in `@Observable`
7. Not extracting subviews -- long body blocks are hard to read and optimize
8. Using `NavigationView` -- deprecated; use `NavigationStack`
9. Inline closures in body -- extract complex closures to methods
10. `.sheet(isPresented:)` when state represents a model -- use `.sheet(item:)` instead
11. **Using `AnyView` for type erasure** -- causes identity resets and disables diffing. Use `@ViewBuilder`, `Group`, or generics instead. See `references/deprecated-migration.md`

## Review Checklist

- [ ] `@Observable` used for shared state models (not `ObservableObject` on iOS 17+)
- [ ] `@State` owns objects; `let`/`@Bindable` receives them
- [ ] `NavigationStack` used (not `NavigationView`)
- [ ] `.task` modifier for async data loading
- [ ] `LazyVStack`/`LazyHStack` for large collections
- [ ] Stable `Identifiable` IDs (not array indices)
- [ ] Views decomposed into focused subviews
- [ ] No heavy computation in view `body`
- [ ] Environment used for deeply shared state
- [ ] Custom `ViewModifier` for repeated styling
- [ ] `.sheet(item:)` preferred over `.sheet(isPresented:)`
- [ ] Sheets own their actions and call `dismiss()` internally
- [ ] MV pattern followed -- no unnecessary view models
- [ ] `@Observable` view model classes are `@MainActor`-isolated
- [ ] Model types passed across concurrency boundaries are `Sendable`

## References

- Architecture, app wiring, and lightweight clients: `references/architecture-patterns.md`
- Design polish (HIG, theming, haptics, transitions, loading, focus): `references/design-polish.md`
- Deprecated API migration: `references/deprecated-migration.md`
- Platform and sharing patterns (Transferable, media, menus, macOS settings): `references/platform-and-sharing.md`

