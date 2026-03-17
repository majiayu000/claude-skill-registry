---
name: creating-github-issues
description: Use when creating GitHub issues, making new issues, filing bugs, requesting features, or before running `gh issue create`. Triggers on "new issue", "create issue", "file issue", "gh issue", "open issue". Ensures proper research, labels, and comprehensive issue documentation.
---

# Creating GitHub Issues

## Overview

Every GitHub issue should be well-researched and clearly documented. This skill ensures issues contain enough context for anyone to understand and implement them.

## Mandatory Workflow

### Step 1: Research the Codebase

Before writing the issue, use the Explore agent or search tools to understand:

- Where relevant code lives (file paths, functions, components)
- How similar functionality is currently implemented
- Database tables, API endpoints, or UI components involved
- Existing patterns that should be followed

**Include in the issue:**
- Specific file paths and line numbers
- Code snippets showing current implementation
- References to similar existing code as examples

**Why:** Issues with research reduce back-and-forth questions and give implementers a head start.

### Step 2: Create the Issue

Use `gh issue create` with a well-structured body:

```bash
gh issue create --title "Brief descriptive title" --body "$(cat <<'EOF'
## Summary
<1-3 sentences describing what needs to be done>

## Current State
<What exists now, with file paths and code references>

## Proposed Changes
<What should change, with specific details>

## Technical Notes
<File paths, database tables, API endpoints, code snippets>

## Acceptance Criteria
- [ ] Specific testable requirement
- [ ] Another requirement
EOF
)"
```

### Step 3: Add Labels

Discover current labels and apply appropriate ones:

```bash
gh label list --limit 50
```

**Common label categories:**

1. **Type** (pick one):
   - `enhancement` - New feature or improvement
   - `bug` - Something isn't working
   - `documentation` - Documentation improvements
   - `question` - Further information requested

2. **Priority** (if applicable):
   - `priority: critical` - Production broken, blocking issue
   - `priority: high` - Important bug fix, urgent feature
   - `priority: low` - Nice to have, can wait

3. **Area** (if applicable):
   - Labels indicating which part of the codebase is affected

```bash
gh issue edit <number> --add-label "enhancement"
```

### Step 4: Add to Project (if applicable)

If the repository uses GitHub Projects:

```bash
gh issue edit <number> --add-project "Project Name"
```

## Issue Template

```markdown
## Summary
<1-3 sentences describing what needs to be done>

## Current State
<What exists now>
- File: `path/to/file.ts:123`
- Current behavior: <description>

## Proposed Changes
<What should change>
1. Change X to do Y
2. Add Z functionality

## Technical Notes
- Relevant files: `src/components/Feature.tsx`, `src/utils/helpers.ts`
- Related functions: `handleSubmit()`, `validateInput()`
- Consider: <architectural notes, edge cases>

## Acceptance Criteria
- [ ] Specific testable requirement
- [ ] Another requirement
- [ ] Tests pass

## Additional Context
<Screenshots, error messages, related issues>
```

## Field Selection Guidelines

### Priority
- **Critical** - Production broken, blocking issue
- **High** - Important bug fix, urgent feature (most bugs default here)
- **Medium** - Standard feature work
- **Low** - Nice to have, can wait

**Default guidance:** Bugs default to High unless trivial. Enhancements default to Medium unless urgent.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Create issue without researching code first | Use Explore agent to find relevant files |
| Generic issue description | Include specific file paths, line numbers, code snippets |
| Missing acceptance criteria | Always include testable requirements |
| No labels | Always add at least a type label |
| Vague title | Make titles specific and searchable |
