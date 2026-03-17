---
name: tauri-backend-testing
description: Generate tests for Tauri backend Rust code, including command handlers, system integration, and IPC communication. Triggers on testing Rust code, Tauri commands, backend tests, or system integration tests.
---

# Tauri Backend Testing Skill

This skill enables Claude to generate high-quality, comprehensive tests for the Desktop Ethereal project's Tauri backend Rust code.

## When to Apply This Skill

Apply this skill when the user:

- Asks to **write tests** for Tauri command handlers or Rust backend code
- Asks to **review existing backend tests** for completeness
- Mentions **Tauri commands**, **Rust testing**, or **backend tests**
- Requests **system integration testing** or **IPC communication tests**
- Wants to improve **test coverage** for backend code

**Do NOT apply** when:

- User is asking about frontend/React tests
- User is asking about E2E tests
- User is only asking conceptual questions without code context

## Quick Reference

### Tech Stack

| Tool | Version | Purpose |
| ------ | --------- | --------- |
| Rust | 1.70+ | Programming language |
| Tauri | 2.0+ | Desktop framework |
| cargo-nextest | 0.9+ | Test runner |
| tokio | 1.0+ | Async runtime |

### Key Commands

```bash
# Run all backend tests
cargo test

# Run tests with nextest
cargo nextest run

# Run specific test
cargo test test_name

# Generate coverage report
cargo tarpaulin --out Html
```

## Test Structure Template

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tauri::test::{mock_app, mock_window};

    // Test setup
    fn setup_test_app() -> tauri::App {
        mock_app()
    }

    // Command handler tests (REQUIRED)
    mod command_handlers {
        use super::*;

        #[test]
        fn test_command_success() {
            // Arrange
            let app = setup_test_app();
            let window = mock_window(&app, "main");
            let expected_param = "test_value";

            // Act
            let result = some_tauri_command(window, expected_param);

            // Assert
            assert!(result.is_ok());
            assert_eq!(result.unwrap(), "expected_result");
        }

        #[test]
        fn test_command_error() {
            // Arrange
            let app = setup_test_app();
            let window = mock_window(&app, "main");
            let invalid_param = "";

            // Act
            let result = some_tauri_command(window, invalid_param);

            // Assert
            assert!(result.is_err());
            assert_eq!(result.unwrap_err().to_string(), "Expected error message");
        }
    }

    // System integration tests
    mod system_integration {
        use super::*;

        #[tokio::test]
        async fn test_system_monitoring() {
            // Arrange
            let app = setup_test_app();

            // Act
            let stats = get_system_stats().await;

            // Assert
            assert!(stats.is_ok());
            let stats = stats.unwrap();
            assert!(stats.cpu_usage >= 0.0);
            assert!(stats.cpu_usage <= 100.0);
        }
    }

    // IPC communication tests
    mod ipc_communication {
        use super::*;

        #[test]
        fn test_event_emission() {
            // Arrange
            let app = setup_test_app();
            let window = mock_window(&app, "main");
            let expected_data = TestData { value: 42 };

            // Act
            let result = emit_test_event(&window, &expected_data);

            // Assert
            assert!(result.is_ok());
            // Verify event was emitted (implementation dependent)
        }
    }
}
```

## Testing Workflow (CRITICAL)

### ⚠️ Incremental Approach Required

**NEVER generate all test files at once.** For complex modules or multi-file testing:

1. **Analyze & Plan**: List all functions, order by complexity (simple → complex)
1. **Process ONE at a time**: Write test → Run test → Fix if needed → Next
1. **Verify before proceeding**: Do NOT continue to next function until current passes

```
For each function:
  ┌────────────────────────────────────────┐
  │ 1. Write test                          │
  │ 2. Run: cargo test function_name       │
  │ 3. PASS? → Mark complete, next func    │
  │    FAIL? → Fix first, then continue    │
  │ 4. Check coverage                      │
  └────────────────────────────────────────┘
```

### Complexity-Based Order

Process in this order for multi-function testing:

1. 🟢 Simple pure functions (no side effects)
1. 🟢 Command handlers with basic logic
1. 🟡 Functions with system calls
1. 🟡 Async functions
1. 🔴 Complex system integration functions
1. 🔴 IPC communication functions (last)

## Core Principles

### 1. AAA Pattern (Arrange-Act-Assert)

Every test should clearly separate:

- **Arrange**: Setup test data and environment
- **Act**: Call the function under test
- **Assert**: Verify expected outcomes

### 2. Black-Box Testing

- Test observable behavior, not implementation details
- Focus on inputs and outputs
- Avoid testing internal state directly

### 3. Single Behavior Per Test

Each test verifies ONE observable behavior:

```rust
// ✅ Good: One behavior
#[test]
fn test_command_success() {
    // Test successful command execution
}

// ❌ Bad: Multiple behaviors
#[test]
fn test_command_all_cases() {
    // Test success, error, and edge cases in one test
}
```

### 4. Descriptive Naming

Use `test_<function>_<behavior>_<condition>`:

```rust
#[test]
fn test_get_gpu_stats_returns_valid_data_when_gpu_present()
#[test]
fn test_set_click_through_fails_when_invalid_window()
#[test]
fn test_listen_for_events_handles_multiple_events()
```

## Required Test Scenarios

### Always Required (All Functions)

1. **Success Case**: Function works as expected with valid inputs
1. **Error Case**: Function handles errors appropriately
1. **Edge Cases**: Boundary conditions, null/empty inputs

### Conditional (When Present)

| Feature | Test Focus |
| --------- | ----------- |
| `Result<T, E>` return | Both Ok and Err variants |
| System calls | Mock system dependencies |
| Async operations | Test with tokio runtime |
| Tauri commands | Test with mock window/app |
| Event emission | Verify events are emitted |
| State mutation | Verify state changes correctly |

## Coverage Goals (Per Function)

For each test function generated, aim for:

- ✅ **100%** function coverage
- ✅ **100%** statement coverage
- ✅ **>95%** branch coverage
- ✅ **>95%** line coverage

## Tauri-Specific Considerations

### Testing Tauri Commands

Always test Tauri commands with mock windows:

```rust
#[test]
fn test_tauri_command() {
    // Create mock app and window
    let app = mock_app();
    let window = mock_window(&app, "main");

    // Test command with mock window
    let result = tauri_command(window, param);

    // Assert result
    assert!(result.is_ok());
}
```

### Mocking System Dependencies

For functions that interact with system resources:

```rust
// Use cfg(test) to provide mock implementations
#[cfg(not(test))]
fn get_system_temperature() -> Result<u32, String> {
    // Real implementation
    nvml_wrapper::get_temperature()
}

#[cfg(test)]
fn get_system_temperature() -> Result<u32, String> {
    // Mock implementation
    Ok(75)
}
```

### Testing Async Functions

For async Tauri functions:

```rust
#[tokio::test]
async fn test_async_command() {
    // Arrange
    let app = mock_app();
    let window = mock_window(&app, "main");

    // Act
    let result = async_tauri_command(window, param).await;

    // Assert
    assert!(result.is_ok());
}
```

## Detailed Guides

For more detailed information, refer to:

- `references/workflow.md` - **Incremental testing workflow** (MUST READ for multi-function testing)
- `references/mocking.md` - Mock patterns and best practices for system dependencies
- `references/async-testing.md` - Async operations and system calls
- `references/ipc-testing.md` - IPC communication and event testing
- `references/command-testing.md` - Tauri command handler testing

## Authoritative References

### Primary Specification (MUST follow)

- **`docs/backend-testing.md`** - The canonical testing specification for Desktop Ethereal backend.

### Reference Examples in Codebase

- `src-tauri/src/main.rs` - Main application with command handlers
- `src-tauri/tests/` - Integration tests (to be created)
- `src-tauri/Cargo.toml` - Dependencies and test configuration

### Project Configuration

- `src-tauri/Cargo.toml` - Rust configuration
- `.cargo/config.toml` - Cargo configuration
