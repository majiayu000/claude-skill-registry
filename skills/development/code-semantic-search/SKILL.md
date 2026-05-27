---
name: code-semantic-search
description: Semantic code search using Phase 1 vector embeddings and Phase 2 hybrid search.
version: 1.0.0
model: sonnet
invoked_by: user
user_invocable: true
tools: [Read, Write, Edit]
---

# Code Semantic Search

## Overview

Semantic code search using Phase 1 vector embeddings and Phase 2
hybrid search (semantic + structural). Find code by meaning, not
just keywords.

**Core principle:** Search code by what it does, not what it's called.

## Phase 2: Hybrid Search

This skill now supports three search modes:

1. **Hybrid (Default)**:
   - Combines semantic + structural search
   - Best accuracy (95%+)
   - Slightly slower but still <150ms
   - Recommended for all searches

2. **Semantic-Only**:
   - Uses only Phase 1 semantic vectors
   - Fastest (<50ms)
   - Good for conceptual searches
   - Use when structure doesn't matter

3. **Structural-Only**:
   - Uses only ast-grep patterns
   - Precise for exact matches
   - Best for finding function/class definitions
   - Use when you need exact structural patterns

### Performance Comparison

| Mode            | Speed  | Accuracy | Best For          |
| --------------- | ------ | -------- | ----------------- |
| Hybrid          | <150ms | 95%      | General search    |
| Semantic-only   | <50ms  | 85%      | Concepts          |
| Structural-only | <50ms  | 100%     | Exact patterns    |
| Phase 1 only    | <50ms  | 80%      | Legacy (fallback) |

## When to Use

**Always:**

- Finding authentication logic without knowing function names
- Searching for error handling patterns
- Locating database queries
- Finding similar code to a concept
- Discovering implementation patterns

**Don't Use:**

- Exact text matching (use Grep instead)
- File name searches (use Glob instead)
- Simple keyword searches (use ripgrep instead)

## Usage Examples

### Hybrid Search (Recommended)

```javascript
// Basic hybrid search
Skill({ skill: 'code-semantic-search', args: 'find authentication logic' });

// With options
Skill({
  skill: 'code-semantic-search',
  args: 'database queries',
  options: {
    mode: 'hybrid',
    language: 'javascript',
    limit: 10,
  },
});
```

### Semantic-Only Search

```javascript
// Fast conceptual search
Skill({
  skill: 'code-semantic-search',
  args: 'find authentication',
  options: { mode: 'semantic-only' },
});
```

### Structural-Only Search

```javascript
// Exact pattern matching
Skill({
  skill: 'code-semantic-search',
  args: 'find function authenticate',
  options: { mode: 'structural-only' },
});
```

## Implementation Reference

**Hybrid Search:** `.claude/lib/code-indexing/hybrid-search.cjs`

**Query Analysis:** `.claude/lib/code-indexing/query-analyzer.cjs`

**Result Ranking:** `.claude/lib/code-indexing/result-ranker.cjs`

## Integration Points

- **developer**: Code exploration, implementation discovery
- **architect**: System understanding, pattern analysis
- **code-reviewer**: Finding similar patterns, consistency checks
- **reverse-engineer**: Understanding unfamiliar codebases
- **researcher**: Research existing implementations

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
