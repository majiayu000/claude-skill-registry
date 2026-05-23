---
name: cargo-rust
description: Rust package manager and build system. Cargo commands, dependency management, and workspace patterns.
version: 1.0.0
---


# Cargo Rust Skill

**Trit**: -1 (MINUS - build verification and constraint checking)  
**Foundation**: Cargo + rustc + crates.io  

## Core Concept

Cargo manages Rust projects with:
- Dependency resolution
- Build orchestration  
- Testing and benchmarking
- Publishing to crates.io

## Commands

```bash
# Build
cargo build
cargo build --release

# Test
cargo test
cargo test --lib

# Check (fast)
cargo check
cargo clippy

# Run
cargo run
cargo run --release

# Add dependency
cargo add serde
cargo add serde --features derive
```

## Workspace Pattern

```toml
# Cargo.toml (workspace root)
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
```

## GF(3) Integration

```rust
fn trit_from_build(result: &BuildResult) -> i8 {
    match result {
        BuildResult::Error(_) => -1,   // MINUS: compilation failure
        BuildResult::Warning(_) => 0,  // ERGODIC: warnings
        BuildResult::Success => 1,     // PLUS: clean build
    }
}
```

## Canonical Triads

```
cargo-rust (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓
cargo-rust (-1) ⊗ nickel (0) ⊗ world-hopping (+1) = 0 ✓
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
cargo-rust (+) + SDF.Ch4 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch10: Adventure Game Example
- Ch7: Propagators

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.