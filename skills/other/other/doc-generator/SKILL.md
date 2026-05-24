---
name: doc-generator
description: 'Generate or remediate documentation with human-quality writing and style.'
globs: "**/*.md"
alwaysApply: false
  adherence. Use when creating new documentation, rewriting AI-generated content,
  or applying style profiles. Do not use for slop detection only (use slop-detector)
  or learning styles (use style-learner).
category: artifact-generation
tags:
- documentation
- writing
- generation
- remediation
- polish
tools: []
complexity: medium
model_hint: standard
estimated_tokens: 1600
progressive_loading: true
modules:
- modules/generation-guidelines.md
- modules/remediation-workflow.md
- modules/quality-gates.md
dependencies:
- scribe:shared
- scribe:slop-detector
---
# Documentation Generator

**A document costs the sum of its readers' time. Earn that
cost or cut.**

Generate documents that are grounded in specific claims, lead
with their thesis, and earn every sentence. Filler phrases like
"In today's fast-paced world" and vague descriptors like
"thorough" or "complete" without evidence are bloat. So is
any sentence that does not carry, instance, bound, or repeat
the document's one takeaway.

This skill enforces both **sentence-level cleanliness** (no
slop vocabulary, em dash overuse, or sycophantic openers) and
**document-level economy** (thesis-first, every sentence
earns weight, repetition reserved for the thesis). See
`Skill(scribe:slop-detector)` module `document-economy.md`
for the full rubric.

## Core Writing Principles

Use active voice and an authorial perspective. Explain the
reasoning behind technical choices (why this database, not
that one) rather than presenting neutral boilerplate. Use
bullets sparingly for short, parallel summaries; convert
multi-line bullet waterfalls into prose so the reasoning
survives.

### Vocabulary and Style

Avoid business jargon and linguistic tics like mirrored
sentence structures or em dash overuse. Use the imperative
mood for docstrings ("Validate input", not "Validates").
Do not humanize non-living constructs ("the code wants",
"the function speaks to").

| Instead of | Use |
|------------|-----|
| fallback | default, secondary |
| leverage | use |
| utilize | use |
| facilitate | help, enable |
| comprehensive | thorough, complete |

### 9. Limit Humanizing Constructs

"Lives under," "speaks to," and similar phrases only make sense
for living things.

### 10. Imperative Mood for Docstrings

"Validate" not "Validates" (per PEP 257, pydocstyle, ruff).

## Required TodoWrite Items

1. `doc-generator:scope-defined` - Target files and type identified
2. `doc-generator:style-loaded` - Style profile applied (if available)
3. `doc-generator:content-drafted` - Initial content created
4. `doc-generator:slop-scanned` - AI markers checked
5. `doc-generator:quality-verified` - Principles checklist passed
6. `doc-generator:user-approved` - Final approval received

## Mode: Generation

For new documentation:

### Step 1: Define Scope

```markdown
## Generation Request

**Type**: [README/Guide/API docs/Tutorial]
**Audience**: [developers/users/admins]
**Audience size**: [1 / small team / org / public]
**Read frequency**: [once / weekly / per-invocation]
**Thesis**: [one sentence the reader must walk away with]
**Length target**: [~X words or sections]
**Style profile**: [profile name or "default"]
```

The **Thesis** field is required. If you cannot state the
takeaway in one sentence, the scope is not ready. Audience
size and read frequency feed the reader-time budget (see
`scribe:slop-detector` module `document-economy.md`): a
skill loaded daily by 50 users has a wildly different
budget than a 1:1 design note.

### Step 2: Load Style (if available)

If a style profile exists:
```bash
cat .scribe/style-profile.yaml
```

Apply voice, vocabulary, and structural guidelines.

### Step 3: Draft Content

**Lead with the thesis.** The first paragraph must state the
single takeaway. If a reader stops after the lead, they should
still leave with the message. Echo the thesis once in the body
and once at the close; cut every other repetition.

Follow the 10 core principles above. For each section:

1. Start with the essential information (state the thesis or
   a clear instance of it)
2. Add context only if it adds value (does it carry, instance,
   or bound the thesis?)
3. Use specific examples (one is proof; two is emphasis;
   three is filler)
4. Prefer prose over bullets
5. End when information is complete (no summary padding,
   no "in conclusion" restatements)

### Step 4: Run Slop Detector

```
Skill(scribe:slop-detector)
```

Fix any findings before proceeding.

### Step 5: Quality Gate

Verify against checklist:

Sentence-level:
- [ ] No tier-1 slop words
- [ ] Em dash count < 3 per 1000 words
- [ ] Bullet ratio < 40%
- [ ] All claims grounded with specifics
- [ ] No formulaic openers or closers
- [ ] Authorial perspective present
- [ ] No emojis (unless explicitly requested)

Document-level (document-economy module):
- [ ] Thesis stated in the lead, single and clear (2/2)
- [ ] >80% of sentences carry, instance, bound, or repeat
      the thesis (2/2)
- [ ] Thesis echoed at least 3 times; non-thesis repetition
      cut (2/2)
- [ ] Writing time roughly proportional to (audience size ×
      read frequency × per-read time)

## Mode: Remediation

For cleaning up existing content:

Load: `@modules/remediation-workflow.md`

### Step 1: Analyze Current State

```bash
# Get slop score
Skill(scribe:slop-detector) --target file.md
```

### Step 2: Section-by-Section Approach

For large files (>200 lines), edit incrementally:

```markdown
## Section: [Name] (Lines X-Y)

**Current slop score**: X.X
**Issues found**: [list]

**Proposed changes**:
1. [Change 1]
2. [Change 2]

**Before**:
> [current text]

**After**:
> [proposed text]

Proceed? [Y/n/edit]
```

### Step 3: Preserve Intent

Never change WHAT is said, only HOW. If meaning is unclear, ask.

### Step 4: Re-verify

After edits, re-run slop-detector to confirm improvement.

## Docstring-Specific Rules

When editing code comments:

1. **ONLY modify docstring/comment text**
2. **Never change surrounding code**
3. **Use imperative mood** ("Validate input" not "Validates input")
4. **Brief is better** - remove filler
5. **Keep Args/Returns structure** if present

## Module Reference

- See `modules/generation-guidelines.md` for content creation patterns
- See `modules/quality-gates.md` for validation criteria

## Integration with Other Skills

| Skill | When to Use |
|-------|-------------|
| slop-detector | After drafting, before approval |
| style-learner | Before generation to load profile |
| sanctum:doc-updates | For broader doc maintenance |

## Exit Criteria

- Content created or remediated
- Slop score < 1.5 (clean rating)
- Quality gate checklist passed
- User approval received
- No emojis present (unless specified)
