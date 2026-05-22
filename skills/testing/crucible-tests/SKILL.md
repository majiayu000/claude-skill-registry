---
name: crucible-tests
description: Write unit tests using the Crucible test framework for Lean 4 projects. Use when creating tests, adding test files, or when the user mentions Crucible, unit tests, or testing Lean code.
---

# Crucible Test Framework

Crucible is a lightweight test framework for Lean 4 used across this workspace.

## Quick Start

```lean
import Crucible
import MyProject  -- Import the code being tested

namespace MyProjectTests.ModuleTests

open Crucible
open MyProject

testSuite "Module Name"

test "descriptive test name" := do
  actualValue ≡ expectedValue

test "another test" := do
  someOption ≡? expectedValue  -- Option assertion

#generate_tests

end MyProjectTests.ModuleTests
```

## Test Runner (Tests/Main.lean)

```lean
import Crucible
import MyProjectTests.ModuleTests
-- import all test modules

open Crucible

def main : IO UInt32 := runAllSuites
```

## Assertions

### Core Assertions

| Syntax | Function | Description |
|--------|----------|-------------|
| `a ≡ b` | `shouldBe a b` | Assert equality |
| `opt ≡? val` | `shouldBeSome opt val` | Assert Option contains value |
| | `shouldBeNone opt` | Assert Option is none |
| | `shouldSatisfy cond msg` | Assert condition is true |
| | `shouldMatch val pred desc` | Assert value satisfies predicate |
| | `shouldBeNear a b eps` | Assert floats approximately equal (default eps: 0.0001) |
| | `ensure cond msg` | Throw if condition false |

### Collection Assertions

| Function | Description |
|----------|-------------|
| `shouldHaveLength list n` | Assert list has length n |
| `shouldContain list elem` | Assert list contains element |
| `shouldContainAll list elems` | Assert list contains all elements |
| `shouldBeEmpty list` | Assert list is empty |
| `shouldNotBeEmpty list` | Assert list is not empty |

### String Assertions

| Function | Description |
|----------|-------------|
| `shouldStartWith str prefix` | Assert string starts with prefix |
| `shouldEndWith str suffix` | Assert string ends with suffix |
| `shouldContainSubstr str sub` | Assert string contains substring |

### Exception Assertions

| Function | Description |
|----------|-------------|
| `shouldThrow action` | Assert action throws any exception |
| `shouldThrowWith action substr` | Assert action throws with message containing substring |
| `shouldThrowMatching action pred` | Assert action throws matching predicate |
| `shouldNotThrow action` | Assert action completes without throwing |

### Comparison Assertions

| Function | Description |
|----------|-------------|
| `shouldBeBetween val min max` | Assert value is in range (inclusive) |

### Assertion Context

| Function | Description |
|----------|-------------|
| `withContext assertion msg` | Add context to error messages |
| `withMessage msg assertion` | Replace error message on failure |

## Test Fixtures (Setup/Teardown)

Use fixture hooks for shared setup and cleanup:

```lean
testSuite "Database Tests"

-- Runs once before all tests in the suite
beforeAll := do
  IO.println "Connecting to database..."

-- Runs once after all tests (even if tests fail)
afterAll := do
  IO.println "Closing database connection..."

-- Runs before each individual test
beforeEach := do
  IO.println "Starting transaction..."

-- Runs after each individual test (even if test fails)
afterEach := do
  IO.println "Rolling back transaction..."

test "insert works" := do
  -- database is set up, transaction started
  ...

test "query works" := do
  -- fresh transaction for this test
  ...

#generate_tests
```

### Hook Behavior

| Hook | When it runs | On failure |
|------|--------------|------------|
| `beforeAll` | Once before first test | Skips all tests in suite |
| `afterAll` | Once after last test | Always runs (errors logged) |
| `beforeEach` | Before each test | Test fails |
| `afterEach` | After each test | Always runs (errors logged) |

### Hooks are Optional

You can define any combination of hooks - they're all optional:

```lean
testSuite "Simple Tests"

-- Only define beforeEach if you need per-test setup
beforeEach := do
  resetGlobalState

test "test 1" := ...
test "test 2" := ...

#generate_tests
```

## Timeouts and Retries

```lean
-- Per-test timeout (milliseconds)
test "slow operation" (timeout := 5000) := do
  slowFunction

-- Per-test retry count
test "flaky test" (retry := 3) := do
  flakyOperation

-- Both
test "network call" (timeout := 2000) (retry := 2) := do
  networkOperation

-- Global defaults in runner
def main : IO UInt32 := runAllSuites (timeout := 10000) (retry := 1)
```

## Test File Structure

```
MyProject/
  lakefile.lean      # Add: lean_exe tests where root := "Tests/Main.lean"
  Tests/
    Main.lean        # Test runner with runAllSuites
    Core.lean        # Tests for Core module
    Parser.lean      # Tests for Parser module
```

### lakefile.lean

```lean
require crucible from git "https://github.com/nathanial/crucible" @ "master"

@[default_target]
lean_lib MyProject

lean_exe tests where
  root := `Tests.Main
```

## Common Patterns

### Multiple assertions in one test
```lean
test "constructor preserves values" := do
  let obj := MyType.mk 1 "hello"
  obj.id ≡ 1
  obj.name ≡ "hello"
```

### Testing IO operations
```lean
test "file operations" := do
  let content ← IO.FS.readFile "test.txt"
  content.length ≡ 42
```

### Custom helper for domain-specific assertions
```lean
def colorApproxEq (c1 c2 : Color) (eps : Float := 0.001) : Bool :=
  floatNear c1.r c2.r eps && floatNear c1.g c2.g eps

test "color interpolation" := do
  let c := Color.lerp Color.red Color.blue 0.5
  ensure (colorApproxEq c expectedColor) "colors should match"
```

### Testing error conditions
```lean
-- Simple: just verify it throws
test "throws on invalid input" := do
  shouldThrow (riskyOperation (-1))

-- Verify error message contains expected text
test "error message is descriptive" := do
  shouldThrowWith (parseNumber "abc") "invalid number"

-- Custom predicate for complex error checking
test "specific error type" := do
  shouldThrowMatching (networkCall) fun msg => msg.startsWith "NetworkError"

-- Verify operation succeeds (doesn't throw)
test "valid input succeeds" := do
  shouldNotThrow (parseNumber "42")
```

### Adding context to assertions
```lean
test "user validation" := do
  let user := fetchUser "alice"
  (user.age ≡ 25) |> withContext "checking user age"
  (user.name ≡ "Alice") |> withContext "checking user name"
  (user.email ≡ "alice@example.com") |> withContext "checking email"
```

### Multiple test suites in one file
```lean
namespace Tests.Core
testSuite "Core Types"
test "test 1" := ...
#generate_tests
end Tests.Core

namespace Tests.Parser
testSuite "Parser"
test "test 2" := ...
#generate_tests
end Tests.Parser
```

### Organizing tests with section comments
```lean
testSuite "MyModule"

/-! ## Constructor Tests -/

test "default constructor" := ...
test "custom constructor" := ...

/-! ## Method Tests -/

test "method returns correct value" := ...

#generate_tests
```

## Float Comparisons

Use `floatNear` (from Crucible) or `shouldBeNear` for floating point:

```lean
test "float calculation" := do
  let result := computePi
  shouldBeNear result 3.14159 0.00001
  -- or
  ensure (floatNear result 3.14159 0.00001) "pi approximation"
```

## Running Tests

```bash
lake build tests && .lake/build/bin/tests
# or
lake test  # if configured in lakefile.lean
```
