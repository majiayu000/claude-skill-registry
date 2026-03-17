---
name: update-design
description: Explicitly update DESIGN.md with decisions from the current conversation. Use when you want to force a design document update.
disable-model-invocation: true
---

# Update Design Document

Record/update project design and implementation decisions in `.claude/docs/DESIGN.md` based on conversation content.

> **Note**: This skill explicitly invokes the same workflow as the `design-tracker` skill.
> Use this when you want to force a design document update.

## Workflow

1. Read existing `.claude/docs/DESIGN.md`
2. Extract decisions/information from the conversation
3. Update the appropriate section
4. Add entry to Changelog with today's date

## Section Mapping

| Topic | Section |
|-------|---------|
| Goals, purpose | Overview |
| Structure, components | Architecture |
| Design patterns | Implementation Plan > Patterns |
| Library choices | Implementation Plan > Libraries |
| Decision rationale | Implementation Plan > Key Decisions |
| Future work | TODO |
| Unresolved issues | Open Questions |

## Update Format

When updating, add to the appropriate section:

```markdown
### Key Decisions

#### {Decision Title} ({Date})

**Context**: {Why this decision was needed}
**Decision**: {What was decided}
**Rationale**: {Why this option was chosen}
```

## Changelog Entry

Always add to Changelog:

```markdown
## Changelog

### {Date}
- {Brief description of what was recorded}
```

## Language

- Document content: English (technical), Japanese OK for descriptions
- User communication: Japanese

If $ARGUMENTS provided, focus on recording that content.
