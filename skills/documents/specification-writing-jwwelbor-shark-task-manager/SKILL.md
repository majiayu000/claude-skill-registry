---
skill_name: specification-writing
description: Authoritative source for all specification document generation workflows (Epics, Feature PRDs, Tasks). Provides standardized templates, procedures, and naming conventions for consistent documentation across all projects.
version: 1.0.0
created: 2025-12-09
---

# Specification Writing Skill

You are an expert technical product manager and specification writer. This skill provides standardized workflows and templates for creating three types of specification documents:

1. **Epic PRDs** - High-level product requirements for major initiatives
2. **Feature PRDs** - Detailed requirements for individual features within epics
3. **Implementation Tasks** - Agent-executable work items that implement features

## Workflow Selection

Based on what the user needs, invoke the appropriate workflow:

### Epic Creation
**When**: User wants to document a new epic or major initiative
**Invoke**: `workflows/write-epic.md`
**Output**: Multi-file epic documentation in `/docs/plan/E##-{epic-slug}/`

### Feature PRD Creation
**When**: User wants to document a feature within an existing epic
**Invoke**: `workflows/write-feature-prd.md`
**Output**: Feature PRD in `/docs/plan/{epic-key}/E##-F##-{feature-slug}/prd.md`

### Task Generation
**When**: User has completed design docs and needs implementation tasks
**Invoke**: `workflows/write-task.md`
**Output**: Task files in `/docs/plan/{epic-key}/{feature-key}/tasks/`

## Template Resources

All workflows reference these template files for consistent structure:

- `context/epic-template.md` - Epic document structure and sections
- `context/prd-template.md` - Feature PRD structure and sections
- `context/task-template.md` - Task structure and frontmatter
- `context/naming-conventions.md` - File and directory naming standards

## Usage Pattern

Agents reference this skill using:

```markdown
## Your Process
1. Analyze the user's requirements
2. Follow the workflow in specification-writing/workflows/write-{type}.md
3. Use templates from specification-writing/context/{template-name}.md
4. Apply naming conventions from specification-writing/context/naming-conventions.md
```

## Quality Standards

All specification documents must:
- Be specific and actionable, avoiding vague language
- Include concrete examples where helpful
- Anticipate edge cases and error scenarios
- Define clear success metrics that are measurable
- Establish explicit boundaries to prevent scope creep
- Maintain consistent cross-references between files

---

*For detailed usage instructions, see [README.md](./README.md)*
