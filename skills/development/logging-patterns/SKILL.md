---
id: logging-patterns
name: Logging Patterns
description: >-
  Common logging patterns and practices. This skill is designed to be
  included in composite skills via the 'includes' feature.
tags: [logging, observability, example]
---

# Logging Patterns

Foundational logging practices for observable applications.

## Rules

- Use structured logging (key-value pairs, not interpolated strings)
- Include request/correlation IDs in all log entries
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Include enough context to debug issues without the code
- Don't log sensitive information (passwords, tokens, PII)

## Pitfalls

- Logging sensitive data (passwords, API keys, PII)
- Inconsistent log levels across the codebase
- Missing correlation IDs in distributed systems
- Logging at wrong levels (DEBUG in prod, ERROR for non-errors)

## Examples

```rust
// Structured logging with tracing
use tracing::{info, error, instrument};

#[instrument(skip(password))]
fn authenticate(user_id: &str, password: &str) -> Result<Token> {
    info!(user_id, "authentication attempt");

    match verify_credentials(user_id, password) {
        Ok(token) => {
            info!(user_id, "authentication successful");
            Ok(token)
        }
        Err(e) => {
            error!(user_id, error = %e, "authentication failed");
            Err(e)
        }
    }
}
```
