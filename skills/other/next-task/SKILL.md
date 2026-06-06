---
name: next-task
description: Select the next backlog task and drive it through isolated implementation, review, docs, verification, and publish gates from a git-branchless detached HEAD. Use when "next task", "work the backlog", "pick the next issue", "do the next thing", or "start the next task".
disable-model-invocation: true
metadata:
  short-description: Isolated backlog orchestrator
---

# next-task — extend-op backlog-to-branch orchestrator

`next-task` is an `extend` op-cell: select one real backlog item, isolate it, implement it, prove it, and end at an explicit delivery decision. It is a workflow driver, not a suggestion engine. It records the chosen task verbatim, separates planning from implementation, runs quality gates before publish, and never pushes until the final user decision.

Load these local references before running the workflow:

- `references/isolation.md` — detached-HEAD setup, branchless recovery, branch/push/PR path.
- `references/gates.md` — slop, docs/changelog, review-loop, and repo-native verifier gates.

## When to Apply / NOT

Apply when the user explicitly asks for the next task, backlog work, next issue selection, or a complete task-to-branch workflow.

Do **not** apply for ad-hoc bug fixes with a known target, pure review, pure planning, broad project audits, speculative roadmap work, or any task that should stay in the current checkout. This skill is explicit-invocation-only.

## State Contract

Use only `.outline/next-task/`:

```json
{
  "flow.json": {
    "version": 1,
    "status": "selecting|isolating|exploring|planning|implementing|gating|complete|blocked",
    "phase": "source|selection|isolation|explore|plan|implement|gates|decision",
    "task": { "id": "", "source": "", "title": "", "body": "", "labels": [], "url": "" },
    "policy": { "source": "", "filters": {}, "stopPoint": "publish|pr|local|queue|pick-another" },
    "selection": { "score": 0, "readiness": [], "blockers": [] },
    "git": { "mode": "detached-head", "base": "", "baseSha": "", "startSha": "", "headSha": "", "publishBranch": "" },
    "decisions": [],
    "gateResults": [],
    "updatedAt": "ISO-8601"
  },
  "current.md": "verbatim selected task text",
  "queue.md": "optional local queue source",
  "tasks.json": "optional active-task registry for collision avoidance",
  "low-debt.md": "LOW review findings that do not block critical/high cleanup"
}
```

`current.md` is not a summary. Paste the selected issue/card/backlog item exactly, then append a short provenance block: source, selection time, base ref, chosen stop point.

## Workflow

### 1. Resolve task source

1. Detect available sources:
   - GitHub issues when `gh` is authenticated and a remote points at GitHub.
   - GitLab issues when `glab` is authenticated and a remote points at GitLab.
   - Local backlog files: `PLAN.md`, `TODO.md`, `tasks.md`, `docs/**/*.md`, and `.outline/next-task/queue.md`.
2. If more than one source is plausible, use `ask` with a single-select question. One option is Recommended: prefer the source with explicit open tasks and tracker metadata; otherwise prefer `.outline/next-task/queue.md`; otherwise local Markdown.
3. Capture optional filters in the same decision: label, milestone, assignee, priority, and stop point.
4. Fetch with native commands/tools:

```bash
gh issue list --state open --json number,title,labels,state,body,milestone,assignees,createdAt,url --limit 100

glab issue list --state opened --output json --per-page 100
```

For Markdown backlogs, use `find` to locate candidate files and `search` with:

```text
^\s*[-*]\s+\[ \]\s+(?:\((P0|P1|P2|critical|high|medium|low)\)\s*)?(.*)$
^\s*(TODO|FIXME|NEXT|P0|P1|P2|CRITICAL|HIGH):\s+(.*)$
```

5. Normalize every candidate to:

```json
{
  "id": "source-local-id",
  "source": "github|gitlab|markdown|queue",
  "title": "",
  "body": "",
  "labels": [],
  "priority": "critical|high|medium|low|unknown",
  "milestone": "",
  "dependencies": [],
  "filesMentioned": [],
  "url": "",
  "raw": "verbatim source text"
}
```

### 2. Select and claim the next task

1. Exclude already-claimed tasks in `.outline/next-task/flow.json` or any active `.outline/next-task/tasks.json` registry you find in sibling worktrees.
2. Exclude GitHub issues that already have an open PR. Fetch once:

```bash
gh pr list --state open --json number,title,body,headRefName,url --limit 100
```

Treat closing keywords in PR body, title `(#N)`, and issue-number branch suffixes as PR-linked evidence. Closing keywords are stronger than suffixes.
3. Score remaining candidates:

| Signal | Score |
|---|---:|
| `critical`, `P0`, `sev0`, blocking release | +100 |
| `high`, `P1`, `sev1` | +50 |
| `security`, `vulnerability`, `CVE` | +40 |
| `bug`, `regression`, `crash`, `data-loss` | +30 |
| `small`, `quick`, `good first`, file count <= 3 | +20 |
| Bug older than 30 days | +10 |
| Missing dependency / blocked label | -100 |
| Mentioned files do not exist and task is not a creation task | -25 |
| Open linked PR | exclude |

4. Readiness check before presenting:
   - Dependencies marked done or absent.
   - Mentioned files exist, or the task is explicitly about creating them.
   - Required secrets/accounts are not necessary for local implementation; if they are, mark blocked.
   - The task has enough acceptance text to plan; if not, ask one clarifying question or choose another candidate.
5. Present top five with `ask`, single-select. Each option includes score, labels, blockers, and provenance. If no task is ready, offer: widen filters, choose a blocked task anyway, edit `.outline/next-task/queue.md`, or stop.
6. Write `.outline/next-task/current.md` with the selected task verbatim. Update `flow.json` with task, policy, score, and `phase: isolation`.

### 3. Isolate in git-branchless detached HEAD

Run the recipe in `references/isolation.md`.

Required invariant: implementation starts from detached HEAD, not a branch. Branch creation is a publish step after gates pass.

Minimum sequence:

```bash
git fetch --prune origin
git checkout --detach origin/<base>
```

If no remote base exists and the user explicitly accepts local-only work, detach from current `HEAD` and record `base: HEAD` in `flow.json`.

Claim before editing. Validate all untrusted task fields before using them in a ref, path, shell argument, or branch name. Never force-push.

### 4. Explore, plan, approve, implement

1. **Explore.** Delegate discovery to a generic ODIN `explore` agent when the affected files are unknown; otherwise do the narrow lookup directly. Required output:
   - task understanding;
   - primary files, related files, tests, docs;
   - existing patterns to follow;
   - dependency/caller risks via codegraph when indexed, otherwise `ast-grep` + search;
   - edge cases and verifier command candidates.
2. **Plan.** Use a generic `plan` or `task` agent for non-trivial tasks. The plan must be concrete JSON or Markdown with ordered steps, files, tests, risks, verification commands, and rollback scope. Do not allow implementation in the planning pass.
3. **Approve.** Present the plan with `ask`:
   - `approve-plan` (Recommended when specific, testable, and scoped);
   - `revise-plan`;
   - `pick-another-task`;
   - `stop-keep-claimed`.
4. **Implement.** Use generic ODIN `task` or `deep_task` agents for disjoint file groups, or implement directly for narrow changes. Implementation agents may edit and commit, but may not push, create PRs, mark gates passed, or delete the task claim.
5. Commit per concern while detached:
   - implementation;
   - tests;
   - docs/config;
   - gate fixes.

### 5. Run gates

Run all gates in `references/gates.md` in order:

1. Slop cleanup gate — deterministic HIGH-only cleanup, verifier, rollback on regression.
2. Docs/changelog sync gate — safe version/Unreleased fixes only; flag semantic drift.
3. Review gate — parallel generic reviewer agents, false-positive contract, critical/high loop with stall detection.
4. Repo-native verifier gate — the project’s own test/lint/build/type command set must pass.

Gate mutations are ordinary commits only after green verification. On any red verifier, restore the offending batch with `git restore -- <files...>`, rerun the same verifier to confirm baseline recovery, and keep the gate open.

### 6. Completion decision

Use `ask` after all gates pass. Single-select:

1. `publish-branch` — Recommended when the stop point is branch publication. Create branch at detached tip and push: `git branch <branch> HEAD`; `git push -u origin <branch>`.
2. `open-pr` — create branch and push, then `gh pr create --base <base> --head <branch> --title <title> --body <summary>`.
3. `keep-in-queue` — leave local commits and state intact; record blocker/next action in `flow.json` and `current.md`.
4. `pick-another-task` — release or close the current claim per user choice, then restart at source resolution.

Never force-push. Never delete remote branches. If publication fails because a branch already exists, choose a new branch suffix or ask.

## Anti-patterns

- Branch-first implementation. Detached HEAD is the work surface; branches are publish artifacts.
- Auto-selecting a source when multiple real sources exist.
- Summarizing the selected task instead of recording the source text verbatim.
- Implementing before the plan is approved.
- Letting implementation agents run review, docs, PR, or push steps.
- Single-reviewer approval for a non-trivial diff.
- Accepting false-positive dismissals without reasons.
- Auto-fixing MEDIUM/LOW cleanup findings.
- Guessing documentation rewrites beyond exact version and minimal changelog fixes.
- Treating missing tests as passing tests.
- Keeping gate fixes after a red verifier.
- Force-pushing or rewriting remote history.
- Silently shrinking the selected task to an easier subset.

## Validation Gates

| Gate | Pass Criteria | Blocks |
|---|---|---|
| Source resolved | Exactly one source selected, filters recorded, candidates normalized | Ambiguous source without `ask` |
| Task selected | Score/readiness computed, user selected one option, `current.md` contains verbatim task | No ready task or no recorded task |
| Claim written | `.outline/next-task/flow.json` updated before edits | Concurrent claim risk |
| Isolation | Detached HEAD from validated base; branch not created yet | Dirty state, invalid base, unsafe slug |
| Exploration | Primary/related/test/doc surfaces known or explicitly unavailable | Unknown edit surface |
| Plan approval | User approved specific plan with tests and verification | Implementation attempt |
| Implementation | Plan steps complete, commits are concern-sized | Uncommitted or partial work |
| Slop gate | HIGH deterministic cleanup applied or flagged, verifier green | Regression or unsafe fix |
| Docs gate | Safe fixes applied; semantic drift flagged | Public-surface drift unreported |
| Review gate | No open critical/high findings, or explicit user deferral at iteration cap/stall | Open critical/high without decision |
| Verifier gate | Repo-native test/lint/build/type commands pass | Any red required command |
| Decision gate | User chose publish/PR/queue/pick-another | Any remote action before choice |

Output at completion: selected task, detached-head base, commits created, changed files, gate results, verifier commands, rollback actions if any, and final decision.