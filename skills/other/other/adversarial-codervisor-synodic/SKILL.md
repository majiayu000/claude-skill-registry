---
name: adversarial
description: "Generative-adversarial coordination — locks a generator and critic agent in an escalating quality loop. The critic actively tries to break the generator's output with increasing sophistication. Quality emerges from adversarial pressure, not checklist compliance. Use when you need deep quality hardening beyond standard review, or when the user invokes /adversarial run <spec-path>."
---

# Generative-Adversarial Skill

> **Governance:** This skill implements the Harness governance protocol.
> See [HARNESS.md](../../HARNESS.md) for the evaluation model, checkpoint protocol,
> and feedback taxonomy. Adversarial's checkpoint map:
> - Step 3 ATTACK rounds → Layer 2 (escalating AI critic)
> - Step 4 TERMINATION check → Layer 1 (algorithmic convergence)
> - Step 5 Escalate → Layer 3

Lock a generator and critic agent in an escalating quality loop. The critic doesn't just review — it *actively tries to break* the generator's output. The generator doesn't just fix — it *anticipates and preempts* the critic's attack patterns. Quality emerges from adversarial pressure, not checklist compliance.

**This is not code review.** Human review has social dynamics — reviewers don't want to seem hostile, authors get defensive. Agents have no ego. The adversarial pressure can be maximally intense without social cost.

**Agent property exploited:** No fatigue + lossless critique — agents maintain consistent quality across arbitrarily many review rounds without ego, defensiveness, or cognitive degradation.

## Usage

```
/adversarial run <spec-path> [--max-rounds N] [--escalation progressive|fixed|random]
```

Examples:
```
/adversarial run specs/051-api-endpoint/README.md
/adversarial run specs/051-api-endpoint/README.md --max-rounds 6 --escalation progressive
```

## Configuration

Defaults can be overridden by placing an `.adversarial.yaml` in the repo root:

```yaml
adversarial:
  max_rounds: 5                         # Hard cap on iteration count (default: 5)
  escalation: progressive               # progressive | fixed | random
  termination:
    consecutive_clean_rounds: 2          # Rounds with no new issues to stop (default: 2)
  critic_modes:                          # Escalation ladder (order matters for progressive)
    - syntax-and-types
    - edge-cases
    - concurrency-safety
    - adversarial-inputs
    - semantic-analysis
```

## Escalation Ladder

| Round | Critic Mode | Description |
|-------|-------------|-------------|
| 1 | `syntax-and-types` | Surface-level correctness: types, signatures, null checks |
| 2 | `edge-cases` | Boundary conditions: empty inputs, overflow, off-by-one |
| 3 | `concurrency-safety` | Race conditions, deadlocks, resource contention |
| 4 | `adversarial-inputs` | Malformed data, injection attempts, resource exhaustion |
| 5+ | `semantic-analysis` | Logic errors, invariant violations, specification gaps |

## Escalation Modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| `progressive` | Critic difficulty increases each round following the ladder | Default — most efficient for iterative hardening |
| `fixed` | Critic uses the same attack level every round | When targeting a specific quality dimension |
| `random` | Critic randomly selects attack level each round | When testing robustness against unpredictable challenge |

## Generator-Critic Contract

The adversarial loop works because both roles follow a contract:

**Generator MUST:**
- Produce a complete, testable artifact each round
- Address all issues from the previous round
- Not suppress or ignore critic feedback

**Critic MUST:**
- Provide specific, reproducible issues (not vague complaints)
- Escalate difficulty as configured
- Report "clean" honestly when no issues are found
- Provide concrete failing test cases where possible, not abstract objections

## Orchestration Protocol

When invoked, execute the following steps **exactly**:

### Step 1 — Initialize

1. Read the spec at `<spec-path>`.
2. Generate a work ID: `adversarial-{unix-timestamp}` (e.g., `adversarial-1710600000`).
3. Create `.adversarial/{work-id}/` directory.
4. Initialize `manifest.json`:
   ```json
   {
     "id": "{work-id}",
     "spec": "{spec-path}",
     "status": "generating",
     "rounds": [],
     "metrics": {}
   }
   ```
5. Read `.adversarial.yaml` from the repo root if it exists and override defaults.
6. Record the start time for cycle-time measurement.

### Step 2 — Generate (initial artifact)

Spawn a **general-purpose subagent** with `isolation: worktree`:

```
Agent(
  subagent_type: "general-purpose",
  isolation: "worktree",
  prompt: <GENERATE_PROMPT below>
)
```

**GENERATE_PROMPT:**

> You are the GENERATOR in a generative-adversarial coding loop.
> Your output will be attacked by a critic agent that actively tries to break it.
> Anticipate attacks and build robust code from the start.
>
> ## Spec
> {full spec content}
>
> ## Previous round feedback (if any)
> {attack results from previous critic round, or "None — this is the first generation."}
>
> ## Critic mode for next round
> {the critic mode that will be used to attack this output}
>
> ## Instructions
>
> 1. Read the spec carefully.
> 2. If there is previous feedback, address EVERY issue raised by the critic.
> 3. Anticipate the upcoming critic mode and preemptively harden your code.
> 4. Run any tests mentioned in the spec.
> 5. Commit all changes with prefix `adversarial(gen-r{round}):`.
> 6. After committing, run `git diff main...HEAD --stat`.
>
> ## Output format
>
> ```
> === GENERATE REPORT ===
> ROUND: {round number}
> STATUS: COMPLETE | PARTIAL
> FILES: {comma-separated list of files changed}
> TESTS: PASS | FAIL | SKIPPED
> COMMIT: {short SHA}
> WORKTREE_BRANCH: {branch name}
> HARDENING: {what you did to anticipate the next attack}
> === END GENERATE REPORT ===
> ```

After the generate subagent returns:
- Parse the GENERATE REPORT.
- Record in the manifest under the current round.
- Run STATIC GATE (Step 2.5).

### Step 2.5 — STATIC GATE

After GENERATE completes, run project-level static checks (same as Factory):

1. **Detect languages changed** from the GENERATE REPORT files list:
   - **Rust** (`.rs`): `cargo check` and `cargo clippy -- -D warnings`
   - **TypeScript/JavaScript** (`.ts`, `.tsx`, `.js`, `.jsx`): `tsc --noEmit` and `eslint`
   - **Python** (`.py`): `pyright` and `ruff check`

2. **Custom rules**: Run `.harness/rules/` scripts against the diff.

3. **If failures:** Route back to Step 2 with failures as rework feedback. Cap at 2 static rework attempts (same as Factory). Track as `static_rework_count`.

4. **If pass:** Proceed to Step 3 (Attack).

### Step 3 — Attack (critic round)

Spawn a **general-purpose subagent** (no worktree — read-only critic):

```
Agent(
  subagent_type: "general-purpose",
  prompt: <ATTACK_PROMPT below>
)
```

**ATTACK_PROMPT:**

> You are the CRITIC in a generative-adversarial coding loop.
> Your job is to ACTIVELY TRY TO BREAK the generator's output.
> You are NOT a polite code reviewer — you are an adversarial attacker.
>
> ## Original spec
> {full spec content}
>
> ## Current round: {round number}
> ## Critic mode: {critic_mode}
> ## Escalation: {escalation mode}
>
> ## Changes to attack
> Run `git diff main...{worktree-branch}` to see all changes made by the generator.
> Also read the changed files directly for full context.
>
> ## Previous attack results (if any)
> {issues from previous rounds and whether they were fixed}
>
> ## Attack instructions by mode
>
> **syntax-and-types:** Check type correctness, missing null/undefined checks,
> wrong return types, incorrect function signatures, missing imports.
>
> **edge-cases:** Test boundary conditions — empty inputs, single-element
> collections, max/min values, unicode strings, zero-length strings, negative
> numbers, overflow conditions, off-by-one errors.
>
> **concurrency-safety:** Look for race conditions, deadlocks, missing locks,
> non-atomic read-modify-write sequences, shared mutable state without
> synchronization, resource leaks under concurrent access.
>
> **adversarial-inputs:** Construct SQL injection payloads, XSS vectors,
> path traversal attacks, oversized payloads, malformed JSON/XML,
> time-of-check-time-of-use attacks, resource exhaustion inputs.
>
> **semantic-analysis:** Analyze business logic correctness, invariant
> violations, specification gaps, implicit assumptions that could fail,
> missing error recovery paths, incorrect state machine transitions.
>
> ## Rules
>
> 1. You MUST try hard to find issues. Do not be lenient.
> 2. Every issue must be specific and reproducible — include a test case
>    or concrete scenario that demonstrates the problem.
> 3. Do NOT raise style or preference issues — only functional problems.
> 4. Re-check ALL issues from previous rounds to verify they were actually fixed.
>    Report any regressions.
> 5. If you genuinely cannot find any issues at this mode level, report CLEAN.
>    Do not fabricate issues.
>
> ## Output format
>
> If issues found:
> ```
> === ATTACK REPORT ===
> ROUND: {round number}
> MODE: {critic_mode}
> VERDICT: ISSUES_FOUND
> ISSUES:
> - [category] {specific description}
>   TEST_CASE: {concrete input or scenario that demonstrates the problem}
> - [category] {specific description}
>   TEST_CASE: {concrete input or scenario}
> REGRESSIONS: {list of previously-fixed issues that reappeared, or "none"}
> SUMMARY: {one-line summary}
> === END ATTACK REPORT ===
> ```
>
> If no issues found:
> ```
> === ATTACK REPORT ===
> ROUND: {round number}
> MODE: {critic_mode}
> VERDICT: CLEAN
> SUMMARY: {one-line summary of what was checked}
> === END ATTACK REPORT ===
> ```

After the attack subagent returns:
- Parse the ATTACK REPORT.
- Record in the manifest under the current round.
- Proceed to Step 4 (Termination Check).

### Step 4 — Termination Check

Evaluate whether to continue or stop the adversarial loop:

1. **Check consecutive clean rounds.** Count how many consecutive CLEAN verdicts have been returned.
   - If `consecutive_clean_rounds >= termination.consecutive_clean_rounds` (default 2): **TERMINATE — quality threshold met.** Proceed to Step 6.

2. **Check round cap.** If current round >= `max_rounds`: **TERMINATE — round cap reached.** Proceed to Step 6 if last round was CLEAN, otherwise Step 7 (Escalate).

3. **Check quality plateau.** If the last 3 rounds all found issues but the issue count is not decreasing: **TERMINATE — plateau detected.** Proceed to Step 7 (Escalate).

4. **Otherwise:** Determine the next critic mode:
   - `progressive`: advance to the next mode in the `critic_modes` ladder. If at the end, stay on the last mode.
   - `fixed`: use the same mode.
   - `random`: randomly select from `critic_modes`.

   Route back to Step 2 (Generate) with the attack results as feedback.

### Step 5 — (reserved for future use)

### Step 6 — Create PR

1. Push the build branch: `git push -u origin adversarial/{work-id}`
2. Create a PR using `gh pr create`:
   ```
   gh pr create \
     --title "adversarial: {spec title}" \
     --body "## Adversarial Hardening Report

   **Spec:** {spec-path}
   **Work ID:** {work-id}
   **Rounds completed:** {total rounds}
   **Termination reason:** {consecutive clean | round cap}
   **Escalation mode:** {escalation}

   ## Round History
   {table: round, critic_mode, verdict, issue_count}

   ## Issues Found & Fixed
   {categorized list of all issues discovered and resolved}

   ## Hardening Coverage
   {which critic modes were applied and passed clean}

   ---
   *Produced by the Synodic adversarial skill.*"
   ```
3. Update the manifest with final status and metrics.
4. Report success to the user with the PR URL.

### Step 7 — Escalate

If the round cap is reached without achieving clean termination:

1. Update the manifest: `"status": "escalated"`.
2. Report to the user:
   - The adversarial loop did not achieve clean termination in {max_rounds} rounds.
   - Show remaining issues from the last attack round.
   - The build branch `adversarial/{work-id}` contains the latest hardened version.
3. Do NOT create a PR.

### Step 8 — Finalize Manifest

After Step 6 or Step 7, update `.adversarial/{work-id}/manifest.json` with:

```json
{
  "metrics": {
    "cycle_time_seconds": 0,
    "total_rounds": 0,
    "static_rework_count": 0,
    "termination_reason": "consecutive_clean|round_cap|plateau",
    "issues_found_total": 0,
    "issues_by_category": {"edge-cases": 0, "concurrency-safety": 0},
    "regressions_detected": 0,
    "critic_modes_passed_clean": ["syntax-and-types", "edge-cases"]
  }
}
```

### Step 8b — Persist to GovernanceLog

Append a summary record to `.harness/adversarial.governance.jsonl`:

```json
{
  "work_id": "adversarial-...",
  "source": "adversarial",
  "spec": "specs/...",
  "timestamp": "<ISO 8601>",
  "status": "hardened|escalated",
  "total_rounds": 0,
  "static_rework_count": 0,
  "termination_reason": "consecutive_clean|round_cap|plateau",
  "escalation": "progressive",
  "rounds": [
    {"round": 1, "mode": "syntax-and-types", "verdict": "ISSUES_FOUND", "issue_count": 2},
    {"round": 2, "mode": "edge-cases", "verdict": "CLEAN", "issue_count": 0}
  ],
  "issues": [
    {"round": 1, "category": "syntax-and-types", "description": "...", "fixed": true},
    {"round": 1, "category": "syntax-and-types", "description": "...", "fixed": true}
  ],
  "regressions_detected": 0,
  "critic_modes_passed_clean": ["syntax-and-types", "edge-cases"],
  "cycle_time_seconds": 0
}
```

After appending, commit the updated `governance.jsonl` as part of the adversarial run.

## Parsing Rules

- GENERATE REPORT is between `=== GENERATE REPORT ===` and `=== END GENERATE REPORT ===`.
- ATTACK REPORT is between `=== ATTACK REPORT ===` and `=== END ATTACK REPORT ===`.
- If a subagent response doesn't contain the expected block, log the raw response in the manifest and treat it as FAILED.

## Important Notes

- **The critic is adversarial, not hostile.** It follows the contract: specific, reproducible issues with concrete test cases. No vague complaints or style preferences.
- **Never adversarial within adversarial.** Inner critic criticizes outer critic — meta-critique without grounded production. This is the one invalid composition.
- `.adversarial/` directory is gitignored (per-run manifests are local artifacts). Governance logs go to `.harness/adversarial.governance.jsonl`.
- The generator runs in `isolation: worktree` so it has its own git branch.
- The critic runs WITHOUT worktree — read-only adversarial review. This ensures context isolation (critic cannot see generator's reasoning).
- **Regression tracking** is mandatory. Each attack round re-checks ALL previous issues. Regressions are tracked separately in the manifest.
- **Quality plateau detection** prevents infinite loops where the generator and critic cycle without improvement. If issue count doesn't decrease over 3 rounds, terminate.
- **Static gate** runs between generate and attack rounds, same as Factory. Static rework does not count toward the adversarial round limit.

## Composability

| Composition | Valid | Rationale |
|-------------|-------|-----------|
| Swarm → Adversarial | Yes | Each swarm branch gets adversarial hardening before merge |
| Factory → Adversarial | Yes | Factory BUILD output gets deep adversarial hardening |
| Fractal → Adversarial | Yes | Each fractal leaf's output is quality-checked adversarially |
| Pipeline → Adversarial | Yes | Each pipeline stage gets adversarial hardening |
| **Adversarial → Adversarial** | **No** | Inner critic criticizes outer critic — meta-critique without grounded production |

## Comparison with Other Skills

| Aspect | Factory | Fractal | Swarm | Adversarial |
|--------|---------|---------|-------|-------------|
| Shape | Linear pipeline | Recursive tree | Parallel fan-out | Iterative loop |
| Quality model | Single review | Bounded rework | Best-of-N | Escalating attack |
| Parallelism | Sequential | Parallel leaves | Parallel branches | Sequential rounds |
| Strength | Efficient review | Complex decomposition | Strategy exploration | Deep hardening |
| When to use | Standard implementation | Task too large | Multiple approaches | Security/correctness critical |
