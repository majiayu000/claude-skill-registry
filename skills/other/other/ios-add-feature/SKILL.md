---
name: ios-add-feature
description: Scaffold a new feature with View, ViewModel, and tests following ios-std conventions.
argument-hint: "<feature-name> [--with-detail] [--with-form] [--no-tests]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add a complete feature module to an existing iOS project with View, ViewModel, and tests.

## Arguments
- `feature-name` — Feature name in PascalCase (e.g., `Settings`, `UserProfile`)
- `--with-detail` — Include detail view for drill-down
- `--with-form` — Include form/edit view
- `--no-tests` — Skip test file generation

## What gets created

### Default
```
Features/<Feature>/
├── <Feature>View.swift           # Main view
├── <Feature>ViewModel.swift      # ViewModel with state + intents
└── <Feature>Row.swift            # List row component (if list-based)

Tests/UnitTests/
└── <Feature>ViewModelTests.swift # ViewModel tests
```

### With `--with-detail`
```
Features/<Feature>/
├── <Feature>View.swift
├── <Feature>ViewModel.swift
├── <Feature>DetailView.swift     # Detail view
└── <Feature>DetailViewModel.swift
```

### With `--with-form`
```
Features/<Feature>/
├── <Feature>View.swift
├── <Feature>ViewModel.swift
├── <Feature>FormView.swift       # Create/edit form
└── <Feature>FormViewModel.swift
```

## Conventions

### File naming
- Views: `<Feature>View.swift`
- ViewModels: `<Feature>ViewModel.swift`
- Rows/cells: `<Feature>Row.swift`
- Tests: `<Feature>ViewModelTests.swift`

### ViewModel pattern
- `@MainActor final class`
- `@Published private(set)` for state
- Public methods for intents
- Dependencies injected via init
- Uses `PersistenceStore` protocol (not SwiftData directly)

### View pattern
- `@StateObject` for owned ViewModel
- `@EnvironmentObject` for shared services
- No business logic in views
- Accessibility labels on controls

### Test pattern (Swift Testing)
- `struct` (not `XCTestCase` class)
- `init()` for setup (not `setUp()`)
- `@Test func methodName()` (no `test_` prefix)
- `#expect(condition)` for assertions
- `@Test(arguments:)` for parameterized tests

## Workflow
1. Create feature folder under `Features/`
2. Create View with basic layout
3. Create ViewModel with state and intents
4. Wire up to DependencyContainer
5. Create tests for ViewModel
6. Run `./scripts/lint.sh` and tests to verify

## Output
Summarize: files created, how to access the feature, test coverage.

## Reference
For templates and patterns, see `reference/ios-add-feature-reference.md`
