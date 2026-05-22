---
name: clean-architecture-ios
description: "Expert Clean Architecture decisions for iOS/tvOS: when Clean Architecture adds value vs overkill, layer boundary judgment calls, dependency rule violations to catch, and practical trade-offs between purity and pragmatism. Use when designing app architecture, debugging layer violations, or deciding what belongs where. Trigger keywords: Clean Architecture, layer, domain, data, presentation, use case, repository, dependency rule, entity, DTO, mapper"
version: "3.0.0"
---

# Clean Architecture iOS — Expert Decisions

Expert decision frameworks for Clean Architecture choices. Claude knows the layers — this skill provides judgment calls for boundary decisions and pragmatic trade-offs.

---

## Decision Trees

### When Clean Architecture Is Worth It

```
Is this a side project or prototype?
├─ YES → Skip Clean Architecture (YAGNI)
│  └─ Simple MVVM with services is fine
│
└─ NO → How many data sources?
   ├─ 1 (just API) → Lightweight Clean Architecture
   │  └─ Skip local data source, repository = API wrapper
   │
   └─ Multiple (API + cache + local DB)
      └─ How long will codebase live?
         ├─ < 1 year → Consider simpler approach
         └─ > 1 year → Full Clean Architecture
            └─ Team size > 2? → Strongly recommended
```

**Clean Architecture wins**: Apps with complex business logic, multiple data sources, long maintenance lifetime, or teams > 3 developers.

**Clean Architecture is overkill**: Prototypes, simple apps with single API, short-lived projects, solo developers who know the whole codebase.

### Where Does This Code Belong?

```
Does it know about UIKit/SwiftUI?
├─ YES → Presentation Layer
│  └─ Views, ViewModels, Coordinators
│
└─ NO → Does it know about network/database specifics?
   ├─ YES → Data Layer
   │  └─ Repositories (impl), DataSources, DTOs, Mappers
   │
   └─ NO → Is it a business rule or core model?
      ├─ YES → Domain Layer
      │  └─ Entities, UseCases, Repository protocols
      │
      └─ NO → Reconsider if it's needed
```

### UseCase Granularity

```
Is this operation a single business action?
├─ YES → One UseCase per operation
│  Example: CreateOrderUseCase, GetUserUseCase
│
└─ NO → Does it combine multiple actions?
   ├─ YES → Can actions be reused independently?
   │  ├─ YES → Separate UseCases, compose in ViewModel
   │  └─ NO → Single UseCase with clear naming
   │
   └─ NO → Is it just CRUD?
      ├─ YES → Consider skipping UseCase
      │  └─ ViewModel → Repository directly is OK for simple CRUD
      │
      └─ NO → Review the operation's purpose
```

**The trap**: Creating UseCases for every operation. If it's just `repository.get(id:)` pass-through, skip the UseCase.

---

## NEVER Do

### Dependency Rule Violations

**NEVER** import outer layers in inner layers:
```swift
// ❌ Domain importing Data layer
// Domain/UseCases/GetUserUseCase.swift
import Alamofire  // Data layer framework!
import CoreData   // Data layer framework!

// ❌ Domain importing Presentation layer
import SwiftUI    // Presentation framework!

// ✅ Domain has NO framework imports (except Foundation)
import Foundation
```

**NEVER** let Domain know about DTOs:
```swift
// ❌ Repository protocol returns DTO
protocol UserRepositoryProtocol {
    func getUser(id: String) async throws -> UserDTO  // Data layer type!
}

// ✅ Repository protocol returns Entity
protocol UserRepositoryProtocol {
    func getUser(id: String) async throws -> User  // Domain type
}
```

**NEVER** put business logic in Repository:
```swift
// ❌ Business validation in Repository
final class UserRepository: UserRepositoryProtocol {
    func updateUser(_ user: User) async throws -> User {
        // Business rule leaked into Data layer!
        guard user.email.contains("@") else {
            throw ValidationError.invalidEmail
        }
        return try await remoteDataSource.update(user)
    }
}

// ✅ Business logic in UseCase
final class UpdateUserUseCase {
    func execute(user: User) async throws -> User {
        guard user.email.contains("@") else {
            throw DomainError.validation("Invalid email")
        }
        return try await repository.updateUser(user)
    }
}
```

### Entity Anti-Patterns

**NEVER** add framework dependencies to Entities:
```swift
// ❌ Entity with Codable for JSON
struct User: Codable {  // Codable couples to serialization format
    let id: String
    let createdAt: Date  // Will have JSON parsing issues
}

// ✅ Pure Entity, DTOs handle serialization
struct User: Identifiable, Equatable {
    let id: String
    let createdAt: Date
}

// Data layer handles Codable
struct UserDTO: Codable {
    let id: String
    let created_at: String  // API format
}
```

**NEVER** put computed properties that need external data in Entities:
```swift
// ❌ Entity needs external service
struct Order {
    let items: [OrderItem]

    var totalWithTax: Decimal {
        // Where does tax rate come from? External dependency!
        total * TaxService.currentRate
    }
}

// ✅ Calculation in UseCase
final class CalculateOrderTotalUseCase {
    private let taxService: TaxServiceProtocol

    func execute(order: Order) -> Decimal {
        order.total * taxService.currentRate
    }
}
```

### Mapper Anti-Patterns

**NEVER** put Mappers in Domain layer:
```swift
// ❌ Domain knows about mapping
// Domain/Mappers/UserMapper.swift  — WRONG LOCATION!

// ✅ Mappers live in Data layer
// Data/Mappers/UserMapper.swift
```

**NEVER** map in Repository if domain logic is needed:
```swift
// ❌ Silent default in mapper
enum ProductMapper {
    static func toDomain(_ dto: ProductDTO) -> Product {
        Product(
            currency: Product.Currency(rawValue: dto.currency) ?? .usd  // Silent default!
        )
    }
}

// ✅ Throw on invalid data, let UseCase handle
enum ProductMapper {
    static func toDomain(_ dto: ProductDTO) throws -> Product {
        guard let currency = Product.Currency(rawValue: dto.currency) else {
            throw MappingError.invalidCurrency(dto.currency)
        }
        return Product(currency: currency)
    }
}
```

---

## Pragmatic Patterns

### When to Skip the UseCase

```swift
// ✅ Simple CRUD — ViewModel → Repository is fine
@MainActor
final class UserListViewModel: ObservableObject {
    private let repository: UserRepositoryProtocol

    func loadUsers() async {
        // Direct repository call for simple fetch
        users = try? await repository.getUsers()
    }
}

// ✅ UseCase needed — business logic involved
final class PlaceOrderUseCase {
    func execute(cart: Cart) async throws -> Order {
        // Validate stock
        // Calculate totals
        // Apply discounts
        // Create order
        // Notify inventory
        // Return order
    }
}
```

**Rule**: No business logic? Skip UseCase. Any validation, transformation, or orchestration? Create UseCase.

### Repository Caching Strategy

```swift
final class UserRepository: UserRepositoryProtocol {
    func getUser(id: String) async throws -> User {
        // Strategy 1: Cache-first (offline-capable)
        if let cached = try? await localDataSource.getUser(id: id) {
            // Return cached, refresh in background
            Task { try? await refreshUser(id: id) }
            return UserMapper.toDomain(cached)
        }

        // Strategy 2: Network-first (always fresh)
        let dto = try await remoteDataSource.fetchUser(id: id)
        try? await localDataSource.save(dto)  // Cache for offline
        return UserMapper.toDomain(dto)
    }
}
```

### Minimal DI Container

```swift
// For small-medium apps, simple factory is enough
@MainActor
final class Container {
    static let shared = Container()

    // Lazy initialization — created on first use
    lazy var networkClient = NetworkClient()
    lazy var userRepository: UserRepositoryProtocol = UserRepository(
        remote: UserRemoteDataSource(client: networkClient),
        local: UserLocalDataSource()
    )

    // Factory methods for UseCases
    func makeGetUserUseCase() -> GetUserUseCaseProtocol {
        GetUserUseCase(repository: userRepository)
    }

    // Factory methods for ViewModels
    func makeUserProfileViewModel() -> UserProfileViewModel {
        UserProfileViewModel(getUser: makeGetUserUseCase())
    }
}
```

---

## Layer Reference

### Dependency Direction

```
Presentation → Domain ← Data

✅ Presentation depends on Domain (imports UseCases, Entities)
✅ Data depends on Domain (implements Repository protocols)
❌ Domain depends on nothing (no imports from other layers)
```

### What Goes Where

| Layer | Contains | Does NOT Contain |
|-------|----------|------------------|
| **Domain** | Entities, UseCases, Repository protocols, Domain errors | UIKit, SwiftUI, Codable DTOs, Network code |
| **Data** | Repository impl, DataSources, DTOs, Mappers, Network | UI code, Business rules, UseCases |
| **Presentation** | Views, ViewModels, Coordinators, UI components | Network code, Database code, DTOs |

### Protocol Placement

| Protocol | Lives In | Implemented By |
|----------|----------|----------------|
| `UserRepositoryProtocol` | Domain | Data (UserRepository) |
| `UserRemoteDataSourceProtocol` | Data | Data (UserRemoteDataSource) |
| `GetUserUseCaseProtocol` | Domain | Domain (GetUserUseCase) |

---

## Testing Strategy

### What to Test Where

| Layer | Test Focus | Mock |
|-------|------------|------|
| **Domain (UseCases)** | Business logic, validation, orchestration | Repository protocols |
| **Data (Repositories)** | Coordination, caching, error mapping | DataSource protocols |
| **Presentation (ViewModels)** | State changes, user actions | UseCase protocols |

```swift
// UseCase test — mock Repository
func test_createOrder_validatesStock() async throws {
    mockProductRepo.stubbedProduct = Product(inStock: false)

    await XCTAssertThrowsError(
        try await sut.execute(items: [item])
    ) { error in
        XCTAssertEqual(error as? DomainError, .businessRule("Out of stock"))
    }
}

// ViewModel test — mock UseCase
func test_loadUser_updatesState() async {
    mockGetUserUseCase.stubbedUser = User(name: "John")

    await sut.loadUser(id: "123")

    XCTAssertEqual(sut.user?.name, "John")
    XCTAssertFalse(sut.isLoading)
}
```

---

## Quick Reference

### Clean Architecture Checklist

- [ ] Domain layer has zero framework imports (except Foundation)
- [ ] Entities are pure structs with no Codable
- [ ] Repository protocols live in Domain
- [ ] Repository implementations live in Data
- [ ] DTOs and Mappers live in Data
- [ ] UseCases contain business logic, not pass-through
- [ ] ViewModels depend on UseCase protocols, not concrete classes
- [ ] No circular dependencies between layers

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| `import UIKit` in Domain | Layer violation | Move to Presentation |
| UseCase just calls `repo.get()` | Unnecessary abstraction | ViewModel → Repo directly |
| DTO in Domain | Layer violation | Keep DTOs in Data |
| Business logic in Repository | Wrong layer | Move to UseCase |
| ViewModel imports NetworkClient | Skipped layers | Use Repository |
