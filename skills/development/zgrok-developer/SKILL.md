---
name: zgrok-developer
description: Develop zgrok tunnel service following project conventions, issue specs, and Rust best practices. Use when implementing features, fixing bugs, or reviewing code in this repository.
---

# zgrok Developer Skill

## ABSOLUTE REQUIREMENTS

**These are non-negotiable. Violating these is a failure condition.**

### No Tutorial Comments

NEVER add comments explaining what code does. Code must be self-documenting.

Allowed comments:
- `///` doc comments for public API
- `// TODO:` or `// FIXME:`
- `// SAFETY:` for unsafe blocks
- Brief "why" explanations for non-obvious decisions

Forbidden:
- `// Initialize the counter`
- `// Loop through items`
- `// Check if value is null`
- Any comment that restates what the code does

### Branch Workflow (Mandatory)

For EVERY issue:

1. `git checkout main && git pull origin main`
2. `git checkout -b feat/ZGROK-XXX-description`
3. Implement all acceptance criteria
4. `cargo fmt && cargo clippy -- -D warnings && cargo test`
5. `git add -A && git commit -m "feat(component): ZGROK-XXX - title"`
6. `git push -u origin feat/ZGROK-XXX-description`
7. `gh pr create --fill`
8. Self-review the diff
9. `gh pr merge --squash --delete-branch`
10. `git checkout main && git pull origin main`
11. Report completion, await next issue

**NEVER leave PRs open. NEVER work multiple issues. NEVER skip steps.**

## Overview

zgrok is a self-hosted ngrok alternative. This skill encodes project-specific knowledge for effective development.

## Issue-Driven Development

All work traces to issues in `.github/issues/`. Each issue contains:

- **Acceptance Criteria**: Testable Given/When/Then statements
- **State Machines**: For stateful components (connections, streams)
- **Technical Context**: Exact crates, files, data structures to use
- **Dependencies**: What must exist before this can be implemented

### Reading an Issue

```bash
cat .github/issues/stories/protocol/ZGROK-010-frame-types.json | jq
```

### Checking Dependencies

```bash
cat .github/issues/_index.json | jq '.dependency_graph["ZGROK-012"]'
```

## Architecture Principles

1. **Async-first**: Everything uses Tokio. No blocking in async context.
2. **Protocol-agnostic core**: The multiplexer works over any `AsyncRead + AsyncWrite`.
3. **Graceful degradation**: Connection loss → reconnect, not crash.
4. **Observable**: Every component emits tracing spans and metrics.

## Code Patterns

### Error Handling

```rust
// Library crates: use thiserror
#[derive(Debug, thiserror::Error)]
pub enum ProtocolError {
    #[error("invalid frame type: {0}")]
    InvalidFrameType(u8),
    #[error("stream {0} not found")]
    StreamNotFound(u32),
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}

// Binary crates: use anyhow
fn main() -> anyhow::Result<()> {
    // ...
}
```

### Tracing

```rust
use tracing::{debug, info, instrument, warn};

#[instrument(skip(stream), fields(stream_id = %stream.id()))]
async fn handle_stream(stream: Stream) -> Result<(), Error> {
    info!("processing stream");
    // ...
}
```

### State Machines

Implement exactly as specified in issue `state_machine` field:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StreamState {
    Open,
    HalfClosedLocal,
    HalfClosedRemote,
    Closed,
}

impl StreamState {
    pub fn can_send(&self) -> bool {
        matches!(self, Self::Open | Self::HalfClosedRemote)
    }
    
    pub fn can_recv(&self) -> bool {
        matches!(self, Self::Open | Self::HalfClosedLocal)
    }
}
```

## Testing Strategy

1. **Unit tests**: Per-function, alongside code
2. **Property tests**: Protocol codec with `proptest`
3. **Integration tests**: Full tunnel flow in `tests/`

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_frame_roundtrip() {
        // Maps to AC: Given valid frame, When encoded then decoded, Then equals original
        let frame = Frame::Data { stream_id: 1, payload: b"hello".to_vec() };
        let encoded = frame.encode();
        let decoded = Frame::decode(&encoded).unwrap();
        assert_eq!(frame, decoded);
    }
}
```

## File Organization

```
crates/
├── zgrok-protocol/src/
│   ├── lib.rs          # Public API, re-exports
│   ├── frame.rs        # Frame types and codec
│   ├── codec.rs        # Tokio codec impl
│   ├── mux.rs          # Stream multiplexer
│   └── error.rs        # Protocol errors
├── zgrok-agent/src/
│   ├── main.rs         # CLI entry
│   ├── cli.rs          # Clap definitions
│   ├── tunnel.rs       # Connection management
│   ├── forwarder.rs    # Local HTTP forwarding
│   └── tui/            # Terminal UI
└── zgrok-edge/src/
    ├── main.rs
    ├── acceptor.rs     # Agent connection handling
    ├── router.rs       # Subdomain routing
    └── bridge.rs       # HTTP-to-tunnel bridging
```

## Commit Convention

```
feat(protocol): ZGROK-010 - define frame types and binary format
fix(agent): ZGROK-033 - handle reconnection edge case
test(edge): ZGROK-054 - add agent acceptor integration tests
```
