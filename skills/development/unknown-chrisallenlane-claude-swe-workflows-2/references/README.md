# /tidy-docs - Documentation Hygiene

## Overview

The `/tidy-docs` skill spawns a `doc-maintainer` agent to comprehensively audit all project documentation. It audits every documentation file for correctness, completeness, freshness, and consistency — then fixes what it can within its authority and reports anything requiring user approval.

The skill lives in the `/tidy-*` namespace because the find→fix seam is small for most documentation issues — typos, stale code examples, broken links, freshness drift are all mechanical to correct. Anything genuinely judgment-laden (a deprecation that needs a stakeholder decision, an architectural claim that may no longer be true) surfaces in the "Issues Requiring User Approval" section rather than being auto-fixed.

**Key benefits:**
- Catches stale docs, broken links, and code-documentation drift in one sweep
- Autonomous fixes within the agent's authority — no per-fix approval interrupts
- Comprehensive: reviews all docs, not just recently changed ones
- Surfaces judgment-laden items separately so the operator can make those calls
- Offers to commit changes when done

## When to Use

**Use `/tidy-docs` for:**
- After a major feature or refactoring pass
- Before a release (catch stale docs)
- Periodic documentation hygiene
- When you suspect docs have drifted from the code
- As part of `/refactor` or `/review-arch` completion (it runs automatically)

**Don't use `/tidy-docs` for:**
- Updating docs for a specific change (the `/implement` and `/bug-fix` workflows do this as part of their flow)
- Writing new documentation from scratch (just ask directly)

## Workflow

```
┌─────────────────────────────────────────────────────┐
│                  TIDY-DOCS                          │
├─────────────────────────────────────────────────────┤
│  1. Spawn doc-maintainer agent                      │
│     • Discovers all .md files in project            │
│     • Reviews each for quality checklist:           │
│       - Code-documentation consistency              │
│       - Completeness                                │
│       - Link validation                             │
│       - Style consistency                           │
│       - Freshness                                   │
│     • Fixes issues autonomously (within authority)  │
│  2. Report results to user                          │
│     • What was reviewed                             │
│     • What was changed                              │
│     • Issues requiring user approval                │
│  3. Commit (optional, if changes were made)         │
└─────────────────────────────────────────────────────┘
```

## Example Session

```
> /tidy-docs

Spawning doc-maintainer agent for comprehensive audit...

## Documentation Audit Report

### Changes Made
1. skills/implement/references/README.md — Updated example to match current CLI flags
2. CLAUDE.md — Fixed skill list ordering to match directory structure

### Issues Requiring User Approval
- README.md installation section references deprecated flag (needs user decision on replacement)

### No Issues Found
- Link validation: all links resolve
- Style consistency: headings, code blocks, terminology all consistent
- Freshness: no references to removed features

Commit documentation fixes?
> Yes

Committed: "docs: tidy project documentation"
```

## Tips

1. **Run after `/refactor`, or after acting on `/review-arch`'s recommendations.** Code restructuring — tactical or architectural — often makes docs stale.

2. **Run before releases.** Stale docs in a release are embarrassing. A quick `/tidy-docs` pass catches drift. For a full pre-release sweep across every review dimension, `/review-deep` runs `/tidy-docs` as one of its phases.

3. **Different from `/implement` step 9.** The `/implement` workflow's documentation step is scoped to the git diff. `/tidy-docs` audits everything regardless of recent changes.
