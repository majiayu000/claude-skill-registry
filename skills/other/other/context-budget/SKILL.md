---
name: context-budget
description: "Context budget tracking and skill loading limits for agent sessions. Monitors token consumption per agent, enforces preloading limits, and alerts on context bloat. Use when spawning agents, configuring skill preloading, or optimizing token usage."
---

# Context Budget Management

## Why This Matters
The system prompt already includes ~50 built-in instructions. Adding a 451-line CLAUDE.md means every agent starts with ~500 instructions, of which only 10-20 are relevant. Instruction degradation is uniform — when context bloats, ALL instructions degrade, not just those at the bottom.

## Skill Preloading Limits
- **Max 5 preloaded skills per agent** (via `skills` field in agent spec)
- **Max 500 lines total** preloaded skill content per agent
- **Max 8 on-demand skills** available per API request (LLM selection degrades beyond 8)
- Preloaded skills bypass the 8-skill on-demand limit entirely

## Per-Agent Budget Targets
| Agent Tier | Max Preloaded Skills | Max Lines | Rationale |
|------------|---------------------|-----------|-----------|
| Haiku (junior-coder, docs, explainer, optimizer) | 3 | 200 | Limited context capacity |
| Sonnet (coder, tech-lead, reviewer, qa, etc.) | 5 | 400 | Standard working context |
| Opus (planner, red-teamer, senior-coder) | 5 | 500 | Deep reasoning, can handle more |

## Tracking Checklist
When spawning an agent:
1. Count preloaded skills from agent spec `skills` field
2. Sum total lines across all preloaded SKILL.md files
3. If > 500 lines total → remove least-relevant skill or split skill into sub-skills
4. Log which skills are loaded per agent session to claude-mem (for optimizer analysis)

## Context Bloat Signals
Watch for these signs that an agent's context is overloaded:
- Agent ignores instructions that are clearly in its preloaded skills
- Agent repeats questions that are already answered in its context
- Agent produces inconsistent output between similar tasks
- Agent takes longer on simple tasks (reasoning through noise)

## MCP Context Impact
MCP tool descriptions load into context alongside skills. Account for:
- Serena: ~500 tokens for tool descriptions (find_symbol, get_symbols_overview, etc.)
- context7: ~200 tokens (query-docs, resolve-library-id)
- claude-mem: ~300 tokens (search, save_memory, get_observations, timeline)
- Linear: ~800 tokens (many issue/project tools)
Total MCP overhead: ~1,800 tokens baseline, always present
Factor this into per-agent budget calculations.

## Measurement
- Count lines of each SKILL.md: `wc -l .claude/skills/*/SKILL.md`
- Sum per agent configuration from agent spec `skills` field
- Log task outcomes to claude-mem using this schema:
  ```
  "Agent [type] ([model]) [passed|failed] [task-type]: [one-line reason]"
  Example: "Agent coder (sonnet) passed rust-implementation: all tests green, clippy clean"
  Example: "Agent junior-coder (haiku) failed test-writing: couldn't handle async test patterns"
  ```
- Run optimizer agent periodically to review budget efficiency
