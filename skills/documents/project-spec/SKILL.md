---
name: project-spec
description: Generate CLAUDE.md project files. Execution contracts that eliminate ambiguity.
---

# Project Spec Skill

**Core Principle:** A good CLAUDE.md means Claude never has to guess.

## Template Selection

| Project | Use |
|---------|-----|
| Quick build (<8h) | template-minimal.md |
| Complex / Calculator / Multi-page | template-full.md |

## Defaults (Don't specify if these apply)

```
Code maturity: Production
Maintainer: Solo dev
Lifetime: Multi-year
Tech debt: Minimal, documented
Failure impact: Business-impacting
Code ownership: Shared
Review strictness: Standard
Error handling: Fail fast
Logging: Basic (errors)
Data sensitivity: Personal
UI tolerance: Visually close
Refactor permission: None
Dependency policy: Well-known only
Human review: Detailed
Output timing: Correctness first (not fast draft)
Partial completion: Not acceptable
Session: Expect interruptions, be resumable
```

Only specify **deviations** from defaults.

## Required Sections (Every CLAUDE.md)

```
[CRITICAL] Critical Rules (stop-on-missing, non-goals)
[CRITICAL] Project Overview (type, goal, timeline)
[CRITICAL] Scope (in/out/future)
[CRITICAL] Constraints
[CRITICAL] Definition of Done
```

## Critical Rules Block (Copy to every CLAUDE.md)

```markdown
## ⚠️ Critical Rules

**If info missing:** STOP → List missing → Ask → Do NOT assume

**Claude must NOT:**
- Add features outside this document
- Add dependencies without approval
- Refactor unrelated code
- Make "improvements" outside scope

**Authority:** CLAUDE.md > skills > comments > chat > assumptions (FORBIDDEN)
```

## Anti-Patterns

| ❌ Bad | ✅ Good |
|--------|---------|
| "Make it look professional" | "#1a1a1a text, Inter 700, 48px H1" |
| "Standard contact form" | "Fields: Name*, Email*, Phone, Message*" |
| "Similar to competitor" | "Hero: 60/40 split, CTA left" |
| "Client will provide" | "Copy pending by [date]" |
| "Modern design" | "Tailwind, rounded-lg, shadow-sm" |

## Tier Markers

| Marker | Meaning |
|--------|---------|
| `[CRITICAL]` | Read before coding |
| `[REFERENCE]` | Read when needed |
| `[NO-IMPL]` | Doesn't affect code |

## References

- [template-minimal.md](references/template-minimal.md) — Quick builds
- [template-full.md](references/template-full.md) — Complex projects
- [examples.md](references/examples.md) — Real examples
