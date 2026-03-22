---
name: tool-usage-discipline
description: Use skills for domain knowledge, MCP tools over manual lookups
category: Workflow Orchestration
---

# Skill: tool-usage-discipline

## What I do

I ensure the most efficient and accurate use of available tools. I prioritise high-context MCP tools and loaded skills over manual exploration, preventing reinventing the wheel and reducing context bloat.

## When to use me

- Before starting any investigation or code change
- To decide whether to use a specific MCP tool or a manual bash command
- When facing a large codebase where manual navigation is inefficient
- To optimise token usage and session length

## Core principles

1. **Prioritise MCP** — Use specialized tools (LSP, grep, glob) before generic ones (bash ls/cat).
2. **Consult skills first** — Use loaded skills for domain expertise before seeking external information.
3. **Avoid redundancy** — Don't call a tool if you already have the information in your context.
4. **Cache results** — Store complex tool outputs (e.g. large grep results) in memory for the duration of the session.

## Patterns & examples

**Tool Selection Decision Matrix:**
- **Code Search:** Use `grep` or `ast_grep` (fast, indexed) over manual `find` + `cat`.
- **Navigation:** Use `lsp_goto_definition` over manual searching.
- **Verification:** Use `lsp_diagnostics` before running a full build.
- **Domain Knowledge:** Use the `skill()` or `vault-rag` tools before web search.

**Efficient Pattern:**
- **Inefficient:** `ls -R`, `cat file1`, `cat file2`, `grep "pattern" file1`...
- **Efficient:** `grep -r "pattern"` followed by `read` on the most relevant match.

## Anti-patterns to avoid

- ❌ **Tool spam** — Calling multiple tools to get information that a single, better tool could provide.
- ❌ **Reinventing the tool** — Writing a complex bash script when an MCP tool already handles that use case.
- ❌ **Ignoring tool documentation** — Using a tool sub-optimally because you haven't checked its parameters.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Tool Usage Discipline.md`

## Related skills

- `pre-action` — Deciding on the best tool approach
- `memory-keeper` — Storing tool results to avoid repeat calls
- `knowledge-base` — Using specialized search tools
- `token-efficiency` — Optimising tool calls for token budget
