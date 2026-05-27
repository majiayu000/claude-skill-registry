---
name: codebase-audit
description: "全面代码库审计 — 自适应并行深度分析（前后端契约、数据完整性、异常处理/安全、架构/技术债、配置/缓存），输出按严重程度排序的统一报告和修复路线图。Use when user asks to audit, analyze, or review an entire codebase for design issues, find hidden bugs, check architecture health, or asks '全面审查', '代码库审计', '分析设计问题', 'audit codebase', 'health check', '有哪些问题'. Also trigger when user asks to find silent degradation, data flow breakpoints, type mismatches between frontend and backend, or wants to understand technical debt across a project."
---

# Codebase Audit — Adaptive Deep Analysis

A comprehensive codebase audit that adapts its agent configuration to the project's tech stack. Each agent uses opus for maximum thoroughness. Results are compiled into a unified report sorted by severity with a phased repair roadmap.

## Core Principles

1. **Opus only** — All audit agents MUST use `model="opus"`. This is non-negotiable. Smaller models miss subtle cross-file issues.
2. **Depth over breadth** — Fewer agents with broader scope and deeper analysis beats many shallow agents. Each agent should trace issues across file boundaries.
3. **Adaptive** — Agent count and focus areas vary by project type. Don't waste an agent on "frontend rendering" for a backend-only project.

## When to Use

- User asks to audit/review/analyze an entire codebase
- User wants to find hidden bugs, silent degradation, or design inconsistencies
- User asks about technical debt, architecture health, or "what's broken"
- Before a major refactor or after inheriting an unfamiliar codebase
- Periodic health check (monthly/quarterly)

## Workflow

### Phase 0: Tech Stack Detection

Detect the project's tech stack to determine the agent configuration:

```
Detection checklist:
- package.json / tsconfig.json → TypeScript/JavaScript (React, Next.js, Vue, etc.)
- pyproject.toml / requirements.txt / setup.py → Python (FastAPI, Django, Pydantic, etc.)
- Cargo.toml → Rust (serde, axum, actix, etc.)
- go.mod → Go (gin, echo, gorm, etc.)
- Multiple stacks → Full-stack project (frontend + backend)
```

### Phase 1: Launch Agents (Adaptive)

Based on the detected stack, choose the appropriate agent configuration below. Launch ALL agents in a SINGLE message with `model="opus"` for every agent.

Read `references/agent-prompts.md` for complete prompt templates.

---

#### Full-Stack Projects (5 agents)

When both frontend and backend exist (e.g., React + FastAPI, Next.js + Go).

| # | Agent | Type | Scope (merged dimensions) |
|---|-------|------|---------------------------|
| 1 | **Frontend-Backend Contract** | `reviewer` | Type consistency (field names, types, missing fields) + Rendering pipeline (layout/block/card routing completeness, dead slots, unrendered fields) + Serialization boundaries (models that silently drop fields). This agent reads BOTH sides and traces data across the API boundary. |
| 2 | **Data Integrity & Flow** | `code-reviewer` | Data pipeline end-to-end: from input through every transformation layer to output. Covers: field resolver filters, serialization/deserialization, model_validate/model_dump, cache read/write symmetry. Finds where fields get silently dropped. Also covers: declaration-execution gaps (registered but unwired handlers, enum without config). |
| 3 | **Error Handling & Security** | `security-reviewer` | Exception patterns (bare except, debug-level errors, warning+fallback), security (hardcoded secrets, injection, unsafe deserialization), silent degradation (error paths that produce user-visible wrong output instead of failing). |
| 4 | **Architecture & Code Quality** | `architect` | Layer violations, circular dependencies, god objects (files >800 lines), code duplication (parallel systems, scattered mapping tables), extension cost analysis (how many files to add a new type), DI pattern consistency. |
| 5 | **Config & Persistence** | `database-reviewer` | Config completeness (template/schema vs code expectations, conflicting defaults), cache key completeness (missing code version dimension), DB schema consistency, temp file cleanup, state persistence across restarts. |

---

#### Backend-Only Projects (4 agents)

When only backend exists (Python API, Rust service, Go microservice, etc.)

| # | Agent | Type | Scope |
|---|-------|------|-------|
| 1 | **API Contract & Data Integrity** | `code-reviewer` | API schema vs internal models, serialization boundaries, data pipeline tracing, field dropping, declaration-execution gaps. |
| 2 | **Error Handling & Security** | `security-reviewer` | Same as full-stack Agent 3. |
| 3 | **Architecture & Code Quality** | `architect` | Same as full-stack Agent 4. |
| 4 | **Config & Persistence** | `database-reviewer` | Same as full-stack Agent 5. |

---

#### Frontend-Only Projects (3 agents)

When only frontend exists (React SPA, Vue app, etc.)

| # | Agent | Type | Scope |
|---|-------|------|-------|
| 1 | **Component Architecture & Rendering** | `reviewer` | Type routing completeness, component registration gaps, dead props/slots, state management consistency, API consumption patterns. |
| 2 | **Error Handling & Code Quality** | `code-reviewer` | Unhandled promise rejections, error boundaries, catch-and-ignore patterns, god components, code duplication. |
| 3 | **Config & Build** | `reviewer` | Build config consistency, env variable management, bundle analysis, dead dependencies. |

---

### Phase 2: Compile Unified Report

After ALL agents complete, compile findings into a single report:

```markdown
# [Project Name] Codebase Audit Report

> Audit date: YYYY-MM-DD
> Target: path
> Tech stack: detected stack
> Agents: N (list agent names)

## Summary
| Level | Count | Key Areas |
|-------|-------|-----------|
| Critical | N | ... |
| High/P1 | N | ... |
| Medium/P2 | N | ... |

## Critical (Fix Immediately)
| # | Problem | Agent | Impact |
|---|---------|-------|--------|
For each: file:line, code snippet, risk description, fix suggestion.

## High / P1 (Fix This Week)
### [Category]
| # | Problem | File(s) |
|---|---------|---------|
Details for each.

## Medium / P2 (Plan to Fix)
[Same structure]

## Repair Roadmap
| Phase | Scope | Est. Files |
|-------|-------|------------|
| Phase 0 (urgent) | Critical fixes | ~N files |
| Phase 1 (this week) | High priority | ~N files |
| Phase 2 (next week) | Medium priority | ~N files |
| Phase 3 (ongoing) | Architecture | ~N files |
```

### Deduplication

Since agents have broader overlapping scopes, deduplication is simpler:
- Same file + same line → merge
- Same root cause found by multiple agents → keep the most detailed one, note cross-agent confirmation (this actually increases confidence)
- Severity conflicts → use the highest

### Severity Classification

| Level | Criteria |
|-------|----------|
| **Critical** | Data loss, rendering failure, security vulnerability, complete feature breakage affecting users NOW |
| **High/P1** | Silent degradation (user sees wrong/incomplete output), type mismatches causing data truncation, missing config causing empty output, architectural violations blocking development |
| **Medium/P2** | Code duplication, inconsistent patterns, suboptimal error handling, tech debt that slows development but doesn't break features |

## Stack-Specific Patterns

Read `references/stack-patterns.md` for technology-specific search patterns.
