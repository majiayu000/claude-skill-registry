---
name: plot
description: >-
  Git-native planning dispatcher. Analyzes current git state and suggests the next action.
  Activates on /plot or when managing planned work through git branches and PRs.
  Spoke commands: /plot-idea, /plot-approve, /plot-deliver, /plot-release, /plot-sprint.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git. Currently uses gh CLI for forge operations, but the workflow works with any git host that supports pull request review.
---

# Plot

Lean, git-native planning system. Plans are markdown files on branches, PRs are workflow metadata, git is the source of truth. Plans merge to main before implementation begins; one plan can spawn multiple parallel implementation branches. Works with any team composition — human, AI-assisted, or fully agentic.

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Active index:** docs/plans/active/
    - **Delivered index:** docs/plans/delivered/
    - **Sprint directory:** docs/sprints/

## Model Guidance

| Steps | Min. Tier | Notes |
|-------|-----------|-------|
| 1. Read State | Small | Git/gh commands, file listing |
| 2. Detect Context | Small | Branch name pattern matching |
| 3. Detect Issues | Small (most), Mid (overlap) | Overlapping plans (3+ shared words) needs mid-tier |
| 4. Status Summary | Small | Template formatting |
| Sprint listing | Small | File listing, date arithmetic |
| Sprint countdown | Small | Date comparison, checkbox counting |

All dispatcher steps are mechanical except the "Overlapping plans" heuristic in step 3, which requires comparing plan titles. A small model should skip title comparison and only flag exact slug duplicates.

## Lifecycle

### Feature / Bug (full lifecycle)

```mermaid
flowchart LR
    subgraph Planning
        A["/plot-idea"] -->|draft PR| B["Refine &<br/>slice branches"]
        B -->|"⏳ gh pr ready"| C["Review plan"]
    end
    subgraph Approval
        C -->|"⏳ /plot-approve<br/>(or PR already merged)"| D["Plan merged<br/>impl PRs created"]
    end
    subgraph Implementation
        D -->|"⚡ create branches"| E["Work on<br/>impl branches"]
        E -->|"⏸ draft → review → merge<br/>(standard code review)"| F["All impls<br/>merged to main"]
    end
    subgraph Delivery
        F -->|"⚡ /plot-deliver"| G["Plan delivered"]
    end
    subgraph Release
        G -->|"⚡ /plot-release rc"| H["RC tag +<br/>checklist"]
        H -->|"⏸ endgame testing"| I{"All verified?"}
        I -->|"no: fix → new RC"| H
        I -->|"⏳ sign-off"| J["⚡ /plot-release"]
    end
```

Legend: ⚡ automate ASAP · ⏸ natural pause · ⏳ human-paced

### Docs / Infra (live when merged)

```mermaid
flowchart LR
    A["/plot-idea<br/>(optional)"] -->|draft PR| B["Refine plan"]
    B -->|"/plot-approve<br/>(if planned)"| C["Impl branch"]
    C -->|"code review<br/>& merge"| D["Merged to main<br/>LIVE"]
    D -->|"/plot-deliver<br/>(if planned)"| E["Plan delivered"]

    F["Direct branch<br/>(no plan)"] -->|"code review<br/>& merge"| D
```

### Sprint Lifecycle

```mermaid
flowchart LR
    A["/plot-sprint<br/><slug>: <goal>"] -->|"⏸ drafting"| B["Planning"]
    B -->|"⏳ /plot-sprint commit"| C["Committed"]
    C -->|"⚡ /plot-sprint start"| D["Active"]
    D -->|"⏳ /plot-sprint close"| E["Closed"]
```

Sprints are an optional temporal lens over plans. Sprint files live in `docs/sprints/`, committed directly to main. See `/plot-sprint` for full details.

### Direct Work (no planning step)

Small features, bug fixes, docs, and infra tasks go directly to a PR:

```
feature/<slug>  →  PR  →  merge
bug/<slug>      →  PR  →  merge
docs/<slug>     →  PR  →  merge
infra/<slug>    →  PR  →  merge
```

## Phases

### Plan Phases

| Phase | Meaning | Trigger | Transition Pacing |
|-------|---------|---------|-------------------|
| Draft | Plan being written/refined | `/plot-idea` | ⏸ natural pause (writing) |
| Approved | Plan merged, impl branches created | `/plot-approve` | ⏳ human-paced (review) → ⚡ automate (branch creation) |
| Delivered | All impl PRs merged, plan delivered | `/plot-deliver` | ⏸ natural pause (implementation) → ⚡ automate (delivery) |
| Released | Included in a versioned release | `/plot-release` | ⚡ automate (RC tag) → ⏸ endgame → ⏳ sign-off → ⏳ human-paced (version bump, tag, push) |

The Release phase includes an RC verification loop. Individual plans don't track a "Testing" phase — the release checklist does. See the Pacing section in the manifesto for details.

### Sprint Phases

| Phase | Meaning | Trigger | Transition Pacing |
|-------|---------|---------|-------------------|
| Planning | Sprint being drafted, items selected | `/plot-sprint <slug>: <goal>` | ⏸ natural pause (drafting) |
| Committed | Team agreed on sprint contents | `/plot-sprint <slug> commit` | ⏳ human-paced (agreement) |
| Active | Sprint running, work in progress | `/plot-sprint <slug> start` | ⚡ automate ASAP |
| Closed | Timebox ended, retro captured | `/plot-sprint <slug> close` | ⏳ human-paced (retrospective) |

## Conventions

- **Branch prefixes:** `idea/` (plans), `feature/`, `bug/`, `docs/`, `infra/` (implementation)
- **Plan files:** `docs/plans/YYYY-MM-DD-<slug>.md` — date-prefixed, never move once created
- **Active index:** `docs/plans/active/<slug>.md` — symlinks to Draft/Approved plans
- **Delivered index:** `docs/plans/delivered/<slug>.md` — symlinks to Delivered plans
- **Plan PR:** starts as draft (being refined), marked ready with `gh pr ready`, titled `Plan: <title>`
- **Impl PRs:** draft, created by `/plot-approve`, reference the plan on main
- **Sprint files:** `docs/sprints/YYYY-Www-<slug>.md` — ISO week-prefixed, committed directly to main
- **Sprint active index:** `docs/sprints/active/<slug>.md` — symlinks to active sprints

## Guardrails

- `/plot-approve` requires plan PR to be non-draft or already merged — no approving unreviewed plans
- `/plot-deliver` requires all impl PRs merged — no premature delivery
- `/plot-release` requires delivered plans — cannot release undelivered work; verifies readiness but does not execute release steps without user confirmation
- `/plot` detects orphan impl branches (no approved plan) — prevents coding without context
- Phase field in plan files is machine-readable — every command checks current phase before acting

## Dispatcher

The `/plot` command analyzes current git state and suggests the next action.

### Decision Tree

```mermaid
flowchart TD
    Start["/plot"] --> ReadState["Read: current branch,<br/>active plans, open PRs"]
    ReadState --> OnIdea{On idea/* branch?}
    OnIdea -->|yes| PlanDraft["Show plan status<br/>Suggest: refine, gh pr ready,<br/>or /plot-approve"]
    OnIdea -->|no| OnImpl{On impl branch?}
    OnImpl -->|yes| HasPlan{Has approved plan?}
    HasPlan -->|yes| ImplStatus["Show impl PR status<br/>Suggest: keep working,<br/>mark ready, or /plot-deliver"]
    HasPlan -->|no| Orphan["Orphan branch!<br/>Suggest: /plot-idea first"]
    OnImpl -->|no| OnMain{On main?}
    OnMain -->|yes| ListPlans["List active plans +<br/>delivered plans awaiting release<br/>Suggest next action"]
    OnMain -->|no| Other["Show general status"]
```

### 1. Read State

Gather context in parallel:

```bash
# Current branch
BRANCH=$(git branch --show-current)

# Active plans on main
ls docs/plans/active/ 2>/dev/null

# Delivered plans
ls docs/plans/delivered/ 2>/dev/null

# Active sprints
ls docs/sprints/active/ 2>/dev/null

# Open PRs on idea/ branches
gh pr list --json number,title,headRefName,isDraft,state --jq '.[] | select(.headRefName | startswith("idea/"))'

# Open PRs on impl branches (feature/, bug/, docs/, infra/)
gh pr list --json number,title,headRefName,isDraft,state --jq '.[] | select(.headRefName | startswith("feature/") or startswith("bug/") or startswith("docs/") or startswith("infra/"))'
```

Also run the bash helpers if a specific slug is in context:
- `./scripts/plot-pr-state.sh <slug>` — plan PR state
- `./scripts/plot-impl-status.sh <slug>` — impl PR states

### 2. Detect Current Context

**If on an `idea/*` branch:**
- Read the plan file from `docs/plans/<slug>.md` on this branch
- Check plan PR state (draft / ready / merged)
- Suggest:
  - If plan PR is draft: "Plan is still a draft. Refine it, then run `gh pr ready <number>` when ready for review."
  - If plan PR is non-draft (ready for review): "Plan is ready for review. Run `/plot-approve <slug>` to merge and create impl branches."
  - If plan PR is merged: "Plan is already approved. Run `/plot-approve <slug>` to create impl branches (if not already created)."

**If on an impl branch (`feature/*`, `bug/*`, `docs/*`, `infra/*`):**
- Check if there's a corresponding approved plan via `docs/plans/active/<slug>.md` on main
- If plan exists: show impl PR status, suggest keep working / mark ready / `/plot-deliver`
- If no plan exists: warn "Orphan branch — no approved plan found. Consider running `/plot-idea` first."

**If on `main`:**
- List all active plans with their phases
- List any delivered plans awaiting release (from `docs/plans/delivered/`)
- List active sprints with countdown and progress: `week-1 — "Ship auth improvements" | 3 days remaining | Must: 2/4 done`. Past end date: show "ended 2 days ago" factually — no warning tone, no nagging.
- Show overall status summary
- Suggest next action based on what's pending

**Otherwise:**
- Show general status: active plans, open PRs, recent deliveries

### 3. Detect Issues

Flag any problems found:

- **Orphan impl branches**: branches with `feature/`, `bug/`, `docs/`, `infra/` prefix that have no corresponding plan in `docs/plans/`
- **Phase mismatches**: plan says Draft but PR is non-draft, or plan says Approved but PR is still open
- **Stale drafts**: impl PRs that have been in draft state for more than 7 days
- **Overlapping plans**: Draft/Approved plans with titles sharing 3+ significant words — flag in the status summary as informational (no blocking)
- **Sprints past end date**: active sprints where end date has passed — flag as informational
- **Multiple active sprints**: more than one active sprint — flag as informational

> **Smaller models:** Skip title-similarity detection. Only report exact slug matches (identical filenames). Title overlap detection requires mid-tier reasoning.

### 4. Status Summary

Print a clear summary:

```
## Plot Status

### Active Plans
- `<slug>` — Phase: <phase> | Plan PR: #<n> (<state>) | Impl PRs: <count> merged / <count> total

### Active Sprints
- `<slug>` — "<goal>" | <N> days remaining | Must: <n>/<m> | Should: <n>/<m> | Could: <n>/<m>

### Issues
- <issue description>

### Suggested Next Step
> <specific command or action>
```
