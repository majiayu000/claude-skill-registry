---
name: research
description: "Deep research on a topic, creating persistent documentation for future reference. Use for technology decisions, competitive analysis, or complex topics."
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# /research

Deep research creating persistent documentation for future reference. Uses Ultrathink for comprehensive analysis.

## Usage

```bash
/research "authentication patterns for multi-tenant SaaS"
/research "real-time collaboration architectures"
/research "Jira vs Linear competitive analysis"
/research "WebSocket vs SSE trade-offs"
```

## Output Locations

```
ideas/
├── [project]/notes/research/     # Project-specific
├── shared/docs/research/         # Cross-project
└── resources/research/           # General reference
```

**Location rules:**
- Project-specific: `ideas/{project}/notes/research/`
- Cross-project: `shared/docs/research/`
- General reference: `resources/research/`

## Process

### 1. Check Existing Research
```bash
grep -r "authentication" ideas/*/notes/research/
grep -r "authentication" shared/docs/research/
```

If found, ask: "Research exists. Update, view, or create new?"

### 2. Deep Research Phase

Invoke `research-specialist` agent:

**Research scope:**
- Official documentation (via Context7)
- Technical blogs and tutorials
- Stack Overflow (high-vote answers)
- GitHub discussions and issues
- Community forums
- Existing solutions/products

**Volume**: Read 20-30+ sources, distill to 3-5 pages

### 3. Create Research Document

**Naming**: lowercase kebab-case (e.g., `auth-patterns-saas.md`)

**Structure:**
```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: NUMBER
related:
  - path/to/related/file.md
tags: ["primary-tag", "secondary-tag"]
---

# Research: [Topic]

## Executive Summary
[2-3 paragraphs of key findings]

## Detailed Findings

### [Subtopic 1]
[Analysis]

### [Subtopic 2]
[Analysis]

## Recommendations
[What to do based on research]

## Must-Read Resources
1. **[Title]** - [url]
   - Why: [Reason]
   - Key point: [Takeaway]

## Additional Resources
- [Title] - [url]

## Gotchas & Warnings
- [Warning 1]

## Decision Matrix (if comparing)

| Criteria | Option A | Option B |
|----------|----------|----------|
| Ease of use | ⭐⭐⭐ | ⭐⭐ |
| Scalability | ⭐⭐⭐⭐ | ⭐⭐⭐ |
```

### 4. Link to Related Work

If research relates to a spec or issue:
- Add reference in research doc
- Update spec/issue to reference research

## When to Use

**Good candidates:**
- Technology decisions affecting architecture
- Competitive analysis for product positioning
- Complex topics with many options
- Best practices you'll reference multiple times
- Market research for product ideas

**Not needed for:**
- Quick one-off questions (just ask)
- Simple API lookups (use Context7)
- Project-specific debugging

## Updating Research

If research exists but is outdated:
```
Options:
1. Update existing (add new findings)
2. Replace entirely (fresh research)
3. View existing
4. Cancel
```

## Integration

Research documents are discovered by:
- `/plan` - Checks for relevant research before planning
- `/spec` - References research in technical notes
- Future sessions - Research persists for reference

```
/research "topic" → ideas/{project}/notes/research/topic.md
                           ↓
              Future work automatically references this
```
