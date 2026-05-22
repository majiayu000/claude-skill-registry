---
name: bash-testing
description: 'This skill should be used when the user asks to "test bash script", "write shell tests", "use shunit2", "use shellspec", "create test suite for bash", or mentions unit testing, test frameworks, mocking, or test-driven development for shell scripts.'
---

# Bash Testing

Testing frameworks and patterns for shell scripts, focusing on shunit2 and shellspec.

## Framework Selection

| Framework     | Strengths                     | Best For                      |
| ------------- | ----------------------------- | ----------------------------- |
| **shunit2**   | xUnit style, simple, portable | Unit tests, function testing  |
| **shellspec** | BDD style, modern, extensive  | Behavior specs, full projects |

## shunit2

### Installation

```bash
# Download directly
curl -L https://github.com/kward/shunit2/raw/master/shunit2 -o shunit2

# Or via package manager
apt install shunit2
brew install shunit2
```

### Basic Test Structure

```bash
#!/usr/bin/env bash

# Source the script being tested
source ./my_script.sh

# Test functions start with test
test_addition() {
    result=$(add 2 3)
    assertEquals "2 + 3 should equal 5" "5" "$result"
}

test_string_output() {
    result=$(greet "World")
    assertEquals "Hello, World" "$result"
}

test_file_creation() {
    create_temp_file
    assertTrue "Temp file should exist" "[ -f /tmp/testfile ]"
}

test_exit_code() {
    validate_input "valid"
    assertEquals "Should return 0 for valid input" 0 $?
}

# Setup and teardown
oneTimeSetUp() {
    # Run once before all tests
    export TEST_DIR=$(mktemp -d)
}

oneTimeTearDown() {
    # Run once after all tests
    rm -rf "$TEST_DIR"
}

setUp() {
    # Run before each test
    cd "$TEST_DIR"
}

tearDown() {
    # Run after each test
    rm -f "$TEST_DIR"/*
}

# Load shunit2
source shunit2
```

### shunit2 Assertions

```bash
# Equality
assertEquals [message] expected actual
assertNotEquals [message] unexpected actual

# Null/Empty
assertNull [message] value
assertNotNull [message] value

# Boolean/Status
assertTrue [message] condition
assertFalse [message] condition

# Same reference (string comparison)
assertSame [message] expected actual
assertNotSame [message] unexpected actual

# Contains (in string)
assertContains [message] container content

# Exit status
assertEquals 0 $?
```

### Testing Functions in Isolation

```bash
#!/usr/bin/env bash

# my_functions.sh
calculate_sum() {
    local -i sum=0
    for num in "$@"; do
        sum+=num
    done
    echo "$sum"
}

validate_email() {
    [[ "$1" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$ ]]
}
```

```bash
#!/usr/bin/env bash
# test_my_functions.sh

source ./my_functions.sh

test_calculate_sum_empty() {
    result=$(calculate_sum)
    assertEquals "Empty sum should be 0" "0" "$result"
}

test_calculate_sum_single() {
    result=$(calculate_sum 5)
    assertEquals "5" "$result"
}

test_calculate_sum_multiple() {
    result=$(calculate_sum 1 2 3 4 5)
    assertEquals "15" "$result"
}

test_validate_email_valid() {
    validate_email "test@example.com"
    assertTrue "Valid email should pass" $?
}

test_validate_email_invalid() {
    validate_email "not-an-email"
    assertFalse "Invalid email should fail" $?
}

source shunit2
```

## shellspec

### Installation

```bash
# Via curl
curl -fsSL https://git.io/shellspec | sh

# Via Homebrew
brew install shellspec

# Via package managers
apt install shellspec
```

### Directory Structure

```
project/
├── lib/
│   └── functions.sh
├── spec/
│   ├── spec_helper.sh
│   ├── functions_spec.sh
│   └── support/
│       └── fixtures/
└── .shellspec
```

### Configuration (.shellspec)

```
--require spec_helper
--format documentation
--color
```

### Basic Spec Structure

```bash
# spec/functions_spec.sh

Describe 'calculate_sum'
  Include lib/functions.sh

  It 'returns 0 for no arguments'
    When call calculate_sum
    The output should eq "0"
    The status should be success
  End

  It 'sums multiple numbers'
    When call calculate_sum 1 2 3 4 5
    The output should eq "15"
  End
End

Describe 'validate_email'
  Include lib/functions.sh

  It 'accepts valid email'
    When call validate_email "test@example.com"
    The status should be success
  End

  It 'rejects invalid email'
    When call validate_email "not-an-email"
    The status should be failure
  End

  Parameters
    "user@domain.com"    success
    "user.name@sub.domain.org" success
    "invalid"            failure
    "@nodomain.com"      failure
  End

  Example "validates $1"
    When call validate_email "$1"
    The status should be "$2"
  End
End
```

### shellspec Matchers

```bash
# Output matchers
The output should eq "exact match"
The output should include "partial"
The output should start with "prefix"
The output should end with "suffix"
The output should match pattern "*glob*"
The output should be blank

# Status matchers
The status should be success    # exit 0
The status should be failure    # exit non-zero
The status should eq 1          # specific code

# Variable matchers
The variable VAR should eq "value"
The variable VAR should be defined
The variable VAR should be undefined

# File matchers
The file "path" should be exist
The file "path" should be file
The file "path" should be directory
The file "path" should be readable

# Path matchers
The path "file.txt" should be exist
```

### Mocking in shellspec

```bash
Describe 'deploy function'
  # Mock external command
  curl() {
    echo "mocked response"
    return 0
  }

  It 'calls API endpoint'
    When call deploy "server"
    The output should include "mocked response"
  End
End

Describe 'file operations'
  # Mock with function override
  Mock rm
    echo "rm called with: $*"
  End

  It 'attempts to remove file'
    When call cleanup_temp
    The output should include "rm called with"
  End
End
```

### Spec Helper

```bash
# spec/spec_helper.sh

# Load common functions
spec_helper_precheck() {
  minimum_version "0.28.0"
}

spec_helper_loaded() {
  # Set up test environment
  export TEST_MODE=true
}

spec_helper_configure() {
  # Import project functions
  import 'lib/functions.sh'
}
```

## Testing Patterns

### Testing Exit Codes

```bash
# shunit2
test_success_exit() {
    run_command "valid_input"
    assertEquals 0 $?
}

test_error_exit() {
    run_command "invalid_input"
    assertEquals 1 $?
}

# shellspec
It 'exits 0 on success'
  When call run_command "valid_input"
  The status should eq 0
End
```

### Testing stdout and stderr

```bash
# shunit2
test_stdout() {
    result=$(my_function 2>/dev/null)
    assertEquals "expected output" "$result"
}

test_stderr() {
    error=$(my_function 2>&1 >/dev/null)
    assertContains "$error" "error message"
}

# shellspec
It 'outputs to stdout'
  When call my_function
  The stdout should eq "expected output"
End

It 'outputs error to stderr'
  When call my_function
  The stderr should include "error message"
End
```

### Testing with Fixtures

```bash
# Setup test fixtures
setUp() {
    TEST_DIR=$(mktemp -d)
    cat > "$TEST_DIR/config.json" <<EOF
{
    "key": "value"
}
EOF
}

tearDown() {
    rm -rf "$TEST_DIR"
}

test_config_parsing() {
    result=$(parse_config "$TEST_DIR/config.json")
    assertEquals "value" "$result"
}
```

### Testing Interactive Functions

```bash
# Provide input via heredoc
test_interactive() {
    result=$(my_prompt <<EOF
yes
EOF
)
    assertEquals "confirmed" "$result"
}

# Or use printf
test_with_input() {
    result=$(printf 'yes\n' | my_prompt)
    assertEquals "confirmed" "$result"
}
```

## Running Tests

```bash
# shunit2
./test_script.sh

# shellspec
shellspec                    # Run all specs
shellspec spec/file_spec.sh  # Run specific spec
shellspec --format tap       # TAP output
shellspec --jobs 4           # Parallel execution
```

## Best Practices

1. **One assertion per test** when practical
2. **Descriptive test names** explaining what's tested
3. **Isolate tests** - no dependencies between tests
4. **Test edge cases** - empty input, special characters, large data
5. **Clean up resources** in tearDown
6. **Mock external commands** - don't test curl, test your logic
7. **Test exit codes** not just output
