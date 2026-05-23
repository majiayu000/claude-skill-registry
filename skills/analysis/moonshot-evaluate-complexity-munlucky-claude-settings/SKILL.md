---
name: moonshot-evaluate-complexity
description: Evaluates complexity (simple, medium, complex) based on estimated files/lines/time. Use after task classification.
context: fork
---

# PM Complexity Evaluation

## Inputs
- `analysisContext.estimates.estimatedFiles`
- `analysisContext.estimates.estimatedLines`
- `analysisContext.estimates.estimatedTime`
- `analysisContext.request.taskType`

## Criteria
- `simple`: 1-2 files, <= 100 lines, <= 1 hour
- `medium`: 3-5 files, 100-300 lines, 1-3 hours
- `complex`: 6+ files, 300+ lines, 3+ hours

If estimates are missing, infer from taskType keywords and note low confidence.

## Output (patch)
```yaml
complexity: medium
estimates.estimatedFiles: 4
estimates.estimatedLines: 180
estimates.estimatedTime: 2h
notes:
  - "complexity=medium, estimated=heuristic"
```
