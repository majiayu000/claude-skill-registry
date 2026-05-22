---
name: generate-test-plan
description: Create comprehensive unit test plans for Swift code with TDD methodology. Use this when planning tests for new features, ensuring test coverage, creating test checklists, or implementing Test-Driven Development practices.
---

# Unit Test Plan Generator

Analyze Swift source files and generate comprehensive unit test plans with TDD focus and high coverage.

## Instructions

When asked to create a test plan for a Swift component:

1. **Analyze the Input**: Identify the main class/struct, its public API (methods and properties), initializers, and dependencies.

2. **Consider Test Categories**:
   - **Happy Path**: Normal, expected inputs and outcomes
   - **Edge Cases**: nil, empty strings/collections, zero, negative values, extreme values
   - **State Changes**: Verify internal state is correctly modified
   - **Invalid Inputs**: Graceful behavior with unexpected/invalid data
   - **Initializer Tests**: Object's initial state with different parameters

3. **Format as Markdown**:
   - Title: `# Test Plan for [ClassName]`
   - Use checkboxes: `- [ ]` for each test case
   - Group under clear headings: `## Initializer`, `## Method: myFunction()`
   - Use descriptive names: `test_when_given_this_should_do_that`

## Example

**Input:**
```swift
class TemperatureConverter {
    private(set) var celsius: Double

    init(celsius: Double) {
        self.celsius = celsius
    }

    func set(kelvin: Double) {
        guard kelvin >= 0 else { return }
        self.celsius = kelvin - 273.15
    }
}
```

**Output:**
```markdown
# Test Plan for TemperatureConverter

## Initializer
- [ ] `test_init_withPositiveCelsius_shouldSetPropertyCorrectly`
- [ ] `test_init_withZeroCelsius_shouldSetPropertyCorrectly`
- [ ] `test_init_withNegativeCelsius_shouldSetPropertyCorrectly`

## Method: set(kelvin:)
- [ ] `test_setKelvin_withPositiveValue_shouldUpdateCelsiusCorrectly`
- [ ] `test_setKelvin_withZeroValue_shouldUpdateCelsiusCorrectly`
- [ ] `test_setKelvin_withNegativeValue_shouldNotUpdateCelsius`
```

## Test Coverage Guidelines
- Test each public method with happy path, edge cases, and invalid inputs
- Verify state changes after method calls
- Test all initializer parameter combinations
- Ensure graceful error handling
- Test boundary conditions
