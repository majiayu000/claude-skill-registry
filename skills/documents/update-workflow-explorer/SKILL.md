---
name: update-workflow-explorer
description: Audit and update workflow-explorer.html flowcharts to match the current codebase logic. Reads all command, skill, and agent source files, compares against the 4 data structures in the HTML file, reports drift, and applies updates. Use when workflow logic has changed and the explorer needs syncing.
disable-model-invocation: true
---

# Update Workflow Explorer

Audit `workflow-explorer.html` and sync its flowchart data with the actual command/skill/agent source files.

## Step 0: Determine Scope

### 0a: Check for explicit context

Check `$ARGUMENTS` for user-provided context about what changed.

- **Context given** (e.g. "I just updated the implementation skill") → narrow to affected flowchart keys using the source mapping below
- **Ambiguous** → ASK user to confirm scope before proceeding

If explicit context was given, skip 0b and proceed to Step 1 with the narrowed scope.

### 0b: Detect git context

If no explicit context was given, check the git state:

1. **Branch check** — run `git branch --show-current`. If not on `main`/`master`, note the feature branch name.
2. **Changed files** — run `git diff main --name-only` (branch changes) and `git diff --name-only` + `git diff --cached --name-only` (uncommitted/staged changes). Combine into a single list of changed files.
3. **Cross-reference** — match changed files against the source mapping below. Identify which flowchart keys are affected.

If changed source files are detected, present findings to the user:

> I'm on branch `{branch}` with changes to these source files:
> - `{file}` → flowchart key(s): `{key}`
> - ...
>
> **Options:**
> 1. **Scope to these changes** — audit only the affected flowchart keys (recommended if this branch represents all recent work)
> 2. **Full audit** — audit all flowchart keys regardless of git state

Wait for user confirmation before proceeding.

If no changed source files are detected (on main with clean tree), proceed with a full audit.

## Step 1: Read Source Files

For each in-scope flowchart key, read its source file(s) and extract the logical flow: steps, gates, decisions, loops, conditional branches, outputs.

### Source Mapping

| Key | Source Files |
|---|---|
| `research` | `commands/workflow/start-research.md` |
| `discussion` | `commands/workflow/start-discussion.md` |
| `specification` | `commands/workflow/start-specification.md` |
| `planning` | `commands/workflow/start-planning.md` |
| `implementation` | `commands/workflow/start-implementation.md` |
| `review` | `commands/workflow/start-review.md` |
| `skill-research` | `skills/technical-research/SKILL.md` |
| `skill-discussion` | `skills/technical-discussion/SKILL.md` |
| `skill-specification` | `skills/technical-specification/SKILL.md` + `skills/technical-specification/references/steps/*.md` |
| `skill-planning` | `skills/technical-planning/SKILL.md` + `skills/technical-planning/references/steps/*.md` |
| `skill-implementation` | `skills/technical-implementation/SKILL.md` + `skills/technical-implementation/references/steps/*.md` |
| `skill-review` | `skills/technical-review/SKILL.md` + `agents/review-task-verifier.md` |
| `start-feature` | `commands/start-feature.md` |
| `link-deps` | `commands/link-dependencies.md` |
| `status` | `commands/workflow/status.md` |
| `view-plan` | `commands/workflow/view-plan.md` |
| `migrate` | `commands/migrate.md` |
| `planning-phase-designer` | `agents/planning-phase-designer.md` |
| `planning-task-designer` | `agents/planning-task-designer.md` |
| `planning-task-author` | `agents/planning-task-author.md` |
| `planning-dependency-grapher` | `agents/planning-dependency-grapher.md` |
| `implementation-task-executor` | `agents/implementation-task-executor.md` |
| `implementation-task-reviewer` | `agents/implementation-task-reviewer.md` |
| `review-task-verifier` | `agents/review-task-verifier.md` |

Use parallel reads (Task tool with Explore agents or multiple Read calls) to gather sources efficiently.

## Step 2: Read Current Flowchart Data

Read `workflow-explorer.html` and extract the 6 data structures for each in-scope key:

1. **`phases[key]`** — metadata (steps, desc, scenarios, detailHTML)
2. **`FLOWCHARTS[key]`** — nodes + connections
3. **`FLOWCHART_DESCS[key]`** — summary, body, meta
4. **`OVERVIEW_*`** — only if phases were added/removed/renamed
5. **`SOURCE_MAP[key]`** — repo-relative path to source file (update when files are renamed)
6. **`SKILL_NEXT_PHASE[key]`** — next-phase navigation for skill flowcharts

## Step 3: Compare and Report

For each key, compare source logic against current flowchart data. Report per key:

- **MATCH** — no drift detected
- **DRIFT** — specific differences (added/removed steps, renamed concepts, changed gates, altered flow)
- **MISSING** — flowchart key exists in sources but not in explorer (or vice versa)

**Present findings to the user and STOP. Wait for confirmation of which changes to apply before proceeding.**

## Step 4: Apply Updates

For each confirmed change, update the following in `workflow-explorer.html`:

- `FLOWCHARTS[key].nodes` and `.connections`
- `FLOWCHART_DESCS[key]` summary, body, meta
- `phases[key]` desc, steps count, detailHTML (if affected)
- `OVERVIEW_*` (only if phases added/removed)

### Data Conventions

Follow the conventions documented in the file header (lines 1-41):

**Node shapes:**
- `pill` — start/end nodes (w:150, h:40)
- `diamond` — decision/routing nodes (w:110-130, h:110-130)
- `stop` — hard-cornered terminal nodes for STOP/BLOCK (w:150-180, h:40, rx:3)
- rect (default) — action step nodes (w:180-200, h:44)

**Connection types:**
- `yes` — green (positive branch from diamond)
- `no` — red (negative branch from diamond)
- `transition` — orange dashed (phase/context transitions)
- `backloop` — gray dashed (retry/loop-back flows)

**Color conventions (type-based, NOT phase-based — use CSS vars):**
- `var(--action)` sky blue — primary work steps (validate, extract, etc.)
- `var(--agent)` cyan — agent invocation nodes (with optional `skillLink` to agent flowchart)
- `var(--text-dim)` gray — utility/support steps (read existing, load format, etc.)
- `var(--ask)` purple — user-interaction nodes
- `var(--routing)` amber — decision diamonds (all diamonds use this)
- `var(--gate)` red — STOP/BLOCK terminal nodes (hard-cornered `stop` shape), cache refresh
- `var(--discovery)` green — discovery script execution
- `var(--skill)` orange — skill invocation pills (with `skillLink`)
- `var(--next)` blue — next-phase navigation nodes (rect, command color, same shape as agent nodes)
- `var(--accent)` blue — entry points, migrations, git commits
- `var(--{phase})` phase color — END output artifacts only (keeps phase identity)

**Node properties:**
- `skillLink` — on nodes that should navigate to a skill or agent flowchart on click
- `desc` — tooltip text describing what the node does

**Next-phase nodes (skill flowcharts only):**
- Every skill flowchart except `skill-review` has a `next` rect node at the end
- Node: `{ id: 'next', label: 'Invoke /start-{phase}', desc: '...', w: 200, h: 44, color: 'var(--next)', bg: 'var(--next-bg)', skillLink: NEXT_PHASE_KEY }`
- Connection: `{ from: 'end', to: 'next', type: 'transition' }`
- All next nodes use consistent command blue (`var(--next)`) regardless of target phase
- `SKILL_NEXT_PHASE` mapping must stay in sync

**SOURCE_MAP maintenance:**
- When source files are renamed or new flowchart keys are added, update `SOURCE_MAP` accordingly
- `SOURCE_MAP` maps flowchart keys to repo-relative file paths for the markdown viewer

## Step 5: Validate and Verify

After applying updates:

1. Check all connection `from`/`to` values reference valid node IDs in the same flowchart
2. Check for orphaned nodes (not referenced by any connection as source or target, excluding `start` nodes)
3. Remind user to open `workflow-explorer.html` in browser for visual verification
