---
name: review-rust-all
description: Run all review-rust* skills as a comprehensive code review. Applies review-rust-code (best practices, type-driven design, error handling), review-rust-async-patterns (tokio concurrency, cancellation safety, channels), and review-rust-memory (allocation reduction, data layout, Feather-Flow-specific patterns). Use after completing a feature or before opening a PR.
---

# Comprehensive Rust Code Review

Orchestrates all three `review-rust*` skills against changed files, then validates with `make ci`. This skill contains no review criteria of its own — all opinions live in the sub-skills.

**Context**: Feather-Flow is a schema validation framework with static analysis as a first-class citizen. See **[HOW_FEATHERFLOW_WORKS.md](../../../HOW_FEATHERFLOW_WORKS.md)** for the full architecture. All code changes should be reviewed in the context of this goal — mandatory schemas, compile-time validation, AST-based dependency extraction, and no CTEs.

## Project Layout

Cargo workspace with crates under `crates/`:

| Crate | Path | Role |
|-------|------|------|
| `ff-cli` | `crates/ff-cli/` | Binary (CLI commands, integration tests) |
| `ff-core` | `crates/ff-core/` | Library (shared types, config, DAG) |
| `ff-analysis` | `crates/ff-analysis/` | Library (DataFusion static analysis) |
| `ff-sql` | `crates/ff-sql/` | Library (SQL parsing, lineage) |
| `ff-jinja` | `crates/ff-jinja/` | Library (Jinja template rendering) |
| `ff-db` | `crates/ff-db/` | Library (database trait + DuckDB) |
| `ff-test` | `crates/ff-test/` | Library (schema test generation) |

## Procedure

### Step 1: Identify changed files

Find modified `.rs` files:

```bash
# If on a feature branch:
git diff --name-only main -- '*.rs'

# If on main with uncommitted changes:
git diff --name-only -- '*.rs'
git diff --cached --name-only -- '*.rs'

# For the last commit:
git diff --name-only HEAD~1 -- '*.rs'
```

Separate into two groups:
- **Production code**: files under `crates/*/src/`
- **Test code**: files under `crates/*/tests/` or ending in `_test.rs`

Read every changed file in full before reviewing.

### Step 2: Apply review-rust-code

Read the full skill file and apply all of its rules against every changed `.rs` file:

```
Read .claude/skills/review-rust-code/SKILL.md
```

### Step 3: Apply review-rust-async-patterns

Check if any changed files contain async code:

```bash
grep -rl 'async\|\.await\|tokio::\|spawn' <changed-files>
```

**Skip this step entirely if none do.**

Otherwise, read the full skill file and apply all of its rules against each async file:

```
Read .claude/skills/review-rust-async-patterns/SKILL.md
```

### Step 4: Apply review-rust-memory

Read the full skill file and apply all of its rules against every changed `.rs` file:

```
Read .claude/skills/review-rust-memory/SKILL.md
```

### Step 5: Report findings

Combine all findings from steps 2-4 into a single report grouped by crate, then by file. Use the severity definitions from the sub-skills. Example format:

```
## ff-analysis

### crates/ff-analysis/src/datafusion_bridge/provider.rs

- **Error**: [description]
- **Warning**: [description]

## ff-cli

### crates/ff-cli/src/commands/common.rs

- **Info**: [description]
```

### Step 6: Verify

Run `make ci` to confirm format, clippy, tests, and docs all pass.

## Usage

```
/review-rust-all
```

Or target specific files:

```
/review-rust-all crates/ff-cli/src/commands/compile.rs crates/ff-analysis/src/datafusion_bridge/propagation.rs
```
