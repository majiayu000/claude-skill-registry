---
name: deep-analysis
description: "Execute high-density analysis on complex ideas/tasks. Move from 'Vague' to 'Verified' by producing: constraints -> core modules -> facts vs assumptions -> ASCII flow maps (boundary + critical path) -> latticework lens sweep -> micro->macro causal chains -> pre-mortem failure modes. Use when analyzing system architecture, validating technical ideas, or decomposing a thorny problem before designing solutions."
---

# Architectural Analysis

## Overview

Execute high-density analysis to transform vague ideas into a verified problem map: constraints, core modules, facts vs assumptions, relationship flows, causal chains, and failure modes. Focus on analysis artifacts that unlock the next workflow step, not a full design.

**Style:** Code-like, Concise, No "AI explaining itself". Pure signal.

## Critical Rules

- **NO FLUFF** - Output must be dense, actionable, and structured
- **VISUALIZE** - Use terminal-friendly ASCII maps (`->`) for structural mappings
- **ANALYZE, DON'T BUILD** - Prefer maps, drivers, and failure modes over implementation plans unless explicitly requested
- **RUTHLESSNESS** - Challenge assumptions at every step. Never confirm user biases
- **LATTICEWORK** - Validate the map with 3-5 lenses; look for convergence/tension/blind spots/surprises

Output modes:
- Default: produce sections 0-5.
- Quick map (info-poor/time-boxed): produce 0/1/3/5 + top 3 unknowns that would change the map.

## NEVER

- NEVER ship a solution-first plan; produce a map that enables the next step.
- NEVER mix facts and assumptions; label unknowns explicitly or the map lies.
- NEVER include non-CORE modules in the flow map; it hides the real bottleneck.
- NEVER output a 1D "A->B->C" only; the flow map must show branches/merges (2D).
- NEVER exceed terminal constraints (aim <= 80 cols, <= 20 lines) or it becomes unreadable.

## The Process

**PHASE 0: CALIBRATION (The Anchor)**

- Bind constraints strictly.
- If constraints are missing: assume "MVP/Prototype Stage" (low cost, high iteration) and proceed.
- If the prompt starts with a solution: rewrite as "problem statement + constraints" before proceeding.
- Output: One-sentence problem statement + constraint list (incl. explicit unknowns).

**PHASE 1: DECOMPOSITION (The Pareto Slice)**

- Decompose into modules and interfaces (treat each module as a black box).
- Identify the Pareto CORE (top risk/weight); mark the rest as later.
- Output: CORE module list with 1-line rationale each.

**PHASE 2: EXCAVATION (First Principles)**

For CORE modules identified in Phase 1:
- Separate facts vs assumptions; name the irreducible constraints/invariants.
- Locate the dominant bottleneck (ask "why not 10x?" to expose limits).
- Output: Compact fact/assumption list per CORE module.

**PHASE 3: RE-ARCHITECTING (Structural Evolution)**

Reassemble components based on First Principles findings, NOT original assumptions:
- Pipeline: CORE modules -> boundary context -> internal critical path -> prune -> output flow map
- Prune redundant hops found in Phase 2 (keep it minimal, not exhaustive).
- Output: Terminal-friendly 2D flow map using `->` (CORE only, 8-20 lines):
  - Boundary context (1-3 lines)
  - Internal critical path with branches/merges (2D; not just a single chain)

Flow map conventions (ASCII only):
- Use `[NOUN_PHRASE]` for nodes (modules, actors, systems)
- Use `->` for directional flow (data, control, dependency)
- Use `A <-> B` only when truly bidirectional
- Add short edge labels sparingly: `A ->(auth)-> B`
- Use indentation and `|` / `+-` to show branches; use `-+` to show merges

Templates:
- Boundary context: `[User/Actor] -> [Entry Point] -> [System] -> [External Dependency]`
- Internal (2D):
  `[Input] -> [Core A] -> [State/DB] -> [Output]`
  `           |-> [Core B] -> [Cache]`

**PHASE 4: OSCILLATION (Zoom In/Out)**

- Pipeline: macro frame -> lattice sweep -> key drivers -> causal chains -> leverage points
- Rule: derive top-down hypotheses, validate bottom-up via key driver mechanics
- Macro frame: boundary + lifecycle + stakeholders + metrics + constraints
  - Lifecycle stage: prototype -> growth -> scale -> decline (pick one)
- Lattice sweep (3-5 lenses; generate dynamically):
  - Ask: who handles it daily? who pays the highest failure cost? who attacks it? who sees incentives/cost curves? who has a different worldview?
  - If unclear, default to: operator / risk / economist / adversary
  - For each lens, extract: missing constraints, likely failure modes, candidate key drivers
- Key drivers (1-3): mechanism + invariants + stress failures + cost model
- Output:
  - 2-4 causal chains: `micro mechanism -> macro consequence` (label: **convergent/tension/blind spot/surprise**)
  - Leverage points (micro changes that shift macro materially)

**PHASE 5: INVERSION (The Pre-Mortem)**

- Assume the proposed approach has FAILED CATASTROPHICALLY 6 months post-launch.
- Ask "How exactly did it break?" (race conditions, cost explosion, user rejection).
- Use Phase 0 constraints to sharpen the failure story.
- Output: "Kill Shots" (fatal flaws) + "Mitigation Hypotheses" (testable preventions).

## Output Format

```
### 0.约束条件 (假设/给定)
问题: [one-sentence problem statement]
约束: [hard constraints]
未知: [unknowns that change the map]

### 1.核心模块 (帕累托Top 20%)
[模块名]: [一句话说明为何这是核心]
[模块名]: [一句话说明为何这是核心]

### 2.第一性原理真相
[模块A] [根本限制/真相]
[模块B] [根本限制/真相]

### 3.逻辑流程图
Flow map (ASCII 2D, `->`, <= 80 cols, 8-20 lines):
[Boundary]
[Actor] -> [Entry] -> [System] -> [External]

[Internal]
[Input] -> [Core A] -> [State/DB] -> [Output]
           |-> [Core B] -> [Cache]
           |-> [Queue] -> [Worker] -> [External]

### 4.对齐检查
宏观: [边界/环境/生命周期/指标/约束]
镜头: [lens] -> [insight]; [lens] -> [insight]; [lens] -> [insight]
关键驱动: [1-3 个主导机制]
微观: [关键驱动的机制/不变量/失败模式/成本模型]
链路: [micro -> macro 因果链(label: convergent/tension/blind spot/surprise) + 杠杆点]

### 5.事前验尸 (失败检查)
* 最薄弱环节: [具体组件]
* 失败模式: [如何崩溃] -> 缓解假设: [可验证的 mitigation hypothesis]
```

## Key Principles

- **Pareto Focus** - Keep CORE only; park the rest
- **Fact vs Assumption** - Turn debates into checkable statements
- **Latticework** - Cross-check with 3-5 lenses; synthesize signals
- **Causal Mapping** - Express micro->macro via chains and leverage points
- **Inversion Thinking** - Assume failure first, then work backwards
- **Terminal First** - Use ASCII maps (`->`) only; no rich diagrams
