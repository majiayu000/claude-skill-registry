---
name: quick
description: "Tracked lightweight execution with composable rigor flags: --trivial, --discuss, --research, --full. Covers zero-ceremony inline fixes (typo, spelling fix, small mistake in a single file, ≤3 edits) through contained multi-file changes."
user-invocable: true
argument-hint: "[--trivial] [--discuss] [--research] [--full] <task>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Skill
  - Task
routing:
  force_route: true
  triggers:
    - quick task
    - small change
    - ad hoc task
    - add a flag
    - small refactor
    - targeted fix
    - quick fix
    - typo fix
    - fix typo
    - fix the typo
    - one-line change
    - trivial fix
    - rename variable
    - rename this variable
    - update value
    - fix import
    - small mistake
    - small mistake in
    - mistake in spelling
    - spelling mistake
    - spelling fix
    - fix the spelling
    - typo in
    - small fix in
    - small fix
    - tiny fix
  not_for: "'quick' as speed preference, general bug diagnosis requiring investigation"
  complexity: Simple
  category: process
---

# /quick - Tracked Lightweight Execution

Quick covers the full lightweight tier from zero-ceremony inline fixes (≤3 edits, `--trivial` mode) through contained multi-file changes. Full-ceremony Simple+ tasks (task_plan.md, agent routing, quality gates) belong in `/do`. The key design principle is **composable rigor**: the base mode is minimal (plan + execute), and users add process incrementally via flags.

**Flags** (all OFF by default):

| Flag | Effect |
|------|--------|
| `--trivial` | Zero-ceremony inline mode for ≤3 file edits: no plan display, no branch, direct commit. Scope-gates strictly — escalates automatically if the task needs more than 3 edits. Use for typo fixes, one-line constant changes, renaming a variable, fixing an import. |
| `--discuss` | Add a pre-planning discussion phase to resolve ambiguities (breadth-first — surfaces all gray areas at once) |
| `--interview` | Add a depth-first decision-tree interview before the edit phase. One question at a time with a recommendation per question. Sibling to `--discuss` — pick `--interview` when decisions are interdependent and answer A constrains valid options for B. |
| `--research` | Add a research phase before planning to build context on unfamiliar code |
| `--full` | Add plan verification + full quality gates (tests, lint, diff review) |
| `--no-branch` | Skip feature branch creation, work on current branch |
| `--no-commit` | Skip the commit step (for batching multiple quick tasks) |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| usage examples, task ID format, error handling | `examples.md` | Loads detailed guidance from `examples.md`. |
| emitting banners, commit format, or STATE.md entries | `templates.md` | Loads detailed guidance from `templates.md`. |

## Instructions

### Phase --trivial: INLINE EXECUTION (only with --trivial flag)

When `--trivial` is passed (or the router recognises a clearly one-line mechanical change), execute inline without plan display, without a feature branch, and without spawning subagents — because the overhead of those steps dwarfs the actual work.

**Step 1: Read CLAUDE.md**

Read repository CLAUDE.md before any edit, because repo-specific constraints affect how even trivial changes should be made.

**Step 2: Scope check**

| Question | If Yes |
|----------|--------|
| Does this need reading docs, investigating behavior, or understanding unfamiliar code? | Drop `--trivial`, redirect to `/quick --research` |
| Does this touch more than 3 files? | Drop `--trivial`, redirect to standard `/quick` |
| Does this add imports from new packages or modify dependency files? | Drop `--trivial`, redirect to standard `/quick` |
| Is the request ambiguous or underspecified? | Ask one clarifying question; if still ambiguous after one round, drop `--trivial` and use `/quick --discuss` |

If redirecting, say: `This task exceeds --trivial scope ([reason]). Continuing as /quick.` Then proceed to Phase 0 with the original request.

**Step 3: Locate target files and execute**

Read the target file(s). Make edits using the Edit tool. Track edit count. After each edit, check: have we hit 3 edits? If more are needed, stop -- do not rationalize "just one more edit." Say: "Scope exceeded during --trivial execution (3+ edits needed). Preserving work done. Continuing as /quick." Hand off to the standard quick phases with context about what was already done.

**Step 4: Check branch**

If on main/master, create a short-lived branch: `git checkout -b quick/<brief-description>`.

**Step 5: Stage and commit**

Stage specific files with `git add <specific-files>`. Commit using the format from `references/templates.md` (conventional commit, type usually `fix:`, `chore:`, or `refactor:`).

**Step 6: Display summary**

Use the `--trivial` summary banner format from `references/templates.md`.

**GATE**: Edit count is 1-3, commit succeeded. STOP — do not proceed to Phase 0.

---

### Phase 0: SETUP

**Step 1: Read CLAUDE.md**

Read and follow the repository's CLAUDE.md before doing anything else, because repo-specific conventions override defaults and skipping this causes style/tooling mismatches.

**Step 2: Parse flags**

Extract `--discuss`, `--interview`, `--research`, `--full`, `--no-branch`, and `--no-commit` from the invocation. Everything remaining after flag extraction is the task description.

**Step 3: Scope check**

If the task involves multiple components, architectural changes, or needs parallel execution, redirect to `/do` instead because quick tasks are single-threaded by design -- parallelism means the task has outgrown this tier.

### Phase 1: DISCUSS (only with --discuss flag)

This phase activates when the user passes `--discuss` or the request contains signals of uncertainty ("not sure", "maybe", "could be", "what do you think").

**Step 1: Identify ambiguities**

Read the request and list specific questions:
- What exactly should change? (if underspecified)
- Which approach among alternatives? (if multiple valid paths)
- What are the acceptance criteria? (if success is unclear)

**Step 2: Present questions**

Use the DISCUSS banner format from `references/templates.md`. Wait for user response. Do not proceed until ambiguities are resolved.

**GATE**: All ambiguities resolved. Proceed to Phase 2 or Phase 3.

### Phase 1.5: INTERVIEW (only with --interview flag)

This phase activates when the user passes `--interview`. It is the depth-first sibling to `--discuss` — pick this mode when decisions are interdependent and answering A would change the valid options for B, so batch-asking forces premature commitments.

**Step 1: Load the depth-first reference**

Load `planning/references/depth-first-interview.md` and follow its phases (PRIME → ENUMERATE BRANCHES → TRAVERSE → COMPILE OUTPUT). The reference enforces a hard cap of 5 total questions and 3-level recursion per branch — these limits are infrastructure, not advisory.

**Step 2: Treat `--interview` as an explicit trigger**

Per the reference's Phase 0 trigger classification, `/quick --interview` is an explicit invocation. Skip the Phase 0 opt-out question — the user already opted in by passing the flag. Go directly to ENUMERATE BRANCHES.

**Step 3: Compile output to inline context**

The reference's Phase 3 emits a structured block (Resolved Decisions / Carried Forward / Scope Boundary / Mode Used). Keep this block inline as the discussion artifact and use it to inform Phase 3 PLAN. Do not write a separate `task_plan.md` for `/quick` tier.

**GATE**: Interview output emitted. Resolved decisions inform the inline plan. Proceed to Phase 2 or Phase 3.

### Phase 2: RESEARCH (only with --research flag)

This phase activates when the user passes `--research` or the task touches code that needs investigation. Use `--research` when touching unfamiliar code because confidence about code behavior is not the same as correctness — `--trivial` exists for when you truly know.

**Step 1: Identify scope**

Determine which files and patterns need reading to understand the change.

**Step 2: Read and analyze**

Read relevant source files, tests, and configuration. Build a mental model of:
- Current behavior
- Where the change fits
- What might break

**Step 3: Summarize findings**

Present a brief (3-5 line) summary of what you learned and how it affects the plan.

**GATE**: Sufficient understanding to plan the change. Proceed to Phase 3.

### Phase 3: PLAN

**Step 1: Generate task ID**

Assign the task ID now, not later, because untracked tasks become invisible and "later" never comes.

Format: `YYMMDD-xxx` where xxx is Base36 sequential (0-9, a-z).

```bash
# Check STATE.md for today's tasks to determine next sequence
date_prefix=$(date +%y%m%d)
```

If STATE.md exists in the repo root, find the highest sequence number for today's date prefix and increment. If no tasks today, start at `001`. Use Base36 for the sequence: 001, 002, ... 009, 00a, 00b, ... 00z, 010, ...

If STATE.md is corrupted, scan git log for `Quick task YYMMDD-` patterns to find the true next ID. If a branch name collision occurs, increment the sequence number and try again.

**Step 2: Create inline plan**

Always display the inline plan, even for obvious tasks, because the plan catches misunderstandings before they become wrong edits and confirms alignment in 10 seconds that saves minutes. Use the inline plan banner instead of writing a `task_plan.md` file; that keeps the workflow in the Simple+ tier and preserves the minimum viable ceremony.

Use the inline plan banner format from `references/templates.md`.

If estimated edits exceed 15, prompt the user to consider `/do` -- edit count is a scope signal regardless of difficulty.

If the task involves security, payments, or data migration, recommend `--full` because a one-line auth change can be catastrophic and risk is about impact, not size.

**Step 3: Create feature branch** (unless --no-branch)

Create a feature branch because small changes on main break the same as big ones:

```bash
git checkout -b quick/<task-id>-<brief-kebab-description>
```

If already on a non-main feature branch and `--no-branch` is set, stay on the current branch.

**GATE**: Task ID assigned, plan displayed, branch created. Proceed to Phase 4.

### Phase 4: EXECUTE

**Step 1: Make edits**

Execute the changes described in the plan. Track edit count throughout.

**Step 2: Scope monitoring**

- At 10 edits: display a warning -- "10 edits reached. Quick tasks typically stay under 15."
- At 15 edits: suggest upgrade -- "15 edits reached. This may benefit from /do with full planning. Continue? [Y/n]"
- No hard cap -- the user decides. Quick's scope is advisory, not enforced like Fast's 3-edit gate.

**Step 3: Verify changes** (base mode)

Run a language-appropriate syntax check on edited files (e.g., `python3 -m py_compile`, `go build ./...`, `tsc --noEmit`). If `--full` flag is set, run the full quality gate instead (see Phase 5).

**GATE**: All planned edits complete. Sanity check passes.

### Phase 5: VERIFY (only with --full flag)

**Step 1: Run tests** for affected packages/modules only -- do not run the full suite unless explicitly requested.

**Step 2: Lint check** using the repo's configured linter on changed files.

**Step 3: Review changes** with `git diff`. Check for unintended changes, missing error handling, and broken imports.

**GATE**: Tests pass, lint clean, diff reviewed. Proceed to Phase 6.

### Phase 6: COMMIT (skip with --no-commit)

Stage specific files with `git add <specific-files>` -- not `git add .`, to avoid accidental inclusions. Commit using the format from `references/templates.md`. Include the task ID in the commit body for traceability.

**GATE**: Commit succeeded. Verify with `git log -1 --oneline`.

### Phase 7: LOG

**Step 1: Update STATE.md**

Log the task to STATE.md because this is how tasks stay visible and cross-referenceable. Use the STATE.md schema from `references/templates.md` to create the file if it does not exist, and append one row per task. If escalated from `--trivial`, use tier `trivial->quick`.

**Step 2: Display summary**

Use the completion banner format from `references/templates.md`.

## Reference Material

> See `references/examples.md` for worked examples per flag mode, task ID format, and error handling.
