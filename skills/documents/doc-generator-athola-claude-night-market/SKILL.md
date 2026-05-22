---
name: doc-generator
description: |

  Triggers: documentation, generate docs, write docs, technical writing
  Generate or remediate documentation with human-quality writing and style adherence.

  Triggers: generate documentation, write readme, create guide, doc generation,
  technical writing, remediate docs, polish content, clean up docs

  Use when: creating new documentation, rewriting AI-generated content,
  applying style profiles to content, polishing drafts

  DO NOT use when: just detecting slop - use slop-detector for analysis only.
  DO NOT use when: learning styles - use style-learner first.

  Use this skill to produce human-quality documentation.
category: artifact-generation
tags: [documentation, writing, generation, remediation, polish]
tools: [Read, Write, Edit, TodoWrite]
complexity: medium
estimated_tokens: 1600
progressive_loading: true
modules:
  - generation-guidelines
  - remediation-workflow
  - quality-gates
dependencies:
  - scribe:shared
  - scribe:slop-detector
  - scribe:style-learner
---

# Documentation Generator Skill

Create and remediate documentation that reads as human-written.

## Core Writing Principles

These principles override defaults and must guide all content:

### 1. Ground Every Claim

Explain WHY with specifics. If you catch yourself writing "ensures," "comprehensive," or "holistic" without evidence, pause.

Before: "This provides comprehensive coverage."
After: "This covers all 47 API endpoints in v2.3."

### 2. Trim Rhetorical Crutches

Skip formulaic openings and forced wrap-ups. End sections once useful information is delivered.

Remove: "In today's fast-paced world...", "In conclusion..."

### 3. Use Specifics

Numbers, commands, filenames, or short anecdotes beat adjectives. If there's no concrete detail, acknowledge what's unknown.

Before: "enterprise-ready solution"
After: "tested with 10M requests/day in production"

### 4. Balance Bullets with Narrative

Bullets summarize actionable items. Long bullet waterfalls invite slop. Convert multi-line bullets to short paragraphs when nuance matters.

### 5. Watch for Linguistic Tics

Overuse of em dashes, mirrored structures, or catchphrases is a giveaway. Read sections aloud. If they sound like templated emails, rework them.

### 6. Show Authorial Perspective

Mention decisions, risks, or why a choice was made. A consistent team voice beats neutral boilerplate.

Before: "The system uses Redis."
After: "We chose Redis over Memcached because sorted sets power our leaderboard."

### 7. Avoid Ambiguous Cliches

Remove phrases like "keeps us honest" or "isn't just X, it's Y." Speak directly about the topic.

### 8. Vocabulary Substitutions

| Instead of | Use |
|------------|-----|
| fallback | default, secondary |
| leverage | use |
| utilize | use |
| facilitate | help, enable |
| comprehensive | thorough, complete |

### 9. Limit Humanizing Constructs

"Lives under," "speaks to," and similar phrases only make sense for living things.

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
**Length target**: [~X words or sections]
**Style profile**: [profile name or "default"]
```

### Step 2: Load Style (if available)

If a style profile exists:
```bash
cat .scribe/style-profile.yaml
```

Apply voice, vocabulary, and structural guidelines.

### Step 3: Draft Content

Follow the 10 core principles above. For each section:

1. Start with the essential information
2. Add context only if it adds value
3. Use specific examples
4. Prefer prose over bullets
5. End when information is complete (no summary padding)

### Step 4: Run Slop Detector

```
Skill(scribe:slop-detector)
```

Fix any findings before proceeding.

### Step 5: Quality Gate

Verify against checklist:
- [ ] No tier-1 slop words
- [ ] Em dash count < 3 per 1000 words
- [ ] Bullet ratio < 40%
- [ ] All claims grounded with specifics
- [ ] No formulaic openers or closers
- [ ] Authorial perspective present
- [ ] No emojis (unless explicitly requested)

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
