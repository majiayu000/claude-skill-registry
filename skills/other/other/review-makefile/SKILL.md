---
name: review-makefile
description: Review Makefiles for best practices, clean code, and proper structure. Use when reviewing, writing, or refactoring Makefiles. Enforces self-documenting help targets, proper PHONY declarations, safety settings, and idiomatic patterns.
---

# Review Makefile - Best Practices & Standards

Apply these standards when writing or reviewing Makefiles to ensure they are clean, maintainable, and follow GNU Make best practices.

## Core Principles

1. **Self-documenting help**: Use comments to auto-generate help text
2. **Safety first**: Include prologue with error handling and safety settings
3. **Explicit PHONY**: Declare all phony targets immediately before definition
4. **Automatic variables**: Use `$@`, `$<`, `$^` to avoid repetition
5. **Consistent naming**: Lowercase internal variables, UPPERCASE environment variables
6. **Minimal recursion**: Avoid recursive make; keep dependency graph in one place

---

## Code Review Checklist

When reviewing Makefiles, ensure:

- **Prologue present**: Safety settings configured (.DELETE_ON_ERROR, SHELL, .SHELLFLAGS)
- **PHONY declarations**: All phony targets explicitly declared
- **Self-documenting help**: Help target auto-generated from ## comments
- **Automatic variables**: Using $@, $<, $^ instead of repeating names
- **Tab indentation**: Recipes use TABs not spaces
- **Variable assignment**: Using := (immediate) instead of = (recursive) unless needed
- **Dependencies declared**: All file prerequisites properly specified
- **Clean target**: Removes all generated files

---

## Prologue Section - Safety Settings

Every Makefile should start with a prologue that sets up safety defaults:

```makefile
# GOOD: Comprehensive prologue
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

# BAD: No prologue, no safety settings
# (missing entirely)
```

### What each setting does:

- **--warn-undefined-variables**: Catches misspelled variable names
- **SHELL := bash**: Explicitly set shell (default is /bin/sh)
- **.SHELLFLAGS := -eu -o pipefail -c**: 
  - `-e`: Exit on error
  - `-u`: Error on undefined variables
  - `-o pipefail`: Pipeline fails if any command fails
  - `-c`: Required for make to pass script to bash
- **.DEFAULT_GOAL := all**: Sets default target (first target otherwise)
- **.DELETE_ON_ERROR**: Remove target if recipe fails
- **.SUFFIXES**: Disable built-in suffix rules for clarity

---

## Self-Documenting Help Target

The best practice is to use `##` comments on targets and auto-generate help:

```makefile
# GOOD: Self-documenting help using comments
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build all crates
	cargo build --workspace

.PHONY: test
test: ## Run all tests
	cargo test --workspace

.PHONY: clean
clean: ## Remove build artifacts
	cargo clean

# BAD: Hardcoded help text (maintenance burden)
help:
	@echo "Featherflow Development Makefile"
	@echo ""
	@echo "Development:"
	@echo "  make build              Build all crates"
	@echo "  make test               Run all tests"
	# ... 50+ lines of manually maintained help text
	# Problem: Easy to forget to update when targets change
```

### Enhanced self-documenting help with sections:

```makefile
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment Variables:"
	@echo "  PROJECT_DIR    Path to test project (default: tests/fixtures/sample_project)"

# Use double-hash comments for targets that should appear in help
.PHONY: build
build: ## Build all crates in the workspace
	cargo build --workspace

# Use single-hash for internal comments
# This internal target won't appear in help
.PHONY: internal-setup
internal-setup:
	mkdir -p build
```

---

## PHONY Target Declarations

Declare ALL phony targets explicitly to prevent conflicts with files:

```makefile
# GOOD: Declare phony immediately before target definition
.PHONY: clean
clean: ## Remove build artifacts
	cargo clean
	rm -rf target

.PHONY: test
test: ## Run all tests
	cargo test --workspace

.PHONY: install
install: ## Install the CLI binary
	cargo install --path crates/ff-cli

# ACCEPTABLE: Group related phony targets
.PHONY: build build-release build-target
build: ## Build debug binaries
	cargo build --workspace

build-release: ## Build release binaries
	cargo build --workspace --release

build-target: ## Build for specific target (set TARGET=...)
	cargo build --release --target $(TARGET)

# BAD: All phony targets at the top (hard to maintain)
.PHONY: build test clean install fmt lint doc
# ... 100 lines later
build:
	cargo build
# Problem: Easy to forget to add new targets to .PHONY list
```

---

## Automatic Variables

Use automatic variables to avoid repetition and improve maintainability:

```makefile
# GOOD: Using automatic variables
%.o: %.c
	$(CC) -c $< -o $@
	# $< = first prerequisite (%.c)
	# $@ = target (%.o)
	# $^ = all prerequisites

build/report.pdf: report.md template.tex
	pandoc $< --template=$(word 2,$^) -o $@
	# $< = report.md (first prereq)
	# $(word 2,$^) = template.tex (second prereq)
	# $@ = build/report.pdf (target)

# BAD: Repeating filenames
%.o: %.c
	$(CC) -c foo.c -o foo.o
	# Hard to maintain, doesn't scale

# Key automatic variables:
# $@ - Target name
# $< - First prerequisite
# $^ - All prerequisites (deduplicated)
# $+ - All prerequisites (with duplicates)
# $? - Prerequisites newer than target
# $* - Stem of pattern match (e.g., "foo" in "foo.o")
```

---

## Variable Conventions

Follow consistent variable naming and assignment:

```makefile
# GOOD: Proper variable conventions
# Environment variables: UPPERCASE with ?= (conditional assignment)
PROJECT_DIR ?= tests/fixtures/sample_project
CC ?= gcc
CFLAGS ?= -Wall -O2

# Internal variables: lowercase with := (immediate assignment)
sources := $(wildcard src/*.c)
objects := $(sources:.c=.o)
binary_name := myapp

# GOOD: Use := for immediate evaluation
files := $(wildcard *.txt)
count := $(words $(files))

# ACCEPTABLE: Use = for recursive evaluation when needed
# (usually only needed for variables that reference undefined vars)
late_binding = $(some_var_defined_later)

# BAD: Mixing conventions
projectdir = tests/fixtures/sample_project  # Should be PROJECT_DIR ?=
CC := gcc  # Should be CC ?= to allow override
Sources := $(wildcard src/*.c)  # Should be lowercase

# BAD: Using = when := is sufficient
files = $(wildcard *.txt)  # Use := for immediate evaluation
```

---

## Makefile Organization

Structure your Makefile into clear sections:

```makefile
# GOOD: Well-organized Makefile
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

# =============================================================================
# Configuration / Environment Variables
# =============================================================================

PROJECT_DIR ?= tests/fixtures/sample_project
RUST_BACKTRACE ?= 1

# =============================================================================
# Internal Variables
# =============================================================================

cargo := cargo
rust_flags := --workspace
project_flag := --project-dir $(PROJECT_DIR)

# =============================================================================
# Development
# =============================================================================

.PHONY: build
build: ## Build all crates
	$(cargo) build $(rust_flags)

.PHONY: watch
watch: ## Watch and rebuild on changes
	cargo watch -x 'build $(rust_flags)'

# =============================================================================
# Testing
# =============================================================================

.PHONY: test
test: ## Run all tests
	$(cargo) test $(rust_flags)

.PHONY: test-verbose
test-verbose: ## Run tests with output
	$(cargo) test $(rust_flags) -- --nocapture

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: lint
lint: fmt-check clippy ## Run all linters

.PHONY: fmt
fmt: ## Format code
	$(cargo) fmt --all

.PHONY: fmt-check
fmt-check: ## Check code formatting
	$(cargo) fmt --all -- --check

.PHONY: clippy
clippy: ## Run clippy linter
	$(cargo) clippy $(rust_flags) --all-targets -- -D warnings

# =============================================================================
# Maintenance
# =============================================================================

.PHONY: clean
clean: ## Remove build artifacts
	$(cargo) clean
	rm -rf $(PROJECT_DIR)/target

# =============================================================================
# Help
# =============================================================================

.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
```

---

## Common Patterns

### Multi-target rules with shared recipe

```makefile
# GOOD: Shared recipe for multiple targets
.PHONY: ff-parse ff-compile ff-run
ff-parse ff-compile ff-run: ff-%: ## CLI: Run ff command (parse/compile/run)
	cargo run -p ff-cli -- $(project_flag) $*

# This creates three targets that share logic
# $* captures the stem (parse, compile, or run)

# ALTERNATIVE: Explicit targets when recipes differ slightly
.PHONY: ff-parse
ff-parse: ## Parse SQL files
	cargo run -p ff-cli -- $(project_flag) parse

.PHONY: ff-compile
ff-compile: ## Compile Jinja templates
	cargo run -p ff-cli -- $(project_flag) compile

.PHONY: ff-run
ff-run: ## Execute compiled SQL
	cargo run -p ff-cli -- $(project_flag) run
```

### Composite targets

```makefile
# GOOD: Composite workflow targets
.PHONY: ci
ci: fmt-check clippy test doc ## Run all CI checks
	@echo "✓ CI checks passed!"

.PHONY: dev-cycle
dev-cycle: ff-seed ff-run ff-test ## Full development cycle
	@echo "✓ Development cycle complete!"

# Use order-only prerequisites for directories
build/%.o: src/%.c | build
	$(CC) -c $< -o $@

build:
	mkdir -p build
```

### Parameterized targets

```makefile
# GOOD: Support parameters via environment variables
.PHONY: ff-run-select
ff-run-select: ## Run specific models (set MODELS='+model_name')
	@if [ -z "$(MODELS)" ]; then \
		echo "Error: MODELS not set. Usage: make ff-run-select MODELS='+model_name'"; \
		exit 1; \
	fi
	cargo run -p ff-cli -- $(project_flag) run --select $(MODELS)

# GOOD: Provide usage hints in help text
.PHONY: build-target
build-target: ## Build for target platform (set TARGET=x86_64-unknown-linux-gnu)
	@if [ -z "$(TARGET)" ]; then \
		echo "Error: TARGET not set"; \
		echo "Usage: make build-target TARGET=x86_64-unknown-linux-gnu"; \
		exit 1; \
	fi
	cargo build --release --target $(TARGET) -p ff-cli
```

### Silent commands

```makefile
# GOOD: Use @ to silence echo for user-facing output
.PHONY: status
status: ## Show project status
	@echo "Project: $(PROJECT_DIR)"
	@echo "Build status: checking..."
	@cargo check --quiet && echo "✓ Build OK" || echo "✗ Build failed"

# GOOD: Keep @ off for debugging/commands you want to see
.PHONY: debug-build
debug-build: ## Build with debug output
	cargo build --workspace --verbose

# BAD: Overusing @ hides useful information
clean:
	@cargo clean
	@rm -rf target
	# Problem: User can't see what's being cleaned
```

---

## Anti-Patterns to Avoid

### Don't use recursive make

```makefile
# BAD: Recursive make (loses dependency graph)
.PHONY: build-all
build-all:
	cd subproject1 && $(MAKE)
	cd subproject2 && $(MAKE)

# GOOD: Use include or workspaces instead
# For Rust workspaces, just use cargo's built-in workspace support
.PHONY: build-all
build-all:
	cargo build --workspace
```

### Don't hardcode paths unnecessarily

```makefile
# BAD: Hardcoded paths
test:
	cargo test --manifest-path /Users/bob/project/Cargo.toml

# GOOD: Use relative paths and variables
MANIFEST_PATH ?= Cargo.toml

.PHONY: test
test:
	cargo test --manifest-path $(MANIFEST_PATH)
```

### Don't mix tabs and spaces

```makefile
# BAD: Using spaces for indentation (Make will fail)
build:
    cargo build  # These are spaces!

# GOOD: Use TAB character
build:
	cargo build  # This is a TAB
```

---

## Testing and Validation

### Pattern for validation targets

```makefile
# GOOD: Clear validation with helpful output
.PHONY: check-rust
check-rust: ## Verify Rust is installed
	@which cargo > /dev/null || (echo "Error: Rust not installed. Visit https://rustup.rs" && exit 1)
	@echo "✓ Rust is installed"

.PHONY: check-deps
check-deps: check-rust ## Check all dependencies
	@echo "✓ All dependencies satisfied"

# GOOD: CI target that fails fast
.PHONY: ci
ci: check-deps fmt-check clippy test ## Run CI checks
	@echo "✓ All CI checks passed!"
```

---

## Real-World Example: Before and After

### Before (Current Anti-Patterns):

```makefile
# No prologue section
# No .PHONY declarations near targets
.PHONY: build build-release test lint fmt check doc clean ci ...

PROJECT_DIR ?= tests/fixtures/sample_project

build:
	cargo build --workspace

# Hardcoded help text (80+ lines)
help:
	@echo "Featherflow Development Makefile"
	@echo ""
	@echo "Development:"
	@echo "  make build              Build all crates"
	# ... many more hardcoded lines
```

### After (Following Best Practices):

```makefile
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

# =============================================================================
# Configuration
# =============================================================================

PROJECT_DIR ?= tests/fixtures/sample_project

# =============================================================================
# Development
# =============================================================================

.PHONY: build
build: ## Build all crates
	cargo build --workspace

.PHONY: build-release
build-release: ## Build release binaries
	cargo build --workspace --release

# =============================================================================
# Testing
# =============================================================================

.PHONY: test
test: ## Run all tests
	cargo test --workspace

# =============================================================================
# Help
# =============================================================================

.PHONY: help
help: ## Show this help message (default target)
	@echo "Featherflow Development Makefile"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment Variables:"
	@echo "  PROJECT_DIR    Test project path (default: tests/fixtures/sample_project)"
```

---

## Summary

When reviewing or writing Makefiles:

1. **Always include the prologue** with safety settings
2. **Use self-documenting help** with `## ` comments
3. **Declare .PHONY immediately before targets** for clarity
4. **Use automatic variables** ($@, $<, $^) to reduce repetition
5. **Follow naming conventions** (UPPERCASE env vars, lowercase internal vars)
6. **Organize into sections** with clear headers
7. **Avoid recursive make** - keep dependency graph unified
8. **Use := for immediate evaluation** unless recursive needed
9. **Tab indent recipes**, never spaces
10. **Make help the default** target for discoverability

For more advanced patterns and examples, see [examples.md](examples.md).

---

## Verification

**After every unit of work, run `make ci` before moving on.** This ensures format, clippy, tests, and docs all pass. Do not proceed to the next task until CI is green.
