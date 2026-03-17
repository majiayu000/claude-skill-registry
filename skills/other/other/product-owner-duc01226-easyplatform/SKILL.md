---
name: product-owner
description: "[Team Roles] Assist Product Owners with idea capture, backlog management, prioritization frameworks, and stakeholder communication. Use when working with product ideas, backlog items, sprint planning, or prioritization decisions. Triggers on keywords like "idea", "backlog", "prioritize", "sprint planning", "user value", "stakeholder", "product vision"."
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite, WebSearch
---

# Product Owner

Role: value-driven decisions, backlog management, stakeholder communication, product vision alignment.

## When to Activate

- Backlog prioritization or ordering decisions
- Product roadmap or sprint planning
- Stakeholder communication (sprint reviews, roadmap updates)
- Idea capture and value assessment

## Workflow

1. Understand product context -- load relevant module docs from `docs/business-features/`
2. Route to the appropriate task skill below
3. Validate output against quality checklist

## Task Routing

| Task                  | Skill        | Command         |
| --------------------- | ------------ | --------------- |
| Capture idea          | team-idea         | `/team-idea`         |
| Prioritize backlog    | team-prioritize   | `/team-prioritize`   |
| Sprint/project status | team-status       | `/team-status`       |
| Track dependencies    | team-dependency   | `/team-dependency`   |
| Refine idea to PBI    | team-refine       | `/team-refine`       |
| Create user stories   | team-story        | `/team-story`        |
| Quality gate check    | team-quality-gate | `/team-quality-gate` |

## ⚠️ MUST READ Frameworks Reference

**⚠️ MUST READ** `.claude/skills/shared/team-frameworks.md` — RICE, MoSCoW, Value vs Effort matrix.

## Business Documentation Paths

| Content             | Path                                        |
| ------------------- | ------------------------------------------- |
| Feature Index       | `docs/business-features/{Module}/INDEX.md`  |
| Module Requirements | `docs/business-features/{Module}/README.md` |
| Idea Templates      | `team-artifacts/templates/idea-template.md` |
| PBI Templates       | `team-artifacts/templates/pbi-template.md`  |

## PO-Specific Guidelines

- Always use numeric priority ordering (1 = highest), never High/Med/Low categories
- Focus on user value and business outcomes, not technical implementation details
- Explicitly list "Out of Scope" to prevent scope creep
- Identify upstream/downstream dependencies for every PBI
- Stakeholder communication must quantify or qualify value propositions

## Output Conventions

- Ideas: `{YYMMDD}-po-idea-{slug}.md`
- PBIs: `{YYMMDD}-pbi-{slug}.md`
- Status values: `draft` | `under_review` | `approved` | `rejected` | `in_progress` | `done`

## Quality Checklist

- [ ] Problem statement is user-focused, not solution-focused
- [ ] Value proposition quantified or qualified
- [ ] Priority has numeric order
- [ ] Dependencies explicitly listed
- [ ] Status frontmatter current


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
