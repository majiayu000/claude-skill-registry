---
name: kg-insights
description: Helps users discover patterns and insights in their Knowledge Graphs.
  Use when users ask about important entities, connections, patterns, or want
  to understand what they can do with their graph. Triggers proactively after
  extraction to show what's possible.
---

# Knowledge Graph Insights

Help users explore their Knowledge Graph with natural questions. Transform graph analysis into actionable insights with clear explanations of why each finding matters.

## What Users Can Ask

| Question | Sub-Resource | When to Use |
|----------|--------------|-------------|
| "Who are the key players?" | `questions/key-players.md` | User wants to find important entities |
| "How is X connected to Y?" | `questions/connections.md` | User wants to understand relationship paths |
| "What groups or clusters exist?" | `questions/groups.md` | User wants to see topic organization |
| "Where is X mentioned?" | `questions/evidence.md` | User wants source citations for claims |
| "What can I do with this graph?" | `POWER-QUERY.md` | User is unsure what's possible |

## Proactive Triggers

Invoke this skill automatically in these situations:

### After Extraction Completes
When `extract_to_kg` finishes successfully:
```
Great! I've added [N] entities and [M] relationships to your graph.

Your Knowledge Graph now has [total] entities. Would you like me to:
1. Show who the key players are
2. Find interesting connections
3. See how topics cluster together

Just ask, or type a number!
```

### After Milestone Reached
When graph reaches 50+ entities:
```
Your Knowledge Graph is growing! With [N] entities, there's a lot to explore.

Some questions you might find interesting:
- "Who appears most often across my sources?"
- "How is [popular entity] connected to [another]?"
- "What are the main topic clusters?"
```

### When User Seems Unsure
If user asks vague questions like "what now?" or "what's next?":
- Read `POWER-QUERY.md` for smart suggestions
- Present personalized options based on their graph's content

## Tool Mapping

Map natural questions to KG tools:

| User Intent | Tool | Parameters |
|-------------|------|------------|
| Key players | `get_kg_stats` | `project_id` |
| Connections | Graph path query | source/target labels |
| Evidence | Source lookup | entity/relationship ID |
| Statistics | `get_kg_stats` | `project_id` |

## Response Format

### Always Include

1. **Direct Answer** - Lead with the key finding
2. **Supporting Data** - Table or list with specifics
3. **Why This Matters** - Explain the significance
4. **Explore Further** - 2-3 follow-up suggestions

### Example Response Structure

```markdown
## Key Players in Your Graph

Based on connection analysis, here are the most influential entities:

| Entity | Type | Connections | Appears In |
|--------|------|-------------|------------|
| [Name] | Person | 12 | 4 sources |
| [Name] | Organization | 8 | 3 sources |

### Why This Matters

These entities are central to your research because:
- **[Name]** appears across multiple sources, suggesting they're a recurring theme
- **[Name]** connects to many other entities, making them a good entry point

### Explore Further

- "How is [Name A] connected to [Name B]?" — Trace the relationship path
- "Show me [Name]'s connections" — See their full network
- "What sources mention [Name]?" — Find evidence and citations
```

## Follow-Up Format (CRITICAL - MUST READ)

**The frontend parses your "Explore Further" section and creates clickable suggestion cards.**

For this to work, you MUST use this exact format:

```markdown
### Explore Further

- "Query in quotes" — Brief description
- "Another query" — Brief description
```

**Required Elements:**
1. Use a bullet list (`-` or `*`)
2. Put the query in **double quotes** (`"query here"`)
3. Add a description after em-dash (`—`) or colon (`:`)

**Correct:**
```
- "Show me Fear's connections" — See the full network
- "How is Hope connected to Fear?" — Trace the path
```

**Wrong (cards won't appear):**
```
- Show me Fear's connections
- How is Hope connected to Fear?
```

**Replace placeholders** like `[Name]` with actual entity names from the user's graph.

## Graph Analysis Methods

Use these approaches when answering questions:

### Finding Key Players (Degree Centrality)
Count connections for each entity. More connections = more central.
- Use `get_kg_stats` for type breakdown
- Cross-reference with source counts

### Finding Paths (Shortest Path)
Use NetworkX path finding to show how entities connect.
- Show step-by-step: A -> B -> C
- Include relationship types at each step

### Finding Clusters (Community Detection)
Group entities that are densely connected.
- Use entity types as initial groupings
- Look for entities bridging groups

### Finding Evidence (Provenance)
Trace entities and relationships back to sources.
- Include confidence scores
- Quote relevant text when available

## Critical Rules

1. **Plain Language First** - Say "well-connected" not "high degree centrality"
2. **Always Explain Why** - Every insight needs a "why this matters"
3. **Offer Next Steps** - Never leave users without options
4. **Use Real Data** - Never make up entity names or statistics
5. **Cite Sources** - When showing evidence, include source references
6. **Quote Follow-Ups** - ALWAYS put follow-up queries in "double quotes" with descriptions
7. **Use Entity Names** - Replace [placeholders] with actual names from the user's graph

## Error Handling

| Issue | Response |
|-------|----------|
| No project selected | "Please select a Knowledge Graph project first, or create one with `kg-bootstrap`" |
| Empty graph | "Your graph doesn't have any entities yet. Add a transcript with `extract_to_kg`" |
| Entity not found | "I couldn't find '[name]' in your graph. Try a different spelling or check available entities" |
| No path exists | "These entities aren't connected in your graph. They may appear in separate contexts" |
