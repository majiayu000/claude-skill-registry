---
name: academic-research-writing
description: Use when writing CS research papers (conference, journal, thesis), reviewing scientific manuscripts, improving academic writing clarity, or preparing IEEE/ACM submissions. Invoke when user mentions paper, manuscript, research writing, journal submission, or needs help with academic structure, formatting, or revision.
---

# Academic Research Writing

## Overview

Comprehensive toolkit for writing and reviewing computer science research papers. Combines paper writing workflows, manuscript review processes, clarity principles, and formatting standards.

## When to Use

**Writing Mode:**
- Writing new research papers (conference, journal, thesis)
- Creating survey/review papers
- Structuring technical contributions

**Review Mode:**
- Reviewing/editing existing manuscripts
- Pre-submission polish
- Addressing reviewer comments
- Collaborative editing

**Both Modes:**
- Improving academic writing clarity
- Preparing IEEE/ACM submissions
- Learning academic writing conventions

## Mode Selection

```
User request received
        |
        v
Is this about WRITING new content or REVIEWING existing content?
        |
        +---> Writing new paper -----> Use Writing Workflow
        |                              (references/writing-workflow.md)
        |
        +---> Reviewing/editing -----> Use Review Workflow
        |     existing manuscript      (references/review-workflow.md)
        |
        +---> Both/unclear ----------> Start with Review Workflow
                                       to assess, then write
```

## Quick Reference

### Writing a Paper

1. **Clarify scope** - topic, venue, format (IEEE/ACM)
2. **Create outline** - section-by-section plan
3. **Draft core sections** - methodology first, then results
4. **Write supporting sections** - intro, related work, discussion
5. **Add citations** - 15-20+ references
6. **Review & polish** - use checklists

See: `references/writing-workflow.md`

### Reviewing a Manuscript

1. **Extract core message** - one sentence summary
2. **Structural pass** - overall organization
3. **Section reviews** - intro, results, discussion
4. **Scientific clarity** - claims, evidence, hedging
5. **Language polish** - terminology, voice
6. **Formatting check** - journal compliance

See: `references/review-workflow.md`

## Core Resources

| Resource | Purpose |
|----------|---------|
| `references/writing-workflow.md` | 6-step paper writing process |
| `references/review-workflow.md` | 8-step manuscript review process |
| `references/narrative-framework.md` | Section-by-section narrative structure (Problem->Solution->Evidence) |
| `references/clarity-principles.md` | Gopen & Swan sentence-level clarity |
| `references/academic-phrasebank.md` | Common academic phrases by section |
| `references/cs-conventions.md` | CS-specific writing conventions |
| `references/section-checklists.md` | Combined quality checklists |
| `references/ieee-formatting.md` | IEEE formatting specifications |
| `references/acm-formatting.md` | ACM formatting specifications |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/paper-structure.md` | Introduction arc, results paragraph, discussion templates |
| `templates/methodology.md` | Core message extraction, structural assessment, language guidelines |

## Evaluation

Use `evaluators/rubric.json` for quality scoring:
- Structure and Organization (weight: 1.0)
- Scientific Rigor (weight: 1.2)
- Language and Clarity (weight: 1.0)
- Section-Specific Quality (weight: 1.0)
- Formatting Compliance (weight: 0.8)
- Citation Quality (weight: 0.8)

**Minimum threshold:** Average score >= 3.5

## Seven Core Principles

1. **Clarity over cleverness** - Scientific clarity beats stylistic elegance
2. **Narrative shapes comprehension** - Structure determines understanding
3. **Audience dictates tone** - Expert vs. general requires different framing
4. **Format signals credibility** - Professional formatting reflects rigor
5. **Claims require evidence** - Strong assertions need strong data
6. **Each section has a job** - Intro sells, Results show, Discussion interprets
7. **Constraints shape structure** - Word limits determine emphasis

## Guardrails

**Critical requirements:**
1. Preserve author voice - edit for clarity, don't rewrite
2. Claims match data - flag overclaiming immediately
3. Quantitative rigor - statistics for all comparisons
4. Logical flow - clear transitions between sections
5. Appropriate hedging - match evidence strength
6. Consistent terminology - same term for same concept

**Common pitfalls to avoid:**
- Overclaiming ("proves" when data only suggests)
- Missing context (results without interpretation)
- Buried lede (important findings hidden)
- Inconsistent terms (alternating synonyms)
- Vague descriptions ("some increase" vs "3-fold increase")

## External Guides

| Guide | Purpose |
|-------|---------|
| `external-guides/how-to-write-a-paper.md` | Practical conference paper structuring guidelines (Introduction paragraphs, experiments, tables/figures) |

## PDF Templates

- `assets/full_paper_template.pdf` - IEEE template
- `assets/interim-layout.pdf` - ACM template
