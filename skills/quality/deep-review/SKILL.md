---
name: deep-review
description: Comprehensive single-document review combining pessimistic and optimistic analysis with improvements. Modifies content.
---

# Deep Review

Comprehensive review that runs both pessimistic and optimistic analysis on a single document, then applies targeted improvements based on findings.

## When to Use

- When `/deep-review` is invoked
- Optionally with a specific file: `/deep-review obsidian/topics/meaning-of-life.md`
- As a daily maintenance task when overdue (integrated with /evolve)

## Instructions

### 1. Select Document

If a specific file is provided as an argument, use it.

Otherwise, use the candidate selection tool to find the highest priority document:

```bash
uv run python scripts/deep_review.py next --obsidian obsidian
```

The tool ranks candidates by:
- Never reviewed (highest priority): base score 100 + days since modification
- Modified since last review: days unreviewed * 2
- Reviewed and unchanged: excluded (no review needed)

If no candidates are found, log to changelog and exit successfully.

### 2. Run Pessimistic Review (Deep Mode)

Read the selected document thoroughly, then apply adversarial analysis using the six philosopher personas from `/pessimistic-review`:

1. **Eliminative Materialist** (Patricia Churchland perspective)
2. **Hard-Nosed Physicalist** (Daniel Dennett perspective)
3. **Quantum Skeptic** (Max Tegmark perspective)
4. **Many-Worlds Defender** (David Deutsch perspective)
5. **Empiricist** (Karl Popper's Ghost perspective)
6. **Buddhist Philosopher** (Nagarjuna perspective)

In deep single-file mode, apply extra scrutiny:
- All six personas must engage specifically with this content
- Look for subtle logical gaps, not just obvious flaws
- Evaluate style guide compliance in detail (see `obsidian/project/writing-style.md`)
- Check every factual claim for support
- Identify internal contradictions

Capture findings:
- **Critical issues** (must fix)
- **Medium issues** (should fix)
- **Low issues** (nice to fix)
- **Counterarguments needing response**
- **Unsupported claims**

### 3. Run Optimistic Review (Deep Mode)

Apply supportive analysis using the six sympathetic philosopher personas from `/optimistic-review`:

1. **Property Dualist** (David Chalmers perspective)
2. **Quantum Mind Theorist** (Henry Stapp perspective)
3. **Phenomenologist** (Thomas Nagel perspective)
4. **Process Philosopher** (Alfred North Whitehead perspective)
5. **Libertarian Free Will Defender** (Robert Kane perspective)
6. **Mysterian** (Colin McGinn perspective)

In deep single-file mode:
- All six personas must engage specifically with this content
- Identify concrete expansion opportunities within this document
- Note cross-linking potential with existing content
- Find unique phrasings and arguments worth preserving
- Identify strengths in argumentation and communication

Capture findings:
- **Strengths to preserve** (do not change these)
- **Expansion opportunities** (thin sections to develop)
- **Cross-links to add** (connections to other site content)
- **Effective patterns** (communication techniques that work)

### 4. Synthesize and Plan Improvements

Based on both reviews, create an improvement plan:

**Must Address** (from pessimistic):
- All critical issues
- Unsupported claims flagged as high priority
- Internal contradictions

**Should Address** (balanced):
- Medium-priority issues from pessimistic review
- Natural expansion points from optimistic review
- Missing connections identified by both

**Preserve** (from optimistic):
- Strong arguments and unique insights
- Effective communication patterns
- Author's voice and style that works

### 5. Apply Improvements

Make targeted edits to the document:

1. Address critical and high-priority issues first
2. Add brief responses to the strongest counterarguments
3. Expand thin sections where optimistic review identified opportunities
4. Add cross-links suggested by optimistic review (using `[[wikilink]]` syntax)
5. Preserve original voice and strong passages

Follow `obsidian/project/writing-style.md` guidelines:
- Front-load important information (LLM truncation resilience)
- Use named-anchor pattern for forward references
- Ensure "Relation to Site Perspective" section is substantive

### 6. Update Frontmatter

After improvements, update the file's frontmatter:

```yaml
ai_modified: 2026-01-07T15:30:00+00:00  # Current ISO timestamp
last_deep_review: 2026-01-07T15:30:00+00:00  # Current ISO timestamp
```

If original was human-authored (`ai_contribution: 0`), update to reflect collaboration:
```yaml
ai_contribution: 30  # Or appropriate percentage based on extent of changes
```

### 7. Create Review Archive

Save a combined review report to `obsidian/reviews/deep-review-YYYY-MM-DD-[slug].md`:

```markdown
---
title: "Deep Review - [Document Title]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified: null
ai_modified: YYYY-MM-DDTHH:MM:SS+00:00
draft: false
topics: []
concepts: []
related_articles: []
ai_contribution: 100
author: null
ai_system: [current model]
ai_generated_date: YYYY-MM-DD
last_curated: null
---

# Deep Review: [Document Title]

**Date**: YYYY-MM-DD
**File**: [filepath]
**Previous review**: [Never / YYYY-MM-DD]

## Pessimistic Analysis Summary

### Critical Issues Found
- [Issue]: [Resolution applied]

### Medium Issues Found
- [Issue]: [Resolution applied or deferred]

### Counterarguments Considered
- [Argument]: [How addressed]

## Optimistic Analysis Summary

### Strengths Preserved
- [Strength]

### Enhancements Made
- [Enhancement]

### Cross-links Added
- [[linked-article]]

## Remaining Items

[Any issues deferred for future work, or "None"]
```

### 8. Update Todo (if needed)

If significant issues remain that couldn't be addressed in this session:

```markdown
### P2: Follow-up items from deep review of [filename]
- **Type**: refine-draft
- **Status**: pending
- **Notes**: Deep review deferred: [list specific items]
```

### 9. Log to Changelog

Append to `obsidian/workflow/changelog.md`:

```markdown
### HH:MM - deep-review
- **Status**: Success
- **File**: [filepath]
- **Critical issues addressed**: [count]
- **Medium issues addressed**: [count]
- **Enhancements made**: [count]
- **Output**: `reviews/deep-review-YYYY-MM-DD-[slug].md`
```

### 10. Commit Changes

Create a git commit:

```
review(deep): Comprehensive review of [filename]

Addressed:
- [Key issue 1]
- [Key issue 2]

Enhanced:
- [Key enhancement]
```

## What NOT to Do

- Don't rewrite content that's working well (preserve strengths)
- Don't add filler content to address "thin" sections
- Don't remove the author's voice or distinctive style
- Don't ignore strong counterarguments from pessimistic review
- Don't skip updating `last_deep_review` timestamp
- Don't review the same document twice in quick succession

## Scoring and Selection

The candidate selection algorithm prioritizes:

1. **Never reviewed** (score = 100 + days_since_modified)
   - A document modified 10 days ago that's never been reviewed scores 110

2. **Modified since review** (score = days_unreviewed * 2)
   - A document reviewed 5 days ago but modified since scores 10

3. **Reviewed, unchanged** (excluded)
   - Documents where content hasn't changed since last review are skipped

This ensures new content gets reviewed first, then modified content, while avoiding redundant reviews.

## Important

- This skill MODIFIES content (unlike standalone pessimistic/optimistic reviews)
- Always update both `ai_modified` and `last_deep_review` timestamps
- Document all changes in the review archive
- The goal is improvement, not perfection
- Preserve what works while fixing what doesn't
- Run daily as part of /evolve workflow