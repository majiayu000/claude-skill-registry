---
name: make
description: |
    Use when automating build, test, and development tasks with language-agnostic task runners. Covers GNU Make, Just, and Task (Taskfile) — tools that provide a consistent interface for project commands across any tech stack.
    USE FOR: Make, Makefile, Just, Justfile, Task, Taskfile, task runners, build automation, project scripts, developer experience, cross-language build commands, phony targets
    DO NOT USE FOR: language-specific build systems (Gradle, MSBuild, webpack — use language-specific skills), CI/CD pipeline configuration, container orchestration
license: MIT
metadata:
  displayName: "Make & Task Runners"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "GNU Make Manual"
    url: "https://www.gnu.org/software/make/manual/"
  - title: "Just GitHub Repository"
    url: "https://github.com/casey/just"
  - title: "Task (Taskfile) Documentation"
    url: "https://taskfile.dev"
---

# Make & Task Runners

## Overview

Every project needs a way to run common commands (build, test, lint, deploy) without remembering the exact incantation. Make, Just, and Task provide a consistent `make build` or `just test` interface regardless of the underlying tech stack.

## Tool Comparison

| Feature | GNU Make | Just | Task |
|---------|----------|------|------|
| File | `Makefile` | `Justfile` | `Taskfile.yml` |
| Language | Make DSL | Custom DSL | YAML |
| Platform | Everywhere | Cross-platform binary | Cross-platform binary |
| Dependencies | Target-based | Recipe-based | Task-based |
| Variables | `$(VAR)` | `{{var}}` | `{{.VAR}}` |
| Shell | sh by default | sh/bash/pwsh | sh/bash/pwsh |
| Arguments | Limited | First-class | First-class |
| Install | Pre-installed on Unix | cargo/brew/choco | go install/brew/choco |

## GNU Make

### Makefile Anatomy

A Makefile consists of **targets**, **prerequisites**, and **recipes**. Recipes must be indented with a **tab** (not spaces).

```makefile
target: prerequisites
	recipe-command
```

Use `.PHONY` to declare targets that don't represent files:

```makefile
.PHONY: build test lint clean dev
```

### Example Makefile

A polyglot project with both Node.js and .NET:

```makefile
.PHONY: build test lint clean dev

build:
	npm run build
	dotnet build

test:
	npm test
	dotnet test

lint:
	npm run lint
	dotnet format --verify-no-changes

clean:
	rm -rf dist/ bin/ obj/ node_modules/

dev:
	npm run dev
```

### Variables

```makefile
APP_NAME := myapp
VERSION := 1.0.0

build:
	docker build -t $(APP_NAME):$(VERSION) .
```

### Automatic Variables

| Variable | Meaning |
|----------|---------|
| `$@` | The target name |
| `$<` | The first prerequisite |
| `$^` | All prerequisites |

### Include Other Makefiles

```makefile
include common.mk
```

### Conditional Logic

```makefile
ifeq ($(OS),Windows_NT)
	SHELL := powershell.exe
endif
```

## Just

### Justfile Syntax

Just is simpler than Make — no tab requirement, first-class arguments, and OS-conditional recipes:

```just
default:
    @just --list

build:
    npm run build
    dotnet build

test *args:
    npm test {{args}}
    dotnet test {{args}}

lint:
    npm run lint
    dotnet format --verify-no-changes

dev port="3000":
    PORT={{port}} npm run dev

# Run in PowerShell on Windows
[windows]
clean:
    Remove-Item -Recurse -Force dist, bin, obj, node_modules

[unix]
clean:
    rm -rf dist/ bin/ obj/ node_modules/
```

### Why Just over Make

- **No tab sensitivity** — indentation uses spaces, not tabs
- **Recipe arguments** — `just test --verbose` passes `--verbose` to the recipe
- **OS-conditional recipes** — `[windows]` and `[unix]` annotations for cross-platform support
- **Dotenv loading** — `set dotenv-load` to automatically load `.env` files
- **Better error messages** — clearer feedback when recipes fail

## Task (Taskfile)

### Taskfile.yml Syntax

```yaml
version: '3'

tasks:
  build:
    cmds:
      - npm run build
      - dotnet build

  test:
    cmds:
      - npm test
      - dotnet test

  lint:
    cmds:
      - npm run lint
      - dotnet format --verify-no-changes

  dev:
    cmds:
      - npm run dev
    env:
      PORT: 3000

  clean:
    cmds:
      - rm -rf dist/ bin/ obj/ node_modules/
```

### Why Task

- **YAML** — familiar syntax for anyone working with CI/CD, Kubernetes, or Docker Compose
- **Cross-platform** — single binary, works on Windows, macOS, and Linux
- **Task dependencies** — `deps: [build]` ensures prerequisites run first
- **Conditional execution** — skip tasks based on file changes or environment
- **Dotenv support** — automatically loads `.env` files
- **Watch mode** — `task --watch test` re-runs on file changes

## When to Use Which

| Scenario | Recommendation |
|----------|----------------|
| Already have a Makefile | Keep Make |
| New project on a mixed team | Just or Task |
| YAML-familiar team | Task |
| Need recipe arguments | Just or Task |
| Windows-first team | Just or Task |
| CI/CD scripts | Make — most compatible |

## Best Practices

- Put a Makefile, Justfile, or Taskfile in every project root — it serves as the entry point for all commands
- Use it as the single interface for all project operations — build, test, lint, format, deploy, clean
- Document available commands with `make help` / `just --list` / `task --list` so new developers can discover what's available
- Keep recipes simple — delegate to real build tools (npm, dotnet, cargo) rather than encoding complex logic in the task file
- Use task runners for developer experience, not as a replacement for language-specific build systems (Gradle, webpack, MSBuild)
- Commit the task file to version control and document it in the README so the whole team uses the same commands
