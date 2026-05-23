---
name: makefile-generation
description: Generate language-specific Makefile with common development targets

Triggers: language-specific, makefile, development, targets, generation
model: claude-sonnet-4
tools: [Read, Write, Bash]
---
## Table of Contents

- [Use When](#use-when)
- [Standard Targets](#standard-targets)
- [Python Makefile](#python-makefile)
- [Rust Makefile](#rust-makefile)
- [TypeScript Makefile](#typescript-makefile)
- [Workflow](#workflow)
- [1. Detect Language](#1-detect-language)
- [2. Load Template](#2-load-template)
- [3. Collect Project Info](#3-collect-project-info)
- [4. Render Template](#4-render-template)
- [5. Verify](#5-verify)
- [Customization](#customization)
- [Related Skills](#related-skills)


# Makefile Generation Skill

Generate a Makefile with standard development targets for Python, Rust, or TypeScript projects.

## Use When

- Need a Makefile for a project without one
- Want to update Makefile with new targets
- Standardizing build automation across projects

## Standard Targets

### Python Makefile

**Common targets**:
- `help` - Show available targets
- `install` - Install dependencies with uv
- `lint` - Run ruff linting
- `format` - Format code with ruff
- `typecheck` - Run mypy type checking
- `test` - Run pytest
- `test-coverage` - Run tests with coverage report
- `check-all` - Run all quality checks
- `clean` - Remove generated files and caches
- `build` - Build distribution packages
- `publish` - Publish to PyPI

### Rust Makefile

**Common targets**:
- `help` - Show available targets
- `fmt` - Format with rustfmt
- `lint` - Run clippy
- `check` - Cargo check
- `test` - Run tests
- `build` - Build release binary
- `clean` - Clean build artifacts

### TypeScript Makefile

**Common targets**:
- `help` - Show available targets
- `install` - Install npm dependencies
- `lint` - Run ESLint
- `format` - Format with Prettier
- `typecheck` - Run tsc type checking
- `test` - Run Jest tests
- `build` - Build for production
- `dev` - Start development server

## Workflow

### 1. Detect Language

```bash
# Check for language indicators
if [ -f "pyproject.toml" ]; then
    LANGUAGE="python"
elif [ -f "Cargo.toml" ]; then
    LANGUAGE="rust"
elif [ -f "package.json" ]; then
    LANGUAGE="typescript"
fi
```
**Verification:** Run the command with `--help` flag to verify availability.

### 2. Load Template

```python
from pathlib import Path

template_path = Path("plugins/attune/templates") / language / "Makefile.template"
```
**Verification:** Run the command with `--help` flag to verify availability.

### 3. Collect Project Info

```python
metadata = {
    "PROJECT_NAME": "my-project",
    "PROJECT_MODULE": "my_project",
    "PYTHON_VERSION": "3.10",
}
```
**Verification:** Run the command with `--help` flag to verify availability.

### 4. Render Template

```python
from template_engine import TemplateEngine

engine = TemplateEngine(metadata)
engine.render_file(template_path, Path("Makefile"))
```
**Verification:** Run the command with `--help` flag to verify availability.

### 5. Verify

```bash
make help
```
**Verification:** Run `make --dry-run` to verify build configuration.

## Customization

Users can add custom targets after the generated ones:

```makefile
# ============================================================================
# CUSTOM TARGETS
# ============================================================================

deploy: build ## Deploy to production
	./scripts/deploy.sh
```
**Verification:** Run the command with `--help` flag to verify availability.

## Related Skills

- `Skill(attune:project-init)` - Full project initialization
- `Skill(abstract:makefile-dogfooder)` - Makefile testing and validation
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
