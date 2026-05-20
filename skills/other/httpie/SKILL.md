---
name: httpie
description: HTTPie human-friendly HTTP client. Use for API testing.
---

# HTTPie

HTTPie started as a CLI (`http get example.com`) and now includes a beautiful **Desktop** app (2025). It is famous for its **human-friendly** syntax.

## When to Use

- **CLI**: `http POST api.com name=John` is faster than `curl -X POST -d '{"name":"John"}' ...`.
- **Desktop**: Cleanest UI in the business. AI-assisted request building.
- **Quick Testing**: Zero config needed.

## Core Concepts

### Simplified Syntax

`:` for headers (`User-Agent:Chrome`), `=` for string data (`name=John`), `:=` for raw JSON (`age:=25`).

### Sessions

Persistent sessions (cookies/headers) in CLI. `http --session=logged-in API`.

## Best Practices (2025)

**Do**:

- **Use the Desktop App**: It syncs with the CLI.
- **Use `--offline`**: To inspect how the request _would_ look without sending it.

**Don't**:

- **Don't use `curl` for JSON**: Unless you are pasting to a colleague who doesn't have HTTPie. HTTPie is superior for JSON.

## References

- [HTTPie Documentation](https://httpie.io/docs)
