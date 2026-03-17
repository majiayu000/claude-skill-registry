---
name: claude-orator
description: Prompt rhetoric coach — deterministic scoring and restructuring using Anthropic best practices
triggers: [PreToolUse]
---

# Orator Plugin

Prompt optimization. Scores prompts across 7 dimensions and restructures them using 8 Anthropic techniques. Deterministic — no LLM calls, no network, in-memory only.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PreToolUse(Task)** | Subagent prompt lacks structure | Suggests `orator_optimize` before dispatching |

Token cost: 0 on well-structured prompts (XML tags, markdown headers, action verbs). ~50-80 on vague prompts. Never blocks — suggestion only.

## Commands

| Command | Description |
|---------|-------------|
| `/reprompt-orator <prompt>` | Optimize a prompt using Anthropic best practices |

## Workflows

### Optimize (standalone)

1. `/reprompt-orator "your prompt here"` or call `orator_optimize(prompt: "...")`
2. Review score breakdown (7 dimensions, 1-10 each)
3. Use the restructured prompt with applied techniques

### Optimize (with siblings)

1. If **historian** active: `search_conversations("prompt optimization")` to find past well-scored prompts
2. `orator_optimize(prompt: "...")` — score and restructure
3. If **praetorian** active: `save_context(type: "decisions", ...)` to preserve the optimized prompt rationale
4. If **gladiator** active: `observe(summary: "xml-tags improved code prompts by +3.2")` to track what works

### Batch review

1. Review subagent prompts across a session
2. `orator_optimize` on each under-specified prompt
3. If **vigil** active: `vigil_save("before-rewrite")` before applying changes
4. Apply restructured prompts

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Historian** | Past well-scored prompts as examples | `search_conversations("prompt patterns")` finds effective prompts from history |
| **Praetorian** | Preserve optimization rationale | Compact optimized prompts and their scores for future reference |
| **Gladiator** | Track what techniques work best | `observe()` records which techniques improve scores most |
| **Oracle** | Find prompt engineering tools | `search("prompt patterns")` discovers relevant community tools |
| **Vigil** | Checkpoint before batch rewrites | `vigil_save()` before applying optimized prompts across files |

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `orator_optimize` | Score prompt across 7 dimensions, apply techniques, return restructured version |

## Scoring Dimensions

Clarity · Specificity · Structure · Context · Examples · Constraints · Tone (each 1-10)

## Techniques

System prompts · XML tags · Chain of thought · Few-shot · Prefill · Long context · Extended thinking · Tool use

## Storage

In-memory only. Zero disk storage. No databases, no external services.

## Requires

```
claude mcp add orator -- npx claude-orator-mcp
```
