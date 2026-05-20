---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding new Views or ViewModels
- Creating new services

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + UI)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests (XCTest)
- Individual functions and utilities
- ViewModel logic
- Model validation
- Helpers and utilities

#### Integration Tests
- Service interactions
- Data persistence
- API calls (mocked)

#### UI Tests (XCUITest)
- Critical user flows
- Complete workflows
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Stories
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to select my problems during onboarding,
so that I receive relevant notifications.
```

### Step 2: Generate Test Cases
For each user story, create comprehensive test cases:

```swift
class ProblemSelectionTests: XCTestCase {

    func testProblemSelection_updatesSelectedProblems() {
        // Test implementation
    }

    func testProblemSelection_requiresAtLeastOneProblem() {
        // Test validation
    }

    func testProblemSelection_persistsToUserDefaults() {
        // Test persistence
    }

    func testProblemSelection_handlesMaxSelection() {
        // Test boundary
    }
}
```

### Step 3: Run Tests (They Should Fail)
```bash
xcodebuild test -scheme aniccaios -destination 'platform=iOS Simulator,name=iPhone 16'
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```swift
// Implementation guided by tests
func selectProblem(_ problem: ProblemType) {
    guard selectedProblems.count < maxSelections else { return }
    selectedProblems.append(problem)
    persistSelection()
}
```

### Step 5: Run Tests Again
```bash
xcodebuild test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
xcodebuild test -scheme aniccaios -enableCodeCoverage YES
# Verify 80%+ coverage achieved
```

## Swift Testing Patterns

### Unit Test Pattern (XCTest)
```swift
import XCTest
@testable import aniccaios

class ProblemTypeTests: XCTestCase {

    func testProblemType_hasDisplayName() {
        let problem = ProblemType.procrastination
        XCTAssertEqual(problem.displayName, "Procrastination")
    }

    func testProblemType_hasIcon() {
        for problem in ProblemType.allCases {
            XCTAssertFalse(problem.icon.isEmpty, "\(problem) should have an icon")
        }
    }

    func testProblemType_hasNudgeMessages() {
        let problem = ProblemType.anxiety
        XCTAssertFalse(problem.nudgeMessages.isEmpty)
    }
}
```

### ViewModel Test Pattern
```swift
class OnboardingViewModelTests: XCTestCase {

    var sut: OnboardingViewModel!

    override func setUp() {
        super.setUp()
        sut = OnboardingViewModel()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testSelectProblem_addsToSelection() {
        sut.selectProblem(.procrastination)

        XCTAssertTrue(sut.selectedProblems.contains(.procrastination))
    }

    func testSelectProblem_togglesIfAlreadySelected() {
        sut.selectProblem(.anxiety)
        sut.selectProblem(.anxiety)

        XCTAssertFalse(sut.selectedProblems.contains(.anxiety))
    }

    func testCanProceed_requiresAtLeastOneProblem() {
        XCTAssertFalse(sut.canProceed)

        sut.selectProblem(.rumination)

        XCTAssertTrue(sut.canProceed)
    }
}
```

### Async Test Pattern
```swift
func testFetchData_returnsData() async throws {
    let service = DataService()

    let result = try await service.fetchData()

    XCTAssertFalse(result.isEmpty)
}

func testFetchData_throwsOnNetworkError() async {
    let service = DataService(networkAvailable: false)

    do {
        _ = try await service.fetchData()
        XCTFail("Expected error to be thrown")
    } catch {
        XCTAssertTrue(error is NetworkError)
    }
}
```

### UI Test Pattern (XCUITest)
```swift
class OnboardingUITests: XCTestCase {

    var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["UI_TESTING"]
        app.launch()
    }

    func testOnboarding_completesSuccessfully() {
        // Welcome step
        app.buttons["Get Started"].tap()

        // Value step
        app.buttons["Continue"].tap()

        // Struggles step - select problems
        app.buttons["Procrastination"].tap()
        app.buttons["Anxiety"].tap()
        app.buttons["Continue"].tap()

        // Notification permission
        // (handled by system, skip in UI test)

        // Verify completion
        XCTAssertTrue(app.staticTexts["My Path"].waitForExistence(timeout: 5))
    }

    func testOnboarding_requiresProblemSelection() {
        app.buttons["Get Started"].tap()
        app.buttons["Continue"].tap()

        // Try to continue without selecting
        let continueButton = app.buttons["Continue"]
        XCTAssertFalse(continueButton.isEnabled)
    }
}
```

## Mocking Dependencies

### Protocol-Based Mocking
```swift
// Define protocol
protocol NotificationScheduling {
    func scheduleNotifications(for problems: [ProblemType])
}

// Production implementation
class ProblemNotificationScheduler: NotificationScheduling {
    func scheduleNotifications(for problems: [ProblemType]) {
        // Real implementation
    }
}

// Mock for testing
class MockNotificationScheduler: NotificationScheduling {
    var scheduledProblems: [ProblemType] = []

    func scheduleNotifications(for problems: [ProblemType]) {
        scheduledProblems = problems
    }
}

// Test usage
func testViewModel_schedulesNotifications() {
    let mockScheduler = MockNotificationScheduler()
    let viewModel = OnboardingViewModel(scheduler: mockScheduler)

    viewModel.completeOnboarding()

    XCTAssertEqual(mockScheduler.scheduledProblems, viewModel.selectedProblems)
}
```

## Edge Cases You MUST Test

1. **Nil/Optional**: What if value is nil?
2. **Empty**: What if array/string is empty?
3. **Invalid Input**: What if wrong data passed?
4. **Boundaries**: Min/max values
5. **Errors**: Network failures, disk full
6. **Permissions**: Denied, not determined
7. **Large Data**: Performance with many items

## Test Quality Checklist

Before marking tests complete:

- [ ] All public functions have unit tests
- [ ] All ViewModels have tests
- [ ] Critical user flows have UI tests
- [ ] Edge cases covered (nil, empty, invalid)
- [ ] Error paths tested (not just happy path)
- [ ] Mocks used for external dependencies
- [ ] Tests are independent (no shared state)
- [ ] Test names describe what's being tested
- [ ] Assertions are specific and meaningful
- [ ] Coverage is 80%+

## Common Testing Mistakes to Avoid

### Testing Implementation Details
```swift
// DON'T test private state
XCTAssertEqual(viewModel.internalCounter, 5)
```

### Test Observable Behavior
```swift
// DO test what users/consumers see
XCTAssertEqual(viewModel.displayText, "Count: 5")
```

### Tests Depend on Each Other
```swift
// DON'T rely on previous test
func testCreatesItem() { /* ... */ }
func testUpdatesSameItem() { /* needs previous test */ }
```

### Independent Tests
```swift
// DO setup data in each test
func testUpdatesItem() {
    let item = createTestItem()
    // Test logic
}
```

## Success Metrics

- 80%+ code coverage achieved
- All tests passing (green)
- No skipped or disabled tests
- Fast test execution
- UI tests cover critical user flows
- Tests catch bugs before production

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
