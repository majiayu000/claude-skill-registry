---
version: 4.1.0-fractal
name: design-orchestration
description: >
  Orchestrates design workflows by routing work through
  brainstorming, multi-agent review, and execution readiness
  in the correct order. Prevents premature implementation,
  skipped validation, and unreviewed high-risk designs.
---

# Design Orchestration (Meta-Skill)

## Purpose

Ensure that **ideas become designs**, **designs are reviewed**, and
**only validated designs reach implementation**.

This skill does not generate designs.
It **controls the flow between other skills**.

---

## Operating Model

This is a **routing and enforcement skill**, not a creative one.

It decides:
- which skill must run next
- whether escalation is required
- whether execution is permitted

---

## Controlled Skills

This meta-skill coordinates the following:

- `brainstorming` — design generation
- `multi-agent-brainstorming` — design validation
- downstream implementation or planning skills

---

## Entry Conditions

Invoke this skill when:
- a user proposes a new feature, system, or change
- a design decision carries meaningful risk
- correctness matters more than speed

---

## Routing Logic

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Step 1 — Brainstorming (Mandatory)](./sub-skills/step-1-brainstorming-mandatory.md)
### 2. [Step 2 — Risk Assessment](./sub-skills/step-2-risk-assessment.md)
### 3. [Step 3 — Conditional Escalation](./sub-skills/step-3-conditional-escalation.md)
### 4. [Step 4 — Multi-Agent Review (If Invoked)](./sub-skills/step-4-multi-agent-review-if-invoked.md)
### 5. [Step 5 — Execution Readiness Check](./sub-skills/step-5-execution-readiness-check.md)
