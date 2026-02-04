---
name: context-engineering
description: Principles for designing context-efficient AI agents and tools. Use when designing LLM tools, agents, MCP servers, or multi-agent systems.
---

# Context Engineering

Principles for maximizing LLM effectiveness by treating context as a finite resource.

## Core Principle

Find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome.

## The Context Budget

LLMs have an "attention budget" that depletes with each token. Context rot causes recall accuracy to decrease as token count grows. Every design decision should optimize for signal density.

## Quick Reference

| Challenge | Strategy | Reference |
| --------- | -------- | --------- |
| Too many tools | Curate minimal viable set | [Tool](references/tool.md) |
| Ambiguous tool selection | Self-contained, unambiguous tools | [Tool](references/tool.md) |
| Context pollution over time | Compaction and summarization | [Agent](references/agent.md) |
| Long-horizon tasks | External memory and note-taking | [Agent](references/agent.md) |
| Exceeding single context limits | Sub-agent architectures | [Multi-Agent](references/multi-agent.md) |
| MCP server bloat | Token-efficient responses | [MCP](references/mcp.md) |
| Measuring effectiveness | End-state evaluation | [Evaluation](references/evaluation.md) |

## Single vs Multi-Agent

Multi-agent adds ~15x token overhead. Use single agent unless:

| Factor | Single Agent | Multi-Agent |
| ------ | ------------ | ----------- |
| Parallelization | Sequential steps | Independent subtasks |
| Context size | Fits in window | Exceeds single context |
| Tool complexity | Focused toolset | Many specialized tools |
| Dependencies | Steps depend on each other | Work can be isolated |

Default to single agent. Add agents only when parallelization or context limits demand it.

## Decision Checklists

### Before Adding to Context

- Is this the minimum information needed?
- Can an agent discover this just-in-time instead?
- Does this justify its token cost?

### Tool Design

- Can a human definitively say which tool to use?
- Does each tool have a distinct, non-overlapping purpose?
- Are responses token-efficient with high signal?
- Do error messages guide toward solutions?

### Agent Design

- Does the system prompt strike the right altitude?
- Are there mechanisms for compaction when context grows?
- Is external memory used for long-horizon tracking?
- Are canonical examples provided instead of exhaustive rules?

### Multi-Agent

- Is the task parallelizable enough to justify coordination overhead?
- Do sub-agents return condensed summaries (not raw results)?
- Is there clear separation of concerns between agents?

## Key Techniques

### Just-in-Time Retrieval

Keep lightweight identifiers (paths, queries, links). Load data dynamically at runtime rather than pre-loading everything upfront.

### Progressive Disclosure

Let agents discover context through exploration. File sizes suggest complexity; naming hints at purpose. Each interaction yields context for the next decision.

### Compaction

Summarize conversations nearing limits. Preserve architectural decisions and critical details; discard redundant tool outputs and verbose messages.

### Structured Note-Taking

Persist notes to external memory (to-do lists, NOTES.md). Pull back into context when needed. Tracks progress without exhausting working context.

### Sub-Agent Distribution

Delegate focused tasks to specialized agents with clean context windows. Each sub-agent explores extensively but returns only condensed summaries (1000-2000 tokens).

## The Golden Rule

Do the simplest thing that works. Start minimal, add complexity only based on observed failure modes.

## References

- [Tool](references/tool.md) - Building self-contained, token-efficient tools
- [Agent](references/agent.md) - Single agent context management
- [Multi-Agent](references/multi-agent.md) - Coordinating multiple agents
- [MCP](references/mcp.md) - Model Context Protocol best practices
- [Evaluation](references/evaluation.md) - Measuring context engineering effectiveness

## Examples

Complete examples from Claude Code:

### Tool Descriptions
- [Bash](examples/tool-bash-example.md) - Boundaries, when NOT to use, good/bad examples
- [Edit](examples/tool-edit-example.md) - Prerequisites, error guidance, concise design
- [Grep](examples/tool-grep-example.md) - Exclusivity, parameter examples, output modes

### Agent Prompts
- [Explore](examples/agent-explore-example.md) - Role definition, constraints, strengths
- [Plan](examples/agent-plan-example.md) - Process steps, output format, boundaries
- [Summarization](examples/agent-summarization-example.md) - Compaction structure, what to preserve
