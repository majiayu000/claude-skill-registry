---
name: deep-analysis
description: "Execute high-density architectural analysis on user ideas. Move from 'Vague' to 'Verified' using a 5-step logic chain: Calibration → Decomposition → Excavation → Re-Architecting → Inversion. This skill should be used when analyzing system architecture, validating technical ideas, or performing pre-mortems on solutions."
---

# Architectural Analysis

## Overview

Execute high-density architectural analysis to transform vague ideas into verified, actionable architectures through a rigorous 5-phase logic chain.

**Style:** Code-like, Concise, No "AI explaining itself". Pure signal.

## Critical Rules

- **NO FLUFF** - Output must be dense, actionable, and structured
- **VISUALIZE** - Use Mermaid.js for all structural mappings
- **RUTHLESSNESS** - Challenge assumptions at every step. Never confirm user biases

## The Process

**PHASE 0: CALIBRATION (The Anchor)**

Evaluate if user has provided concrete constraints before generating solutions:

- IF YES: Bind constraints strictly
- IF NO: Assume context = "MVP/Prototype Stage" (Low Cost, High Iteration, Small Scale) and PROCEED

**PHASE 1: DECOMPOSITION (The Pareto Slice)**

- Smash the problem/system into its smallest indivisible units ("The LEGO Bricks").
- Group atomic units into independent "Black Boxes" (Modules). Modules must be **Decoupled**. Analyzing Module A should not require holding Module B in memory.
- Identify top 20% of modules carrying 80% of functional weight or risk
- Label the rest as "Trivial/Later"
- Output: List CORE modules only. Discard noise

**PHASE 2: EXCAVATION (First Principles)**

For CORE modules identified in Phase 1:

- Strip away all "best practices" and "industry standards"
- Identify Irreducible Truths (Physical limits, Logic gates, Bandwidth laws)
- Ask: "Why can't we do it 10x greater/faster?" to find fundamental bottleneck
- Output: A "Fact vs. Assumption" table for each core module

**PHASE 3: RE-ARCHITECTING (Structural Evolution)**

Reassemble components based on First Principles findings, NOT original assumptions:

- Optimize path: Remove redundant hops/processes found in Phase 2
- Output: Generate a Mermaid.js Flowchart
  - Show data flow, dependencies, and critical paths
  - Structure must be simpler and more direct than initial decomposition

**PHASE 4: OSCILLATION (Zoom In/Out)**

- Action: Oscillate between the texture and the landscape.
- Zoom In: Look at the "Code/Texture" of the Key Driver. (The implementation detail).
- Zoom Out: Look at the "Time/Cycle" of the system. (Where is this in the historical lifecycle?).
- Output: A synthesis of how the micro-detail affects the macro-destiny.

**PHASE 5: INVERSION (The Pre-Mortem)**

Assume solution has FAILED CATASTROPHICALLY 6 months post-launch:

- Do not ask "Will it work?"
- Ask "How exactly did it break?" (Race conditions, cost explosion, user rejection)
- Attack solution using Phase 0 constraints
- Output: List of "Kill Shots" (Fatal Flaws) and required "Patches" (Mitigation strategies)

## Output Format

```
### 0.约束条件 (假设/给定)
...

### 1.核心模块 (帕累托Top 20%)
[模块名]: [一句话说明为何这是核心]
[模块名]: [一句话说明为何这是核心]

### 2.第一性原理真相
[模块A] [根本限制/真相]
[模块B] [根本限制/真相]

### 3.逻辑流程图
[Mermaid Code]

### 4.对齐检查

宏观: [简要生态系统适配检查]
微观: [最高风险组件的机制检查]

### 5.事前验尸 (失败检查)

* 最薄弱环节: [具体组件]
* 失败模式: [如何崩溃] -> 修复: [具体补丁]

```
## Key Principles

- **Pareto Focus** - 20% modules carry 80% weight, ignore the rest initially
- **First Principles** - Strip away conventions to find irreducible truths
- **Inversion Thinking** - Assume failure first, then work backwards
- **Visual Architecture** - Always produce Mermaid diagrams for structural clarity
- **Constraint Binding** - No constraints means MVP mode, proceed anyway

```
