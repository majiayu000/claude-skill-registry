---
name: combine-migration
description: Migrating from Combine to Swift Observation framework and modern async/await patterns. Covers Publisher to AsyncSequence conversion, ObservableObject to @Observable migration, bridging patterns, and reactive code modernization. Use when user asks about Combine migration, ObservableObject to Observable, Publisher to AsyncSequence, or modernizing reactive code.
allowed-tools: Bash, Read, Write, Edit
license: MIT
compatibility: Xcode 26+ with Swift 6 toolchain on macOS
---

# Combine to Observation Migration

Guide for migrating from Combine framework to modern Swift Observation and async/await patterns.

## Prerequisites

- iOS 17+ / macOS 14+ for Observation framework
- Swift 5.9+

---

## Migration Overview

```
┌─────────────────────────────────────────────────────────────┐
│               COMBINE → MODERN SWIFT                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ObservableObject  →  @Observable                           │
│  @Published        →  Regular properties                    │
│  @ObservedObject   →  Direct reference                      │
│  @StateObject      →  @State                                │
│  @EnvironmentObject→  @Environment                          │
│  Publisher         →  AsyncSequence                          │
│  sink/assign       →  for await / async let                 │
│  Cancellable       →  Task cancellation                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ObservableObject to @Observable

### Before: Combine-based ViewModel

```swift
import Combine
import SwiftUI

class UserViewModel: ObservableObject {
    @Published var name: String = ""
    @Published var email: String = ""
    @Published var isLoading: Bool = false
    @Published private(set) var error: Error?

    private var cancellables = Set<AnyCancellable>()

    init() {
        // Debounce name changes for validation
        $name
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .removeDuplicates()
            .sink { [weak self] name in
                self?.validateName(name)
            }
            .store(in: &cancellables)
    }

    func save() {
        isLoading = true
        // Save logic
    }

    private func validateName(_ name: String) {
        // Validation logic
    }
}

// SwiftUI usage
struct UserView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        Form {
            TextField("Name", text: $viewModel.name)
            TextField("Email", text: $viewModel.email)

            if viewModel.isLoading {
                ProgressView()
            }

            Button("Save") {
                viewModel.save()
            }
        }
    }
}
```

### After: Modern @Observable

```swift
import Observation
import SwiftUI

@Observable
class UserViewModel {
    var name: String = ""
    var email: String = ""
    var isLoading: Bool = false
    private(set) var error: Error?

    // Debouncing with Task
    private var validationTask: Task<Void, Never>?

    var nameDidChange: Void {
        // Called when name changes
        validationTask?.cancel()
        validationTask = Task {
            try? await Task.sleep(for: .milliseconds(300))
            guard !Task.isCancelled else { return }
            await validateName(name)
        }
    }

    func save() async {
        isLoading = true
        defer { isLoading = false }

        do {
            try await saveToServer()
        } catch {
            self.error = error
        }
    }

    private func validateName(_ name: String) async {
        // Async validation
    }

    private func saveToServer() async throws {
        // Network call
    }
}

// SwiftUI usage - simpler!
struct UserView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        Form {
            TextField("Name", text: $viewModel.name)
                .onChange(of: viewModel.name) { _, _ in
                    _ = viewModel.nameDidChange
                }

            TextField("Email", text: $viewModel.email)

            if viewModel.isLoading {
                ProgressView()
            }

            Button("Save") {
                Task { await viewModel.save() }
            }
        }
    }
}
```

### Key Differences

| Combine | Observation |
|---------|-------------|
| `class ViewModel: ObservableObject` | `@Observable class ViewModel` |
| `@Published var` | `var` (automatic) |
| `@StateObject` | `@State` |
| `@ObservedObject` | Direct reference |
| `@EnvironmentObject` | `@Environment` |
| `objectWillChange.send()` | Automatic |

---

## Publisher to AsyncSequence

### Converting Publishers to AsyncSequence

```swift
import Combine

extension Publisher where Failure == Never {
    /// Convert any non-failing Publisher to AsyncSequence
    var values: AsyncStream<Output> {
        AsyncStream { continuation in
            let cancellable = self.sink { value in
                continuation.yield(value)
            }

            continuation.onTermination = { _ in
                cancellable.cancel()
            }
        }
    }
}

extension Publisher {
    /// Convert any Publisher to throwing AsyncSequence
    var throwingValues: AsyncThrowingStream<Output, Error> {
        AsyncThrowingStream { continuation in
            let cancellable = self.sink(
                receiveCompletion: { completion in
                    switch completion {
                    case .finished:
                        continuation.finish()
                    case .failure(let error):
                        continuation.finish(throwing: error)
                    }
                },
                receiveValue: { value in
                    continuation.yield(value)
                }
            )

            continuation.onTermination = { _ in
                cancellable.cancel()
            }
        }
    }
}
```

### Before: Combine Pipeline

```swift
class DataService {
    private var cancellables = Set<AnyCancellable>()

    func startMonitoring() {
        NotificationCenter.default
            .publisher(for: .NSManagedObjectContextDidSave)
            .debounce(for: .milliseconds(500), scheduler: RunLoop.main)
            .sink { [weak self] notification in
                self?.handleContextSave(notification)
            }
            .store(in: &cancellables)
    }

    private func handleContextSave(_ notification: Notification) {
        // Handle save
    }
}
```

### After: AsyncSequence

```swift
class DataService {
    private var monitoringTask: Task<Void, Never>?

    func startMonitoring() {
        monitoringTask = Task {
            // Using new iOS 17+ async notification API
            for await notification in NotificationCenter.default.notifications(named: .NSManagedObjectContextDidSave) {
                // Built-in debouncing with Task.sleep
                try? await Task.sleep(for: .milliseconds(500))
                guard !Task.isCancelled else { return }

                await handleContextSave(notification)
            }
        }
    }

    func stopMonitoring() {
        monitoringTask?.cancel()
        monitoringTask = nil
    }

    private func handleContextSave(_ notification: Notification) async {
        // Handle save
    }
}
```

### Custom AsyncSequence for Events

```swift
// Modern event stream
struct LocationUpdates: AsyncSequence {
    typealias Element = CLLocation

    struct AsyncIterator: AsyncIteratorProtocol {
        let manager: CLLocationManager
        var continuation: AsyncStream<CLLocation>.Continuation?

        mutating func next() async -> CLLocation? {
            // Implementation
            return nil
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(manager: CLLocationManager())
    }
}

// Usage
func trackLocation() async {
    for await location in LocationUpdates() {
        print("New location: \(location)")
    }
}
```

---

## Common Patterns Migration

### Debouncing

```swift
// BEFORE: Combine
$searchText
    .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
    .sink { [weak self] text in
        self?.search(text)
    }
    .store(in: &cancellables)

// AFTER: Task-based debounce
@Observable
class SearchViewModel {
    var searchText: String = "" {
        didSet { debouncedSearch() }
    }

    private var searchTask: Task<Void, Never>?

    private func debouncedSearch() {
        searchTask?.cancel()
        searchTask = Task {
            try? await Task.sleep(for: .milliseconds(300))
            guard !Task.isCancelled else { return }
            await performSearch(searchText)
        }
    }

    private func performSearch(_ query: String) async {
        // Search implementation
    }
}
```

### Throttling

```swift
// BEFORE: Combine
$value
    .throttle(for: .seconds(1), scheduler: RunLoop.main, latest: true)
    .sink { value in
        self.process(value)
    }
    .store(in: &cancellables)

// AFTER: Task-based throttle
actor Throttler {
    private var lastExecution: Date?
    private let interval: Duration

    init(interval: Duration) {
        self.interval = interval
    }

    func throttle(_ action: @escaping () async -> Void) async {
        let now = Date()

        if let last = lastExecution {
            let elapsed = now.timeIntervalSince(last)
            if elapsed < interval.timeInterval {
                return  // Skip this call
            }
        }

        lastExecution = now
        await action()
    }
}

extension Duration {
    var timeInterval: TimeInterval {
        let (seconds, attoseconds) = self.components
        return Double(seconds) + Double(attoseconds) / 1e18
    }
}
```

### CombineLatest / Merge

```swift
// BEFORE: Combine
Publishers.CombineLatest($firstName, $lastName)
    .map { "\($0) \($1)" }
    .sink { fullName in
        self.fullName = fullName
    }
    .store(in: &cancellables)

// AFTER: Computed property (simplest)
@Observable
class PersonViewModel {
    var firstName: String = ""
    var lastName: String = ""

    var fullName: String {
        "\(firstName) \(lastName)"
    }
}

// AFTER: AsyncSequence merge (for streams)
func mergeStreams() async {
    async let stream1 = processStream1()
    async let stream2 = processStream2()

    // Process both concurrently
    let results = await (stream1, stream2)
}

// Task group for dynamic merging
func mergeMultiple<T>(_ sequences: [AsyncStream<T>]) -> AsyncStream<T> {
    AsyncStream { continuation in
        Task {
            await withTaskGroup(of: Void.self) { group in
                for sequence in sequences {
                    group.addTask {
                        for await value in sequence {
                            continuation.yield(value)
                        }
                    }
                }
            }
            continuation.finish()
        }
    }
}
```

### Retry Logic

```swift
// BEFORE: Combine
urlSession.dataTaskPublisher(for: url)
    .retry(3)
    .sink(
        receiveCompletion: { _ in },
        receiveValue: { data, response in }
    )
    .store(in: &cancellables)

// AFTER: async/await retry
func fetchWithRetry(url: URL, maxAttempts: Int = 3) async throws -> Data {
    var lastError: Error?

    for attempt in 1...maxAttempts {
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            return data
        } catch {
            lastError = error

            if attempt < maxAttempts {
                // Exponential backoff
                let delay = Duration.seconds(pow(2, Double(attempt - 1)))
                try await Task.sleep(for: delay)
            }
        }
    }

    throw lastError ?? URLError(.unknown)
}
```

### Error Handling

```swift
// BEFORE: Combine
fetchPublisher()
    .catch { error -> AnyPublisher<Data, Never> in
        return Just(Data()).eraseToAnyPublisher()
    }
    .sink { data in
        self.process(data)
    }
    .store(in: &cancellables)

// AFTER: async/await
func fetchWithFallback() async -> Data {
    do {
        return try await fetchData()
    } catch {
        // Log error
        print("Fetch failed: \(error), using fallback")
        return Data()  // Fallback
    }
}

// Or with Result type
func fetchResult() async -> Result<Data, Error> {
    do {
        let data = try await fetchData()
        return .success(data)
    } catch {
        return .failure(error)
    }
}
```

---

## Bridging Combine and Async/Await

### When You Need Both

Sometimes you need to bridge between systems during migration:

```swift
import Combine

// Combine Publisher from async function
extension Publisher {
    static func fromAsync<T>(_ operation: @escaping () async throws -> T) -> AnyPublisher<T, Error> {
        Deferred {
            Future { promise in
                Task {
                    do {
                        let result = try await operation()
                        promise(.success(result))
                    } catch {
                        promise(.failure(error))
                    }
                }
            }
        }
        .eraseToAnyPublisher()
    }
}

// Usage
let publisher = Publisher.fromAsync {
    try await fetchUserData()
}

// Async function from Combine Publisher
extension Publisher {
    func firstValue() async throws -> Output {
        try await withCheckedThrowingContinuation { continuation in
            var cancellable: AnyCancellable?

            cancellable = self.first().sink(
                receiveCompletion: { completion in
                    switch completion {
                    case .finished:
                        break
                    case .failure(let error):
                        continuation.resume(throwing: error)
                    }
                    cancellable?.cancel()
                },
                receiveValue: { value in
                    continuation.resume(returning: value)
                }
            )
        }
    }
}

// Usage
let user = try await userPublisher.firstValue()
```

### Gradual Migration Strategy

```swift
// Phase 1: Keep Combine internally, expose async API
class LegacyService {
    private var cancellables = Set<AnyCancellable>()

    // Legacy Combine implementation
    private func fetchUserCombine() -> AnyPublisher<User, Error> {
        // Existing Combine code
        URLSession.shared.dataTaskPublisher(for: userURL)
            .map(\.data)
            .decode(type: User.self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
    }

    // New async wrapper
    func fetchUser() async throws -> User {
        try await fetchUserCombine().firstValue()
    }
}

// Phase 2: Rewrite internals to async
class ModernService {
    func fetchUser() async throws -> User {
        let (data, _) = try await URLSession.shared.data(from: userURL)
        return try JSONDecoder().decode(User.self, from: data)
    }
}
```

---

## @Observable with Async Operations

### Loading States Pattern

```swift
@Observable
class DataViewModel {
    enum LoadState<T> {
        case idle
        case loading
        case loaded(T)
        case error(Error)
    }

    var userState: LoadState<User> = .idle

    var isLoading: Bool {
        if case .loading = userState { return true }
        return false
    }

    var user: User? {
        if case .loaded(let user) = userState { return user }
        return nil
    }

    var error: Error? {
        if case .error(let error) = userState { return error }
        return nil
    }

    func loadUser() async {
        userState = .loading

        do {
            let user = try await fetchUser()
            userState = .loaded(user)
        } catch {
            userState = .error(error)
        }
    }

    private func fetchUser() async throws -> User {
        // Fetch implementation
        fatalError()
    }
}

struct UserView: View {
    @State private var viewModel = DataViewModel()

    var body: some View {
        Group {
            switch viewModel.userState {
            case .idle:
                Text("Pull to load")
            case .loading:
                ProgressView()
            case .loaded(let user):
                UserProfileView(user: user)
            case .error(let error):
                ErrorView(error: error) {
                    Task { await viewModel.loadUser() }
                }
            }
        }
        .task {
            await viewModel.loadUser()
        }
    }
}
```

### Observing AsyncSequence

```swift
@Observable
class StreamViewModel {
    var messages: [Message] = []
    private var streamTask: Task<Void, Never>?

    func startListening() {
        streamTask = Task {
            for await message in messageStream() {
                messages.append(message)
            }
        }
    }

    func stopListening() {
        streamTask?.cancel()
    }

    private func messageStream() -> AsyncStream<Message> {
        AsyncStream { continuation in
            // Stream implementation
        }
    }
}

struct MessagesView: View {
    @State private var viewModel = StreamViewModel()

    var body: some View {
        List(viewModel.messages) { message in
            MessageRow(message: message)
        }
        .task {
            viewModel.startListening()
        }
        .onDisappear {
            viewModel.stopListening()
        }
    }
}
```

---

## Migration Checklist

### Step-by-Step Guide

```
□ 1. Identify all ObservableObject classes
□ 2. Convert to @Observable one by one
□ 3. Replace @Published with regular properties
□ 4. Replace @StateObject with @State
□ 5. Replace @ObservedObject with direct reference
□ 6. Replace @EnvironmentObject with @Environment
□ 7. Convert Combine pipelines to async/await
□ 8. Replace cancellables with Task cancellation
□ 9. Update tests to use async/await
□ 10. Remove Combine imports where no longer needed
```

### Common Gotchas

```swift
// GOTCHA 1: @Observable requires class, not struct
@Observable
class ViewModel { }  // ✓ Correct

// GOTCHA 2: @State for @Observable in SwiftUI
@State private var viewModel = ViewModel()  // ✓ iOS 17+

// GOTCHA 3: Manual observation still possible
@Observable
class Model {
    var value: Int = 0
}

// Observe changes manually
let model = Model()
withObservationTracking {
    _ = model.value
} onChange: {
    print("Value changed!")
}

// GOTCHA 4: Task cancellation is cooperative
Task {
    try await Task.sleep(for: .seconds(1))
    guard !Task.isCancelled else { return }  // Must check!
    // Continue work
}
```

---

## Best Practices

### DO

```swift
// ✓ Use @Observable for ViewModels
@Observable class ViewModel { }

// ✓ Use async/await for asynchronous operations
func fetch() async throws -> Data

// ✓ Use Task for launching async work from sync context
Button("Load") {
    Task { await viewModel.load() }
}

// ✓ Cancel tasks on disappear
.task { await viewModel.startMonitoring() }
```

### DON'T

```swift
// ✗ Don't mix ObservableObject and @Observable
// Choose one pattern per class

// ✗ Don't forget to cancel tasks
// Always store and cancel long-running tasks

// ✗ Don't use Combine for new code (iOS 17+)
// Use async/await instead

// ✗ Don't block the main thread
// Use Task.detached for CPU-intensive work
```

---

## Official Resources

- [Observation Framework](https://developer.apple.com/documentation/observation)
- [Migrating from ObservableObject](https://developer.apple.com/documentation/observation/migrating-from-observableobject)
- [WWDC23: Discover Observation in SwiftUI](https://developer.apple.com/videos/play/wwdc2023/10149/)
- [Swift Concurrency Documentation](https://developer.apple.com/documentation/swift/concurrency)
