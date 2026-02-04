---
name: init-docs
description: Create or update CLAUDE.md file for this project. Use when initializing a project for Claude Code, or when project structure/architecture has significantly changed.
---

Load the init skill using the Skill Tool.

Follow the next rules!

# CLAUDE.md Refinements

Where creating or updating CLAUDE.md, apply these rules:

## Don't Repeat Auto-Loaded Content

**CRITICAL: `.claude/rules/` is automatically loaded - DO NOT copy any of its content into CLAUDE.md**

This means NO details about:
- Code style guidelines (interface{} vs any, struct field ordering, import groups, etc.)
- Git commit conventions (conventional commits format, AI tool references, etc.)
- Logging requirements (which package to use, what not to use)
- Testing requirements
- Any other rules/conventions already in .claude/rules/

❌ **WRONG - This duplicates golang.md:**
```markdown
### Code Style (Go)
- Use `any` instead of `interface{}`
- Sort struct fields alphabetically
- Split imports into three groups: stdlib, dependencies, internal
```

✅ **CORRECT - Just reference the rules directory:**
```markdown
## Rules and Guidelines

The `.claude/rules/` directory is automatically loaded and contains:
- **golang.md** - Go development principles
- **git.md** - Commit message format
- **testing.md** - Testing policy
```

Or even simpler:
```markdown
All code conventions are defined in `.claude/rules/` (automatically loaded).
```

## Reference, Don't Duplicate ARCHITECTURE.md

If ARCHITECTURE.md exists with detailed architecture, diagrams, and data flows:
- **Replace architecture details** with: "Read ARCHITECTURE.md for [list what's there]"
- Keep only a brief project description
- Add a "Quick Component Location Guide" with just directory names and one-line descriptions

## Avoid Stale Metrics

**Don't include line counts** or other metrics that quickly become outdated:
- ❌ `model.go (714 lines)`
- ✅ `model.go - State machine orchestrator`

Focus on what components do, not their size.

## Verification Checklist

Before finishing, verify your CLAUDE.md does NOT contain:
- [ ] Specific code style rules (any vs interface{}, import grouping, struct field ordering, etc.)
- [ ] Commit message format details (conventional commits, types list, etc.)
- [ ] Logging implementation details (which package to use, what to avoid)
- [ ] Testing requirements or policies
- [ ] Line counts or other size metrics
- [ ] Detailed architecture diagrams (reference ARCHITECTURE.md instead)

CLAUDE.md should ONLY contain:
- [ ] Brief project description
- [ ] Quick component location guide (directory + one-line description)
- [ ] Reference to where detailed info lives (.claude/rules/, ARCHITECTURE.md)
- [ ] Development workflow specific to this project (not general conventions)
- [ ] Environment variables and external dependencies
