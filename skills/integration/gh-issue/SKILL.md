---
name: gh-issue
description: Create a GitHub issue following project guidelines
argument-hint: <title or description>
allowed-tools: Read, Grep, Glob, mcp__github__create_issue, mcp__github__list_issues, mcp__github__search_issues
---

# Create GitHub Issue

Create a new GitHub issue for the gittower/git-flow-next repository following project guidelines.

## Instructions

1. **Gather Information**
   - If `$ARGUMENTS` is provided, use it as the issue title/description
   - If no arguments, ask the user for:
     - Issue type (bug, enhancement, feature)
     - Brief description of the issue

2. **Check for Duplicates**
   - Search existing issues for similar topics
   - If potential duplicates found, show them to the user and ask to confirm creation

3. **Determine Issue Type and Labels**
   - `bug` - Something isn't working
   - `enhancement` - Improvement to existing feature
   - `feature` - New feature request
   - `documentation` - Documentation improvements

4. **Create the Issue**
   - Use clear, descriptive title (imperative mood: "Add...", "Fix...", "Update...")
   - Structure the body with appropriate sections based on type

## Issue Body Templates

### Bug Report
```markdown
## Description
<Clear description of the bug>

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<What should happen>

## Actual Behavior
<What actually happens>

## Environment
- OS:
- Git version:
- git-flow-next version:
```

### Enhancement/Feature
```markdown
## Description
<Clear description of the enhancement/feature>

## Motivation
<Why is this needed? What problem does it solve?>

## Proposed Solution
<How should this work?>

## Alternatives Considered
<Other approaches considered, if any>
```

5. **Report Result**
   - Show the created issue URL
   - Suggest next step: `/analyze-issue <number>` to start working on it
