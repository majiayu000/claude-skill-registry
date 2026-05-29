---
name: moonshot-classify-task
description: Classifies a user request into task types (feature, modification, bugfix, refactor) and extracts intent keywords. Use at the start of PM analysis.
context: fork
---

# PM Task Classification

## Inputs
- `analysisContext.request.userMessage`

## Procedure
1. Identify intent keywords from the user message.
2. Select one taskType: `feature | modification | bugfix | refactor`.
3. Set confidence: `high | medium | low`.

## Heuristics
- feature: "new", "add", "implement", "create", "build"
- modification: "change", "modify", "improve", "adjust", "remove"
- bugfix: "bug", "error", "broken", "fails"
- refactor: "refactor", "clean up", "restructure", "remove duplication"

## Output (patch)
```yaml
request.taskType: feature
request.keywords:
  - implement
  - batch
notes:
  - "taskType=feature, confidence=high"
```
