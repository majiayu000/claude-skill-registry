---
name: coding-standards
description: Apply corbat-coco coding standards to a project being built. Adapts standards based on the detected stack (TypeScript, Python, Java, Go). Generates a CODING_STANDARDS.md file for the user's project.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Coding Standards

Generate and apply coding standards for the user's project based on their stack.

## Step 1: Detect Stack

```bash
ls package.json tsconfig.json pyproject.toml pom.xml go.mod 2>/dev/null
cat package.json 2>/dev/null | grep '"main"\|"type"\|"dependencies"' | head -10
```

## Step 2: Apply Stack-Specific Standards

### TypeScript/Node.js
- ESM only (`"type": "module"` in package.json)
- TypeScript strict mode
- Imports with `.js` extension
- Vitest for testing (80%+ coverage)
- oxlint + prettier/oxfmt
- Zod for validation
- No `any`, no `console.log` in production

### Python
- Type hints everywhere (`def foo(x: int) -> str:`)
- `dataclasses` or `pydantic` for data models
- pytest for testing (80%+ coverage)
- `ruff` for linting + formatting
- `mypy` for type checking
- Virtual environments (`venv` or `uv`)
- No bare `except:` — always catch specific exceptions

### Java/Spring Boot
- Java 21+ with records, sealed classes, pattern matching
- Spring Boot 3.x with virtual threads
- Constructor injection (no field injection)
- Hexagonal/ports-adapters architecture
- JUnit 5 + Mockito for testing (80%+ coverage)
- Checkstyle + Spotbugs
- No `null` — use `Optional<T>` or explicit null checks

### Go
- Go 1.21+ with generics
- `errors.Is` / `errors.As` for error handling
- Table-driven tests with `testing` package
- `golangci-lint` for linting
- No naked returns
- Always check errors (no `_` for errors)
- `context.Context` as first parameter for IO functions

## Step 3: Generate Standards Document

Create `CODING_STANDARDS.md` in the project root:

```markdown
# Coding Standards — [Project Name]

## Language: [Detected Language]
## Framework: [Detected Framework]

## Style
[Stack-specific style rules]

## Testing
[Stack-specific test requirements]

## Security
[Stack-specific security rules]

## Quality Thresholds
- Test coverage: 80%+
- Lint: zero warnings
- Type safety: strict mode enabled
```

## Usage

```
/coding-standards          # detect stack and generate standards
/coding-standards typescript  # force TypeScript standards
/coding-standards python      # force Python standards
/coding-standards java        # force Java standards
/coding-standards go          # force Go standards
```
