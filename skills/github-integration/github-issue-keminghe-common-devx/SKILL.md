---
name: github-issue
description: |
  Generate GitHub issues following repository templates.
  Use when creating bug reports, feature requests, or other issues.
  Triggers: "create issue", "bug report", "feature request", "github issue".
license: MIT
metadata:
  author: KemingHe
  version: "3.0.0"
---

# GitHub Issue Generation

Generate GitHub issues that communicate problems, feature requests, and enhancements following repository templates.

**Temporary persona**: Senior engineering manager with expertise in issue tracking and project communication.

## When to Use This Skill

- Creating a bug report for unexpected behavior
- Requesting a new feature or enhancement
- Documenting technical debt or improvements
- Creating issues that follow repository conventions

## Template Resolution

1. Search `.github/ISSUE_TEMPLATE/` for `bug-report.md`, `feature-request.md`, or other templates
2. Check `.github/ISSUE_TEMPLATE/config.yml` for template configuration
3. If not found, search `**/ISSUE_TEMPLATE/**` across repository
4. If still not found, ask user for template or use minimal structure

## Process

### Step 1: Gather Information

- Search for issue templates in repository
- Classify issue type from user input (bug vs feature vs other)
- Use MCP tools for context:
  - Search existing issues, PRs, discussions for related work
  - Search codebase for recent changes, error patterns
  - Identify dependencies or blockers from prior work
- Extract key information: symptoms, desired functionality, technical requirements

### Step 2: Classify and Consult User

Determine issue type and generate title:

| Type | Format | Example |
| :--- | :--- | :--- |
| Bug | `bug(scope): description` | bug(api): fix null pointer in auth |
| Feature | `feat(scope): description` | feat(ui): add dark mode toggle |

Present template selection and ask:

- Bug: Reproduction steps, expected/actual behavior, environment?
- Feature: Problem statement, proposed solution, alternatives?
- All: Related issues/PRs, priority level?

### Step 3: Generate Issue

- Use template as minimum structure, enrich with critical details
- Include conventional title format
- Populate Related section with discovered issues/PRs (omit if none)
- Add context that helps maintainers: error logs, affected files, user impact
- Use dash bullets, each with specific actionable details
- Apply KISS and DRY: no fluff, but capture all information needed to act

**Enrichment guidance**:

- Bug: Include actual error messages, stack traces, affected code paths
- Feature: Clarify scope boundaries, success criteria, edge cases
- Both: Link related issues/PRs, note blocking dependencies

## Output Format

Present final issue in markdown code block:

```markdown
bug(component): brief description
OR
feat(component): brief description

[complete issue content following template structure]
```

## Constraints

- **Title**: Max 50 characters, imperative mood, `bug(scope):` or `feat(scope):` format
- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Completeness**: Capture all technical details, error messages, requirements
- **KISS and DRY**: Each section conveys unique, specific information - no fluff
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode

---

> GitHub Issue Generation Skill v3.0.0 - KemingHe/common-devx
