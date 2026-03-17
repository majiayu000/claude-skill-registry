---
name: claude-gladiator
description: Continuous learning — hooks observe failures and prompt reflection, sibling synergy deepens analysis with history and tool discovery
triggers: [PostToolUse, Stop]
---

# Gladiator Plugin

Continuous learning. Observes tool failures and prompts reflection at session end to evolve rules, hooks, and skills.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PostToolUse(Bash\|Edit\|Write)** | After tool failure | Observes the error pattern (silent on success) |
| **Stop** | Session ending | Prompts reflection if unprocessed observations exist |

## Commands

| Command | Description |
|---------|-------------|
| `/review-gladiator [topic]` | Batch learn from accumulated observations and session history |

## Workflows

### Observe (automatic via hooks)

Tool failures trigger observation automatically:
```
gladiator_observe(
  summary: "<what failed and how it was fixed>",
  context: {error, tool, before, after},
  tags: ["error", "<tool_name>"]
)
```

### Reflect (standalone)

1. `gladiator_reflect()` — cluster observations into recommendations
2. For each recommendation: read the existing artifact (if overlap detected)
3. Propose UPDATE to existing artifact, not a new duplicate
4. Present to user with reasoning
5. Apply changes one at a time after approval

### Reflect (with siblings)

1. If **historian** active: enrich reflection with broader context
   - `search_conversations("project or topic")` — related past work
   - `get_error_solutions("specific error")` — for error clusters
   - `find_tool_patterns("tool name")` — for tool workflow clusters
2. `gladiator_reflect()` — cluster observations
3. If **oracle** active: for each recommendation involving new artifacts
   - `search("cluster tag")` — check if best-in-class solution already exists
   - Install existing solution instead of reinventing
4. Present enriched recommendations: pattern + history + available tools
5. Apply changes one at a time after approval

### Batch Review (/review-gladiator)

1. If **historian** active: `list_recent_sessions()` to get session refs
2. `gladiator_observe(source: "conversation", session_ref: <ref>)` for relevant sessions
3. `gladiator_reflect()` to cluster all observations
4. If **oracle** active: search for existing solutions before creating new
5. Present recommendations to user

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Historian** | Past solutions enrich reflection | `get_error_solutions()`, `search_conversations()`, `find_tool_patterns()` |
| **Oracle** | Existing tools found before creating new | Search oracle for best-in-class solutions during reflection |
| **Praetorian** | n/a | Gladiator has its own persistence |
| **Vigil** | n/a | Different concerns (files vs patterns) |

## Observation Templates

| Situation | Call |
|-----------|------|
| Tool failure (auto) | `gladiator_observe(summary, context={error, tool, before, after}, tags=["error", tool])` |
| User correction | `gladiator_observe(summary, context={before, after}, tags=["correction"])` |
| Convention found | `gladiator_observe(summary, tags=["convention", "domain"])` |
| Decision made | `gladiator_observe(summary, tags=["architecture", "decision"])` |

## Requires

```
claude mcp add gladiator -- npx claude-gladiator-mcp
```
