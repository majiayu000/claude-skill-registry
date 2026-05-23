---
name: swift-performance
description: Optimize SwiftUI and Swift app performance with Instruments profiling, lazy loading, memory management, and view optimization. Use when diagnosing slow UI, fixing memory leaks, optimizing scroll performance, or reducing app launch time.
user-invocable: false
---

# Swift Performance Optimization

## SwiftUI View Optimization

```swift
// ❌ BAD - Recreates formatter every render
struct BadView: View {
    var body: some View {
        Text(Date(), formatter: DateFormatter()) // New instance each time!
    }
}

// ✅ GOOD - Cached formatter
struct GoodView: View {
    private static let formatter: DateFormatter = {
        let f = DateFormatter()
        f.dateStyle = .medium
        return f
    }()

    var body: some View {
        Text(Date(), formatter: Self.formatter)
    }
}

// ✅ Use Equatable to prevent unnecessary updates
struct ItemView: View, Equatable {
    let item: Item

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.item.id == rhs.item.id
    }

    var body: some View {
        Text(item.name)
    }
}
```

## Lazy Loading

```swift
// ✅ LazyVStack for long lists
ScrollView {
    LazyVStack(spacing: 16) {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// ✅ LazyView wrapper for heavy views
struct LazyView<Content: View>: View {
    let build: () -> Content

    init(_ build: @autoclosure @escaping () -> Content) {
        self.build = build
    }

    var body: Content {
        build()
    }
}

// Usage - defers initialization
NavigationLink {
    LazyView(HeavyDetailView(item: item))
} label: {
    Text(item.name)
}
```

## Memory Management

```swift
// ✅ Avoid retain cycles with weak references
class ViewModel: ObservableObject {
    private var cancellables = Set<AnyCancellable>()

    func observe() {
        NotificationCenter.default
            .publisher(for: .someNotification)
            .sink { [weak self] _ in
                self?.handleNotification()
            }
            .store(in: &cancellables)
    }
}

// ✅ Use value types when possible
struct User: Sendable {  // Struct, not class
    let id: UUID
    let name: String
}

// ✅ Image caching
actor ImageCache {
    private var cache = NSCache<NSString, UIImage>()

    func image(for url: URL) async -> UIImage? {
        let key = url.absoluteString as NSString
        if let cached = cache.object(forKey: key) {
            return cached
        }
        guard let image = await downloadImage(url) else { return nil }
        cache.setObject(image, forKey: key)
        return image
    }
}
```

## Instruments Profiling

| Instrument | Detects |
|------------|---------|
| **Time Profiler** | Slow functions, CPU usage |
| **Allocations** | Memory growth, leaks |
| **Leaks** | Retain cycles |
| **SwiftUI** | View body updates, layout |
| **Core Animation** | Offscreen renders, blending |

## Common Performance Issues

```swift
// ❌ Heavy computation in body
var body: some View {
    let sorted = items.sorted() // Runs every render!
    List(sorted) { ... }
}

// ✅ Move to ViewModel or cache
@Observable class ViewModel {
    var items: [Item] = [] {
        didSet { sortedItems = items.sorted() }
    }
    private(set) var sortedItems: [Item] = []
}

// ❌ Unnecessary state invalidation
@State private var allItems: [Item] = []  // Changes invalidate entire view

// ✅ Use @Observable with granular properties
@Observable class ItemsStore {
    var displayedItems: [Item] = []  // Only this triggers updates
    var metadata: Metadata = .empty   // Independent updates
}
```

## Launch Time Optimization

```swift
// ✅ Defer non-essential work
@main
struct MyApp: App {
    init() {
        // Only critical initialization here
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .task {
                    // Defer analytics, caching, etc.
                    await DeferredSetup.run()
                }
        }
    }
}

// ✅ Use lazy initialization
class AppServices {
    static let shared = AppServices()
    lazy var analytics = AnalyticsService()  // Created on first use
    lazy var imageCache = ImageCache()
}
```
