---
name: testing-r-packages
description: >
  Best practices for writing R package tests using testthat version 3+. Use when writing, organizing, or improving tests for R packages. Covers test structure, expectations, fixtures, snapshots, mocking, and modern testthat 3 patterns including self-sufficient tests, proper cleanup with withr, and snapshot testing.
---

# Testing R Packages with testthat

Modern best practices for R package testing using testthat 3+.

## Initial Setup

Initialize testing with testthat 3rd edition:

```r
usethis::use_testthat(3)
```

This creates `tests/testthat/` directory, adds testthat to `DESCRIPTION` Suggests with `Config/testthat/edition: 3`, and creates `tests/testthat.R`.

## File Organization

**Mirror package structure:**
- Code in `R/foofy.R` → tests in `tests/testthat/test-foofy.R`
- Use `usethis::use_r("foofy")` and `usethis::use_test("foofy")` to create paired files

**Special files:**
- `helper-*.R` - Helper functions and custom expectations, sourced before tests
- `setup-*.R` - Run during `R CMD check` only, not during `load_all()`
- `fixtures/` - Static test data files accessed via `test_path()`

## Test Structure

Tests follow a three-level hierarchy: **File → Test → Expectation**

### Standard Syntax

```r
test_that("descriptive behavior", {
  result <- my_function(input)
  expect_equal(result, expected_value)
})
```

**Test descriptions** should read naturally and describe behavior, not implementation.

### BDD Syntax (describe/it)

For behavior-driven development, use `describe()` and `it()`:

```r
describe("matrix()", {
  it("can be multiplied by a scalar", {
    m1 <- matrix(1:4, 2, 2)
    m2 <- m1 * 2
    expect_equal(matrix(1:4 * 2, 2, 2), m2)
  })

  it("can be transposed", {
    m <- matrix(1:4, 2, 2)
    expect_equal(t(m), matrix(c(1, 3, 2, 4), 2, 2))
  })
})
```

**Key features:**
- `describe()` groups related specifications for a component
- `it()` defines individual specifications (like `test_that()`)
- Supports nesting for hierarchical organization
- `it()` without code creates pending test placeholders

**Use `describe()` to verify you implement the right things, use `test_that()` to ensure you do things right.**

See [references/bdd.md](references/bdd.md) for comprehensive BDD patterns, nested specifications, and test-first workflows.

## Running Tests

Three scales of testing:

**Micro** (interactive development):
```r
devtools::load_all()
expect_equal(foofy(...), expected)
```

**Mezzo** (single file):
```r
testthat::test_file("tests/testthat/test-foofy.R")
# RStudio: Ctrl/Cmd + Shift + T
```

**Macro** (full suite):
```r
devtools::test()    # Ctrl/Cmd + Shift + T
devtools::check()   # Ctrl/Cmd + Shift + E
```

## Core Expectations

### Equality

```r
expect_equal(10, 10 + 1e-7)      # Allows numeric tolerance
expect_identical(10L, 10L)       # Exact match required
expect_all_equal(x, expected)    # Every element matches (v3.3.0+)
```

### Errors, Warnings, Messages

```r
expect_error(1 / "a")
expect_error(bad_call(), class = "specific_error_class")
expect_no_error(valid_call())

expect_warning(deprecated_func())
expect_no_warning(safe_func())

expect_message(informative_func())
expect_no_message(quiet_func())
```

### Pattern Matching

```r
expect_match("Testing is fun!", "Testing")
expect_match(text, "pattern", ignore.case = TRUE)
```

### Structure and Type

```r
expect_length(vector, 10)
expect_type(obj, "list")
expect_s3_class(model, "lm")
expect_s4_class(obj, "MyS4Class")
expect_r6_class(obj, "MyR6Class")      # v3.3.0+
expect_shape(matrix, c(10, 5))         # v3.3.0+
```

### Sets and Collections

```r
expect_setequal(x, y)           # Same elements, any order
expect_contains(fruits, "apple") # Subset check (v3.2.0+)
expect_in("apple", fruits)       # Element in set (v3.2.0+)
expect_disjoint(set1, set2)      # No overlap (v3.3.0+)
```

### Logical

```r
expect_true(condition)
expect_false(condition)
expect_all_true(vector > 0)      # All elements TRUE (v3.3.0+)
expect_all_false(vector < 0)     # All elements FALSE (v3.3.0+)
```

## Design Principles

### 1. Self-Sufficient Tests

Each test should contain all setup, execution, and teardown code:

```r
# Good: self-contained
test_that("foofy() works", {
  data <- data.frame(x = 1:3, y = letters[1:3])
  result <- foofy(data)
  expect_equal(result$x, 1:3)
})

# Bad: relies on ambient state
dat <- data.frame(x = 1:3, y = letters[1:3])
test_that("foofy() works", {
  result <- foofy(dat)  # Where did 'dat' come from?
  expect_equal(result$x, 1:3)
})
```

### 2. Self-Contained Tests (Cleanup Side Effects)

Use `withr` to manage state changes:

```r
test_that("function respects options", {
  withr::local_options(my_option = "test_value")
  withr::local_envvar(MY_VAR = "test")
  withr::local_package("jsonlite")

  result <- my_function()
  expect_equal(result$setting, "test_value")
  # Automatic cleanup after test
})
```

**Common withr functions:**
- `local_options()` - Temporarily set options
- `local_envvar()` - Temporarily set environment variables
- `local_tempfile()` - Create temp file with automatic cleanup
- `local_tempdir()` - Create temp directory with automatic cleanup
- `local_package()` - Temporarily attach package

### 3. Plan for Test Failure

Write tests assuming they will fail and need debugging:
- Tests should run independently in fresh R sessions
- Avoid hidden dependencies on earlier tests
- Make test logic explicit and obvious

### 4. Repetition is Acceptable

Repeat setup code in tests rather than factoring it out. Test clarity is more important than avoiding duplication.

### 5. Use `devtools::load_all()` Workflow

During development:
- Use `devtools::load_all()` instead of `library()`
- Makes all functions available (including unexported)
- Automatically attaches testthat
- Eliminates need for `library()` calls in tests

## Snapshot Testing

For complex output that's difficult to verify programmatically, use snapshot tests. See [references/snapshots.md](references/snapshots.md) for complete guide.

**Basic pattern:**

```r
test_that("error message is helpful", {
  expect_snapshot(
    error = TRUE,
    validate_input(NULL)
  )
})
```

Snapshots stored in `tests/testthat/_snaps/`.

**Workflow:**
```r
devtools::test()                    # Creates new snapshots
testthat::snapshot_review('name')   # Review changes
testthat::snapshot_accept('name')   # Accept changes
```

## Test Fixtures and Data

Three approaches for test data:

**1. Constructor functions** - Create data on-demand:
```r
new_sample_data <- function(n = 10) {
  data.frame(id = seq_len(n), value = rnorm(n))
}
```

**2. Local functions with cleanup** - Handle side effects:
```r
local_temp_csv <- function(data, env = parent.frame()) {
  path <- withr::local_tempfile(fileext = ".csv", .local_envir = env)
  write.csv(data, path, row.names = FALSE)
  path
}
```

**3. Static fixture files** - Store in `fixtures/` directory:
```r
data <- readRDS(test_path("fixtures", "sample_data.rds"))
```

See [references/fixtures.md](references/fixtures.md) for detailed fixture patterns.

## Mocking

Replace external dependencies during testing using `local_mocked_bindings()`. See [references/mocking.md](references/mocking.md) for comprehensive mocking strategies.

**Basic pattern:**

```r
test_that("function works with mocked dependency", {
  local_mocked_bindings(
    external_api = function(...) list(status = "success", data = "mocked")
  )

  result <- my_function_that_calls_api()
  expect_equal(result$status, "success")
})
```

## Common Patterns

### Testing Errors with Specific Classes

```r
test_that("validation catches errors", {
  expect_error(
    validate_input("wrong_type"),
    class = "vctrs_error_cast"
  )
})
```

### Testing with Temporary Files

```r
test_that("file processing works", {
  temp_file <- withr::local_tempfile(
    lines = c("line1", "line2", "line3")
  )

  result <- process_file(temp_file)
  expect_equal(length(result), 3)
})
```

### Testing with Modified Options

```r
test_that("output respects width", {
  withr::local_options(width = 40)

  output <- capture_output(print(my_object))
  expect_lte(max(nchar(strsplit(output, "\n")[[1]])), 40)
})
```

### Testing Multiple Related Cases

```r
test_that("str_trunc() handles all directions", {
  trunc <- function(direction) {
    str_trunc("This string is moderately long", direction, width = 20)
  }

  expect_equal(trunc("right"), "This string is mo...")
  expect_equal(trunc("left"), "...erately long")
  expect_equal(trunc("center"), "This stri...ely long")
})
```

### Custom Expectations in Helper Files

```r
# In tests/testthat/helper-expectations.R
expect_valid_user <- function(user) {
  expect_type(user, "list")
  expect_named(user, c("id", "name", "email"))
  expect_type(user$id, "integer")
  expect_match(user$email, "@")
}

# In test file
test_that("user creation works", {
  user <- create_user("test@example.com")
  expect_valid_user(user)
})
```

## File System Discipline

**Always write to temp directory:**

```r
# Good
output <- withr::local_tempfile(fileext = ".csv")
write.csv(data, output)

# Bad - writes to package directory
write.csv(data, "output.csv")
```

**Access test fixtures with `test_path()`:**

```r
# Good - works in all contexts
data <- readRDS(test_path("fixtures", "data.rds"))

# Bad - relative paths break
data <- readRDS("fixtures/data.rds")
```

## Advanced Topics

For advanced testing scenarios, see:

- **[references/bdd.md](references/bdd.md)** - BDD-style testing with describe/it, nested specifications, test-first workflows
- **[references/snapshots.md](references/snapshots.md)** - Snapshot testing, transforms, variants
- **[references/mocking.md](references/mocking.md)** - Mocking strategies, webfakes, httptest2
- **[references/fixtures.md](references/fixtures.md)** - Fixture patterns, database fixtures, helper files
- **[references/advanced.md](references/advanced.md)** - Skipping tests, secrets management, CRAN requirements, custom expectations, parallel testing

## testthat 3 Modernizations

When working with testthat 3 code, prefer modern patterns:

**Deprecated → Modern:**
- `context()` → Remove (duplicates filename)
- `expect_equivalent()` → `expect_equal(ignore_attr = TRUE)`
- `with_mock()` → `local_mocked_bindings()`
- `is_null()`, `is_true()`, `is_false()` → `expect_null()`, `expect_true()`, `expect_false()`

**New in testthat 3:**
- Edition system (`Config/testthat/edition: 3`)
- Improved snapshot testing
- `waldo::compare()` for better diff output
- Unified condition handling
- `local_mocked_bindings()` works with byte-compiled code
- Parallel test execution support

## Quick Reference

**Initialize:** `usethis::use_testthat(3)`

**Run tests:** `devtools::test()` or Ctrl/Cmd + Shift + T

**Create test file:** `usethis::use_test("name")`

**Review snapshots:** `testthat::snapshot_review()`

**Accept snapshots:** `testthat::snapshot_accept()`

**Find slow tests:** `devtools::test(reporter = "slow")`

**Shuffle tests:** `devtools::test(shuffle = TRUE)`
