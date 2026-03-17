---
name: check-tenets
description: Verify all site content aligns with the five foundational tenets. Use monthly or after major content additions.
---

# Check Tenet Alignment

Verify that all site content aligns with the foundational tenets and does not contradict them.

## When to Use

- Monthly alignment verification
- After adding major new content
- When `/check-tenets` is invoked
- Before publishing draft content

## The Five Tenets

Read `obsidian/tenets/tenets.md` to get the current tenets. As of last update:

### 1. Dualism
**Rules out:** Eliminative materialism, reductive physicalism, any view treating consciousness as purely epiphenomenal or illusory.

### 2. Minimal Quantum Interaction
**Rules out:** Quantum woo/mysticism, uncontrolled psychokinesis, energy injection by mind, empirically detectable mind-matter interactions.

### 3. Bidirectional Interaction
**Rules out:** Pure epiphenomenalism, parallelism without interaction, views where consciousness is "along for the ride."

### 4. No Many Worlds
**Rules out:** Many-worlds interpretation (MWI), treating all quantum branches as equally real, dismissing indexical identity as meaningless.

### 5. Occam's Razor Has Limits
**Rules out:** Using parsimony as a decisive argument against dualism, treating Occam's Razor as more than a defeasible heuristic.

## Instructions

### 1. Read Current Tenets

Always read `obsidian/tenets/tenets.md` first to get the latest tenet definitions and "Rules out" sections.

### 2. Scan All Content

For each markdown file in:
- `obsidian/topics/`
- `obsidian/concepts/`

Analyze the content for potential conflicts:

#### Check for Direct Contradictions
- Does the content explicitly endorse eliminative materialism?
- Does it claim consciousness is an illusion?
- Does it endorse quantum mysticism or "quantum woo"?
- Does it treat consciousness as epiphenomenal?
- Does it endorse many-worlds interpretation?
- Does it use Occam's Razor to dismiss dualism?

#### Check for Implicit Conflicts
- Does the content assume physicalism without acknowledgment?
- Does it dismiss non-physical explanations without argument?
- Does it treat all philosophical positions as equally valid when tenets take a stance?

### 3. Classify Issues

For each potential conflict, classify severity:

- **ERROR**: Direct contradiction of a tenet (e.g., "consciousness is just neurons firing")
- **WARNING**: Implicit assumption that conflicts (e.g., assumes physicalism without stating it)
- **NOTE**: Tension that might need clarification (e.g., discusses a position without noting tenet conflict)

### 4. Generate Report

Create a report at `obsidian/reviews/tenet-check-YYYY-MM-DD.md`:

```markdown
---
title: Tenet Alignment Check - YYYY-MM-DD
created: YYYY-MM-DD
draft: false
ai_contribution: 100
ai_system: [current model]
---

# Tenet Alignment Check

**Date**: YYYY-MM-DD
**Files checked**: N
**Errors**: N
**Warnings**: N
**Notes**: N

## Summary

[Brief summary of findings]

## Errors

### [filename.md]
- **Tenet violated**: [which tenet]
- **Issue**: [description]
- **Quote**: "[relevant quote from content]"
- **Recommendation**: [how to fix]

## Warnings

[Similar format]

## Notes

[Similar format]

## Files Passing All Checks

- file1.md
- file2.md
```

### 5. Log to Changelog

Prepend entry to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - check-tenets
- **Status**: Success/Warnings
- **Files checked**: [count]
- **Errors**: [count]
- **Warnings**: [count]
- **Output**: [[filepath without .md extension]]
```

## Important

- This skill is READ-ONLY for content files
- Only creates report files and updates changelog
- Does NOT modify content - only reports for human review
- Human must decide how to address conflicts
- Some content may intentionally present opposing views for discussion - flag but don't treat as errors if clearly marked as such
