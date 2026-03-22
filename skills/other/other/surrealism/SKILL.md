---
name: surrealism
description: "SurrealDB Surrealism WASM extension development. Write Rust functions, compile to WASM, deploy as database modules. Part of the surreal-skills collection."
license: MIT
metadata:
  version: "1.0.4"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-19"
  upstream:
    repo: "surrealdb/surrealdb"
    release: "v3.0.0"
    sha: "2e0a61fd4daf"
    docs: "https://surrealdb.com/docs/surrealdb/extensions"
---

# Surrealism -- WASM Extensions for SurrealDB

New in SurrealDB 3. Write custom functions in Rust, compile them to WebAssembly
(WASM), and deploy them as native database modules callable from SurrealQL.

## Prerequisites

- Rust toolchain (stable) with `wasm32-unknown-unknown` target
- SurrealDB CLI v3.0.0+ (`surreal` binary with `surreal module` subcommand)
- Familiarity with SurrealQL `DEFINE MODULE` and `DEFINE BUCKET`

## Development Workflow

```
1. Annotate   -- surrealism.toml + #[surrealism] on Rust functions
2. Compile    -- surreal module compile  (produces .wasm binary)
3. Register   -- DEFINE BUCKET + DEFINE MODULE in SurrealQL
```

## Quick Start

```bash
# Create a new Surrealism project
cargo new --lib my_extension
cd my_extension

# Add the WASM target
rustup target add wasm32-unknown-unknown

# Create surrealism.toml (required manifest)
cat > surrealism.toml << 'TOML'
[package]
name = "my_extension"
version = "0.1.0"
TOML

# Write your extension (annotate with #[surrealism])
cat > src/lib.rs << 'RUST'
use surrealism::surrealism;

#[surrealism]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}
RUST

# Compile to WASM using SurrealDB CLI
surreal module compile

# Register in SurrealDB
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test
```

```surql
-- Grant access to the WASM file
DEFINE BUCKET my_bucket;

-- Register the module functions
DEFINE MODULE my_extension FROM 'my_bucket:my_extension.wasm';

-- Use the function in queries
SELECT my_extension::greet('World');
```

## Use Cases

- Custom scalar functions callable from SurrealQL
- Fake/mock data generation for testing
- Domain-specific logic (language processing, quantitative finance, custom encoding)
- Access to niche Rust crate functionality too specific for core SurrealDB
- Custom analyzers for full-text search

## Status

Surrealism is actively in development and not yet stable. The API may change
between SurrealDB 3.x releases. File feedback via GitHub issues/PRs on the
[surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) repository.

## Full Documentation

See the main skill's rule file for complete guidance:
- **[rules/surrealism.md](../../rules/surrealism.md)** -- project setup, Rust function signatures, WASM compilation, DEFINE MODULE/BUCKET syntax, deployment, testing, and best practices
- **[SurrealDB Extensions Docs](https://surrealdb.com/docs/surrealdb/extensions)** -- official documentation
- **[CLI module command](https://surrealdb.com/docs/surrealdb/cli/module)** -- `surreal module` reference
