---
name = "research"
description = "Run source-backed technical research and convert findings into implementation-ready guidance."
---

## Purpose

Use this skill when external documentation, standards, or library comparisons are needed.

## Trigger

- User asks for latest API behavior or version-sensitive guidance
- Tradeoff decisions require evidence from primary sources

## Workflow

1. Split the question into focused research sub-questions.
2. Prefer official docs/specs and primary maintainers.
3. Record version/date context and confidence.
4. Compare options with explicit criteria.
5. Produce implementation recommendations for this repository.

## Output Template

```markdown
## Key Findings
- ...

## Source-Based Comparison
- Option A: ...
- Option B: ...

## Recommendation
- ...

## Risks / Unknowns
- ...
```

## Notes

- Keep quotes short and provide links.
- Escalate to planning (`$plan`) if research changes scope.
