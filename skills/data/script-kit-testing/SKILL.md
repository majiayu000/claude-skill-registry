---
name: script-kit-testing
description: Testing infrastructure for Script Kit GPUI. Use when writing tests, running test suites, or understanding the test organization. Covers smoke tests, SDK tests, test helpers, and test output format.
---

# Script Kit Testing

Testing infrastructure and patterns for Script Kit GPUI.

## Test Directories

- `tests/smoke/` - E2E tests (run via stdin JSON protocol)
- `tests/sdk/` - SDK tests (often `bun run ...`)

## SDK Preload in Tests

```ts
import '../../scripts/kit-sdk'; // globals: arg(), div(), editor(), fields(), captureScreenshot(), getLayoutInfo(), ...
```

## Test Output JSONL Format

```json
{"test":"arg-string-choices","status":"running","timestamp":"2024-..."}
{"test":"arg-string-choices","status":"pass","result":"Apple","duration_ms":45,"timestamp":"2024-..."}
```

Status values: `running | pass | fail | skip` (with `error`/`reason`)

## Minimal Test Skeleton

```ts
import '../../scripts/kit-sdk';

function log(test: string, status: string, extra: any = {}) {
  console.log(JSON.stringify({ test, status, timestamp: new Date().toISOString(), ...extra }));
}

const name = "my-test";
log(name, "running");
const start = Date.now();
try {
  const result = await arg("Pick", ["A", "B"]);
  log(name, "pass", { result, duration_ms: Date.now() - start });
} catch (e) {
  log(name, "fail", { error: String(e), duration_ms: Date.now() - start });
}
```

## Running Tests

```bash
# TypeScript SDK tests
bun run scripts/test-runner.ts
bun run scripts/test-runner.ts tests/sdk/test-arg.ts

# E2E smoke tests via stdin
cargo build && echo '{"type":"run","path":"'"$(pwd)"'/tests/sdk/test-arg.ts"}' | ./target/debug/script-kit-gpui
echo '{"type":"run","path":"'"$(pwd)"'/tests/smoke/hello-world.ts"}' | SCRIPT_KIT_AI_LOG=1 ./target/debug/script-kit-gpui 2>&1

# Rust unit tests
cargo test

# System tests (clipboard, accessibility, macOS APIs)
cargo test --features system-tests

# Run ignored interactive tests
cargo test --features system-tests -- --ignored
```

## Verification Gate (Before Every Commit)

```bash
cargo check && cargo clippy --all-targets -- -D warnings && cargo test
```

## Feature-Gated System Tests

Tests that use clipboard, accessibility APIs, or other system resources:
```rust
#[cfg(feature = "system-tests")]
#[test]
fn test_clipboard_integration() { ... }
```

## Test Helpers

```rust
fn test_scriptlet(name: &str, tool: &str, code: &str) -> Scriptlet {
    Scriptlet { name: name.to_string(), tool: tool.to_string(), code: code.to_string(), ..Default::default() }
}

fn wrap_scripts(scripts: Vec<Script>) -> Vec<Arc<Script>> {
    scripts.into_iter().map(Arc::new).collect()
}
```

## Platform-Specific Tests

```rust
#[cfg(target_os = "macos")]
#[test]
fn test_macos_specific() { ... }

#[cfg(unix)]
#[test]
fn test_unix_signals() { ... }
```

## Anti-Patterns

- **DON'T** use `cx.run()` in unit tests (needs running app)
- **DON'T** rely on global state between tests
- **DON'T** hardcode paths (`/Users/john/...`) - use temp dirs
- **DON'T** forget platform guards for OS-specific tests
- **DON'T** skip cleanup (env vars, temp files)
