---
name: test
description: Use this skill when writing or running tests. Enforces rstest for parametrized tests and DRY test patterns. Use when creating new tests, fixing test failures, or improving test coverage.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(cargo test:*)
---

# Testing with rstest

This project uses rstest for DRY, parametrized tests.

## Running Tests

```bash
cargo test                     # Run all tests
cargo test <test_name>         # Run specific test
cargo test -- --nocapture      # Show stdout
```

## Coverage

Use cargo-llvm-cov to measure test coverage locally:

```bash
cargo llvm-cov                           # Run tests with coverage (text summary)
cargo llvm-cov --html                    # Generate HTML report in target/llvm-cov/html/
cargo llvm-cov --lcov --output-path lcov.info  # Generate LCOV format (used in CI)
```

Coverage is automatically measured and uploaded to Codecov in CI.

## Writing Tests

### Always prefer rstest over plain #[test]

Use `#[rstest]` with `#[case]` for multiple inputs:

```rust
use rstest::*;

#[rstest]
#[case::empty("", true)]
#[case::whitespace("   ", true)]
#[case::valid("hello", false)]
fn test_is_blank(#[case] input: &str, #[case] expected: bool) {
    assert_eq!(is_blank(input), expected);
}
```

### Use fixtures for shared setup

```rust
#[fixture]
fn repository() -> InMemoryRepository {
    let mut r = InMemoryRepository::default();
    // setup
    r
}

#[rstest]
fn test_find(repository: InMemoryRepository) {
    // repository is automatically injected
}
```

### Combine cases with values

```rust
#[rstest]
#[case::admin(User::Admin)]
#[case::guest(User::Guest)]
fn test_access(
    #[case] user: User,
    #[values("read", "write", "delete")] action: &str,
) {
    // Generates 6 tests: admin+read, admin+write, ...
}
```

### Use indoc for multiline test input

```rust
use indoc::indoc;

#[rstest]
#[case::with_frontmatter(
    indoc! {r#"
        ---
        title: "Test"
        ---
        Body content
    "#},
    "Test",
    "Body content\n"
)]
fn test_parse(#[case] input: &str, #[case] title: &str, #[case] body: &str) {
    let doc = parse(input);
    assert_eq!(doc.title, title);
    assert_eq!(doc.body, body);
}
```

## Test Naming

- Use `#[case::descriptive_name]` for named cases
- Test function: `test_<function>_<scenario>` or `should_<behavior>`

## DRY Principles

1. Extract common assertions into helper functions
2. Use fixtures for repeated setup
3. Parametrize similar tests with `#[case]`
4. Use `#[values]` for combinatorial testing
