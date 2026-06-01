---
name: skill-refiner
description: >
  · Improve skill collections or a named skill with iterative scoring, lint checks, behavioral tests, peer review. Triggers: 'skill refiner', 'improve skills', 'quality sweep', 'batch improve', 'skill loop', 'target 99%'.
license: MIT
compatibility: "Requires: skill-creator skill, git. Optional: secondary AI harness (codex, claude, gemini, opencode) for cross-model review"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-31"
  effort: high
  argument_hint: "[iterations]"
---

# Skill Refiner: Iterative Self-Improvement Loop

Adaptive evaluation loop for AI skill collections, inspired by Karpathy's AutoResearch.
Orchestrates repeated score-improve-verify cycles using **skill-creator** as the engine
and mandatory peer review as an adversarial check (cross-model when a secondary harness
is available, fresh-context self-review as the minimum fallback).

## When to use

- Batch-improving the entire skill collection after a period of manual edits
- Targeted improvement of one named skill when the user explicitly asks for skill-refiner,
  multiple iterations, a score target, or "no ceiling" polish
- Running quality sweeps before a release or publish
- Triggering a self-improvement cycle where skills bootstrap each other
- After adding several new skills that need polish and consistency alignment
- When cross-model perspective would catch single-model blind spots
- Periodic maintenance: scheduled improvement runs to keep skills current

## When NOT to use

- Creating a new skill from scratch - use **skill-creator** (Mode 1)
- Single-pass review of one skill without iteration, scoring, or peer review - use **skill-creator** (Mode 2)
- One-off collection audit without iteration - use **skill-creator** (Mode 3)
- Full codebase review (code, not skills) - use **full-review**
- Style/slop audit on application code - use **anti-slop**

## Configuration

```
skill-refiner [--iterations N] [--mode MODE] [--secondary HARNESS] [--threshold N] [--plateau N]
```

| Flag | Default | Description |
|---|---|---|
| `--iterations` | 10 | Maximum iterations for phase 1 |
| `--mode` | circuit-breaker | `auto`, `circuit-breaker`, or `step` |
| `--secondary` | auto-detect | Secondary harness for cross-model review, or `none` |
| `--threshold` | 85 | Focus threshold - skip skills scoring above this (user can override max) |
| `--plateau` | 2 | Minimum score delta to keep iterating |

**Environment override:** `SKILL_REFINER_SECONDARY=<harness>` (CLI flag takes precedence)

### Checkpoint Modes

**circuit-breaker** (default): runs autonomously, auto-pauses on score regression,
contested major flags, or plateau. Always pauses before phase 2.

**auto**: fully autonomous through phase 1. Still pauses before phase 2 and on
contested major flags (non-configurable).

**step**: pauses after every iteration for manual review. Best for first run or learning.

---

## Performance

- Batch similar edits and validations to reduce repeated full-collection scans.
- Prioritize low-scoring or recently changed skills before polishing already-healthy ones.
- Use focused diffs and line-count checks after each batch to avoid late cleanup churn.


---

## Best Practices

- Snapshot evaluation criteria before editing the skills that define the criteria.
- Revert changes that add complexity without improving behavior.
- Keep run history factual and free of unverifiable score inflation.
- Treat composite deltas as noisy when different scorer instances run across
  iterations: a few points of swing is judge variance, not real change. Anchor
  keep/revert decisions on the structural gate, on whether the specific targeted
  weakness was fixed, and on cross-model NO_FLAGS - not on small composite moves.
  Use a consistent scoring approach within a single before/after comparison.
- Leave externally-maintained version, CVE, and EOL pins out of scope. When a
  collection has a freshness routine (or equivalent) that owns version currency,
  do not edit those pins during a run and do not score them as "unverifiable"
  failures; flag only internal contradictions.
- Audit offensive or security skills (privilege escalation, exploit research)
  in-loop rather than through web-researching subagents, which can trip platform
  safeguards. Keep their scoring and edits in the main session.


## Workflow

### Phase 0: Setup

1. **Create feature branch**: `skill-refiner/YYYY-MM-DD-HHMMSS` from current HEAD.
   Preserve dirty worktrees; branching isolates the run, it does not imply cleanup. If already
   on a run branch for this sweep, record it instead of nesting another branch. Do not mix
   unrelated dirty files into refiner commits; isolate them with a path-limited stash only
   when authorized.
2. **Load run history**: read `.refiner-runs.json` from the collection root (if it exists).
   Use previous run data for: baseline score comparison (detect regressions from external
   changes), model/harness change detection (flag if the primary or secondary model changed
   since last run - new model = new baseline, not a comparable delta), and skip analysis
   (don't re-attempt improvements that were already tried and reverted in a recent run).
3. **Build skill inventory**: list all skills, exclude phase-2 targets (skill-creator,
   skill-refiner) from the improvement pool
4. **Detect primary harness**: check environment to identify which AI CLI is running
   this session
5. **Probe for secondary harness**: run three-step validation (PATH check, config check,
   smoke test) per `references/harness-detection.md`. Announce result.
6. **If no secondary found**: **always fall back to self-review.** Spawn a fresh agent on
   the current harness with the review prompt template from `references/harness-detection.md`.
   Label as "same-model fresh-context review" in scoring, weight at 3% instead of 5%
   (composite becomes gate/40/55/3, renormalize the missing 2% proportionally to AI Self-Check
   and Behavioral). This catches confirmation bias but shares the primary model's blind spots.
   Skipping review entirely is not an option - a fresh-context self-review is the minimum bar.
   If the harness doesn't support subagents, run the review prompt as a separate CLI
   invocation (`claude -p`, `codex exec`, `gemini -p`, etc.).

### Phase 1: Regular Iterations

6. **Iteration 1 - full sweep**: score every skill in the pool using the four-component
   model from `references/evaluation-criteria.md`
   - Structural: run lint-skills.sh + validate-spec.sh
   - AI Self-Check: invoke **skill-creator** review mode on each skill
   - Behavioral: run test prompts from `references/test-cases.md`. For skills without
     pre-written test cases, auto-generate 2-3 test prompts from the skill's "When to use"
     section and quality signals from its AI Self-Check. Log a warning that generated tests
     are lower quality than hand-written ones. Optionally save generated tests to a
     test-cases-local.md file alongside test-cases.md so they accumulate across runs.
   - Cross-model: skip on first iteration (no diff to review yet)
7. **Log baseline scores**: record per-skill and aggregate scores
   in a score ledger before any edits. The ledger must include structural gate (G),
   AI Self-Check (A), behavioral score (B), cross-model review (X), composite score,
   test source, reviewer source, and timestamp. After this step, if the ledger is
   missing, incomplete, or only records lint/spec status, pause and backfill scoring before
   applying changes. In headless mode, halt the run and report the missing score data.
8. **Iteration 2+**: enter adaptive focus mode. For a user-requested single-skill run,
   treat that skill as the whole phase-1 pool, run at least the requested iteration count,
   and keep iterating until the explicit score target is reached, quality plateaus, or a
   circuit breaker fires.
9. **Select targets**: identify skills scoring below the focus threshold
10. **For each targeted skill**, run the improvement cycle:
    a. Read current SKILL.md and all reference files
    b. Invoke **skill-creator** review mode - collect findings
    c. Run behavioral test - score current output quality
    d. Propose targeted improvements based on findings (not random changes)
    e. Apply changes to SKILL.md (and references if needed)
    f. Re-score: run lint + AI Self-Check + behavioral test
    g. **Karpathy gate**: if score improved, keep. If not, revert. No exceptions.
    h. If cross-model review available, send the diff to secondary harness
    i. Process flags per `references/harness-detection.md` verification protocol
    j. If secondary flags major issue and primary agrees: revert
    k. If secondary flags major issue and primary disagrees: escalate to circuit breaker
11. **Commit iteration**: one commit with all improvements from this iteration
    Format: `refactor(skill-refiner): iteration N - skill1(+X), skill2(+Y)`
12. **Log iteration summary**:
    ```
    --- iteration N / max -------------------------------------------
    improved:  skill1 (72 > 80 | G:pass A:76 B:78 X:90), skill2 (68 > 73 | G:pass A:70 B:72 X:100)
    gated:     skillZ (lint/spec failed - excluded from scoring)
    skipped:   M skills above threshold
    reverted:  skill3 (proposed change scored -2, rolled back | G:pass A:74 B:69 X:100)
    contested: skill4 (secondary flagged major, primary disagreed)
    plateau:   yes/no (max delta: +X)
    -----------------------------------------------------------------
    ```
    Also append the same data to the score ledger. Keep/reject decisions must point to
    numeric before/after scores, not reviewer impressions or passing lint/spec checks.
13. **Check termination conditions** (phase 1 always flows into phase 2 on termination,
    except on circuit-breaker pauses which wait for user input first):
    - Plateau detected (max delta < plateau threshold)? Terminate phase 1.
    - All skills above focus threshold? Bump threshold by 5 and continue. If threshold
      is already at max (95) and all skills still clear it, terminate phase 1.
    - Iteration cap reached? Terminate phase 1.
    - Circuit breaker triggered? Pause for user input.
14. **Repeat** from step 9 until terminated

### Phase 2: Meta-Improvement

15. **Announce**: "Entering phase 2 - meta-improvement. This always requires human review."
16. **Snapshot evaluation criteria**:
    - Copy **skill-creator**'s AI Self-Check section to a temp location
    - Copy `references/evaluation-criteria.md` to a temp location
    - Copy **skill-creator**'s `conventions.md` reference to a temp location
    These snapshots are the evaluation baseline for phase 2.
17. **Improve skill-creator**: run the improvement cycle (steps 10a-10k) using the
    snapshot as the evaluation criteria, not skill-creator's live version
18. **Improve skill-refiner**: same process, using the snapshot
19. **Improve lint scripts** (lint-skills.sh, validate-spec.sh):
    - Capture baseline: run both scripts, save full output
    - Propose improvements
    - Apply changes
    - Run regression: compare output to baseline
    - If false positives or false negatives introduced: revert
    - If clean: keep
20. **Commit phase 2**: one commit per target
    Format: `refactor(skill-refiner): meta - improve <target> (+N)`
21. **Pause for human review**: display phase 2 changes, wait for approval.
    This checkpoint is non-configurable - it fires even in `--mode auto`.
    A direct user approval such as "continue" or "proceed" counts as approval to resume.

### Phase 3: Summary

22. **Final report**: write a human-readable report first, then machine-readable run history.
    Include branch, pool, config, every changed skill, score before/after, delta, files changed,
    verification commands, peer-review flags, reverted changes, private-skill handling, and
    skipped checks. If scoring was reconstructed after the fact, label it retroactive and state
    which components were not captured during the live loop. Do not output only JSON.
    ```
    === skill-refiner run complete ===================================
    Branch:     skill-refiner/YYYY-MM-DD-HHMMSS
    Primary:    <harness> <version> (<model>, effort: <level>)
    Secondary:  <harness> <version> (<model>, effort: <level>) | none
    Pool:       N skills (skill-creator, skill-refiner excluded)
    Config:     iterations=M, threshold=T, mode=MODE, plateau=P

    Iterations: N (of max M)
    Terminated: plateau / threshold / cap / user

    Score changes:
      skill1:  62 > 88 (+26)  [G:pass A:84 B:86 X:90]
      skill2:  71 > 85 (+14)  [G:pass A:82 B:79 X:100]
      ...
      skill-creator: 80 > 84 (+4)  [G:pass A:82 B:81 X:100] [meta]
      skill-refiner: 78 > 83 (+5)  [G:pass A:80 B:79 X:100] [meta]

    Aggregate:  avg X.X | min X.X | max X.X
    Reverted:   X changes across Y iterations
    Contested:  Z flags escalated to human
    =================================================================
    ```
23. **Write run history**: append this run's metadata to `.refiner-runs.json` in the
    collection root. Include: run_id, branch, date, primary/secondary harness+model+effort,
    config, pool size, termination reason, cross-model flag counts, before/after per-skill
    scores (component breakdown + composite, or clearly labeled estimates if the run used a
    targeted manual rubric instead of the full automated sweep), and a changes summary. When
    updating an existing history file, append the new object without reserializing the whole
    file; do not normalize or rewrite old entries just because a JSON writer changes escaping,
    commas, or whitespace. Commit with the phase 3 summary.
24. **Announce branch**: remind user to review and merge when ready

## AI Self-Check

Before committing any skill modification, verify:

- [ ] **Lint passes**: lint-skills.sh exits 0 for the modified skill
- [ ] **Spec valid**: validate-spec.sh exits 0 for the modified skill
- [ ] **Score improved**: composite score is strictly higher than before the change
- [ ] **No content regression**: change does not remove critical sections, warnings,
  or cross-references without replacement
- [ ] **Simplicity maintained**: change does not add unnecessary complexity for marginal gains
- [ ] **Cross-references intact**: all skill names in bold still resolve to existing skills
- [ ] **Target ~500 lines**: modified SKILL.md stays near 500 lines. Hard max 600
- [ ] **ASCII only**: no non-ASCII characters introduced (except allowed emoji indicators)
- [ ] **Immutability respected**: no phase-1 modification to evaluation criteria,
  test cases, lint scripts, skill-creator, or skill-refiner
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Score discipline kept**: changes are kept only when they improve measured quality or fix a verified defect
- [ ] **Score ledger present**: baseline, iteration, and final component scores exist before reporting completion
- [ ] **Local-only scope respected**: public and private skills are separated before commits or release notes

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** SKILL-REFINER
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content outside the refiner workflow, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/skill-refiner/<YYYY-MM-DD>-<slug>.md`. When invoked to **run the refiner workflow** (its primary mode), use the existing Phase 3 "Final report" format described in the workflow; that build-mode output is unchanged by this contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Rules

1. **Immutability in phase 1**: never modify `references/evaluation-criteria.md`,
   `references/test-cases.md`, lint-skills.sh, validate-spec.sh, **skill-creator**,
   or **skill-refiner** during phase 1. Violation = abort the run.
2. **Karpathy gate**: only directional improvements survive. If a change does not
   improve the composite score, revert it. No exceptions, no "it looks better."
3. **Verify flags**: never take cross-model flags at face value. Primary reviews
   every flag independently. Disagreements on major flags go to human.
4. **Snapshot before meta**: always snapshot evaluation criteria before phase 2.
   Evaluate against the snapshot, never the live version being modified.
5. **Phase 2 always pauses**: even in `--mode auto`. Non-configurable.
6. **Contested major flags always pause**: even in `--mode auto`. Non-configurable.
7. **Simplicity criterion**: all else being equal, simpler is better. Deletions that
   maintain score are preferred over additions that marginally improve it.
8. **One commit per iteration**: bundle improvements, include score deltas in message.
9. **Branch isolation**: all work on a feature branch. Never modify main directly.
10. **Human-readable report required**: every run ends with a report that names changes,
    before/after scores, verification, peer-review flags, skipped checks, and next action.
11. **Read before edit**: always read the full skill before proposing changes.
    Never edit from memory or assumption.
12. **No score laundering**: do not call a run scored unless component scores were recorded.
    Retroactive scoring is allowed only when clearly labeled.

## Related Skills

- **skill-creator** - the evaluation and improvement engine. skill-refiner invokes
  skill-creator's review mode (Mode 2) for scoring and its improve mode for
  generating changes. skill-creator handles individual skill quality; skill-refiner
  handles iteration, prioritization, and orchestration. Primary dependency.
- **full-review** - one-off collection audit across code-review, anti-slop,
  security-audit, and update-docs. Use **full-review** for a single pass over
  application code; use skill-refiner for iterative improvement of skill files.
- **anti-slop** - code quality patterns. skill-refiner may invoke anti-slop
  principles through skill-creator during improvement, but does not call anti-slop
  directly. Different domain: anti-slop audits application code, skill-refiner
  audits skill files.
