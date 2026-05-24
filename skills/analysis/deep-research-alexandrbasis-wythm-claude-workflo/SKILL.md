---
name: deep-research
description: "In-depth research on technical topics using web search, documentation, and codebase analysis. Use when asked to 'research', 'investigate', 'find out about', or explore unfamiliar technologies."
context: fork
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Grep
  - Glob
  - Task
---

# Deep Research

## Overview

Conduct comprehensive research on technical topics, synthesizing information from multiple sources. Since this runs in a forked context, explore extensively - only the final findings return to the main conversation.

## Research Process

### 1. Clarify Scope
Before diving in, understand:
- What specifically needs to be researched?
- What decisions will this inform?
- Any constraints (technology, timeline, team expertise)?

### 2. Source Prioritization

| Priority | Source | Use For |
|----------|--------|---------|
| 1 | Official docs | Authoritative information |
| 2 | GitHub repos | Real implementations, issues |
| 3 | Technical blogs | Best practices, gotchas |
| 4 | Stack Overflow | Common problems, solutions |
| 5 | Codebase analysis | How it relates to our code |

### 3. Research Strategy

**For Technology Evaluation:**
```
1. Official documentation overview
2. GitHub - stars, activity, issues
3. Comparison articles (vs alternatives)
4. Real-world case studies
5. Our codebase - integration points
```

**For Problem Solving:**
```
1. Error message / symptom search
2. GitHub issues in relevant repos
3. Stack Overflow discussions
4. Official troubleshooting guides
5. Our codebase - similar patterns
```

**For Best Practices:**
```
1. Official style guides
2. Community conventions
3. Popular open-source examples
4. Our existing patterns
5. Team preferences (from CLAUDE.md)
```

### 4. Cross-Verification
- Never trust single source
- Verify with official docs
- Check publication date (prefer recent)
- Look for consensus across sources

## Output Format

Return structured findings:

```markdown
# Research Report: [Topic]

**Research Question**: [what was investigated]
**Date**: [ISO date]
**Sources Consulted**: [count]

## Executive Summary
[3-5 sentences answering the research question]

## Key Findings

### Finding 1: [title]
**Confidence**: HIGH/MEDIUM/LOW
**Sources**: [list]

[detailed finding]

### Finding 2: [title]
...

## Recommendations
Based on research:
1. [recommendation with rationale]
2. [recommendation with rationale]

## Sources
- [Source 1](url) - [what it provided]
- [Source 2](url) - [what it provided]

## Open Questions
- [anything that couldn't be answered]
```

## Research Quality Checklist

Before returning findings:
- [ ] Multiple sources consulted
- [ ] Official documentation checked
- [ ] Information is current (check dates)
- [ ] Relevance to Wythm project verified
- [ ] Recommendations are actionable
- [ ] Sources are cited

## Wythm Context

When researching, consider our stack:
- **Backend**: NestJS, TypeScript, Prisma, PostgreSQL
- **Architecture**: DDD + Clean Architecture
- **Future Mobile**: React Native + Expo
- **AI Integration**: OpenAI, Anthropic APIs
