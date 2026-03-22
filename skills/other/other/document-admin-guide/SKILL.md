---
name: document-admin-guide
description: Create user-friendly documentation for admin staff and business users. Use when documenting admin features, creating user guides, or writing non-technical how-to guides for Humberto and parts counter staff.
---

# Admin Guide Documentation Skill

## Purpose

Create documentation for **non-technical users** (Humberto, parts counter staff) who need to use the admin interface without coding knowledge.

## Audience Characteristics

- **No coding experience** - avoid all technical jargon
- **Task-focused** - they want to accomplish something specific
- **Visual learners** - benefit from screenshots and step-by-step guidance
- **Time-constrained** - need quick answers, not deep explanations

## Instructions

When documenting admin features:

1. **Identify the task** the user wants to accomplish
2. **Use plain language** - no technical terms without explanation
3. **Follow the admin-how-to template** in `templates/admin-how-to.md`
4. **Include "What you'll see" sections** for visual guidance
5. **Output to** `/docs/admin-guide/[task-name].md`

## Smart Interaction

### ASK the User When:

- Creating a new admin guide (confirm topic and scope)
- Deleting an admin guide (confirm deletion)
- Major restructure of admin section

### PROCEED Autonomously When:

- Updating existing admin guides
- Adding clarifications or examples
- Fixing typos or improving wording

## Documentation Principles (CRITICAL)

**Before writing ANY documentation**, review `../DOCUMENTATION_PRINCIPLES.md` for:

1. **Ground Truth Only** - Document what exists in code, no speculation
2. **Writing Tone** - Clear and educational without audience labels
3. **Code Examples** - Real files with paths and line numbers
4. **Performance Docs** - Techniques + measurement methods, NOT estimated timings
5. **What NOT to include** - No troubleshooting, future work, or meta-commentary
6. **Diagrams** - Use when they clarify technicals, not for decoration

These principles override any template suggestions that conflict with them.

**Note**: Admin guides target non-technical users, so adapt principles accordingly (e.g., avoid file paths, use plain language).

## Writing Guidelines

### DO:

- Use numbered steps (1, 2, 3...)
- Start steps with action verbs ("Click", "Select", "Enter")
- Include "What you'll see" descriptions
- Keep sentences short (under 20 words)
- Use bullet points for lists
- Define any term that might be unfamiliar

### DON'T:

- Use code blocks (unless showing what to type in a form)
- Reference file paths or technical architecture
- Assume knowledge of developer tools
- Use acronyms without explanation
- Include implementation details
- Add troubleshooting sections (operational knowledge belongs in runbooks, per DOCUMENTATION_PRINCIPLES.md)

## Language Examples

| Instead of...              | Write...                |
| -------------------------- | ----------------------- |
| "Navigate to the endpoint" | "Go to the page"        |
| "Submit the form"          | "Click the Save button" |
| "The API returns..."       | "You'll see..."         |
| "Configure the settings"   | "Change the options"    |
| "Execute the action"       | "Click the button"      |
| "Authenticate"             | "Log in"                |
| "Query the database"       | "Search for"            |

## Template Location

Use the template at: `.claude/skills/document-admin-guide/templates/admin-how-to.md`

## Output Structure

```
docs/admin-guide/
├── index.md              # Overview of admin features
├── getting-started.md    # First-time setup for admins
├── managing-parts.md     # Adding, editing, deleting parts
├── importing-data.md     # Excel import guide
├── managing-images.md    # Part images and 360° views
└── site-settings.md      # Configuring site options
```

**Note**: Troubleshooting content should be documented under `docs/operations/troubleshooting.mdx`.

## Quality Checklist

Before completing:

- [ ] No technical jargon without explanation
- [ ] All steps numbered and start with action verbs
- [ ] "What you'll see" included for complex steps
- [ ] Screenshots described (or placeholder noted)
- [ ] Tested by imagining a non-technical user following along
- [ ] No troubleshooting sections (these belong in runbooks)

## Examples

- "Create a guide for adding new parts" → Creates `/docs/admin-guide/managing-parts.md`
- "Document how to import Excel files" → Creates `/docs/admin-guide/importing-data.md`
- "Write instructions for changing the site logo" → Creates `/docs/admin-guide/site-settings.md`
