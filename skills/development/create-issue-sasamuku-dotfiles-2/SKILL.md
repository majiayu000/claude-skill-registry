---
name: create-issue
description: General guidelines for creating GitHub issues
disable-model-invocation: true
---

# Create Issue

Create a new GitHub issue using GitHub CLI.

## Arguments

$ARGUMENTS

Examples:
- `Add dark mode support` - Create issue with this description
- `Bug: login fails on Safari` - Create bug report
- (empty) - Detect context from conversation and suggest issue

## Process

### 1. Check for Issue Templates

Look for `.github/ISSUE_TEMPLATE` directory.
If templates exist, use the most appropriate one.

### 2. Analyze the Request

Understand context and technical implications:
- Current state vs desired state
- Technical requirements and dependencies
- Potential implementation approaches
- Impact and risks

### 3. Draft the Issue

- **Title**: Clear, descriptive (do NOT use Conventional Commits format)
- **Body**: Structured with:
  - Overview (problem summary)
  - Current state
  - Investigation results
  - Action items
  - Impact analysis
  - Technical considerations

### 4. Get User Approval

```
Issue Draft:

Title: [proposed title]

Body:
[complete issue body]

Do you approve this issue? (y/n)
```

**Wait for user approval before creating.**

### 5. Create the Issue

```bash
gh issue create --title "Title" --body "Body"
```

## Best Practices

- Include specific file paths and line numbers as evidence
- Use markdown formatting
- Keep titles concise but descriptive
