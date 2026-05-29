---
name: writing-style
user-invocable: false
description: |
  Structural pattern analysis for writing-mode review. Performs paragraph-level decomposition and pattern aggregation. Invoked by the team lead during editorial review.
keywords: trope detection, structural analysis, pattern density, writing quality diagnostic, paragraph fingerprinting
---

# Writing Style — Structural Pattern Analysis

## Purpose

A sentence or paragraph can look fine in isolation. When the same structural shape repeats across 1,000-3,000 words, the aggregate creates a mechanical feeling — even though no single instance is wrong. Linear readers miss this because they process sequentially and each paragraph clears the "is this well-written?" bar individually.

This analysis solves the forest-vs-trees problem. It decomposes every paragraph's structure, then aggregates the fingerprints to surface repetition invisible to linear reading.

## How to Use

Invoke this skill using the **Skill** tool: `swarm:writing-style`. Pass the piece's text or file path as the `args` parameter. The skill returns a structured report. The lead relays the report to the editor for interpretation. Invoke during the review phase (required) or optionally during drafting.

**The report is advisory, never gating.** The editor applies editorial judgment to the data. The Economist escape clause applies: if a flagged pattern serves the piece, keep it and note why.

## Analysis Process

**Exclude from analysis:** Table cells, comparison tables, and structured list items with deliberately parallel construction (numbered checklists, step-by-step procedures). These are exempt from construction density calculation but still included in named pattern counts. Report construction density both with and without these items so the editor has both numbers.

**Introductory and concluding paragraphs adjacent to lists are NOT exempt** — only the parallel list items themselves.

### Pass 1: Structural Decomposition

For each body paragraph, classify:

**1. Opening move** — how the paragraph begins:
- `claim`: declarative assertion
- `scenario`: narrative with actors or concrete situation
- `question`: interrogative opening
- `data`: leads with a statistic or cited fact
- `contrast`: opens with negation or opposition
- `definition`: introduces or defines a term
- `transition`: bridges from previous section
- `imperative`: directive opening

**2. Dominant sentence shape:**
- `declarative`: simple subject-verb-object statements
- `contrast-pivot`: sentences built on "not X — it is Y" or "X, but Y"
- `question-answer`: rhetorical question followed by its answer
- `conditional`: "when X, then Y" or "if X, then Y"
- `enumeration`: listing or cataloguing items
- `narrative`: sequential events with actors
- `compound-aside`: sentences with em-dash parenthetical asides (banned — flag for rewrite)

**3. Named trope patterns present (if any):**
- `negative-parallelism`: "X is not [assumption]. It is [reframe]."
- `countdown`: "Not X. Not Y. [Resolution]."
- `self-posed-qa`: Question posed and immediately answered. Exclude H2/H3 section headings that are questions — question-format headings are a structural choice, not a rhetorical trope. Only count questions posed within body paragraph text.
- `same-phrase-recycled`: A multi-word formulation appearing verbatim elsewhere in the piece
- `punchy-fragment`: One-sentence standalone paragraph used for emphasis
- `dead-metaphor`: A metaphor that has already appeared earlier in the piece
- `anaphora`: Same opening word as the previous paragraph
- `tricolon`: Three-part list or phrase

Record each paragraph's structural fingerprint in compact notation.

### Pass 2: Pattern Aggregation

Review ALL fingerprints together and analyze:

**A. Named pattern frequency**

Count each named trope pattern across the full piece. For each, report:
- Total count
- Distribution by section (which sections contain instances)
- Whether instances cluster in one section or distribute evenly
- Cite each instance with its section and paragraph number

**B. Opening move distribution**

- Count how many paragraphs use each opening move type
- Calculate the percentage for each type
- Flag any opening move that accounts for more than 30% of all paragraphs
- Flag 3+ consecutive paragraphs with the same opening move

**C. Section structural fingerprint**

Classify each top-level section's overall pattern:
- `CLAIM-EVIDENCE`: Opens with a declarative claim, supports with data/examples
- `SCENARIO-ANALYSIS`: Opens with a narrative scenario, analyzes implications
- `QUESTION-ANSWER`: Opens with a question, provides the answer
- `PROBLEM-SOLUTION`: Defines a problem, proposes a fix
- `DEFINITION-EXPANSION`: Defines a term, expands on implications
- `COMPARISON`: Contrasts two approaches or states
- `LIST-FRAMEWORK`: Enumerates multiple sub-points under a thesis

Flag when 3+ sections share the same fingerprint.

**D. Sentence length variance**

For each section, assess the approximate spread of sentence lengths. Flag sections where most sentences fall in the same 15-25 word band (low variance).

**E. Construction density**

Count ALL identified trope pattern instances per 500 words of body text. Flag when density exceeds 3 per 500 words.

**F. Paragraph opener concentration**

Map the first word of every body paragraph. Flag any word that opens more than 20% of paragraphs.

## Output Format

```
## Structural Pattern Analysis: <title or slug>

### Named Patterns

| Pattern | Count | Limit | Status | Distribution |
|---------|-------|-------|--------|--------------|
| Negative parallelism | N | 1 | GREEN/YELLOW/RED | Sections: ... |
| Countdown | N | 1 | GREEN/YELLOW/RED | Sections: ... |
| Self-posed Q&A | N | 1 | GREEN/YELLOW/RED | Sections: ... |
| Same-phrase recycled | N | 1 | GREEN/YELLOW/RED | Phrases: ... |
| Punchy fragment | N | 2 | GREEN/YELLOW/RED | Sections: ... |
| Dead metaphor | N | 2 | GREEN/YELLOW/RED | Metaphor: ... |
| Anaphora (consecutive) | N | 3 | GREEN/YELLOW/RED | Sections: ... |
| Tricolon | N | 1 | GREEN/YELLOW/RED | Sections: ... |

**Instances (for any YELLOW or RED):**
- [Pattern]: §[section] ¶[paragraph]: "[quoted text]"

### Structural Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Opening move concentration | [top opener]: N of M paragraphs (X%) | GREEN/YELLOW/RED |
| Section fingerprint variety | N distinct of M sections | GREEN/YELLOW/RED |
| Sentence length variance | [assessment per section] | GREEN/YELLOW/RED |
| Construction density | X per 500 words (with lists) / Y per 500 words (excl. lists) | GREEN/YELLOW/RED |
| Paragraph opener word concentration | "[word]": X% of paragraphs | GREEN/YELLOW/RED |

**Section fingerprints:**
- §1 [heading]: [FINGERPRINT-TYPE]
- §2 [heading]: [FINGERPRINT-TYPE]
[Flag if 3+ sections share the same fingerprint]

**Opening move distribution:**
- claim: N (X%)
- scenario: N (X%)
- contrast: N (X%)
...

### Priority Issues

[Top 2-3 issues by severity. For each: what the pattern is, where it concentrates, and a specific suggestion for varying the structure.]

### Summary

- RED: N issues
- YELLOW: N issues
- GREEN: N issues
```

## Thresholds

| Pattern | GREEN | YELLOW | RED |
|---------|-------|--------|-----|
| Negative parallelism | 0-1 | 2 | 3+ |
| Countdown | 0-1 | 2 | 3+ |
| Self-posed Q&A | 0-1 | 2 | 3+ |
| Same-phrase recycled | 0-1 | 2 | 3+ |
| Punchy fragment | 0-2 | 3 | 4+ |
| Dead metaphor | 0-2 | 3 | 4+ |
| Anaphora (consecutive same opener) | 0-3 | 4 | 5+ |
| Tricolon | 0-1 | 2 | 3+ |
| Construction density (per 500 words, excl. parallel lists) | 0-3 | 4-5 | 6+ |
| Sentence length variance (per section) | varied | narrow band | monotone |
| Section fingerprint repeats | 0-2 | 3 | 4+ |
| Opener move concentration (max %) | <30% | 30-40% | >40% |
| Paragraph opener word concentration (max %) | <20% | 20-30% | >30% |

Thresholds are calibrated to short-to-medium pieces (350-800 words). For longer pieces, apply proportionally more tolerance on named pattern counts.
