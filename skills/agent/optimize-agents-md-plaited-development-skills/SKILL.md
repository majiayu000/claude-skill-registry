---
name: optimize-agents-md
description: Optimize AGENTS.md and rules for token efficiency. Auto-invoked when user asks about improving agent instructions, compressing AGENTS.md, or making rules more effective.
license: ISC
---

# Optimize AGENTS.md

Apply Boris Cherny's compression principles to AGENTS.md and rules files.

**Target**: ~2.5k tokens (most are 10k+ unnecessarily)

## When to Use

- User wants to improve their AGENTS.md or CLAUDE.md
- Agent instructions feel verbose or redundant
- Rules exist but lack verification patterns
- Setting up a new project's agent configuration

## Anti-Patterns to Fix

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Context stuffing | Repeating info agents already know | Delete obvious instructions |
| Static memory | No learnings section | Add `## Learnings` with dates |
| Format drift | Inconsistent structure | Use consistent headers |
| Missing verification | No way to check work | Add `*Verify:*` patterns to rules |
| Verbose rules | Paragraphs instead of patterns | Compress to pattern + verify + fix |

## Workflow

### Phase 1: Analyze Current State

```bash
# Count tokens (rough estimate: words × 1.3)
wc -w AGENTS.md

# Find redundancy with project files
grep -l "bun test" AGENTS.md package.json
```

Look for:
- Instructions duplicating package.json scripts
- Explanations of common tools (git, npm, bun)
- Verbose descriptions that could be tables
- Rules without verification patterns

### Phase 2: Compress AGENTS.md

**Structure target:**

```markdown
# AGENTS.md

## Overview
[1-2 sentences: what this project is]

## Capabilities  
[Bullet list of key features/commands]

## Structure
[Brief file tree of key paths]

## Commands
[Essential commands only - not everything in package.json]

## Verification
[How to check work is correct]

## Workflow
[Key constraints: plan first, verify incrementally]

## Rules
[Links to rule files or inline compressed rules]

## Learnings
[Dated entries from actual issues encountered]
```

**Compression techniques:**
- Tables over paragraphs
- Bullets over sentences
- Delete anything in package.json
- Delete tool explanations (agents know git, npm, bun)
- Merge related sections

### Phase 3: Optimize Rules

Transform verbose rules into verification patterns:

**Before (verbose):**
```markdown
## Type Aliases Over Interfaces

In this codebase, we prefer using TypeScript type aliases 
instead of interfaces. This provides better consistency 
and flexibility when working with unions and intersections.

Example:
// Good
type User = { name: string }

// Bad  
interface User { name: string }
```

**After (compressed with verification):**
```markdown
**Type over interface** - `type User = {` instead of `interface User {`
*Verify:* `grep 'interface [A-Z]' src/`
*Fix:* Replace `interface X {` with `type X = {`
```

**Pattern format:**
```
**Rule name** - Brief description with example
*Verify:* Command or tool to check compliance
*Fix:* How to resolve violations
```

### Phase 4: Add Living Document Features

**Learnings section:**
```markdown
## Learnings
- 2024-01-15: Skills use CLI tools, never duplicate logic
- 2024-01-20: Rules need verification patterns for self-checking
```

**Update trigger:** Add learnings when:
- A mistake required correction
- A pattern was discovered
- A constraint was clarified

## Verification

After optimization:

1. **Token count**: `wc -w AGENTS.md` × 1.3 ≈ tokens (target: <2.5k)
2. **No redundancy**: `grep` for duplicated info in package.json
3. **Rules have patterns**: Each rule has `*Verify:*` line
4. **Learnings exist**: `## Learnings` section present

## Example Transformations

### Commands Section

**Before (340 words):**
```markdown
## Development Commands

To install dependencies, run the following command...
[lengthy explanation of bun install]

To run tests, you can use...
[explanation of test runner]
```

**After (40 words):**
```markdown
## Commands
```bash
bun install    # Setup
bun run check  # Lint/format
bun test       # Unit tests
```
```

### Capability Description

**Before:**
```markdown
This package provides TypeScript Language Server Protocol 
integration that allows you to get type information, find 
symbols across your workspace, locate references to symbols,
and perform batch analysis of files.
```

**After:**
```markdown
**LSP** (`lsp-*`): Type-aware hover, symbol search, references, batch analysis
```

## Related Skills

- **scaffold-rules** - Install optimized rules with verification patterns
- **validate-skill** - Validate skill structure
