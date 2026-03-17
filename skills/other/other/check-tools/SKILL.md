---
name: check-tools
description: Validates development tool installations across Python, Node.js, Java, Go, Rust, C/C++, Git, and system utilities. Use when verifying environments or troubleshooting dependencies.
metadata:
  version: 1.1.3
---

# Check Tools - Development Environment Validator

## Core Philosophy

Systematically verify tool presence and versions across major programming ecosystems. Provide actionable feedback about availability and validate complete toolchains with awareness of interdependencies (e.g., Node.js requires npm).

## Environment Compatibility

This skill supports flexible validation modes:
- **Strict mode**: Fail on missing core tools (python3, node, git, gcc)
- **Lenient mode**: Report all tools but only warn on optional ones
- **Custom mode**: Define required vs optional tools per project

Default behavior reports all tools without failing validation, suitable for diverse PaaS environments.

## When to Use This Skill

Trigger this skill when working on:

- **Environment setup verification** - Validating that all required tools are installed
- **Troubleshooting build failures** - Checking for missing dependencies or version mismatches
- **Documentation generation** - Creating system requirements documentation
- **CI/CD pipeline setup** - Ensuring container images have required tools
- **Onboarding new developers** - Verifying development environment readiness
- **Cross-platform development** - Checking tool availability across different operating systems
- **Polyglot projects** - Validating toolchains for multiple programming languages

## Tool Categories

### 1. Python Ecosystem

**Core Tools** (typically available):
- `python3`, `python` - Python interpreters ✅
- `pip` - Package installer ✅
- `uv` - Fast Python package installer ✅

**Development Tools** (install as needed):
- `poetry` - Dependency management and packaging
- `black` - Code formatter
- `mypy` - Static type checker
- `pytest` - Testing framework
- `ruff` - Fast Python linter

**Validation Pattern**:
```bash
if command -v python3 &> /dev/null; then
    python3 --version
fi
```

### 2. Node.js Ecosystem

**Core Tools** (typically available):
- `node` - Node.js runtime ✅
- `npm` - Package manager ✅

**Development Tools** (install as needed):
- `nvm` - Node version manager
- `yarn` - Fast, reliable package manager
- `pnpm` - Efficient disk space package manager
- `eslint` - JavaScript linter
- `prettier` - Code formatter
- `chromedriver` - Browser automation

**Validation Pattern**:
```bash
if command -v node &> /dev/null; then
    node --version
    # Check for multiple Node versions via nvm
    if [[ -s "/opt/nvm/nvm.sh" ]]; then
        source "/opt/nvm/nvm.sh"
        nvm list
    fi
fi
```

### 3. Java Ecosystem

**Core Tools** (typically available):
- `java` - Java runtime and compiler ✅

**Build Tools** (install as needed):
- `mvn` - Maven build tool
- `gradle` - Gradle build tool

**Validation Pattern**:
```bash
if command -v java &> /dev/null; then
    java -version 2>&1 | head -3
fi
```

### 4. Go Ecosystem

**Development Tools** (install as needed):
- `go` - Go compiler and toolchain

**Validation Pattern**:
```bash
if command -v go &> /dev/null; then
    go version
fi
```

### 5. Rust Ecosystem

**Development Tools** (install as needed):
- `rustc` - Rust compiler
- `cargo` - Rust package manager and build tool

**Environment Setup**:
```bash
# Source cargo environment if it exists
if [[ -f "$HOME/.cargo/env" ]]; then
    source "$HOME/.cargo/env"
fi
```

### 6. C/C++ Ecosystem

**Core Tools** (typically available):
- `gcc` - GNU Compiler Collection ✅

**Build Tools** (install as needed):
- `clang` - LLVM C/C++ compiler
- `cmake` - Cross-platform build system
- `ninja` - Small build system with focus on speed
- `conan` - C/C++ package manager

**Validation Pattern**:
```bash
if command -v gcc &> /dev/null; then
    gcc --version | head -1
fi
```

### 7. System Utilities

**Core Tools** (typically available):
- `git` - Version control ✅
- `curl` - Data transfer tool ✅
- `awk` - Pattern scanning and processing ✅
- `sed` - Stream editor ✅
- `grep` - Pattern matching ✅
- `gzip` - File compression ✅
- `tar` - Archive utility ✅
- `make` - Build automation ✅

**Development Tools** (install as needed):
- `jq` - JSON processor
- `rg` (ripgrep) - Fast text search
- `tmux` - Terminal multiplexer
- `yq` - YAML processor
- `vim` - Vi improved
- `nano` - Simple text editor

## Validation Strategies

### Basic Presence & Version Check

Combine tool detection with version extraction:

```bash
check_tool() {
    local tool=$1
    local required=${2:-false}

    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool: $($tool --version 2>&1 | head -1)"
        return 0
    else
        if [[ "$required" == "true" ]]; then
            echo "❌ $tool: not found (REQUIRED)"
            return 1
        else
            echo "⚠️  $tool: not found (optional)"
            return 0
        fi
    fi
}

# Usage
check_tool python3 true   # Required
check_tool poetry false   # Optional
```

### Environment-Specific Loading

Some tools require environment setup before detection:

```bash
# Load version managers if present
[[ -f "$HOME/.nvm/nvm.sh" ]] && source "$HOME/.nvm/nvm.sh"
[[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"

# Then check tools
check_tool node true
check_tool cargo false
```

## Output Formatting

### Visual Indicators

- ✅ Tool found and working
- ❌ Tool not found or not working
- ⚠️  Tool optional but recommended

### Categorical Organization

Group tools by ecosystem for clarity:

```
=================== Python ===================
✅ python3: Python 3.11.4
✅ pip: pip 23.1.2
✅ poetry: Poetry (version 1.5.1)
❌ mypy: not found

=================== NodeJS ===================
✅ node: v20.5.0
✅ npm: 9.8.0
...
```

### ASCII Art Banners

Create visually appealing output for tool reports:

```bash
cat << 'EOF'
   _____ _                 _        _____           _
  / ____| |               | |      / ____|         | |
 | |    | | __ _ _   _  __| | ___  | |     ___   __| | ___
 | |    | |/ _` | | | |/ _` |/ _ \ | |    / _ \ / _` |/ _ \
 | |____| | (_| | |_| | (_| |  __/ | |___| (_) | (_| |  __/
  \_____|_|\__,_|\__,_|\__,_|\___|  \_____\___/ \__,_|\___|

      Development Environment Tool Versions
      =====================================
EOF
```

## Common Use Cases

### 1. Container/Docker Environment Validation

When setting up development containers, validate that all required tools are installed:

```bash
#!/bin/bash
# Validate Python data science environment
check_tool python3 "required"
check_tool pip "required"
check_tool jupyter "required"
check_tool pandas "optional - data analysis"
check_tool numpy "optional - numerical computing"
```

### 2. CI/CD Pipeline Health Checks

Add environment validation as the first step in CI pipelines:

```yaml
# .github/workflows/validate.yml
steps:
  - name: Validate Build Environment
    run: |
      ./scripts/check-tools.sh
      if [ $? -ne 0 ]; then
        echo "Build environment validation failed"
        exit 1
      fi
```

## Implementation Patterns

### Modular Validation Functions

```bash
validate_python_tools() {
    local failed=0

    for tool in python3 pip poetry pytest black; do
        if ! command -v "$tool" &> /dev/null; then
            echo "❌ $tool: not found"
            failed=1
        else
            echo "✅ $tool: $($tool --version 2>&1 | head -1)"
        fi
    done

    return $failed
}
```

### Cross-Platform Considerations

```bash
case "$(uname -s)" in
    Linux*) check_linux_tools ;;
    Darwin*) check_macos_tools ;;
esac
```

## Best Practices

1. **Fail on missing core tools only** - python3, node, git, gcc must be present
2. **Source environments first** - Load nvm, cargo before checking tools
3. **Show versions, not just presence** - Use `tool --version 2>&1 | head -1`
4. **Use visual indicators** - ✅ (available), ❌ (required missing), ⚠️ (optional missing)
5. **Return proper exit codes** - 0 for success, 1 for missing required tools

## Quick Reference: Tool Availability

| Ecosystem | Core (typically present) | Optional (install as needed) |
|-----------|-------------------------|------------------------------|
| Python    | python3, pip, uv        | poetry, black, mypy, pytest, ruff |
| Node.js   | node, npm               | nvm, yarn, pnpm, eslint, prettier |
| Java      | java                    | maven, gradle |
| Go        | -                       | go |
| Rust      | -                       | rustc, cargo |
| C/C++     | gcc                     | clang, cmake, ninja, conan |
| Utils     | git, curl, awk, grep, sed, tar, make, gzip | jq, rg, tmux, yq, vim, nano |

Use `check_required_tool` for core tools, `check_optional_tool` for others.

## Constraints

**DO**: Use `command -v` for detection, source environments (nvm, cargo) first, handle stderr for versions, group by ecosystem, return proper exit codes
**DON'T**: Assume paths, hardcode locations, ignore stderr, mark all tools as required

## Reference Files

- **`assets/check-tools.sh`**: Focused development tool validation script (exit codes, quick checks)
- **`assets/environment-diagnostic.sh`**: Comprehensive system and tool diagnostic with three modes:
  - `tools` - Development tools only (fast validation)
  - `system` - System info, hardware, mounts, processes
  - `full` - Complete diagnostic with package inventories
- **`references/tool-categories.md`**: Detailed breakdown of tools by category with installation instructions

## Validation Checklist

Before delivering, verify:
- [ ] Core tools marked required, others optional
- [ ] Environments sourced (nvm, cargo) before checking
- [ ] Versions extracted correctly (handle stderr)
- [ ] Visual indicators consistent (✅/❌/⚠️)
- [ ] Exit code 0 for success, 1 only for missing core tools

## Example Output

```
   _____ _                 _        _____           _
  / ____| |               | |      / ____|         | |
 | |    | | __ _ _   _  __| | ___  | |     ___   __| | ___
 | |    | |/ _` | | | |/ _` |/ _ \ | |    / _ \ / _` |/ _ \
 | |____| | (_| | |_| | (_| |  __/ | |___| (_) | (_| |  __/
  \_____|_|\__,_|\__,_|\__,_|\___|  \_____\___/ \__,_|\___|

      Development Environment Tool Versions
      =====================================

=================== Python ===================
✅ python3: Python 3.12.3
✅ pip: pip 24.0
✅ uv: uv 0.9.2
⚠️  poetry: not found (optional)
⚠️  black: not found (optional)
⚠️  mypy: not found (optional)
⚠️  pytest: not found (optional)
⚠️  ruff: not found (optional)

=================== NodeJS ===================
✅ node: v22.20.0
✅ npm: 10.9.3
⚠️  nvm: not found (optional)
⚠️  yarn: not found (optional)
⚠️  pnpm: not found (optional)

=================== Java ===================
✅ java: openjdk 11.0.25 2024-10-15
⚠️  mvn: not found (optional)
⚠️  gradle: not found (optional)

=================== C/C++ ===================
✅ gcc: gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0

=================== System Utilities ===================
✅ git: git version 2.34.1
✅ curl: curl 7.81.0
✅ awk: GNU Awk 5.1.0
✅ sed: sed (GNU sed) 4.8
✅ grep: grep (GNU grep) 3.7
⚠️  jq: not found (optional)
⚠️  rg: not found (optional)

=================== Summary ===================
✅ All required tools present
   (Optional tools marked with ⚠️ can be installed as needed)
```

## Getting Started

### Quick Validation
```bash
# Fast tool check (exit code validation)
bash assets/check-tools.sh

# Development tools only
bash assets/environment-diagnostic.sh tools

# System diagnostics only
bash assets/environment-diagnostic.sh system

# Complete diagnostic with report
bash assets/environment-diagnostic.sh full /path/to/report.txt
```

### Customization
1. **For CI/CD**: Use `check-tools.sh` (fast, exit code based)
2. **For debugging**: Use `environment-diagnostic.sh full` (comprehensive)
3. **For onboarding**: Use `environment-diagnostic.sh tools` with package lists
4. **Modify required/optional**: Edit `check_required_tool` and `check_optional_tool` calls

Both scripts support minimal PaaS environments and full development setups.
