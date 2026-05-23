---
name: deep-research
description: Use when user requests research requiring multiple sources, comprehensive analysis, or synthesis across topics - technical research, domain knowledge gathering, market analysis, or learning about complex subjects
---

# Deep Research

Autonomous multi-agent research system. Dispatches parallel sub-agents, stores findings to files, synthesizes into briefs or reports.

**Core principle:** Planning → Parallel research agents → File-based findings → Synthesis = high quality research with minimal context usage.

## When to Use

```dot
digraph when_to_use {
    "User requests research?" [shape=diamond];
    "Quick factual lookup?" [shape=diamond];
    "Use single search tool directly" [shape=box];
    "Multiple sources or synthesis needed?" [shape=diamond];
    "deep-research" [shape=box];

    "User requests research?" -> "Quick factual lookup?" [label="yes"];
    "Quick factual lookup?" -> "Use single search tool directly" [label="yes"];
    "Quick factual lookup?" -> "Multiple sources or synthesis needed?" [label="no"];
    "Multiple sources or synthesis needed?" -> "deep-research" [label="yes"];
}
```

**Use for:** Technical research, domain knowledge, market analysis, architectural patterns, comparing approaches, learning complex topics

**Don't use for:** Single fact lookups, specific URL fetches, questions answerable in one search

## The Process

```dot
digraph process {
    rankdir=TB;

    "Create research directory in scratchpad" -> "Dispatch Query Analyzer agent";
    "Dispatch Query Analyzer agent" -> "Analyzer writes research-plan.md";
    "Analyzer writes research-plan.md" -> "Read plan, dispatch N Research agents IN PARALLEL";
    "Read plan, dispatch N Research agents IN PARALLEL" -> "Each agent writes findings-{thread}.md";
    "Each agent writes findings-{thread}.md" -> "Wait for all agents";
    "Wait for all agents" -> "Dispatch Synthesizer agent";
    "Dispatch Synthesizer agent" -> "Synthesizer reads all findings, writes final-output.md";
    "Synthesizer reads all findings, writes final-output.md" -> "Read final output, present summary to user";
}
```

## Quick Reference

### Phase 1: Planning (Query Analyzer Agent)

Uses `./query-analyzer-prompt.md`. Writes `research-plan.md` containing:
- Query type: technical | domain | hybrid
- Complexity: simple (2-3 agents) | moderate (3-4) | complex (5-6)
- Research threads with source recommendations
- Output format recommendation: brief | report

### Phase 2: Parallel Research

Uses `./research-agent-prompt.md`. Each agent:
1. Invokes `exa-search` skill for source strategy
2. Executes searches (Exa-primary, see Source Selection below)
3. Writes `findings-{thread-name}.md`

**Source Selection:**

| Query Signal | Primary Source |
|--------------|----------------|
| Code, APIs, libraries | `mcp__exa__get_code_context_exa` |
| Concepts, analysis, opinions | `mcp__exa__web_search_exa` |
| Video explanations needed | `yt-transcribe` skill |
| Very recent news (< 1 week) | `WebSearch` fallback |

### Phase 3: Synthesis

Uses `./synthesizer-prompt.md`. Reads all findings files, writes `final-output.md`:
- **Actionable Brief** (~300 words): Simple query + clear consensus
- **Structured Report** (~1500 words): Complex query or conflicting findings

## Agent Dispatch Methods

**For complex queries (4+ threads):** Use Task tool with `subagent_type: "general-purpose"` for true sub-agent isolation. Dispatch all research agents in a single message (parallel Task calls).

**For simpler queries (2-3 threads):** Parallel tool calls within same context is acceptable - make all searches simultaneously, then write findings files.

Either way: research threads must execute in parallel, not sequentially.

## File Structure

```
{scratchpad}/deep-research-{timestamp}/
├── research-plan.md
├── findings-*.md
└── final-output.md
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Doing research yourself instead of dispatching agents | Always use the three-phase architecture |
| Keeping findings in context instead of files | Each agent MUST write to files |
| Sequential research agents | Dispatch all research agents in PARALLEL |
| Skipping planning phase | Always run Query Analyzer first |
| Using WebSearch as default | Exa is primary; WebSearch only for very recent news |

## Red Flags - STOP

- "I'll just do a quick search myself" → Use the full process
- "I don't need to write files for this" → Files are mandatory
- "I'll research these topics one at a time" → Parallel dispatch
- "This is simple, I'll skip planning" → Always plan first
