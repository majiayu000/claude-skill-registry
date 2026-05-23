---
name: prd-builder
description: PRD templates and structure for product requirements documents. 
---

# PRD Builder Skill

Provides templates for creating comprehensive Product Requirements Documents. Keep asking questions to clarify doubts and get >= 95% understanding of what the user wants.

## When to Use

Automatically invoked by `/majestic:prd` command. Provides:

- Standard PRD template structure
- Technical expansion sections
- Backlog item format

## Templates

- [resources/prd-template.md](resources/prd-template.md) - Core PRD structure (10 sections)
- [resources/technical-expansion.md](resources/technical-expansion.md) - API, Data Model, Security, Performance sections

## Best Practices

- **Clear, actionable language** - Specific requirements, not vague descriptions
- **User story IDs** - Traceable requirements (US-001, FR-001)
- **Testable acceptance criteria** - Measurable success conditions
- **Explicit scope boundaries** - Non-goals prevent scope creep
- **Developer-ready** - Empowers "how" decisions while defining "what"
