---
name: Swift Concurrency
description: Use when swift's modern concurrency model including async/await, actors, task groups, structured concurrency, and async sequences for building safe, performant concurrent code without data races or callback pyramids.
allowed-tools: []
---

# Swift Concurrency

## Introduction

Swift's modern concurrency model provides structured, safe concurrent
programming through async/await syntax, actors for data isolation, and task
management primitives. This system eliminates common concurrency bugs like data
races and callback hell while improving code readability and maintainability.

Introduced in Swift 5.5, the concurrency model integrates with the language's
type system to enforce safety at compile time. Actors protect mutable state,
async/await makes asynchronous code look synchronous, and structured
concurrency ensures tasks are properly managed and cancelled.

This skill covers async functions, actors, task groups, cancellation, async
sequences, and patterns for migrating from completion handlers to modern
concurrency.

## Async/Await Fundamentals

Async/await syntax enables writing asynchronous code that reads like synchronous
code, without nested callbacks or complex error handling chains.

```swift
// Basic async function
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Calling async functions
func loadUserProfile() async {
    do {
        let user = try await fetchUser(id: 42)
        print("Loaded user: \(user.name)")
    } catch {
        print("Failed to load user: \(error)")
    }
}

// Sequential async calls
func loadFullProfile() async throws -> Profile {
    let user = try await fetchUser(id: 42)
    let posts = try await fetchPosts(userId: user.id)
    let comments = try await fetchComments(userId: user.id)

    return Profile(user: user, posts: posts, comments: comments)
}

// Parallel async calls with async let
func loadProfileParallel() async throws -> Profile {
    async let user = fetchUser(id: 42)
    async let posts = fetchPosts(userId: 42)
    async let comments = fetchComments(userId: 42)

    return try await Profile(
        user: user,
        posts: posts,
        comments: comments
    )
}

// Async properties
struct UserRepository {
    var currentUser: User {
        get async throws {
            return try await fetchUser(id: getCurrentUserId())
        }
    }
}

// Using async properties
func displayUser(repo: UserRepository) async {
    do {
        let user = try await repo.currentUser
        print(user.name)
    } catch {
        print("Error: \(error)")
    }
}

// Async initializers
class DataManager {
    let data: Data

    init() async throws {
        let url = URL(string: "https://api.example.com/config")!
        let (data, _) = try await URLSession.shared.data(from: url)
        self.data = data
    }
}
```

Async functions suspend execution at await points, allowing other work to
proceed without blocking threads. The runtime manages suspension and resumption
efficiently.

## Actors for Safe Concurrency

Actors protect mutable state from concurrent access, preventing data races by
ensuring only one task can access actor-isolated state at a time.

```swift
// Basic actor
actor Counter {
    private var value = 0

    func increment() {
        value += 1
    }

    func getValue() -> Int {
        return value
    }
}

// Using actors
func useCounter() async {
    let counter = Counter()

    await counter.increment()
    let value = await counter.getValue()
    print("Counter: \(value)")
}

// Actor with async methods
actor ImageCache {
    private var cache: [URL: Image] = [:]

    func image(for url: URL) async throws -> Image {
        if let cached = cache[url] {
            return cached
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        guard let image = Image(data: data) else {
            throw ImageError.invalidData
        }

        cache[url] = image
        return image
    }

    func clear() {
        cache.removeAll()
    }
}

enum ImageError: Error {
    case invalidData
}

struct Image {
    init?(data: Data) {
        // Initialize image
        return nil
    }
}

// MainActor for UI updates
@MainActor
class ViewModel: ObservableObject {
    @Published var users: [User] = []

    func loadUsers() async {
        do {
            let fetchedUsers = try await fetchAllUsers()
            users = fetchedUsers // Safe: on main actor
        } catch {
            print("Failed to load users: \(error)")
        }
    }
}

func fetchAllUsers() async throws -> [User] {
    return []
}

// Nonisolated methods
actor DatabaseManager {
    private var connection: Connection?

    nonisolated func formatQuery(_ query: String) -> String {
        // Doesn't access actor state, no await needed
        return query.trimmingCharacters(in: .whitespaces)
    }

    func execute(_ query: String) async throws {
        // Accesses actor state
        guard let connection = connection else {
            throw DatabaseError.notConnected
        }
        // Execute query
    }
}

struct Connection {}
enum DatabaseError: Error {
    case notConnected
}

// Global actor for custom isolation
@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

@DatabaseActor
class QueryBuilder {
    var table: String = ""

    func buildQuery() -> String {
        return "SELECT * FROM \(table)"
    }
}
```

Actors automatically serialize access to their state, eliminating data races
while maintaining code clarity and avoiding manual lock management.

## Structured Concurrency with Task Groups

Task groups enable spawning multiple concurrent tasks with automatic lifecycle
management and result collection.

```swift
// Basic task group
func fetchMultipleUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}

// Non-throwing task group
func loadImages(urls: [URL]) async -> [Image] {
    await withTaskGroup(of: Image?.self) { group in
        for url in urls {
            group.addTask {
                try? await downloadImage(from: url)
            }
        }

        var images: [Image] = []
        for await image in group {
            if let image = image {
                images.append(image)
            }
        }
        return images
    }
}

func downloadImage(from url: URL) async throws -> Image {
    let (data, _) = try await URLSession.shared.data(from: url)
    guard let image = Image(data: data) else {
        throw ImageError.invalidData
    }
    return image
}

// Limited concurrency with task groups
func processItems<T>(
    _ items: [T],
    maxConcurrent: Int,
    process: @escaping (T) async throws -> Void
) async throws {
    try await withThrowingTaskGroup(of: Void.self) { group in
        var index = 0

        // Start initial batch
        for _ in 0..<min(maxConcurrent, items.count) {
            let item = items[index]
            group.addTask {
                try await process(item)
            }
            index += 1
        }

        // Process remaining items
        while index < items.count {
            try await group.next()
            let item = items[index]
            group.addTask {
                try await process(item)
            }
            index += 1
        }

        // Wait for remaining tasks
        try await group.waitForAll()
    }
}

// Task group with results dictionary
func fetchUserData(userIds: [Int]) async throws -> [Int: UserData] {
    try await withThrowingTaskGroup(
        of: (Int, UserData).self
    ) { group in
        for id in userIds {
            group.addTask {
                let data = try await loadUserData(id: id)
                return (id, data)
            }
        }

        var results: [Int: UserData] = [:]
        for try await (id, data) in group {
            results[id] = data
        }
        return results
    }
}

struct UserData {}

func loadUserData(id: Int) async throws -> UserData {
    return UserData()
}

// Early termination
func findFirstMatch(items: [String]) async -> String? {
    await withTaskGroup(of: String?.self) { group in
        for item in items {
            group.addTask {
                await checkMatch(item)
            }
        }

        for await result in group {
            if let match = result {
                group.cancelAll()
                return match
            }
        }
        return nil
    }
}

func checkMatch(_ item: String) async -> String? {
    // Simulate async work
    return item.count > 5 ? item : nil
}
```

Task groups provide structured concurrency: all child tasks complete or are
cancelled before the group exits, preventing task leaks.

## Task Management and Cancellation

Tasks represent units of asynchronous work with lifecycle management,
cancellation support, and priority configuration.

```swift
// Creating detached tasks
func backgroundUpdate() {
    Task.detached(priority: .background) {
        await performHeavyComputation()
    }
}

func performHeavyComputation() async {
    // Heavy work
}

// Storing and cancelling tasks
class DataLoader {
    private var loadTask: Task<Data, Error>?

    func startLoading() {
        loadTask = Task {
            try await loadData()
        }
    }

    func cancelLoading() {
        loadTask?.cancel()
        loadTask = nil
    }

    func loadData() async throws -> Data {
        let url = URL(string: "https://api.example.com/data")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}

// Checking for cancellation
func processLargeDataset(items: [Item]) async throws {
    for item in items {
        try Task.checkCancellation()
        await process(item)
    }
}

struct Item {}

func process(_ item: Item) async {
    // Process item
}

// Cooperative cancellation
func downloadWithProgress(url: URL) async throws -> Data {
    let (bytes, response) = try await URLSession.shared.bytes(from: url)

    var data = Data()
    for try await byte in bytes {
        if Task.isCancelled {
            throw CancellationError()
        }
        data.append(byte)
    }

    return data
}

// Task priorities
enum TaskPriority {
    case high, medium, low

    var priority: TaskPriority {
        switch self {
        case .high: return .high
        case .medium: return .medium
        case .low: return .low
        }
    }
}

func scheduleTask(priority: TaskPriority, work: @escaping () async -> Void) {
    Task(priority: priority.priority) {
        await work()
    }
}

// Task values and results
func loadUserAsync() async throws -> User {
    let task = Task<User, Error> {
        try await fetchUser(id: 1)
    }

    return try await task.value
}

// Unstructured tasks with context
@MainActor
class ViewController {
    func loadData() {
        Task { @MainActor in
            let data = try await fetchData()
            updateUI(with: data)
        }
    }

    func fetchData() async throws -> Data {
        return Data()
    }

    func updateUI(with data: Data) {
        // Update UI
    }
}
```

Tasks automatically inherit priority, task-local values, and actor context from
their creation site, ensuring proper execution environment.

## Async Sequences

Async sequences provide asynchronous iteration over values that arrive over
time, enabling clean handling of streams, events, and paginated data.

```swift
// Basic async sequence
struct AsyncCountdown: AsyncSequence {
    typealias Element = Int

    let start: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var current: Int

        mutating func next() async -> Int? {
            guard current >= 0 else { return nil }
            let value = current
            current -= 1
            try? await Task.sleep(nanoseconds: 1_000_000_000)
            return value
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        return AsyncIterator(current: start)
    }
}

// Using async sequences
func countDown() async {
    let countdown = AsyncCountdown(start: 5)
    for await number in countdown {
        print(number)
    }
}

// Async sequence operations
func processStream(urls: [URL]) async throws {
    let (bytes, _) = try await URLSession.shared.bytes(
        from: urls[0]
    )

    for try await byte in bytes {
        processByte(byte)
    }
}

func processByte(_ byte: UInt8) {
    // Process byte
}

// AsyncStream for custom sequences
func temperatures() -> AsyncStream<Double> {
    AsyncStream { continuation in
        let sensor = TemperatureSensor()
        sensor.onReading = { temperature in
            continuation.yield(temperature)
        }

        continuation.onTermination = { _ in
            sensor.stop()
        }

        sensor.start()
    }
}

class TemperatureSensor {
    var onReading: ((Double) -> Void)?

    func start() {}
    func stop() {}
}

// Using AsyncStream
func monitorTemperature() async {
    for await temp in temperatures() {
        print("Temperature: \(temp)°C")
        if temp > 100 {
            break
        }
    }
}

// Transforming async sequences
func filteredTemperatures() async {
    let temps = temperatures()
    for await temp in temps where temp > 0 {
        print("Positive temperature: \(temp)")
    }
}

// AsyncThrowingStream for errors
func networkEvents() -> AsyncThrowingStream<NetworkEvent, Error> {
    AsyncThrowingStream { continuation in
        let monitor = NetworkMonitor()

        monitor.onEvent = { event in
            continuation.yield(event)
        }

        monitor.onError = { error in
            continuation.finish(throwing: error)
        }

        monitor.start()
    }
}

struct NetworkEvent {}

class NetworkMonitor {
    var onEvent: ((NetworkEvent) -> Void)?
    var onError: ((Error) -> Void)?

    func start() {}
}
```

Async sequences integrate with for-await-in loops and support transformation,
filtering, and composition like synchronous sequences.

## Best Practices

1. **Use async/await instead of completion handlers** to improve readability and
   avoid callback pyramids in new code

2. **Protect mutable state with actors** rather than manual locks to prevent
   data races with compile-time guarantees

3. **Prefer structured concurrency** with task groups over detached tasks to
   ensure proper lifecycle management and cancellation

4. **Check Task.isCancelled in long-running operations** to enable cooperative
   cancellation and resource cleanup

5. **Use MainActor for UI code** to ensure UI updates happen on the main thread
   without explicit dispatch calls

6. **Leverage async let for parallel execution** when multiple independent async
   operations can run concurrently

7. **Employ async sequences for streams** instead of callbacks or delegates when
   handling values that arrive over time

8. **Mark nonisolated methods appropriately** on actors when they don't access
   isolated state to avoid unnecessary awaits

9. **Set task priorities explicitly** for background work to prevent priority
   inversion and ensure responsive UI

10. **Use withTaskCancellationHandler** to clean up resources immediately when
    tasks are cancelled rather than waiting for checkpoints

## Common Pitfalls

1. **Blocking main thread with await** in synchronous contexts causes hangs;
   create Task wrappers to bridge to async code

2. **Not checking for cancellation** in long operations wastes resources and
   delays response to user actions

3. **Creating retain cycles with unowned/weak** incorrectly in async closures
   can cause crashes or memory leaks

4. **Mixing async/await with completion handlers** improperly creates race
   conditions and difficult-to-debug behavior

5. **Overusing detached tasks** loses structured concurrency benefits like
   automatic cancellation and priority inheritance

6. **Forgetting await on actor methods** causes compilation errors since actor
   isolation requires suspension points

7. **Not using throwing variants** of task APIs when errors are possible leads
   to silent failures and unhandled errors

8. **Accessing actor state without isolation** by making properties public
   defeats the purpose of actor protection

9. **Creating too many concurrent tasks** without limits exhausts system
   resources and degrades performance

10. **Assuming immediate execution** after await; other tasks may run before
    continuation, breaking assumptions about state

## When to Use This Skill

Use Swift concurrency when building iOS 15+, macOS 12+, watchOS 8+, or tvOS 15+
applications that perform asynchronous operations like networking, file I/O, or
background processing.

Apply async/await when working with URLSession, Core Data async methods, or any
API that supports modern concurrency instead of completion handlers.

Employ actors when managing shared mutable state accessed from multiple
concurrent contexts, especially in data managers, caches, or repositories.

Leverage task groups when performing multiple independent async operations that
should be coordinated, like fetching data for multiple users or processing a
batch of items concurrently.

Use async sequences when handling streams of data from sensors, network
connections, file reading, or any source that produces values over time.

## Resources

- [Swift Concurrency Documentation](<https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/>)
- [Meet async/await WWDC Session](<https://developer.apple.com/videos/play/wwdc2021/10132/>)
- [Protect Mutable State with Swift Actors](<https://developer.apple.com/videos/play/wwdc2021/10133/>)
- [Swift Evolution - Concurrency Proposals](<https://github.com/apple/swift-evolution/blob/main/proposals/0296-async-await.md>)
- [Swift Concurrency Roadmap](<https://forums.swift.org/t/swift-concurrency-roadmap/41611>)
