---
name: solid
description: SOLID 원칙 기반 iOS 객체지향 설계. 의존성 관리, 확장성, 유지보수성을 위한 5가지 핵심 원칙 적용. Use when designing class hierarchies, applying design patterns, reviewing object-oriented code structure, or applying SOLID principles during architecture design and refactoring.
---

# SOLID 원칙 - iOS 객체지향 설계 가이드

SOLID 원칙을 적용하여 유지보수 가능하고 확장 가능한 iOS 코드를 작성한다.
의존성 관리, 책임 분리, 확장성을 고려한 설계를 지원한다.

## 상세 원칙 참조

각 원칙의 상세 내용, iOS 예제, 안티패턴, 리팩토링 방법은 references 디렉토리를 참고한다:

| 원칙 | 참조 파일 | 핵심 |
|------|-----------|------|
| SRP | `references/srp.md` | 모듈은 하나의 Actor에게만 책임 |
| OCP | `references/ocp.md` | 확장에 열리고 수정에 닫힘 |
| LSP | `references/lsp.md` | 하위 타입은 상위 타입 대체 가능 |
| ISP | `references/isp.md` | 사용하지 않는 인터페이스에 의존 금지 |
| DIP | `references/dip.md` | 고수준이 저수준에 의존하지 않음 |

## 객체지향의 본질

핵심은 의존성 역전(Dependency Inversion)이다.
- Runtime 흐름: 고수준 → 저수준
- Source Code 의존성: 저수준 → 고수준 (역전!)
- 고수준 정책을 저수준 세부사항으로부터 보호한다.

## 적용 워크플로우

### 1단계: 설계 전 체크리스트

```
□ Actor를 식별했는가? (SRP)
□ 변경 가능한 지점을 파악했는가? (OCP)
□ 추상화가 필요한 곳을 찾았는가? (DIP)
□ 인터페이스가 비대한가? (ISP)
□ 상속 관계가 적절한가? (LSP)
```

### 2단계: 코드 작성 중 체크리스트

```
□ 클래스가 여러 Actor를 섬기고 있는가? (SRP 위반)
□ 새 기능 추가 시 기존 코드를 수정하는가? (OCP 위반)
□ protocol에 구체 클래스를 직접 의존하는가? (DIP 위반)
□ protocol에 사용하지 않는 메서드가 있는가? (ISP 위반)
□ 하위 타입이 상위 타입의 계약을 위반하는가? (LSP 위반)
```

### 3단계: 리팩토링 우선순위

```
우선순위 1: DIP 위반 → protocol 도입으로 의존성 역전
우선순위 2: SRP 위반 → Actor별로 책임 분리
우선순위 3: OCP 위반 → protocol + 구현체로 확장
우선순위 4: ISP 위반 → protocol 분리
우선순위 5: LSP 위반 → 상속 대신 composition 고려
```

## iOS에서 SOLID 적용 요약

### Repository 패턴 (DIP + SRP + OCP)

```swift
// DIP: 추상화에 의존
protocol UserRepository {
    func fetchUser(id: String) async throws -> User
    func saveUser(_ user: User) async throws
}

// SRP: 네트워크 데이터 소스는 네트워크만 책임
class NetworkUserRepository: UserRepository {
    private let apiClient: APIClient
    
    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }
    
    func fetchUser(id: String) async throws -> User {
        try await apiClient.request(.getUser(id))
    }
    
    func saveUser(_ user: User) async throws {
        try await apiClient.request(.updateUser(user))
    }
}

// OCP: 새로운 저장소 추가 시 기존 코드 수정 불필요
class CachedUserRepository: UserRepository {
    private let cache: Cache
    
    func fetchUser(id: String) async throws -> User {
        try cache.get(id)
    }
    
    func saveUser(_ user: User) async throws {
        try cache.set(user, key: user.id)
    }
}

// UseCase는 추상화에만 의존 (DIP)
class FetchUserUseCase {
    private let repository: UserRepository
    
    init(repository: UserRepository) {
        self.repository = repository
    }
    
    func execute(id: String) async throws -> User {
        try await repository.fetchUser(id: id)
    }
}
```

## 안티패턴 감지

### Massive View Controller (SRP + DIP 위반)

```swift
// ❌ 나쁜 예
class ProductListViewController: UIViewController {
    func fetchProducts() {
        URLSession.shared.dataTask(with: url) { data, _, _ in
            // JSON 파싱, 할인 계산, UI 업데이트 모두 여기서
        }
    }
}

// ✅ 좋은 예
class ProductListViewController: UIViewController {
    private let viewModel: ProductListViewModel
    // UI만 담당
}
```

### 구체 클래스 직접 의존 (DIP 위반)

```swift
// ❌ 나쁜 예
class OrderService {
    let database = MySQLDatabase()
}

// ✅ 좋은 예
class OrderService {
    private let repository: OrderRepository // protocol 의존
    
    init(repository: OrderRepository) {
        self.repository = repository
    }
}
```

### Fat Interface (ISP 위반)

```swift
// ❌ 나쁜 예
protocol DataSource {
    func fetch() -> [Item]
    func save(_ item: Item)
    func delete(_ item: Item)
    func search(_ query: String) -> [Item]
}

// ✅ 좋은 예
protocol Fetchable { func fetch() -> [Item] }
protocol Savable { func save(_ item: Item) }
protocol Deletable { func delete(_ item: Item) }
protocol Searchable { func search(_ query: String) -> [Item] }
```

## 실전 팁

1. DIP부터 시작: 의존성 방향이 가장 중요
2. Actor 찾기: SRP 적용의 시작점
3. protocol 먼저: Swift는 protocol-oriented
4. 점진적 적용: 한 번에 모두 적용하려 하지 말 것
5. 테스트로 검증: SOLID 준수 여부는 테스트 용이성으로 확인
