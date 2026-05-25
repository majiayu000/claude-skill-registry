---
name: swift-patterns
description: SwiftUI view composition, @Observable patterns, async/await concurrency, TCA architecture, and Combine reactive streams.
---

# Swift Patterns

Modern Swift patterns for iOS/macOS application development.

## SwiftUI View Composition

```swift
// Small, focused views composed together
struct ProductCard: View {
    let product: Product

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            ProductImage(url: product.imageURL)
            ProductInfo(name: product.name, price: product.price)
            RatingStars(rating: product.rating, count: product.reviewCount)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// Extract subviews for readability and reusability
struct ProductImage: View {
    let url: URL

    var body: some View {
        AsyncImage(url: url) { phase in
            switch phase {
            case .success(let image):
                image.resizable().aspectRatio(contentMode: .fill)
            case .failure:
                Image(systemName: "photo").foregroundStyle(.secondary)
            case .empty:
                ProgressView()
            @unknown default:
                EmptyView()
            }
        }
        .frame(height: 200)
        .clipped()
    }
}

// ViewModifier for reusable styling
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}
```

## @Observable Pattern (iOS 17+)

```swift
import Observation

@Observable
final class ProductStore {
    var products: [Product] = []
    var isLoading = false
    var errorMessage: String?

    private let apiClient: APIClient

    init(apiClient: APIClient = .shared) {
        self.apiClient = apiClient
    }

    func loadProducts() async {
        isLoading = true
        errorMessage = nil

        do {
            products = try await apiClient.fetchProducts()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func deleteProduct(_ product: Product) async throws {
        try await apiClient.deleteProduct(id: product.id)
        products.removeAll { $0.id == product.id }
    }
}

// Usage in SwiftUI (automatic tracking, no @Published needed)
struct ProductListView: View {
    @State private var store = ProductStore()

    var body: some View {
        List(store.products) { product in
            ProductCard(product: product)
        }
        .overlay {
            if store.isLoading { ProgressView() }
            if let error = store.errorMessage {
                ContentUnavailableView("Error", systemImage: "exclamationmark.triangle",
                                       description: Text(error))
            }
        }
        .task { await store.loadProducts() }
    }
}
```

## Structured Concurrency

```swift
// TaskGroup for parallel async work
func loadDashboard() async throws -> Dashboard {
    async let profile = apiClient.fetchProfile()
    async let orders = apiClient.fetchRecentOrders()
    async let recommendations = apiClient.fetchRecommendations()

    // All three run concurrently, await all results
    return try await Dashboard(
        profile: profile,
        orders: orders,
        recommendations: recommendations
    )
}

// TaskGroup with dynamic number of tasks
func loadImages(urls: [URL]) async -> [URL: UIImage] {
    await withTaskGroup(of: (URL, UIImage?).self) { group in
        for url in urls {
            group.addTask {
                let image = try? await ImageLoader.load(url)
                return (url, image)
            }
        }

        var results: [URL: UIImage] = [:]
        for await (url, image) in group {
            if let image { results[url] = image }
        }
        return results
    }
}

// Actor for thread-safe shared state
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    private var inFlight: [URL: Task<UIImage, Error>] = [:]

    func image(for url: URL) async throws -> UIImage {
        if let cached = cache[url] { return cached }

        // Coalesce duplicate requests
        if let existing = inFlight[url] {
            return try await existing.value
        }

        let task = Task {
            let (data, _) = try await URLSession.shared.data(from: url)
            guard let image = UIImage(data: data) else {
                throw ImageError.invalidData
            }
            return image
        }

        inFlight[url] = task
        let image = try await task.value
        cache[url] = image
        inFlight[url] = nil
        return image
    }
}
```

## TCA (The Composable Architecture) Pattern

```swift
import ComposableArchitecture

@Reducer
struct ProductFeature {
    @ObservableState
    struct State: Equatable {
        var products: [Product] = []
        var isLoading = false
        var alert: AlertState<Action>?
    }

    enum Action {
        case onAppear
        case productsLoaded(Result<[Product], Error>)
        case deleteProduct(Product)
        case alertDismissed
    }

    @Dependency(\.apiClient) var apiClient

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .onAppear:
                state.isLoading = true
                return .run { send in
                    let result = await Result { try await apiClient.fetchProducts() }
                    await send(.productsLoaded(result))
                }

            case .productsLoaded(.success(let products)):
                state.isLoading = false
                state.products = products
                return .none

            case .productsLoaded(.failure(let error)):
                state.isLoading = false
                state.alert = AlertState { TextState(error.localizedDescription) }
                return .none

            case .deleteProduct(let product):
                state.products.removeAll { $0.id == product.id }
                return .run { _ in try await apiClient.deleteProduct(id: product.id) }

            case .alertDismissed:
                state.alert = nil
                return .none
            }
        }
    }
}
```

## Checklist

- [ ] Views under 50 lines; extract subviews for composition
- [ ] Use @Observable (iOS 17+) over ObservableObject/@Published
- [ ] Structured concurrency with async let for parallel work
- [ ] Actors for shared mutable state (not locks/queues)
- [ ] ViewModifiers for reusable styling patterns
- [ ] Environment for dependency injection in SwiftUI
- [ ] Task cancellation handled (check Task.isCancelled)
- [ ] Preview providers for every view with mock data

## Anti-Patterns

- Massive views: 200+ line body property (extract subviews)
- @StateObject in child views: use @State or pass as parameter
- Blocking main thread with synchronous work in views
- Force unwrapping optionals: use guard let or nil coalescing
- Ignoring task cancellation: leaked work after view disappears
- Using singletons instead of dependency injection (untestable)
