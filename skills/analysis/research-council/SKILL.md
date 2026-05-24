---
name: research-council
description: |
  Lightweight parallel research orchestration without full council debate.
  Spawns oracle agents with different queries, collects findings, synthesizes report.
model_invoked: true
triggers:
  - "research council"
  - "parallel research"
  - "multi-source research"
  - "investigate from multiple angles"
  - "comprehensive research"
---

# Research Council Skill

## Purpose

Orchestrate parallel research across multiple sources without the full Architecture Council process. Used when you need comprehensive research from different angles but don't need architectural debate and synthesis.

## When to Use

| Use Research Council | Use Architecture Council |
|---------------------|-------------------------|
| Pure information gathering | Architectural decisions |
| Multiple search queries | Design tradeoff analysis |
| External standards research | Specification writing |
| Quick multi-angle investigation | ADR creation |
| Technology evaluation | System design |

## Council Composition

| Agent | Query Focus | MCP |
|-------|-------------|-----|
| **Internal Oracle** | Codebase patterns | Grep, Glob, Read |
| **Docs Oracle** | Effect documentation | deepwiki |
| **Standards Oracle** | Industry standards | exa, playwright |
| **Community Oracle** | Best practices, examples | exa |

## Protocol

### Phase 1: Query Definition

Define parallel research queries:

```
1. Internal: "How does our codebase handle X?"
2. Docs: "What does Effect documentation say about X?"
3. Standards: "What industry standards apply to X?"
4. Community: "What are common patterns for X?"
```

### Phase 2: Parallel Research

Spawn oracle agents in parallel:
- Each oracle queries its domain
- Writes findings to shared report
- Signals completion

### Phase 3: Synthesis

Combine findings into research report:
- Cross-reference sources
- Identify consensus
- Flag contradictions
- Summarize actionable insights

## Report Format

```markdown
# Research Report: <Topic>

**Generated**: YYYY-MM-DD
**Author**: Research Council

---

## Executive Summary

[Key findings in 3-5 bullet points]

---

## Internal Analysis

**Query**: "How does our codebase handle X?"

### Findings

[Codebase patterns found]

### Codebase References

| File | Relevance |
|------|-----------|
| `src/lib/...` | Description |

---

## Documentation Research

**Query**: "What does Effect documentation say about X?"
**Source**: deepwiki: Effect-TS/effect

### Findings

[Documentation patterns]

### Verification Status

- [x] API verified current
- [ ] Breaking changes checked

---

## Industry Standards

**Query**: "What industry standards apply to X?"
**Source**: exa search, ISA/FDA/ISO references

### Findings

[Standards references]

### Applicable Standards

| Standard | Relevance | Link |
|----------|-----------|------|
| ISA-95 | ... | ... |

---

## Community Patterns

**Query**: "What are common patterns for X?"
**Source**: exa search, GitHub, blog posts

### Findings

[Community patterns]

### References

1. [Reference 1]
2. [Reference 2]

---

## Cross-Reference Analysis

### Consensus

[What all sources agree on]

### Contradictions

[Where sources disagree]

### Gaps

[What no source addressed]

---

## Recommendations

1. [Actionable recommendation]
2. [Actionable recommendation]

---

## Sources

[Full citation list]
```

## Example Invocation

### User Request
> "Research how event sourcing is used in IIoT manufacturing systems"

### Claude Response

```
I'll convene a Research Council to investigate this from multiple angles.

**Research Queries**:
1. Internal: "Event patterns in our IIoT codebase"
2. Docs: "Effect EventLog patterns"
3. Standards: "ISA-95 event sourcing manufacturing"
4. Community: "IIoT event sourcing best practices"

[Oracles run in parallel]

**Report generated**: thoughts/shared/reports/2026-01-26-es-iiot-research.md
```

## MCP Tool Usage

### deepwiki (Documentation)

```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "What is the recommended pattern for EventLog in production use?"
```

### exa (Web Search)

```
mcp__exa__search
  query: "ISA-95 event sourcing manufacturing operations management 2024"
```

```
mcp__exa__search
  query: "event sourcing IIoT best practices industrial"
```

### playwright (Standards Scraping)

For regulatory documents that need scraping:

```
mcp__playwright__navigate
  url: "https://www.isa.org/standards/..."
```

## Query Templates

### Technology Evaluation

```
Internal: "Do we already use {technology}?"
Docs: "What is {technology} designed for?"
Standards: "{technology} in {domain} standards"
Community: "{technology} production experience reviews"
```

### Pattern Investigation

```
Internal: "How do we implement {pattern}?"
Docs: "Recommended implementation of {pattern}"
Standards: "Industry standards for {pattern}"
Community: "{pattern} best practices {domain}"
```

### Problem Research

```
Internal: "Do we have this {problem}?"
Docs: "Known issues with {related-feature}"
Standards: "Industry solutions for {problem}"
Community: "{problem} solutions {technology}"
```

## Lightweight vs Full Council

### Research Council (This Skill)

```
Queries → Oracles → Report
```
- ~10-15 minutes
- Information gathering
- Report output

### Architecture Council (Full)

```
Documents → Agents → Journal → Synthesis → Spec → ADR → WBS
```
- ~30-60 minutes
- Decision making
- Multiple artifacts

## Output Location

Reports go to:
```
thoughts/shared/reports/YYYY-MM-DD-<topic>.md
```

## Related Skills

| Skill | Integration |
|-------|-------------|
| `/architecture-council` | Upgrade to full council when decisions needed |
| `/grounded-research` | Single-source research |
| `/effect-research` | Effect-specific research |

## Anti-Patterns

### DON'T: Use for decisions
```
❌ "Should we use X or Y?" → Use Architecture Council
✅ "What is X and Y?" → Use Research Council
```

### DON'T: Skip internal analysis
```
❌ Only search externally
✅ Always check codebase first
```

### DON'T: Ignore contradictions
```
❌ "Source A says X"
✅ "Source A says X, but Source B says Y. Resolution needed."
```
