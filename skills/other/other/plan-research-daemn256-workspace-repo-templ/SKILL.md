---
name: plan-research
description: Research a problem space with evidence gathering and source validation
---

# Plan Research

Uses **Planner**. Investigate a problem space by gathering evidence from the codebase, documentation, and external sources. Produce a structured research summary with cited sources.

**Prerequisites:** Clear research question or problem statement

---

## Phase 1: Scope the Investigation

### Define Research Boundaries

1. State the research question clearly
2. Identify what you need to learn and why
3. Define what is in-scope and out-of-scope
4. List known starting points (files, docs, APIs, prior ADRs)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 1 — Scope

## Research Question

<Clear statement of what needs to be investigated>

## Scope

**In:** <what to investigate>
**Out:** <what to exclude>

## Starting Points

- <file, doc, or source 1>
- <file, doc, or source 2>

## Next Step

Begin evidence gathering.

**Approval Required:** No
```

---

## Phase 2: Gather Evidence

### Internal Sources

1. Search the codebase for relevant patterns, implementations, and conventions
2. Read existing ADRs, architecture docs, and design notes
3. Review git history for context on past decisions
4. Quantify where possible (line counts, file counts, dependency counts)

### External Sources

1. Use `web/fetch` to read official documentation, changelogs, or specifications
2. Use `web/githubRepo` to inspect upstream repositories for README, examples, or release notes
3. Do NOT rely solely on training knowledge for version-specific behavior, API signatures, or configuration options — verify against the source
4. Cite every external source with a URL or repository reference

### Evidence Standards

- Every claim must link to a specific file, line, URL, or commit
- Distinguish verified facts from inferences
- Note contradictions between sources
- Record what you searched for and didn't find (negative evidence)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Gather Evidence

## Findings

### <Topic 1>

<Finding with source citation>

**Source:** <file path, URL, or commit>

### <Topic 2>

<Finding with source citation>

**Source:** <file path, URL, or commit>

## Negative Evidence

- Searched for <X>, not found in <scope>

## Next Step

Synthesize findings into a research summary.

**Approval Required:** No
```

---

## Phase 3: Synthesize

### Produce Research Summary

1. Combine findings into a coherent picture
2. Identify patterns, gaps, and contradictions
3. State implications for the original research question
4. List open questions that remain unanswered

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 3 — Synthesize

## Research Summary

<Coherent synthesis of findings>

## Key Insights

1. <insight 1>
2. <insight 2>
3. <insight 3>

## Open Questions

- <question that remains unanswered>

## Sources

| Source | Type                | Key Finding       |
| ------ | ------------------- | ----------------- |
| <ref>  | <internal/external> | <what it told us> |

## Next Step

Research complete. Findings available for design, planning, or decision-making.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms the research summary is accurate and sufficient.

---

## Error Handling

| Error                       | Recovery                                                 |
| --------------------------- | -------------------------------------------------------- |
| Research question too broad | Narrow scope, break into sub-questions                   |
| External source unavailable | Note the gap, try alternative sources                    |
| Contradictory evidence      | Document both sides, flag for human judgment             |
| Insufficient evidence       | State what's missing, recommend additional investigation |
