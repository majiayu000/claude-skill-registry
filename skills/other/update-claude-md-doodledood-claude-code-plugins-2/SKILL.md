---
name: update-claude-md
description: Create or update CLAUDE.md with best practices - brevity, universal applicability, progressive disclosure
---

Update my CLAUDE.md based on: $ARGUMENTS

Current CLAUDE.md:
@CLAUDE.md

---

Make targeted updates based on my request. Only explore codebase if essential info is missing.

If my request conflicts with best practices below, still make the update but note the tradeoff.

**Best Practices** (CLAUDE.md is the highest-leverage config point):

**Structure** - Cover these if creating/missing critical sections:
- **WHAT**: Tech stack, project structure, key entry points (critical for monorepos)
- **WHY**: Project purpose, component relationships, domain terminology
- **HOW**: Build/test/run commands, verification steps

**Length** (LLMs follow ~150 instructions reliably; system uses ~50):
- Simple: 30-60 lines | Standard: 60-150 | Complex: 150-300 max

**Progressive Disclosure** - For complex projects, create separate docs and reference them:
```
docs/testing.md, docs/architecture.md, docs/conventions.md
```
Then in CLAUDE.md: "See docs/testing.md for test patterns"

**Prefer pointers over copies** - Use `file:line` references instead of pasting code snippets (avoids staleness).

**Do**: Universal instructions | Imperative language | Verified commands | Reference (don't copy) README

**Don't**:
- Style rules → use linters, formatters, or Claude Code hooks instead
- Task-specific instructions → gets ignored if not relevant to current task
- File/function enumeration → describe patterns instead
- Auto-generated boilerplate

Bad: `Always use camelCase. Document with JSDoc.`
Good: `npm test  # Required before PR`

Verify: <300 lines, no style rules, universal instructions, commands tested.
