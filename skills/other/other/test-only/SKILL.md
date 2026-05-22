---
name: test-only
description: Multi-platform Test Only mode. Reads platform-context.json and routes to the correct test framework guidance (Swift Testing for iOS, Jest/Vitest for Node.js, cargo test for Rust, pytest for Python, go test for Go).
---

# Test Only Mode — Multi-Platform

Routes test generation to the correct framework based on the platform detected by the Platform Detection Engine.

## Entry conditions

- `EXECUTION_MODE=test-only` or `--mode test-only` flag
- `platform-context.json` must exist (run Platform Detection first if missing)
- Skips Phases 0–2 (inputs gate, planning, implementation)

## Unified flow

```
/feature-marker --mode test-only prd-{slug}
      ↓
1. Load platform-context.json
      ↓
2. Identify files without test coverage (platform-specific convention)
      ↓
3. Present to user: "Found N files without tests. Generate? [yes/no/select]"
      ↓
4. Generate tests in correct framework for platform
      ↓
5. Run platform test suite
      ↓
6. Report: coverage before/after, tests passing/failing
      ↓
7. Save to .claude/feature-state/{slug}/test-results.md
```

## Step 2: Finding untested files by platform

### 🍎 iOS / Swift

Files to test: `*ViewModel.swift`, `*UseCase.swift`, `*Repository.swift`, `*Service.swift`

```bash
# Production Swift files without a *Tests.swift counterpart
find . -name "*.swift" \
  ! -name "*Tests.swift" \
  ! -name "*Mock*.swift" \
  ! -name "*Stub*.swift" \
  ! -path "*/Tests/*" \
  ! -path "*/.build/*" \
  -type f
```

For each found file, check if a `{FileName}Tests.swift` exists anywhere in the project:
- If no → candidate for test generation
- If yes → check test count (`grep -c "@Test\|func test" {TestFile}`)

### 🟨 Node.js / TypeScript

```bash
# TypeScript files without *.test.ts or *.spec.ts counterpart
find src -name "*.ts" \
  ! -name "*.test.ts" \
  ! -name "*.spec.ts" \
  ! -name "*.d.ts" \
  ! -path "*/node_modules/*" \
  -type f
```

Check if `{file}.test.ts` or `__tests__/{file}.test.ts` exists.

### 🦀 Rust

```bash
# Rust source files — check if they contain #[cfg(test)]
find src -name "*.rs" -type f | while read f; do
  grep -q "#\[cfg(test)\]" "$f" || echo "$f (no tests)"
done
```

### 🐍 Python

```bash
# Python files without test_*.py counterpart
find . -name "*.py" \
  ! -name "test_*.py" \
  ! -name "*_test.py" \
  ! -path "*/tests/*" \
  ! -path "*/.venv/*" \
  -type f
```

Check for `tests/test_{filename}.py` or `test_{filename}.py` in same directory.

### 🐹 Go

```bash
# Go files without _test.go counterpart
find . -name "*.go" \
  ! -name "*_test.go" \
  ! -path "*/vendor/*" \
  -type f
```

Check if `{filename_without_ext}_test.go` exists in same directory.

---

## Step 4: Test generation patterns by platform

### 🍎 iOS / Swift — Swift Testing

**When to use Swift Testing vs XCTest**: Read `test_framework` from `platform-context.json`.
- `"swift-testing"` → use `@Test`, `@Suite`, `#expect`
- `"xctest"` → use `XCTestCase`, `func test*()`, `XCTAssert*`

Default for new files: always Swift Testing.

```swift
// Swift Testing pattern
import Testing
@testable import {ModuleName}

@Suite("{TypeName}")
struct {TypeName}Tests {

    @Test("does X when Y")
    func testBehavior() async throws {
        // Arrange
        let sut = {TypeName}(dep: Mock{Dep}())
        // Act
        let result = await sut.action()
        // Assert
        #expect(result == expectedValue)
    }

    @Test("handles failure gracefully")
    func testFailurePath() async {
        let sut = {TypeName}(dep: Mock{Dep}(shouldFail: true))
        let result = await sut.action()
        #expect(result == nil)
    }
}
```

Run: `swift test --parallel`

### 🟨 Node.js — Jest or Vitest

Detect from `platform-context.json → platforms[0].test_command`:
- Contains `jest` → Jest pattern
- Contains `vitest` → Vitest pattern (identical API, different imports)

```typescript
// Jest / Vitest pattern
import { {TypeName} } from '../{filename}'

describe('{TypeName}', () => {
  let sut: {TypeName}
  let mockDep: jest.Mocked<{DepType}>

  beforeEach(() => {
    mockDep = {
      method: jest.fn().mockResolvedValue(expectedValue),
    }
    sut = new {TypeName}(mockDep)
  })

  it('returns expected value when called with valid input', async () => {
    const result = await sut.action('valid-input')
    expect(result).toEqual(expectedValue)
    expect(mockDep.method).toHaveBeenCalledWith('valid-input')
  })

  it('throws error when dep fails', async () => {
    mockDep.method.mockRejectedValue(new Error('dep error'))
    await expect(sut.action('input')).rejects.toThrow('dep error')
  })
})
```

Run: `jest --findRelatedTests {modified_files}` or `vitest run`

### 🦀 Rust — inline #[cfg(test)]

Add tests inside the same file, at the bottom:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_action_returns_expected() {
        let result = action("input");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), expected_value);
    }

    #[test]
    fn test_action_fails_on_invalid_input() {
        let result = action("");
        assert!(result.is_err());
    }

    #[tokio::test]  // for async functions
    async fn test_async_action() {
        let result = async_action("input").await;
        assert!(result.is_ok());
    }
}
```

Run: `cargo test -- --nocapture`

### 🐍 Python — pytest

```python
# tests/test_{filename}.py
import pytest
from {module} import {TypeName}

class Test{TypeName}:
    def test_action_returns_expected(self, mock_dep):
        sut = {TypeName}(dep=mock_dep)
        result = sut.action("valid-input")
        assert result == expected_value

    def test_action_fails_on_invalid_input(self, mock_dep):
        mock_dep.method.side_effect = ValueError("invalid")
        sut = {TypeName}(dep=mock_dep)
        with pytest.raises(ValueError, match="invalid"):
            sut.action("")

    @pytest.mark.asyncio
    async def test_async_action(self, mock_dep):
        sut = {TypeName}(dep=mock_dep)
        result = await sut.async_action("input")
        assert result is not None
```

Run: `pytest tests/test_{filename}.py --tb=short -v`

### 🐹 Go — standard testing package

```go
// {filename}_test.go
package {package}

import (
    "testing"
)

func Test{TypeName}Action(t *testing.T) {
    t.Run("returns expected value for valid input", func(t *testing.T) {
        sut := New{TypeName}(mockDep)
        got, err := sut.Action("valid-input")
        if err != nil {
            t.Fatalf("unexpected error: %v", err)
        }
        if got != expectedValue {
            t.Errorf("got %q, want %q", got, expectedValue)
        }
    })

    t.Run("returns error for empty input", func(t *testing.T) {
        sut := New{TypeName}(mockDep)
        _, err := sut.Action("")
        if err == nil {
            t.Error("expected error for empty input, got nil")
        }
    })
}
```

Run: `go test ./... -v -run Test{TypeName}`

---

## Step 5: Test execution

After generating tests, run the full test suite for the platform:

| Platform | Command |
|----------|---------|
| iOS | `swift test --parallel` |
| Node.js (jest) | `jest --findRelatedTests {modified_files}` |
| Node.js (vitest) | `vitest run --reporter=verbose` |
| Rust | `cargo test -- --nocapture` |
| Python | `pytest --tb=short -v {test_files}` |
| Go | `go test ./... -v` |

## Step 6: Report

```markdown
## Test Only Mode — Results

**Platform:** iOS (Swift Package)
**Test framework:** Swift Testing

### Files analyzed
- PersonalTrainerViewModel.swift — had 0 tests → 5 tests generated
- ConnectTrainerUseCase.swift — had 0 tests → 3 tests generated
- TrainerRepository.swift — skipped (user declined)

### Test run
Running: swift test --parallel
✅ 8 passed, 0 failed

### Coverage delta
Before: 42% (estimated)
After: ~61% (estimated)
```

## iOS extra step: XcodeBuildMCP

After running `swift test`, if `capabilities.xcodebuildmcp_available == true`:

```
/xcodebuildmcp build_run_sim
→ ✅ App running on iPhone 16 Simulator (iOS 18.3)
or
→ ⚠️ Simulator build not attempted (XcodeBuildMCP not available)
```

This step is **always non-blocking**.

## /swift-testing skill integration (iOS only)

When `primary_platform == "ios"`, invoke the `/swift-testing` skill for enriched guidance:
- Test structure with `@Suite` and `@Test` annotations
- `#expect` / `#require` macro usage
- Async testing patterns
- Test organization and traits

For all other platforms, the Test Only skill provides built-in guidance without invoking an external skill.
