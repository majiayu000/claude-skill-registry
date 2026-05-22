---
name: technical-writing
description: Creates high-quality technical documentation including API documentation, user guides, tutorials, architecture documents, README files, release notes, and technical specifications. Produces clear, structured, and comprehensive documentation following industry best practices. Use when writing technical documentation, creating API docs, developing user guides, documenting architecture, writing tutorials, preparing release notes, or when users mention "technical writing", "documentation", "API docs", "user guide", "tutorial", "README", "technical specification", "architecture document", or "developer documentation".
---

# Technical Writing

Creates professional technical documentation with clear structure, appropriate detail level, and user-focused content.

## Workflow

## 1. Identify Documentation Type

Determine which type of documentation is needed:

- **API Documentation** - REST, GraphQL, webhooks, authentication
- **User Guides** - Features, how-tos, troubleshooting
- **Tutorials** - Learning-focused with hands-on examples
- **Architecture Documents** - System design, technical decisions
- **README Files** - Project overview, quick start
- **Release Notes** - Changes, migrations, breaking changes
- **Technical Specifications** - Requirements, constraints

**For detailed templates and patterns:** Load [documentation-types-and-workflows.md](references/documentation-types-and-workflows.md)

### 2. Gather Context

Collect essential information before writing:

- **Audience** - Developers, end-users, managers, administrators
- **Technical depth** - Beginner, intermediate, advanced
- **Scope** - Codebase/APIs/systems to document
- **Standards** - Style guides or organizational requirements
- **Related docs** - Existing documentation to reference or integrate with

### 3. Structure Content

Apply clear organization principles:

- Lead with overview/introduction
- Use descriptive heading hierarchy (H1 → H2 → H3)
- Include table of contents for documents with >3 sections
- Group related information logically
- Place examples immediately after concepts
- Add diagrams/visuals for complex workflows

### 4. Write Clear Content

Follow core writing principles:

- **Active voice** - "The API returns..." not "The response is returned..."
- **Specificity** - "Response time < 200ms" not "Fast response"
- **Define acronyms** - "API (Application Programming Interface)" on first use
- **Consistent terminology** - Same terms throughout document
- **Imperative instructions** - "Run the command" not "You should run..."
- **Show examples** - Provide code/output for every concept

**For comprehensive style guidance:** Load [writing-guidelines.md](references/writing-guidelines.md)

### 5. Add Code Examples

Code example requirements:

- Specify language in code blocks: ```python,```javascript
- Show complete, runnable examples (not fragments)
- Include input/output pairs
- Add explanatory comments for complex logic
- Test all code before publishing

### 6. Review and Validate

Quality assurance checklist:

- ✓ Verify technical accuracy
- ✓ Test all code examples
- ✓ Check clarity and completeness
- ✓ Ensure consistent terminology
- ✓ Validate all links and references

## Documentation Templates

### README Files

Essential components for project documentation:

```markdown
# Project Name
Brief description of what the project does

## Features
- Key feature 1
- Key feature 2
- Key feature 3

## Installation
[step-by-step installation commands]

## Quick Start
[minimal working example]

## Configuration
[environment variables or config options]

## License
[license type]
```

### Release Notes

Structure for version releases:

```markdown
# Version X.X.X - YYYY-MM-DD

## Summary
[High-level overview of this release]

## New Features
- Feature description (#issue-number)
- Feature description (#issue-number)

## Bug Fixes
- Fix description (#issue-number)
- Fix description (#issue-number)

## Breaking Changes
⚠️ **Change that breaks compatibility**
Migration guide: [step-by-step migration instructions]

## Deprecations
- Deprecated feature (will be removed in vX.X)
```

## Quality Standards

Documentation quality checklist before publishing:

- [ ] **Accuracy** - All technical details are correct
- [ ] **Completeness** - All necessary topics covered
- [ ] **Clarity** - Target audience can understand content
- [ ] **Examples** - Working code included and tested
- [ ] **Structure** - Logical organization with clear headings
- [ ] **Consistency** - Terminology and formatting consistent
- [ ] **Links** - All hyperlinks are valid
- [ ] **Grammar** - No spelling or grammatical errors
- [ ] **Current** - Version numbers and dates up-to-date

## Common Pitfalls to Avoid

1. **Assuming knowledge** - Define all acronyms and technical terms
2. **Vague instructions** - Be specific with concrete examples
3. **Missing error scenarios** - Document errors and solutions
4. **Outdated examples** - Test and update code regularly
5. **Inconsistent terminology** - Use identical terms throughout
6. **Missing prerequisites** - List all requirements upfront
7. **Poor formatting** - Use headings, lists, code blocks properly
8. **No examples** - Always include working code samples
9. **Wrong audience level** - Match technical depth to readers
10. **Dense text** - Break into scannable sections with clear headings

## Reference Files

- **[documentation-types-and-workflows.md](references/documentation-types-and-workflows.md)** - Complete templates and patterns for API docs, user guides, tutorials, architecture docs, and technical specifications
- **[writing-guidelines.md](references/writing-guidelines.md)** - Detailed style rules for clarity, active voice, specificity, consistency, heading hierarchy, code formatting, and lists
