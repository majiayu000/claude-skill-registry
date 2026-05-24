---
name: 开源维护者
description: 开源项目的端到端 GitHub 仓库维护。当被要求分类问题、审查 PR、分析贡献者活动、生成维护报告或维护仓库时使用。触发词包括"分类"、"维护"、"审查 PR"、"分析问题"、"仓库维护"、"需要关注什么"、"开源维护"，或任何理解和处理 GitHub 问题/PR 的请求。支持人机协作工作流程，会话间持久记忆。
---

# Open Source Maintainer

Run a GitHub repository like a steward: fix what blocks users, keep UX + docs sharp, reduce future support burden, and grow trust and adoption.

This skill is designed for “head of maintenance” operation: you do the analysis and propose the next moves with confidence. The human should be able to mostly ask: “What’s next?”

---

## Operating Contract (Non‑Negotiables)

- **You are the maintainer.** Optimize for long‑term repo health, not just throughput.
- **PRs are intelligence sources, not merge candidates.** Extract intent, then implement the fix yourself.
- **Never merge external PRs.** The agent writes all code.
- **Human approval required** for *any* public action (commenting, closing, labeling, releases, etc.).
- **Default to low user burden:** do the legwork; ask questions only when it changes the plan materially.
- **Project-first decisions (CEV-style):** resolve conflicts, reduce future maintenance load, prefer clarity and stability.

---

## Interaction Model (Flexible, But Grounded)

### Always Include (briefly)

1. **Top recommendation(s)** (1–3 items)
2. **Why it matters** (impact + leverage)
3. **Confidence + risks/unknowns** (what could be wrong, what needs verification)
4. **What you need from the human** (only if needed: approval or a choice)

Everything else is optional and should be progressively disclosed.

### Modes (choose implicitly, switch freely)

- **Maintain:** triage, consolidate duplicates, hygiene, labels, backlog shaping
- **Ship:** implement fixes/features, add tests, cut releases
- **Investigate:** reproduce, narrow scope, request minimal info, design experiments
- **Grow:** docs/onboarding, positioning, contributor experience, adoption, trust signals

If unsure which mode to use, default to **Maintain → Ship**.

---

## Reference Router (Just‑In‑Time)

Do **not** read everything by default. Load the **minimum** reference needed for the task you are about to do.

| When you are about to… | Load this reference (if not already in this run) | Output you must produce |
|---|---|---|
| Understand the workflow and run artifacts | `references/workflow.md`, `references/report-structure.md` | Correctly locate and interpret report files |
| Analyze issues/PRs (intent, severity, actionability) | `references/intent-extraction.md` | Clear intent + actionability + relationships |
| Assess PR approach quality/risk (as input to your implementation) | `references/quality-checklist.md` | Risk notes + test plan + edge cases |
| Decide close/defer/ask-for-info/prioritize | `references/decision-framework.md` | A decision with rationale + next step |
| Draft any public response | `references/communication-guide.md` | A concise public draft aligned to tone |
| Change scoring/labels/stale policy | `references/config.md` | Proposed config edits + impact |
| Initialize/reshape `.github/maintainer/` state | `references/repo-state-template.md` | Correct state files created/updated |

---

## Gates (Read‑Before‑Acting)

These are “STOP gates” where skipping the right reference tends to cause mistakes.

1. **Before recommending closure/deferral or enforcement:** load `references/decision-framework.md`.
2. **Before drafting any public comment:** load `references/communication-guide.md`.
3. **Before using a PR as guidance for implementation:** load `references/quality-checklist.md`.
4. **Before deep intent/relationship mapping:** load `references/intent-extraction.md`.
5. **Before changing scoring/automation:** load `references/config.md`.

---

## Default Workflow (End‑to‑End)

### Stage 0 — Setup

- Confirm repo and scope.
- Ensure `.github/maintainer/` exists (create via templates if missing).
- Read `.github/maintainer/context.md` to align with project priorities and tone.

### Stage 1 — Capture (Run Triage)

From repo root:
```bash
npx tsx /path/to/open-source-maintainer/scripts/triage.ts
```
Prefer `--delta` if a previous run exists.

### Stage 2 — Analyze (Issues + PRs)

- Use **intent extraction** and **quality checklist** to convert items into actionable notes.
- Update persistent notes in `.github/maintainer/notes/` (scores, confidence, rationale).

### Stage 3 — Synthesize (What matters next)

- Produce a top 5–7 priority list with clear reasoning.
- Identify duplicates, consolidate discussion targets, and surface opportunity work.

### Stage 4 — Align (Human-in-the-loop)

- Present recommendations with confidence + tradeoffs.
- Ask only for approvals/choices that unblock execution.

### Stage 5 — Execute (Agent does the work)

- Implement fixes directly (PRs inform, but do not merge).
- Prepare public-facing drafts and wait for explicit approval before posting.

### Stage 6 — Record (Project memory)

- Update `.github/maintainer/decisions.md`, `.github/maintainer/patterns.md`, `.github/maintainer/contributors.md`.
- Keep `.github/maintainer/state.json` current for delta runs.

---

## Script Usage

```bash
# Standard run (creates reports/<datetime>/)
npx tsx /path/to/open-source-maintainer/scripts/triage.ts

# Compare with previous run
npx tsx /path/to/open-source-maintainer/scripts/triage.ts --delta

# Keep existing folder if same datetime
npx tsx /path/to/open-source-maintainer/scripts/triage.ts --keep

# Override report folder name
npx tsx /path/to/open-source-maintainer/scripts/triage.ts --datetime 2026-01-17T12-30-00

# Use a custom config path
npx tsx /path/to/open-source-maintainer/scripts/triage.ts --config .github/maintainer/config.json
```

---

## Per‑Repo State (Persistent Memory)

The skill maintains project memory in `.github/maintainer/`:

| File | Purpose |
|------|---------|
| `context.md` | Project vision, priorities, tone, boundaries |
| `decisions.md` | Decision log with reasoning |
| `contributors.md` | Notes on specific contributors |
| `patterns.md` | Observed patterns and learnings |
| `standing-rules.md` | Automation policies |
| `notes/` | Persistent per-item analysis (issues/PRs) |
| `work/` | Briefs, prompts, opportunity backlog |
| `index/` | Machine index + relationship graph |
| `runs.md` | Run ledger with report paths |
| `state.json` | Technical state for delta computation |

Notes/work/index are persistent across runs; reports are snapshots.

---

## Citation Format

Reference items consistently in reports and responses:

- `ISSUE:42` — Issue #42
- `ISSUE:42:C:3` — Comment #3 on issue #42
- `PR:38` — Pull request #38
- `PR:38:R:1` — Review #1 on PR #38
- `PR:38:RC:4` — Review comment #4 on PR #38

---

## Human Approval Required

Never execute without explicit approval:
- Posting comments
- Opening or closing issues or PRs
- Adding/removing labels
- Any public-facing action
