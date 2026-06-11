---
name: toolkit-evolution
description: "Closed-loop toolkit self-improvement: discover gaps, diagnose, propose, critique, build, test, evolve."
user-invocable: true
argument-hint: "<optional: focus area like 'routing' or 'hooks'>"
command: evolve
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - Skill
routing:
  triggers:
    - "evolve toolkit"
    - "improve the system"
    - "self-improve"
    - "toolkit evolution"
    - "what should we improve"
    - "find improvement opportunities"
    - "discover skill gaps"
    - "what skills are missing"
    - "systematic improvement"
  pairs_with:
    - multi-persona-critique
    - skill-eval
  complexity: Complex
  category: meta-tooling
---

# Toolkit Evolution

Schedulable (nightly) or manually-invoked 7-phase pipeline for continuous toolkit self-improvement. Discovers gaps, diagnoses problems from evidence, proposes solutions, critiques via multi-persona review, builds winners on isolated branches, A/B tests, and promotes via PR.

Nightly sibling of `auto-dream` (2:07 AM consolidates memories; 3:07 AM this skill diagnoses and builds). They feed each other: dream's graduated learnings inform evolution's diagnosis; evolution's results become dream's next input.

Invoke: `/evolve`, `/evolve routing`, `/evolve hooks`, `/evolve --discover`. Cron setup in `references/evolve-preferred-patterns.md` § Scheduling.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| running DISCOVER/DIAGNOSE commands: learning DB queries, git scan, drift checks | `diagnose-scripts.md` | Loads detailed guidance from `diagnose-scripts.md`. |
| writing the evolution cycle report | `evolution-report-template.md` | Loads detailed guidance from `evolution-report-template.md`. |
| Phase 3 CRITIQUE fallback; failure modes, error handling, cost estimates, cron setup | `evolve-preferred-patterns.md` | Loads detailed guidance from `evolve-preferred-patterns.md`. |
| Phase 6 EVOLVE: PR creation, merge, branch cleanup, learning records | `evolve-scripts.md` | Loads detailed guidance from `evolve-scripts.md`. |

## Instructions

### Phase 0: DISCOVER -- Find what's missing

**Goal**: Identify skills, agents, or capability categories the toolkit should have but doesn't. While later phases improve existing components, this phase finds entirely new capabilities the toolkit is missing.

**Frequency**: Monthly, not every run. The DISCOVER phase only executes if:
- `--discover` flag is passed explicitly, OR
- It has been 30+ days since the last discovery run

Check the last discovery run date using the frequency check command from `references/diagnose-scripts.md` § Discovery Frequency Check.

If neither condition is met, skip directly to Phase 1.

**Step 1: Gather briefing data**

Collect current toolkit state using the briefing data commands from `references/diagnose-scripts.md` § DISCOVER Step 1. Brief all 5 perspective agents with the same baseline.

**Step 2: Dispatch 5 perspective agents in parallel**

See `references/evolve-preferred-patterns.md` § Phase 0 DISCOVER for the full agent table and proposal format. Dispatch all 5 simultaneously.

**Step 3: Deduplicate and filter** -- remove duplicates of existing skills (check `skills/INDEX.json`), remove proposals with no evidence (require at least one concrete data point), group similar proposals and note convergent evidence.

**Step 4: Feed into DIAGNOSE** -- append surviving proposals to the Phase 1 opportunity list with source tagged `[DISCOVER]`.

**Step 5: Save discovery report** to `evolution-reports/discovery-{YYYY-MM-DD}.md` (run `mkdir -p evolution-reports` first). Include briefing data, all proposals, filtering rationale, forwarded proposals, and date stamp.

**Gate**: Discovery report saved. Proposals forwarded to Phase 1. Proceed to DIAGNOSE.

---

### Phase 1: DIAGNOSE -- Find improvement opportunities

**Goal**: Identify 5-10 evidence-backed improvement opportunities from multiple data sources.

**Step 1: Query the learning database for recent failures and routing mismatches**

Run the 4 search queries from `references/diagnose-scripts.md` § DIAGNOSE Step 1.

Look for: routing decision patterns, recurring routing failures and mismatches, skills that consistently underperform, error patterns without automated fixes.

**Step 2: Scan recent git history for patterns**

Run the git history commands from `references/diagnose-scripts.md` § DIAGNOSE Step 2.

**Step 3: Check auto-dream reports for accumulated insights**

Run the dream report check from `references/diagnose-scripts.md` § DIAGNOSE Step 3, then read the most recent dream-analysis file.

**Step 3b: Cross-validate dream insights against current state**

Before treating any dream insight as a proposal signal, verify it still reflects the current repo. Use the cross-validation commands from `references/diagnose-scripts.md` § DIAGNOSE Step 3b.

Mark an insight as STALE if: (a) it names a file that no longer exists, OR (b) it claims recent activity but `git log` shows nothing in the past 7 days.

**Step 4: Check routing-table drift**

Skills present in `skills/INDEX.json` but absent from the routing manifest represent a documentation gap. Run the routing-drift check from `references/diagnose-scripts.md` § DIAGNOSE Step 4.

**Step 4b: Check for orphaned ADR session files**

Run the orphaned session check from `references/diagnose-scripts.md` § DIAGNOSE Step 4b. Flag any found -- do not remove automatically.

**Step 4c: Scan for registered stub hooks**

Run the stub hook audit from `references/diagnose-scripts.md` § DIAGNOSE Step 4c. Flag any stub hook as a cleanup opportunity.

**Step 4d: Check usage and governance signals**

Run the usage and governance commands from `references/diagnose-scripts.md` § DIAGNOSE Step 4d. Feed dormant skills/agents into gap discovery (tag `[USAGE]`) and cluster unresolved governance events into the "what's failing" diagnosis (tag `[GOVERNANCE]`).

**Step 5: Dedup against prior proposals**

Load `references/evolution-history.md`. Check each opportunity against: (a) Rejected Proposals -- do not re-propose unless the reopen condition is met, (b) Shelved Proposals -- re-propose only if the reactivation condition is now satisfied, (c) Distilled Lessons -- apply the learned criteria to filter weak proposals early.

**Step 6: Narrow by focus area (if provided)**

If the user specified a focus area (e.g., "routing", "hooks", "agents"), filter all findings to that domain.

**Step 7: Compile opportunity list**

Output a numbered list of 5-10 improvement opportunities. Each entry must include:
- **What**: One-sentence description of the problem or gap
- **Evidence**: Which data source surfaced it (learning DB entry, git churn, dream report)
- **Impact**: Estimated user impact (High/Medium/Low)

**Gate**: At least 3 evidence-backed opportunities identified. If fewer than 3, expand the time window or broaden the data sources. Do not proceed with speculative opportunities that lack evidence.

---

### Phase 2: PROPOSE -- Generate concrete solutions

**Goal**: Transform opportunities into actionable proposals with clear scope.

**Step 1: Generate proposals**

For each opportunity from Phase 1, propose 1-2 concrete solutions. Each proposal must be actionable:
- "Add failure mode X to agent Y's prompt" (not "improve agent Y")
- "Create a reference file for Z in skill W" (not "enhance skill W")
- "Modify Phase 3 of skill V to include check for Q" (not "make skill V better")

**Step 2: Estimate effort**

| Effort | Definition |
|--------|-----------|
| Small | Single file edit, <30 lines changed |
| Medium | 2-5 files, new reference or script, <200 lines |
| Large | New skill or agent, multiple components, >200 lines |

**Step 3: Check for duplicates**

```bash
cat skills/INDEX.json | python3 -c "import sys,json; idx=json.load(sys.stdin); [print(k,'-',v.get('description','')) for k,v in idx.get('skills',{}).items()]" 2>/dev/null || echo "INDEX.json parse failed -- check manually"
```

Drop any proposal that duplicates an existing skill or capability.

**Step 4: Rank proposals**

Rank by: (Impact score) x (1 / Effort score), where High=3, Medium=2, Low=1 and Small=1, Medium=2, Large=3.

Output: ranked list of 5-10 proposals, each with proposal description, scope, effort, and expected outcome.

**Gate**: All proposals are concrete (specific files/skills named), non-duplicative (verified against INDEX.json), and ranked. Proceed with the top 5.

---

### Phase 3: CRITIQUE -- Multi-persona evaluation

**Goal**: Evaluate proposals from multiple perspectives to surface blind spots.

**Step 1: Check for multi-persona-critique skill**

```bash
test -f skills/research/multi-persona-critique/SKILL.md && echo "AVAILABLE" || echo "NOT AVAILABLE"
```

**Step 2a: If multi-persona-critique is available**

```
Skill(skill="multi-persona-critique", args="Evaluate these toolkit improvement proposals: {proposals}")
```

**Step 2b: If NOT available -- use inline fallback**

See `references/evolve-preferred-patterns.md` § Phase 3 Inline Critique Fallback for the 3-agent dispatch prompts and scoring table.

**Step 3: Synthesize consensus**

For each proposal, average persona scores (STRONG=3, MODERATE=2, WEAK=1):
- Score >= 2.5 = STRONG consensus
- Score 1.5-2.4 = MODERATE consensus
- Score < 1.5 = WEAK consensus (shelve)

**Gate**: All personas have reported. Synthesis complete. At least 1 proposal rated STRONG. If no STRONG proposals, revisit Phase 2 with the critique feedback, or report to user that no high-confidence improvements were found this cycle.

**On early exit (no STRONG proposals): always record to the learning DB before stopping.** See `references/evolve-scripts.md` § Early Exit Record for the learning-db command template.

---

### Phase 4: BUILD -- Implement winners

**Goal**: Implement the top 1-3 STRONG-rated proposals on isolated feature branches.

**Constraint**: Maximum 3 implementations per cycle. Focus over breadth.

**Step 1: Select winners**

Take the top 1-3 proposals rated STRONG by consensus. Do not pad with MODERATE proposals.

**Step 2: Dispatch implementation agents**

For each winner, dispatch an implementation agent in an isolated context. See `references/evolve-scripts.md` § Build Dispatch for the proposal-type to implementation-approach table.

Each implementation must create a feature branch `feat/evolve-{proposal-slug}` and commit with a descriptive message.

**Step 3: Validate** -- run `python3 -m scripts.skill_eval.quick_validate skills/{skill-name}`, `python3 -m py_compile {script}`, and `bash -n {script}` on each implementation.

**Gate**: All implementations committed on feature branches. Basic validation passed. Proceed to testing.

---

### Phase 5: VALIDATE -- A/B test implementations

**Goal**: Empirically verify that each implementation improves outcomes vs baseline.

**Step 1: Create test cases**

For each implementation, create 3-5 realistic test prompts that exercise the changed behavior.

**Step 2: Run comparisons**

See `references/evolve-scripts.md` § Validate Run for the skill-eval command and manual fallback pattern.

**Step 3: Evaluate results**

Win condition for each implementation:
- 60%+ of test cases show improvement on at least one dimension
- No dimension regressed by more than 1 point (on a 5-point scale)
- No new failures introduced

**Gate**: All implementations tested. Win/loss determined for each. Evidence recorded.

---

### Phase 6: EVOLVE -- Promote winners and record learnings

**Goal**: Ship winners via PR, record all outcomes in the learning database.

**Step 1: Handle winners (WIN status)**

For each winning implementation, create a PR using the template from `references/evolve-scripts.md` § Step 1, then merge. After creating the PR, run pr-review to validate, then merge.

The multi-persona critique + A/B testing gate is the review. Auto-merge is safe because the validation happened before this step.

**Step 1b: Clean up the feature branch after merge**

Use the cleanup commands from `references/evolve-scripts.md` § Step 1b.

**Step 2: Handle losers (LOSS status)**

Record what was tried and why it failed using the failure template from `references/evolve-scripts.md` § Step 2.

**Step 3: Record the full cycle**

Record using the full cycle template from `references/evolve-scripts.md` § Step 3.

**Step 4: Write evolution report**

Write the dated report to `evolution-reports/evolution-report-{YYYY-MM-DD}.md` using the template in `references/evolution-report-template.md`. See setup command in `references/evolve-scripts.md` § Step 4.

**Gate**: Winners merged. Learnings recorded for all proposals (wins and losses). Evolution report written. Cycle complete.

---

## Reference Loading

| Signal | Load |
|--------|------|
| Running Phase 0 DISCOVER (frequency check, briefing data commands needed) | `references/diagnose-scripts.md` |
| Running Phase 1 DIAGNOSE (Steps 1-4c commands needed) | `references/diagnose-scripts.md` |
| Phase 0 perspective agent table, proposal format | `references/evolve-preferred-patterns.md` |
| Phase 3 inline critique fallback (multi-persona not available) | `references/evolve-preferred-patterns.md` |
| Failure modes, error handling, cost estimate, cron scheduling | `references/evolve-preferred-patterns.md` |
| Running Phase 6 EVOLVE (PR template, merge, cleanup, learning DB commands) | `references/evolve-scripts.md` |
| Writing or reading the evolution report | `references/evolution-report-template.md` |
| Running Phase 1 DIAGNOSE (dedup against prior proposals) or Phase 2 PROPOSE | `references/evolution-history.md` |

---

## References

- `references/evolution-report-template.md` -- Template for the evolution report
- `references/diagnose-scripts.md` -- Phase 0 and Phase 1 bash/Python commands
- `references/evolve-scripts.md` -- Phase 6 PR, merge, cleanup, and learning DB commands
- `references/evolve-preferred-patterns.md` -- Failure modes, error handling, cost, critique fallback, scheduling
- `references/evolution-history.md` -- Graduated proposal ledger, shelved conditions, rejected proposals, cycle summaries
- `skills/meta/auto-dream/SKILL.md` -- Nightly sibling: memory consolidation and learning graduation
- `skills/meta/skill-eval/SKILL.md` -- Skill testing and benchmarking
- `skills/research/multi-persona-critique/SKILL.md` -- Multi-persona evaluation (may not exist yet; inline fallback in references)
- `skills/meta/skill-creator/SKILL.md` -- Skill creation methodology
- `skills/meta/agent-comparison/SKILL.md` -- A/B testing methodology
- `skills/infrastructure/headless-cron-creator/SKILL.md` -- Cron job creation patterns
