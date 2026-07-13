---

name: fix
description: >
  Use when something is broken and the user wants it fully diagnosed AND
  resolved end-to-end, not just investigated — chains investigation,
  implementation, testing, and commit based on scope: bugs, Claude Code hook
  failures, dependency/import errors, or PR review feedback. Examples: "fix
  this failing build", "fix this bug", "the hook isn't firing, fix it",
  "resolve these dependency errors", "address the PR feedback and fix the
  code".
allowed-tools: [Bash, Read, Grep, Write, Edit, Task]
requires_rules:
  - swarm-patterns
  - agent-routing
requires_domain: software-development
---

# Fix

Workflow orchestrator for bug investigation and resolution. Chains specialized skills based on issue scope.

## Usage

```
/fix <scope> [options] [description]
```

If invoked with no/partial arguments, see `question-flow.md` for the guided
AskUserQuestion phases that resolve scope + options before Step 0 below.

## Scopes

| Scope | Chain | Description |
|-------|-------|-------------|
| `bug` | debug -> implement_task -> test-driven-development -> commit | General bug fix workflow |
| `hook` | debug-hooks -> hook-developer -> implement_task -> test hook | Hook-specific debugging |
| `deps` | dependency-preflight -> oracle -> plan-agent -> implement_plan -> qlty-check | Dependency issues |
| `pr-comments` | github-search -> research-codebase -> plan-agent -> implement_plan -> commit | Address PR feedback |

## Options

| Option | Effect |
|--------|--------|
| `--no-test` | Skip regression test creation |
| `--dry-run` | Diagnose only, don't implement fix |
| `--no-commit` | Don't auto-commit the fix |

## Where to Look

| File | Load when you need... |
|------|------------------------|
| `question-flow.md` | `/fix` invoked bare — guided Phase 0-4 AskUserQuestion flow to resolve scope/options |
| `workflow-diagnosis.md` | Step 0 (load orchestration) through Phase 4.5 — parse args, parallel investigation, diagnosis report, human checkpoint, premortem |
| `workflow-implementation.md` | Worktree option through Phase 8 — per-scope implementation routing, regression test, verification checkpoint, commit |
| `chains.md` | Flow diagrams per scope (bug/hook/deps/pr-comments) |
| `handoff-examples.md` | Handoff YAML format + worked invocation examples |

<HARD-GATE>
Do NOT apply a fix until:
1. Root cause is identified (not just symptoms)
2. The bug has been reproduced
3. Pre-mortem: "What could go wrong with this fix?" has been considered

(Enforced at the end of Phase 4.5 in `workflow-diagnosis.md`.)
</HARD-GATE>

## Error Handling

| Error | Action |
|-------|--------|
| Investigation finds nothing | Ask user for more context |
| User rejects diagnosis | Refine hypothesis with user input |
| Fix breaks other tests | Rollback, refine approach |
| User rejects verification | Offer to revert or adjust |
| Commit fails | Present error, offer retry |

## Integration with Other Skills

This skill orchestrates:
- `debug` / `debug-hooks`: Initial investigation
- `sleuth`: Parallel investigation agent
- `kraken`: TDD implementation agent
- `implement_task`: Single task implementation
- `test-driven-development`: Test creation
- `plan-agent`: Complex fix planning
- `dependency-preflight`: Dependency checks
- `oracle` / `research-codebase`: Context gathering
- `github-search`: PR context fetching
- `qlty-check`: Quality verification
- `premortem`: Risk assessment before implementation
- `commit`: Git commit workflow
- `create_handoff`: Session handoff

## Checkpoints Summary

| Checkpoint | Purpose | Skip Condition |
|------------|---------|----------------|
| After diagnosis | Confirm root cause | Never skip |
| After premortem | Accept or mitigate risks | No HIGH tigers |
| After fix | Verify resolution | Never skip |
| Before commit | Review changes | `--no-commit` |

The human checkpoints are critical for:
1. Preventing wrong fixes from being implemented
2. Ensuring user understands what changed
3. Catching edge cases only humans notice

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The fix is obvious, no need to investigate" | Obvious fixes often mask deeper root causes. Investigate first. |
| "I'll skip the reproduction step" | Without reproduction, you can't verify the fix works. |
| "This is a simple one-liner fix" | Simple fixes in complex systems still need testing. |
| "I already know what's wrong" | Confirmation bias. Let the evidence lead, not assumptions. |
| "It works on my end" | Environment-specific fixes hide the real bug. Reproduce in context. |
