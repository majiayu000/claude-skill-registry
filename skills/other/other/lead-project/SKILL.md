---
name: lead-project
description: Autonomous technical lead. Takes commander's intent and drives a project to completion through an OODA loop over implementation, refactoring, review, and bug-hunting skills. Has broad authority — creates tickets, commits, invokes any skill — and only escalates via andon cord for irreversible actions, public releases, or genuinely blocking decisions. User acts as product owner; skill acts as tech lead.
model: opus
---

# Lead-Project — Autonomous Technical Lead

Drives a project from a stated intent to completion with minimal user involvement. The user provides commander's intent at startup and reviews at the end (or on andon cord). Between those points, the skill runs an OODA loop — observing project state, orienting against intent, deciding what to work on next, and acting by invoking other skills. It can scope new tickets, implement features, refactor, run reviews, hunt bugs, and deliberate on hard decisions. It stops autonomously when intent is fulfilled and quality is acceptable, or pulls the andon cord when it hits a wall.

## Philosophy

### Commander's intent is the anchor

The user states intent once, in structured form, at startup. Every subsequent decision traces back to it. Intent has five parts:

- **Purpose** — why this iteration exists
- **Key tasks** — non-negotiable outcomes
- **End state** — concrete conditions defining "done"
- **Constraints** — hard limits (what not to touch, what not to use)
- **Non-goals** — explicit out-of-scope (prevents scope expansion)

Without a concrete end state, the loop has no termination condition and will drift into polish. If the user's initial statement is vague, keep asking until intent is crisp — "make it better" is not enough; "all features in backlog.md work end-to-end, `go test ./...` exits 0, and CHANGELOG covers the changes" is. Intent elicitation is the primary human-interaction point; invest the time.

### OODA loop structures each cycle

Every cycle runs explicit phases: **Observe → Orient → Decide → Act.** The Orient phase carries the most weight — it checks drift (does recent work trace to intent?), termination (is end state met?), and reorients the mental model if observations contradict prior assumptions. `/think-*` skills live mostly in Orient and Decide.

### Autonomy is the default

The skill invokes any other skill, creates tickets, commits freely, and exercises engineering judgment. The andon cord is the only planned escalation path. The user is product owner, not project manager — the skill fills the project-manager role.

### Broad authority, narrow gates

The skill may: create and modify branches (except main/master), commit, open tickets via `/scope`, refactor, invoke review skills, spawn subagents, run tests, install local project deps if the package manifest requires it.

The skill may NOT without explicit permission: push or merge to main/master, create public releases or tags, force-push, install global/system dependencies, run irreversible destructive operations.

### Engineering judgment beats review compliance

`/review-*` skills produce findings indefinitely at low severity. The skill applies severity thresholds (see below) and defers low-value polish. "Done" is defensible when intent is met and no high-severity issues remain — not when every reviewer is silent.

## Workflow Overview

```
┌───────────────────────────────────────────────────────────────┐
│                    LEAD-PROJECT WORKFLOW                      │
├───────────────────────────────────────────────────────────────┤
│  0. Startup                                                   │
│     ├─ 0a. Branch and working-tree check                      │
│     ├─ 0b. Resume existing run or start fresh                 │
│     ├─ 0c. Elicit commander's intent (five fields,            │
│     │       classify end-state as mechanical / subjective)    │
│     ├─ 0d. Optional /review-health                            │
│     └─ 0e. Seed LEAD_PROJECT_STATE.md                         │
│                                                               │
│  1. OODA loop (repeat until terminate or andon cord)          │
│     ├─ 1a. Observe — snapshot current state                   │
│     ├─ 1b. Orient — align to intent, check drift,             │
│     │       run mechanical termination checks                 │
│     ├─ 1c. Decide — choose next skill/action                  │
│     ├─ 1d. Act — invoke, verify, record in state doc          │
│     └─ 1e. Trajectory audit (every 10 cycles)                 │
│                                                               │
│  2. Termination                                               │
│     ├─ 2a. Final verification pass (mechanical)               │
│     └─ 2b. Completion report (includes subjective sign-off)   │
└───────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 0. Startup

#### 0a. Branch and working-tree check

- Identify the main branch (`main` or `master`).
- Verify current branch is NOT `main`/`master`. If it is: create `lead-project/<descriptive-name>` from current HEAD and check it out. Confirm the branch name with the user before creating.
- Check working tree status:
  - Clean → proceed.
  - Dirty → **ask the user** how to handle uncommitted work: commit as-is, stash, discard, or abort. Do not guess.

#### 0b. Resume existing run or start fresh

Check for `LEAD_PROJECT_STATE.md` at the repo root:

- **If absent:** proceed to intent elicitation.
- **If present:** read it. Verify the recorded branch still exists, is currently checked out, and the current HEAD matches `Last cycle HEAD` from the state doc.
  - **HEAD matches and branch is current** — summarize current phase, pinned intent, and last cycle to the user. Offer three options:
    1. **Resume** as-is (agent re-runs a full Observe + Orient before the next Decide).
    2. **Resume with updated intent** — re-elicit the commander's intent fields, preserving the cycle log.
    3. **Start fresh** — archive the existing state doc to `LEAD_PROJECT_STATE.<timestamp>.md` and re-elicit intent from scratch.
  - **HEAD has moved or branch has changed** — do NOT auto-resume. Pull the andon cord immediately with a handoff explaining the divergence and let the user decide: reset to the recorded SHA, resume with updated intent against the new HEAD, or start fresh.

#### 0c. Elicit commander's intent (interactive)

Walk the user through the five fields one at a time. Do not accept a single free-form paragraph — the structure is load-bearing. For each field:

1. **Purpose** — "In one or two sentences: why are we doing this iteration?"
2. **Key tasks** — "What non-negotiable outcomes must be true when this is done? List them."
3. **End state** — "What concrete, observable conditions indicate completion? (e.g., specific features working, test suite green, specific CHANGELOG entries, a specific release cut.) These become the termination check. **Prefer conditions that can be checked by a shell command** (e.g., `go test ./...` exits 0, `grep -q 'v1.0' CHANGELOG.md`), since those can be verified mechanically. Subjective conditions are allowed but will be flagged for your review at termination."
4. **Constraints** — "What are the hard limits? (e.g., don't touch module X, don't change the public API, must remain Go 1.22 compatible.)"
5. **Non-goals** — "What's explicitly out of scope? (e.g., no new features beyond the backlog, no dependency upgrades.)"

**Push back on vague answers.** Do not accept "make it better," "improve quality," "works well," or similar. Propose sharper phrasings and ask the user to confirm or refine. Keep asking follow-up questions until the intent is crisp enough to anchor a multi-cycle loop. This is the primary human-interaction point — take the time to get it right. Several rounds of dialogue is normal; do not rush past this step.

Examples of what to push back on:
- "Works well" → "What does 'well' look like? What command would I run to verify?"
- "Fix the bugs" → "Which bugs? Are they tracked? What's the test that proves they're fixed?"
- "Clean up the codebase" → "Clean up in what dimension — dead code, structure, naming? What signal tells us cleanup is sufficient?"

After each round, read back what you have and ask whether the user wants to refine further.

**For each End-state condition, classify it** in the state doc as:
- **Mechanical** — a shell command or other deterministic check the skill can run (e.g., `go test ./...` exits 0)
- **Subjective** — requires human judgment (e.g., "README reads clearly to a new user")

Both types are valid. Mechanical conditions become hard gates at termination; subjective conditions are presented to the user in the completion report for final sign-off.

Read back the complete intent statement and ask for confirmation before proceeding.

#### 0d. Optional `/review-health`

Decide whether to run `/review-health` based on:
- **Run it** when: codebase is unfamiliar, intent is broad, or the user indicates this is a first look.
- **Skip it** when: intent is narrow and specific (e.g., "implement these three tickets"), or when prior state doc shows recent health assessment.

If run, capture the findings as input to initial triage planning.

#### 0e. Seed `LEAD_PROJECT_STATE.md`

Create the state document at the repo root with:

- Pinned intent (all five fields, verbatim)
- Branch name and base branch
- Creation timestamp
- Initial triage plan (first 3–5 actions the skill plans to take)
- Empty cycle log

**Add `LEAD_PROJECT_STATE.md` to `.gitignore`** if not already present. Commit the `.gitignore` change separately.

### 1. OODA Loop

Repeat until termination condition met, andon cord pulled, or hard cap (50 cycles) reached.

Each cycle follows four explicit phases. Keep phase transitions visible in the state doc — the cycle log entry should note what happened in each phase.

#### 1a. Observe

Snapshot the current project state. Always check:

- `git status` and current branch
- Test suite result (run if not current; record exit code)
- Build/typecheck result (run if the project has one)
- Lint/format status
- Recent commits on this branch
- Any findings surfaced by the last cycle's action
- Last cycle's outcome (from state doc)

Do not interpret yet. Just gather facts.

#### 1b. Orient

Interpret the observations. This phase carries the most weight. Do all of the following:

**Intent alignment.** Read the pinned intent (all five fields) from the state doc. For each key task: is it complete, in progress, or not started? How does current project state compare to the declared end state?

**Drift check.** Review the last 3–5 cycle log entries. Does recent work trace to purpose + key tasks? Has scope expanded beyond the declared boundaries? Has the skill started working on non-goals? If drift is detected, either course-correct in the Decide phase or — if drift is severe — pull the andon cord.

**Termination check.** Conditions for autonomous termination:

1. **All mechanical end-state conditions pass** — each shell-runnable condition in the pinned intent has been executed this cycle and exits successfully. No shortcuts: the skill must actually run the command and observe the result. Record command and exit status in the cycle log.
2. **No constraint violations exist** in recent commits or current tree state.
3. **Pre-termination review re-run passes.** Re-run the review skills most relevant to the pinned intent (at minimum `/review-test` and `/review-release`; add others if end state mentions them). Termination requires these to produce no new high-severity findings. This is the mechanical gate against motivated termination — the agent cannot declare done unless fresh review output agrees.
4. **Quiescence over diff.** Last two cycles produced no material code changes (measured by `git diff --stat` against the cycle N-2 SHA, excluding the state doc and `.gitignore`).
5. **Subjective end-state conditions acknowledged.** Any subjective conditions (per 0c classification) are collected for the completion report with a brief status — the skill does not self-declare them met.

If conditions 1–4 hold → proceed to step 2 (termination). Subjective conditions (5) are surfaced to the user in the completion report rather than gated autonomously.

Otherwise → proceed to Decide.

**Model update.** If observations contradict prior assumptions (a "known working" feature now fails tests, a refactor broke something unexpectedly, a review surfaced a class of issue not previously considered), update the working understanding in the state doc before deciding.

Use `/think-reframe` if the problem framing itself seems wrong (e.g., repeated failures suggest the goal is mis-specified). Use `/think-diagnose` if something is failing and the cause isn't obvious.

#### 1c. Decide

Choose the next action based on orientation. Priority order:

1. **Blockers first.** Broken tests, broken build, failing CI — fix before anything else.
2. **Key tasks next.** Unfinished key-task items from intent take priority over polish.
3. **High-severity findings** from reviews before medium/low.
4. **Implementation before cleanup.** If the backlog contains unimplemented tickets, prefer `/implement` over `/refactor`/`/review-*` until the backlog is empty.
5. **Cleanup and reviews** once the feature work is done.

Available actions (non-exhaustive):

- `/scope` — draft new tickets when gaps emerge that serve intent
- `/implement` or `/implement-batch` or `/implement-project` — execute ticketed work
- `/refactor` or `/refactor-deep` — code quality cleanup
- `/review-arch`, `/review-test`, `/review-doc`, `/review-release`, `/review-perf`, `/review-a11y`, `/review-security` — targeted reviews
- `/review-deep` — comprehensive review pass
- `/bug-hunt` — proactive bug discovery
- `/bug-fix` — diagnosis-first bug fixing
- `/test-mutation` — mutation testing
- `/think-deliberate` — adversarial option selection when two or more choices are materially different and the trade-off is unclear
- `/think-scrutinize` — stress-test a plan before executing it, when the plan is risky or novel
- `/think-brainstorm` — divergent idea generation when no obvious action presents itself

When invoking a sub-skill that supports autonomous mode, use it. When a sub-skill requires interactive input, answer autonomously using engineering judgment anchored to the pinned commander's intent. Only pull the andon cord if the sub-skill itself pulls its andon cord for reasons this skill cannot resolve.

**Reviewer tie-breaker.** If two review skills produce contradictory findings on the same file within the run — e.g., `/refactor` removed a helper that `/review-arch` later recommends restoring, or `/review-test` wants a test split that `/review-doc` flags as harming readability — **do not oscillate**. Pull the andon cord. Contradictory review verdicts are a product judgment call the user should make, not a loop the skill should try to resolve. Include both findings in the handoff.

**Reviewer invocation cap.** A given review sub-skill (e.g., `/review-arch`) may be re-invoked only if files it previously flagged have been materially modified since. Rerunning a review against unchanged code thrashes. Record each review invocation and its target scope in the state doc; check before re-invoking.

Record the chosen action and rationale (one or two sentences) in the cycle log before proceeding.

#### 1d. Act

Execute the chosen action. After it completes:

- Verify: tests still pass, build still works, nothing obvious is broken.
- Sub-skills usually commit their own work. If the action made changes outside a sub-skill (e.g., a direct fix), commit them with a message that references the key task it serves.
- Update the cycle log in the state doc: cycle number, action, outcome, duration (roughly), any new findings, whether the action moved toward intent.
- Increment cycle counter.

Return to step 1a for the next cycle.

#### 1e. Trajectory audit (periodic)

**Every 10 cycles** (cycles 10, 20, 30, 40), perform a trajectory audit at the start of the cycle, before Observe. This is an internal self-check — not user-facing unless it triggers the andon cord.

The audit asks: are we converging toward intent, or drifting/thrashing?

**Audit inputs (read directly, not from cycle log narrative):**
- `git log --oneline <branch-start>..HEAD` — actual commits made
- `git diff --stat <branch-start>..HEAD` — actual changes
- Pinned intent (all five fields, verbatim)
- Current deferred-items list from state doc
- Mechanical end-state conditions and their last-known status

**Audit questions:**
- Do the commit subjects trace to key tasks in the pinned intent, or have they drifted into unrelated work?
- Are key tasks showing progress over the last 10 cycles (new commits, closed tickets, passing checks), or has work concentrated elsewhere?
- Is the deferred-items list growing faster than the completion list?
- Are the same files being repeatedly touched by different sub-skills (oscillation)?

**Audit verdict:**
- **Converging** — recent work traces to intent, key tasks advancing, mechanical conditions trending toward pass. Continue.
- **Diverging** — recent work predominantly on non-intent items, or scope has expanded beyond declared boundaries. Attempt one course-correction cycle (Decide reaches for the highest-priority key task). If the next audit (10 cycles later) also returns Diverging, pull the andon cord.
- **Thrashing** — oscillation detected (same files being rewritten, reviewers producing contradictory findings, no net progress). Pull the andon cord immediately.

Record the audit verdict in the state doc under a `## Trajectory Audits` section. Two consecutive Diverging verdicts, or any Thrashing verdict, pulls the cord.

### 2. Termination

#### 2a. Final verification pass

Before declaring done, perform one last verification. This is partly redundant with the Orient-phase termination check — that's intentional. Redundancy here catches race conditions between "check passed in Orient" and "report generated in 2b."

- Re-run all mechanical end-state conditions. Record exact command and exit status.
- Full test suite passes.
- Build/typecheck/lint all clean.
- Smoke-test any explicit features listed in key tasks, if feasible.
- Confirm no constraint violations in recent commits (grep for protected paths from the Constraints field).

If any check fails, treat as a blocker — return to the loop and fix it.

#### 2b. Completion report

Produce a completion report for the user. The report is ordered by review priority — the sections most likely to need user scrutiny come first.

**Evidence format.** For every claim of a completed key task or end-state condition, provide **both**:
- A brief narrative (one sentence) — what happened and why the user should believe it
- A concrete artifact — commit SHA, test command + output, file:line reference, or ticket ID

Narrative without an artifact is not evidence. An artifact without narrative is unreadable. Both together let the user skim at narrative level and drill into the artifact when a claim looks suspicious.

```
## Lead-Project Complete

### Commander's intent
[Verbatim, all five fields]

### Outcome
[One-paragraph summary of whether intent was fulfilled and how. State plainly if
 any mechanical end-state condition failed or any subjective condition needs user sign-off.]

### Top things to scrutinize
[Three to five items the user should look at first. Pick the items where the
 skill's judgment is most likely to be wrong or where the stakes are highest:
 - commits touching sensitive or high-risk code,
 - findings the skill downgraded or deferred,
 - decisions made via /think-deliberate,
 - places where subjective end-state conditions require sign-off.
 Each item: one sentence + artifact (SHA, file:line, or state-doc section).]

### End-state verification
**Mechanical conditions:**
- [✓] <condition 1> — <narrative> — `<command>` exit 0 at SHA <short>
- [✓] <condition 2> — <narrative> — `<command>` exit 0 at SHA <short>

**Subjective conditions (awaiting user sign-off):**
- [?] <condition 3> — <narrative of what was done toward it> — see SHA <short>, file:line

### Key tasks status
- [✓] <task 1> — <narrative> — SHA <short> / ticket #N
- [✓] <task 2> — <narrative> — SHA <short>
- [~] <task 3> — partial, see Deferred
- ...

### Deferred items
[Findings and opportunities the skill chose not to address.
 Grouped by severity and type. Each item: one-line description,
 rationale for deferral, pointer to where it's tracked.]

- [medium | /review-test | cycle 14] <description> — deferred because <reason> — tracked in state doc section X
- [low | /review-doc | cycle 22] <description> — deferred because <reason>

### Constraint/non-goal adherence
[Confirm no violations. If any close calls occurred, name them with commit SHAs
 so the user can verify.]

### Recommendations
[Suggested next steps: "ready to merge," "consider follow-up iteration for deferred items,"
 "one open design question remains (see handoff)," etc.]

### Changes summary
- Branch: <branch name> (SHA <short>)
- Base: <base branch> (SHA <short>)
- Commits on branch: N
- Net lines: +X/-Y
- Tickets created: N (list IDs)
- Tickets closed: N (list IDs)

### Run metadata
- Cycles: N of 50
- Actions taken: [grouped: "2x /implement, 3x /refactor, 1x /review-arch, 1x /review-test"]
- Trajectory audits: [verdicts at each audit point]
- Duration (wall-clock, approximate)
```

The user decides whether to merge to main, run another iteration, or pause.

## Commander's Intent — Field Reference

### Purpose

One or two sentences stating *why* this iteration exists. The underlying motivation, not the tactical outcome.

Good: "Ship v1.0 of the MCP server to external users."
Weak: "Work on the MCP server."

### Key tasks

Non-negotiable outcomes that must be true at the end. Written as state, not activity. Listable — between 2 and 10 items.

Good:
- "All tickets in milestone `v1.0` are closed."
- "README contains installation and usage sections."
- "Test suite covers every exported function."

Weak:
- "Improve tests." (not observable)
- "Fix bugs." (not specific)

### End state

Concrete, observable conditions defining completion. Pragmatically: what could the skill check to prove it is done? These become the termination conditions.

Good:
- "`go test ./...` exits 0."
- "`go build` produces a binary that responds to `--help`."
- "CHANGELOG has a v1.0 entry listing all user-visible changes."

Weak:
- "Works well." (not observable)
- "Feels polished." (not verifiable)

### Constraints

Hard limits. The skill must not violate these during the loop.

Examples:
- "Do not modify the public API of package `auth`."
- "Must remain compatible with Go 1.22."
- "No new runtime dependencies."

### Non-goals

Explicit out-of-scope. Things the skill should leave alone even if it sees opportunity.

Examples:
- "No performance optimization this iteration."
- "Do not touch the frontend."
- "Dependency upgrades are out of scope."

## Severity Thresholds for "Done"

Reviewers produce findings indefinitely. The skill applies thresholds:

| Severity       | Handling                                                                                                                        |
|----------------|---------------------------------------------------------------------------------------------------------------------------------|
| Critical/High  | Must address before termination. Blocks the termination check.                                                                 |
| Medium         | Address if the fix is bounded (small, obvious, localized). Otherwise defer with a note in the state doc. Does not block termination. |
| Low/Info       | Defer by default with a note. Does not block termination.                                                                      |

The skill records every deferral with rationale in the state doc so the completion report can present them transparently.

## Andon Cord Protocol

**The andon cord is the only planned escalation path.** The user is not checking in between cycles — they will only be interrupted when the cord is pulled. Pull it sparingly but decisively.

### Before pulling the cord

1. Attempt autonomous resolution first.
2. For judgment calls, try `/think-deliberate` or `/think-reframe` before escalating.
3. Re-read the commander's intent — is the apparent blocker actually a signal that intent needs clarification?
4. Only pull if autonomous resolution has failed or is clearly futile.

### Andon cord triggers

Pull the cord when:

- **Irreversible action required.** Publishing a release, pushing/merging to main/master, force-push, installing global dependencies, deleting data or untracked work.
- **Blocking decision requires product judgment.** Feature direction, UX choice, or ambiguous requirement that `/think-deliberate` cannot resolve from information available in the repo.
- **Stuck.** Same failure mode has occurred 3 or more times across attempts despite different strategies.
- **Drift is severe.** Recent work has diverged materially from intent and the skill cannot determine whether to continue on the new path or revert.
- **Trajectory audit returns Thrashing**, or two consecutive audits return Diverging (see 1e).
- **Reviewers produce contradictory findings on the same file.** Do not oscillate — surface both findings and let the user decide.
- **Fundamental assumption broken.** Something the skill believed to be true about the codebase turned out to be false in a way that invalidates the triage plan.
- **Constraint conflict.** A key task appears to require violating a stated constraint (or vice versa) and the conflict cannot be resolved by the skill.
- **Resume-time HEAD divergence.** On resume, recorded branch SHA does not match current HEAD.
- **Hard cap hit.** 50 cycles elapsed without reaching termination. Something is likely wrong — hand off rather than continue.
- **Sub-skill andon cord cascades up.** A sub-skill pulled its own andon cord for a reason this skill cannot resolve.

### Handoff format

When pulling the cord, produce a structured handoff document. Append it to the state doc under a `## Andon Cord` section and present it to the user.

```
## Andon Cord — Cycle N

### Project orientation (30-second reorient)
[One paragraph. For a user returning cold: what is this project, where
 does it stand right now, what has changed since they last looked.
 Key-task status: which are done, in progress, deferred. Major recent
 milestones. Skip project background the user already knows — focus on
 state that has changed during this run.]

### What I was trying to do
[The key task or intent item driving this cycle.]

### What went wrong
[Specific failure mode. Concrete, not vague.]

### What I tried
[Actions attempted, /think-* skills invoked and their verdicts, alternative approaches considered.]

### What I need from you
[Specific decision, permission, or information required.
 Phrase as a yes/no or multiple-choice question when possible.]

### Current state
- Branch: <name> (at SHA <short>)
- Commits on branch: N
- Tests: <pass/fail with detail>
- Build: <pass/fail>
- Mechanical end-state conditions: <K of M passing>
- Pending key tasks: <summary>

### To resume
[Instructions for re-invoking /lead-project after the blocker is resolved.
 Reference the state doc for context preservation.]
```

After pulling the cord: stop. Do not attempt additional cycles. Wait for user input.

## State Management

### `LEAD_PROJECT_STATE.md`

Maintained at the repo root. Gitignored. Survives across invocations so the skill can resume.

**Structure:**

```markdown
# Lead-Project State

Started: <timestamp>
Branch: <branch-name>
Branch SHA at startup: <short SHA>
Base branch: <main-branch>
Base SHA at startup: <short SHA>
Last cycle HEAD: <short SHA>
Current phase: <startup | ooda-cycle | termination | andon-cord>
Cycle: N
Status: <active | paused-on-andon | complete>

## Commander's Intent

### Purpose
<verbatim>

### Key tasks
- <task 1>
- <task 2>

### End state

**Mechanical** (shell-runnable, gate termination):
- <condition 1> — `<command>`
- <condition 2> — `<command>`

**Subjective** (user sign-off at completion):
- <condition 3>

### Constraints
- <constraint 1>

### Non-goals
- <non-goal 1>

## Orientation

### Current understanding
<agent's working mental model — what's true about the project,
 updated when observations contradict prior assumptions>

### Drift status
<OK | drifting — why>

## Triage plan

Initial plan set at startup, updated as orientation evolves.

1. <planned action>
2. <planned action>
3. <planned action>

## Cycle log

### Cycle N — <timestamp> — HEAD <short SHA>
- Observe: <one-line summary of state>
- Orient: <one-line summary of interpretation — drift status, termination status, mechanical-condition pass/fail counts>
- Decide: <action chosen + one-line rationale>
- Act: <skill invoked, outcome, changes + commit SHAs>

### Cycle N+1 — <timestamp> — HEAD <short SHA>
...

## Trajectory audits

Internal convergence/divergence/thrashing verdicts at cycles 10, 20, 30, 40.

- Cycle 10: <converging | diverging | thrashing> — <brief rationale>
- Cycle 20: ...

## Review invocation log

Track review sub-skill invocations to enforce the "only re-invoke if flagged files changed" rule.

- /review-arch @ cycle 7 — scope: repo-wide — flagged files: [list]
- /review-test @ cycle 12 — scope: pkg/foo — flagged files: [list]

## Deferred items

Findings and opportunities the skill chose not to address, with rationale.

- [medium | /review-test] <description> — deferred because <reason>
- [low | /review-doc] <description> — deferred because <reason>

## Open questions

Questions the skill is tracking but has resolved autonomously for now
(to surface in completion report).

- <question>
```

**Update at every OODA phase transition.** The state doc is the persistent Orientation — losing it means losing the agent's memory.

### `.gitignore`

Ensure `LEAD_PROJECT_STATE.md` is ignored. Commit the `.gitignore` change on the working branch at startup if needed.

## Hard Caps

- **50 cycles** — if the loop reaches cycle 50 without terminating, pull the andon cord. Something is likely wrong; hand off rather than continue.
- **3 consecutive failed actions** — if the skill attempts the same goal 3 times with different strategies and all fail, pull the andon cord.

## Agent Coordination

**Sequential execution.** One cycle at a time, one skill invocation per cycle. No parallel cycles.

**Context discipline.** The skill is a thin coordinator. It delegates all implementation to sub-skills. It maintains only summary-level state in its context; `LEAD_PROJECT_STATE.md` holds durable memory.

**Sub-skill invocation.** Invoke via Skill tool with autonomous overrides where supported. When a sub-skill requires interactive input, answer using engineering judgment referenced to the pinned intent.

## Abort Conditions

**Do NOT abort for:**

- Individual cycle failures (try a different approach in the next cycle)
- Sub-skill findings that look overzealous (apply severity threshold, defer)
- Drift that can be course-corrected autonomously

**Pull the andon cord for:**

- Triggers listed under "Andon cord triggers" above

**Abort the entire workflow for:**

- User interrupts
- Critical system error (repository corrupted, git state unrecoverable)
- User declines to confirm the commander's intent at startup

## Integration with Other Skills

**Relationship to `/implement-project`:**

`/implement-project` is a once-through pipeline over a known set of tickets. `/lead-project` is an open-ended loop that decides what to work on next. `/lead-project` may *invoke* `/implement-project` when it has a coherent batch of tickets to execute.

**Relationship to `/scope` and `/scope-project`:**

`/scope` and `/scope-project` create tickets. `/lead-project` may invoke `/scope` when it identifies a gap worth ticketing. `/scope-project` is typically run by the user before `/lead-project` to establish the initial backlog.

**Relationship to `/review-deep`:**

`/review-deep` is a comprehensive review pass. `/lead-project` may invoke it near the end of a run to validate end-state conditions, or invoke individual `/review-*` skills earlier when specific concerns arise.

**Relationship to `/think-*` skills:**

- `/think-reframe` — in Orient, when the problem framing seems wrong
- `/think-diagnose` — in Orient, when a failure cause is unclear
- `/think-deliberate` — in Decide, when options are materially different
- `/think-scrutinize` — in Decide, when a plan is risky or novel
- `/think-brainstorm` — in Decide, when no obvious next action presents itself

`/think-reflect` is intentionally NOT invoked in the loop — it is calibrated for human consumption after the fact. The user may invoke it themselves on the completion report.

**Hierarchy:**

```
/lead-project
├── (startup)
│   └── /review-health (optional)
├── (per cycle, any of:)
│   ├── /scope
│   ├── /implement | /implement-batch | /implement-project
│   ├── /refactor | /refactor-deep
│   ├── /review-arch | /review-test | /review-doc | /review-release
│   ├── /review-perf | /review-a11y | /review-security
│   ├── /review-deep
│   ├── /bug-hunt | /bug-fix
│   ├── /test-mutation
│   └── /think-reframe | /think-diagnose | /think-deliberate
│       | /think-scrutinize | /think-brainstorm
└── (termination)
    └── Completion report
```
