---
name: swift-composable-architecture
description: Use when building, refactoring, debugging, or testing iOS/macOS features using The Composable Architecture (TCA). Covers feature structure, effects, dependencies, navigation patterns, and testing with TestStore.
license: MIT
metadata:
  author: hakonbogen
  version: "1.0.0"
---

You are an expert in The Composable Architecture (TCA) by Point-Free. Help developers write correct, testable, and composable Swift code following TCA patterns.

## Core Principles

- **Unidirectional data flow**: Action → Reducer → State → View
- **State as value types**: Simple, equatable structs
- **Effects are explicit**: Side effects return from reducers as `Effect` values
- **Composition over inheritance**: Small, isolated, recombinable modules
- **Testability first**: Every feature testable with `TestStore`

## The Four Building Blocks

1. **State** – Data for UI and logic (`@ObservableState struct`)
2. **Action** – All events: user actions, effects, delegates (`enum` with `@CasePathable`)
3. **Reducer** – Pure function evolving state, returning effects (`@Reducer macro`)
4. **Store** – Runtime connecting state, reducer, and views (`StoreOf<Feature>`)

## Feature Structure

```swift
@Reducer
struct Feature {
  @ObservableState
  struct State: Equatable {
    var items: IdentifiedArrayOf<Item> = []
    var isLoading = false
  }

  @CasePathable
  enum Action {
    case onAppear
    case itemsResponse(Result<[Item], Error>)
    case delegate(Delegate)
    @CasePathable
    enum Delegate { case itemSelected(Item) }
  }

  @Dependency(\.apiClient) var apiClient

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case .onAppear:
        state.isLoading = true
        return .run { send in
          await send(.itemsResponse(Result { try await apiClient.fetchItems() }))
        }
      case .itemsResponse(.success(let items)):
        state.isLoading = false
        state.items = IdentifiedArray(uniqueElements: items)
        return .none
      case .itemsResponse(.failure):
        state.isLoading = false
        return .none
      case .delegate:
        return .none
      }
    }
  }
}
```

## Store and View Connection

```swift
struct FeatureView: View {
  let store: StoreOf<Feature>

  var body: some View {
    List(store.items) { item in
      Text(item.title)
    }
    .onAppear { store.send(.onAppear) }
  }
}
```

Create store at app entry, pass down to views - never create stores inside views.

## Effects

| Pattern | Use Case |
|---------|----------|
| `.none` | Synchronous state change, no side effect |
| `.run { send in }` | Async work, send actions back |
| `.cancellable(id:)` | Long-running/replaceable effects |
| `.cancel(id:)` | Cancel a running effect |
| `.merge(...)` | Run multiple effects in parallel |
| `.concatenate(...)` | Run effects sequentially |

### Cancellation

```swift
enum CancelID { case search }

case .searchQueryChanged(let query):
  return .run { send in
    try await clock.sleep(for: .milliseconds(300))
    await send(.searchResponse(try await api.search(query)))
  }
  .cancellable(id: CancelID.search, cancelInFlight: true)
```

`cancelInFlight: true` auto-cancels previous effect with same ID.

## Dependencies

### Built-in Dependencies

`@Dependency(\.uuid)`, `@Dependency(\.date)`, `@Dependency(\.continuousClock)`, `@Dependency(\.mainQueue)`

### Custom Dependencies

1. Define client struct with closures
2. Conform to `DependencyKey` with `liveValue`, `testValue`, `previewValue`
3. Extend `DependencyValues` with computed property
4. Use `@Dependency(\.yourClient)` in reducer

Test override: `withDependencies { $0.apiClient.fetch = { .mock } }`

## Composition

### Child Features

Use `Scope` to embed children:

```swift
var body: some ReducerOf<Self> {
  Scope(state: \.child, action: \.child) { ChildFeature() }
  Reduce { state, action in ... }
}
```

View: `ChildView(store: store.scope(state: \.child, action: \.child))`

### Collections

Use `IdentifiedArrayOf<ChildFeature.State>` with `.forEach(\.items, action: \.items) { ChildFeature() }`

## Navigation

### Tree-Based (sheets, alerts, single drill-down)

- Model with optional state: `@Presents var detail: DetailFeature.State?`
- Action: `case detail(PresentationAction<DetailFeature.Action>)`
- Reducer: `.ifLet(\.$detail, action: \.detail) { DetailFeature() }`
- View: `.sheet(item: $store.scope(state: \.detail, action: \.detail))`

### Stack-Based (NavigationStack, deep linking)

- Model with `StackState<Path.State>` and `StackActionOf<Path>`
- Define `@Reducer enum Path { case detail(DetailFeature) ... }`
- Reducer: `.forEach(\.path, action: \.path)`
- View: `NavigationStack(path: $store.scope(state: \.path, action: \.path))`

### Delegates

Child emits delegate actions for outcomes; parent responds without child knowing parent's implementation.

## Testing

### TestStore Basics

```swift
let store = TestStore(initialState: Feature.State()) {
  Feature()
} withDependencies: {
  $0.apiClient.fetch = { .mock }
}

await store.send(.onAppear) { $0.isLoading = true }
await store.receive(\.itemsResponse.success) { $0.isLoading = false; $0.items = [.mock] }
```

### Key Patterns

- **Override dependencies** - never hit real APIs in tests
- **Assert all state changes** - mutations in trailing closure
- **Receive all effects** - TestStore enforces exhaustivity
- **TestClock** - control time-based effects with `clock.advance(by:)`
- **Integration tests** - test composed parent+child features together

## Higher-Order Reducers

For cross-cutting concerns (logging, analytics, metrics, feature flags):

```swift
extension Reducer {
  func analytics(_ tracker: AnalyticsClient) -> some ReducerOf<Self> {
    Reduce { state, action in
      tracker.track(action)
      return self.reduce(into: &state, action: action)
    }
  }
}
```

## Modern TCA (2025+)

- `@Reducer` macro generates boilerplate
- `@ObservableState` replaces manual `WithViewStore`
- `@CasePathable` enables key path syntax for actions (`\.action.child`)
- `@Dependency` with built-in clients (Clock, UUID, Date)
- `@MainActor` on State when SwiftUI requires it
- Direct store access in views (no more `viewStore`)

## Critical Rules

### DO:
- Keep reducers pure - side effects through `Effect` only
- Use `IdentifiedArray` for collections
- Test state transitions and effect outputs
- Use delegates for child→parent communication

### DO NOT:
- Mutate state outside reducers
- Call async code directly in reducers
- Create stores inside views
- Use `@State`/`@StateObject` for TCA-managed state
- Skip receiving actions in tests
