---
name: cc-documentation-quality
description: "Review documentation quality across README, comments, API docs, changelog, and AI documentation (CLAUDE.md, .cursorrules, copilot-instructions). Use when checking if documentation matches code, comments are stale, new features lack docs, or reviewing PR documentation. Triggers on: review docs, stale comments, update changelog, documentation debt, README accuracy, PR documentation review, missing docs."
---

# Documentation Quality

## STOP - Documentation Freshness

- **Documentation rots faster than code.** Stale docs are worse than no docs.
- **If code changed, check which docs need updating** - README, CLAUDE.md, API docs, comments
- **Comments explain WHY, not WHAT** - If it repeats the code, delete it

---

## Core Principle

> "The purpose of comments is to explain things that aren't obvious from the code."
> — Ousterhout, APOSD

**Good documentation:**
- Explains WHY, not WHAT
- Uses different words than the code
- Stays synchronized with implementation
- Describes the non-obvious

---

## Documentation Checklist

### 1. README Accuracy
- [ ] Does README describe current behavior?
- [ ] Are setup instructions still valid?
- [ ] Do examples still work?
- [ ] Are dependencies current?
- [ ] Is the feature list accurate?

### 2. Comment Freshness
- [ ] Do comments match the code they describe?
- [ ] Are TODOs still relevant or stale?
- [ ] Do function comments match signatures?
- [ ] Are "temporary" comments actually temporary?

### 3. API Documentation
- [ ] Public interfaces have doc comments?
- [ ] Parameters documented with types and constraints?
- [ ] Return values documented?
- [ ] Exceptions/errors documented?
- [ ] Examples provided for complex APIs?

### 4. Changelog Updates
- [ ] Breaking changes documented?
- [ ] New features listed?
- [ ] Bug fixes noted?
- [ ] Migration instructions for breaking changes?

### 5. Comment Quality (APOSD)
- [ ] Comments describe non-obvious things?
- [ ] Comments use different words than code?
- [ ] Interface comments present (before implementation)?
- [ ] Comments explain "why", not "what"?
- [ ] No comments that repeat the code?

### 6. Missing Documentation
- [ ] New public APIs documented?
- [ ] New configuration options documented?
- [ ] New environment variables documented?
- [ ] New CLI flags documented?

### 7. AI Documentation
Check all AI config files that exist in the project:

| File | Tool |
|------|------|
| `CLAUDE.md` | Claude Code |
| `.cursorrules` / `.cursorignore` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `AGENTS.md` | Copilot Workspace |
| `.windsurfrules` | Windsurf |
| `.aider.conf.yml` | Aider |
| `.continue/config.json` | Continue.dev |
| `.clinerules` | Cline |
| `.roomodes` | Roo Code |
| `CONVENTIONS.md` | Various |

- [ ] AI docs reflect current architecture?
- [ ] Agent/skill descriptions accurate?
- [ ] File structure documentation up to date?
- [ ] All AI config files consistent with each other?
- [ ] Version numbers synchronized?

---

## Comment Anti-Patterns

| Anti-Pattern | Example | Problem |
|--------------|---------|---------|
| Repeat the code | `i++ // increment i` | Zero value |
| State the obvious | `// loop through users` | Noise |
| Stale comment | Comment says X, code does Y | Dangerous |
| TODO forever | `// TODO: fix this` from 2019 | Clutter |
| Commented-out code | Dead code masquerading as comment | Confusion |

---

## Comment Patterns That Add Value

| Pattern | Example | Value |
|---------|---------|-------|
| Explain rationale | `// Use insertion sort: n < 10 always` | Design decision |
| Warn about non-obvious | `// Must call before X, else crash` | Prevent bugs |
| Summarize algorithm | `// Binary search on sorted timestamps` | Quick understanding |
| Document edge case | `// Empty list returns -1, not null` | Clarify behavior |
| Reference external | `// Per RFC 7231 section 6.5.4` | Authority |

---

## Severity Guide

| Finding | Severity |
|---------|----------|
| README contradicts actual behavior | CRITICAL |
| API doc says wrong return type | CRITICAL |
| Stale comment causes bug risk | CRITICAL |
| CLAUDE.md describes deleted/renamed files | CRITICAL |
| New public API undocumented | IMPORTANT |
| Breaking change not in changelog | IMPORTANT |
| CLAUDE.md missing new features/agents | IMPORTANT |
| AI doc version mismatch | IMPORTANT |
| Stale TODO from distant past | SUGGESTION |
| Could add clarifying comment | SUGGESTION |
| Minor README improvement | SUGGESTION |

---

## Questions to Ask

1. "If someone reads only the docs, will they use this correctly?"
2. "If the code changes, which docs need updating?"
3. "Does this comment tell me something the code doesn't?"
4. "Is this TODO actionable or just noise?"


---

## Chain

| After | Next |
|-------|------|
| Docs need code changes | Back to implementation |
| Docs verified | Done (pre-commit gate) |

