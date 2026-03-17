---
name: deep-review
description: Comprehensive single-document review combining pessimistic and optimistic analysis with improvements. Modifies content.
---

# Deep Review

Comprehensive review that runs both pessimistic and optimistic analysis on a single document, then applies targeted improvements based on findings.

## When to Use

- When `/deep-review` is invoked
- Optionally with a specific file: `/deep-review obsidian/topics/meaning-of-life.md`
- As a regular maintenance task in the evolution loop cycle

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

### 1.5. Check Previous Reviews

Before reviewing, check if this document has been reviewed before:

```bash
ls -t obsidian/reviews/deep-review-*-[slug].md 2>/dev/null | head -1
```

**If a previous review exists, READ IT.** This is critical for convergence:
- Note what issues were previously identified and marked as resolved
- Note what counterarguments were already addressed
- Note what strengths were identified (preserve these)

**Issue tracking rule**: If a previous review marked an issue as "resolved," do NOT re-flag it as critical unless:
1. The resolution was actually incorrect or incomplete
2. New content has been added that reintroduces the problem
3. The article has been substantively modified since the last review

Philosophical disagreements that were acknowledged as "bedrock disagreements" in a previous review should NOT be re-flagged. The goal is convergence, not endless oscillation.

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

Capture findings using these severity definitions:

**Critical issues** (must fix) — ONLY flag as critical if:
- Factual error (wrong date, misattributed quote, incorrect scientific claim)
- **Attribution error** (claims attributed to wrong author, or claims author didn't make)
- **Dropped qualifiers** that change meaning (e.g., "default causal profile" → "causal profile")
- Internal contradiction (article contradicts itself)
- Missing required section (e.g., no "Relation to Site Perspective")
- Broken links or references
- Severe style guide violation (e.g., missing front-loaded summary)
- **Source/Map conflation** (Map interpretation presented as source's claim)

**NOT critical** — These are medium or low, not critical:
- "Persona X disagrees with the position" (philosophical disagreement is expected)
- "Response to objection Y could be stronger" (unless it's a strawman)
- "Section Z is thin" (expansion opportunity, not critical flaw)
- Issues that were addressed in a previous review

**Medium issues** (should fix):
- Weak engagement with major counterarguments
- Missing cross-links to related content
- Prose that could be tightened

**Low issues** (nice to fix):
- Minor style improvements
- Additional examples that could help

**Counterarguments needing response** — Note these separately

**Unsupported claims** — Flag factual claims without support

### 2.5 Attribution Accuracy Check (Required for Source-Based Articles)

If the article is based on a specific source (research paper, philosopher's work), run this dedicated check. **These errors are critical** because they damage credibility.

#### Misattribution Check
- [ ] Are all claims attributed to the source actually in the source?
- [ ] Did we attribute a framework/constraints to the right author? (e.g., "five constraints" are Saad's, not Chalmers')
- [ ] Did we claim the author discusses something they don't? (e.g., "Many-Worlds" when they don't mention it)

#### Qualifier Preservation Check
- [ ] Are crucial qualifiers preserved? ("default causal profile" not just "causal profile")
- [ ] Did we change "X or at least Y" to just "X"?
- [ ] Did we change "some" to "all" or "wherever"?

#### Position Strength Check
- [ ] Did we present exploratory positions as commitments? ("explores" ≠ "argues")
- [ ] Did we claim shared commitments that aren't shared? (e.g., "shares our rejection of MWI" when author expresses "sympathy for MWI")
- [ ] Did we use "solves" or "answers" when source uses "addresses" or "explores"?

#### Source/Map Separation Check
- [ ] Is source exposition clearly separated from Map interpretation?
- [ ] Are Map-specific arguments (tenets, quantum interactionism) clearly labeled as such?
- [ ] Did we inject Map arguments as if they came from the source?

#### Self-Contradiction Check
- [ ] Did we claim something is "not required" but also "required" in different sections?
- [ ] Are claims about the theory's commitments consistent throughout?

**If any check fails, this is a CRITICAL issue.** Fix it before proceeding to optimistic review.

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

### 4.5 Length Check (Length-Neutral Mode)

Before applying improvements, check article length against section thresholds:

```bash
uv run python -c "
from pathlib import Path
from tools.curate.length import analyze_length
a = analyze_length(Path('[filepath]'))
print(f'{a.word_count} words ({a.excess_percent:.0f}% of {a.soft_threshold} target) - {a.status}')
"
```

**Thresholds by section (soft/hard/critical):**
| Section | Soft | Hard | Critical |
|---------|------|------|----------|
| concepts/ | 2500 | 3500 | 5000 |
| topics/ | 3000 | 4000 | 6000 |
| apex/ | 4000 | 5000 | 6500 |
| voids/ | 2000 | 3000 | 4000 |

**If article is at or above soft threshold:**
- Operate in **length-neutral mode**
- For each addition, identify an equivalent passage to trim or remove
- Combine sections where possible instead of adding new ones
- Prefer tightening prose over adding new content
- Replace verbose explanations with links to existing concept pages

**If article exceeds hard threshold:**
- Apply condensation as part of this review
- Follow `/condense` principles: cut redundancy, extract tangents, tighten prose
- Document word count before/after in the review archive

**If article is below soft threshold:**
- Normal improvements allowed
- Expansion opportunities from optimistic review can be addressed

### 5. Apply Improvements

Make targeted edits to the document:

1. Address critical and high-priority issues first
2. Add brief responses to the strongest counterarguments
3. Expand thin sections where optimistic review identified opportunities
4. Add cross-links suggested by optimistic review (using `[[wikilink]]` syntax)
5. Preserve original voice and strong passages
6. **Add `description` if missing** — 150-160 chars emphasizing human+AI collaboration, iterative refinement, pursuit of truth (not generic)

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

**Date**: YYYY-MM-DD
**Article**: [[article-slug|Article Title]]
**Previous review**: [[previous-review-slug|YYYY-MM-DD]] or Never

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

## Stability Notes

[Note any issues that represent fundamental philosophical disagreements rather than fixable problems. Future reviews should NOT re-flag these as critical. Example: "MWI proponents will always find the indexical argument unsatisfying—this is a bedrock disagreement, not a flaw to fix."]
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

Prepend to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - deep-review
- **Status**: Success
- **File**: [[filepath without .md extension]]
- **Word count**: [before] → [after] ([+/-change])
- **Critical issues addressed**: [count]
- **Medium issues addressed**: [count]
- **Enhancements made**: [count]
- **Output**: [[reviews/deep-review-YYYY-MM-DD-slug]]
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
- Don't expand articles already at or above soft threshold without equivalent cuts
- Don't ignore length warnings - if the article is too long, address it
- **Don't re-flag issues that previous reviews marked as resolved** — If a prior review said "addressed Dennett's heterophenomenology," don't flag "functionalist response too weak" again unless there's a specific new problem
- **Don't treat philosophical disagreement as "critical"** — The adversarial personas are *designed* to disagree with dualist content. "MWI defender finds this unsatisfying" is not a critical issue; it's an expected philosophical standoff
- **Don't oscillate** — If you find yourself wanting to expand something a previous review trimmed (or vice versa), that's a signal the article has reached stability, not that it needs more changes

### Attribution Errors to Catch

These errors have been identified in outer reviews and ARE critical issues:

- **Don't miss misattribution** — If the article says "Chalmers argues X" but X is actually from Saad, this is critical
- **Don't miss dropped qualifiers** — "Default causal profile" → "causal profile" loses essential meaning
- **Don't miss overstated positions** — "Explores" → "argues" is a misrepresentation
- **Don't miss source/Map conflation** — Map's quantum speculation presented as if it's the source author's claim
- **Don't miss self-contradiction** — Claiming theory "doesn't require X" then later "requires X"
- **Don't miss false shared commitments** — Claiming author "shares our rejection of MWI" when they express sympathy for MWI

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
- Runs regularly as part of the evolution loop cycle
- **Convergence matters**: Articles should stabilize after 2-3 reviews. If you're making similar changes to what previous reviews made, the article is likely already at a good state. A review that finds "no critical issues" is a SUCCESS, not a failure to find problems.