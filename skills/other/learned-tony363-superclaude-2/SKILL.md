---
name: learned-skills-index
description: Index directory for automatically learned skills from execution feedback
type: index
---

# Learned Skills Index

This directory contains skills that have been automatically extracted from successful
execution sessions. These skills represent patterns that led to quality improvements
and are available for retrieval in future tasks.

## How Skills Are Learned

1. **Execution**: Claude Code runs a task with `--loop` enabled
2. **Feedback Collection**: Each iteration's quality scores and improvements are recorded
3. **Pattern Extraction**: Successful patterns are extracted from quality-improving iterations
4. **Skill Generation**: Patterns are compiled into a learnable skill definition
5. **Promotion Gate**: Skills must meet quality thresholds before promotion

## Skill Status

| Status | Meaning |
|--------|---------|
| **Pending** | Skill extracted but not yet promoted (needs more validation) |
| **Promoted** | Skill has been validated and can be applied to new tasks |
| **Archived** | Skill deprecated or superseded by newer learning |

## Quality Thresholds for Promotion

- Minimum quality score: 85.0
- Minimum successful applications: 2
- Minimum success rate: 70%

## Directory Structure

```
learned/
├── SKILL.md                    # This index file
├── learned-backend-auth/       # Example learned skill
│   ├── SKILL.md               # Skill definition
│   └── metadata.json          # Machine-readable metadata
└── learned-frontend-form/      # Another learned skill
    ├── SKILL.md
    └── metadata.json
```

## Integration

Learned skills are automatically retrieved based on:
- Task description keywords
- File types being modified
- Domain context

To manually query learned skills:
```python
from core.skill_persistence import retrieve_skills_for_task

skills = retrieve_skills_for_task(
    task_description="your task here",
    domain="backend"  # optional
)
```

## Safety

All learned skills include full provenance:
- Source session ID
- Source repository
- Timestamp of learning
- Quality progression

This enables rollback and audit of any behavioral changes from learned skills.
