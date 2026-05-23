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
- **LANGUAGE** - Default output in Simplified Chinese; avoid English abbreviations in node names and labels

Output modes:
- Default: produce sections 0-5.
- Quick map (info-poor/time-boxed): produce 0/1/3/5 + top 3 unknowns that would change the map.

## NEVER

- NEVER ship a solution-first plan; produce a map that enables the next step.
- NEVER mix facts and assumptions; label unknowns explicitly or the map lies.
- NEVER include non-CORE modules in the flow map; it hides the real bottleneck.
- NEVER write the flow map as a dense paragraph; it must be laid out line-by-line.
- NEVER use English abbreviations for flow nodes; use clear Chinese nouns instead.
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
- Output: Console-friendly flow map using `->` (CORE only, 6-15 lines):
  - Boundary context (vertical chain)
  - Internal critical path (one main chain)

Flow map conventions (ASCII only):
- Use Chinese noun phrases for node names; avoid English abbreviations.
- Prefer the single critical path over full coverage; do not force branches/merges.
- Layout as a vertical chain: one node per line, connect with `->` on the next line.
- Keep it readable: <= 80 cols per line, <= 20 lines total.

Template (vertical chain):
边界:
参与者
 -> 入口
 -> 系统
 -> 外部依赖

关键路径:
输入
 -> 核心模块
 -> 状态/存储
 -> 输出

**PHASE 4: OSCILLATION (Zoom In/Out)**

- Pipeline: macro frame -> latticework check -> key drivers -> causal chains -> leverage points
- Rule: derive top-down hypotheses, validate bottom-up via key driver mechanics
- Macro frame: boundary + lifecycle + stakeholders + metrics + constraints
  - Lifecycle stage: prototype -> growth -> scale -> decline (pick one)
- Latticework check (internal, do NOT expand in output):
  - Assume the role of 查理·芒格.
  - Cross-check with at least 3 mental models: 激励机制, 二阶效应, 机会成本, 安全边际, 能力圈(认知边界).
  - Extract only the synthesized signals for output: 收敛 / 张力 / 空白 / 惊喜
- Key drivers (1-3): mechanism + invariants + stress failures + cost model
- Output:
  - 2-4 causal chains: `微观机制 -> 宏观结果` (标签: **收敛/张力/空白/惊喜**)
  - Leverage points (micro changes that shift macro materially)

**PHASE 5: INVERSION (The Pre-Mortem)**

- Assume the proposed approach has FAILED CATASTROPHICALLY 6 months post-launch.
- Ask "How exactly did it break?" (race conditions, cost explosion, user rejection).
- Use Phase 0 constraints to sharpen the failure story.
- Output: "致命点" (fatal flaws) + "缓解假设" (testable preventions).

## Output Format

```
### 0.约束条件 (假设/给定)
问题: [一句话问题陈述]
约束: [硬约束列表]
未知: [会改变分析结论的关键未知]

### 1.核心模块 (帕累托前 20%)
[模块名]: [一句话说明为何这是核心]
[模块名]: [一句话说明为何这是核心]

### 2.第一性原理真相
[模块A] [根本限制/真相]
[模块B] [根本限制/真相]

### 3.逻辑流程图
控制台风格（使用 `->`，中文节点名，避免英文缩写；每行一个节点）:
边界:
参与者
 -> 入口
 -> 系统
 -> 外部依赖

关键路径:
输入
 -> 核心模块
 -> 状态/存储
 -> 输出

### 4.对齐检查（格栅快速校验）
宏观: [边界/生命周期/参与方/成功指标/硬约束]
关键驱动: [1-3 个主导机制]
格栅结论: 收敛[...]；张力[...]；空白[...]；惊喜[...]
因果链: [微观机制 -> 宏观结果 | 标签: 收敛/张力/空白/惊喜 | 杠杆点: ...]

### 5.事前验尸 (失败检查)
* 最薄弱环节: [具体组件]
* 失败模式: [如何崩溃] -> 缓解假设: [可验证的缓解假设]
```

## Key Principles

- **Pareto Focus** - Keep CORE only; park the rest
- **Fact vs Assumption** - Turn debates into checkable statements
- **Latticework** - Cross-check with 3-5 lenses; synthesize signals
- **Causal Mapping** - Express micro->macro via chains and leverage points
- **Inversion Thinking** - Assume failure first, then work backwards
- **Terminal First** - Use ASCII maps (`->`) only; no rich diagrams
