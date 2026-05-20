---
name: telemetry
description: Telemetry and observability conventions. Apply when adding tracing, logging, metrics, or instrumentation to Rust code.
---

# Telemetry & Observability Conventions

If the project has a dedicated telemetry/observability spec or conventions document, read it first — it takes precedence over the generic guidance below.

## Log Levels

| Level | When to Use | Example |
|---|---|---|
| `error!` | Unrecoverable failures requiring operator attention | External service call failed permanently |
| `warn!` | Recoverable issues, degraded operation | Retry triggered, fallback activated |
| `info!` | Lifecycle events, operational milestones | Server started, connection established |
| `debug!` | Internal state useful during development | State machine transition details |
| `trace!` | Per-frame, hot-path data (high volume) | Frame encoded, bytes serialized |

## Instrumentation Depth

Not all code deserves the same instrumentation level. Choose based on the crate's role:

- **Hot-path code** (serialization, framing, tight loops): `trace!` only, no spans. Spans add overhead that matters here.
- **Type definition crates** (pure data types, no logic): `trace!` only if anything at all.
- **Core business logic** (servers, handlers, state machines): Full instrumentation — `#[instrument]` + spans.
- **Client-facing code** (SDKs, CLI flows): Full instrumentation for debuggability.

## `#[instrument]` Rules

- Use on async functions that represent logical operations or flow steps
- Skip on hot-path synchronous functions (serialization, encoding, tight loops)
- Always `skip` sensitive fields: tokens, keys, passwords, raw payloads
- Include identifying fields that aid correlation (IDs, resource names)
- Set appropriate `level` — default is `INFO`, use `level = "debug"` or `level = "trace"` for noisy functions

## Structured Logging

Always use named fields, never string interpolation:

```rust
// Good: named fields — searchable, parseable
trace!(payload_bytes = payload.len(), frame_bytes = buf.len(), "frame encoded");

// Bad: string interpolation — opaque to log aggregators
trace!("frame encoded, payload={}, frame={}", payload.len(), buf.len());
```

## Span Design

For request/message processing pipelines, use a three-tier span pattern:

- **Inbound span:** one per received message/request (message type, size, sender ID)
- **Process span:** business logic processing (operation type, affected resources)
- **Outbound span:** one per response/forwarded message (recipient, payload size)

This gives visibility into where time is spent and enables per-hop latency analysis.

## General Principles

- Prefer `tracing` over `log` — structured spans enable distributed tracing
- Log at the point of decision, not at every intermediate step
- Include enough context to diagnose without reproducing: IDs, sizes, error details
- Never log secrets, tokens, keys, or raw user data — even at `trace!` level
- Use `Display` for user-facing context, `Debug` for developer diagnostics
