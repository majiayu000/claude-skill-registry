---
name: goals
description: 'Maintain GOALS.yaml fitness specification. Generate new goals from repo state, prune stale goals, update drifted checks. Triggers: "goals", "goal status", "show goals", "generate goals", "add goals", "prune goals", "update goals", "clean goals".'
metadata:
  tier: product
  dependencies: []
---

# /goals — Fitness Goal Maintenance

> Maintain the GOALS.yaml that `/evolve` consumes. Run checks, generate new goals from repo state, prune stale ones.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Quick Start

```bash
/goals                    # Status dashboard (default)
/goals generate           # Scan repo, propose new goals
/goals prune              # Find stale/broken goals, propose fixes
```

---

## Mode Selection

Parse the user's input to determine the mode:

| Input | Mode |
|-------|------|
| `/goals`, `/goals status`, "goal status", "show goals" | **status** |
| `/goals generate`, "generate goals", "add goals" | **generate** |
| `/goals prune`, "prune goals", "update goals", "clean goals" | **prune** |

---

## Status Mode (default)

### Step 1: Parse GOALS.yaml

Read `GOALS.yaml` from the repo root. Extract:
- `version`, `mission`, `pillars`
- All goals with `id`, `description`, `check`, `weight`, `pillar` (optional)

### Step 2: Run All Checks

For each goal, execute the `check` command using Bash:
- **Exit 0** = PASS
- **Non-zero exit** = FAIL
- **Command error** (command not found, syntax error) = ERROR

Capture exit code and stderr for each. Run in parallel where possible (independent checks).

### Step 3: Group and Report

Group results by category:
1. **Pillar goals** — grouped by pillar, sorted by weight (highest first)
2. **Infrastructure goals** — sorted by weight
3. **Cross-runtime goals** — sorted by weight

For each goal, show:
```
[PASS] id (weight N) — description
[FAIL] id (weight N) — description
  └─ stderr: <first line of error output>
[ERROR] id (weight N) — description
  └─ error: <command error>
```

### Step 4: Summary

```
Fitness: 52/65 passing (80%)

By pillar:
  knowledge-compounding:   9/11 (82%)  weight: 45/51
  validated-acceleration:  4/5  (80%)  weight: 13/17
  goal-driven-automation:  5/5  (100%) weight: 17/17
  zero-friction-workflow:  8/10 (80%)  weight: 25/34

Infrastructure: 20/25 (80%)
Cross-runtime: 6/9 (67%)
```

### Step 5: Staleness Check

Flag goals whose `check` references paths that don't exist:
- Extract file paths from check commands (patterns: `test -f <path>`, `grep ... <path>`, `cat <path>`)
- Check each path with `test -e`
- Report stale references

---

## Generate Mode

### Step 1: Read Context

Read these files (in parallel):
- `GOALS.yaml` — existing goal IDs
- `PRODUCT.md` — design principles, value props, pillars
- `README.md` — claims, badges, features
- `skills/SKILL-TIERS.md` — full skill list

### Step 2: Identify Coverage Gaps

**Uncovered skills:** For each skill in `skills/*/SKILL.md`, check if any existing goal's `check` field references that skill directory. List skills with no goal.

**Uncovered infrastructure:** Scan `tests/`, `hooks/`, `scripts/` for scripts not referenced by any goal's `check`.

**Pillar coverage:** Check each of the 4 pillars has adequate goals. Reference the theoretical pillar mapping in `references/generation-heuristics.md`.

**Claim verification:** Scan README.md for quantitative claims (numbers, "all", "every") that have no corresponding goal verifying them.

### Step 3: Propose Goals

For each gap, draft a goal:
```yaml
- id: <kebab-case-id>
  description: "<what it measures>"
  check: "<shell command, exit 0 = pass>"
  weight: <1-5>
  pillar: <pillar-name>  # omit for infrastructure
```

Apply quality criteria from `references/generation-heuristics.md`:
- Mechanically verifiable (shell command)
- Not trivially true
- Not duplicative of existing goals
- Weighted by impact

### Step 4: User Selection

Present proposals via `AskUserQuestion`. Group by category:
- "Which pillar goals should be added?"
- "Which infrastructure goals should be added?"

Allow multi-select. User can also provide custom edits.

### Step 5: Write Accepted Goals

Append accepted goals to `GOALS.yaml` in the appropriate section (pillar or infrastructure).

Update the header comment counts:
```yaml
# Total: N goals (X pillar + Y infrastructure + Z cross-runtime)
```

Count mechanically — `grep -c '^ *- id:' GOALS.yaml` — don't estimate.

---

## Prune Mode

### Step 1: Run All Checks

Same as Status Mode Step 2. Collect exit codes, stderr, and timing.

### Step 2: Classify Issues

For each goal, check for:

**Broken checks** (ERROR status):
- Command not found
- Syntax error in check
- References deleted files/directories

**Orphaned references:**
- Check references skills (`skills/<name>/`) that don't exist
- Check references files that don't exist
- Check references CLI commands that aren't installed

**Count drift:**
- Header comment says `N goals` but actual count differs
- Pillar sub-counts don't match actual

**Trivially true** (heuristic):
- Check is `test -f <path>` for a file that's been in git for 6+ months unchanged
- Check is `grep -q <literal>` for content that hasn't changed in 6+ months

### Step 3: Propose Actions

For each issue, propose one of:
- **Remove** — goal is obsolete or duplicative
- **Update check** — fix the command to reference correct paths/patterns
- **Keep** — acknowledge the issue but justify keeping the goal

Present via `AskUserQuestion` with multi-select.

### Step 4: Apply Changes

For accepted removals: delete the goal entry from GOALS.yaml.
For accepted updates: replace the check command.

### Step 5: Update Counts

Recount all goals mechanically and update the header comment.

---

## Examples

### Checking fitness status across all goals

**User says:** `/goals`

**What happens:**
1. Parses `GOALS.yaml` from the repo root, extracting all goals with their checks, weights, and pillar assignments.
2. Executes every goal's `check` command and records PASS/FAIL/ERROR results.
3. Groups results by pillar and infrastructure, then prints a fitness summary with pass rates and weighted scores.

**Result:** A dashboard showing overall fitness (e.g., "52/65 passing, 80%") with per-pillar breakdowns and any stale or broken checks flagged.

### Generating new goals from repo state

**User says:** `/goals generate`

**What happens:**
1. Reads `GOALS.yaml`, `PRODUCT.md`, `README.md`, and `skills/SKILL-TIERS.md` to understand current coverage.
2. Identifies gaps: skills with no corresponding goal, infrastructure scripts not covered by any check, pillars with thin coverage, and README claims with no verification.
3. Drafts new goals with mechanically verifiable shell checks and presents them for user selection via multi-select prompt.

**Result:** User-approved goals are appended to `GOALS.yaml` with updated header counts, closing coverage gaps.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `GOALS.yaml: No such file or directory` | The repo has no goals file yet | Create an initial `GOALS.yaml` with at least one goal, or run `/goals generate` which will offer to scaffold one |
| Multiple goals show ERROR status | Check commands reference tools or paths that are not available in the current environment | Run `/goals prune` to identify and fix broken checks. Ensure required CLI tools are installed |
| Pillar counts in header comment drift from actual | Goals were manually added or removed without updating the header | Run `/goals prune` which mechanically recounts and updates the header comment |
| Generate mode proposes trivially true goals | Heuristics matched stable files that rarely change | Review proposals carefully during the selection step and reject goals that check for files unchanged in 6+ months |
| Staleness check flags valid paths as missing | Check commands use relative paths that depend on working directory | Ensure check commands use repo-root-relative paths or prefix with `cd "$(git rev-parse --show-toplevel)" &&` |

## See Also

- `/evolve` — consumes GOALS.yaml for fitness-scored improvement loops
- `skills/evolve/references/goals-schema.md` — GOALS.yaml schema definition
- `references/generation-heuristics.md` — goal quality criteria and scan sources
