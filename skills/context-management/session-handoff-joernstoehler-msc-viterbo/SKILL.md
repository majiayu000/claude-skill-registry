---
name: session-handoff
description: Use this skill proactively when wrapping up a session to prepare the repo for the next agent. Read this before finalizing PRs, closing issues, or ending sessions.
---

# Session Handoff

This project is long-running with many agents working sequentially and in parallel. Always leave the repo in a state where the next agent can pick up work without confusion.

## Core Principles

### 1. No False or Misleading Content
Remove stale information that would confuse future agents.

**Actions:**
- Edit or delete documentation for removed features
- Update code comments when implementation changes
- Remove TODO comments that are already done
- Delete outdated architecture notes

### 2. Preserve Context Where It's Needed
Put the "why" where future agents will look for it.

**Actions:**
- Add code comments explaining non-obvious design decisions
- Write architecture decision records in `docs/` folders
- Update thesis sections with experiment rationale and status
- Document what worked and what didn't in data directories

### 3. Move Toward Standard Patterns
Long-running projects accumulate complexity. Fight this by refactoring toward well-known patterns.

**Actions:**
- Separate tangled experiments into independent ones
- Replace custom solutions with standard patterns when possible
- Use standard terminology (e.g., data science terms) over project-specific jargon
- Simplify interfaces between components (use simple data artifacts)
- Tell Jörn when you find better standard terminology he should adopt

**Rationale:** Agents know standard patterns well. Custom patterns require extra learning time that compounds across sessions.

### 4. Track Approval Status
Distinguish what Jörn approved from agent proposals. This is critical for project management.

**Markers to use:**
- `<!-- approved -->` - Jörn explicitly approved this
- `<!-- unapproved -->` - Agent proposal awaiting Jörn's review
- Code comment: "API unstable (not Jörn-approved)" vs "API stable (Jörn-approved)"

**Where this matters:**
- GitHub issue bodies and roadmap documents
- Public API function signatures
- Thesis structure and major claims
- Experimental methodologies

## Before Ending Your Session

1. **Clean up**: Remove misleading content, fix stale comments
2. **Document decisions**: Add "why" context where future agents need it
3. **Update research ledger**: Record findings in thesis appendix (see packages/latex_viterbo/chapters/appendix-research-ledger.tex)
4. **Mark approval status**: Add `<!-- approved -->` or `<!-- unapproved -->` markers
5. **Simplify if possible**: Did you introduce complexity that could be standard patterns instead?

## Questions for Skill Maintainers

<!--
Q: Should we have a checklist that agents run through before wrapping up?
Q: Are there other approval markers we need beyond approved/unapproved?
Q: Should we enforce that all GitHub issues have approval markers in their bodies?
-->
