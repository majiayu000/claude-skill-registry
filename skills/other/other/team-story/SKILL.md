---
name: team-story
version: 1.2.0
description: "[Team] Break PBIs into user stories using vertical slicing, SPIDR splitting, and INVEST criteria. Use when creating user stories from PBIs, slicing features, or breaking down requirements. Triggers on keywords like "user story", "create stories", "slice pbi", "story breakdown", "vertical slice", "split story"."
argument-hint: "<path-to-pbi-file-or-PBI-ID>"
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite
infer: true
---

# User Story Creation

Break Product Backlog Items into implementable user stories using vertical slicing and SPIDR patterns.

## MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **MUST READ** `.claude/skills/shared/team-frameworks.md` — INVEST, SPIDR, MoSCoW frameworks
- **MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin scenario templates
- **MUST READ** `.claude/skills/shared/module-detection-keywords.md` — module detection keywords
- **MUST READ** `references/story-patterns.md` — scenarios, templates, anti-patterns

## Pre-Workflow

- Activate `business-analyst` skill for domain context and requirements analysis

## When to Use

- PBI ready for story breakdown
- Feature needs vertical slicing
- Creating sprint-ready work items
- Story too large (effort >8)

## Workflow

1. Read PBI artifact and acceptance criteria
2. **Load domain context** if module detected (see `references/story-patterns.md`)
3. Identify vertical slices (end-to-end functionality)
4. **Apply SPIDR splitting** if stories too large (see shared frameworks)
5. Apply INVEST criteria to each story (see shared frameworks)
6. Create user stories with GIVEN/WHEN/THEN (min 3 scenarios)
7. Save to `team-artifacts/pbis/stories/`
8. **Validate stories** (MANDATORY) - Interview user
9. Suggest next: `/team-test-spec` or `/team-design-spec`

## Output

- **Path:** `team-artifacts/pbis/stories/{YYMMDD}-us-{pbi-slug}.md`
- **Format:** Single file with all stories (use ## headers per story)

## Story Format

```markdown
## Story N: {Title}

**As a** {user role}
**I want** {goal}
**So that** {benefit}

### Acceptance Criteria (min 3 scenarios: happy, edge, error)

```gherkin
Scenario: {Title}
  Given {context}
  When {action}
  Then {outcome}
```
```

## Quality Checklist

- [ ] Each story follows "As a... I want... So that..." format
- [ ] SPIDR splitting applied (effort <= 8, prefer <= 5)
- [ ] At least 3 scenarios per story: happy, edge, error
- [ ] All scenarios use GIVEN/WHEN/THEN format
- [ ] Effort estimated in Fibonacci (1, 2, 3, 5, 8)
- [ ] Stories independent (can develop in any order)
- [ ] Out of scope explicitly listed
- [ ] Dependencies identified (upstream/downstream)
- [ ] Domain vocabulary used correctly (if applicable)
- [ ] Validation interview completed (MANDATORY)

## Related

| Type           | Reference                                                    |
| -------------- | ------------------------------------------------------------ |
| **Role Skill** | `business-analyst`                                           |
| **Input**      | `/team-refine` output (PBI)                                  |
| **Next Steps** | `/team-test-spec`, `/team-design-spec`, `/team-prioritize`   |

## Triggers

Activates on: story, user story, user stories, slice, slicing, split story, breakdown


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
