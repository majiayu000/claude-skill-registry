---
name: subagent-driven
description: Execute a multi-task plan by dispatching one fresh subagent per task, auditing each result against an adversarial review gate before the next starts, and closing with a broad whole-branch review. Use when a plan, checklist, or multi-step change has tasks that can be delegated, or when the user says "subagent-driven", "delegated execution", "execute the plan with subagents", or hands you an ordered plan to run.
metadata:
  short-description: Per-task implementer→reviewer loop with an audit gate between tasks
---

# Subagent-Driven — per-task implementer→audit loop

Execute a plan as a chain of delegated subagents. Each task gets a fresh
implementer with a self-contained brief; a fresh reviewer audits the result
before the next task starts; a broad whole-branch review closes the run. The
audit is the completion gate — a task is done only when its verifier passes
**and** the audit clears. A green verifier proves the worker's own check ran;
it is not an audit.

**Why fresh subagents.** You delegate to workers with isolated context. You
construct exactly what each needs — they never inherit your session, the plan
file, or prior workers' history. That keeps them focused and keeps your own
context free for coordination.

**Continuous execution.** Do not check in between tasks. Run every task in the
plan without stopping. Stop only for: a BLOCKED status you cannot resolve, an
ambiguity that genuinely blocks progress, or all tasks complete. "Should I
continue?" prompts waste the user's time — they asked you to execute the plan.

**Narration.** Between tool calls, at most one short line. The ledger and tool
results carry the record.

## When to Apply / NOT

Apply when work decomposes into ordered tasks with clean boundaries and you
want each delegated, audited, and committed before the next starts: a written
plan, a checklist, "execute this with subagents."

NOT:
- Independent fan-out with a single compose-and-review at the end → `parallel-launch`. That skill runs concurrent agents on separate concerns and reviews once; this one runs an *ordered* chain with a gate *between* tasks.
- Review and fix an *existing* diff until clean → `review-fix-grill-loop`. That grills a change-set you already have; this one *produces* the change-set task by task.
- You implement the slices yourself, no delegation → `incremental-implementation`.
- A single atomic change → edit it directly. Don't dispatch a worker for a one-liner.

## Core Loop

Before Task 1, scan the plan once for self-conflicts: tasks that contradict
each other or the Global Constraints, or anything the plan mandates that the
review rubric treats as a defect (a test asserting nothing, verbatim
duplication of a logic block). Batch every finding into one question to the
user — each beside the plan text that mandates it, asking which governs —
before execution, not one interrupt per discovery. Clean scan → proceed silently.

For each task, in order:

1. **Decompose and classify the op.** Split into tasks with explicit
   boundaries: which files each touches, what it depends on, what "done" means.
   One concern per task. Two tasks editing the same file are not independent —
   sequence or merge them. Classify each task's op before dispatch:
   **compress** (preserve behavior, cut entropy), **extend** (add capability,
   every line load-bearing), **correct** (restore a named invariant), **purge**
   (remove a surface, transfer-proof). The op is the brief's frame and the
   reviewer's lens.
2. **Brief.** Run `scripts/task-brief PLAN_FILE N` — it extracts the task's
   full text to a uniquely named file and prints the path. The brief is the
   single source of requirements; the dispatch only frames it.
3. **Dispatch one fresh implementer.** Spawn a new `general-purpose` subagent
   with `implementer-prompt.md` filled in. Fresh per task: no carried context,
   no resumed worker. Record the BASE commit (current HEAD) before dispatching —
   you need it for the review package.
4. **Worker implements, tests, commits, self-reviews.** The worker makes the
   change, runs the verification command from its brief, commits one concern
   with an `Op:` trailer, self-reviews against the rejection grounds, writes its
   full report to the report file, and returns a short status (see statuses below).
5. **Build the review package.** Run `scripts/review-package BASE HEAD` — it
   writes one file (commit list, stat summary, full diff with context) that
   never enters your context, and reports that file's path. Use the BASE you
   recorded — never `HEAD~1`, which silently drops all but the last commit of a
   multi-commit task.
6. **Audit before proceeding.** Dispatch a fresh `general-purpose` reviewer with
   `task-reviewer-prompt.md`, handing it the brief path, the report path, the
   diff-package path, and the verbatim Global Constraints. The audit checks
   **scope drift** (only the task's files changed), **correctness** (does what
   the brief asked), **contract alignment** (matches existing patterns and
   interfaces), **stale references** (no dangling names, dead imports, orphaned
   callers), **and the four rejection grounds** — Excess, Graft, Sprawl, Sever.
   Worker output is trusted after this audit, not before.
7. **Gate.** Audit clean and verifier green → mark the task complete in the
   ledger, move to the next. Audit finds a Critical/Important issue (including
   any rejection ground) → dispatch a fix worker with the complete findings
   list, then re-review. Do not start the next task on an unaudited or suspect
   result. If the audit cannot be cleared, abort the chain rather than build on it.

## Dispatch Brief

Each brief is self-contained — the worker reads only what the brief points to.
Pass file *paths*, not contents; keep static material under ~50 lines inline,
point to everything larger.

- **Goal** — one sentence: what this task changes and why.
- **Op** — compress | extend | correct | purge. Stay inside it.
- **Files** — the paths to edit, as paths. Name files the worker must NOT touch.
- **Constraints** — patterns to follow, interfaces to preserve, what is out of scope.
- **Verification** — the exact command that proves the task works (test,
  typecheck, build, lint). The worker runs it before reporting done.
- **Commit** — one concern, one commit, conventional prefix + `Op:` trailer.
  `correct` adds `Restores:`; `purge` adds `Removes:`.

A dispatch describes one task, not the session's history. Never paste
accumulated prior-task summaries ("state after Tasks 1-3") into later
dispatches — a fresh subagent needs its task, the interfaces it touches, and
the global constraints. Nothing else.

## Reviewer Is Self-Contained

The loop's gate is the local `task-reviewer-prompt.md` dispatched to a fresh
`general-purpose` subagent. No hard dependency on any external named agent — the
skill works standalone. If the compound-engineering plugin happens to be
installed, `ce-adversarial-reviewer` is an optional drop-in for the audit role;
the loop does not require it and never assumes it.

## Implementer Statuses

Workers report one of four. Handle each:

- **DONE** — build the review package and dispatch the reviewer.
- **DONE_WITH_CONCERNS** — completed but flagged doubts. Read them first. If
  they touch correctness or scope, resolve before review; if they are
  observations ("this file is getting large"), note and proceed.
- **NEEDS_CONTEXT** — missing information. Supply it and re-dispatch.
- **BLOCKED** — cannot complete. Diagnose: context problem → add context,
  re-dispatch same model; needs more reasoning → re-dispatch a more capable
  model; too large → split it; plan is wrong → escalate to the user.

Never ignore an escalation, and never force the same model to retry unchanged.
If the worker said it is stuck, something must change before the retry.

The reviewer may report **⚠️ Cannot verify from diff** items — requirements
living in unchanged code or spanning tasks. They do not block the rest of the
review, but you resolve each one yourself before marking the task complete: you
hold the cross-task context the reviewer lacks. A confirmed gap is a failed spec
review — back to the implementer, then re-review.

## Model Selection

Use the least capable model that fits the role — but turn count beats token
price, and the cheapest models often take 2-3× the turns on multi-step work.

- Touches 1-2 files with a complete spec → cheap model. When the brief contains
  the complete code to write, it is transcription plus testing — cheapest tier.
- Multiple files with integration concerns → standard model. Mid-tier is the
  floor for reviewers and for implementers working from prose.
- Design judgment or broad codebase understanding → most capable model. The
  final whole-branch review is one of these — run it on the most capable
  available model, not the session default.

**Always specify the model explicitly when dispatching.** An omitted model
inherits your session's — usually the most expensive — and silently defeats this.

## Parallel Dispatch

Tasks with no shared files and no ordering dependency can run as concurrent
workers. Document the independence argument before you do — two tasks touching
one file are not independent. Respect the platform's active-subagent limit, queue
overflow, and treat spawn errors as backpressure (slow down, don't drop the task).

The per-task gate does not relax under parallelism — this is what separates the
skill from `parallel-launch`'s single end-of-run review. Every result is audited
on its own before it reaches the shared branch; concurrency only overlaps the
*implement* step, never the gate.

Git state is not parallel-safe in a single checkout, and this skill's audit runs
against committed ranges (`review-package BASE HEAD`), so the commit must exist
before the audit. Keep that ordering consistent under parallelism: give each
worker its own worktree (`git clone --shared` / the worktree skill) where it
commits in isolation, audit each worktree's `BASE..HEAD` independently, and
integrate into the main checkout only after that worker's audit clears —
serialize the integration so one result lands at a time. Never let two workers
commit into one shared index or HEAD. No parallel primitive → run the same tasks
sequentially.

## Tree-Clean Recovery

A worker that dies mid-task leaves a dirty tree. Inspect first (`git status`,
`git diff`) and revert **only** that worker's changes: discard its edits, remove
the stray files it created, leave any pre-existing uncommitted work untouched.
Never blanket-reset or `git clean` the whole tree — that destroys work outside
the task. Once the tree is back to the last good commit for the task's files,
re-dispatch fresh. Never resume a dead worker onto a dirty tree, and never build
the next task on uncommitted partial work.

## Reviewer-Prompt Discipline

When you fill a reviewer template, the gate stays honest only if you don't
pre-cook it:

- **Don't pre-judge findings.** Never tell a reviewer to ignore or not flag an
  issue, and never pre-rate severity ("treat it as Minor at most"). If your
  prompt contains "do not flag," "don't treat X as a defect," "at most Minor,"
  or "the plan chose" — stop, you are pre-judging to spare yourself a review
  loop. Let the reviewer raise it; adjudicate in the loop.
- **Copy binding constraints verbatim.** The Global Constraints block is the
  reviewer's attention lens — exact values, exact formats, stated relationships
  ("same layout as X", "matches Y"). The template already carries the process
  rules (YAGNI, test hygiene, rejection grounds); this block is what THIS spec demands.
- **Hand the reviewer its diff as a file** (`scripts/review-package BASE HEAD`).
  The diff never enters your context; the reviewer sees commits, stat, and full
  diff in one Read.
- **One task per dispatch.** No pasted session history.
- **Don't re-run the implementer's tests for the reviewer** — the report carries
  the test evidence; the reviewer runs a focused test only on a named doubt.
- **Plan-mandated findings are the user's call.** A finding that conflicts with
  what the plan's text requires: present the finding and the plan text, ask
  which governs. Do not dismiss it because the plan mandates it, and do not
  dispatch a fix that contradicts the plan without asking.
- **Fix dispatches carry the implementer contract** — the fixer re-runs the
  tests covering its change and reports the command and output. Name the
  covering test files; a one-line fix does not need the whole suite. Confirm the
  fix report has the covering tests, the command, and the output before re-review.
- **One fixer for the final review's findings** — dispatch ONE fix worker with
  the complete list, not one fixer per finding. Per-finding fixers each rebuild
  context and re-run suites.

## Durable Progress

Conversation memory does not survive compaction. Controllers that lost their
place have re-dispatched entire completed task sequences — the single most
expensive failure. Track progress in a ledger file, not only in todos.

- At skill start, check for a ledger:
  `cat "$(git rev-parse --show-toplevel)/.outline/sdd/progress.md"`. Tasks marked
  complete there are DONE — do not re-dispatch; resume at the first incomplete task.
- When a review comes back clean, append one line:
  `Task N: complete (commits <base7>..<head7>, op:<op>, review clean)`.
- The ledger is your recovery map: the commits it names exist in git even when
  your context no longer remembers creating them. After compaction, trust the
  ledger and `git log` over recollection.
- `git clean -fdx` destroys the ledger (git-ignored scratch); if that happens,
  recover from `git log`.

The workspace (`scripts/sd-workspace` → `.outline/sdd`) holds briefs, reports,
review packages, and the ledger. It self-ignores, so it never shows in
`git status` and never gets committed.

## Final Whole-Branch Review and Ship

After all tasks land:

1. Build the branch package: `scripts/review-package MERGE_BASE HEAD` where
   `MERGE_BASE = git merge-base main HEAD`. Hand the printed path to a final
   reviewer on the most capable model. Point it at the Minor findings the ledger
   accumulated so it can triage what must be fixed before merge.
2. Final-review findings → ONE fix worker with the complete list, then re-review.
3. **Ship via ODIN's atomic path, not a single squash.** Sort the work into
   atomic commits in detached HEAD, each carrying its `Op:` trailer (`Restores:`
   for `correct`, `Removes:` for `purge`). Publish with git-branchless `submit`,
   or run `atomic-commit-and-push`. Do not invent a branch-finishing or
   code-review-request flow outside this path.

## Validation Gates

| Gate | Pass criteria | Blocking |
|---|---|---|
| Pre-flight plan scan | Self-conflicts batched to the user before Task 1; clean scan proceeds silently | Yes |
| Op classified | Each task's op (compress/extend/correct/purge) set before dispatch | Yes |
| Brief completeness | Every brief has goal, op, files (+ do-not-touch), constraints, verification command, commit instruction | Yes |
| Fresh worker per task | New subagent, explicit model, no inherited context | Yes |
| Diff as file | `review-package BASE HEAD` (recorded BASE, never `HEAD~1`) before any reviewer dispatch | Yes |
| Audit between tasks | Fresh reviewer clears scope/correctness/contract/stale-refs + rejection grounds before the next task starts | Yes |
| Atomic commits | One concern per task, one commit, `Op:` trailer (+ `Restores:`/`Removes:`) | Yes |
| Tree-clean recovery | Worker death → revert only that worker's changes, re-dispatch fresh; never resume onto a dirty tree | Yes |
| Ledger maintained | Completed tasks appended to `.outline/sdd/progress.md`; resume reads it after compaction | Yes |
| Final review + ship | Whole-branch review on the most capable model, then atomic commits + `submit`/`atomic-commit-and-push` | Yes |

## Anti-Patterns

- **Trusting a green verifier as the audit.** It proves the worker's check ran, not that the change is correct or in scope.
- **Building the next task on an unaudited or suspect result.** The gate is mandatory, not advisory.
- **`HEAD~1` as the review base.** It silently truncates multi-commit tasks. Use the recorded BASE.
- **Pre-judging the reviewer** — "do not flag," "at most Minor," pre-rated severity. The gate is worthless if you cook it.
- **Two workers editing one file concurrently.** Concurrent edits corrupt each other's diffs. Sequence shared-file tasks or give each a worktree.
- **Pasting session history into a dispatch.** A fresh worker needs its task, its interfaces, and the constraints — nothing else.
- **Blanket-reset on worker death.** Revert only that worker's changes; `git clean -fdx` destroys user work and the ledger.
- **Re-dispatching a task the ledger marks complete.** Check the ledger and `git log` after any compaction or resume.
- **Squash-shipping.** The final ship is atomic commits with `Op:` trailers via the ODIN path, not one opaque merge commit.
