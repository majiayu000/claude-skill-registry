---
name: ios-generate-unit-tests
description: Generate comprehensive unit tests for iOS RxSwift project files (ViewModels, UseCases, Services). Creates complete test files with nested mocks, RxTest patterns, session error handling, and memory leak tests. Use when "generate unit tests", "write tests for", "create unit tests", "add tests for", or analyzing Swift files in PayooMerchant project.
allowed-tools: Read, Write, Glob, Grep
---

# iOS RxSwift Unit Test Generator

Automatically generate comprehensive unit tests for iOS RxSwift project following Clean Architecture patterns.

## When to Activate

- "generate unit tests for [file]"
- "write tests for [ViewModel/UseCase/Service]"
- "create unit tests for this file"
- "add tests for [class name]"
- "test [file path]"

## Process

### 1. Identify Target File

**Ask user for file to test** (if not provided):
```
Which file would you like to generate tests for?
Provide the file path or class name (e.g., BalanceInformationViewModel.swift)
```

**Read target file** and determine type:
- ViewModel: Has `ViewModelType`, `Input`, `Output`, `transform` method
- UseCase: Implements `*UseCaseType` protocol
- Service: Implements service protocol

### 2. Read Testing Guide

**CRITICAL**: Read the comprehensive testing guide:
```
~/Library/Application Support/Code/User/prompts/ios-mc-generate-unit-test.prompt.md
```

This guide contains ALL rules, patterns, and examples to follow.

### 3. Analyze Target File

**Extract from target file:**
- Class name and type (ViewModel/UseCase/Service)
- All dependencies (injected in initializer)
- Protocol types for each dependency
- Public methods and their signatures
- Input/Output structure (for ViewModels)
- Observable/Single/Completable return types

**Search for protocol definitions** if needed:
```bash
Glob: **/*UseCaseType.swift
Grep: "protocol [DependencyName]"
```

### 4. Generate Test File

**Create complete test file** at:
```
PayooMerchantTests/[appropriate-folder]/[ClassName]Tests.swift
```

**Folder structure:**
- ViewModels → `PayooMerchantTests/ViewModel/`
- UseCases → `PayooMerchantTests/UseCase/`
- Services → `PayooMerchantTests/Mock/Service/`

**Test file MUST include:**

1. **Required imports**:
   ```swift
   import XCTest
   import RxSwift
   import RxCocoa
   import RxTest
   import RxBlocking
   import Domain
   @testable import PayooMerchant
   ```

2. **Test class with nested mocks**:
   - ALL mocks as `private final class` nested inside test class
   - One mock for EACH dependency
   - Include call tracking (`callCount`, `lastParams`)
   - Include configurable return values

3. **Properties section**:
   - `private var disposeBag: DisposeBag!`
   - `private var scheduler: TestScheduler!`
   - Mock instances for each dependency

4. **setUp/tearDown**:
   - Initialize disposeBag, scheduler, all mocks
   - Clean up all properties to nil

5. **Test data factories**:
   - Helper methods to create test entities
   - Use default parameters

6. **Comprehensive test methods**:
   - Initial load success
   - Load error handling
   - Empty state
   - Loading state
   - Session error handling (if API calls)
   - Memory leak test (for ViewModels)
   - Permission tests (if applicable)
   - User action tests
   - State transition tests
   - Edge cases

**Follow naming convention**:
```swift
func test_methodName_condition_expectedBehavior()
```

### 5. Generate Tests Based on Type

#### For ViewModels:
- Test each Input → Output transformation
- Use `TestScheduler` and hot observables for inputs
- Create observers for each output driver
- Test loading states, errors, empty states
- Include memory leak test:
  ```swift
  func test_viewModel_shouldDeallocateProperly()
  ```

#### For UseCases:
- Test each public method
- Mock all service dependencies
- Test success and error scenarios
- **CRITICAL**: Test session error handling:
  ```swift
  func test_catchSessionError_SessionTimeoutError_shouldSetExpiredState()
  func test_catchSessionError_ForceUpdateError_shouldSetForceUpdateState()
  ```

#### For Services:
- Test all CRUD operations
- Test observable streams
- Test data persistence

### 6. Validate Generated Tests

**Ensure:**
- ✅ All mocks are nested `private final class`
- ✅ Proper imports included
- ✅ setUp/tearDown with cleanup
- ✅ DisposeBag and TestScheduler used
- ✅ Descriptive test names
- ✅ Descriptive assertions with messages
- ✅ All dependencies mocked
- ✅ Session error tests for API calls
- ✅ Memory leak test for ViewModels

## Output Format

After generating tests, show:

```markdown
✅ Generated Unit Tests: [ClassName]Tests.swift

📁 Location: PayooMerchantTests/[folder]/[ClassName]Tests.swift

📊 Test Coverage:
- [X] Nested mocks created: [count]
- [X] Test methods: [count]
- [X] Scenarios covered:
  ✓ Success cases
  ✓ Error handling
  ✓ Empty states
  ✓ Loading states
  ✓ Session errors (if API)
  ✓ Memory leak test (if ViewModel)
  ✓ [Other scenarios]

🎯 Test Naming Pattern:
test_methodName_condition_expectedBehavior

⚡ Next Steps:
1. Review generated tests
2. Run: xcodebuild test -scheme PayooMerchantTests
3. Or run specific plan: bundle exec fastlane run_test_plan test_plan:"[plan-name]"

📖 Generated following guide: ~/Library/Application Support/Code/User/prompts/ios-mc-generate-unit-test.prompt.md
```

## Key Rules (from Testing Guide)

1. **ALWAYS** create mocks as nested `private final class`
2. **ALWAYS** use TestScheduler for ViewModels
3. **ALWAYS** include session error tests for API calls
4. **ALWAYS** include memory leak test for ViewModels
5. **ALWAYS** use descriptive assertions with messages
6. **ALWAYS** follow Arrange-Act-Assert pattern
7. **NEVER** create global/standalone mock classes
8. **NEVER** skip setUp/tearDown cleanup

## Example Test Structure

```swift
final class BalanceInformationViewModelTests: XCTestCase {
    // MARK: - Mocks
    private final class MockBalanceUseCase: BalanceUseCaseType {
        var getBalanceResult: Single<Balance> = .never()
        var getBalanceCallCount = 0
        
        func getBalance() -> Single<Balance> {
            getBalanceCallCount += 1
            return getBalanceResult
        }
    }
    
    // MARK: - Properties
    private var disposeBag: DisposeBag!
    private var scheduler: TestScheduler!
    private var mockBalanceUC: MockBalanceUseCase!
    
    // MARK: - Setup & Teardown
    override func setUp() {
        super.setUp()
        disposeBag = DisposeBag()
        scheduler = TestScheduler(initialClock: 0)
        mockBalanceUC = MockBalanceUseCase()
    }
    
    override func tearDown() {
        disposeBag = nil
        scheduler = nil
        mockBalanceUC = nil
        super.tearDown()
    }
    
    // MARK: - Test Data Factory
    private func makeTestBalance() -> Balance {
        // ...
    }
    
    // MARK: - Tests
    func test_transform_withLoadTrigger_shouldReturnBalance() {
        // Arrange
        // Act
        // Assert
    }
}
```

---

**References:**
- Testing Guide: `~/Library/Application Support/Code/User/prompts/ios-mc-generate-unit-test.prompt.md`
- Project Structure: `PayooMerchantTests/`
- Existing Tests: Use as reference for patterns
