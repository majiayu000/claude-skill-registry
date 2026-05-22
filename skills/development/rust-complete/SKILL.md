---
id: rust-complete
name: Complete Rust Development
description: >-
  A comprehensive skill for Rust development that combines error handling,
  testing, and logging patterns. Demonstrates the 'includes' composition
  feature by merging content from multiple standalone skills.
tags: [rust, complete, example]
includes:
  - skill: rust-error-handling
    into: rules
  - skill: testing-patterns
    into: checklist
  - skill: logging-patterns
    into: rules
    prefix: "[Logging] "
---

# Complete Rust Development

A comprehensive Rust development skill that combines error handling, testing,
and logging patterns through composition.

This skill demonstrates the `includes` feature:
- Error handling rules from `rust-error-handling` are merged into Rules
- Testing checklist from `testing-patterns` is merged into Checklist
- Logging rules from `logging-patterns` are merged into Rules with a prefix

## Rules

- Follow Rust idioms and conventions
- Use `clippy` for linting: `cargo clippy -- -D warnings`
- Format code with `rustfmt`: `cargo fmt`
- Keep unsafe blocks minimal and well-documented

## Examples

```rust
// Idiomatic Rust with proper error handling, logging, and tests
use anyhow::{Context, Result};
use tracing::{info, instrument};

#[instrument]
pub fn process_data(input: &str) -> Result<Output> {
    info!("processing data");

    let parsed = parse_input(input)
        .context("failed to parse input")?;

    let result = transform(parsed)
        .context("transformation failed")?;

    info!(output_size = result.len(), "processing complete");
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_data_happy_path() {
        let input = "valid input";
        let result = process_data(input);
        assert!(result.is_ok());
    }

    #[test]
    fn test_process_data_invalid_input() {
        let input = "";
        let result = process_data(input);
        assert!(result.is_err());
    }
}
```

## Checklist

- [ ] Code passes `cargo clippy -- -D warnings`
- [ ] Code is formatted with `cargo fmt`
- [ ] No `unsafe` blocks (or they are justified and documented)
- [ ] Dependencies are minimal and audited
