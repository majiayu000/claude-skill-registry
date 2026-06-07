---
description: Implements an approved spec by having Claude design and run its own Claude Code dynamic workflow (real parallel subagents) — you hand it the goal and constraints, it chooses the orchestration. Test-first is enforced as a quality bar (tests accompany or precede code and the suite is left green), not as supervised Red-Green-Refactor. A peer of /optimus:tdd for spec implementation; prefer it for large or parallelizable specs where one linear pass is slow. Requires /optimus:init and a spec (auto-detects docs/specs/ or docs/jira/, or pass a path). Uses meaningfully more tokens than a normal session. Use when a spec is ready to build and you want fan-out implementation instead of turn-by-turn TDD cycles.
disable-model-invocation: true
---

# Workflow-Driven Implementation

Implement an approved spec by having Claude **design and run its own Claude Code dynamic workflow** — an orchestration of real parallel subagents that build the spec in the background. You supply the spec, the goal, and the constraints; Claude chooses the phases, how many agents to run, and how they divide and cross-check the work. Only the final result returns to this conversation.

This skill is a peer of `/optimus:tdd`. Both implement a spec and feed the same `→ /optimus:pr` handoff; they differ in *how* they build.

**The quality bar, not a ceremony.** This skill does not supervise Red-Green-Refactor. It hands Claude a test-first **quality bar** — tests accompany or precede the code they cover, the full suite is run and left green, and that green run is the completion gate. If you want enforced per-behavior test-first discipline with a failing-test-first guarantee (the Iron Law), use `/optimus:tdd` instead. For restructuring existing code without new behavior, use `/optimus:refactor`.

## Step 1: Pre-flight

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, run this skill inside the repo the user is targeting. If ambiguous, ask which repo.

### Verify prerequisites

Check that `.claude/CLAUDE.md` exists. If it doesn't, stop and recommend running `/optimus:init` first — coding guidelines and project context steer the workflow's quality bar.

This skill launches a Claude Code **dynamic workflow** (Step 4 invokes the Workflow tool). If dynamic workflows are not available in this session — a recent Claude Code is required, and on some plans the feature must be enabled in `/config` — stop now and tell the user to enable it. Do not proceed to create a branch in Step 3 for a launch that cannot run.

Load these documents (they become constraints in the workflow brief):

| Document | Role |
|----------|------|
| `.claude/CLAUDE.md` | Project overview — tech stack, test runner command |
| `coding-guidelines.md` | Code quality reference the workflow must follow |
| `testing.md` | Testing conventions — file location, naming, framework, mocking |
| `docs/product/tech-stack.md` *(if present)* | SDD steering — target stack |
| `docs/product/mvp-prd.md` *(if present)* | SDD steering — MVP scope |

Load the two `docs/` rows **only if they exist** (the optional spec-driven-development steering cascade scaffolded by `/optimus:spec-init`); see `$CLAUDE_PLUGIN_ROOT/references/sdd-mapping.md` for the precedence contract. For monorepos, read the "Monorepo Scoping Rule" section of `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` and load the targeted subproject's docs.

### Verify test infrastructure

Locate the test runner command from `testing.md`, `CLAUDE.md`, or project manifests (`package.json` scripts, `Makefile`, `Cargo.toml`, etc.). Run it once to confirm it works and the suite is **currently green**.

- **Green** — proceed to Step 2. (The post-workflow green run in Step 5 is only meaningful against a known-green baseline.)
- **Failing** — stop and report. Resolve existing failures first; otherwise the workflow's green gate is meaningless.
- **No test runner found** — stop and recommend `/optimus:init` to set up test infrastructure. For a project with no code or detectable stack yet, tell the user to pick **Scaffold new project** when init asks.

**Capture the coverage baseline now** — this green run is the only point before the workflow modifies the tree. Detect a coverage command per `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/coverage-detection.md`; if one exists, run it once and record the result as the Step 6 `Before` value. If none is available, skip this — Step 6 omits the Coverage section.

## Step 2: Acquire the spec

Resolve the spec with the shared cascade in `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/spec-context-detection.md` (explicit `docs/specs/`/`docs/jira/` reference → build-spec auto-discovery → JIRA auto-discovery → none, plus long-spec distillation to a single-sentence goal).

If the cascade resolved a spec, use it. Otherwise, if the user gave a task inline (e.g., `/optimus:workflow "Build the CSV import pipeline"`), use it. Otherwise, use `AskUserQuestion` — header "Spec", question "What spec or feature should the workflow implement?".

Whatever the source — a spec or JIRA context the cascade resolved, an inline argument, or the answer above — apply the shared reference's **Distillation** step to the final spec/goal: if it runs longer than ~2-3 sentences, distill it to a single-sentence goal (the brief's `Goal:` slot in Step 4) and confirm via `AskUserQuestion` before proceeding.

**Light suitability guard** (this skill skips TDD's full classification — a workflow is not bound to testable-behavior decomposition):
- If the task is clearly **restructuring existing code without new behavior** → recommend `/optimus:refactor` and stop.
- If it is **documentation-only or pure configuration** → note a workflow is overkill; a normal turn (or `/optimus:commit`) suffices. Stop unless the user insists.
- Otherwise, proceed.

## Step 3: Create a feature branch

Keep the user's original branch clean — all workflow edits land on a new branch.

1. Record the current branch (this becomes the PR/MR target): `git rev-parse --abbrev-ref HEAD`
2. Derive a branch name. Read `$CLAUDE_PLUGIN_ROOT/skills/commit/references/branch-naming.md` for the convention. `<type>` is `feat` (or `fix`); `<description>` is the slugified goal.
3. Create and switch: `git checkout -b <branch-name>`
4. Report:

```
## Branch

Created branch `<branch-name>` from `<original-branch>`.
The workflow will build on this branch.
```

Do **not** add git-worktree isolation here — workflow subagents already run as isolated background agents with auto-approved edits; a second isolation layer would only blur the edit-scope guardrail in Step 4.

## Step 4: Design and run the workflow

Compose the brief below from the spec (Step 2) and the loaded docs (Step 1), then **launch the workflow now, in this live session: design a workflow script that carries out the brief, then invoke the Workflow tool with that script.** The brief is the source material for the script — its task, scope, and quality bar; *you* author the orchestration and start the run. Do **not** emit the brief as a copy-paste block for the user to run, and do not wait for a trigger phrase — calling the Workflow tool is what launches it. Claude Code shows the planned phases for the user to approve before the run starts; tell the user to expect that approval gate and that the run uses meaningfully more tokens than a normal turn.

Fill the bracketed slots: scope from the spec's Components / Acceptance Criteria and Out-of-Scope sections — when the source is a JIRA ticket or an inline goal with no Out-of-Scope section, derive the in-scope set from the goal and acceptance criteria and set out-of-scope to "anything not required by the stated goal". Build the edit-forbidden list from the project's protected paths: read `.claude/settings.json` `permissions.deny` if it exists (written by `/optimus:permissions`), and always include the defaults shown in the brief's Edit-mode block below (`.git`, `.claude/`, CI config, generated/vendored dirs, unrelated subprojects). If `/optimus:permissions` has not run, use those defaults and tell the user that running it first tightens the boundary.

**Authoring rules (do not violate):**
1. **Do not prescribe** the phases, the number of agents, or a phase plan. A pattern hint (fan-out / pipeline / adversarial cross-check) is an *optional* preference only — Claude is capable of choosing the shape that fits the spec.
2. **Scope is mandatory** — bound the target set to the spec and give an early-stop condition. Do **not** set concurrency or total-agent caps (the brief notes the runtime's auto-caps).
3. **State the edit guardrail explicitly** — name where agents may and may not edit (the brief's Edit-mode block explains why this boundary is the only thing keeping changes in scope).

The brief:

```
Run a workflow to implement the spec below in this repository.

Spec: <path or inline goal from Step 2>
Goal: <single-sentence goal from Step 2>

Desired outcome: working, integrated code that satisfies the spec — every in-scope
component built, wired together, and covered by tests, with the full project test
suite passing.

You design the orchestration. Decide the phases, how many agents to run, how to divide
the spec across them, and where it's worth having agents cross-check or integrate each
other's work. I'm giving you the spec, the constraints, and the quality bar — you write
the workflow script and choose its shape. (A fan-out by component or a build-then-integrate
pipeline are both fine if they fit; that's your call, not a requirement.)

Quality bar — test-first:
- Tests accompany or precede the code they cover; do not ship implementation for an
  in-scope behavior without a test that exercises it.
- Follow this project's testing conventions (framework, file location, naming, mocking)
  from testing.md, and its code quality rules from coding-guidelines.md.
- Before returning, run the full project test suite and leave it green. The green run is
  the completion gate — do not report done on a suite you have not run, and drop or fix
  anything you cannot get to pass.
- If this project has a lint or type-check command (in CLAUDE.md or its manifest), leave it
  clean too — passing tests do not catch type errors.
- Don't just run more agents — apply whatever review or cross-checking makes the result
  trustworthy.

Scope:
- In scope: <components / acceptance criteria from the spec>.
- Out of scope: <the spec's Out-of-Scope items>. Don't build beyond the spec, and don't
  add documentation the spec didn't ask for.
- Edit mode: agents may create and edit files anywhere in the repo needed to implement
  the spec, INCLUDING tests. Do NOT touch: <forbidden paths — e.g. .git, .claude/, CI
  config, generated/vendored dirs, unrelated subprojects>. (Workflow agents auto-approve
  edits regardless of session mode — this boundary is the only thing keeping edits in scope.)
- Stop early once the spec is fully implemented and the suite is green; keep work bounded
  to the in-scope targets above. (The runtime auto-caps concurrency and total agent count —
  you don't set these.)

Output: the working code in the working tree, plus a final summary listing each component
you built, the test files that cover it, the final test result (e.g. "142 passed"), and
anything in scope you deliberately deferred and why.
```

For a small, clearly-bounded spec, trim the brief to its essentials (task line, scope, edit-mode, the test-first one-liner, output) — match the weight to the task; never pad.

## Step 5: Verify the result (hard gate)

The workflow returns only its final answer — intermediate agent work stayed in the workflow's own variables. **Re-verify independently; never report success on the workflow's self-report.**

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` and apply its gate function. First confirm the workflow actually did the work: run `git status --short` and `git diff --stat`, and verify the tree was modified in the spec's in-scope areas — per the protocol's evidence table, a completed agent is proven by the VCS diff, not its self-report, so an empty or off-target diff is a gate failure (handle it like the red case below) even when the suite is green. Then run the full test suite fresh now, read the complete output, and confirm it is **green** (0 failures, exit 0). If a lint or type-check command is configured (`CLAUDE.md` or the project manifest), run it too and require it to pass — type errors hide behind passing tests, so a green suite with a failing type-check is **not** a pass. If you captured a coverage baseline in Step 1, run the coverage command again now to get the Step 6 `After` value; if that run fails or yields no percentage, omit the Coverage section in Step 6 rather than emitting a half-filled one.

- **Suite green, lint/type-check clean, and the diff shows the in-scope work** — proceed to Step 6.
- **Suite red, lint/type-check failing, an empty or off-target diff, or a partial/broken tree** — do **not** commit, and do **not** proceed to Step 6 or Step 7. Report the failures with evidence (the actual failing output). Then use `AskUserQuestion` — header "Workflow result", question "The workflow did not leave the suite green and clean. How do you want to proceed?":
  - **Fix forward** — "Run a focused follow-up (a normal turn or a smaller workflow) to green the suite and clear any type/lint errors." When it finishes, **re-run this Step 5 gate** from the top — only a green, clean re-verification advances to Step 6.
  - **Discard** — "Abandon this attempt." The workflow's output is still uncommitted in the working tree and is usually new, untracked files, so `git checkout`/`git reset` alone won't clear it: show the user `git status`, then have them run `git reset --hard` **and** `git clean -fd` to drop tracked and untracked changes before switching off the branch. Then **stop** — do not emit a summary or commit.

  Do not auto-revert — leave the user in control of the isolated branch.

## Step 6: Emit the Implementation Summary

Emit this block into the conversation so `/optimus:pr` can read it. The headings `## Implementation Summary` and `### Components Built` are **case-sensitive literals** the `/optimus:pr` detector keys on — do not reword them. Populate from the workflow's returned summary, the Step 5 verification run, and `git` state.

```
## Implementation Summary

### Components Built
| # | Component | Tests | Status |
|---|-----------|-------|--------|
| 1 | [component] | [test file(s)] | ✓ Complete |
| 2 | [component] | — | Deferred — [reason] |

### Stats
- Orchestration: [one line — how Claude shaped the workflow, e.g. "fan-out by component, 6 agents, then 1 integration pass"]
- Tests: [N] written/updated, all passing ✓
- Files created: [list]
- Files modified: [list]

### Verification
- Test suite: [command] — [result, e.g. "142 passed", exit 0]
- Type-check / lint: [result, or omit this line if none configured]

### Coverage
[The `Before` baseline is captured in Step 1 and the `After` value in Step 5, using the coverage
command detected per `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/coverage-detection.md`. Follow
that reference's "When to omit" rule — emit this section only when both Before and After are real
percentages.]
- Before: [X]%
- After: [Y]%
- Delta: +[Z]%
```

## Step 7: Commit, push, and hand off

1. **Commit** the work the workflow produced. Stage specific files (prefer `git add <files>`; use `git add -A` only if many changed). Never stage files that look like secrets (`.env`, credentials, keys) — warn if any appear in `git status`. Generate a conventional commit message per `$CLAUDE_PLUGIN_ROOT/skills/commit-message/references/conventional-commit-format.md` and commit. (A single commit for the fan-out is fine — there are no per-cycle commits to reconstruct.)
2. **Push:** `git push -u origin <branch-name>`. If the push fails, report the error and stop — the user must resolve it before a PR/MR can be created.
3. **Report:**

```
### Git Activity
- Branch: `<branch-name>` (from `<original-branch>`)
- Commits: [N]
- Pushed: ✓
```

### Next step — create the PR/MR with `/optimus:pr`

Run `/optimus:pr` **in this same conversation**. Staying here lets `/optimus:pr` read the `## Implementation Summary` block above and populate the PR description's `## Intent` (Scope from components built, Non-goals from deferred components) and `## Test plan` (one item per component, plus the coverage delta); it then owns the rest of the PR/MR flow (default-branch detection, CLI install, existing-PR detection, preview-and-confirm — see `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md`). (If you stopped before the auto-commit, run `/optimus:commit` first to capture the work.)

Tell the user the closing tip per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` "Closing tip wording" — use **Variant A** with `<continuation-skill(s)>` = `/optimus:pr` and `<non-continuation-examples>` = `/optimus:code-review`.
