---
name: ic-curate
description: Curate external IC10 resources without generating code. Use when user wants to find existing scripts, tutorials, or community solutions for Stationeers automation.
---

# IC10 Resource Curator

Find and organize external IC10 resources. Pure curation - no code generation.

## Workflow

1. **Search Phase**
   Use Task tool to spawn:
   - `resource-curator` - Search all external sources

2. **Guide Creation**
   Agent saves guide to `guides/[topic]-resources.md`

3. **Present Results**
   Summarize findings with top recommendations

## Instructions

When the user asks to find or curate resources:

1. Extract the topic from their request

2. Launch `resource-curator` agent with:
   - Topic keywords
   - Any specific constraints (e.g., "simple", "for beginners")

3. Wait for agent to complete search and guide creation

4. Present summary to user:
   - Number of resources found
   - Top 2-3 recommendations with links
   - Path to full guide

5. Do NOT offer to generate code (that's ic-generate's job)

## Example Triggers

- "Find trading scripts"
- "What IC10 examples exist for solar tracking?"
- "Curate resources for pressure control"
- "Search for existing airlock solutions"
- "What's out there for furnace automation?"
- "Show me community scripts for..."

## Output Format

After curation completes, respond with:

```
## Found Resources for "[Topic]"

I searched GitHub, Wiki, and Reddit for [topic] IC10 resources.

**Results**: X resources across Y sources

### Top Recommendations

1. **[Title]** - [1-line description]
   [URL]

2. **[Title]** - [1-line description]
   [URL]

3. **[Title]** - [1-line description]
   [URL]

Full guide saved to: `guides/[topic]-resources.md`
```

## Notes

- This skill is for discovery only
- If user wants custom code, direct them to use ic-generate
- Always include links to original sources
- Note when searches return few or no results
