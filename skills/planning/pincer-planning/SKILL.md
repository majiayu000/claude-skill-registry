---
name: pincer-planning
description: "Bidirectional planning for ambiguous or design-heavy tasks. Use when the user requests help breaking down a problem or formulating a plan, and also when an existing plan has too many gaps or needs refinement; converge top-down framing with bottom-up inventory and explicit questions."
---

# Pincer Planning

## Overview
Create a plan by pairing a top-down framing with a bottom-up inventory, stress-testing both with questions, then merging into a single, gap-checked plan. Use for design, strategy, or fuzzy scopes.

## Quick start
1) Draft top-down framing (goal, constraints, success criteria).
2) Draft bottom-up inventory (facts, assets, risks, unknowns).
3) Ask clarifying questions (use AskUser).
4) Flip perspective and refine the opposite view.
5) Merge into a single plan and list remaining gaps.

## Core Guidance
- Start with either top-down or bottom-up; explicitly label the other side as provisional.
- Ask 3–7 targeted questions that would change the plan, then wait for answers.
- After answering, re-run the opposite perspective to find contradictions or gaps.
- Converge: produce a merged plan plus a short gap list (what’s still unknown).
- Keep planning separate from execution; do not run tools during planning.

## Trust / Permissions
- **Always**: Read local files, ask clarifying questions, draft plans.
- **Ask**: Any writes to disk (e.g., saving plan.json), network calls, or execution.
- **Never**: Destructive actions or credential exfiltration.

## Resources
- `references/pincer-checklist.md`: Question prompts and convergence checks.
- `templates/plan.json`: Plan scaffold with top-down and bottom-up sections.

## Validation
- Confirm top-down and bottom-up sections converge; list explicit gaps.
- Ensure questions are answered before final plan is delivered.
