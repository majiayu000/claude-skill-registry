---
name: benchmark-advisor
description: Suggests which benchmarks to run based on code changes
---

# Benchmark Advisor Skill

This skill analyzes your code changes and recommends specific Criterion benchmarks to run.

## When to Use

This skill automatically activates when:
- You've made changes to performance-critical code
- You're preparing to commit performance-related work
- You want to verify your changes don't introduce regressions

## How It Works

1. **Detects Changed Files**: Analyzes `git diff` to see which files you've modified
2. **Maps to Benchmarks**: Uses pattern matching to identify relevant benchmarks
3. **Provides Recommendations**: Suggests specific `cargo bench` commands with explanations

## Usage

Simply ask:
- "What benchmarks should I run?"
- "Which benchmarks are affected by my changes?"
- "Suggest benchmarks for my current work"

## Skill Logic

```bash
# 1. Detect changed files
CHANGED_FILES=$(git diff --name-only HEAD)

# 2. Load mapping configuration
# See mapping.toml for file-to-benchmark mappings

# 3. Match changed files to benchmarks
# Example mappings:
#   src/cache/**/*.rs → cargo bench --bench cache
#   src/config/**/*.rs → cargo bench --bench config
#   src/main.rs → cargo bench (full suite - affects startup time)

# 4. Generate recommendation with explanation
```

## Example Interaction

**User:** "What benchmarks should I run?"

**Claude:** "I analyzed your changes and found modifications to:
- `src/cache/manifest.rs`
- `src/cache/lru.rs`

**Recommended benchmarks:**
```bash
cargo bench --bench cache
```

**Why**: Changes to cache implementation files can affect cache operation performance (get_model, add_model, remove_model, lru_eviction).

You can also run the full suite if you want comprehensive validation:
```bash
cargo bench
```"

## Mapping Configuration

The skill uses `mapping.toml` to define file patterns and their corresponding benchmarks:

```toml
# Cache-related files
[[mapping]]
pattern = "src/cache/**/*.rs"
benchmark = "cargo bench --bench cache"
reason = "Cache implementation changes can affect cache operation performance"

# Config-related files
[[mapping]]
pattern = "src/config/**/*.rs"
benchmark = "cargo bench --bench config"
reason = "Config loading and merging performance may be impacted"

# Main entry point
[[mapping]]
pattern = "src/main.rs"
benchmark = "cargo bench"
reason = "Main entry point affects startup time - run full suite"
```

## Output Format

**Concise**: Lists changed files, recommended command, and brief explanation

**No false positives**: Only suggests benchmarks for performance-critical changes

**Actionable**: Provides exact commands to copy/paste
