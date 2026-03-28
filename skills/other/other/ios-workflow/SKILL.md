---
name: ios-workflow
description: iOS-specific workflow activated automatically when platform-context.json reports primary_platform=ios. Handles toolchain verification, Swift Testing patterns, XcodeBuildMCP integration, and SwiftLint.
---

# iOS Workflow

Activated **automatically** when the Platform Detection Engine identifies an iOS/Swift project.
**Never activate this manually in non-iOS projects.**

## Phase 1: Toolchain verification

When iOS is detected, check and report tool availability:

```
🍎 iOS project detected. Checking toolchain...

✅ swift        — found (Swift 6.0.3)
✅ xcodebuild   — found (Xcode 16.2)
✅ swiftlint    — found (0.57.0)
✅ XcodeBuildMCP — found (~/.claude/skills/xcodebuildmcp/SKILL.md)
⚠️ xcbeautify  — not found (optional: brew install xcbeautify)

iOS toolchain ready.
```

Checks to perform:
- `swift --version` → report Swift version
- `xcodebuild -version` → report Xcode version
- `command -v swiftlint && swiftlint version` → report version or "not found"
- `ls ~/.claude/skills/xcodebuildmcp/SKILL.md 2>/dev/null` → XcodeBuildMCP presence
- `command -v xcbeautify` → optional, just report

**None of these checks are blockers** — missing tools generate warnings, not errors.

## Phase 2: Test Framework Detection

Determine whether the project uses Swift Testing or XCTest:

```bash
# Count test files using each framework
swift_testing_count=$(grep -r "import Testing" . --include="*.swift" -l 2>/dev/null | wc -l)
xctest_count=$(grep -r "import XCTest" . --include="*.swift" -l 2>/dev/null | wc -l)
```

- `swift_testing_count > 0` AND `xctest_count == 0` → use **Swift Testing**
- `xctest_count > 0` AND `swift_testing_count == 0` → use **XCTest** (legacy)
- Both present → use **Swift Testing** for new tests, keep existing XCTest tests
- None found → default to **Swift Testing** (modern standard)

Report to user:
```
🧪 Test framework: Swift Testing (@Test, @Suite, #expect)
```
or:
```
🧪 Test framework: XCTest (existing project uses XCTest — maintaining consistency)
```

## Phase 3: iOS Test Pipeline

Execute in this exact order:

### Step 1 — Unit tests (swift test or xcodebuild)

```bash
# Option A: Swift Package Manager project
swift test --parallel

# Option B: Xcode project/workspace (if .xcodeproj/.xcworkspace found)
xcodebuild test \
  -scheme {detected_scheme} \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -resultBundlePath .claude/feature-state/{slug}/test-results.xcresult \
  | xcbeautify 2>/dev/null || cat
```

Detect which to use: if `Package.swift` exists without `.xcodeproj` → use `swift test`.

### Step 2 — SwiftLint (files modified by this feature only)

Run SwiftLint **only on modified files** — not the whole project:

```bash
# Get files modified since the feature branch started
modified_files=$(git diff --name-only HEAD~1 -- "*.swift" 2>/dev/null)

# Run swiftlint on those files only (if swiftlint is available)
if command -v swiftlint > /dev/null 2>&1 && [ -n "$modified_files" ]; then
  swiftlint lint $modified_files --reporter json > .claude/feature-state/{slug}/swiftlint.json
  swiftlint lint $modified_files  # human-readable output
fi
```

If swiftlint not found: skip with `⚠️ swiftlint not found — skipping lint`.

### Step 3 — XcodeBuildMCP build + simulator (optional, non-blocking)

Only if `capabilities.xcodebuildmcp_available == true` in platform-context.json:

```
1. /xcodebuildmcp discover_projs
   → find .xcodeproj or .xcworkspace

2. /xcodebuildmcp session_set_defaults
   → configure scheme, destination, configuration

3. /xcodebuildmcp build_run_sim
   → build + launch on iOS Simulator
   → capture build output and simulator status
```

Result reporting:
```
✅ App running on iPhone 16 Simulator (iOS 18.3)
```
or:
```
⚠️ Simulator build failed: [error summary] — tests passed, continuing to commit
```

**XcodeBuildMCP failure is non-blocking.** Unit tests passing is sufficient for the workflow.

## Swift Testing patterns for iOS

When generating new tests (Test Only mode or per-task test generation), always use Swift Testing — **never XCTest** — unless the project exclusively uses XCTest.

### Required imports and structure

```swift
import Testing
@testable import {ModuleName}

@Suite("ViewModel or UseCase Name")
struct PersonalTrainerViewModelTests {

    @Test("describe the behavior, not the method name")
    func loadsTrainerOnAppear() async throws {
        // Arrange
        let viewModel = PersonalTrainerViewModel(
            discoverTrainersUseCase: MockDiscoverTrainersUseCase(),
            featureFlagChecker: MockFeatureFlagChecker(enabled: true)
        )

        // Act
        await viewModel.onAppear()

        // Assert
        #expect(viewModel.isFeatureEnabled == true)
        #expect(viewModel.currentTrainer != nil)
    }

    @Test("does not load trainer when feature flag is disabled")
    func doesNotLoadWhenDisabled() async {
        let viewModel = PersonalTrainerViewModel(
            featureFlagChecker: MockFeatureFlagChecker(enabled: false)
        )
        await viewModel.onAppear()
        #expect(viewModel.currentTrainer == nil)
    }

    // Parameterized test
    @Test("requestConnection returns true for valid trainer IDs",
          arguments: ["trainer-alpha", "trainer-beta", "trainer-gamma"])
    func requestConnectionSucceeds(trainerId: String) async {
        let viewModel = PersonalTrainerViewModel(
            connectTrainerUseCase: MockConnectTrainerUseCase(shouldSucceed: true)
        )
        let result = await viewModel.requestConnection(trainerId: trainerId)
        #expect(result == true)
    }
}
```

### Rules for iOS tests

- Use `@Suite` to group related tests (one suite per ViewModel/UseCase/Repository)
- Use `@Test("behavior description")` — describe what it does, not the method
- Use `#expect(condition)` for assertions — never `XCTAssert`
- Use `#require(value)` to unwrap optionals that must exist
- Use `throws` for tests that can throw, `async throws` for async tests
- Use `arguments:` for data-driven tests (replaces XCTest `parametrize`)
- Use `.tags()` trait for categorization: `@Test("...", .tags(.unit, .viewModel))`
- **Never** use `XCTest`, `XCTAssert*`, or `class FooTests: XCTestCase`

### File structure for iOS tests

Follow the existing project convention. If no convention exists, use:

```
{ProjectName}/
└── {ProjectName}Tests/
    ├── Domain/
    │   └── UseCases/
    │       └── {UseCase}Tests.swift     ← one file per use case
    ├── Data/
    │   ├── Repositories/
    │   │   └── {Repository}Tests.swift
    │   └── Services/
    │       └── {Service}Tests.swift
    └── Presentation/
        └── Features/
            └── {Feature}/
                └── {Feature}ViewModelTests.swift
```

### Test file naming

- One test file per production file: `PersonalTrainerViewModel.swift` → `PersonalTrainerViewModelTests.swift`
- Place in mirror directory under `{ProjectName}Tests/`

## Test Only mode — iOS

When `--mode test-only` is invoked on an iOS project:

1. Detect test framework (Swift Testing vs XCTest)
2. Find Swift files without corresponding test files:
   ```bash
   find . -name "*.swift" \
     ! -name "*Tests.swift" \
     ! -name "*Mock*" \
     ! -path "*/Tests/*" \
     -type f 2>/dev/null
   ```
3. For each file without tests, check if it's testable (ViewModels, UseCases, Repositories, Services)
4. Present to user:
   ```
   Found 3 files without test coverage:
   - Presentation/Features/PersonalTrainer/PersonalTrainerViewModel.swift
   - Domain/UseCases/ConnectTrainerUseCase.swift
   - Data/Repositories/TrainerRepository.swift

   Generate Swift Testing tests for these files? [yes/no/select]
   ```
5. Generate tests following Swift Testing patterns above
6. Run `swift test --parallel`
7. If XcodeBuildMCP available: optionally run build on simulator
8. Report coverage delta

## Configuration in platform-context.json

The iOS entry in `platform-context.json` includes:

```json
{
  "type": "ios",
  "test_framework": "swift-testing",
  "capabilities": {
    "swiftlint_available": true,
    "xcodebuildmcp_available": true,
    "swift_testing_available": true
  }
}
```

This configuration is **ignored completely** on non-iOS projects.
