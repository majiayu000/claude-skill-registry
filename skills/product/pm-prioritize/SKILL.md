---
name: pm-prioritize
description: Use when ranking a list of requirements, features, or backlog items using RICE / ICE / MoSCoW / Kano. Built-in decision tree picks the right framework based on data availability and decision context. Output is a transparent matrix, 2×2 Impact/Effort quadrant, and a Sprint allocation proposal. User-invoked only — do NOT auto-trigger. Triggers on "/pm-prioritize", "/prioritize", "приоритизация", "ранжируй бэклог", "RICE-анализ", "prioritize requirements", "RICE", "ICE", "MoSCoW", "Kano", "rank backlog".
---

# pm-prioritize — Rank requirements with RICE / ICE / MoSCoW / Kano

Part of the Personal Corp framework — running a one-person business through AI agents.

Rank a list of requirements using a structured framework. A built-in decision tree picks the right framework based on data availability and decision context. Output is transparent and traceable, so a team can argue with the scores instead of the recommendation.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Requirement list | yes | Name + brief description; ≥ 3 items. Can take a pain-point list from `/pm-feedback` or a feature list from `/pm-prd` |
| Framework | no | RICE / ICE / MoSCoW / Kano; auto-recommended if not given |
| Business goal | no | Current focus (growth / retention / revenue / efficiency); affects weighting |
| Resource constraint | no | Available dev capacity (person-days or Story Points) |

## Optional config

Most of the skill works out-of-box. If you want stable defaults across runs, add an `## Prioritize Config` section to your project's `CLAUDE.md`:

```markdown
## Prioritize Config

### Default framework (optional)
If unset, the skill auto-recommends per the decision table below.
- default_framework: RICE | ICE | MoSCoW | Kano

### Default resource constraint (optional)
Used in the Sprint allocation step. Skip if you'd rather state it per run.
- sprint_capacity: 20 person-days per Sprint

### Backlog source (optional)
Where the skill should fetch the requirement list from when you don't paste one.
- backlog_source: gh-issues  # gh-issues | github-project | tasks-file | paste
- gh_owner: your-github-handle
- gh_repo: your-main-repo
- gh_label: backlog
- tasks_file: docs/backlog.md
```

When a config field is set, the skill uses it silently. When unset, the skill asks (see "When input is incomplete").

## Research commands (auto-discovery)

If the user points at a backlog source instead of pasting items, the skill can pull the list itself:

```bash
# GitHub issues by label
gh issue list -R $OWNER/$REPO --label $LABEL --state open \
  --json number,title,body --limit 100

# GitHub Project items
gh project item-list $PROJECT_ID --owner $OWNER --format json

# Local backlog file
cat $TASKS_FILE
```

## Step 1 — Pick a framework

If unspecified, recommend per this decision table:

| Condition | Recommended | Why |
|---|---|---|
| Have user-impact data per item (DAU, conversion), trustworthy | **RICE** | Most quantitative, traceable |
| Have intuition but no precise data | **ICE** | Quick scoring, tolerates subjectivity |
| Need 4-bucket alignment fast (e.g. team meeting) | **MoSCoW** | Forces "must" / "won't" consensus |
| Need to understand requirement nature, plan features | **Kano** | Identifies delight features |

**Framework comparison:**

| Framework | Use case | Strength | Limit | Time |
|---|---|---|---|---|
| **RICE** | Data-supported quarterly planning | Most objective, comparable | Depends on data quality | Medium |
| **ICE** | Fast decisions, brainstorming | Simple, fast | Highly subjective | Low |
| **MoSCoW** | Release planning, stakeholder alignment | Forces consensus | Easy to put everything in Must | Low |
| **Kano** | Feature planning, satisfaction research | Identifies delighters | Needs user research data | High |

## Step 2 — Score requirements

### RICE (default)

| Dimension | Meaning | Scoring | Common error |
|---|---|---|---|
| **R**each | Users impacted in one cycle | Concrete number ("5000 users/month") | "All users theoretically" as Reach |
| **I**mpact | Per-user impact magnitude | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal | Everything gets 3 |
| **C**onfidence | Confidence in the estimate | 100% = data, 80% = indirect evidence, 50% = gut | 100% with no data |
| **E**ffort | Total person-months across all roles | Includes design + dev + QA + integration | Counting only dev |

**RICE Score = (R × I × C) / E** — higher = higher priority.

**Calibration mechanism:**
- Score the same dimension across all items first (all R, then all I) — avoids per-item anchoring bias
- R calibration: pick a baseline ("login: affects 100% of users"), score others relative
- I calibration: ≤ 50% of items can score 3 — forces differentiation
- E calibration: must include design (20%) + dev (50%) + QA (20%) + integration (10%)

### ICE (fast)

Score 1-10 on each dimension. **ICE Score = I × C × E / 10**.

| Dimension | Scoring |
|---|---|
| **I**mpact | 1 = trivial, 5 = medium, 10 = transformational |
| **C**onfidence | 1 = pure guess, 5 = indirect evidence, 10 = A/B test data |
| **E**ase | 1 = very hard (> 3 months), 5 = medium (2-4 weeks), 10 = trivial (< 1 day) |

### MoSCoW

| Bucket | Definition | Suggested share |
|---|---|---|
| **Must Have** | Without it, can't ship; users can't use core feature | ≤ 60% |
| **Should Have** | Important but has workaround; one-Sprint delay non-fatal | ~ 20% |
| **Could Have** | Nice-to-have; better with, fine without | ~ 10% |
| **Won't Have (this time)** | Explicitly out of scope; possibly later | ~ 10% |

**Common trap:** everything ends up Must Have. Counter: cap Must Have at 60%, force trade-offs.

### Kano

| Type | Trait | Detection | Strategy |
|---|---|---|---|
| **Must-be** | Absence → dissatisfaction; presence → taken for granted | Users don't ask for it but rage when missing | Reach passing grade, don't over-invest |
| **One-dimensional** | More = more satisfaction (linear) | Users actively request | Core competitive area, top-tier execution |
| **Attractive** | Absence → no dissatisfaction; presence → delight | Unexpected, evokes "wow" | Differentiator (decays to one-dimensional over years) |
| **Indifferent** | Doesn't matter either way | No user reaction | Don't invest |
| **Reverse** | Presence reduces satisfaction | Adds complexity, annoys users | Remove immediately |

**Kano decay:** today's Attractive feature becomes One-dimensional, then Must-be over 2-3 years (e.g. fingerprint unlock). Continuously create new delighters.

## Step 3 — Output ranking

**RICE results table:**

| Rank | Requirement | R | I | C | E | RICE Score | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | {name} | {n} | {0.25-3} | {50-100%} | {pm} | {score} | This cycle |

**Impact × Effort 2×2:**

| Quadrant | Impact | Effort | Strategy | Items |
|---|---|---|---|---|
| **Quick Wins** | High | Low | Do first | {list} |
| **Strategic** | High | High | Plan carefully | {list} |
| **Fill-ins** | Low | Low | When idle | {list} |
| **Avoid** | Low | High | Don't do | {list} |

**Sprint allocation:**
- Allocate per `sprint_capacity` (config) or stated resource constraint
- Quick Wins fill first; Strategic by RICE Score
- Reserve 10-20% per Sprint for unexpected work

## Step 4 — Decision log

- **Core trade-offs:** why A over B this cycle
- **Disputed items:** which ranks may be contested, and why
- **Confidence flags:** which scores have C < 80% — propose validation experiments
- **Next-cycle candidates:** Won't-Have items most likely to promote next cycle

## Quality bar

1. Every score has a one-sentence rationale
2. Effort includes design + dev + QA + integration
3. C < 80% items get "validate via small experiment" tag
4. Must Have ≤ 60% of total
5. Calibration mechanism applied to avoid anchoring

## Red lines

1. **Not a decision-maker** — output is a recommendation; the final call is the team's
2. **No hidden assumptions** — every score's assumption is explicit
3. **Never ignore Effort** — no "must do" recommendation based on Impact alone

## When input is incomplete

- **No backlog source provided** → ask: "Where is the list — paste, file path, or a GitHub issues filter (owner/repo + label or milestone)?"
- **No business goal** → ask: "Current focus this cycle — growth / retention / revenue / efficiency? Optional, but it tightens the recommendation."
- **No resource constraint** → ask: "Available capacity for the next cycle — person-days or Story Points? Optional, but needed for Sprint allocation."
- **Framework unset** → don't ask. Auto-recommend per the Step 1 decision table and propose it with a one-sentence rationale; user confirms or overrides.
- **< 3 requirements** → still rank, but flag "sample too small, add more for stability"
- **No data at all** → switch to ICE or MoSCoW; tag "qualitative ranking due to missing quantitative data"

## Related skills

- [`weekly-planning`](../weekly-planning/) — uses the ranked backlog from this skill to pick weekly OKRs / outcomes. Prioritization **feeds** OKR selection, not replaces it.
- [`weekly-retro`](../weekly-retro/) — feeds the next backlog with retro findings and carry-over items
- `/pm-user-stories` — top-priority requirements → break into Stories
- `/pm-prd` — Must-Have requirements → write PRDs