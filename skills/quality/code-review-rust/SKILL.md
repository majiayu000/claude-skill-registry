---
name: code-review-rust
description: Rust-specific code review guidelines focusing on error handling, safety, and idiomatic patterns
category: development
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Rust Code Review

Includes all guidelines from code-review skill, plus Rust-specific rules.

## No `unwrap` in Non-test Code

The reviewer MUST:
- Flag every `unwrap()`, `unwrap_err()`, or `expect_err()` outside tests.

Preferred alternatives:
- Use `?` and propagate errors when the function returns `Result`.
- Handle errors explicitly (map to a domain error, log and fallback, or early return).
- Use `expect()` only when failure is logically impossible or globally fatal, and the message explains why.

Bad:
```rust
let cfg = read_config().unwrap();
```

Better:
```rust
let cfg = read_config()?;
```

Acceptable only with proof:
```rust
let cfg = read_config().expect(
    "config is validated and loaded at startup; reaching here means startup checks passed"
);
```

The reviewer MUST reject vague `expect` messages (e.g. "should not fail").

## No `panic!` in Non-test Code

The reviewer MUST:
- Flag all `panic!`, `todo!`, and `unimplemented!` outside tests.

The reviewer SHOULD:
- Prefer returning and propagating proper errors.
- Fail early at startup via error returns instead of panics deep in logic.
- Encourage tests to use panics and unwraps only with clear messages (e.g. `expect("reason")`).

## `unreachable!()` Usage

The reviewer MUST:
- Flag `unreachable!()` unless a clear invariant explanation is provided.

It MAY be accepted if:
- The branch is genuinely impossible by construction.
- A comment documents the invariant (why this branch cannot be reached).

Otherwise, prefer returning a domain error instead of `unreachable!()`.

## No Silently Ignored Errors (Non-test Code)

The reviewer MUST:
- Flag any ignored `Result` or `Option` unless the error is handled or logged, there is a clear comment explaining why ignoring is safe, or the error type is `()` and this is intentional.

Bad:
```rust
let _ = do_something_fallible();
do_something_fallible().ok();
```

Acceptable:
```rust
if let Err(e) = do_something_fallible() {
    log::warn!("failed to do something: {}", e);
}

// Safe to ignore: telemetry failures do not affect correctness.
let _ = send_telemetry(&metrics);
```

Tests MAY ignore errors, but explicit assertions are encouraged.

## Idiomatic Rust and Built-ins

The reviewer SHOULD:
- Suggest `?` for simple error propagation instead of manual `match`.
- Use iterator methods (`map`, `filter`, `collect`, etc.) when they simplify logic.
- Use `Option` and `Result` combinators (`map`, `and_then`, `ok_or`, etc.) where they make code clearer.

The reviewer MUST NOT:
- Suggest overly clever refactors that hurt readability.

## Performance

The reviewer SHOULD:
- Point out obvious waste such as repeated `to_string` or `clone` in hot loops, or missing `with_capacity` for growing collections.

The reviewer MUST:
- Favor correctness and clarity over small micro-optimizations.
- Avoid speculative performance claims without a clear reason.

## Documentation and Comments

The reviewer SHOULD:
- Ensure new or changed public APIs have basic `///` docs covering behavior, arguments, return values, and possible errors.
- Encourage comments where logic is non-obvious, especially around `unsafe` code, concurrency and ordering assumptions, or invariants the type system does not enforce.

The reviewer SHOULD NOT:
- Request redundant "code-as-English" comments.
