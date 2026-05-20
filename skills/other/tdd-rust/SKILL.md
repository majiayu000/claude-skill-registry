---
name: tdd-rust
description: Test-Driven Development workflow for Rust - write test first, watch it fail, implement minimal code
invocation_pattern: "^/(tdd|test-first)\\b"
---

# TDD Workflow for Rust Projects

Enforce strict Test-Driven Development: **Red → Green → Refactor**

## Workflow Steps

### 1. RED: Write failing test first

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_session_metadata() {
        let path = Path::new("tests/fixtures/session.jsonl");
        let metadata = extract_metadata(path).unwrap();

        assert_eq!(metadata.message_count, 42);
        assert!(metadata.first_timestamp < metadata.last_timestamp);
    }
}
```

**Run test to verify failure:**
```bash
cargo test test_parse_session_metadata
# Expected: FAILED (function doesn't exist yet)
```

### 2. GREEN: Implement minimal code to pass

```rust
pub fn extract_metadata(path: &Path) -> anyhow::Result<SessionMetadata> {
    // Minimal implementation
    Ok(SessionMetadata {
        message_count: 42, // Hardcoded for first pass
        first_timestamp: Utc::now(),
        last_timestamp: Utc::now(),
        // ...
    })
}
```

**Run test again:**
```bash
cargo test test_parse_session_metadata
# Expected: PASSED
```

### 3. REFACTOR: Improve implementation

```rust
pub fn extract_metadata(path: &Path) -> anyhow::Result<SessionMetadata> {
    let file = File::open(path).context("Failed to open session file")?;
    let reader = BufReader::new(file);

    let mut first_line: Option<SessionLine> = None;
    let mut last_line: Option<SessionLine> = None;
    let mut count = 0;

    for line in reader.lines() {
        let line = line?;
        if let Ok(parsed) = serde_json::from_str::<SessionLine>(&line) {
            if first_line.is_none() {
                first_line = Some(parsed.clone());
            }
            last_line = Some(parsed);
            count += 1;
        }
    }

    Ok(SessionMetadata {
        message_count: count,
        first_timestamp: first_line.map(|l| l.timestamp).unwrap_or_else(Utc::now),
        last_timestamp: last_line.map(|l| l.timestamp).unwrap_or_else(Utc::now),
        // ...
    })
}
```

**Final verification:**
```bash
cargo test test_parse_session_metadata
cargo clippy --all-targets
```

## Test Organization

### Unit Tests (embedded in module)
```rust
// src/parsers/session_index.rs
pub fn extract_metadata(path: &Path) -> anyhow::Result<SessionMetadata> {
    // Implementation
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_metadata_valid_file() {
        // Test happy path
    }

    #[test]
    fn test_extract_metadata_malformed_lines() {
        // Test error handling
    }
}
```

### Integration Tests (tests/ directory)
```rust
// tests/integration_test.rs
use ccboard_core::store::DataStore;

#[tokio::test]
async fn test_initial_load() {
    let store = DataStore::new();
    let report = store.initial_load().await.unwrap();
    assert!(report.stats_loaded);
}
```

## Fixtures Management

Store sanitized test data in `tests/fixtures/`:
```
tests/
├─ fixtures/
│  ├─ stats-cache.json
│  ├─ session.jsonl
│  ├─ settings.json
│  └─ agent.md
└─ integration_test.rs
```

Load fixtures in tests:
```rust
#[test]
fn test_parse_stats() {
    let fixture = include_str!("../tests/fixtures/stats-cache.json");
    let stats: StatsCache = serde_json::from_str(fixture).unwrap();
    assert!(stats.total_input_tokens > 0);
}
```

## Async Tests

```rust
use tokio::test;

#[tokio::test]
async fn test_parallel_session_scan() {
    let store = DataStore::new();

    // Test concurrent operations
    let tasks = vec![
        store.reload_stats(),
        store.update_session(path),
    ];

    let results = futures::future::join_all(tasks).await;
    // Assertions
}
```

## Property-Based Testing (Optional)

```toml
# Cargo.toml
[dev-dependencies]
proptest = "1"
```

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_session_parse_never_panics(s in "\\PC*") {
        // Should handle any input without panicking
        let _ = serde_json::from_str::<SessionLine>(&s);
    }
}
```

## Pre-Commit Checklist

Before EVERY commit:
```bash
cargo fmt --all              # Format code
cargo clippy --all-targets   # Lint
cargo test --all             # All tests pass
```

## Command Shortcuts

```bash
# Run specific test
cargo test test_name

# Run tests with output
cargo test -- --nocapture

# Run tests in module
cargo test parsers::

# Watch mode
cargo watch -x test

# Coverage (requires cargo-tarpaulin)
cargo tarpaulin --out Html
```

## Anti-Patterns

❌ **DON'T** skip the RED phase (test must fail first)
❌ **DON'T** write implementation before test
❌ **DON'T** use `.unwrap()` in tests - use `.expect("meaningful message")`
❌ **DON'T** commit without running tests

✅ **DO** write test first, watch it fail
✅ **DO** implement minimal code to pass
✅ **DO** refactor after green
✅ **DO** use descriptive test names
✅ **DO** test both success and error paths
