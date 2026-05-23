---
name: coordinator-pattern
description: "Expert Coordinator pattern decisions for iOS/tvOS: when coordinators add value vs overkill, parent-child coordinator hierarchy design, SwiftUI vs UIKit coordinator differences, and flow completion handling. Use when designing navigation architecture, implementing multi-step flows, or decoupling views from navigation. Trigger keywords: Coordinator, navigation, flow, parent coordinator, child coordinator, deep link, routing, navigation hierarchy, flow completion"
version: "3.0.0"
---

# Coordinator Pattern — Expert Decisions

Expert decision frameworks for Coordinator pattern choices. Claude knows the pattern — this skill provides judgment calls for when coordinators add value and how to structure hierarchies.

---

## Decision Trees

### Do You Need Coordinators?

```
How many navigation flows does your app have?
├─ 1-2 simple flows
│  └─ Skip coordinators
│     NavigationStack + simple Router is enough
│
├─ 3-5 distinct flows
│  └─ Consider coordinators IF:
│     • Flows have complex branching
│     • Deep linking is required
│     • Flows need to share navigation logic
│
└─ 6+ flows or multi-team development
   └─ Coordinators recommended
      • Clear ownership boundaries
      • Parallel development possible
      • Testable navigation logic
```

**The trap**: Adding coordinators to simple apps. If your app is 5 screens with linear flow, coordinators add complexity without benefit.

### Coordinator Hierarchy Design

```
Does this flow need to manage sub-flows?
├─ NO (leaf coordinator)
│  └─ Simple coordinator
│     Owns NavigationPath, creates views
│
└─ YES (has sub-flows)
   └─ Parent coordinator
      Manages childCoordinators array
      Delegates to child for sub-flows
```

### SwiftUI vs UIKit Coordinator

```
Which UI framework?
├─ SwiftUI
│  └─ Coordinator as ObservableObject
│     • Owns NavigationPath
│     • @ViewBuilder for destinations
│     • Pass via EnvironmentObject or explicit injection
│
└─ UIKit
   └─ Coordinator owns UINavigationController
      • Creates and pushes ViewControllers
      • Uses delegation for flow completion
      • Manages childCoordinators manually
```

### Flow Completion Strategy

```
How does a flow end?
├─ Success (user completed task)
│  └─ Delegate method with result
│     coordinator.didCompleteLogin(user: user)
│
├─ Cancellation (user backed out)
│  └─ Delegate method without result
│     coordinator.didCancelLogin()
│
└─ Automatic (flow naturally ends)
   └─ Parent removes child automatically
      No explicit completion needed
```

---

## NEVER Do

### Child Coordinator Lifecycle

**NEVER** forget to remove child coordinators:
```swift
// ❌ Memory leak — child coordinator retained forever
final class ParentCoordinator {
    var childCoordinators: [Coordinator] = []

    func startLoginFlow() {
        let loginCoordinator = LoginCoordinator()
        childCoordinators.append(loginCoordinator)
        loginCoordinator.start()
        // Never removed! Leaks.
    }
}

// ✅ Remove child on flow completion
final class ParentCoordinator: LoginCoordinatorDelegate {
    var childCoordinators: [Coordinator] = []

    func startLoginFlow() {
        let loginCoordinator = LoginCoordinator()
        loginCoordinator.delegate = self
        childCoordinators.append(loginCoordinator)
        loginCoordinator.start()
    }

    func loginCoordinatorDidFinish(_ coordinator: LoginCoordinator) {
        childCoordinators.removeAll { $0 === coordinator }
    }
}
```

**NEVER** use strong parent references:
```swift
// ❌ Retain cycle — coordinator never deallocates
final class ChildCoordinator {
    var parent: ParentCoordinator  // Strong reference!
}

// ✅ Weak parent or delegate
final class ChildCoordinator {
    weak var delegate: ChildCoordinatorDelegate?
    // OR
    weak var parent: ParentCoordinator?
}
```

### Coordinator Responsibilities

**NEVER** put business logic in coordinators:
```swift
// ❌ Coordinator doing business logic
final class CheckoutCoordinator {
    func completeOrder() async {
        // Business logic leaked into coordinator!
        let total = cart.items.reduce(0) { $0 + $1.price }
        let tax = total * 0.08
        try await paymentService.charge(total + tax)
    }
}

// ✅ Coordinator orchestrates, ViewModel/UseCase handles logic
final class CheckoutCoordinator {
    func showCheckout() {
        let viewModel = CheckoutViewModel(
            cartService: container.cartService,
            paymentService: container.paymentService
        )
        // ViewModel handles business logic
    }
}
```

**NEVER** let views know about coordinator hierarchy:
```swift
// ❌ View knows about parent coordinator
struct LoginView: View {
    let coordinator: LoginCoordinator

    var body: some View {
        Button("Done") {
            coordinator.parent?.childDidFinish(coordinator)  // Wrong!
        }
    }
}

// ✅ View only knows its immediate coordinator
struct LoginView: View {
    let coordinator: LoginCoordinator

    var body: some View {
        Button("Done") {
            coordinator.completeLogin()  // Coordinator handles delegation
        }
    }
}
```

### SwiftUI-Specific

**NEVER** create coordinators as @StateObject in child views:
```swift
// ❌ New coordinator created on every parent rebuild
struct ParentView: View {
    var body: some View {
        ChildView()  // Child creates its own coordinator
    }
}

struct ChildView: View {
    @StateObject var coordinator = ChildCoordinator()  // Wrong!
}

// ✅ Parent creates and owns coordinator
struct ParentView: View {
    @StateObject var childCoordinator = ChildCoordinator()

    var body: some View {
        ChildView(coordinator: childCoordinator)
    }
}
```

**NEVER** use NavigationLink directly when using coordinators:
```swift
// ❌ Bypasses coordinator — navigation untracked
struct UserListView: View {
    var body: some View {
        NavigationLink("User") {
            UserDetailView()  // Coordinator doesn't know about this!
        }
    }
}

// ✅ Delegate navigation to coordinator
struct UserListView: View {
    @ObservedObject var coordinator: UsersCoordinator

    var body: some View {
        Button("User") {
            coordinator.showUserDetail(userId: "123")
        }
    }
}
```

---

## Essential Patterns

### SwiftUI Coordinator Protocol

```swift
@MainActor
protocol Coordinator: ObservableObject {
    associatedtype Route: Hashable
    var path: NavigationPath { get set }

    func start() -> AnyView
    func navigate(to route: Route)
    func pop()
    func popToRoot()
}

extension Coordinator {
    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path = NavigationPath()
    }
}
```

### Parent-Child Coordinator

```swift
@MainActor
protocol ParentCoordinatorProtocol: AnyObject {
    var childCoordinators: [any Coordinator] { get set }
    func addChild(_ coordinator: any Coordinator)
    func removeChild(_ coordinator: any Coordinator)
}

extension ParentCoordinatorProtocol {
    func addChild(_ coordinator: any Coordinator) {
        childCoordinators.append(coordinator)
    }

    func removeChild(_ coordinator: any Coordinator) {
        childCoordinators.removeAll { $0 === coordinator as AnyObject }
    }
}

// Tab coordinator managing child coordinators
@MainActor
final class TabCoordinator: ParentCoordinatorProtocol, ObservableObject {
    var childCoordinators: [any Coordinator] = []

    lazy var homeCoordinator: HomeCoordinator = {
        let coordinator = HomeCoordinator()
        coordinator.parent = self
        addChild(coordinator)
        return coordinator
    }()

    lazy var profileCoordinator: ProfileCoordinator = {
        let coordinator = ProfileCoordinator()
        coordinator.parent = self
        addChild(coordinator)
        return coordinator
    }()
}
```

### Flow Completion with Result

```swift
protocol LoginCoordinatorDelegate: AnyObject {
    func loginCoordinator(_ coordinator: LoginCoordinator, didFinishWith result: LoginResult)
}

enum LoginResult {
    case success(User)
    case cancelled
}

@MainActor
final class LoginCoordinator: ObservableObject {
    weak var delegate: LoginCoordinatorDelegate?
    @Published var path = NavigationPath()

    enum Route: Hashable {
        case credentials
        case forgotPassword
        case twoFactor(email: String)
    }

    func completeLogin(user: User) {
        delegate?.loginCoordinator(self, didFinishWith: .success(user))
    }

    func cancel() {
        delegate?.loginCoordinator(self, didFinishWith: .cancelled)
    }
}
```

### Deep Link Integration

```swift
@MainActor
final class AppCoordinator: ObservableObject, ParentCoordinatorProtocol {
    var childCoordinators: [any Coordinator] = []
    @Published var path = NavigationPath()

    func handle(deepLink: DeepLink) {
        // Reset to known state
        popToRoot()
        childCoordinators.forEach { removeChild($0) }

        // Navigate to deep link destination
        switch deepLink {
        case .user(let id):
            navigate(to: .userList)
            navigate(to: .userDetail(userId: id))

        case .checkout:
            let checkoutCoordinator = CheckoutCoordinator()
            checkoutCoordinator.delegate = self
            addChild(checkoutCoordinator)
            // Present checkout flow

        case .settings(let section):
            navigate(to: .settings)
            if let section = section {
                navigate(to: .settingsSection(section))
            }
        }
    }
}
```

---

## Quick Reference

### Coordinator Checklist

- [ ] Coordinator owns NavigationPath (SwiftUI) or UINavigationController (UIKit)
- [ ] Parent-child references are weak
- [ ] Child coordinators removed on flow completion
- [ ] Views don't know about coordinator hierarchy
- [ ] Business logic stays in ViewModels/UseCases
- [ ] Deep links handled at appropriate coordinator level

### When to Use Coordinators

| Scenario | Use Coordinator? |
|----------|------------------|
| Simple 3-5 screen app | No — simple Router |
| Multiple independent flows | Yes |
| Deep linking required | Likely yes |
| Multi-step wizard flows | Yes |
| Cross-tab navigation | Yes |
| A/B testing navigation | Yes |
| Team-based feature ownership | Yes |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| childCoordinators grows forever | Memory leak | Remove on completion |
| Strong parent reference | Retain cycle | Use weak or delegate |
| Business logic in coordinator | Wrong layer | Move to ViewModel/UseCase |
| View creates NavigationLink | Bypasses coordinator | Delegate to coordinator |
| @StateObject coordinator in child | Recreated on rebuild | Parent owns coordinator |
| Coordinator creates its own views | Can't inject dependencies | Use ViewFactory |

### Coordinator vs Router

| Aspect | Coordinator | Router |
|--------|-------------|--------|
| Complexity | Higher | Lower |
| Hierarchy support | Yes (parent-child) | No |
| Flow isolation | Strong | Weak |
| Testing | Excellent | Good |
| Learning curve | Steep | Gentle |
| Best for | Large apps, teams | Small-medium apps |
