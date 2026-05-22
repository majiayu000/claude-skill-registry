---
name: workflow-feature-shipper
description: "Use when you need to ship a single PR-sized feature end-to-end (plan -> implement -> verify) with artifacts. Ship core product features quickly in a Next.js codebase: turn a feature idea into an executable plan, implement in PR-sized slices, and keep artifacts under runs/ (or OpenSpec changes/ when available). Supports plan-only mode for early scoping. For prototype UI work, include a demo-ready wow moment (animation/micro-interaction) by default unless user opts out."
---

# Feature Shipper

Turn "I want to build a feature" into a fast execution chain.

## Input (Pass Paths Only)

- `feature.md`: Requirements description (acceptance criteria + non-goals)
- `repo_root`
- `run_dir`

### Optional flags (recommended inside `feature.md`)

- `mode`: `plan-only` | `execute` (default: `execute`)
- `feature_slug`: short slug for artifact naming (default: derived from title + timestamp)
- `quality_bar`: `demo-ready` | `functional-only` (default: `demo-ready` for user-facing UI features)

## Output (Persisted)

- `evidence/features/<feature_slug>-plan.md` (checklist plan: tasks + verification)
- `evidence/parallel/features/<feature_slug>/` (if implementation is split)
- `evidence/features/<feature_slug>-summary.md`

## Process

0. Hooks doctor (required check; non-blocking): Run `tool-hooks-doctor` once at the start of the session to verify `skill-evolution` hooks are enabled. If missing, offer to install project-level hooks; continue either way.
1. Read `feature.md`, normalize into: acceptance criteria, boundaries, risks, rollback.
2. **Prototype UI rule (default)**: if this feature affects user-facing UI and `quality_bar` isn’t `functional-only`, propose 1 “demo moment” (animation/micro-interaction) and add it to acceptance criteria. Must respect `prefers-reduced-motion`.
3. Produce 2 options (A: minimal; B: cleaner but slower), default to A. If user cares about “demo feel”, offer A-demo-ready vs A-functional-only as explicit sub-options.
4. Split into PR-sized small steps (each independently runnable + rollback-able).
5. Write plan to `evidence/features/<feature_slug>-plan.md`.
6. If `mode: plan-only`, stop here and ask for confirmation before implementing.
7. Implement (batch execution + checkpoints):
    - UI visual/layout/animation changes → First call `tool-design-style-selector` to load the project’s `design-system.md`, then strictly follow it. If `tool-ui-ux-pro-max` is installed, use it to ground motion/UX constraints (search “animation” + “accessibility”). For complex visual/animation/responsive design, delegate to `/gemini` frontend UI/UX senior design agent.
    - Business logic/data flow/integration → Implement directly.
    - **Default batch rhythm**: 3 small tasks per batch → run verification → report and wait for feedback; stop immediately for help when blocked/verification fails.
    - After each batch (or before merge), recommend using `review-quality` for a conclusive review + verdict.
      - `review-quality` is the single entry point and will auto-triage: if React/Next.js performance risk is detected, it will also run `review-react-best-practices`.
      - If the user explicitly wants *only* a React/Next.js perf audit, run `review-react-best-practices` directly.
8. Verification: can run, can build (and existing tests pass).
   - If verification fails (tests/build/runtime error): run `tool-systematic-debugging` before attempting more fixes.
   - Persist debugging artifacts to:
     - `evidence/features/<feature_slug>-debug.md` (repro steps, hypotheses, root cause, fix + re-verify)
9. Write `evidence/features/<feature_slug>-summary.md`: what was done, how verified, next steps.
10. Wrap up: Do a `skill-evolution` **Evolution checkpoint** (3 questions); if user chooses "want to optimize", run `skill-improver` based on this `run_dir` to produce minimal patch suggestions

## Delivery Requirements

- No "big bang" refactoring
- Don't introduce new complexity (unless it significantly reduces future cost, and user confirms)
