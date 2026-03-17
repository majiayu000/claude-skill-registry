---
name: reclaude
description: Refactor CLAUDE.md files to follow progressive disclosure principles. Use when CLAUDE.md is too long or disorganized.
---

# reclaude

Refactor CLAUDE.md files to follow progressive disclosure principles.

## Prompt

I want you to refactor my CLAUDE.md file to follow progressive disclosure principles.

Follow these steps:

### 1. Check length

Report the current line count. Flag issues:
- **Ideal**: <50 lines
- **Acceptable**: 50-100 lines
- **Needs refactoring**: >100 lines (move content to `.claude/rules/` files)

### 2. Ensure verification section exists

Check for a `## Verification` section with commands Claude can run after making changes. If missing:
- Look in package.json for test/lint/typecheck/build scripts
- Look for Makefile, justfile, or other task runners
- Add a `## Verification` section with discovered commands

This is critical—Claude performs dramatically better when it can verify its work.

### 3. Find contradictions

Identify any instructions that conflict with each other. For each contradiction, ask me which version I want to keep.

### 4. Check for global skill extraction candidates

Look for content that could become a **reusable global skill** in `~/.claude/skills/`:
- Is about a tool/framework (not project-specific)
- Same instructions appear (or would apply) in 2+ projects
- Is substantial (>20 lines)

If found, suggest creating a global skill with name and description.

### 5. Identify essentials for root CLAUDE.md

Extract only what belongs in the root CLAUDE.md:
- One-line project description
- Package manager (if not npm)
- Non-obvious commands only (skip `npm test`, `npm run build` if standard)
- Links to `.claude/rules/` files with brief descriptions
- Verification section (always required)

### 6. Group remaining content

Organize remaining instructions into `.claude/rules/` files by category (e.g., TypeScript conventions, testing patterns, API design, Git workflow).

### 7. Flag for deletion

Identify content that should be removed entirely:
- **API documentation** — link to external docs instead
- **Code examples** — Claude can infer from reading source files
- **Interface/type definitions** — these exist in the code
- **Generic advice** — "write clean code", "follow best practices"
- **Obvious instructions** — "use TypeScript for .ts files"
- **Redundant info** — things Claude already knows
- **Too vague** — instructions that aren't actionable

## Target Template

```markdown
# Project Name

One-line description.

## Commands
- `command` - what it does (only non-obvious ones)

## Rules
- [Topic](/.claude/rules/topic.md) — brief description

## Verification
After making changes:
- `npm test` - Run tests
- `npm run lint` - Check linting
```

## What to Keep vs Remove

**Keep in CLAUDE.md:**
- Commands Claude can't guess from package.json
- Non-standard patterns specific to this project
- Project gotchas and footguns
- Links to detailed rules files

**Move to `.claude/rules/`:**
- Detailed conventions (>10 lines on a topic)
- Style guides
- Architecture decisions
- Workflow documentation

**Remove entirely:**
- Anything Claude can infer from reading the codebase
- Standard practices for the language/framework
- Documentation that exists elsewhere (link instead)
