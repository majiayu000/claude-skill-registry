---
name: implementation-runner
description: Performs implementation in the chain and records completion state and changed files in analysisContext. Use during implementation.
---

# Implementation Runner

## Inputs
- `analysisContext.request.userMessage`
- `analysisContext.decisions.skillChain`
- `analysisContext.repo.openFiles`
- `analysisContext.artifacts.contextDocPath` (if present)

## Procedure
1. Check requirements and context.
2. Define change scope and implement.
3. Record changed files and key change summary.
4. Update implementation completion in `analysisContext`.

## Output (patch)
```yaml
signals.implementationComplete: true
repo.changedFiles:
  - src/...
notes:
  - "implementation: complete, changed_files=3"
```

## Rules
- Do not call other skills/subagents.
- If failed or deferred, record the reason in `notes`.
