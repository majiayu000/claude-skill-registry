---
name: efficiency-tracker
description: Tracks workflow status and generates a flow report.
---

# Efficiency Tracker Skill

**Role**: Record workflow status and generate a flow report (timeline, blocking, verification results, commit links).

## Inputs
- Feature name: `{feature-name}`
- Phase/branch info (optional)
- Verification command results (optional)

## Behavior
1. Record start/end timestamps and active phase.
2. Add blocking intervals (e.g., waiting for UI spec, waiting for API spec) as notes.
3. Record verification commands (typecheck/build/lint) and results.
4. Record changed files/commit links and author notes.
5. Append to or create `{tasksRoot}/{feature-name}/flow-report.md`.

## Outputs
- flow-report.md update log
- Optionally add timeline entries to session-log/day-...

## Execution snippet
```
Update the workflow report.
- Feature: {featureName}
- Phase: {phase}
- Blocking notes: {blockingNotes}
- Verification results: {verifyResults}
- Commits/files: {commitRefs}
Output: flow-report.md update
```

## Token limit
- **Per `.claude/docs/guidelines/document-memory-policy.md`**: Keep flow-report.md under 4000 tokens
- Archive older entries if exceeding limit
