---
name: solid-detection
description: Multi-language SOLID detection rules. Project type detection, interface locations, file size limits per language.
argument-hint: "[file-or-directory] [--language]"
user-invocable: false
---

# SOLID Detection Skill

## Project Detection

Detect project type from configuration files:

```bash
# Next.js (priority over React)
[ -f "package.json" ] && grep -q '"next"' package.json

# React (no "next" in package.json)
[ -f "package.json" ] && grep -q '"react"' package.json && ! grep -q '"next"' package.json

# Generic TypeScript (no react/next, has .ts files)
[ -f "package.json" ] && ! grep -q '"react"' package.json && ! grep -q '"next"' package.json
[ -f "tsconfig.json" ] || [ -f "bun.lockb" ] || [ -f "bunfig.toml" ]

# Laravel
[ -f "composer.json" ] && grep -q '"laravel' composer.json

# Swift
[ -f "Package.swift" ] || ls *.xcodeproj

# Java
[ -f "pom.xml" ] || [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]

# Go
[ -f "go.mod" ]

# Ruby
[ -f "Gemfile" ] && [ -f "Rakefile" ]

# Rust
[ -f "Cargo.toml" ]

# Python
[ -f "pyproject.toml" ] || [ -f "requirements.txt" ]
```

**Priority order:** Next.js > React > Generic TS > Laravel > Swift > Java > Go > Ruby > Rust > Python

## Language Rules

### Next.js / TypeScript

| Rule | Value |
|------|-------|
| File limit | 150 lines |
| Interface location | `modules/[feature]/src/interfaces/` |
| Shared interfaces | `modules/cores/interfaces/` |
| Forbidden | Interfaces in `components/`, `app/` |
| SOLID skill | `solid-nextjs` |

**Pattern detection**:
```regex
^(export )?(interface|type) \w+
```

### React / TypeScript

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `modules/[feature]/src/interfaces/` |
| Shared interfaces | `modules/cores/interfaces/` |
| Forbidden | Interfaces in `components/` files |
| SOLID skill | `solid-react` |

**Pattern detection**:
```regex
^(export )?(interface|type) \w+
```

### Generic TypeScript / Bun / Node.js

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `modules/[feature]/src/interfaces/` |
| Shared interfaces | `modules/cores/interfaces/` |
| Structure | **Modular MANDATORY** |
| Forbidden | Interfaces in service/lib files |
| SOLID skill | `solid-generic` |

**Pattern detection**:
```regex
^(export )?(interface|type) \w+
```

### Laravel / PHP

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `FuseCore/[Module]/App/Contracts/` |
| Shared interfaces | `FuseCore/Core/App/Contracts/` |
| Structure | **FuseCore Modular MANDATORY** |
| Forbidden | Interfaces outside Contracts/ |
| SOLID skill | `solid-php` |

**Pattern detection**:
```regex
^interface \w+
```

### Swift

| Rule | Value |
|------|-------|
| File limit | 150 lines |
| Interface location | `Features/[Feature]/Protocols/` |
| Shared interfaces | `Core/Protocols/` |
| Structure | **Features Modular MANDATORY** |
| Forbidden | Protocols outside Protocols/ |
| SOLID skill | `solid-swift` |

**Pattern detection**:
```regex
^protocol \w+
```

### Java

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `modules/[feature]/interfaces/` |
| Shared interfaces | `modules/core/interfaces/` |
| Structure | **Modular MANDATORY** |
| Forbidden | Interfaces in impl files |
| SOLID skill | `solid-java` |

**Pattern detection**:
```regex
^(public )?(interface) \w+
```

### Go

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `internal/modules/[feature]/ports/` |
| Shared interfaces | `internal/core/ports/` |
| Structure | **Modular MANDATORY** |
| Forbidden | Interfaces in impl files |
| SOLID skill | `solid-go` |

**Pattern detection**:
```regex
^type \w+ interface \{
```

### Ruby

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `app/modules/[feature]/contracts/` |
| Shared interfaces | `app/modules/core/contracts/` |
| Structure | **Modular MANDATORY** |
| Forbidden | Contracts in model files |
| SOLID skill | `solid-ruby` |

**Pattern detection**:
```regex
^module \w+Contract
```

### Rust

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `src/modules/[feature]/traits.rs` |
| Shared interfaces | `src/core/traits.rs` |
| Structure | **Modular MANDATORY** |
| Forbidden | Traits in impl files |
| SOLID skill | `solid-rust` |

**Pattern detection**:
```regex
^pub trait \w+
```

### Python

| Rule | Value |
|------|-------|
| File limit | 100 lines |
| Interface location | `src/interfaces/` |
| Forbidden | ABC outside interfaces/ |

**Pattern detection**:
```regex
class \w+\(.*ABC.*\)
```

## Line Counting

Exclude from count:
- Blank lines
- Comments (`//`, `/* */`, `#`, `"""`)
- Import statements (optional)

```bash
# TypeScript/Go/Rust/Swift
grep -v '^\s*$\|^\s*//\|^\s*/\*\|^\s*\*' file

# PHP
grep -v '^\s*$\|^\s*//\|^\s*#\|^\s*/\*\|^\s*\*' file

# Python
grep -v '^\s*$\|^\s*#\|^\s*"""' file
```

## Validation Actions

| Severity | Action |
|----------|--------|
| Interface in wrong location | **BLOCK** (exit 2) |
| File over limit | **WARNING** (exit 0) |
| Missing documentation | **WARNING** |

## Skill Mapping

| Project Type | SOLID Skill | Skill Path |
|--------------|-------------|------------|
| `nextjs` | solid-nextjs | `nextjs-expert/skills/solid-nextjs/` |
| `react` | solid-react | `react-expert/skills/solid-react/` |
| `generic` | solid-generic | `solid/skills/solid-generic/` |
| `laravel` | solid-php | `laravel-expert/skills/solid-php/` |
| `swift` | solid-swift | `swift-apple-expert/skills/solid-swift/` |
| `java` | solid-java | `solid/skills/solid-java/` |
| `go` | solid-go | `solid/skills/solid-go/` |
| `ruby` | solid-ruby | `solid/skills/solid-ruby/` |
| `rust` | solid-rust | `solid/skills/solid-rust/` |
| `python` | _(no skill yet)_ | - |

## Environment Variables

Set by `detect-project.sh`:

```bash
SOLID_PROJECT_TYPE=nextjs|react|generic|laravel|swift|java|go|ruby|rust|python|unknown
SOLID_FILE_LIMIT=100|150
SOLID_INTERFACE_DIR=path/to/interfaces
SOLID_STRUCTURE=modular
```
