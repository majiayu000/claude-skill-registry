---
name: check-ushabti-prerequisites
description: Verify required Ushabti files exist before proceeding. Use when starting agent work to ensure prerequisites are met.
user-invocable: false
---

# Ushabti Prerequisites

## How to Check Prerequisites

Run these commands to verify required files exist:

```bash
[ -f .ushabti/laws.md ] && echo "✓ laws.md exists" || echo "✗ laws.md MISSING (run Lawgiver)"
[ -f .ushabti/style.md ] && echo "✓ style.md exists" || echo "✗ style.md MISSING (run Artisan)"
[ -f .ushabti/docs/index.md ] && echo "✓ docs/index.md exists" || echo "✗ docs/index.md MISSING (run Surveyor)"
[ -d .ushabti/phases ] && echo "✓ phases/ exists" || echo "✗ phases/ MISSING (run Scribe)"
```

## Required Files by Agent

| Agent | laws.md | style.md | docs/ | phases/ |
|-------|---------|----------|-------|---------|
| Lawgiver | Creates | — | Creates scaffold | — |
| Artisan | Required | Creates | — | — |
| Surveyor | — | — | Creates comprehensive | — |
| Scribe | Required | Required | Required (scaffold OK) | Creates |
| Builder | Required | Required | Recommended | Required |
| Overseer | Required | Required | Recommended | Required |

## Bootstrap Flow

**For a new project (empty directory):**

1. **Lawgiver** — Creates `.ushabti/laws.md` and a minimal docs scaffold (`.ushabti/docs/index.md`)
2. **Artisan** — Creates `.ushabti/style.md`, recommends Surveyor for comprehensive docs
3. **Surveyor** (optional) — Creates comprehensive documentation in `.ushabti/docs/`
4. **Scribe** — Plans the first Phase (scaffold docs are sufficient to proceed)
5. **Builder** — Implements the Phase
6. **Overseer** — Reviews and approves the Phase

**For an existing project:**

1. **Surveyor** — Documents the existing codebase
2. **Lawgiver** — Defines project invariants (docs already exist)
3. **Artisan** — Defines project style
4. **Scribe → Builder → Overseer** — Normal Phase cycle

## Docs Scaffold vs Comprehensive Docs

**Scaffold** (created by Lawgiver): Minimal `index.md` with placeholder content. Marked with "Scaffold documentation" text. Sufficient for Scribe to plan, but Surveyor should run for full documentation.

**Comprehensive** (created by Surveyor): Full project documentation with multiple files covering architecture, systems, and APIs.
