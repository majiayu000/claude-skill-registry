---
name: work
description: Execute a plan or concrete work prompt end-to-end. Use when implementing from docs/plans, a spec path, or a clear build request; use /debug for open-ended bugs.
argument-hint: "[Plan doc path or description of work. Blank to auto use latest plan doc]"
metadata:
  short-description: End-to-end implementation from plan or prompt
---

# Work Execution

Execute a plan or prompt systematically. Ship complete features by understanding requirements quickly, following existing patterns, and maintaining quality.

`Op: extend` — this skill adds structured plan handling, execution-engine selection, and a shipping tail to plain implementation.

## Input document

`<input_document>` = `$ARGUMENTS`

## Phase 0: Input triage

Determine how to proceed based on `<input_document>`.

**Plan document** (input is a path to an existing plan or spec):

- Read the plan's metadata first — YAML frontmatter for markdown, visible header for HTML.
- If it carries `artifact_contract: odin-unified-plan/v1`, classify `artifact_readiness` before reading the body.
  - `requirements-only` → stop. Tell the user this plan needs `/plan` enrichment before implementation. Offer `/plan <plan-path>`.
  - `implementation-ready` plus `execution: code` → continue to Phase 1 using the unified-plan reader strategy.
  - Any other readiness value or non-code/unclassified execution mode → do not auto-execute as code. Route `execution: knowledge-work` to the carve-out; otherwise ask the user to return to `/plan` for an implementation-ready code plan.
  - Progress-like values (`active`, `in_progress`, `completed`, `done`) are invalid readiness values. Stop and ask for plan repair.
- If it carries `execution: knowledge-work`, load `references/non-code-execution.md` and follow that carve-out.
- Otherwise (legacy plan, field absent, or `execution: code`) → continue to Phase 1.

**Blank invocation:** glob `docs/plans/*.md` and `docs/plans/*.html`. Inspect metadata for the newest candidates and auto-select only when the newest matching artifact is `implementation-ready` plus `execution: code` or a legacy code plan. Stop instead of silently executing a requirements-only, knowledge-work, approach-plan, or unclassified artifact. Ask for an explicit path or `/plan` enrichment.

**Superseded sibling:** if a requirements-only candidate has a same-basename file in the other format (`<basename>.md` / `<basename>.html`) that is `implementation-ready`, the requirements-only copy is stale — select the implementation-ready sibling instead of stopping.

**Bare prompt** (input is a description, not a file path):

1. **Scan the work area.**
   - Identify files likely to change.
   - Find existing test files for those areas (search for test/spec files that import, reference, or share names with the implementation files).
   - Note local patterns and conventions.

2. **Assess complexity and route.**

   | Complexity | Signals | Action |
   |---|---|---|
   | **Trivial** | 1-2 files, no behavioral change (typo, config, rename) | Proceed to Phase 1 step 2 (environment setup), then implement directly — no task list, no execution loop. Apply Test Discovery if behavior-bearing code is touched. |
   | **Small / Medium** | Clear scope, under ~10 files | Build a task list from discovery. Proceed to Phase 1 step 2. |
   | **Large** | Cross-cutting, architectural decisions, 10+ files, touches auth/payments/migrations | Inform the user this would benefit from `/plan` to surface edge cases and scope boundaries. Honor their choice. If proceeding, build a task list and continue. |

## Phase 1: Quick start

1. **Read plan and clarify** _(skip if arriving from Phase 0 with a bare prompt)_

   - For unified plans, size your read. A short plan (a screen or two) can be read in full. For a long implementation-ready plan, do **not** read the whole document first — build a section map, then read only what the active unit needs: metadata, `Goal Capsule`, `Verification Contract`, `Definition of Done`, the `Implementation Units` heading list, and only the active U-ID section plus referenced R/F/AE/KTD excerpts. Read appendices or unrelated U-IDs only when cited.
     - Markdown: scan headings with `rg -n '^#{1,3} ' <plan>`.
     - HTML: scan `<h1>`–`<h3>` elements and anchor ids.
     - Match stable section names / unit IDs (`Goal Capsule`, `Verification Contract`, `### U<N>.`, …), ignoring wrapper tags.
   - For legacy plans, read the document completely.
   - Treat the plan as a decision artifact, not an execution script.
   - Use sections such as `Implementation Units`, `Work Breakdown`, `Requirements`, `Files`, `Test Scenarios`, or `Verification` as primary source material.
   - Note `Execution note` on each unit — these carry execution posture (e.g., test-first, characterization-first).
   - Note `Deferred to Implementation` / `Implementation-Time Unknowns` before starting.
   - Note `Scope Boundaries` — explicit non-goals. Refer back if implementation drifts.
   - If anything is unclear or ambiguous, ask clarifying questions now.
   - Do not edit the plan body during execution. Progress lives in git commits and the task tracker, not the plan. Ignore legacy `- [ ]` / `- [x]` marks or `status:` fields on unit headings.

2. **Setup environment**

   First, check the current branch:

   ```bash
   current_branch=$(git branch --show-current)
   default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

   if [ -z "$default_branch" ]; then
     default_branch=$(git rev-parse --verify origin/main >/dev/null 2>&1 && echo "main" || echo "master")
   fi
   ```

   **If already on a feature branch** (not default):

   - Check whether the branch name is meaningful (e.g., `feat/login`, `fix/email-validation`). Auto-generated worktree names or opaque names are not meaningful.
   - If meaningless, suggest `git branch -m <meaningful-name>` derived from the plan title or work description.
   - Ask: "Continue working on `[current_branch]`, or create a new branch?"
   - If continuing, proceed to step 3. If creating new, follow Option A or B below.

   **If on the default branch**, choose:

   **Option A: Create a new branch**
   ```bash
   git pull origin [default_branch]
   git checkout -b feature-branch-name
   ```
   Use a meaningful name (e.g., `feat/user-authentication`, `fix/email-validation`).

   **Option B: Use a worktree (recommended for parallel development)**
   ```
   /worktree
   # Detects existing isolation, prefers harness-native worktree tool, else creates from default branch.
   ```

   **Option C: Continue on the default branch**
   - Requires explicit user confirmation.
   - Only proceed after the user explicitly says "yes, commit to [default_branch]".
   - Never commit directly to the default branch without explicit permission.

3. **Create task list** _(skip if Phase 0 already built one, or if Phase 0 routed as Trivial)_

   Use the platform's task tracking tool to break the plan into actionable tasks.

   - Derive tasks from implementation units, dependencies, files, test targets, and verification criteria.
   - Preserve U-IDs as prefixes in task subjects (e.g., "U3: Add parser coverage").
   - Carry each unit's `Execution note` into the task when present.
   - Read each unit's `Patterns to follow` before implementing.
   - Use each unit's `Verification` field as the primary "done" signal.
   - Do not expect the plan to contain implementation code, micro-step TDD instructions, or exact shell commands.
   - Include dependencies between tasks.
   - Prioritize based on what must happen first.
   - Include testing and quality-check tasks.
   - Keep tasks specific and completable.

4. **Choose execution engine, then strategy**

   For implementation-ready unified code plans, first pick the engine: inline/subagent (default), goal-mode, or dynamic-workflow. Read `references/execution-engines.md` for the host-capability probe, selection table, copyable prompts, and resume rules. An engine choice never changes tail ownership.

   For the inline/subagent engine, **prefer subagents for any structured multi-unit plan** — each worker gets a fresh context window for one unit. **Parallelize independent units whenever safe**; fall back to serial only when parallel isn't safe or the harness cannot isolate concurrent writes. Let the plan's `Dependencies` and `Files` drive batching.

   | Strategy | When to use |
   |---|---|
   | **Inline** | Trivial work, user interaction mid-flight, or bare prompts without structured units. |
   | **Serial subagents** | Default for structured multi-unit plans whose units are dependent, few, or whose parallel-safety is uncertain. |
   | **Parallel subagents** | Independent units (per the Parallel Safety Check) when the harness can isolate concurrent work. |

   **Parallel Safety Check** — before dispatching a batch:

   1. Map files to units from each candidate unit's `Files:` section (Create/Modify/Test paths).
   2. **File overlap is necessary but not sufficient.** Also serialize units that contend on shared types/APIs/interfaces, DB migrations, generated artifacts, lockfiles, snapshots, shared config/schema, or environment singletons (one dev server/port, shared database, browser sessions, package installs, MCP rate limits).
   3. **No contention:** dispatch the batch in parallel.
   4. **Contention with harness-native isolation:** parallel is recoverable but not automatically safe — overlapping edits still need a real merge. Serialize contending units by default; run parallel-isolated only when the expected merge is trivial. Log predicted overlap.
   5. **Contention without isolation (shared workspace):** serialize — in a shared directory only the last writer survives.
   6. **Cap concurrency** at ~3-5 workers even when more units are independent.
   7. **Abort criteria:** if a batch produces broad unplanned edits, out-of-scope test failures, or repeated conflicts, stop parallelizing and finish the rest serially.

   **Isolation is the harness's job, never `/work`'s** — never run `git worktree add` yourself. Probe what your subagent mechanism provides and pick the parallel path:
   - **Harness-native isolated workers** — each worker edits an isolated workspace the harness manages (e.g., Claude Code `Agent` with `isolation: "worktree"` + `run_in_background: true`). Parallelize freely, including overlapping-file units, subject to merge-cost judgment. Works even when already inside a worktree — harness worktrees are peers, not nested.
   - **Shared workspace only** — subagents run in your working directory. Parallelize disjoint-file units only; contending units run serial.
   - **No subagent mechanism:** run inline.

   **Dispatch** uses the harness's subagent/worker mechanism. Give each worker:
   - The plan path plus a **bounded unit packet** — Goal Capsule, Definition of Done, the unit's section, relevant Verification Contract entries, and any referenced R/F/AE/KTD excerpts. Do not send "read the whole plan."
   - The unit's Goal, Files, Approach, Execution note, Patterns, Test scenarios, Verification, and any resolved deferred questions.
   - Instruction to check whether test scenarios cover happy paths, edge cases, error paths, and integration, and supplement gaps before writing tests.
   - Instruction to report changed file paths in its final message.
   - **Do not commit in a shared workspace.** In worktree-isolated branches, workers may stage and commit inside their own branch; the orchestrator still owns merging those branches in dependency order and the authoritative test runs.

   **Shared-workspace constraints** — when subagents share your working directory: they must not `git add`, commit, or run the full test suite concurrently (index corruption + test interference); the orchestrator does all that after the batch. A worker may run a single focused unit test only if it touches no shared state.

   **Permission mode:** Omit the `mode` parameter when dispatching subagents so the user's configured permission settings apply. Do not pass `mode: "auto"`.

   **After each serial unit:** review the diff against the unit's scope and `Files:`, run relevant tests, fix before dispatching the next, update the task list, and commit.

   **After a parallel batch — the orchestrator integrates; never trust the handoff summary alone:**
   1. Wait for every worker to finish.
   2. **Inspect the actual tree, not reported paths.** Determine what each worker really changed (`git status`/diff).
   3. **Detect real collisions** — 2+ workers that actually modified the same file. In a shared workspace only the last writer survived: commit the non-colliding work first, then re-run the colliding units serially. With harness-native isolation the collision surfaces as a merge conflict at integration.
   4. **Review, test, and commit each unit in dependency order.** Stage only that unit's files, commit with a message derived from its Goal, run relevant tests, and fix before the next.
   5. Update the task list.
   6. **Release the workers** — close/clean up each worker handle so it stops holding a concurrency slot or leaving orphans.
   7. Dispatch the next dependency layer.

## Phase 2: Execute

1. **Task execution loop**

   For each task in priority order:

   ```
   while tasks remain:
     - Mark task in-progress
     - Read any referenced files from the plan or Phase 0
     - If the unit's work is already present and matches the plan's intent, verify it matches, mark complete, and move on
     - Look for similar patterns in codebase
     - Find existing test files for implementation files being changed (Test Discovery)
     - Implement following existing conventions
     - Add, update, or remove tests to match changes
     - Run System-Wide Test Check
     - Run tests after changes
     - Assess testing coverage
     - Mark task completed
     - Evaluate for incremental commit
   ```

   When a unit carries an `Execution note`, honor it. For test-first units, write the failing test before implementation. For characterization-first units, capture existing behavior before changing it. For units without an `Execution note`, proceed pragmatically.

   Guardrails:
   - Do not write the test and implementation in the same step when working test-first.
   - Do not skip verifying that a new test fails before implementing the fix or feature.
   - Do not over-implement beyond the current behavior slice when working test-first.
   - Skip test-first discipline for trivial renames, pure configuration, and pure styling work.

   **Test Discovery** — before implementing changes to a file, find its existing test files (search for test/spec files that import, reference, or share naming patterns with the implementation file). Changes to implementation files should be accompanied by corresponding test updates — new tests for new behavior, modified tests for changed behavior, removed or updated tests for deleted behavior.

   **Test Scenario Completeness** — before writing tests for a feature-bearing unit, check whether the plan's `Test scenarios` cover all applicable categories. If a category is missing or vague, supplement from the unit's context:

   | Category | When it applies | How to derive if missing |
   |---|---|---|
   | Happy path | Always for feature-bearing units | Read the unit's Goal and Approach for core input/output pairs. |
   | Edge cases | Unit has meaningful boundaries | Identify boundary values, empty/nil inputs, concurrent access. |
   | Error/failure paths | Unit has failure modes | Enumerate invalid inputs, permission/auth denials, downstream failures. |
   | Integration | Unit crosses layers | Identify the cross-layer chain and exercise it without mocks. |

   **System-Wide Test Check** — before marking a task done, pause and ask:

   | Question | What to do |
   |---|---|
   | What fires when this runs? | Read actual code for callbacks, middleware, observers, event handlers — trace two levels out. |
   | Do my tests exercise the real chain? | Write at least one integration test using real objects through the full chain. No mocks for interacting layers. |
   | Can failure leave orphaned state? | Trace failure path with real objects. Test cleanup or idempotency. |
   | What other interfaces expose this? | Grep for the method/behavior in related classes. Add parity now if needed. |
   | Do error strategies align across layers? | List specific error classes at each layer. Verify rescue list matches what lower layer raises. |

   Skip for leaf-node changes with no callbacks, no state persistence, no parallel interfaces.

2. **Incremental commits**

   | Commit when... | Don't commit when... |
   |---|---|
   | Logical unit complete | Small part of a larger unit |
   | Tests pass + meaningful progress | Tests failing |
   | About to switch contexts | Purely scaffolding with no behavior |
   | About to attempt risky/uncertain changes | Would need a "WIP" message |

   Heuristic: "Can I write a commit message that describes a complete, valuable change?"

   If the plan has Implementation Units, use them as a starting guide for commit boundaries — but adapt based on what you find. Use each unit's Goal to inform the commit message.

   Commit workflow:
   ```bash
   # 1. Verify tests pass (project's test command)
   # 2. Stage only files related to this logical unit
   git add <files related to this logical unit>
   # 3. Commit with conventional message
   git commit -m "feat(scope): description of this unit"
   ```

   Handle merge conflicts immediately. Incremental commits make conflict resolution easier.

3. **Follow existing patterns**

   - The plan should reference similar code — read those files first.
   - Match naming conventions exactly.
   - Reuse existing components where possible.
   - Follow the project's coding standards already in context.
   - When in doubt, grep for similar implementations.

4. **Test continuously**

   - Run relevant tests after each significant change.
   - Fix failures immediately.
   - Add new tests for new behavior, update tests for changed behavior, remove tests for deleted behavior.
   - Unit tests with mocks prove logic in isolation. Integration tests with real objects prove layers work together. If your change touches callbacks, middleware, or error handling, you need both.

5. **Simplify as you go**

   After completing a cluster of related implementation units (or every 2-3 units), review recently changed files for simplification opportunities — consolidate duplicated patterns, extract shared helpers, improve reuse.

   Do not simplify after every single unit; early patterns may diverge intentionally in later units. Wait for a natural phase boundary or when accumulated complexity is visible.

   Invoke `/simplify` at phase boundaries when the diff is >=30 lines. If `/simplify` is unavailable, do a brief manual pass.

6. **Figma Design Sync** (if applicable)

   For UI work with Figma designs:

   - Implement components following design specs.
   - Load `references/agents/figma-design-sync.md` and dispatch a generic subagent seeded with that local prompt to compare implementation against the Figma design.
   - Fix visual differences identified.
   - Repeat until implementation matches design.

7. **Frontend design guidance** (if applicable)

   For UI tasks without a Figma design — where the implementation touches view, template, component, layout, or page files, creates user-visible routes, or the plan contains explicit UI/frontend/design language:

   - Preserve existing design-system conventions.
   - Use real UI controls and states.
   - Keep layouts responsive.
   - Verify text does not overflow or overlap.
   - When browser tooling is available, inspect at desktop and mobile widths before final validation. If no browser access is available, do a code-level responsive/layout review and record that browser verification was unavailable.

8. **Track progress**

   - Keep the task list updated as tasks complete.
   - Note blockers or unexpected discoveries.
   - Create new tasks if scope expands.
   - Keep the user informed of major milestones.
   - Reference U-IDs and stable R-IDs / A/F/AE IDs in blockers, deferred-work notes, task summaries, and final verification — not routine status updates. Use IDs the plan supplies; do not invent ones it does not.
   - For long-running work, write a scratch progress artifact to `/tmp/odin/work/<run-id>/progress.json` (or equivalent) so state survives context compaction. Never write progress into the plan body.

## Phase 3-4: Quality check and finishing work

When all Phase 2 tasks are complete, load `references/shipping-workflow.md` and run the full shipping tail. Do not skip this.

**Code review path.** Review with `/review` — it self-sizes. Skip dedicated review only for purely mechanical diffs (formatting, dep-bumps, lint-only, generated). `/review` is review-only; apply fixes afterward per `references/review-findings-followup.md`, then handle residuals through the Residual Work Gate in `references/shipping-workflow.md`.

## Behavioral rules

- Ask clarifying questions once at the start; do not re-scope the plan into human-time phases or session subsets.
- Use the plan as authority; load the references it provides and match existing patterns rather than inventing.
- Run tests after each behavior-bearing change and fix failures immediately; do not batch testing to the end.
- Review every non-mechanical diff with `/review`; document the reason when skipping.
- Mark all tasks complete before finishing; do not leave features 80% done.
- Track progress in the task tracker, never in the plan body.
