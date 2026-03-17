---
name: moonshot-detect-uncertainty
description: Detects missing requirements and generates clarification questions. Use after classification/complexity to decide if user input is needed.
context: fork
---

# PM Uncertainty Detection

## Inputs
- `analysisContext.request.userMessage`
- `analysisContext.request.keywords`
- `analysisContext.request.taskType`
- `analysisContext.signals.hasContextMd`

## Triggers and questions
- UI/version: if UI/screen keywords exist, confirm design spec version
- API: if API keyword exists, confirm endpoint, request/response schema, error format
- Date range: if date/period keywords exist, confirm single vs range
- Paging: if list/table keywords exist, confirm server vs client paging
- Error handling: for new features, confirm alert/toast/inline policy

## Output (patch)
```yaml
missingInfo:
  - category: api-spec
    priority: HIGH
    question: "Please share the API endpoint, request/response schema, and error format."
    reason: "A stable contract is required for mock and type definitions."
signals.hasPendingQuestions: true
```
