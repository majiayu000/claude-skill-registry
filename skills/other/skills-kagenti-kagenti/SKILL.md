---
name: skills
description: Skill management - create, validate, and improve Claude Code skills
---

```mermaid
flowchart TD
    START([Skills]) --> SCAN["skills:scan"]:::skills
    SCAN -->|New repo| WRITE["skills:write"]:::skills
    SCAN -->|Existing| VALIDATE["skills:validate"]:::skills
    VALIDATE -->|Issues| WRITE
    VALIDATE -->|All pass| REPORT[Generate Report]
    WRITE --> VALIDATE
    REPORT --> RETRO["skills:retrospective"]:::skills
    RETRO -->|Gaps| WRITE

    classDef skills fill:#607D8B,stroke:#333,color:white
```

> Follow this diagram as the workflow.

# Skills Management

Skills for managing the skill system itself.

| Skill | Purpose |
|-------|---------|
| `skills:write` | Create new skills following the standard template |
| `skills:validate` | Validate skill format, naming, and structure |
| `skills:scan` | Scan a repository and generate initial skill set based on technology stack |
| `skills:retrospective` | Review session to identify skill gaps and improvements |

## Related Skills

- `tdd:ci` - TDD workflow that uses skill patterns
- `rca:ci` - RCA workflow that uses skill patterns
- `meta:write-docs` - Documentation writing guidelines
