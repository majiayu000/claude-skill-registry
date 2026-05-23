---
name: create-runbook
description: Extract a reusable runbook from a successful investigation or troubleshooting session. Use when Claude has just completed a multi-step diagnosis that could help future investigations.
user-invocable: true
---

# Create Runbook

Extract procedural knowledge from this conversation into a reusable runbook.

## When to use this

After completing a multi-step investigation that:
- Spanned multiple datasources (Xatu, Prometheus, Loki, Dora)
- Followed a diagnostic pattern others could reuse
- Discovered insights that would help future investigations

## Runbook format

Create a markdown file with YAML frontmatter in the `runbooks/` directory:

```markdown
---
name: [Imperative title, e.g., "Investigate Finality Delay"]
description: [1-2 sentence summary for semantic search matching]
tags: [keywords for search, 3-6 tags]
prerequisites: [datasources needed, e.g., xatu, prometheus, dora]
---

[Opening paragraph explaining WHEN this runbook applies and WHAT problem it solves.
Use MUST/SHOULD/MAY keywords inline to indicate requirement levels.]

## Approach

1. **[Step title]** - [Description with MUST/SHOULD/MAY constraints inline]

   ```python
   [Optional: Example code if helpful, but prefer referencing search_examples]
   ```

2. **[Next step]** - Use `search_examples("relevant query")` for the query pattern.
   You SHOULD [constraint]. You MAY [optional action].

## Key Thresholds

[If applicable, include a table of healthy/warning/critical thresholds]

## Notes

- [Key insight or gotcha learned during the investigation]
- [Threshold values or timing considerations]
```

## Constraint keywords (RFC 2119)

Use these keywords inline in the prose to indicate requirement levels:

- **MUST** - Non-negotiable requirement. The investigation will fail or produce wrong results without this.
- **SHOULD** - Strongly recommended. Skip only with good reason and document why.
- **MAY** - Optional. Use judgment based on context and time available.

## Guidelines for extraction

1. **Focus on the diagnostic pattern**, not the specific incident details
2. **Reference examples** instead of embedding queries - use `search_examples("...")`
3. **Include key thresholds** discovered during the investigation
4. **Document gotchas** - what would have tripped you up without prior knowledge?
5. **Keep it actionable** - every step should tell the user what to do, not just what to think about

## Naming conventions

- File name: `kebab-case.md` (e.g., `finality_delay.md`, `block-propagation.md`)
- Runbook name: Imperative mood (e.g., "Investigate X", "Diagnose Y", "Debug Z")
- Tags: lowercase, single words or short phrases

## Output

Save the runbook to: `runbooks/[kebab-case-name].md`

After creating the runbook, verify it loads correctly:
1. The server should log "Runbook registry loaded" with the updated count
2. The runbook should be searchable via `search_runbooks`

$ARGUMENTS
