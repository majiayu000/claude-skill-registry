---
name: just-pro
description: This skill provides patterns for setting up just (command runner) in projects. Use PROACTIVELY when creating build systems, setting up new repos, or when the user asks about just/justfile configuration. Covers both simple single-project repos and monorepos with hierarchical justfile modules.
---

# Justfile Skill

Build system configuration using [just](https://just.systems), a modern command runner.

**Related skills:**
- **mise** - Tool version management (includes just+mise integration patterns)
- **go-pro**, **rust-pro**, **typescript-pro** - Language-specific templates

## Installation

```bash
# Via mise (recommended - version pinned per-project)
mise use just

# macOS
brew install just

# Linux/Windows (via cargo)
cargo install just

# Or prebuilt binaries: https://github.com/casey/just/releases
```

## When to Use Just

| Scenario | Recommendation |
|----------|----------------|
| Cross-language monorepo | **just** - Unified interface across packages |
| Single Go/Rust project | **just** or language-native (go/cargo) |
| Node.js project | npm scripts primary, just optional wrapper |
| CI/CD porcelain | **just** - Single entry point for all operations |
| Simple scripts | **just** - Better than shell scripts |

## Project Patterns

### Simple Repo (Single Package)

For single-language projects, create one `justfile` at repo root.

```just
# Project Build System
# Usage: just --list

default:
    @just --list

# === Quality Gates ===
check: fmt lint test
    @echo "All checks passed"

fmt:
    go fmt ./...

lint:
    go tool golangci-lint run

test:
    go test -race ./...

build:
    go build -o bin/app ./cmd/app
```

See `references/simple-repo.just` for complete templates.

### Monorepo (Multiple Packages)

For monorepos, use hierarchical justfiles with the `mod` system:

```
repo/
├── justfile              # Router - imports package modules
└── packages/
    ├── api-go/
    │   └── justfile      # Go package recipes
    ├── web/
    │   └── justfile      # TypeScript package recipes (optional)
    └── ops/
        └── justfile      # DevOps recipes
```

**Root justfile** (router):
```just
# Monorepo Build System
# Usage: just --list
# Usage: just go <recipe>

mod go "packages/api-go"
mod web "packages/web"
mod ops "ops"

default:
    @just --list

# Umbrella recipes call into modules
check: (go::check) (web::check)
    @echo "All checks passed"

setup: (go::setup) (web::setup)
    @echo "All toolchains ready"
```

**Commands become**: `just go check`, `just go lint`, `just web build`, `just ops deploy`

See `references/monorepo-root.just` and `references/package-go.just` for templates.

## Recipe Patterns

### Quality Gates

Always provide a single `check` recipe that runs all quality gates:

```just
# Full quality gates - run before commits
check: fmt lint test coverage-check
    @echo "All checks passed"
```

### Quick Check (Dev Iteration)

Fast feedback loop for development - essential checks only:

```just
# Quick feedback loop - essential checks only
check-quick: lint test
    @echo "Quick checks passed"
```

### Clean Recipe

Standard cleanup for build artifacts and caches:

```just
# Remove build artifacts and caches
clean:
    rm -rf build/ coverage.out node_modules/.cache
```

### Parallel Check Execution (CI)

Run package checks in parallel for faster CI:

```just
# Run all package checks in parallel (CI optimization)
check-parallel:
    @just api check & just web check & wait
```

### Coverage Enforcement

Use shebang for multi-line shell logic:

```just
# Check coverage meets 70% minimum
coverage-check:
    #!/usr/bin/env bash
    set -euo pipefail
    go test -race -coverprofile=coverage.out ./...
    COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    COVERAGE_INT=${COVERAGE%.*}
    [ "$COVERAGE_INT" -ge 70 ] || (echo "FAIL: Coverage ${COVERAGE}% < 70%" && exit 1)
    echo "PASS: Coverage ${COVERAGE}%"
```

The `#!/usr/bin/env bash` shebang runs the entire recipe as a single shell script (variables persist across lines).

### Umbrella Recipes with Module Dependencies

```just
# Root justfile calling into modules
check: (go::check) (web::check)
    @echo "All checks passed"
```

### Optional Modules

For packages that may not exist in all environments:

```just
mod? optional-package "packages/optional"
```

### Documentation Comments

Every recipe should have a doc comment (shown in `just --list`):

```just
# Run unit tests with race detection
test:
    go test -race ./...
```

**Module doc comments** - Comments above `mod` statements also appear in `just --list`:

```just
# Go API (GraphQL + Watermill)
mod api "packages/api"

# Next.js frontend
mod web "packages/web"

# PostgreSQL database
mod db "packages/db"
```

Output of `just --list`:
```
api ...      # Go API (GraphQL + Watermill)
db ...       # PostgreSQL database
web ...      # Next.js frontend
```

Always add doc comments to module imports for discoverability.

## Module System Details

### Syntax

```just
mod <name> "<path>"              # Required module
mod? <name> "<path>"             # Optional module (no error if missing)
mod <name>                       # Module at ./<name>/justfile
```

### Working Directory

Recipes in modules run with their working directory set to the module's directory, not the root. This is the desired behavior for package-local commands.

### Listing Module Recipes

```bash
just --list           # Root recipes + module names
just --list go        # Recipes in 'go' module
just --list-submodules # All recipes including submodules
```

**Important**: Use `just --list <module>` not `just <module> --list`. The flag must come before the module name.

### Calling Module Recipes

```bash
just go check         # From command line
(go::check)          # As dependency in justfile
```

## Integration with Language Toolchains

### Go Projects

```just
# Uses go.mod tool directive for pinned versions
lint:
    go tool golangci-lint run

# Auto-fix linting issues (chains goimports to fix imports after modernize changes)
fix:
    go tool golangci-lint run --fix
    go tool goimports -w .
```

**Why chain goimports?** The `modernize` linter may change code (e.g., `fmt.Errorf()` → `errors.New()`) without updating imports, breaking builds. Running `goimports` after `--fix` resolves this.

### TypeScript/Node Projects

Two approaches:

**Option A**: Thin wrapper (recommended for consistency)
```just
# packages/web/justfile
check:
    npm run check

lint:
    npm run lint

test:
    npm test
```

**Option B**: Direct delegation from root (simpler)
```just
# Root justfile - no web module
ts-web-check:
    cd packages/web && npm run check
```

### Rust Projects

```just
check: fmt lint test
    @echo "All checks passed"

fmt:
    cargo fmt --all

lint:
    cargo clippy -- -D warnings

test:
    cargo test
```

## Mise Integration

When a project uses [mise](https://mise.jdx.dev) for tool version management, just recipes should use `mise exec` to ensure pinned versions are used regardless of developer shell setup.

**See the `mise` skill** for full mise setup including shell config, direnv integration, and project `.mise.toml` patterns.

### Shell Override (Recommended)

```just
# All recipes automatically use mise-pinned tools
set shell := ["mise", "exec", "--", "bash", "-c"]

build:
    npm run build

test:
    go test ./...
```

### Graceful Degradation

For repos where mise is optional:

```just
set shell := ["bash", "-c"]

# Use mise if available, otherwise fall back to PATH
_exec cmd:
    #!/usr/bin/env bash
    if command -v mise &>/dev/null; then
        mise exec -- {{cmd}}
    else
        {{cmd}}
    fi

build: (_exec "npm run build")
test: (_exec "go test ./...")
lint: (_exec "golangci-lint run")
```

Note: No `.mise.toml` check needed - mise traverses parent directories automatically.

### Why This Matters

| Developer Setup | Without mise exec | With mise exec |
|-----------------|-------------------|----------------|
| Has direnv + mise | Correct versions | Correct versions |
| Has mise activate | Correct versions | Correct versions |
| Fresh clone, no setup | System tools (wrong version) | Pinned versions |
| CI/CD | Needs activation step | Just works |

**Recommendation**: Use the shell override for team repos. Use graceful degradation for open source where mise adoption varies.

### Caveats

**Failure mode**: Shell override + mise not installed = cryptic "could not find shell" error. Use graceful degradation for open source.

**First clone**: Contributors must run `mise trust` to allow the repo's config:

```just
setup:
    mise trust
    mise install
    @echo "Toolchain ready"
```

---

## Security Auditing

All language templates include consistent audit recipes:

| Recipe | Purpose |
|--------|---------|
| `audit` | Check for vulnerabilities (informational) |
| `audit-fix` | Auto-fix where possible (npm only) |
| `audit-ci` | CI-friendly (strict, production deps only) |

**Language tools:**

| Language | Tool | Installation |
|----------|------|--------------|
| Node/npm | `npm audit` | Built-in |
| Go | `govulncheck` | `go get -tool golang.org/x/vuln/cmd/govulncheck@latest` |
| Rust | `cargo audit` | `cargo install cargo-audit` |

---

## Reference Templates

Load the appropriate template based on project structure:

| Template | Use Case |
|----------|----------|
| `references/simple-repo.just` | Single-package repositories |
| `references/monorepo-root.just` | Monorepo root router |
| `references/package-go.just` | Go package in monorepo |
| `references/package-ts.just` | TypeScript package in monorepo |
| `references/package-rust.just` | Rust package in monorepo |

**Note**: Reference files use `.just` extension for organization. Actual project files must be named `justfile` (no extension) or `.justfile`.
