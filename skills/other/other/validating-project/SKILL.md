---
name: validating-project
description: Auto-detect and run formatters, linters, type checkers, and tests for the current project. Use when validating a project, running all checks, checking code quality before committing, or verifying the build passes.
context: fork
---

# Validating Project

Auto-detect project tooling and run validation steps in the correct order.

## Process

1. Check `./CLAUDE.md` for validation tools and project permissions
2. Auto-detect project type if needed (package.json, pyproject.toml, Cargo.toml, Makefile, go.mod)
3. Run validation pipeline: **Format -> Lint -> Type Check -> Test**
4. Stop immediately on failures
5. Report results

## Tool Commands by Project Type

### Make-based (check first -- overrides everything)

```bash
make format && make lint && make typecheck && make test
```

Or `make validate` if available.

### Python

```bash
uv run ruff format .
uv run ruff check .
uv run ty check        # or uv run mypy, uv run pyright
uv run pytest
```

### Node.js / TypeScript

```bash
pnpm run format        # or npx prettier --write .
pnpm run lint          # or npx eslint .
pnpm run typecheck     # or npx tsc --noEmit
pnpm test
```

### Rust

```bash
cargo fmt
cargo clippy
cargo test
```

### Go

```bash
gofmt -w .
go vet ./...
go test ./...
```

## Auto-Discovery Logic

```bash
# Priority order
if [ -f "Makefile" ]; then
  # Check for make validate/format/lint/test targets
elif [ -f "pyproject.toml" ]; then
  # Python -- check for uv, poetry
elif [ -f "package.json" ]; then
  # Node.js -- check for pnpm, npm, yarn
elif [ -f "Cargo.toml" ]; then
  # Rust
elif [ -f "go.mod" ]; then
  # Go
fi
```

## Error Handling

- **Tool not found**: Provide installation instructions
- **Configuration missing**: Suggest minimal setup
- **Validation failures**: Show specific fix recommendations
- **Dependency conflicts**: Suggest resolution strategies

## CLAUDE.md Integration

Cache discovered validation info in the project's CLAUDE.md:

```markdown
## Project Validation Tools

- **Format**: make format
- **Lint**: make lint
- **Type Check**: make typecheck
- **Test**: make test
```
