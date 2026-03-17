---
name: ExUnit Test Framework
description: Execute and generate ExUnit tests for Elixir projects with setup callbacks, describe blocks, and async testing support
version: 1.0.0
---

# ExUnit Test Framework

## Purpose

Provide ExUnit test execution and generation for Elixir projects, supporting:
- Test file generation from templates (_test.exs files)
- Test execution with Mix test integration
- Setup and setup_all callbacks
- Describe blocks for test organization
- Async testing support

## Usage

### Generate Test File

Create a test file from a bug report or feature description:

```bash
elixir generate-test.exs \
  --source lib/calculator.ex \
  --output test/calculator_test.exs \
  --module Calculator \
  --description "Division by zero error"
```

### Execute Tests

Run ExUnit tests and return structured results:

```bash
elixir run-test.exs \
  --file test/calculator_test.exs \
  --format json
```

## Command Line Options

### generate-test.exs

- `--source <path>` - Source file to test (required)
- `--output <path>` - Output test file path (required)
- `--module <name>` - Module name to test (required)
- `--description <text>` - Bug description or test purpose
- `--async` - Enable async testing (default: false)

### run-test.exs

- `--file <path>` - Test file to execute (required)
- `--format <json|doc>` - Output format (default: json)
- `--trace` - Run with detailed trace

## Output Format

### Test Generation

Returns JSON with generated test file information:

```json
{
  "success": true,
  "testFile": "test/calculator_test.exs",
  "testCount": 1,
  "template": "unit-test",
  "async": false
}
```

### Test Execution

Returns JSON with test results:

```json
{
  "success": false,
  "passed": 2,
  "failed": 1,
  "total": 3,
  "duration": 0.234,
  "failures": [
    {
      "test": "test divide by zero raises ArithmeticError",
      "error": "Expected ArithmeticError to be raised",
      "file": "test/calculator_test.exs",
      "line": 15
    }
  ]
}
```

## ExUnit Test Structure

### Basic Test

```elixir
defmodule CalculatorTest do
  use ExUnit.Case

  test "adds two numbers" do
    assert Calculator.add(1, 2) == 3
  end
end
```

### With Describe Blocks

```elixir
defmodule CalculatorTest do
  use ExUnit.Case

  describe "add/2" do
    test "adds positive numbers" do
      assert Calculator.add(1, 2) == 3
    end

    test "adds negative numbers" do
      assert Calculator.add(-1, -2) == -3
    end
  end

  describe "divide/2" do
    test "divides numbers" do
      assert Calculator.divide(6, 2) == 3
    end

    test "raises on division by zero" do
      assert_raise ArithmeticError, fn ->
        Calculator.divide(1, 0)
      end
    end
  end
end
```

### With Setup Callbacks

```elixir
defmodule UserTest do
  use ExUnit.Case

  setup do
    user = %User{name: "John", email: "john@example.com"}
    {:ok, user: user}
  end

  test "user has name", %{user: user} do
    assert user.name == "John"
  end

  test "user has email", %{user: user} do
    assert user.email == "john@example.com"
  end
end
```

### Async Testing

```elixir
defmodule FastTest do
  use ExUnit.Case, async: true

  test "runs in parallel with other async tests" do
    assert 1 + 1 == 2
  end
end
```

## Common Assertions

- `assert expr` - Ensures expression is truthy
- `refute expr` - Ensures expression is falsy
- `assert_raise Exception, fn -> ... end` - Expects exception
- `assert_received message` - Asserts message was received
- `assert x == y` - Equality assertion (preferred over pattern matching)

## Integration with deep-debugger

The deep-debugger agent uses this skill for Elixir projects:

1. **Test Recreation**: Generate failing test from bug report
2. **Test Validation**: Execute test to verify it fails consistently
3. **Fix Verification**: Re-run test after fix to ensure it passes

Example workflow:
```markdown
1. deep-debugger receives bug report for Elixir project
2. Invokes test-detector to identify ExUnit
3. Invokes exunit-test/generate-test.exs to create failing test
4. Invokes exunit-test/run-test.exs to validate test fails
5. Delegates fix to elixir-phoenix-expert agent
6. Invokes exunit-test/run-test.exs to verify fix
```

## Dependencies

Requires Elixir and Mix to be installed:

```bash
elixir --version  # Should be 1.12 or higher
mix --version     # Elixir's build tool
```

ExUnit is built into Elixir, no additional installation needed.

## File Naming Conventions

- Test files must end with `_test.exs`
- Mirror source file structure: `lib/calculator.ex` → `test/calculator_test.exs`
- Test helper: `test/test_helper.exs` (required)

## Error Handling

### Test Generation Errors

```json
{
  "success": false,
  "error": "Source file not found",
  "file": "lib/missing.ex"
}
```

### Test Execution Errors

```json
{
  "success": false,
  "error": "Mix test failed",
  "output": "** (CompileError) ..."
}
```

## See Also

- [ExUnit Documentation](https://hexdocs.pm/ex_unit/ExUnit.html)
- [Elixir School Testing Guide](https://elixirschool.com/en/lessons/testing/basics)
- [templates/](templates/) - Test file templates
