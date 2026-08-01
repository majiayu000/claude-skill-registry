---
name: kai-growth-plan
description: Generate a stage-appropriate marketing plan based on your company's MRR/stage. Uses the marketing-by-stage playbook to tell you exactly what to do (and what NOT to do) at pre-launch, early ($0-10K MRR), growth ($10-100K MRR), or scale ($100K+ MRR). Use when "what should I do for marketing", "growth plan", "marketing plan", "I just raised a round", "marketing strategy", "what's the right marketing for my stage", "GTM strategy", or any request for a stage-appropriate marketing roadmap.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A marketing plan the founder can start executing on Monday, matched to the company's actual stage — so that effort goes to the constraint that is currently binding growth rather than to the tactic that is currently fashionable. The plan names what to do, what to deliberately not do, which growth loop to build, and what to measure.

The wrong strategy at the right stage wastes money. Stage diagnosis is the load-bearing judgment in this skill.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`).

- **E3** — a named human approved the exact plan document.
- **C3** — the plan clears `banned_word_check`, and someone other than its author read it end to end.
- **O1** — every P0 recommendation names the metric it targets, with a baseline, a threshold, and an owner. A plan whose first work item has no metric is not finished.

A plan nobody executes is not CLOSED. Its outcome is `plan_adopted` / `first_action_shipped`, read at 30 days.

## Constraints

- **Stage first.** Do not produce recommendations before diagnosing stage from revenue, retention, team, and current channels. A plan built on an assumed stage is worse than no plan.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft. Do not open with discovery questions the repo can answer.
- **Provenance.** Any quantitative or client-facing claim — benchmarks, CAC, conversion rates, competitor traffic, market size — runs through the collector first and cites a source. Missing data is a data gap, never a benchmark. See `harness/references/audit-data-provenance.md`.
- **Anti-patterns are mandatory output, not a bonus.** What not to do at this stage is the half of the plan that saves money.
- **KaiCalls fit logic applies** when the business appears phone-led. Disclose the ownership relationship, compare alternatives, and do not lead with it when phone demand is low or the workflow is self-serve by design.
- **No spend commitments.** Budget allocation is a recommendation; it does not authorize spend.

## Context

| Need | Load |
|---|---|
| Stage definitions and stage-specific moves | `knowledge/playbooks/marketing-by-stage.md` |
| Which growth loop fits the product | `knowledge/playbooks/growth-loops-applied.md` |
| Demand generation mechanics | `knowledge/playbooks/demand-generation.md` |
| Metrics that matter per stage | `knowledge/playbooks/saas-metrics-guide.md` |
| Distribution, first growth hire, channel coverage | `knowledge/playbooks/growth-hacker-first-hire-os.md` |
| Budget frameworks | `knowledge/playbooks/marketing-budget-forecasting.md` |
| Which framework governs a conflict | `knowledge/_arbitration.md` + `knowledge/frameworks/marketing-science/diagnosis-first-operating-order.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Stage map** — the one table worth carrying inline, because it anchors every downstream call:

| Stage | Revenue | Goal | Marketing mode |
|-------|---------|------|----------------|
| Pre-Launch | $0 | Validate demand | Talk to humans, build waitlist |
| Early | $0–$10K MRR | Find PMF + first channel | Manual, unscalable, learn what works |
| Growth | $10K–$100K MRR | Optimize + expand channels | Systematize what works, test new channels |
| Scale | $100K+ MRR | Systematize + build team | Hire, automate, diversify |

**Output** goes to `workspace/growth-plan/`: stage assessment, 90-day plan, budget allocation, metrics dashboard, skill routing, anti-patterns. Same paths as v1 — downstream tooling does not branch on version.

**Routing.** The plan should end by naming which `/kai` skills execute it and when. This skill identifies which growth loop to build; it does not design the loop.

## Escalate when

- Revenue, retention, or channel data is unavailable and the stage cannot be diagnosed — say so rather than guessing a stage.
- The user's stated stage conflicts with their numbers.
- The plan would require spend the user has not authorized.
- The business is in a regulated category where the obvious channel recommendation carries compliance risk.
- Two loaded frameworks give conflicting guidance and `knowledge/_arbitration.md` does not resolve it.
