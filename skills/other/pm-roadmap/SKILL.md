---
name: pm-roadmap
description: Сводит статус итерации, оценивает прогресс milestones, фиксирует изменения приоритетов, отслеживает зависимости и выдаёт roadmap в формате Now/Next/Later с атрибуцией задержек по 5 причинам, health score и фреймворком обрезки scope при нехватке ресурсов. User-invoked only — do NOT auto-trigger. Triggers on /pm-roadmap, "обнови roadmap", "статус спринта", "анализ задержек", "update roadmap", "sprint status", "milestone progress", "delay analysis".
---

# pm-roadmap — Roadmap update


Part of the Personal Corp framework — running a one-person business through AI agents.
Aggregate current iteration status, evaluate milestone progress, track priority changes and dependencies, output a roadmap status overview and planning suggestions.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Iteration status | yes | Current Sprint task list and statuses (manual or pulled from PM tool) |
| Roadmap horizon | no | Quarter / half / year; default quarter |
| Changes | no | Items needing priority or timeline adjustment + reason |
| Dependencies | no | Cross-team / tech dependencies and current state |

## Step 1 — Get current state

If a PM tool integration is available, pull the current Sprint task list and bucket by status. Otherwise ask the user for the list in any format (table, screenshot, verbal).

## Step 2 — Iteration status summary

| Field | Value |
|---|---|
| Sprint name / period | {Sprint X / date range} |
| Planned tasks | {N} |
| Done | {X} ({X/N%}) |
| In progress | {Y} |
| Not started | {Z} |
| Blocked / delayed | {W} |
| Estimated on-time delivery | {%} |

**Delayed-task analysis:**

| Task | Original due | New ETA | Reason | Milestone impact |
|---|---|---|---|---|
| {task} | {date} | {date} | {cause} | yes/no |

**Five-cause delay attribution:**

| Cause | Pattern | Improvement |
|---|---|---|
| **Scope change** | Mid-development requirement edits, scope creep | Strengthen requirement freeze; route changes through approval |
| **Estimation gap** | Actual effort far exceeds estimate | Calibrate from history, add buffer |
| **Tech risk** | Approach proves infeasible, perf wall, tech debt blocking | Pre-development tech-spike phase |
| **Dependency block** | Waiting on another team / third party / approval | 2-week-ahead dependency early-warning |
| **Headcount change** | PTO, attrition, redirected | 20% capacity buffer in planning |

If the same root cause appears 3+ times, escalate to a process-improvement item.

## Step 3 — Milestone progress

| Milestone | Target date | Key deliverable | Progress | Status | Risks |
|---|---|---|---|---|---|
| {M1} | {date} | {deliverable} | {X%} | On-time / at-risk / delayed | {risk} |

**Status criteria:**
- **On-time:** progress ≥ time elapsed; no blocking deps
- **At-risk:** progress slightly behind, or unresolved dependency
- **Delayed:** progress significantly behind, or critical dependency blocked

## Step 4 — Priority change log

| Item | Change | Old priority | New priority | Reason | Impact |
|---|---|---|---|---|---|
| {item} | Up / down / new / removed | {P0/P1/P2} | {P0/P1/P2} | {reason} | {scope} |

**Change-reason categories:**
- User-feedback driven (from `/pm-feedback`)
- Competitor driven (from `/pm-competitive`)
- Data driven (from `/pm-metrics`)
- Resource change (team capacity, tech approach change)
- External (compliance, partner ask)

## Step 5 — Dependency tracking

| Dependency | Type | Owner / consumer | Need-by | State | Risk |
|---|---|---|---|---|---|
| {desc} | Tech / team / external | {who depends on whom} | {date} | Resolved / in progress / blocked | High / medium / low |

**Dependency types:**
- **Tech:** infrastructure, APIs, services
- **Cross-team:** other product lines, design, data team
- **External:** third-party services, partners, approval flows

## Step 6 — Forward-looking plan

Recommend the next 2-3 iterations.

**Now / Next / Later view:**

| Horizon | Items | Priority | Confidence | Dependencies |
|---|---|---|---|---|
| **Now** (current iteration) | {in-flight work} | Locked | High | {resolved} |
| **Next** (1-2 iterations out) | {planned work} | Locked / TBD | Medium-high | {to follow up} |
| **Later** (3+ iterations out) | {directional plans} | Directional | Low-medium | {to evaluate} |

**Capacity assessment:**
- Available capacity next iteration: {X} person-days
- Allocation suggestion: 70% planned features + 20% tech debt + 10% buffer
- Given current delays, prioritize next: {list}

**Roadmap health score:**

| Dimension | Weight | Scoring | Score |
|---|---|---|---|
| On-time delivery rate | 30% | > 80% = 5, 60-80% = 3, < 60% = 1 | {X} |
| Scope stability | 20% | Change < 10% = 5, 10-30% = 3, > 30% = 1 | {X} |
| Dependency resolution | 20% | > 90% = 5, 70-90% = 3, < 70% = 1 | {X} |
| OKR alignment | 15% | All work traces to OKR = 5 | {X} |
| Team confidence | 15% | Team confident on timely delivery = 5 | {X} |

**Composite:** weighted total ≥ 4 healthy / 3-4 at-risk / < 3 needs urgent action.

**Feature-cut decision framework (when capacity is short):**

| Cut first | Reason | Condition |
|---|---|---|
| Nice-to-have | Doesn't affect core value | Cut directly |
| Splittable feature's second half | MVP-first | Confirm MVP standalone usable |
| Polish / perfectionism | Functional > perfect | No irreversible tech debt introduced |
| Low-confidence requirements | Unvalidated hypotheses | Tag "deferred for validation" |

**Principle:** cut scope > delay > add people (Brooks's Law: adding people to a late project makes it later).

## Step 7 — Output report

```markdown
# Roadmap Update

**Date:** {date}
**Horizon:** {quarter / half}
**Current iteration:** {Sprint name / dates}

## 1. Current Iteration Status
Completion rate: {X%} ({done}/{total})
Blockers: {N}

## 2. Milestone Progress
| Milestone | Target | Progress | Status |
|---|---|---|---|

## 3. Priority Changes
| Item | Change | Reason |
|---|---|---|

## 4. Dependencies & Risks
- High-risk dependencies: {desc}
- Coordination needed: {desc}

## 5. Roadmap (Now / Next / Later)
(table)

## 6. Next-Step Recommendations
1. {recommendation 1}
2. {recommendation 2}
3. {recommendation 3}
```

## Quality bar

1. Status info accurate — delayed tasks have specific cause + new ETA
2. Milestone evaluation evidenced — no "almost done" / "soon"
3. Changes traceable — every priority change records reason and decider
4. Risks raised proactively — not waiting for blow-up to report
5. Recommendations actionable — owner-assignable
6. Health score tracked over time to observe improvement trend

## Roadmap-communication guide

Different audiences need different granularity:

| Audience | Focus | Format | Cadence |
|---|---|---|---|
| **CEO / VP** | Strategy, milestones, risks | Now/Next/Later high-level | Monthly |
| **Engineering** | Sprint tasks, deps, tech detail | Detailed task list + dep graph | Daily / weekly |
| **Sales / CS** | Customer-promised features, ETAs | Feature timeline | Monthly |
| **External customers** | Upcoming capabilities | Quarterly themes (no dates) | Quarterly |

**Three rules:**
1. Don't promise specific dates externally — promise "Q2", not "April 15"
2. Don't hide delays — early bad news beats late bad news
3. Don't treat the roadmap as a contract — plans change

## Red lines

1. **No hidden delays** — report delays honestly
2. **No false promises** — don't be over-optimistic on future timelines
3. **No ignored dependencies** — cross-team dependencies are tracked explicitly

## When input is incomplete

- **No task list** → ask for at least milestones + key deliverables status
- **No priority changes recorded** → output current state only, tag "recommend logging changes"
- **First use, no history** → help build the baseline framework

## Related skills

- `/pm-prioritize` — re-rank items in the roadmap
- `/pm-metrics` — metric review feeds roadmap adjustments
- `/pm-brainstorm` — explore innovation directions for the Later column

