---
name: build-iphone-apps
description: Build professional native iPhone apps in Swift with SwiftUI and UIKit. Full lifecycle development - build, debug, test, optimize, ship. CLI-focused workflow. Use when building iOS apps, adding features, debugging, testing, or optimizing iPhone applications.
---

# Build iPhone Apps - Professional iOS Development

Expert guidance for building native iPhone apps using Swift, SwiftUI, and UIKit with CLI-first workflow.

## Core Principles

### 1. Prove, Don't Promise

Never say "this should work." Always verify:

```bash
# Build
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' build

# Test
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' test

# Launch
xcrun simctl boot "iPhone 16"
xcrun simctl install booted ./build/Build/Products/Debug-iphonesimulator/AppName.app
xcrun simctl launch booted com.company.AppName
```

**If you didn't run it, you don't know it works.**

### 2. Tests for Correctness, Eyes for Quality

| Question | How to Answer |
|----------|---------------|
| Does the logic work? | Write test, see it pass |
| Does it look right? | Launch in simulator, visual check |
| Does it feel right? | User tests interaction |
| Does it crash? | Test + launch verification |
| Is it fast enough? | Profiler |

**Tests verify correctness. Users verify desirability.**

### 3. Report Outcomes, Not Code

❌ **Bad**: "I refactored DataService to use async/await with weak self capture"
✅ **Good**: "Fixed the memory leak. `leaks` now shows 0 leaks. App tested stable for 5 minutes."

**Users care what's different, not what changed.**

### 4. Small Steps, Always Verified

```
Change → Verify → Report → Next change
```

Never batch work. Each change verified before the next. If something breaks, you know exactly what caused it.

### 5. Ask Before, Not After

- Unclear requirement? **Ask now**
- Multiple valid approaches? **Ask which**
- Scope creep? **Ask if wanted**
- Big refactor needed? **Ask permission**

❌ **Wrong**: Build for 30 minutes, then "is this what you wanted?"
✅ **Right**: "Before I start, does X mean Y or Z?"

### 6. Always Leave It Working

Every stopping point = working state. Tests pass, app launches, changes committed.

### 7. Debug Logging Protocol

```swift
// DEBUG: Testing YIN accuracy corrections
print("YIN Detected: \(frequency) Hz")
```

1. **Mark clearly** with `// DEBUG:` prefix
2. **Gather data** to understand the problem
3. **Remove before final commit** (unless explicitly requested)

**Production code should not have debug prints.** Use `os_log` for production.

---

## Verification Loop

After every change:

```bash
# 1. Build
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' build

# 2. Test
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' test

# 3. Launch
xcrun simctl boot "iPhone 16"
xcrun simctl install booted ./build/Build/Products/Debug-iphonesimulator/AppName.app
xcrun simctl launch booted com.company.AppName
```

Report: "Build: ✓, Tests: 12 pass 0 fail, App launches"

---

## When to Write Tests

✅ **Write test when**:
- Logic must be correct (calculations, transformations)
- State changes (add, delete, update)
- Edge cases (nil, empty, boundaries)
- Bug fixes (reproduce, then fix)
- Refactoring (prove behavior unchanged)

⏭️ **Skip test when**:
- UI exploration ("make it blue")
- Rapid prototyping
- Subjective quality
- One-off verification

**Principle**: Tests verify correctness without reading code.

---

## SwiftUI Patterns

### State Management
```swift
// View-local state
@State private var isExpanded = false

// Shared observable
@StateObject private var viewModel = MyViewModel()

// Environment
@Environment(\.colorScheme) var colorScheme
```

### Memory Management
```swift
// Avoid retain cycles
service.fetchData { [weak self] result in
    guard let self = self else { return }
    self.handle(result)
}

// UI updates
@MainActor
func updateUI() { /* ... */ }
```

---

## CLI Commands

### Build
```bash
xcodebuild -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16' build
xcodebuild clean -scheme AppName
```

### Test
```bash
xcodebuild test -scheme AppName -destination 'platform=iOS Simulator,name=iPhone 16'
xcodebuild test -only-testing:AppTests/FeatureTests/test_specific
```

### Simulator
```bash
xcrun simctl list devices
xcrun simctl boot "iPhone 16"
xcrun simctl install booted path/to/App.app
xcrun simctl launch booted com.company.AppName
xcrun simctl spawn booted log stream
```

---

## Remember

1. **Prove it works** - Build, test, launch
2. **Small steps** - Verify each change
3. **Ask first** - Clarify requirements
4. **Report outcomes** - What's different
5. **Leave it working** - Every stop = working state
6. **Tests for logic, eyes for UI**
7. **Mark debug logging, remove before commit**
