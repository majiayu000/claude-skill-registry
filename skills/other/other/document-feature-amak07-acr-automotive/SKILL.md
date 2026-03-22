---
name: document-feature
description: Generate standardized feature documentation using Good Docs templates. Use when documenting a feature, creating feature docs, or writing technical documentation for a specific capability.
---

# Feature Documentation Skill

## Diátaxis Framework

This skill supports three documentation types. **When creating a NEW document**, ask the user which type they need:

| Type          | Template                 | Purpose                               | Audience   |
| ------------- | ------------------------ | ------------------------------------- | ---------- |
| **Tutorial**  | `templates/tutorial.md`  | Learning-focused, step-by-step guide  | Beginners  |
| **How-To**    | `templates/how-to.md`    | Task-focused, solve specific problems | Developers |
| **Reference** | `templates/reference.md` | Technical specs, API docs             | Developers |

> **Note**: For admin/non-technical users, use the `document-admin-guide` skill instead.

## Smart Interaction

### ASK the User When:

- **Creating new doc**: Confirm doc type (Tutorial/How-To/Reference), audience, and output location
- **Deleting a doc**: Always confirm before deletion
- **Major restructure**: Moving multiple docs or changing navigation
- **Ambiguous request**: Can't determine intent from context

### PROCEED Autonomously When:

- **Updating existing doc**: Use best judgment, preserve existing structure
- **Adding content**: Follow existing template/format
- **Fixing errors/typos**: Non-destructive improvements
- **Adding diagrams**: Enhancement to existing doc
- **Updating code examples**: Keep docs in sync with codebase

## Documentation Principles (CRITICAL)

**Before writing ANY documentation**, review `../DOCUMENTATION_PRINCIPLES.md` for:

1. **Ground Truth Only** - Document what exists in code, no speculation
2. **Writing Tone** - Clear and educational without audience labels
3. **Code Examples** - Real files with paths and line numbers
4. **Performance Docs** - Techniques + measurement methods, NOT estimated timings
5. **What NOT to include** - No troubleshooting, future work, or meta-commentary
6. **Diagrams** - Use when they clarify technicals, not for decoration

These principles override any template suggestions that conflict with them.

## Instructions

When documenting a feature:

1. **Determine doc type** - Ask user if creating new doc; infer from existing if updating
2. **Explore the codebase** to find all related files for this feature
3. **Use the appropriate template** from `templates/` folder
4. **Generate Mermaid diagrams** for architecture (when they clarify complex concepts)
5. **Include real code examples** from the codebase (not hypothetical)
6. **Check for existing ADRs** in `/docs/architecture/decisions/` related to this feature
7. **Output to** appropriate location based on doc type

## Output Locations

| Doc Type  | Output Path                               |
| --------- | ----------------------------------------- |
| Tutorial  | `/docs/getting-started/[feature-name].md` |
| How-To    | `/docs/developer-guide/[task-name].md`    |
| Reference | `/docs/architecture/[component-name].md`  |

## Templates

All templates are located in `.claude/skills/document-feature/templates/`:

- **tutorial.md** - For learning-focused beginner guides
- **how-to.md** - For task-focused developer guides
- **reference.md** - For API/component technical reference

## Diagram Standards

- Use Mermaid for all diagrams
- C4-style naming: System, Container, Component
- Sequence diagrams for data flows
- Include legends for complex diagrams

## Quality Checklist

Before completing:

- [ ] Correct template used for doc type
- [ ] At least one architecture diagram (if applicable)
- [ ] Real code examples from codebase
- [ ] File paths verified to exist
- [ ] Links to related docs included
- [ ] Prerequisites section included (for tutorials/how-tos)

## Examples

### Creating New Docs (Will Ask User)

- "Document the search feature" → Ask: Tutorial, How-To, or Reference?
- "Create docs for Excel import" → Ask: What type and audience?

### Updating Existing Docs (Autonomous)

- "Update the search docs with new API endpoint" → Updates existing doc
- "Add error handling examples to API reference" → Adds to existing doc
- "Fix outdated code example in tutorial" → Fixes without asking

### Routing by Request Type

- "Help new devs understand search" → Tutorial
- "How to implement search filtering" → How-To
- "Document the search API" → Reference
