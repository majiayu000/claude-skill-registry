---
name: ai-onboard
description: "Use at session start to detect available skills, load active context, and enforce skill usage discipline for the current session."
effort: medium
argument-hint: ""
---


# Onboard

## Purpose

Framework bootstrap and enforcement. Detects available skills, loads active context (spec, tasks, decisions), presents quick status, and enforces skill usage discipline. Prevents agents from bypassing skills with rationalizations.

## Trigger

- Auto-triggered via SessionStart hook
- Manual: `/ai-onboard`
- Context: beginning of any non-trivial session.

## Procedure

1. **Detect skills** -- scan `.claude/skills/` for available SKILL.md files. Build a capability map.

2. **Load active context**:
   - Read `.ai-engineering/specs/spec.md` -- current spec
   - Read `.ai-engineering/specs/plan.md` -- current tasks
   - Read `.ai-engineering/state/decision-store.json` -- active decisions and risk acceptances
   - Read `.ai-engineering/contexts/team/lessons.md` -- accumulated rules and patterns

3. **Present status** -- concise summary to user:
   ```
   Active spec: spec-054 (Hooks, Security, Observability)
   Tasks: 12/18 complete, 2 blocked
   Decisions: 3 active, 1 expiring in 5 days
   Skills: 29 loaded
   ```

4. **Enforce skill discipline** -- install the following rule for the session:

   > **If a skill applies to the current task, you MUST use it.** No exceptions. No "this is too simple" shortcuts.

## Red Flags Table

Rationalization patterns agents use to skip skills. Every one of these is wrong.

| # | Rationalization | Why it is wrong | Correct action |
|---|----------------|-----------------|----------------|
| 1 | "This is too simple for planning" | Simple tasks still need scope definition | Use `/ai-plan` (trivial pipeline) |
| 2 | "I'll just make a quick fix" | Quick fixes skip root cause analysis | Use `/ai-debug` |
| 3 | "Tests aren't needed for this change" | Every behavioral change needs verification | Use `/ai-test` |
| 4 | "I already know the answer" | Confidence without verification is the #1 source of bugs | Use `/ai-explore` first |
| 5 | "The user is in a hurry" | Skipping process creates more delay from rework | Follow the process faster, do not skip steps |
| 6 | "This is just a config change" | Config changes affect runtime behavior | Use `/ai-test` to verify |
| 7 | "I'll add tests later" | Later never comes; RED before GREEN | TDD protocol: tests first |
| 8 | "The existing tests cover this" | Assumption without verification | Run tests, check coverage |
| 9 | "This doesn't need a spec" | Every pipeline requires a spec, even trivial | Use `/ai-brainstorm` |
| 10 | "I'll clean up the commit message later" | Commit messages are permanent documentation | Use `/ai-commit` |
| 11 | "Security scanning would slow us down" | A leaked secret takes hours to rotate | Gitleaks runs in seconds |
| 12 | "This refactor is obvious" | Obvious refactors still need test verification | Use `/ai-simplify` |

## Detection Rules

When the user's request matches these patterns, enforce the corresponding skill:

| User intent pattern | Required skill |
|-------------------|----------------|
| "implement", "build", "add feature" | `/ai-plan` then `/ai-dispatch` |
| "fix", "bug", "broken", "not working" | `/ai-debug` |
| "test", "coverage", "verify" | `/ai-test` |
| "refactor", "restructure", "move" | `/ai-simplify` |
| "explain", "how does", "what is" | `/ai-explain` |
| "commit", "push", "save" | `/ai-commit` |
| "PR", "pull request", "review" | `/ai-pr` |
| "deploy", "release", "publish" | `/ai-release` |
| "conflict", "merge conflict" | `/ai-resolve-conflicts` |
| "incident", "outage", "postmortem" | `/ai-postmortem` |

## Quick Reference

```
/ai-onboard     # manual bootstrap (usually auto-triggered)
```

No arguments. Reads project state and configures the session.

## Boundaries

- Onboard is read-only -- it does not modify project files
- It does not execute tasks -- it configures the session for correct execution
- If no active spec exists, report it but do not block the session

$ARGUMENTS
