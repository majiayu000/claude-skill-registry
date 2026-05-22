---
name: mvvm-architecture
description: "Expert MVVM decisions for iOS/tvOS: choosing between ViewModel patterns (state enum vs published properties vs Combine), service layer boundaries, dependency injection strategies, and testing approaches. Use when designing ViewModel architecture, debugging data flow issues, or deciding where business logic belongs. Trigger keywords: MVVM, ViewModel, ObservableObject, @StateObject, service layer, dependency injection, unit test, mock, architecture"
version: "3.0.0"
---

# MVVM Architecture — Expert Decisions

Expert decision frameworks for MVVM choices in iOS/tvOS. Claude knows MVVM basics — this skill provides judgment calls for non-obvious decisions.

---

## Decision Trees

### ViewModel Pattern Selection

```
Does the screen have distinct, mutually exclusive states?
├─ YES (loading → loaded → error)
│  └─ State Enum Pattern
│     @Published var state: State = .idle
│     enum State { case idle, loading, loaded(Data), error(String) }
│
└─ NO (multiple independent properties)
   └─ Does the screen need form validation?
      ├─ YES → Combine Pattern (publishers for validation chains)
      └─ NO → Published Properties Pattern (simplest)
```

**When State Enum wins**: Product detail (loading → product → error), authentication flows, wizard steps. Forces exhaustive handling.

**When Published Properties win**: Dashboard with multiple independent sections that load/fail independently. State enum becomes unwieldy with 2^n combinations.

### Where Does Logic Belong?

```
Is it data transformation for display?
├─ YES → ViewModel (formatting, filtering visible data)
│
└─ NO → Is it reusable business logic?
   ├─ YES → Service Layer (API calls, validation rules, caching)
   │
   └─ NO → Is it pure domain logic?
      ├─ YES → Model (computed properties, domain rules)
      └─ NO → Reconsider if it's needed
```

**The trap**: Putting API calls directly in ViewModel. Makes testing require network mocking instead of simple service mocking.

### @StateObject Injection

```
Does ViewModel need dependencies from parent?
├─ NO → Direct initialization
│  @StateObject private var viewModel = UserViewModel()
│
└─ YES → How many dependencies?
   ├─ 1-2 → Init parameter
   │  init(userId: String) {
   │      _viewModel = StateObject(wrappedValue: UserViewModel(userId: userId))
   │  }
   │
   └─ Many → Factory/Container
      @StateObject private var viewModel: UserViewModel
      init() {
          _viewModel = StateObject(wrappedValue: Container.shared.makeUserViewModel())
      }
```

---

## NEVER Do

### ViewModel Anti-Patterns

**NEVER** load data in ViewModel `init`:
```swift
// ❌ Starts loading before view appears, can't cancel, can't retry
class BadViewModel: ObservableObject {
    init() {
        Task { await loadData() }  // Fire-and-forget in init
    }
}

// ✅ Load via .task modifier — automatic cancellation on disappear
struct GoodView: View {
    @StateObject var viewModel = GoodViewModel()
    var body: some View {
        content.task { await viewModel.loadData() }
    }
}
```

**NEVER** expose mutable state directly:
```swift
// ❌ Anyone can mutate — no control over state transitions
class BadViewModel: ObservableObject {
    @Published var users: [User] = []  // Public setter
}

// ✅ private(set) — only ViewModel controls mutations
class GoodViewModel: ObservableObject {
    @Published private(set) var users: [User] = []

    func addUser(_ user: User) {
        // Validation, analytics, etc.
        users.append(user)
    }
}
```

**NEVER** put UI-specific code in ViewModel:
```swift
// ❌ ViewModel knows about colors, fonts, formatters
class BadViewModel: ObservableObject {
    @Published var priceColor: Color = .green
    @Published var formattedDate: String = ""  // Pre-formatted for display
}

// ✅ Return data, let View handle presentation
class GoodViewModel: ObservableObject {
    @Published private(set) var price: Decimal = 0
    @Published private(set) var date: Date = .now
}
// View: Text(viewModel.price, format: .currency(code: "USD"))
```

**NEVER** create god ViewModels:
```swift
// ❌ One ViewModel for entire feature area
class UserViewModel: ObservableObject {
    // Profile, settings, posts, friends, notifications, activity...
    // 50+ @Published properties, 30+ methods
}

// ✅ One ViewModel per screen/concern
class UserProfileViewModel: ObservableObject { }
class UserSettingsViewModel: ObservableObject { }
class UserPostsViewModel: ObservableObject { }
```

### Service Layer Anti-Patterns

**NEVER** use concrete dependencies:
```swift
// ❌ Hard to test — must mock URLSession
class BadViewModel: ObservableObject {
    func loadUsers() async {
        let url = URL(string: "https://api.example.com/users")!
        let (data, _) = try await URLSession.shared.data(from: url)  // Concrete
    }
}

// ✅ Protocol dependency — inject mock for testing
protocol UserServiceProtocol {
    func fetchUsers() async throws -> [User]
}

class GoodViewModel: ObservableObject {
    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }
}
```

**NEVER** ignore task cancellation:
```swift
// ❌ Shows error for cancelled task (user navigated away)
func loadData() async {
    do {
        users = try await service.fetchUsers()
    } catch {
        errorMessage = error.localizedDescription  // CancellationError shows error!
    }
}

// ✅ Handle cancellation separately
func loadData() async {
    do {
        users = try await service.fetchUsers()
    } catch is CancellationError {
        return  // User navigated away — don't show error
    } catch {
        errorMessage = error.localizedDescription
    }
}
```

---

## Core Patterns

### Minimal ViewModel Template

```swift
@MainActor
final class FeatureViewModel: ObservableObject {
    // MARK: - State
    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false
    @Published var error: Error?

    // MARK: - Dependencies
    private let service: ServiceProtocol

    init(service: ServiceProtocol = Service()) {
        self.service = service
    }

    // MARK: - Actions
    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await service.fetchItems()
        } catch is CancellationError {
            return
        } catch {
            self.error = error
        }
    }
}
```

### State Enum Pattern

```swift
@MainActor
final class DetailViewModel: ObservableObject {
    enum State: Equatable {
        case idle
        case loading
        case loaded(Item)
        case error(String)

        var item: Item? {
            guard case .loaded(let item) = self else { return nil }
            return item
        }
    }

    @Published private(set) var state: State = .idle

    func load(id: String) async {
        state = .loading
        do {
            let item = try await service.fetch(id: id)
            state = .loaded(item)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}

// View exhaustive handling
switch viewModel.state {
case .idle, .loading: ProgressView()
case .loaded(let item): ItemView(item: item)
case .error(let message): ErrorView(message: message)
}
```

### Service Protocol Pattern

```swift
// Protocol — the contract
protocol UserServiceProtocol {
    func fetchUser(id: String) async throws -> User
    func updateUser(_ user: User) async throws -> User
}

// Real implementation
final class UserService: UserServiceProtocol {
    private let client: NetworkClient

    func fetchUser(id: String) async throws -> User {
        try await client.request(.user(id: id))
    }
}

// Mock for testing
final class MockUserService: UserServiceProtocol {
    var stubbedUser: User?
    var fetchError: Error?
    var fetchCallCount = 0

    func fetchUser(id: String) async throws -> User {
        fetchCallCount += 1
        if let error = fetchError { throw error }
        return stubbedUser ?? User.mock()
    }
}
```

---

## Testing Strategy

### ViewModel Test Structure

```swift
@MainActor
final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        mockService = MockUserService()
        sut = UserViewModel(service: mockService)
    }

    func test_loadUser_success_updatesState() async {
        // Given
        mockService.stubbedUser = User.mock(name: "John")

        // When
        await sut.loadUser(id: "123")

        // Then
        XCTAssertEqual(sut.user?.name, "John")
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }

    func test_loadUser_failure_setsError() async {
        // Given
        mockService.fetchError = NetworkError.noConnection

        // When
        await sut.loadUser(id: "123")

        // Then
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.error)
    }
}
```

**Test what matters**:
1. State changes on success/failure
2. Service method called with correct parameters
3. Loading states transition correctly
4. Error handling doesn't crash

**Don't test**:
- SwiftUI bindings (Apple's responsibility)
- Service implementation (separate test file)

---

## Dependency Injection

### Simple: Default Parameters

```swift
// Most apps need nothing more complex
class UserViewModel: ObservableObject {
    init(service: UserServiceProtocol = UserService()) {
        self.service = service
    }
}

// Test: UserViewModel(service: MockUserService())
// Production: UserViewModel() — uses default
```

### Complex: Factory Container

```swift
// Only when you have many cross-cutting dependencies
@MainActor
final class Container {
    static let shared = Container()

    lazy var networkClient = NetworkClient()
    lazy var authService = AuthService(client: networkClient)
    lazy var userService = UserService(client: networkClient, auth: authService)

    func makeUserViewModel() -> UserViewModel {
        UserViewModel(service: userService)
    }
}
```

---

## Quick Reference

### Layer Responsibilities

| Layer | Contains | Examples |
|-------|----------|----------|
| **Model** | Domain data + pure logic | User, Order, validation rules |
| **ViewModel** | Screen state + UI logic | Loading/error states, list filtering |
| **Service** | Business operations | API calls, caching, persistence |
| **View** | Presentation | Layout, styling, animations |

### ViewModel Checklist

- [ ] `@MainActor` on class
- [ ] `private(set)` on @Published properties
- [ ] Protocol-based dependencies with defaults
- [ ] CancellationError handled separately
- [ ] No UI types (Color, Font, etc.)
- [ ] No direct network/database calls
- [ ] Testable without UI framework
