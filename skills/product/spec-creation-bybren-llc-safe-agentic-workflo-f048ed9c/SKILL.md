---
name: spec-creation
description: Spec creation with pattern references, acceptance criteria, and demo scripts. Use when creating implementation specs, defining acceptance criteria, or breaking down user stories.
---

# Spec Creation Skill

## Purpose

Guide spec creation with clear acceptance criteria, pattern references, and testable success validation.

## When This Skill Applies

- Creating implementation specs
- Breaking down user stories
- Defining acceptance criteria
- Translating business requirements to technical specs

## Spec Template (MANDATORY)

```markdown
# SPEC-{TICKET_PREFIX}-{number}: {Feature Name}

## Summary
{One paragraph describing the feature}

## User Story
As a [user type], I want [goal] so that [benefit].

## Acceptance Criteria
- [ ] {Testable criterion 1}
- [ ] {Testable criterion 2}
- [ ] {Testable criterion 3}

## Pattern References
- **UI**: `docs/patterns/ui/{pattern}.md`
- **API**: `docs/patterns/api/{pattern}.md`
- **Database**: `docs/patterns/database/{pattern}.md`

## Success Validation Command
```bash
{validation command}
```

## Demo Script
1. Navigate to {page}
2. Click {button}
3. Observe {expected behavior}

## Logical Commits
1. `feat(scope): implement data model [{TICKET_PREFIX}-{number}]`
2. `feat(scope): add API endpoint [{TICKET_PREFIX}-{number}]`
3. `feat(scope): create UI component [{TICKET_PREFIX}-{number}]`
```

## Acceptance Criteria Patterns

```markdown
# User Actions
- [ ] User can {action} → {result}

# Data
- [ ] Data persists after {action}
- [ ] User can only see their own {data type}

# Errors
- [ ] Invalid input shows {error message}
```

## Quality Checklist

- [ ] All acceptance criteria are testable
- [ ] Pattern references point to existing patterns
- [ ] Success validation command is runnable
- [ ] Linear ticket referenced

## Reference

- **Spec Template**: `docs/archive/specs/spec_template.md`
- **Pattern Library**: `docs/patterns/README.md`
