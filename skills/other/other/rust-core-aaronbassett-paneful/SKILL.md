---
name: rust-core
description: "Comprehensive Rust development expertise covering core principles, patterns, error handling, async programming, testing, and performance optimization. Use when working on Rust projects requiring guidance on: (1) Language fundamentals (ownership, lifetimes, borrowing), (2) Architectural decisions and design patterns, (3) Web development (Axum, Actix-web, Rocket), (4) AI/LLM integration, (5) CLI/TUI applications, (6) Desktop development with Tauri, (7) Async/await and concurrency, (8) Error handling strategies, (9) Testing and benchmarking, (10) Performance optimization, (11) Logging and observability, or (12) Code reviews and best practices."
---

# Rust Core Development

Comprehensive guidance for Rust development across web, CLI, desktop, AI/LLM applications, and systems programming.

## Quick Reference Guide

### By Task Type

**Getting Started**
- **New Project Setup**: Use `scripts/init_rust_project.sh` to scaffold a project with best practices
- **Core Principles**: See [references/principles.md](references/principles.md) for ownership, borrowing, and Rust fundamentals
- **Common Errors**: See [references/common-errors.md](references/common-errors.md) for solutions to frequent compiler errors

**Writing Code**
- **Design Patterns**: Consult [references/patterns.md](references/patterns.md) for builder, newtype, RAII, and other patterns
- **Error Handling**: See [references/error-handling.md](references/error-handling.md) for Result, Option, anyhow, and thiserror
- **Async Programming**: See [references/async-patterns.md](references/async-patterns.md) for Tokio, channels, and concurrency

**Domain-Specific Development**
- **Web APIs**: See [references/web-frameworks.md](references/web-frameworks.md) for Axum, Actix-web, and Rocket
- **AI/LLM**: See [references/ai-llm.md](references/ai-llm.md) for OpenAI, Anthropic, Ollama, and RAG
- **CLI Tools**: See [references/cli-tui.md](references/cli-tui.md) for Clap and Ratatui
- **Desktop Apps**: See [references/desktop-tauri.md](references/desktop-tauri.md) for Tauri
- **Logging**: See [references/logging-observability.md](references/logging-observability.md) for tracing and metrics

**Code Quality**
- **Testing**: See [references/testing.md](references/testing.md) for unit, integration, and property-based testing
- **Code Review**: See [references/code-review.md](references/code-review.md) for review checklist and anti-patterns
- **Performance**: See [references/performance.md](references/performance.md) for profiling and optimization

**Project Management**
- **Dependencies**: See [references/dependencies.md](references/dependencies.md) for Cargo.toml best practices
- **Project Structure**: See [references/project-structure.md](references/project-structure.md) for modules and workspaces
- **Essential Crates**: See [references/crates-core.md](references/crates-core.md) for commonly used libraries

### By Question Type

| Question | Reference |
|----------|-----------|
| "How do I handle errors?" | [error-handling.md](references/error-handling.md) |
| "Which web framework should I use?" | [web-frameworks.md](references/web-frameworks.md) |
| "How do I work with async/await?" | [async-patterns.md](references/async-patterns.md) |
| "How do I integrate OpenAI/Claude?" | [ai-llm.md](references/ai-llm.md) |
| "How do I build a CLI?" | [cli-tui.md](references/cli-tui.md) |
| "How do I create a desktop app?" | [desktop-tauri.md](references/desktop-tauri.md) |
| "Why won't this compile?" | [common-errors.md](references/common-errors.md) |
| "How do I improve performance?" | [performance.md](references/performance.md) |
| "How do I add logging?" | [logging-observability.md](references/logging-observability.md) |
| "How should I name this?" | [naming.md](references/naming.md) |
| "What are best practices?" | [principles.md](references/principles.md) |
| "How do I test this?" | [testing.md](references/testing.md) |

## Core Workflows

### 1. Starting a New Project

1. **Initialize Project**
   ```bash
   ./scripts/init_rust_project.sh my-project
   ```

2. **Set Up Development Tools**
   - Configure linting: Copy `assets/configs/clippy.toml` and `assets/configs/rustfmt.toml`
   - Configure security: Copy `assets/configs/deny.toml`
   - Run audit: `./scripts/audit_dependencies.sh`

3. **Add Logging**
   ```bash
   ./scripts/setup_logging.sh
   ```

4. **Choose Architecture**
   - **Web API**: Consult [web-frameworks.md](references/web-frameworks.md) for Axum, Actix-web, or Rocket
   - **CLI Tool**: See [cli-tui.md](references/cli-tui.md) for Clap
   - **Desktop App**: See [desktop-tauri.md](references/desktop-tauri.md)
   - **Library**: See [project-structure.md](references/project-structure.md)

### 2. Implementing Features

1. **Design First**
   - Review [principles.md](references/principles.md) for ownership and type-driven design
   - Check [patterns.md](references/patterns.md) for applicable design patterns
   - Plan error handling strategy from [error-handling.md](references/error-handling.md)

2. **Write Code**
   - Follow naming conventions from [naming.md](references/naming.md)
   - Use appropriate patterns and error handling
   - Add tracing/logging as you go

3. **Test**
   - Write unit tests (see [testing.md](references/testing.md))
   - Add integration tests for public APIs
   - Consider property-based tests for complex logic

### 3. Code Review and Refinement

1. **Self-Review**
   - Run through [code-review.md](references/code-review.md) checklist
   - Check for common anti-patterns
   - Verify error handling

2. **Performance Check**
   - Profile if performance-critical (see [performance.md](references/performance.md))
   - Benchmark changes with Criterion
   - Avoid premature optimization

3. **Security Audit**
   ```bash
   ./scripts/audit_dependencies.sh
   ```

## Decision Guides

### Choosing a Web Framework

**Use Axum when:**
- Building modern REST/GraphQL APIs
- Want composable middleware (Tower ecosystem)
- Prefer type-driven extractors
- Building microservices

**Use Actix-web when:**
- Need maximum performance
- Building high-throughput APIs
- Want mature, battle-tested framework
- Familiar with actor model

**Use Rocket when:**
- Rapid prototyping
- Want batteries-included features
- Smaller team or learning Rust web
- Traditional web application

See [web-frameworks.md](references/web-frameworks.md) for detailed comparison and code examples.

### Error Handling Strategy

**Use `anyhow` for:**
- Applications (binaries)
- Quick prototyping
- Internal tools
- When you need ergonomic error handling with context

**Use `thiserror` for:**
- Libraries (public APIs)
- When consumers need to handle specific error cases
- Type-safe error hierarchies
- Production code with well-defined error types

See [error-handling.md](references/error-handling.md) for patterns and examples.

### When to Use Async

**Use async/await when:**
- I/O-bound operations (network, file system)
- Web servers handling many concurrent requests
- Database connection pooling
- Working with streams of data

**Don't use async when:**
- CPU-bound operations (use `spawn_blocking` instead)
- Simple CLI tools
- Performance isn't critical
- Complexity isn't justified

See [async-patterns.md](references/async-patterns.md) for Tokio patterns and best practices.

## Automation Scripts

### Available Scripts

**`scripts/init_rust_project.sh`**
Initialize a new Rust project with best practices:
- Common dependencies (anyhow, thiserror, serde, tracing)
- Benchmark setup with Criterion
- Optimized release profile
- Proper .gitignore

Usage: `./scripts/init_rust_project.sh my-project [bin|lib]`

**`scripts/audit_dependencies.sh`**
Audit dependencies for security and licensing:
- Runs cargo-audit for security vulnerabilities
- Runs cargo-deny for license compliance
- Shows outdated dependencies

Usage: `./scripts/audit_dependencies.sh`

**`scripts/setup_logging.sh`**
Set up tracing-based logging:
- Adds tracing dependencies
- Creates logging module with JSON support
- Provides initialization code

Usage: `./scripts/setup_logging.sh`

## Configuration Templates

### `assets/configs/clippy.toml`
Clippy linting configuration for strict code quality

### `assets/configs/rustfmt.toml`
Code formatting configuration (100 char width, Unix newlines)

### `assets/configs/deny.toml`
cargo-deny configuration for:
- Security advisory checking
- License compliance (MIT, Apache-2.0, BSD allowed)
- Duplicate dependency detection
- Source verification

## Reference Documentation

All reference files provide in-depth guidance on specific topics:

### Core Language
- **[principles.md](references/principles.md)** - Ownership, borrowing, zero-cost abstractions
- **[patterns.md](references/patterns.md)** - Builder, newtype, RAII, iterator, visitor patterns
- **[error-handling.md](references/error-handling.md)** - Result, Option, anyhow, thiserror
- **[naming.md](references/naming.md)** - Rust naming conventions
- **[common-errors.md](references/common-errors.md)** - Borrow checker, lifetime errors, solutions

### Development
- **[testing.md](references/testing.md)** - Unit, integration, property-based, benchmarking
- **[project-structure.md](references/project-structure.md)** - Modules, workspaces, organization
- **[dependencies.md](references/dependencies.md)** - Cargo.toml, features, version management
- **[performance.md](references/performance.md)** - Profiling, optimization, benchmarking
- **[code-review.md](references/code-review.md)** - Review checklist, anti-patterns

### Async & Concurrency
- **[async-patterns.md](references/async-patterns.md)** - Tokio, futures, streams, channels

### Domains
- **[web-frameworks.md](references/web-frameworks.md)** - Axum, Actix-web, Rocket comparison
- **[ai-llm.md](references/ai-llm.md)** - OpenAI, Anthropic, Ollama, RAG, function calling
- **[cli-tui.md](references/cli-tui.md)** - Clap, Ratatui, terminal interfaces
- **[desktop-tauri.md](references/desktop-tauri.md)** - Desktop apps, plugins, IPC
- **[logging-observability.md](references/logging-observability.md)** - Tracing, metrics, OpenTelemetry

### Libraries
- **[crates-core.md](references/crates-core.md)** - Essential crates (serde, tokio, anyhow, reqwest)

## When to Consult References

**Load references progressively as needed:**

1. **Starting out**: Read [principles.md](references/principles.md) to understand Rust fundamentals
2. **Choosing approach**: Consult domain-specific guides ([web-frameworks.md](references/web-frameworks.md), [ai-llm.md](references/ai-llm.md), etc.)
3. **Implementing**: Reference [patterns.md](references/patterns.md) and [error-handling.md](references/error-handling.md)
4. **Debugging**: Check [common-errors.md](references/common-errors.md)
5. **Optimizing**: See [performance.md](references/performance.md)
6. **Reviewing**: Use [code-review.md](references/code-review.md) checklist

Don't load all references at once—consult them as specific needs arise.

## Best Practices Summary

1. **Embrace the borrow checker** - Work with ownership, not against it
2. **Use type-driven design** - Make invalid states unrepresentable
3. **Handle errors explicitly** - Use Result and Option, avoid unwrap()
4. **Test comprehensively** - Unit tests, integration tests, property tests
5. **Profile before optimizing** - Measure, don't guess
6. **Add structured logging** - Use tracing for observability
7. **Review security** - Audit dependencies, validate inputs
8. **Follow conventions** - rustfmt, clippy, naming conventions
9. **Document public APIs** - Doc comments with examples
10. **Keep it simple** - Prefer clarity over cleverness
