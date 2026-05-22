---
name: enhance-docs
description: Use when documentation needs to be updated, clarified, or reorganized to better serve users' jobs-to-be-done with low cognitive load and high signal.
---

# Enhance Docs

## Overview
Improve documentation so it is up to date, coherent, and centered on users' jobs-to-be-done. Favor less content with higher clarity.

## Inputs (ask if missing, max 5)
- Docs scope (which files or sections)
- Primary audiences and their jobs-to-be-done
- Source of truth for product behavior (code, APIs, changelog)
- Recent changes or upcoming releases
- Constraints (tone, length, compliance, deadlines)

## Principles
- **Less is more**: reduce noise, keep only what helps users act.
- **Low cognitive load**: short paragraphs, clear headings, predictable structure.
- **High signal**: prioritize steps, outcomes, and decision points.
- **JTBD-first**: structure around what users are trying to accomplish.

## Workflow
1. **Map jobs-to-be-done**
   - List top 3-5 user jobs and the docs that should enable each.
2. **Check freshness and accuracy**
   - Compare docs against current behavior, APIs, and recent changes.
3. **Simplify and restructure**
   - Remove redundancy, collapse long lists, and apply progressive disclosure.
4. **Improve coherence**
   - Align terminology, fix contradictions, and add consistent cross-links.
5. **Clarify with examples**
   - Add minimal examples only where they unblock action.
6. **Deliver ranked improvements**
   - Prioritize changes by impact on user success and confusion reduction.

## Output Format
```
## Documentation Enhancement

### Context Summary
[1-3 sentences]

### JTBD Map
- Job: ... -> Docs: ... -> Success criteria: ...

### Issues (ranked)
1) [Issue] — impact: high, evidence: ...

### Proposed Changes (ranked)
1) [Change] — rationale: ...

### Quick Wins
- ...

### Open Questions
- ...
```

## Quick Reference
- Trim before adding.
- Structure by jobs and outcomes, not features.
- Keep headings short and action-oriented.

## Common Mistakes
- Adding more text instead of removing noise
- Mixing audiences in the same section
- Describing features without user tasks
- Missing cross-links or inconsistent terminology
