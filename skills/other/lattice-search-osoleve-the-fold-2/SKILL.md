---
name: lattice-search
description: Search and navigate The Fold's skill lattice using meta-tooling. Use for finding functions, exploring dependencies, type-aware queries, and cross-reference analysis. Invoke when searching for capabilities, exploring the codebase structure, or finding how functions relate.
allowed-tools: Bash(./fold:*), Read, Grep, Glob
---

# Lattice Search Skill

## Overview

The Fold's lattice is a DAG of verified skills with comprehensive meta-tooling for discovery and navigation. This skill provides search, inspection, and cross-reference capabilities.

Use lattice search for:
- Finding functions by name, description, or type signature
- Exploring skill dependencies and dependents
- Understanding what a skill exports
- Tracing call graphs (what calls what)
- Discovering capabilities you didn't know existed

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `lf` | Full-text search (BM25 ranked) | `(lf "matrix decomposition")` |
| `lfe` | Exact symbol lookup | `(lfe 'vec3)` |
| `lfp` | Prefix search | `(lfp 'matrix)` |
| `lfs` | Substring search | `(lfs 'c2d)` |
| `li` | Skill description | `(li 'linalg)` |
| `le` | List exports | `(le 'linalg)` |
| `lm` | List modules | `(lm 'linalg)` |
| `ld` | Dependencies (what it needs) | `(ld 'physics/diff)` |
| `lu` | Dependents (what uses it) | `(lu 'linalg)` |
| `lxu` | Callers (what calls this) | `(lxu 'matrix-rows)` |
| `lxc` | Callees (what this calls) | `(lxc 'floyd-warshall)` |
| `ls` | Lattice statistics | `(ls)` |

## Instructions

### Basic Search

```bash
# Full-text search - finds functions, skills, descriptions
./fold "(lf \"parser combinator\")"

# Exact symbol lookup (falls back to substring if not found)
./fold "(lfe 'maybe-bind)"

# Prefix search - finds all symbols starting with prefix
./fold "(lfp 'matrix)"      # matrix-*, matrix-multiply, etc.

# Substring search - finds symbols containing substring
./fold "(lfs 'zoh)"         # finds c2d-zoh, d2c-zoh, etc.

# Autocomplete suggestions
./fold "(lattice-complete \"mat\")"
```

### Type-Aware Search (Hoogle-style)

```bash
# Find functions with type in signature
./fold "(lf-type \"Monad\")"

# Find functions that take a specific type as input
./fold "(lf-input \"Matrix\")"

# Find functions that return a specific type
./fold "(lf-output \"Maybe\")"
```

### Cross-Reference Queries

```bash
# Build the cross-reference cache first (only needed once per session)
./fold -s dev "(build-xref-cache!)"

# What functions call this?
./fold -s dev "(lxu 'matrix-rows)"

# What does this function call?
./fold -s dev "(lxc 'floyd-warshall)"

# All transitive callers
./fold -s dev "(xref-callers-transitive 'fn)"

# Most-called functions (hot spots)
./fold -s dev "(xref-most-called 10)"
```

### DAG Navigation

```bash
# What does this skill depend on?
./fold "(ld 'physics/diff)"

# What skills use this one?
./fold "(lu 'linalg)"

# Find path between skills
./fold "(lattice-path 'physics/diff 'linalg)"

# Tier 0 skills (foundational, no deps)
./fold "(lattice-roots)"

# Skills with no dependents (leaves)
./fold "(lattice-leaves)"

# Most-depended-on skills (hubs)
./fold "(lattice-hubs)"
```

### Inspection

```bash
# Full skill description
./fold "(li 'linalg)"

# List all exports from a skill
./fold "(le 'linalg)"

# List modules with descriptions
./fold "(lm 'linalg)"

# One-line summary of all skills
./fold "(lattice-summary)"

# Structured data for programmatic use
./fold "(lattice-info 'linalg)"
```

### Analytics & Health

```bash
# Lattice statistics
./fold "(ls)"

# Health check (missing deps, cycles)
./fold "(lh)"

# Metadata coverage report
./fold "(lattice-coverage-pretty)"

# Print full DAG structure
./fold "(lattice-graph)"
```

### Manifest Auditing

```bash
# Find missing/phantom exports in a skill
./fold "(audit-skill-pretty 'fp)"

# List exports to add to manifest
./fold "(suggest-missing 'fp)"
```

## Search Best Practices

1. **Start broad, then narrow**: Use `(lf "concept")` first, then `(lfe 'symbol)` for exact matches
2. **Use substring for partial names**: If you know part of a name (like `c2d`), use `(lfs 'c2d)`
3. **Try multiple query variations**: Function might be named differently than expected
4. **Check skill exports**: Use `(le 'skill-name)` to see what a skill actually exports
5. **Not all functions are exported**: Use `(audit-skill 'name)` to find functions in source but missing from manifests

## Examples

### Example 1: Finding Matrix Operations

```bash
# Start with full-text search
./fold "(lf \"matrix multiplication\")"

# Found 'linalg' skill, check its exports
./fold "(le 'linalg)"

# Get module list to understand structure
./fold "(lm 'linalg)"
```

### Example 2: Exploring a Function's Usage

```bash
# Who calls matrix-transpose?
./fold -s dev "(build-xref-cache!)"
./fold -s dev "(lxu 'matrix-transpose)"

# What does the main caller depend on?
./fold -s dev "(lxc 'the-caller-function)"
```

### Example 3: Finding Control System Functions

```bash
# Don't know exact name, try substring
./fold "(lfs 'c2d)"
# Returns: c2d-zoh, c2d-tustin, etc.

# Get full info on the skill
./fold "(li 'fp)"
./fold "(le 'fp)"
```

### Example 4: Discovering Capabilities

```bash
# What can I do with parsers?
./fold "(lf \"parser\")"

# What monads are available?
./fold "(lf-type \"Monad\")"

# What data structures exist?
./fold "(li 'data)"
./fold "(le 'data)"
```

## Lattice Structure

| Tier | Skills | Purpose |
|------|--------|---------|
| 0 | linalg, data, algebra, random | Foundational (no lattice deps) |
| 1 | numeric, geometry, autodiff, fp, query, dsl, info, number-theory, meta | Intermediate |
| 2+ | physics/diff, physics/classical, tiles, sim, automata, pipeline | Advanced |

## Module Locations

| Component | Path |
|-----------|------|
| Knowledge Graph | `lattice/meta/kg.ss` |
| BM25 Search | `lattice/meta/bm25.ss` |
| Search API | `lattice/meta/search.ss` |
| Type Search | `lattice/meta/type-search.ss` |
| Cross-Reference | `lattice/meta/xref.ss` |
| DAG Navigation | `lattice/meta/dag.ss` |
| Inspection | `lattice/meta/inspect.ss` |
| Unified Entry | `lattice/meta/meta.ss` |
