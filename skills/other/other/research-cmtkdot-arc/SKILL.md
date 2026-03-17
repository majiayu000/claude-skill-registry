---
name: research
description: Use when the user asks to research, investigate, compare approaches, or explore a topic in depth. Supports configurable depth and multi-source synthesis.
invocation: agent
---

# Research

Deep research with multi-source synthesis. Uses `multi-ai` skill for provider routing when available.

## Workflow

### Step 1: Determine Depth

Use AskUserQuestion if depth is not specified:

- **Quick**: Fast overview of key concepts (2-3 sources)
- **Standard**: Comprehensive analysis with examples (5-8 sources)
- **Deep**: Thorough research with citations and evidence (10+ sources)

If the user provides `--depth`, skip the question.

### Step 2: Provider Routing

- If `ARC_MULTI_AI=true` and providers are available, use multi-provider research via `multi-ai` skill.
- Otherwise run Claude-only research with the same structure.

### Step 3: Multi-Source Synthesis

Launch the `persona-research-synthesizer` agent with gathered context:

```
subagent_type: "arc:persona-research-synthesizer"
run_in_background: true
prompt: "Research topic: <topic>\nDepth: <depth>\nProviders: <available providers>"
```

Output a status message and end your turn. The system wakes you when the agent finishes.

### Step 4: Report Results

```
## Research Complete

**Topic**: <topic>
**Depth**: <quick|standard|deep>
**Sources Consulted**: <count>

### Key Findings
[Structured findings with evidence]

### Comparative Analysis
[Pros/cons of different approaches]

### Recommendations
[Actionable recommendations with rationale]

### Next Steps
- `/arc:core:plan` to plan implementation based on findings
- `/arc:specialized:prd` to write a PRD incorporating research
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Topic too broad | Ask user to narrow scope |
| No external providers | Continue with Claude-only research |
| Low confidence findings | Flag uncertainty, recommend deeper research |
