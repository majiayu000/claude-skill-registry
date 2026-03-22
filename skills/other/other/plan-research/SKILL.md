---
name: plan-research
description: Research a problem space with evidence gathering and source validation.
---

# Plan Research

The Planner drives this workflow. Investigate a problem space by gathering evidence from the codebase, documentation, and external sources. Produce a structured research summary with cited sources.

---

## Phase 1: Scope the Investigation

Define the boundaries before researching.

### Steps

1. State the research question clearly
2. Identify what you need to learn and why
3. Define what is in-scope and out-of-scope
4. List known starting points (files, docs, APIs, prior ADRs)

### Output

Produce a scoped research brief covering: research question, in/out scope, starting points.

**Approval Required:** No

---

## Phase 2: Gather Evidence

Collect evidence from internal and external sources.

### Internal Sources

1. Search the codebase for relevant patterns, implementations, and conventions
2. Read existing ADRs, architecture docs, and design notes
3. Review git history for context on past decisions
4. Quantify where possible (line counts, file counts, dependency counts)

### External Sources

1. Use `WebFetch` to read official documentation, changelogs, or specifications
2. Use `mcp__github__search_repositories` to explore prior art in open source
3. Do NOT rely solely on training knowledge for version-specific behavior, API signatures, or configuration options — verify against the source
4. Cite every external source with a URL or repository reference

### Evidence Standards

- Every claim must link to a specific file, line, URL, or commit
- Distinguish verified facts from inferences
- Note contradictions between sources
- Record what you searched for and didn't find (negative evidence)

### Output

Produce a findings report covering: topic-by-topic findings with sources, negative evidence.

**Approval Required:** No

---

## Phase 3: Synthesize

Combine findings into a structured research summary.

### Steps

1. Combine findings into a coherent picture
2. Identify patterns, gaps, and contradictions
3. State implications for the original research question
4. List open questions that remain unanswered

### Output

Produce a research summary covering: synthesis narrative, key insights (numbered), open questions, sources table (source | type | key finding).

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms the research summary is accurate and sufficient.

**Approval Required:** Yes

---

## Error Handling

| Error                       | Recovery                                                 |
| --------------------------- | -------------------------------------------------------- |
| Research question too broad | Narrow scope, break into sub-questions                   |
| External source unavailable | Note the gap, try alternative sources                    |
| Contradictory evidence      | Document both sides, flag for human judgment             |
| Insufficient evidence       | State what's missing, recommend additional investigation |
