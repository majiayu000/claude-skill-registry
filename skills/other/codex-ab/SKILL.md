---
name: codex-ab
description: Run an A/B codex review experiment — holistic codex review vs 3 focused dimension passes (security, ecto, liveview) on the branch diff, classify findings, report a panel-value verdict. Use when the branch is fresh, before any codex review runs.
effort: medium
argument-hint: "[base-branch]"
---

# Codex Panel A/B (contributor instrument — verdict decided)

Answer one question with evidence: **do dimension-focused codex passes find
real issues that one holistic `codex exec review` misses?** Runs both on the
same diff, then classifies every focused finding against the holistic pass.

> **DECIDED 2026-07-10 after 4 runs (2 fresh): panel KILLED.** Fresh-only
> 1 real miss / 1 false positive plus one zero-value run at 4× cost —
> real misses did not outnumber FPs. Kept as contributor tooling (NOT
> distributed) for one possible retest: a UI-heavy diff with a single
> extra liveview-focused pass (2× cost). Scoreboard:
> `.claude/research/2026-07-03-codex-review-integration.md` §7.

## Usage

```
/codex-ab            # A/B against main (~5 min, 4 codex runs)
/codex-ab develop    # explicit base branch
```

## Iron Laws

1. **FRESH DIFF ONLY** — ask the user to confirm this branch has NOT been
   codex-reviewed yet (cloud or `/phx:codex-loop`). A drained diff returns
   NO FINDINGS everywhere and proves nothing — wasted quota
2. **Verify every REAL MISS in the code before counting it** — a focused
   finding only scores if the issue actually exists at that file:line
3. **Read ONLY the findings `.md` files** — streams are diverted to `.log`
   files; never cat a log into context (10k+ lines each)
4. **Exactly 4 codex runs, never re-run dimensions** — bounded quota
5. **Persist the verdict** — an unrecorded experiment is wasted quota

## Workflow

### Step 1: Preflight

Run `command -v codex` — missing → STOP with install hint. Then:

- `git status --short` dirty → warn (codex flags local dirt as findings)
- Ask: "Has codex already reviewed this branch (PR review or codex-loop)?"
  If yes → STOP, explain the fresh-diff requirement (Iron Law 1)

### Step 2: Run the A/B (background, ~5 min)

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/codex-panel-ab.sh {base} \
  .claude/reviews/codex-ab-$(date +%Y-%m-%d-%H%M)
```

Use `run_in_background` — it runs 1 holistic `codex exec review` + 3
focused `codex exec` workers (security / ecto / liveview) in parallel,
all streams redirected. Do other work or wait; never poll.

### Step 3: Classify

Read the 4 findings files (`holistic.md`, `security.md`, `ecto.md`,
`liveview.md` — small). For EACH focused finding:

| Class | Meaning | Test |
|-------|---------|------|
| DUPLICATE | Holistic already found it | Same file + same defect |
| REAL MISS | Genuine issue holistic missed | Read the code at file:line — defect confirmed (Iron Law 2) |
| FALSE POSITIVE | Manufactured, pre-existing, or wrong | Code check fails, or issue exists on base branch too |

### Step 4: Verdict

Present:

```markdown
## Codex Panel A/B — {branch} vs {base}
| dimension | findings | duplicate | real miss | false positive |
Holistic-only findings: {n}
Verdict this run: {REAL MISS count} real miss vs {FP count} false positive
Decision rule: build --codex-panel only if real misses outnumber false
positives across 2-3 fresh branches.
```

Write the verdict table to `.claude/reviews/codex-ab-{date}/VERDICT.md`.
Suggest repeating on the next 1–2 fresh branches before deciding.

## Integration

```text
fresh branch → /codex-ab (YOU ARE HERE) → verdict logged
   ├─ real misses win across runs → build /phx:review --codex-panel
   └─ duplicates/FPs win → keep holistic /phx:codex-loop, drop panel idea
       └─ OUTCOME 2026-07-10: this branch won — panel dropped
```

## References

- `${CLAUDE_SKILL_DIR}/scripts/codex-panel-ab.sh` — the 4-run harness
- Related: `/phx:codex-loop` (holistic fix loop), `/phx:review --codex`
