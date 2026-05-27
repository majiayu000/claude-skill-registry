---
name: dgr
description: Audit-ready decision artifacts for LLM outputs — assumptions, risks, recommendation, and review gating (schema-valid JSON).
homepage: https://www.clawhub.ai/sapenov/dgr
metadata:
  clawdbot:
    emoji: "🧭"
  category: "reasoning"
---

# DGR — Decision‑Grade Reasoning (Governance Protocol)

**Purpose:** produce an auditable, machine‑validated decision record for review and storage.

**Slug:** dgr · **Version:** 1.0.4 · **Modes:** dgr_min / dgr_full / dgr_strict · **Output:** schema-valid JSON

## What this skill does
DGR is a **reasoning governance protocol** that produces a **machine‑validated, auditable artifact** describing:
- the decision context,
- explicit assumptions and risks,
- a recommendation with rationale,
- and a consistency check.

This skill is designed for **high‑stakes** or **review‑required** decisions where you want traceability and structured review.

## How to use
1. **Ask your question** — Provide a decision request or problem context
2. **Pick mode:** `dgr_min` | `dgr_full` | `dgr_strict`
3. **Store JSON artifact** in ticket / incident / audit log

## What this skill is NOT (non‑claims)
This skill does **NOT** guarantee:
- correctness, optimality, or truth,
- elimination of hallucinations,
- legal/medical/financial advice suitability,
- or regulatory compliance by itself.

DGR improves **process quality** (clarity, traceability, reviewability) — not outcome certainty.

## When to use
Use when you need:
- an auditable record of reasoning,
- explicit assumptions/risks surfaced,
- reviewer‑friendly structure,
- a consistent output format across tasks and models.

## Inputs
- A user request/question (free text).
- Optional: context identifiers (ticket ID, policy name), and desired **mode**: `dgr_min`, `dgr_full`, or `dgr_strict`.

## Mode Behavior

| Mode | Speed | Detail Level | Clarifications | Review Required | Use Case |
|------|-------|--------------|---------------|----------------|----------|
| `dgr_min` | Fastest | Minimal compliant output | Only critical gaps | Risk-based | Quick decisions, low stakes |
| `dgr_full` | Moderate | Fuller decomposition + alternatives | More proactive | Balanced | Standard decision support |
| `dgr_strict` | Slower | Conservative analysis | More questioning | Default on ambiguity | High-stakes, uncertain contexts |

## Outputs
A single JSON artifact matching `schema.json`.

Minimum acceptance criteria (see `schema.json`):
- at least **1 assumption**
- at least **1 risk**
- `recommendation` present
- `consistency_check` present

## Safety / governance boundaries
- Always **ask for clarification** if key decision inputs are missing.
- If the decision is high‑risk, escalate via `recommendation.review_required = true`.
- If uncertainty is high, explicitly state uncertainty and limit scope.
- Do not fabricate sources or cite documents you did not see.

## Files in this skill
- `prompt.md` — operational instructions
- `schema.json` — output schema (stub aligned to DGR spec)
- `examples/*.md` — example inputs and outputs
- `field_guide.md` — how to interpret DGR artifact fields

## Quick start
1) Provide a decision request.
2) Choose a mode (`dgr_min` default).
3) The skill returns a JSON artifact suitable for review and storage.

## Changelog
**1.0.4** — Remove redundant CLAWHUB_SUMMARY.md; summary now sourced from SKILL.md front-matter.

**1.0.3** — Tighten front-matter description for better conversion, add reasoning category, compress identity block for faster scanning.

**1.0.2** — Add ClawHub front-matter metadata with emoji and homepage for improved discovery and presentation.

**1.0.0** — Initial public release of DGR skill bundle with auditable decision reasoning framework, governance protocols, and structured output format.

> Note: This is an **opt‑in** reasoning mode. It is meant to be used alongside human decision‑making, not as a replacement.
