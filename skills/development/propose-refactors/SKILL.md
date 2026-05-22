---
name: propose-refactors
description: Provide expert code review and refactoring suggestions for Swift code, focusing on clarity, maintainability, performance, and modern best practices. Use this during code reviews, when improving code quality, or identifying technical debt.
---

# Code Review & Refactoring Suggestions

Analyze Swift code and provide actionable refactoring suggestions focused on clarity, maintainability, performance, and modern Swift best practices.

## Review Focus Areas

### 1. Clarity & Readability
- Self-documenting code with clear names
- Avoid overly complex expressions
- Comment long or complex logic blocks

### 2. Swift Best Practices
- **Value vs. Reference Types**: Could a `class` be a `struct`?
- **Immutability**: Use `let` instead of `var` wherever possible
- **Control Flow**: Use `guard` for early exits
- **Functional Programming**: Replace imperative loops with `map`, `filter`, `compactMap`
- **API Design**: Intuitive public API that hides implementation details

### 3. Architectural Principles
- **Single Responsibility Principle (SRP)**: One reason to change per type
- **Don't Repeat Yourself (DRY)**: Extract duplicated code
- **Dependency Inversion**: Use protocols for easier testing and dependency injection

## Output Format

```markdown
# Refactoring Suggestions for [FileName]

[If no issues: "No major refactoring opportunities were identified. The code is clean and well-structured."]

---
**Suggestion:** [Brief summary of recommended change]

**Location:** [Line number or function/property name]

**Reasoning:** [Why this change is recommended, referencing specific principles]

**Example:**
```swift
// Before
...
// After
...
```
---
```

## Example Review

For code with issues:

```markdown
# Refactoring Suggestions for TemperatureConverter.swift

---
**Suggestion:** Consider making `TemperatureConverter` a struct instead of a class

**Location:** Line 3 (class declaration)

**Reasoning:** This type has no inheritance requirements and leverages value semantics would be more appropriate. Structs are preferred in Swift for data-centric types without identity requirements.

**Example:**
```swift
// Before
class TemperatureConverter {
    var celsius: Double
}

// After
struct TemperatureConverter {
    var celsius: Double
}
```
---

**Suggestion:** Replace `var` with `let` for immutable property

**Location:** Line 12 (`threshold` property)

**Reasoning:** This property is never reassigned after initialization. Using `let` makes the immutability explicit and prevents accidental modifications.
---
```

## Tone
Constructive and educational - explain the "why" behind each suggestion.
