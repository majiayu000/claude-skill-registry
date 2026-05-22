---
name: doc-sync
description: Synchronizes CLAUDE.md navigation indexes and README.md architecture docs across a repository. Use when asked to "sync docs", "update CLAUDE.md files", "ensure documentation is in sync", "audit documentation", or when documentation maintenance is needed after code changes.
license: MIT
metadata:
version: 1.0.0
model: claude-sonnet-4-5
---

# Doc Sync

Maintains the CLAUDE.md navigation hierarchy and optional README.md architecture docs across a repository. This skill is self-contained and performs all documentation work directly.

## Scope Resolution

Determine scope FIRST:

| User Request                                            | Scope                                     |
| ------------------------------------------------------- | ----------------------------------------- |
| "sync docs" / "update documentation" / no specific path | REPOSITORY-WIDE                           |
| "sync docs in src/validator/"                           | DIRECTORY: src/validator/ and descendants |
| "update CLAUDE.md for parser.py"                        | FILE: single file's parent directory      |

For REPOSITORY-WIDE scope, perform a full audit. For narrower scopes, operate only within the specified boundary.

## CLAUDE.md Format Specification

### Index Format

Use tabular format with What and When columns:

```markdown
## Files

| File        | What                           | When to read                              |
| ----------- | ------------------------------ | ----------------------------------------- |
| `cache.rs`  | LRU cache with O(1) operations | Implementing caching, debugging evictions |
| `errors.rs` | Error types and Result aliases | Adding error variants, handling failures  |

## Subdirectories

| Directory   | What                          | When to read                              |
| ----------- | ----------------------------- | ----------------------------------------- |
| `config/`   | Runtime configuration loading | Adding config options, modifying defaults |
| `handlers/` | HTTP request handlers         | Adding endpoints, modifying request flow  |
```

### Column Guidelines

- **File/Directory**: Use backticks around names: `cache.rs`, `config/`
- **What**: Factual description of contents (nouns, not actions)
- **When to read**: Task-oriented triggers using action verbs (implementing, debugging, modifying, adding, understanding)
- At least one column must have content; empty cells use `-`

### Trigger Quality Test

Given task "add a new validation rule", can an LLM scan the "When to read" column and identify the right file?

### ROOT vs SUBDIRECTORY CLAUDE.md

**ROOT CLAUDE.md:**

```markdown
# [Project Name]

[One sentence: what this is]

## Files

| File | What | When to read |
| ---- | ---- | ------------ |

## Subdirectories

| Directory | What | When to read |
| --------- | ---- | ------------ |

## Build

[Copy-pasteable command]

## Test

[Copy-pasteable command]

## Development

[Setup instructions, environment requirements, workflow notes]
```

**SUBDIRECTORY CLAUDE.md:**

```markdown
# [directory-name]/

## Files

| File | What | When to read |
| ---- | ---- | ------------ |

## Subdirectories

| Directory | What | When to read |
| --------- | ---- | ------------ |
```

**Critical constraint:** Subdirectory CLAUDE.md files are PURE INDEX. No prose, no overview sections, no architectural explanations. Those belong in README.md.

## README.md Specification

### Creation Criteria (Invisible Knowledge Test)

Create README.md ONLY when the directory contains knowledge NOT visible from reading the code:

- Multiple components interact through non-obvious contracts or protocols
- Design tradeoffs were made that affect how code should be modified
- The directory's structure encodes domain knowledge (e.g., processing order matters)
- Failure modes or edge cases aren't apparent from reading individual files
- There are "rules" developers must follow that aren't enforced by the compiler/linter

**DO NOT create README.md when:**

- The directory is purely organizational (just groups related files)
- Code is self-explanatory with good function/module docs
- You'd be restating what CLAUDE.md index entries already convey

### Content Test

For each sentence in README.md, ask: "Could a developer learn this by reading the source files?"

- If YES: delete the sentence
- If NO: keep it

README.md earns its tokens by providing INVISIBLE knowledge: the reasoning behind the code, not descriptions of the code.

### README.md Structure

```markdown
# [Component Name]

## Overview

[One paragraph: what problem this solves, high-level approach]

## Architecture

[How sub-components interact; data flow; key abstractions]

## Design Decisions

[Tradeoffs made and why; alternatives considered]

## Invariants

[Rules that must be maintained; constraints not enforced by code]
```

## Workflow

### Phase 1: Discovery

Map directories requiring CLAUDE.md verification:

```bash
# Find all directories (excluding .git, node_modules, __pycache__, etc.)
find . -type d \( -name .git -o -name node_modules -o -name __pycache__ -o -name .venv -o -name target -o -name dist -o -name build \) -prune -o -type d -print
```

For each directory in scope, record:

1. Does CLAUDE.md exist?
2. If yes, does it have the required table-based index structure?
3. What files/subdirectories exist that need indexing?

### Phase 2: Audit

For each directory, check for drift and misplaced content:

```
<audit_check dir="[path]">
CLAUDE.md exists: [YES/NO]
Has table-based index: [YES/NO]
Files in directory: [list]
Files in index: [list]
Missing from index: [list]
Stale in index (file deleted): [list]
Triggers are task-oriented: [YES/NO/PARTIAL]
Contains misplaced content: [YES/NO] (architecture/design docs that belong in README.md)
README.md exists: [YES/NO]
README.md warranted: [YES/NO] (invisible knowledge present?)
</audit_check>
```

### Phase 3: Content Migration

**Critical:** If CLAUDE.md contains content that does NOT belong there, migrate it:

Content that MUST be moved from CLAUDE.md to README.md:

- Architecture explanations or diagrams
- Design decision documentation
- Component interaction descriptions
- Overview sections with prose (in subdirectory CLAUDE.md files)
- Invariants or rules documentation
- Any "why" explanations beyond simple triggers

Migration process:

1. Identify misplaced content in CLAUDE.md
2. Create or update README.md with the architectural content
3. Strip CLAUDE.md down to pure index format
4. Add README.md to the CLAUDE.md index table

### Phase 4: Index Updates

For each directory needing work:

**Creating/Updating CLAUDE.md:**

1. Use the appropriate template (ROOT or SUBDIRECTORY)
2. Populate tables with all files and subdirectories
3. Write "What" column: factual content description
4. Write "When to read" column: action-oriented triggers
5. If README.md exists, include it in the Files table

**Creating README.md (only when warranted):**

1. Verify invisible knowledge criteria are met
2. Document architecture, design decisions, invariants
3. Apply the content test: remove anything visible from code
4. Keep under ~500 tokens

### Phase 5: Verification

After all updates complete, verify:

1. Every directory in scope has CLAUDE.md
2. All CLAUDE.md files use table-based index format
3. No drift remains (files <-> index entries match)
4. No misplaced content in CLAUDE.md (architecture docs moved to README.md)
5. README.md files are indexed in their parent CLAUDE.md
6. Subdirectory CLAUDE.md files contain no prose/overview sections

## Output Format

```
## Doc Sync Report

### Scope: [REPOSITORY-WIDE | directory path]

### Changes Made
- CREATED: [list of new CLAUDE.md files]
- UPDATED: [list of modified CLAUDE.md files]
- MIGRATED: [list of content moved from CLAUDE.md to README.md]
- CREATED: [list of new README.md files]
- FLAGGED: [any issues requiring human decision]

### Verification
- Directories audited: [count]
- CLAUDE.md coverage: [count]/[total] (100%)
- Drift detected: [count] entries fixed
- Content migrations: [count] (architecture docs moved to README.md)
- README.md files: [count] (only where warranted)
```

## Exclusions

DO NOT index:

- Generated files (dist/, build/, _.generated._, compiled outputs)
- Vendored dependencies (node_modules/, vendor/, third_party/)
- Git internals (.git/)
- IDE/editor configs (.idea/, .vscode/ unless project-specific settings)

DO index:

- Hidden config files that affect development (.eslintrc, .env.example, .gitignore)
- Test files and test directories
- Documentation files (including README.md)

## Anti-Patterns

### Index Anti-Patterns

**Too vague (matches everything):**

```markdown
| `config/` | Configuration | Working with configuration |
```

**Content description instead of trigger:**

```markdown
| `cache.rs` | Contains the LRU cache implementation | - |
```

**Missing action verb:**

```markdown
| `parser.py` | Input parsing | Input parsing and format handling |
```

### Correct Examples

```markdown
| `cache.rs` | LRU cache with O(1) get/set | Implementing caching, debugging misses, tuning eviction |
| `config/` | YAML config parsing, env overrides | Adding config options, changing defaults, debugging config loading |
```

## When NOT to Use This Skill

- Single file documentation (inline comments, docstrings) - handle directly
- Code comments - handle directly
- Function/module docstrings - handle directly
- This skill is for CLAUDE.md/README.md synchronization specifically

## Reference

For additional trigger pattern examples, see `references/trigger-patterns.md`.
