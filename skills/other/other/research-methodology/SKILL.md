---
name: research-methodology
description: Structured research using sophisticated query design, source vetting, and synthesis techniques. Use when conducting competitive analysis, market scans, historical investigations, or trend research.
tags: [research, analysis, fact-checking, synthesis]
triggers:
  - research topic
  - competitive analysis
  - market scan
  - trend analysis
  - fact verification
  - investigate
---

# Research Methodology

Structured approach to finding, vetting, and synthesizing information from diverse
sources. Turns research questions into trustworthy, actionable findings through
systematic query design, source evaluation, and cross-referencing.

## When to Use This Skill

- Conducting competitive analysis or market scans
- Investigating historical events, trends, or technical evolution
- Fact-checking claims across multiple sources
- Synthesizing research into structured deliverables (reports, tables, timelines)
- Any research task that requires more than a single search query

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/search-strategies.md` | Query design, source vetting, fact verification, synthesis techniques | Starting any research task |

---

## Workflow

```
Phase 1: Scope       → Define research objective, key questions, constraints
Phase 2: Explore     → Design queries, search broadly, capture sources
Phase 3: Verify      → Vet sources, cross-reference claims, assess credibility
Phase 4: Synthesize  → Organize findings into structured deliverables
```

---

## Phase 1: Scope the Research

Before searching, clarify the research objective:

1. **State the question** -- what exactly are we trying to learn?
2. **Define success criteria** -- what does a complete answer look like?
3. **Set constraints** -- time period, geography, domains, source types
4. **List hypotheses** -- what do we expect to find? (helps detect bias)
5. **Identify key terms** -- domain vocabulary, synonyms, related concepts

### Scoping Template

```markdown
**Research Question**: [precise question]
**Success Criteria**: [what constitutes a complete answer]
**Constraints**: [time period, scope, source types]
**Key Terms**: [domain vocabulary and synonyms]
**Initial Hypotheses**: [what we expect, to check against later]
```

---

## Phase 2: Explore

Design multiple query variations and search broadly before narrowing:

1. **Create 3-5 query variations** per research question
2. **Search broadly first** -- cast a wide net with general terms
3. **Refine iteratively** -- narrow based on initial results
4. **Track what you searched** -- record every query for reproducibility

### Query Design Principles

- Use exact-match phrases in quotes for precision
- Exclude noise with negative keywords
- Target specific timeframes for recency or historical depth
- Vary terminology across queries to avoid vocabulary bias
- Use domain-specific operators when available (site:, filetype:, etc.)

### Source Capture

For each promising source, record:
- URL and access date
- Key claims with direct quotes
- Author/publisher and their domain authority
- Any noted biases or limitations

---

## Phase 3: Verify

Vet sources and cross-reference claims before trusting them:

1. **Assess source authority** -- who wrote it, what are their credentials?
2. **Check recency** -- is the information current enough for the question?
3. **Detect bias** -- does the source have a commercial, political, or ideological interest?
4. **Triangulate** -- require 2+ independent sources for any key claim
5. **Seek primary sources** -- follow citation chains to the original data

### Confidence Rating

| Level | Criteria |
|-------|----------|
| **Confirmed** | 3+ independent, authoritative sources agree |
| **Likely** | 2 sources agree, no contradictions found |
| **Uncertain** | Single source or sources disagree |
| **Contested** | Credible sources directly contradict each other |

---

## Phase 4: Synthesize

Organize findings into a structured deliverable:

### Standard Research Report Structure

```markdown
## Research Summary
[1-2 paragraph overview of findings]

## Key Findings
- [Finding 1] — [confidence level]
- [Finding 2] — [confidence level]

## Detailed Analysis
[Organized by theme or question]

## Source Credibility Assessment
| Source | Authority | Recency | Bias Risk | Rating |
|--------|-----------|---------|-----------|--------|

## Gaps and Limitations
[What we couldn't determine and why]

## Recommendations
[Next steps or actions based on findings]
```

---

## Anti-Patterns

- Do not rely on a single source for any key claim
- Do not present uncertain findings as confirmed facts
- Do not skip source vetting for convenience
- Do not omit contradictory evidence -- always surface disagreements
- Do not let initial hypotheses bias which findings you report
