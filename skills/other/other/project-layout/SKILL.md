---
name: project-layout
description: File and directory naming conventions for this project. Load when creating new files.
---

# Project Layout Conventions

This project follows conventions derived from the Go standard library and evolved through use. When in doubt, match existing patterns.

---

## Directory Structure

```
cmd/cooked/              # Single binary entry point
internal/                # All Go packages
embed/                   # go:embed assets (CSS, JS, templates)
testdata/                # Fixtures, golden files
```

**Rules:**
- All Go code lives in `internal/` — nothing is exported
- Subpackages only when crossing clear domain boundaries
- `embed/` holds downloaded assets populated by `make deps`

---

## File Naming Patterns

### Core Implementation Files

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `feature.go` | Primary implementation | `render.go`, `cache.go` |
| `feature_variant.go` | Variant of same feature | `render_mdx.go`, `cache_lru.go` |
| `feature_subtype.go` | Implementation by type | `render_markdown.go`, `render_code.go` |
| `feature_handlers.go` | HTTP handlers for feature | `render_handlers.go` |

### Test Files

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `feature_test.go` | Unit tests | `cache_test.go` |
| `feature_fuzz_test.go` | Fuzz tests (separate file) | `url_fuzz_test.go` |
| `feature_benchmark_test.go` | Benchmarks (when many) | `render_benchmark_test.go` |
| `feature_integration_test.go` | Integration tests | `server_integration_test.go` |
| `fixtures_test.go` | Shared test fixtures | `fixtures_test.go` |
| `helpers_test.go` | Shared test helpers | `helpers_test.go` |

**Fuzz tests MUST be in separate `*_fuzz_test.go` files.** Never mix with unit tests.

---

## Naming Decision Tree

### New feature file?

```
Is it HTTP handlers?
  YES → feature_handlers.go
  NO  → feature.go

Is it a variant of existing feature?
  YES → feature_variant.go (e.g., render_mdx.go)
  NO  → feature.go

Is it one of many implementations?
  YES → feature_type.go (e.g., render_markdown.go)
  NO  → feature.go
```

### New test file?

```
Is it a fuzz test?
  YES → feature_fuzz_test.go (ALWAYS separate)

Is it benchmarks only?
  YES → feature_benchmark_test.go (if many benchmarks)
  NO  → Add to feature_test.go

Is it integration (needs external services)?
  YES → feature_integration_test.go
  NO  → feature_test.go
```

---

## Package Organization

### When to Create Subpackages

Create a subpackage when:
- Domain is clearly separate
- Would cause import cycles otherwise
- Natural API boundary exists

Do NOT create subpackages for:
- Mere file organization
- "Cleaner" structure
- Matching patterns from other languages

### File Grouping Within Package

Group by feature prefix:

```
render.go               # Core rendering
render_markdown.go      # Markdown rendering
render_mdx.go           # MDX preprocessing
render_code.go          # Code file rendering
render_test.go          # All render tests
```

NOT by technical layer:

```
# WRONG - don't do this
handlers/render.go
config/render.go
```

---

## Test Data Location

```
testdata/           # Package-level fixtures
  golden/           # Golden files (expected HTML output)
  fixtures/         # Input fixtures (markdown, code files)
```

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| `utils/`, `helpers/`, `common/` | Dumping grounds — be specific |
| `models/`, `handlers/`, `services/` | Layer-based organization — use feature-based |
| Deep nesting (`internal/a/b/c/d/`) | Increases cognitive load |
| `pkg/` directory | Nothing is exported — use `internal/` |
| CamelCase file names | Go convention is `snake_case.go` |
| Generic `fuzz_test.go` | Use `feature_fuzz_test.go` per feature |

---

## Quick Reference

```
# New feature
feature.go
feature_test.go

# Feature with variants
feature.go
feature_variant.go
feature_test.go
feature_variant_test.go

# Feature with implementations
feature.go           # Interface + registry
feature_foo.go       # Foo implementation
feature_bar.go       # Bar implementation
feature_test.go      # All tests

# Feature with handlers
feature.go
feature_handlers.go
feature_test.go
feature_handlers_test.go

# Feature with fuzz tests
feature.go
feature_test.go
feature_fuzz_test.go
```
