---
name: post-mortem
description: 'Wrap up completed work. Council validates the implementation, then extract learnings. Triggers: "post-mortem", "wrap up", "close epic", "what did we learn".'
context: fork
metadata:
  tier: judgment
  dependencies:
    - council  # multi-model judgment
    - retro    # optional - extracts learnings (graceful skip on failure)
    - beads    # optional - for issue status
---

# Post-Mortem Skill

> **Purpose:** Wrap up completed work — validate it shipped correctly and extract learnings.

Two steps:
1. `/council validate` — Did we implement it correctly?
2. `/retro` — What did we learn?

---

## Quick Start

```bash
/post-mortem                    # wraps up recent work
/post-mortem epic-123           # wraps up specific epic
/post-mortem --quick recent     # fast inline wrap-up, no spawning
/post-mortem --deep recent      # thorough council review
/post-mortem --mixed epic-123   # cross-vendor (Claude + Codex)
/post-mortem --explorers=2 epic-123  # deep investigation before judging
/post-mortem --debate epic-123      # two-round adversarial review
/post-mortem --skip-checkpoint-policy epic-123  # skip ratchet chain validation
```

---

## Execution Steps

### Pre-Flight Checks

Before proceeding, verify:
1. **Git repo exists:** `git rev-parse --git-dir 2>/dev/null` — if not, error: "Not in a git repository"
2. **Work was done:** `git log --oneline -1 2>/dev/null` — if empty, error: "No commits found. Run /implement first."
3. **Epic context:** If epic ID provided, verify it has closed children. If 0 closed children, error: "No completed work to review."

### Step 0.5: Checkpoint-Policy Preflight (MANDATORY)

Read `references/checkpoint-policy.md` for the full checkpoint-policy preflight procedure. It validates the ratchet chain, checks artifact availability, and runs idempotency checks. BLOCK on prior FAIL verdicts; WARN on everything else.

### Step 1: Identify Completed Work and Record Timing

**Record the post-mortem start time for cycle-time tracking:**
```bash
PM_START=$(date +%s)
```

**If epic/issue ID provided:** Use it directly.

**If no ID:** Find recently completed work:
```bash
# Check for closed beads
bd list --status closed --since "7 days ago" 2>/dev/null | head -5

# Or check recent git activity
git log --oneline --since="7 days ago" | head -10
```

### Step 2: Load the Original Plan/Spec

Before invoking council, load the original plan for comparison:

1. **If epic/issue ID provided:** `bd show <id>` to get the spec/description
2. **Search for plan doc:** `ls .agents/plans/ | grep <target-keyword>`
3. **Check git log:** `git log --oneline | head -10` to find the relevant bead reference

If a plan is found, include it in the council packet's `context.spec` field:
```json
{
  "spec": {
    "source": "bead na-0042",
    "content": "<the original plan/spec text>"
  }
}
```

### Step 2.5: Pre-Council Metadata Verification (MANDATORY)

Read `references/metadata-verification.md` for the full verification procedure. Mechanically checks: plan vs actual files, file existence in commits, cross-references in docs, and ASCII diagram integrity. Failures are included in the council packet as `context.metadata_failures`.

### Step 3: Council Validates the Work

Run `/council` with the **retrospective** preset and always 3 judges:

```
/council --deep --preset=retrospective validate <epic-or-recent>
```

**Default (3 judges with retrospective perspectives):**
- `plan-compliance`: What was planned vs what was delivered? What's missing? What was added?
- `tech-debt`: What shortcuts were taken? What will bite us later? What needs cleanup?
- `learnings`: What patterns emerged? What should be extracted as reusable knowledge?

Post-mortem always uses 3 judges (`--deep`) because completed work deserves thorough review.

**Timeout:** Post-mortem inherits council timeout settings. If judges time out,
the council report will note partial results. Post-mortem treats a partial council
report the same as a full report — the verdict stands with available judges.

The plan/spec content is injected into the council packet context so the `plan-compliance` judge can compare planned vs delivered.

**With --quick (inline, no spawning):**
```
/council --quick validate <epic-or-recent>
```
Single-agent structured review. Fast wrap-up without spawning.

**With debate mode:**
```
/post-mortem --debate epic-123
```
Enables adversarial two-round review for post-implementation validation. Use for high-stakes shipped work where missed findings have production consequences. See `/council` docs for full --debate details.

**Advanced options (passed through to council):**
- `--mixed` — Cross-vendor (Claude + Codex) with retrospective perspectives
- `--preset=<name>` — Override with different personas (e.g., `--preset=ops` for production readiness)
- `--explorers=N` — Each judge spawns N explorers to investigate the implementation deeply before judging
- `--debate` — Two-round adversarial review (judges critique each other's findings before final verdict)

### Step 4: Extract Learnings

Run `/retro` to capture what we learned:

```
/retro <epic-or-recent>
```

**Retro captures:**
- What went well?
- What was harder than expected?
- What would we do differently?
- Patterns to reuse?
- Anti-patterns to avoid?

**Error Handling:**

| Failure | Behavior |
|---------|----------|
| Council fails | Stop, report council error, no retro |
| Retro fails | Proceed, report learnings as "⚠️ SKIPPED: retro unavailable" |
| Both succeed | Full post-mortem with council + learnings |

Post-mortem always completes if council succeeds. Retro is optional enrichment.

### Step 5: Write Post-Mortem Report

**Write to:** `.agents/council/YYYY-MM-DD-post-mortem-<topic>.md`

```markdown
# Post-Mortem: <Epic/Topic>

**Date:** YYYY-MM-DD
**Epic:** <epic-id or "recent">
**Duration:** <elapsed time from PM_START to now>
**Cycle-Time Trend:** <compare against prior post-mortems — is this faster or slower? Check .agents/retros/ for prior Duration values>

## Council Verdict: PASS / WARN / FAIL

| Judge | Verdict | Key Finding |
|-------|---------|-------------|
| Plan-Compliance | ... | ... |
| Tech-Debt | ... | ... |
| Learnings | ... | ... |

### Implementation Assessment
<council summary>

### Concerns
<any issues found>

## Learnings (from /retro)

### What Went Well
- ...

### What Was Hard
- ...

### Do Differently Next Time
- ...

### Patterns to Reuse
- ...

### Anti-Patterns to Avoid
- ...

## Proactive Improvement Agenda

| # | Area | Improvement | Priority | Horizon | Effort | Evidence |
|---|------|-------------|----------|---------|--------|----------|
| 1 | repo / execution / ci-automation | ... | P0/P1/P2 | now/next-cycle/later | S/M/L | ... |

### Recommended Next /rpi
/rpi "<highest-value improvement>"

## Status

[ ] CLOSED - Work complete, learnings captured
[ ] FOLLOW-UP - Issues need addressing (create new beads)
```

### Step 5.5: Synthesize Proactive Improvement Agenda (MANDATORY)

**After writing the post-mortem report, analyze retro + council context and proactively propose improvements to repo quality and execution quality.**

Read the retro output (from Step 4) and the council report (from Step 3). For each learning, ask:
1. **What process does this improve?** (build, test, review, deploy, documentation, automation, etc.)
2. **What's the concrete change?** (new check, new automation, workflow change, tooling improvement)
3. **Is it actionable in one RPI cycle?** (if not, split into smaller pieces)

Coverage requirements:
- Include at least **5** improvements total.
- Cover all three surfaces:
  - `repo` (code/contracts/docs quality)
  - `execution` (planning/implementation/review workflow)
  - `ci-automation` (validation/tooling reliability)
- Include at least **1 quick win** (small, low-risk, same-session viable).

Write process improvement items with type `process-improvement` (distinct from `tech-debt` or `improvement`). Each item must have:
- `title`: imperative form, e.g. "Add pre-commit lint check"
- `area`: which part of the development process to improve
- `description`: 2-3 sentences describing the change and why retro evidence supports it
- `evidence`: which retro finding or council finding motivates this
- `priority`: P0 / P1 / P2
- `horizon`: now / next-cycle / later
- `effort`: S / M / L

**These items feed directly into Step 8 (Harvest Next Work) alongside council findings. They are the flywheel's growth vector — each cycle makes the system smarter.**

Write this into the post-mortem report under `## Proactive Improvement Agenda`.

Example output:
```markdown
## Proactive Improvement Agenda

| # | Area | Improvement | Priority | Horizon | Effort | Evidence |
|---|------|-------------|----------|---------|--------|----------|
| 1 | ci-automation | Add validation metadata requirement for Go tasks | P0 | now | S | Workers shipped untested code when metadata didn't require `go test` |
| 2 | execution | Add consistency-check finding category in review | P1 | next-cycle | M | Partial refactoring left stale references undetected |

### Recommended Next /rpi
/rpi "<highest-value improvement>"
```

### Step 6: Feed the Knowledge Flywheel

Post-mortem automatically feeds learnings into the flywheel:

```bash
if command -v ao &>/dev/null; then
  ao forge markdown .agents/learnings/*.md 2>/dev/null
  echo "Learnings indexed in knowledge flywheel"

  # Close the MemRL feedback loop — update utility scores for cited learnings
  ao feedback-loop 2>/dev/null
  echo "Feedback loop closed"

  # Record session outcome when transcript/session metadata is available
  # (skip gracefully when unavailable)
  ao session-outcome --session "${SESSION_ID:-post-mortem}" 2>/dev/null || true
  echo "Session outcome recorded (or skipped if metadata unavailable)"

  # Validate and lock artifacts that passed council review
  ao temper validate .agents/learnings/YYYY-MM-DD-*.md 2>/dev/null || true
  echo "Artifacts validated for tempering"
else
  # Learnings are already in .agents/learnings/ from /retro (Step 4).
  # Without ao CLI, grep-based search in /research, /knowledge, and /inject
  # will find them directly — no copy to pending needed.

  # Feedback-loop fallback: update confidence for cited learnings
  mkdir -p .agents/ao
  if [ -f .agents/ao/citations.jsonl ]; then
    echo "Processing citation feedback (ao-free fallback)..."
    # Read cited learning files and boost confidence notation
    while IFS= read -r line; do
      CITED_FILE=$(echo "$line" | grep -o '"learning_file":"[^"]*"' | cut -d'"' -f4)
      if [ -f "$CITED_FILE" ]; then
        # Note: confidence boost tracked via citation count, not file modification
        echo "Cited: $CITED_FILE"
      fi
    done < .agents/ao/citations.jsonl
  fi

  # Session-outcome fallback: record this session's outcome
  EPIC_ID="<epic-id>"
  echo "{\"epic\": \"$EPIC_ID\", \"verdict\": \"<council-verdict>\", \"cycle_time_minutes\": 0, \"timestamp\": \"$(date -Iseconds)\"}" >> .agents/ao/outcomes.jsonl

  # Skip ao temper validate (no fallback needed — tempering is an optimization)
  echo "Flywheel fed locally (ao CLI not available — learnings searchable via grep)"
fi
```

### Step 7: Report to User

Tell the user:
1. Council verdict on implementation
2. Key learnings
3. Any follow-up items
4. Location of post-mortem report
5. Knowledge flywheel status
6. **Suggested next `/rpi` command** (ALWAYS — this is how the flywheel spins itself)
7. Top proactive improvements (top 3), including one quick win

**The next `/rpi` suggestion is MANDATORY, not opt-in.** After every post-mortem, present the highest-severity harvested item as a ready-to-copy command:

```markdown
## Flywheel: Next Cycle

Based on this post-mortem, the highest-priority follow-up is:

> **<title>** (<type>, <severity>)
> <1-line description>

Ready to run:
```
/rpi "<title>"
```

Or see all N harvested items in `.agents/rpi/next-work.jsonl`.
```

If no items were harvested, write: "Flywheel stable — no follow-up items identified."

### Step 8: Harvest Next Work

Scan the council report and retro for actionable follow-up items:

1. **Council findings:** Extract tech debt, warnings, and improvement suggestions from the council report (items with severity "significant" or "critical" that weren't addressed in this epic)
2. **Retro patterns:** Extract recurring patterns from retro learnings that warrant dedicated RPIs (items from "Do Differently Next Time" and "Anti-Patterns to Avoid")
3. **Process improvements:** Include all items from Step 5.5 (type: `process-improvement`). These are the flywheel's growth vector — each cycle makes development more effective.
4. **Write `## Next Work` section** to the post-mortem report:

```markdown
## Next Work

| # | Title | Type | Severity | Source | Target Repo |
|---|-------|------|----------|--------|-------------|
| 1 | <title> | tech-debt / improvement / pattern-fix / process-improvement | high / medium / low | council-finding / retro-learning / retro-pattern | <repo-name or *> |
```

5. **SCHEMA VALIDATION (MANDATORY):** Before writing, validate each harvested item against the schema contract (`.agents/rpi/next-work.schema.md`):

```bash
validate_next_work_item() {
  local item="$1"
  local title=$(echo "$item" | jq -r '.title // empty')
  local type=$(echo "$item" | jq -r '.type // empty')
  local severity=$(echo "$item" | jq -r '.severity // empty')
  local source=$(echo "$item" | jq -r '.source // empty')
  local description=$(echo "$item" | jq -r '.description // empty')
  local target_repo=$(echo "$item" | jq -r '.target_repo // empty')

  # Required fields
  if [ -z "$title" ] || [ -z "$description" ]; then
    echo "SCHEMA VALIDATION FAILED: missing title or description for item"
    return 1
  fi

  # target_repo required (v1.2)
  if [ -z "$target_repo" ]; then
    echo "SCHEMA VALIDATION FAILED: missing target_repo for item '$title'"
    return 1
  fi

  # Type enum validation
  case "$type" in
    tech-debt|improvement|pattern-fix|process-improvement) ;;
    *) echo "SCHEMA VALIDATION FAILED: invalid type '$type' for item '$title'"; return 1 ;;
  esac

  # Severity enum validation
  case "$severity" in
    high|medium|low) ;;
    *) echo "SCHEMA VALIDATION FAILED: invalid severity '$severity' for item '$title'"; return 1 ;;
  esac

  # Source enum validation
  case "$source" in
    council-finding|retro-learning|retro-pattern) ;;
    *) echo "SCHEMA VALIDATION FAILED: invalid source '$source' for item '$title'"; return 1 ;;
  esac

  return 0
}

# Validate each item; drop invalid items (do NOT block the entire harvest)
VALID_ITEMS=()
INVALID_COUNT=0
for item in "${HARVESTED_ITEMS[@]}"; do
  if validate_next_work_item "$item"; then
    VALID_ITEMS+=("$item")
  else
    INVALID_COUNT=$((INVALID_COUNT + 1))
  fi
done
echo "Schema validation: ${#VALID_ITEMS[@]}/$((${#VALID_ITEMS[@]} + INVALID_COUNT)) items passed"
```

6. **Write to next-work.jsonl** (canonical path: `.agents/rpi/next-work.jsonl`):

```bash
mkdir -p .agents/rpi

# Resolve current repo name for target_repo default
CURRENT_REPO=$(bd config --get prefix 2>/dev/null \
  || basename "$(git remote get-url origin 2>/dev/null)" .git 2>/dev/null \
  || basename "$(pwd)")

# Assign target_repo to each validated item (v1.2):
#   process-improvement → "*" (applies across all repos)
#   all other types     → CURRENT_REPO (scoped to this repo)
for i in "${!VALID_ITEMS[@]}"; do
  item="${VALID_ITEMS[$i]}"
  item_type=$(echo "$item" | jq -r '.type')
  if [ "$item_type" = "process-improvement" ]; then
    VALID_ITEMS[$i]=$(echo "$item" | jq -c '.target_repo = "*"')
  else
    VALID_ITEMS[$i]=$(echo "$item" | jq -c --arg repo "$CURRENT_REPO" '.target_repo = $repo')
  fi
done

# Append one entry per epic (schema v1.2: .agents/rpi/next-work.schema.md)
# Only include VALID_ITEMS that passed schema validation
# Each item: {title, type, severity, source, description, evidence, target_repo}
# Entry fields: source_epic, timestamp, items[], consumed: false
```

Use the Write tool to append a single JSON line to `.agents/rpi/next-work.jsonl` with:
- `source_epic`: the epic ID being post-mortemed
- `timestamp`: current ISO-8601
- `items`: array of harvested items (min 0 — if nothing found, write entry with empty items array)
- `consumed`: false, `consumed_by`: null, `consumed_at`: null

7. **Do NOT auto-create bd issues.** Report the items and suggest: "Run `/rpi --spawn-next` to create an epic from these items."

If no actionable items found, write: "No follow-up items identified. Flywheel stable."

---

## Integration with Workflow

```
/plan epic-123
    │
    ▼
/pre-mortem (council on plan)
    │
    ▼
/implement
    │
    ▼
/vibe (council on code)
    │
    ▼
Ship it
    │
    ▼
/post-mortem              ← You are here
    │
    ├── Council validates implementation
    ├── Retro extracts learnings
    ├── Synthesize process improvements
    └── Suggest next /rpi ──────────┐
                                    │
    ┌───────────────────────────────┘
    │  (flywheel: learnings become next work)
    ▼
/rpi "<highest-priority enhancement>"
```

---

## Examples

### Wrap Up Recent Work

**User says:** `/post-mortem`

**What happens:**
1. Agent scans recent commits (last 7 days)
2. Runs `/council --deep --preset=retrospective validate recent`
3. 3 judges (plan-compliance, tech-debt, learnings) review
4. Runs `/retro` to extract learnings
5. Synthesizes process improvement proposals
6. Harvests next-work items to `.agents/rpi/next-work.jsonl`
7. Feeds learnings to knowledge flywheel via `ao forge`

**Result:** Post-mortem report with learnings, tech debt identified, and suggested next `/rpi` command.

### Wrap Up Specific Epic

**User says:** `/post-mortem ag-5k2`

**What happens:**
1. Agent loads original plan from `bd show ag-5k2`
2. Council reviews implementation vs plan
3. Retro captures what went well and what was hard
4. Process improvements identified (e.g., "Add pre-commit lint check")
5. Next-work items harvested and written to JSONL

**Result:** Epic-specific post-mortem with 3 harvested follow-up items (2 tech-debt, 1 process-improvement).

### Cross-Vendor Review

**User says:** `/post-mortem --mixed ag-3b7`

**What happens:**
1. Agent runs 3 Claude + 3 Codex judges
2. Cross-vendor perspectives catch edge cases
3. Verdict: WARN (missing error handling in 2 files)
4. Harvests 1 tech-debt item

**Result:** Higher confidence validation with cross-vendor review before closing epic.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Council times out | Epic too large or too many files changed | Split post-mortem into smaller reviews or increase timeout |
| Retro fails but council succeeds | `/retro` skill unavailable or errors | Post-mortem proceeds with "⚠️ SKIPPED: retro unavailable" — council findings still captured |
| No next-work items harvested | Council found no tech debt or improvements | Flywheel stable — write entry with empty items array to next-work.jsonl |
| Schema validation failed | Harvested item missing required field or has invalid enum value | Drop invalid item, log error, proceed with valid items only |
| Checkpoint-policy preflight blocks | Prior FAIL verdict in ratchet chain without fix | Resolve prior failure (fix + re-vibe) or skip checkpoint-policy via `--skip-checkpoint-policy` |
| Metadata verification fails | Plan vs actual files mismatch or missing cross-references | Include failures in council packet as `context.metadata_failures` — judges assess severity |

---

## See Also

- `skills/council/SKILL.md` — Multi-model validation council
- `skills/retro/SKILL.md` — Extract learnings
- `skills/vibe/SKILL.md` — Council validates code (`/vibe` after coding)
- `skills/pre-mortem/SKILL.md` — Council validates plans (before implementation)
- `.agents/specs/conflict-resolution-algorithm.md` — Conflict resolution for agent findings
