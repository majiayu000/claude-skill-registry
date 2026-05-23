---
name: AILANG Code Writing
description: Write and run AILANG code with correct syntax. Use when user asks to write AILANG programs, fix AILANG syntax errors, run AILANG code, or needs help with AILANG syntax. Includes version checking, syntax validation, and common patterns.
---

# AILANG Code Writing

Write correct AILANG code following current syntax (v0.3.12+).

## Quick Start

AILANG is a pure functional programming language with Hindley-Milner type inference and algebraic effects.

**Most common usage:**
```bash
ailang run --caps IO --entry main solution.ail   # Run with effects
ailang repl                                        # Interactive development
ailang check solution.ail                          # Type-check only
```

## When to Use This Skill

Invoke this skill when:
- User asks to write AILANG code
- User needs help with AILANG syntax errors
- User wants to run AILANG programs
- User asks about AILANG features or capabilities
- User mentions AILANG version or syntax

## Available Scripts

### `scripts/check_version.sh`
Check current active AILANG prompt version from `prompts/versions.json`.

**Usage:**
```bash
.claude/skills/use-ailang/scripts/check_version.sh
```

**Output:**
```
Active AILANG version: v0.3.12
Prompt file: prompts/v0.3.12.md
Status: File exists ✓
```

### `scripts/validate_code.sh <file.ail>`
Validate AILANG code syntax using `ailang check`.

**Usage:**
```bash
.claude/skills/use-ailang/scripts/validate_code.sh solution.ail
```

**Output:**
```
Validating solution.ail...
✓ Type check passed
```

## Key Resources

### 1. **Current Version Check** (Always Use First!)
```bash
# Check active prompt version
.claude/skills/use-ailang/scripts/check_version.sh
```

The active version in `prompts/versions.json` is the source of truth for current AILANG syntax.

### 2. **Syntax Quick Reference**
See [`resources/syntax_quick_ref.md`](resources/syntax_quick_ref.md) for:
- Basic syntax rules (func, semicolons, patterns)
- Core language features (functions, ADTs, records, effects)
- Standard library overview
- What works vs what doesn't work

### 3. **Common Patterns**
See [`resources/common_patterns.md`](resources/common_patterns.md) for:
- Recursion patterns (no loops!)
- Pattern matching examples
- Effects and IO patterns
- Record updates
- Common mistakes and fixes
- Best practices

### 4. **Full Documentation**
- **Teaching prompt**: Check active version in prompts/versions.json, then use that prompt file
- **Website**: https://ailang.sunholo.com/
- **Examples**: `examples/` directory (66 files, 48 passing)
- **REPL commands**: `docs/docs/reference/repl-commands.md`

## Usage Contexts

### 1. REPL (Interactive Development)
**Most flexible** - No module declaration needed:

```bash
ailang repl
```

```ailang
> 5 + 3
8 : int

> let double = func(x: int) -> int { x * 2 }
> double(21)
42 : int

> :type double
func(int) -> int
```

### 2. Module Files (General Programs)
**Standard usage** - Module with exported functions:

```ailang
module myapp/main

import std/io (println)

export func main() -> () ! {IO} {
  println("Hello, AILANG!")
}
```

```bash
# Run with effects (flags BEFORE filename!)
ailang run --caps IO main.ail

# Type-check only
ailang check main.ail
```

### 3. Eval Harness (AI Benchmarks)
**Specific structure required** - Must use `module benchmark/solution`:

```ailang
module benchmark/solution

import std/io (println)

export func main() -> () ! {IO} {
  println("Benchmark solution")
}
```

**Note:** Teaching prompts in `prompts/` use eval harness conventions for AI code generation benchmarks.

## AILANG CLI Reference

### Core Commands

```bash
# Interactive REPL
ailang repl

# Run a program (flags BEFORE filename!)
ailang run --caps IO,FS --entry main file.ail

# Type-check without running
ailang check file.ail

# Watch for changes and auto-reload
ailang watch file.ail

# Output module interface (JSON)
ailang iface mymodule

# Export training data
ailang export-training
```

### Run Command Flags

**IMPORTANT**: Flags must come BEFORE the filename!

```bash
# ✅ CORRECT
ailang run --caps IO,FS --entry main file.ail

# ❌ WRONG
ailang run file.ail --caps IO  # Flags ignored!
```

**Available flags:**
- `--caps <list>` - Enable capabilities (IO, FS, Net, Clock)
- `--entry <name>` - Entrypoint function (default: main)
- `--args-json <json>` - JSON arguments to pass to entrypoint
- `--trace` - Enable execution tracing
- `--print` - Print return value (default: true)
- `--no-print` - Suppress output (exit code only)

### Development Commands

```bash
# Validate builtin registry
ailang doctor builtins

# List all builtins
ailang builtins list --by-module

# Run tests
ailang test
```

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (YAML frontmatter + overview)
2. **Load on demand**: `resources/syntax_quick_ref.md` (detailed syntax)
3. **Load on demand**: `resources/common_patterns.md` (examples and patterns)
4. **Execute as needed**: Scripts in `scripts/` directory

This saves context tokens while providing access to comprehensive information when needed.

## Version Information

**Current active version**: Check with `scripts/check_version.sh`

**As of this skill**: v0.3.12 (October 2025)

Key features by version:
- v0.3.12: Emphasis on show() function (recovery release)
- v0.3.9: JSON encoding, HTTP headers for AI API integration
- v0.3.8: Multi-line ADTs, record updates, auto-import prelude
- v0.3.7: Effect system with capability security
- v0.3.5: Anonymous functions, letrec, numeric conversions

Check `CHANGELOG.md` for detailed version history.

## Installation (For Reference)

```bash
# From releases (recommended)
wget https://github.com/sunholo-data/ailang/releases/latest/download/ailang-<platform>.tar.gz
tar xzf ailang-<platform>.tar.gz
sudo mv ailang /usr/local/bin/

# Or build from source
git clone https://github.com/sunholo-data/ailang
cd ailang
make install
```

## Getting Help

- **Version check**: `.claude/skills/use-ailang/scripts/check_version.sh`
- **Syntax reference**: `resources/syntax_quick_ref.md`
- **Common patterns**: `resources/common_patterns.md`
- **Teaching prompt**: Use active version from prompts/versions.json
- **Documentation**: https://ailang.sunholo.com/
- **Examples**: `examples/` directory
- **Issues**: https://github.com/sunholo-data/ailang/issues
- **REPL help**: Type `:help` in the REPL

## Workflow

When user asks for AILANG code:

1. **Check version** (optional, if uncertain):
   ```bash
   .claude/skills/use-ailang/scripts/check_version.sh
   ```

2. **Load syntax reference** (if needed):
   Read `resources/syntax_quick_ref.md` for detailed syntax rules

3. **Load common patterns** (if needed):
   Read `resources/common_patterns.md` for examples and best practices

4. **Write code** following current syntax

5. **Validate code** (optional):
   ```bash
   .claude/skills/use-ailang/scripts/validate_code.sh solution.ail
   ```

6. **Help user run** with correct CLI flags

## Notes

- This skill follows Anthropic's Agent Skills specification (Oct 2025)
- Uses progressive disclosure to save context tokens
- Scripts execute without loading into context window
- Resource files loaded on demand when detailed reference needed
- Always check `prompts/versions.json` for latest active version when writing benchmark code
