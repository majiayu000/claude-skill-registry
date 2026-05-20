---
name: setup-validation
description: Set up a build/test/lint validation loop for the current project. Detects the tech stack and configures CLAUDE.md with verification commands.
disable-model-invocation: true
---

# Setup Validation Loop

Detect the project's tech stack and configure a build/test/lint validation loop in CLAUDE.md.

## Usage

`/setup-validation`

## Procedure

### Step 1: Detect Tech Stack

Scan the project root for configuration files to identify:

| File | Indicates |
|------|-----------|
| `package.json` | Node.js / JavaScript / TypeScript |
| `tsconfig.json` | TypeScript |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pyproject.toml` or `setup.py` or `requirements.txt` | Python |
| `Gemfile` | Ruby |
| `pom.xml` or `build.gradle` | Java/Kotlin |
| `Makefile` | Make-based build |
| `CMakeLists.txt` | C/C++ |
| `.csproj` or `*.sln` | .NET / C# |

### Step 2: Detect Build System

Based on detected stack, identify the build command:

- **Node.js**: Check `package.json` scripts for `build`, `compile`, or `tsc`
- **Rust**: `cargo build`
- **Go**: `go build ./...`
- **Python**: Check for `build` in pyproject.toml, or `python -m build`
- **Make**: `make` or `make all`

If no build step is found, note that as acceptable (some projects don't need one).

### Step 3: Detect Test Runner

Identify the test command:

- **Node.js**: Check for `jest`, `vitest`, `mocha`, `ava` in devDependencies. Check `package.json` scripts for `test`
- **Rust**: `cargo test`
- **Go**: `go test ./...`
- **Python**: Check for `pytest`, `unittest`, `nose2`. Look for `pytest.ini` or `[tool.pytest]` in pyproject.toml
- **Ruby**: `bundle exec rspec` or `rake test`
- **Java**: `mvn test` or `gradle test`

Also detect single-file test commands (e.g., `pytest path/to/test.py`) for faster iteration.

### Step 4: Detect Linter/Formatter

Identify lint and format commands:

- **Node.js**: Check for `eslint`, `prettier`, `biome` in devDependencies. Check scripts for `lint`, `format`
- **Rust**: `cargo clippy` (lint), `cargo fmt` (format)
- **Go**: `golangci-lint run` (lint), `gofmt` (format)
- **Python**: Check for `ruff`, `flake8`, `black`, `isort`. Prefer `ruff check` + `ruff format` if available
- **Ruby**: `rubocop`

### Step 5: Present Proposed Validation Loop

Show the user what was detected:

```
## Detected Validation Loop

Tech stack: [language] + [framework]
Build:      [command or "none needed"]
Test (all): [command]
Test (one): [command] [file]
Lint:       [command]
Format:     [command]
```

Ask the user to confirm or modify.

### Step 6: Update CLAUDE.md

Add or update a "Build & Validation" section in `./CLAUDE.md`:

```markdown
## Build & Validation

- Build: `[command]`
- Test all: `[command]`
- Test single file: `[command] [path]`
- Lint: `[command]`
- Format: `[command]`

Always run the test command after making changes. Run lint before committing.
```

If `CLAUDE.md` doesn't exist, create it with this section.
If it exists, append this section (or update it if the section already exists).

### Step 7: Offer Hook Setup

Ask the user if they'd like to auto-run the formatter after every file edit:

> "Would you like to set up a PostToolUse hook to auto-format files after edits? This runs your formatter automatically whenever Claude edits a file."

If yes, suggest running `/setup-hooks` to configure it.
