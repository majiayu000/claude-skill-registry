---
name: "Claude Code Skill Definition"
description: "A SKILL.md file that defines a Claude Code skill with metadata, instructions, and examples"
path_patterns:
  - ".claude/skills/*/SKILL.md"
  - ".claude/skills/**/SKILL.md"
target_audience: "Claude Code agents auto-selecting skills based on user intent"
frequency: "Created once per skill, updated as requirements evolve"
quality_criteria:
  - name: Kebab-Case Name
    description: "Skill name must be lowercase with hyphens only (e.g., `github-pr-review`, `unit-test-generator`). No underscores, spaces, or reserved words like `anthropic`, `claude`, or `general`."
  - name: Third-Person Description
    description: "Description must be written in third person (e.g., 'Generates...' not 'I generate...'). Under 300 characters. Must clearly state WHAT the skill does and WHEN to use it."
  - name: Discoverable Keywords
    description: "Description must include specific technical terms a user might say (e.g., 'PostgreSQL', 'React components', 'AWS Lambda') to enable reliable auto-selection."
  - name: Progressive Disclosure
    description: "Main SKILL.md file must be under 500 lines. Large reference docs or schemas must be split into separate support files loaded on demand."
  - name: Input Handling
    description: "Must clearly define required inputs before execution begins. Instructions must tell Claude to ask the user for missing inputs rather than guessing."
  - name: Output Format
    description: "Must explicitly state how output should be formatted (e.g., 'Output as a JSON block' or 'Create a markdown file at path X')."
  - name: Worked Example
    description: "Must include at least one Input -> Output example showing the ideal result. Few-shot examples significantly reduce hallucinations."
  - name: Guardrails Section
    description: "Must include a section listing what Claude should NOT do (e.g., 'Do not delete existing comments', 'Do not mock database connections')."
  - name: Concrete File References
    description: "Instructions must use specific file paths, not vague descriptions (e.g., 'Read src/config.json' not 'Read the config file')."
  - name: Plan Before Action
    description: "For complex tasks, instructions must include an analysis/planning step before implementation begins."
---

# Claude Code Skill Definition: [skill-name]

A `SKILL.md` file defines a skill that Claude Code can auto-select based on user intent. Unlike slash commands (invoked explicitly via `/command`), skills are discovered and triggered automatically when Claude determines they match the user's request.

## File Structure

```
.claude/
└── skills/
    ├── database-migration/       # Skill directory (kebab-case)
    │   ├── SKILL.md              # Entry point (required)
    │   └── schema-reference.txt  # Support file (loaded on demand)
    └── code-reviewer/
        └── SKILL.md
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: database-migration
description: "Generates database migration files for schema changes. Use when adding, modifying, or removing database tables or columns."
---
```

### Body (Instructions)

The markdown body instructs Claude how to execute the skill once selected.

## Example: Complete Skill Definition

```markdown
---
name: github-pr-review
description: "Reviews GitHub pull requests for code quality, security issues, and adherence to project conventions. Use when the user mentions reviewing a PR, code review, or asks about changes in a pull request."
---

# github-pr-review

Reviews GitHub pull requests and provides structured feedback.

## Required Inputs

Before proceeding, ensure you have:
1. PR number or URL (ask user if not provided)
2. Review focus areas (optional: security, performance, style)

## Execution Steps

### Step 1: Analyze PR Context

Fetch the PR details and understand:
- Files changed and their purposes
- Base branch and target branch
- Related issues or requirements

### Step 2: Review Code Changes

For each changed file:
1. Check for security vulnerabilities
2. Verify error handling
3. Assess test coverage
4. Review naming conventions
5. Identify performance concerns

### Step 3: Generate Review

Create a structured review with:
- Summary of changes
- Critical issues (must fix)
- Suggestions (nice to have)
- Questions for the author

## Example

**Input:** "Review PR #42"

**Output:**

## PR #42 Review: Add user authentication

### Summary
This PR adds JWT-based authentication to the API endpoints.

### Critical Issues
1. **Line 45 in auth.js**: Token expiration not validated before use
2. **Line 89 in middleware.js**: Missing rate limiting on login endpoint

### Suggestions
- Consider adding refresh token rotation
- Add integration tests for the auth flow

### Questions
- Should failed login attempts trigger account lockout?

## Guardrails

- Do NOT approve or merge PRs automatically
- Do NOT modify code in the PR
- Do NOT dismiss existing reviews
- Do NOT share sensitive information found in code
```

## Naming Conventions

| Bad Name | Good Name | Why? |
|----------|-----------|------|
| `github` | `github-pr-review` | "github" is too broad; be specific about the action |
| `process_data` | `csv-data-processor` | Use hyphens, not underscores; specify the data type |
| `my-tool` | `unit-test-generator` | Generic names are not discoverable; describe the output |
| `claude-helper` | `api-error-analyzer` | Avoid reserved words; focus on functionality |

## Description Best Practices

### Good Description
> "Generates database migration files from schema changes. Use when the user needs to add columns, create tables, or modify database structure."

### Poor Description
> "You can use this to help with database stuff."

### What Makes a Good Description

1. **Third person voice**: "Generates..." not "I generate..."
2. **Specific action**: "migration files" not "database stuff"
3. **Clear trigger**: "Use when..." clause
4. **Technical keywords**: Terms users actually say

## Subagent Delegation

For tasks requiring extensive file reading or research, delegate to a subagent to preserve context:

```markdown
## Step 2: Analyze Codebase

Create a subagent to:
1. Scan the `src/` directory for circular dependencies
2. Identify unused exports
3. Return only a summary, not full file contents

This prevents the main context from being polluted with irrelevant code.
```

## Testing Checklist

Before publishing, verify:

- [ ] **Discovery Test**: Clear history, ask a vague related question. Does the skill trigger?
- [ ] **Argument Test**: Omit a required input. Does Claude ask for it?
- [ ] **Negative Test**: Ask something outside scope. Does the skill stay silent?
- [ ] **Edge Case Test**: Empty inputs, large inputs, malformed data handled?
