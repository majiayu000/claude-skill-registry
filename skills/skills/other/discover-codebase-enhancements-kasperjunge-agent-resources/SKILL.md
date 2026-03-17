---
name: discover-codebase-enhancements
description: Use when the user asks for a deep codebase analysis to identify and rank improvements, optimizations, architectural enhancements, or potential bugs aligned to developer, end-user, and agent jobs-to-be-done.
---

# Discover Codebase Enhancements

## Overview
Spend significant time crawling and analyzing the codebase to surface high-impact improvements. Center findings on the jobs-to-be-done of the codebase, developers, end users, and AI agents working in the repo.

## Inputs (ask if missing, max 5)
- Target area or scope (whole repo or specific modules)
- Primary user jobs-to-be-done and business goals
- Known pain points or incidents
- Constraints (time, risk tolerance, release window)
- Evidence sources allowed (tests, metrics, logs)

## Jobs-to-Be-Done Lens
- **Codebase**: reliability, simplicity, maintainability
- **Developers**: speed, clarity, safe changes
- **End users**: correctness, performance, usability
- **AI agents**: discoverability, consistency, explicit patterns

## Workflow
1. **Deep crawl**
   - Read architecture docs, READMEs, key modules, and tests.
   - Search for hotspots (TODO/FIXME, large files, duplication, complex flows).
2. **Evidence gathering**
   - Note error-prone areas, missing tests, performance risks, and coupling.
   - Capture references to files/functions and concrete symptoms.
3. **Opportunity synthesis**
   - Group findings by theme: correctness, performance, DX, architecture, tests, tooling.
4. **Impact scoring**
   - Rate impact, effort, risk, and evidence strength.
5. **Ranked recommendations**
   - Present top enhancements with rationale and expected outcomes.

## Output Format
```
## Codebase Enhancement Discovery

### Context Summary
[1-3 sentences]

### JTBD Summary
- Codebase: ...
- Developers: ...
- End users: ...
- AI agents: ...

### Evidence Sources
- Files/modules reviewed: ...
- Patterns searched: ...
- Tests or metrics considered: ...

### Ranked Enhancements
1) [Enhancement]
   - Category: ...
   - Impact: high | Effort: medium | Risk: low | Evidence: moderate
   - Rationale: ...
   - Affected areas: ...

### Quick Wins
- ...

### Open Questions
- ...
```

## Quick Reference
- Spend more time exploring than feels necessary.
- Prefer evidence-backed findings over speculation.
- Center recommendations on user and developer outcomes.

## Common Mistakes
- Skimming without enough code context
- Listing fixes without evidence or impact scoring
- Ignoring AI agent or developer workflows
- Recommending changes that fight existing architecture
