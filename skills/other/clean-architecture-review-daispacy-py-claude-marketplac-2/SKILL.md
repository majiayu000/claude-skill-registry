---
name: clean-architecture-review
description: Validate Clean Architecture implementation in iOS. Checks layer separation (Presentation/Domain/Data), MVVM patterns, dependency injection with Swinject, and UseCase/Repository patterns. Use when reviewing architecture, checking layer boundaries, or validating DI.
allowed-tools: Read, Grep, Glob
---

# Clean Architecture Validator

Verify Clean Architecture and MVVM implementation in iOS code following Payoo Merchant patterns.

## When to Activate

- "architecture review", "layer separation", "clean architecture"
- "MVVM", "dependency injection", "DI"
- "use case", "repository pattern"
- Reviewing module structure or refactoring

## Architecture Layers

**Presentation** → ViewControllers, ViewModels, Views
**Domain** → UseCases (business logic), Models, Repository protocols
**Data** → Repository implementations, API Services, Local Storage

**Correct Flow**:
```
UI → ViewController → ViewModel → UseCase → Repository → API/DB
```

## Review Process

### Step 1: Map Architecture

Classify files into layers:
- Presentation: `*ViewController.swift`, `*ViewModel.swift`
- Domain: `*UseCase.swift`, `*Repository.swift` (protocols)
- Data: `*RepositoryImpl.swift`, `*ApiService.swift`

### Step 2: Check Layer Violations

**Critical Issues**:
- 🔴 ViewModel calling API directly (bypassing UseCase)
- 🔴 Business logic in ViewModel (should be in UseCase)
- 🔴 UseCase calling API directly (bypassing Repository)
- 🔴 Direct instantiation (no DI)

### Step 3: Verify Patterns

**BaseViewModel**:
```swift
✅ class PaymentViewModel: BaseViewModel<PaymentState>
❌ class PaymentViewModel  // Should extend BaseViewModel
```

**UseCase Pattern**:
```swift
✅ protocol PaymentUseCase { }
✅ class PaymentUseCaseImpl: PaymentUseCase { }
❌ class PaymentUseCase { }  // Should be protocol + impl
```

**Repository Pattern**:
```swift
✅ protocol PaymentRepository { }  // In Domain
✅ class PaymentRepositoryImpl: PaymentRepository { }  // In Data
```

**Dependency Injection**:
```swift
✅ init(paymentUC: PaymentUseCase) {  // Constructor injection
    self.paymentUC = paymentUC
}
❌ let paymentUC = PaymentUseCaseImpl()  // Direct instantiation
```

### Step 4: Generate Report

Provide:
- Architecture compliance score
- Layer violations by severity
- Current vs. should-be architecture
- Refactoring steps
- Effort estimate

## Common Violations

### ❌ ViewModel Bypassing UseCase
```swift
class PaymentViewModel {
    private let apiService: PaymentApiService  // WRONG LAYER!
}
```
**Should be**:
```swift
class PaymentViewModel {
    private let paymentUC: PaymentUseCase  // CORRECT!
}
```

### ❌ Business Logic in ViewModel
```swift
class PaymentViewModel {
    func processPayment(amount: Double) {
        // ❌ Validation in ViewModel
        guard amount > 1000 else { return }
        // ❌ Business rules in ViewModel
        let fee = amount * 0.01
    }
}
```
**Should be in UseCase**:
```swift
class PaymentUseCaseImpl {
    func execute(amount: Double) -> Single<PaymentResult> {
        // ✅ Validation in UseCase
        return validateAmount(amount)
            .flatMap { processPayment($0) }
    }
}
```

## Output Format

```markdown
# Clean Architecture Review

## Compliance Score: X/100

## Critical Violations: X

### 1. ViewModel Bypassing UseCase
**File**: `PaymentViewModel.swift:15`
**Current**: ViewModel → API
**Should be**: ViewModel → UseCase → Repository → API

**Fix**: [Refactoring steps]

---

## Dependency Graph

### Current (Problematic)
ViewModel → ApiService ❌

### Should Be
ViewModel → UseCase → Repository → ApiService ✅

## Recommendations
1. Create missing UseCases
2. Move business logic to Domain layer
3. Setup DI container
4. Add Repository layer

## Effort Estimate
- Module refactoring: X hours
- DI setup: X hours
- Testing: X hours
```

## Quick Checks

**Layer Boundaries**:
- [ ] ViewModels only depend on UseCases
- [ ] UseCases contain all business logic
- [ ] Repositories handle data access only
- [ ] No UI code in Domain/Data layers

**Dependency Injection**:
- [ ] All dependencies via constructor
- [ ] No direct instantiation
- [ ] Swinject container registration
- [ ] Protocol-based dependencies

**Patterns**:
- [ ] ViewModels extend BaseViewModel
- [ ] UseCases follow protocol + impl
- [ ] Repositories follow protocol + impl
- [ ] State management via setState()

## Reference

**Detailed Examples**: See `examples.md` for complete architecture patterns and refactoring guides.
