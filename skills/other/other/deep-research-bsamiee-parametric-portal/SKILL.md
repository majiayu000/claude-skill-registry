---
name: deep-research
type: simple
depth: extended
user-invocable: false
description: >-
  Orchestrates two-round parallel agent research with Exa orientation, breadth-first discovery, and depth-focused synthesis. Use when conducting comprehensive research, exploring complex topics requiring multi-source validation, or synthesizing findings from distributed investigation streams.
---

# [H1][DEEP-RESEARCH]
>**Dictum:** *Iterative dispatch with inter-round critique maximizes research coverage.*

<br>

Conduct comprehensive topic research via parallel agent dispatch.

**Workflow:**
1. §ORIENT — Execute 3 Exa searches via `exa-tools` skill, map landscape, extract facets
2. §ROUND_1 — Dispatch 6-10 agents for breadth coverage via `parallel-dispatch` skill
3. §CRITIQUE_1 — Filter findings, retain quality, build skeleton with gaps
4. §ROUND_2 — Dispatch 6-10 agents to flesh out skeleton
5. §CRITIQUE_2 — Synthesize holistically, deduplicate, produce final output

**Dependencies:**
- `exa-tools` — Web search and code context queries (primary)
- `perplexity-tools` — Deep research and reasoning queries (supplementary)
- `tavily-tools` — Web search with domain governance (supplementary)
- `parallel-dispatch` — Agent orchestration mechanics

**Input:**
- `Topic`: Domain to research
- `OutputPath`: Target file path (passed by invoking command, default: `report.md`)
- `Constraints`: Context, scaffold, style from invoking skill

[CRITICAL]:
- [ALWAYS] Main agent writes to `OutputPath` only—no other files.
- [ALWAYS] Sub-agents RETURN structured text—main agent is sole file writer.
- [NEVER] Sub-agents use Write, Edit, Bash, or create any files.

---
## [1][ORIENT]
>**Dictum:** *Initial queries map landscape before dispatch.*

<br>

Main agent executes exactly 3 Exa searches via `exa-tools` skill before dispatch.

Map domain landscape; identify facets for agent assignment. Produce facet list (6-10 independent research areas) for Round 1.

[IMPORTANT]:
- [ALWAYS] Execute 3 Exa searches via `exa-tools` skill before dispatch.
- [ALWAYS] Extract facet boundaries from results.
- [ALWAYS] Use `deep` search tier for highest-quality results when topic warrants it.
- [NEVER] Dispatch before orient completes.
- [NEVER] Accept sources older than 6 months unless topic is historical.

---
## [2][ROUND_1]
>**Dictum:** *Breadth via parallel dispatch—6-10 agents exploring independent facets.*

<br>

Dispatch 6-10 sub-agents via `parallel-dispatch`. Assign each agent unique scope from orient facets.

**Agent Count:** Scale by task complexity (default: 6).

**Agent Prompt:**
```
Scope: [Specific facet from orient]
Objective: Research this facet comprehensively
Output: Return structured text (CRITICAL → FINDINGS → SOURCES)
Context: [Topic background, constraints]
Constraint: DO NOT write files—return text only
```

[CRITICAL]:
- [ALWAYS] Dispatch ALL agents in ONE message block.
- [ALWAYS] Include "DO NOT write files" constraint in every agent prompt.
- [NEVER] Create overlapping scopes.

---
## [3][CRITIQUE_1]
>**Dictum:** *Main agent builds skeleton—retains quality, identifies gaps.*

<br>

Main agent (NOT sub-agent) processes Round 1 outputs.

| [INDEX] | [ACTION] | [CRITERIA]                                                        |
| :-----: | -------- | ----------------------------------------------------------------- |
|   [1]   | Remove   | Lacks focus, duplicates, no sources, pre-2025, fails quality      |
|   [2]   | Retain   | Addresses topic, sources, dates 2025-2026, converges across range |

Build skeleton from retained findings: `[Domain N]: [findings]` + `Gaps:` + `Depth-Targets:`

[CRITICAL] Skeleton is first corpus—Round 2 fleshes it out.

---
## [4][ROUND_2]
>**Dictum:** *Depth via parallel dispatch—same agent count, focused on skeleton gaps.*

<br>

Dispatch 6-10 sub-agents (same count as Round 1) via `parallel-dispatch`.

**Agent Assignment:**

| [INDEX] | [TYPE]  | [PURPOSE]                   | [COUNT] |
| :-----: | ------- | --------------------------- | ------- |
|   [1]   | Focused | Specific gaps from skeleton | 4-6     |
|   [2]   | Wide    | Broader context for areas   | 2-4     |

**Agent Prompt:**
```
Scope: [Gap or depth-target from skeleton]
Objective: [Focused: fill gap | Wide: broaden context]
Output: Return structured text (CRITICAL → FINDINGS → SOURCES)
Context: [Skeleton content—build on, don't repeat]
Prior: [Relevant Round 1 findings]
Constraint: DO NOT write files—return text only
```

[CRITICAL]:
- [ALWAYS] Same agent count as Round 1.
- [ALWAYS] Include skeleton context.
- [ALWAYS] Include "DO NOT write files" constraint in every agent prompt.

---
## [5][CRITIQUE_2]
>**Dictum:** *Main agent synthesizes holistically—final corpus for downstream use.*

<br>

Main agent (NOT sub-agent) compiles final research output and writes to `OutputPath`.

**Integrate:** Merge Round 2 → skeleton. Cross-reference rounds. Resolve conflicts (prioritize sourced, current, convergent).<br>
**Filter:** Remove duplicates, out-of-scope content, superseded items, unresolved conflicts.<br>
**Write:** Single file to `OutputPath`:
- `## [1][FINDINGS]` — Synthesized research by domain
- `## [2][CONFIDENCE]` — High (convergent), Medium (single-source), Low (gaps)
- `## [3][SOURCES]` — All sources with attribution

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent incomplete synthesis.*

<br>

[VERIFY]:
- [ ] Orient: 3 Exa searches executed via `exa-tools` skill
- [ ] Round 1: 6-10 agents in ONE message, all returned text (no file writes)
- [ ] Critique 1: Skeleton built, gaps identified
- [ ] Round 2: Same count, focused on skeleton, all returned text (no file writes)
- [ ] Critique 2: Final synthesis, duplicates removed
- [ ] Single file written to `OutputPath` by main agent only
