---
name: Rust
description: Rust development patterns, project setup, CLI/TUI applications, error handling, and system integration
---

# Rust Development

This skill covers Rust development with two specialized reference documents:

## When Starting a New Project

Use **[Rust-Project-Setup.md](Rust-Project-Setup.md)** for:
- Creating new Rust CLI/TUI applications from scratch
- Cargo.toml setup and dependency selection
- Module structure and organization
- System dependency documentation (ALSA, X11, OpenGL, etc.)
- Configuration with serde/toml
- README and documentation templates
- Step-by-step implementation workflow

## When Writing Code

Use **[Rust-Patterns.md](Rust-Patterns.md)** for:
- Trait-based abstractions for swappable implementations
- Error handling (anyhow vs thiserror)
- CLI argument parsing with clap
- Structured logging with tracing
- Frame timing and performance monitoring
- Linux device I/O (v4l2, video processing)
- Color space conversion (RGB to YUYV)
- Testing patterns with mocks

## Quick Reference

### Error Handling Decision

```
Is this a library?
├─ Yes → Use thiserror for typed errors
└─ No (application) → Use anyhow with .context()
```

### Common Dependencies

| Need | Crate | Notes |
|------|-------|-------|
| Error handling (app) | `anyhow` | Flexible, ergonomic |
| Error handling (lib) | `thiserror` | Typed errors |
| CLI parsing | `clap` v4 | Use derive feature |
| TUI framework | `ratatui` | With crossterm |
| Configuration | `serde` + `toml` | Standard approach |
| Async runtime | `tokio` | Most popular |
| HTTP client | `reqwest` | High-level, async |
| Logging | `tracing` | Structured logging |

### Cargo Commands

```bash
cargo check          # Fast compilation check
cargo build          # Debug build
cargo build --release # Optimized build
cargo test           # Run tests
cargo clippy         # Lint code
cargo fmt            # Format code
cargo doc --open     # Generate docs
```

### Cargo.lock Decision

- **Applications/Binaries**: Commit Cargo.lock (reproducible builds)
- **Libraries**: Don't commit (let downstream decide versions)
