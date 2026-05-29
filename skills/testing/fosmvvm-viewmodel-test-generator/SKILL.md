---
name: fosmvvm-viewmodel-test-generator
description: Generate comprehensive ViewModel tests with multi-locale translation verification. Use when creating test coverage for ViewModels, especially those with localization.
---

# FOSMVVM ViewModel Test Generator

Generate test files for ViewModels following FOSMVVM testing patterns.

## Conceptual Foundation

> For full architecture context, see [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md#testing-support)

ViewModel testing in FOSMVVM verifies three critical aspects:

1. **Codable round-trip** - ViewModel encodes and decodes without data loss
2. **Versioning stability** - Structure hasn't changed unexpectedly
3. **Multi-locale translations** - All `@LocalizedString` properties have values in all supported locales

The `LocalizableTestCase` protocol provides infrastructure that tests all three in a single call.

---

## When to Use This Skill

- Creating tests for new ViewModels
- Adding test coverage to existing ViewModels
- Verifying localization completeness across locales
- Testing ViewModels with embedded/nested child ViewModels
- Verifying `@LocalizedSubs` substitution behavior

## What This Skill Generates

| File | Location | Purpose |
|------|----------|---------|
| `{Name}ViewModelTests.swift` | `Tests/{Target}Tests/Localization/` | Test suite conforming to `LocalizableTestCase` |
| `{Name}ViewModel.yml` | `Tests/{Target}Tests/TestYAML/` | YAML translations for test (if needed) |

---

## The Testing Pattern

### Standard Pattern (Most Tests)

For most ViewModels, a single line provides complete coverage:

```swift
@Test func dashboardViewModel() throws {
    try expectFullViewModelTests(DashboardViewModel.self)
}
```

This verifies:
- Codable encoding/decoding
- Versioned ViewModel stability
- Translations exist for all locales (en, es by default)

**This is sufficient for the vast majority of ViewModel tests.**

### Extended Pattern (Specific Formatting Verification)

When testing specific formatting behavior (substitutions, compound strings), add locale-specific assertions:

```swift
@Test func greetingWithSubstitution() throws {
    try expectFullViewModelTests(GreetingViewModel.self)

    // Verify specific substitution behavior
    let vm: GreetingViewModel = try .stub()
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.welcomeMessage.localizedString == "Welcome, John!")
}
```

This is optional - use only when verifying specific formatting techniques.

---

## LocalizableTestCase Protocol

Test suites conform to `LocalizableTestCase` to access testing infrastructure:

```swift
import FOSFoundation
@testable import FOSMVVM
import FOSTesting
import Foundation
import Testing
@testable import {ViewModelsTarget}

@Suite("My ViewModel Tests")
struct MyViewModelTests: LocalizableTestCase {
    let locStore: LocalizationStore

    init() throws {
        self.locStore = try Self.loadLocalizationStore(
            bundle: {ViewModelsTarget}.resourceAccess,
            resourceDirectoryName: ""
        )
    }
}
```

The `{ViewModelsTarget}.resourceAccess` is the resource accessor defined when creating the ViewModels SPM target (via `FOSResourceAccessor` build tool plugin).

### What LocalizableTestCase Provides

| Property/Method | Purpose |
|-----------------|---------|
| `locStore` | Required - the localization store |
| `locales` | Optional - locales to test (default: en, es) |
| `encoder(locale:)` | Creates a localizing JSONEncoder |
| `en`, `es`, `enGB`, `enUS` | Locale constants |

### Testing Methods

| Method | Use When |
|--------|----------|
| `expectFullViewModelTests(_:)` | **Primary** - complete ViewModel testing |
| `expectTranslations(_:)` | Translation-only verification |
| `expectFullFieldValidationModelTests(_:)` | Testing FieldValidationModel types |
| `expectFullFormFieldTests(_:)` | Testing FormField instances |
| `expectCodable(_:encoder:)` | Codable round-trip only |
| `expectVersionedViewModel(_:encoder:)` | Versioning stability only |

---

## YAML Requirements

### ViewModels with @LocalizedString

Every ViewModel with `@LocalizedString` properties needs YAML entries:

```swift
@ViewModel
public struct DashboardViewModel: RequestableViewModel {
    @LocalizedString public var pageTitle      // Needs YAML entry
    @LocalizedString public var emptyMessage   // Needs YAML entry
    public let itemCount: Int                   // No YAML needed
}
```

```yaml
# DashboardViewModel.yml
en:
  DashboardViewModel:
    pageTitle: "Dashboard"
    emptyMessage: "No items yet"

es:
  DashboardViewModel:
    pageTitle: "Tablero"
    emptyMessage: "No hay elementos todavía"
```

### Embedded ViewModels

When a ViewModel contains child ViewModels, all types in the hierarchy need YAML entries:

```swift
@ViewModel
public struct BoardViewModel: RequestableViewModel {
    @LocalizedString public var title
    public let cards: [CardViewModel]  // Child ViewModel
}

@ViewModel
public struct CardViewModel {
    @LocalizedString public var cardTitle
}
```

Both `BoardViewModel` and `CardViewModel` need YAML entries (can be in same or separate files).

### Private Test ViewModels

When tests define private ViewModel structs for testing specific scenarios, those also need YAML:

```swift
// In test file
private struct TestParentViewModel: ViewModel {
    @LocalizedString var title
    let children: [TestChildViewModel]
}

private struct TestChildViewModel: ViewModel {
    @LocalizedString var label
}
```

Add entries to a test YAML file for these private types.

---

## Generation Process

### Step 1: Identify ViewModels to Test

Determine which ViewModels need test coverage:
- New ViewModels being created
- Existing ViewModels without tests
- ViewModels with localization properties

### Step 2: Check YAML Coverage

Verify YAML entries exist for:
- The ViewModel itself
- Any embedded/child ViewModels
- All supported locales (typically en, es)

### Step 3: Generate Test File

Create test suite conforming to `LocalizableTestCase`:
- One `@Test` function per ViewModel (or logical grouping)
- Use `expectFullViewModelTests()` as the primary assertion
- Add specific formatting tests only when needed

### Step 4: Run Tests

```bash
swift test --filter {TestSuiteName}
```

---

## File Templates

See [reference.md](reference.md) for complete file templates.

---

## Common Scenarios

### Testing a Single Top-Level ViewModel

```swift
@Test func dashboardViewModel() throws {
    try expectFullViewModelTests(DashboardViewModel.self)
}
```

### Testing Multiple Related ViewModels

```swift
@Test func boardViewModels() throws {
    try expectFullViewModelTests(BoardViewModel.self)
    try expectFullViewModelTests(ColumnViewModel.self)
    try expectFullViewModelTests(CardViewModel.self)
}
```

### Testing with Custom Locales

```swift
var locales: Set<Locale> { [en, es, enGB] }  // Override default

@Test func multiLocaleViewModel() throws {
    try expectFullViewModelTests(MyViewModel.self)
    // Tests en, es, AND en-GB
}
```

### Testing Substitution Behavior

```swift
@Test func greetingSubstitutions() throws {
    try expectFullViewModelTests(GreetingViewModel.self)

    let vm: GreetingViewModel = try .stub(userName: "Alice")
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.welcomeMessage.localizedString == "Welcome, Alice!")
}
```

### Testing Embedded ViewModels

```swift
@Test func parentWithChildren() throws {
    // Tests parent AND verifies children can be encoded/decoded
    try expectFullViewModelTests(ParentViewModel.self)

    // Optionally verify specific child values
    let vm: ParentViewModel = try .stub()
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.children[0].label.localizedString == "Child 1")
}
```

---

## Troubleshooting

### "Missing Translation" Error

```
FOSLocalizableError: _pageTitle -- Missing Translation -- en
```

**Cause:** YAML entry missing for a `@LocalizedString` property.

**Fix:** Add the property to the YAML file:
```yaml
en:
  MyViewModel:
    pageTitle: "Page Title"  # Add this
```

### "Is pending localization" Error

**Cause:** The ViewModel wasn't encoded with a localizing encoder.

**Fix:** Ensure using `encoder(locale:)` or `expectFullViewModelTests()`.

### Test Passes But Translations Seem Wrong

**Cause:** YAML values exist but may have typos or wrong content.

**Fix:** Add specific assertions to verify exact values:
```swift
let vm = try .stub().toJSON(encoder: encoder(locale: en)).fromJSON()
#expect(try vm.title.localizedString == "Expected Value")
```

---

## Naming Conventions

| Concept | Convention | Example |
|---------|------------|---------|
| Test suite | `{Feature}ViewModelTests` | `DashboardViewModelTests` |
| Test file | `{Feature}ViewModelTests.swift` | `DashboardViewModelTests.swift` |
| YAML file | `{ViewModelName}.yml` | `DashboardViewModel.yml` |
| Test method | `{viewModelName}()` or descriptive | `dashboardViewModel()` |

---

## See Also

- [FOSMVVMArchitecture.md - Testing Support](../../docs/FOSMVVMArchitecture.md#testing-support) - Architecture overview
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - For creating ViewModels
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - For form validation testing
- [reference.md](reference.md) - Complete file templates

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-02 | Initial skill |
| 1.1 | 2026-01-19 | Updated LocalizableTestCase example to use {ViewModelsTarget}.resourceAccess pattern. |
