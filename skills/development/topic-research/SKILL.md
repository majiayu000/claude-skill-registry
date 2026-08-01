---
name: topic-research
description: Research and synthesize information about {{TOPIC}}. Use when {{TRIGGER_CONTEXTS}}.
  Produces {{OUTPUT_FORMAT}} with citations.
---

---
name: {{TOPIC}}-research
description: Research and synthesize information about {{TOPIC}}. Use when {{TRIGGER_CONTEXTS}}. Produces {{OUTPUT_FORMAT}} with citations.
---

# {{TOPIC}} Research

## Source Priority

Check sources in this order:

1. **{{PRIMARY_SOURCE}}** — Authoritative for {{reason}}
2. **{{SECONDARY_SOURCE}}** — Good for {{reason}}
3. **General web search** — For background and recent developments

## Research Workflow

### Step 1: Scope Definition

Before searching, clarify:
- What specific questions need answers?
- What time range is relevant?
- What level of detail is needed?

### Step 2: Gather Information

For each source:
1. Search with specific queries
2. Extract relevant facts
3. Note the source URL and date

### Step 3: Synthesize

Combine findings into {{OUTPUT_FORMAT}}:
- Lead with key findings
- Support claims with citations
- Note conflicting information
- Highlight gaps

## Output Format

{{DESCRIBE_FORMAT}}

### Summary Structure

```markdown
## Key Findings
- [Finding 1](source_url)
- [Finding 2](source_url)

## Details

### Topic Area 1
[Detailed findings with inline citations]

### Topic Area 2
[Detailed findings with inline citations]

## Gaps & Limitations
- [What couldn't be determined]
- [Areas needing more research]

## Sources
- [Source 1 Title](url) — accessed YYYY-MM-DD
- [Source 2 Title](url) — accessed YYYY-MM-DD
```

## Citation Style

Use inline citations: `[claim](source_url)`

For multiple sources supporting one claim: `[claim](source1)` `[2](source2)`

## Quality Checks

Before delivering:
- [ ] All claims have citations
- [ ] Sources are authoritative and recent
- [ ] Conflicting information is noted
- [ ] Gaps are acknowledged
- [ ] Format matches requested output

## Tips

- Prefer primary sources over summaries
- Note publication dates for time-sensitive info
- Cross-reference claims across multiple sources
- Be explicit about uncertainty
