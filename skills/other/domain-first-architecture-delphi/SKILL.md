---
name: domain-first-architecture-delphi
description: Use when architecture feels component-based but ownership is split across technical buckets (tables/init/debug), causing god files, duplicate paths, and hidden dependency flow.
---

# Domain-First Architecture Delphi

## Overview

Use Delphi to expose one specific structural failure: the code claims domain modeling, but ownership is organized by technical buckets (all tables together, all init together, all debug together).

This skill does **not** ask “what files are big?” It asks:
1. What is the canonical path per concept?
2. Where are alternate paths?
3. Which alternates are duplicates vs diverged behavior?
4. What is the minimum replace→wire→delete sequence?

**REQUIRED SUB-SKILL:** `delphi`

---

## Use This Skill When

Use when 2+ are true:
- A single file defines many domains (or 1000+ lines with unrelated ownership).
- Init logic for multiple domains is fused into one orchestration block.
- Adding one domain feature touches 4+ files across 3+ directories.
- You see repeated “must match X in Y” comments.
- You suspect multiple sources of truth for one concept.
- You need ticketable seams, not generic “refactor” advice.

Do **not** use for style cleanup, naming cleanup, or lint-only reviews.

---

## Required Artifacts (Non-Negotiable)

Every run must produce these artifacts.

### 1) Concept Inventory

| Concept | Canonical Path | Alternate Paths Found | Divergence Type | Evidence |
|---|---|---|---|---|

Divergence types:
- `DUP_PATH` — copy of same logic
- `DIVERGENT_PATH` — same concept with behavior drift
- `MULTI_SOURCE` — multiple sources of truth
- `LAYER_MISMATCH` — ownership split by layer bucket
- `HIDDEN_DAG` — init dependency exists but not explicit

### 2) Architectural Mismatch Matrix

| Domain | Schema Owner | Init Owner | Runtime Owner | Debug Owner | Files Touched for One Change | Mismatch | Severity |
|---|---|---|---|---|---:|---|---|

### 3) Init Dependency DAG (with payloads)

Must include data carried by each edge, not just control flow.

Example:
```text
spawn_planets -> planet_entity_ids
planet_entity_ids -> seed_markets
planet_entity_ids -> spawn_npcs
```

### 4) Replace→Wire→Delete Map (per finding)

```text
Replace: old_fn_a, old_fn_b
Wire: callers X/Y/Z -> canonical_fn
Delete: old_fn_a, old_fn_b after verification
```

No map = no actionable finding.

---

## Process

### Phase 0 — RED Baseline (Before Guidance)

Run 3 workers without this skill prompt. Force scenario tasks:
1. Planet feature change crossing map+zone+market
2. Ship/module change crossing spawn+tactics+loot
3. NPC debug command + trace change

Record:
- Files touched
- Dirs touched
- Cross-layer hops
- Worker rationalizations (verbatim)

### Phase 1 — Parallel Delphi Lenses

Run 5 workers in parallel using `worker-prompts.md`:
- Domain ownership mismatch
- Change-coupling / friction
- Init DAG extraction
- False-constraint audit (framework myths vs real constraints)
- Safe seam extraction

### Phase 2 — Synthesis

Merge findings into the 4 required artifacts.
Reject any finding lacking file/symbol evidence.

### Phase 3 — Ticketization

Create:
1. One synthesis ticket
2. One ticket per P0/P1 finding

Each ticket must contain:
- Goal
- Exact seam boundary
- First move-only step
- Acceptance criteria
- Verification commands
- Dependencies

---

## Scoring Rules

Per finding:
- Severity: `P0 | P1 | P2`
- Friction score: `files_touched + (dirs_touched * 2) + (cross_layer_hops * 3)`
- Blast radius: `low | medium | high`
- Confidence: `high | medium | low`
- Evidence: `file + symbol + line range`

If score or evidence is missing, drop the finding.

---

## Guardrails

- Do not propose “lint rules” as primary solution for semantic duplication.
- Do not substitute PR process templates for architectural detection.
- Do not open with monolithic rewrites.
- Start with move-only splits + re-exports, then extraction, then behavior changes.
- Re-run concept inventory after each stage and compare deltas.

Success means alternate paths shrink and divergence labels resolve.
