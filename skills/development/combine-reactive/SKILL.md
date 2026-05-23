---
name: combine-reactive
description: "Expert Combine decisions for iOS/tvOS: when Combine vs async/await, Subject selection trade-offs, operator chain design, and memory management patterns. Use when implementing reactive streams, choosing between concurrency models, or debugging Combine memory leaks. Trigger keywords: Combine, Publisher, Subscriber, Subject, PassthroughSubject, CurrentValueSubject, async/await, AnyCancellable, sink, operators, reactive"
version: "3.0.0"
---

# Combine Reactive — Expert Decisions

Expert decision frameworks for Combine choices. Claude knows Combine syntax — this skill provides judgment calls for when Combine adds value vs async/await and how to avoid common pitfalls.

---

## Decision Trees

### Combine vs Async/Await

```
What's your data flow pattern?
├─ Single async operation (fetch once)
│  └─ async/await
│     Simpler, built into language
│
├─ Stream of values over time
│  └─ Is it UI-driven (user events)?
│     ├─ YES → Combine (debounce, throttle shine here)
│     └─ NO → AsyncSequence may suffice
│
├─ Combining multiple data sources
│  └─ How many sources?
│     ├─ 2-3 → Combine's CombineLatest, Zip
│     └─ Many → Consider structured concurrency (TaskGroup)
│
└─ Existing codebase uses Combine?
   └─ Maintain consistency unless migrating
```

**The trap**: Using Combine for simple one-shot async. `async/await` is cleaner and doesn't need cancellable management.

### Subject Type Selection

```
Do you need to access current value?
├─ YES → CurrentValueSubject
│  Can read .value synchronously
│  New subscribers get current value immediately
│
└─ NO → Is it event-based (discrete occurrences)?
   ├─ YES → PassthroughSubject
   │  No stored value, subscribers only get new emissions
   │
   └─ NO (need replay of past values) →
      Consider external state management
      Combine has no built-in ReplaySubject
```

### Operator Chain Design

```
What transformation is needed?
├─ Value transformation
│  └─ map (simple), compactMap (filter nils), flatMap (nested publishers)
│
├─ Filtering
│  └─ filter, removeDuplicates, first, dropFirst
│
├─ Timing
│  └─ User input → debounce (wait for pause)
│     Scrolling → throttle (rate limit)
│
├─ Error handling
│  └─ Can provide fallback? → catch, replaceError
│     Need retry? → retry(n)
│
└─ Combining streams
   └─ Need all values paired? → zip
      Need latest from each? → combineLatest
      Merge into one stream? → merge
```

---

## NEVER Do

### Subscription Management

**NEVER** forget to store subscriptions:
```swift
// ❌ Subscription cancelled immediately
func loadData() {
    publisher.sink { value in
        self.data = value  // Never called!
    }
    // sink returns AnyCancellable that's immediately deallocated
}

// ✅ Store in Set<AnyCancellable>
private var cancellables = Set<AnyCancellable>()

func loadData() {
    publisher.sink { value in
        self.data = value
    }
    .store(in: &cancellables)
}
```

**NEVER** capture self strongly in sink closures:
```swift
// ❌ Retain cycle — ViewModel never deallocates
publisher
    .sink { value in
        self.updateUI(value)  // Strong capture!
    }
    .store(in: &cancellables)

// ✅ Use [weak self]
publisher
    .sink { [weak self] value in
        self?.updateUI(value)
    }
    .store(in: &cancellables)
```

**NEVER** use assign(to:on:) with classes:
```swift
// ❌ Strong reference to self — retain cycle
publisher
    .assign(to: \.text, on: self)  // Retains self!
    .store(in: &cancellables)

// ✅ Use sink with weak self
publisher
    .sink { [weak self] value in
        self?.text = value
    }
    .store(in: &cancellables)

// Or use assign(to:) with @Published (no retain cycle)
publisher
    .assign(to: &$text)  // Safe — doesn't return cancellable
```

### Subject Misuse

**NEVER** expose subjects directly:
```swift
// ❌ External code can send values
class ViewModel {
    let users = PassthroughSubject<[User], Never>()  // Public subject!
}

// External code:
viewModel.users.send([])  // Breaks encapsulation

// ✅ Expose as Publisher
class ViewModel {
    private let usersSubject = PassthroughSubject<[User], Never>()

    var users: AnyPublisher<[User], Never> {
        usersSubject.eraseToAnyPublisher()
    }
}
```

**NEVER** send on subject from multiple threads without care:
```swift
// ❌ Race condition — undefined behavior
DispatchQueue.global().async {
    subject.send(value1)
}
DispatchQueue.global().async {
    subject.send(value2)
}

// ✅ Serialize access
let subject = PassthroughSubject<Value, Never>()
let serialQueue = DispatchQueue(label: "subject.serial")

serialQueue.async {
    subject.send(value)
}

// Or use .receive(on:) to ensure delivery on specific scheduler
```

### Operator Mistakes

**NEVER** use flatMap when you mean map:
```swift
// ❌ Confusing — flatMap for non-publisher transformation
publisher
    .flatMap { user -> AnyPublisher<String, Never> in
        Just(user.name).eraseToAnyPublisher()  // Overkill!
    }

// ✅ Use map for simple transformation
publisher
    .map { user in user.name }
```

**NEVER** forget to handle errors in sink:
```swift
// ❌ Compiler allows this but errors are ignored
publisher  // Has Error type
    .sink { value in
        // Only handles values, error terminates silently
    }

// ✅ Handle both completion and value
publisher
    .sink(
        receiveCompletion: { completion in
            if case .failure(let error) = completion {
                handleError(error)
            }
        },
        receiveValue: { value in
            handleValue(value)
        }
    )
```

**NEVER** debounce without scheduler on main:
```swift
// ❌ Debouncing on background scheduler, updating UI
searchText
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.global())
    .sink { [weak self] text in
        self?.results = search(text)  // UI update on background thread!
    }

// ✅ Receive on main for UI updates
searchText
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
    .sink { [weak self] text in
        self?.results = search(text)
    }

// Or explicitly receive on main
searchText
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.global())
    .receive(on: DispatchQueue.main)
    .sink { ... }
```

---

## Essential Patterns

### ViewModel with Combine

```swift
@MainActor
final class SearchViewModel: ObservableObject {
    @Published var searchText = ""
    @Published private(set) var results: [SearchResult] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private let searchService: SearchServiceProtocol
    private var cancellables = Set<AnyCancellable>()

    init(searchService: SearchServiceProtocol) {
        self.searchService = searchService
        setupSearch()
    }

    private func setupSearch() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .filter { !$0.isEmpty }
            .handleEvents(receiveOutput: { [weak self] _ in
                self?.isLoading = true
                self?.error = nil
            })
            .flatMap { [weak self] query -> AnyPublisher<[SearchResult], Never> in
                guard let self = self else {
                    return Just([]).eraseToAnyPublisher()
                }
                return self.searchService.search(query: query)
                    .catch { [weak self] error -> Just<[SearchResult]> in
                        self?.error = error
                        return Just([])
                    }
                    .eraseToAnyPublisher()
            }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] results in
                self?.results = results
                self?.isLoading = false
            }
            .store(in: &cancellables)
    }
}
```

### Combine to Async Bridge

```swift
extension Publisher where Failure == Error {
    func async() async throws -> Output {
        try await withCheckedThrowingContinuation { continuation in
            var cancellable: AnyCancellable?
            var didResume = false

            cancellable = first()
                .sink(
                    receiveCompletion: { completion in
                        guard !didResume else { return }
                        didResume = true

                        switch completion {
                        case .finished:
                            break  // Value handled in receiveValue
                        case .failure(let error):
                            continuation.resume(throwing: error)
                        }
                        cancellable?.cancel()
                    },
                    receiveValue: { value in
                        guard !didResume else { return }
                        didResume = true
                        continuation.resume(returning: value)
                    }
                )
        }
    }
}

// Usage
Task {
    let user = try await fetchUserPublisher.async()
}
```

### Event Bus Pattern

```swift
final class EventBus {
    static let shared = EventBus()

    // Private subjects
    private let userLoggedInSubject = PassthroughSubject<User, Never>()
    private let userLoggedOutSubject = PassthroughSubject<Void, Never>()
    private let cartUpdatedSubject = PassthroughSubject<Cart, Never>()

    // Public publishers (read-only)
    var userLoggedIn: AnyPublisher<User, Never> {
        userLoggedInSubject.eraseToAnyPublisher()
    }

    var userLoggedOut: AnyPublisher<Void, Never> {
        userLoggedOutSubject.eraseToAnyPublisher()
    }

    var cartUpdated: AnyPublisher<Cart, Never> {
        cartUpdatedSubject.eraseToAnyPublisher()
    }

    // Send methods
    func send(userLoggedIn user: User) {
        userLoggedInSubject.send(user)
    }

    func sendUserLoggedOut() {
        userLoggedOutSubject.send()
    }

    func send(cartUpdated cart: Cart) {
        cartUpdatedSubject.send(cart)
    }
}
```

---

## Quick Reference

### Combine vs Async/Await Decision

| Scenario | Prefer |
|----------|--------|
| Single async call | async/await |
| Stream of values | Combine |
| User input debouncing | Combine |
| Combining multiple API calls | Either (async let or CombineLatest) |
| Existing Combine codebase | Combine for consistency |
| New project, simple needs | async/await |

### Subject Comparison

| Subject | Stores Value | New Subscribers Get |
|---------|--------------|---------------------|
| PassthroughSubject | No | Only new values |
| CurrentValueSubject | Yes | Current + new values |

### Common Operators

| Category | Operators |
|----------|-----------|
| Transform | map, flatMap, compactMap, scan |
| Filter | filter, removeDuplicates, first, dropFirst |
| Combine | combineLatest, zip, merge |
| Timing | debounce, throttle, delay |
| Error | catch, retry, replaceError |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Subscription not stored | Immediate cancellation | .store(in: &cancellables) |
| Strong self in sink | Retain cycle | [weak self] |
| assign(to:on:self) | Retain cycle | Use sink or assign(to:&$property) |
| Public Subject | Encapsulation broken | Expose as AnyPublisher |
| flatMap for simple transform | Overkill | Use map |
| Debounce on background, sink updates UI | Threading bug | receive(on: .main) |
| Empty receiveCompletion | Errors ignored | Handle .failure case |
