---
name: templates-mike-coulbourn-claude-vibes
description: Use this template for simple Skills that don't need scripts, utilities,
  or extensive documentation.
---

# Basic Skill Template

Use this template for simple Skills that don't need scripts, utilities, or extensive documentation.

## When to use this template

- Instructions and examples fit in one file
- No scripts or utilities needed
- Straightforward workflow
- Limited documentation requirements

---

## Template

```yaml
---
name: your-skill-name
description: [What it does] + [When to use it] + [Trigger terms users would say]. Max 1024 characters.
---

# Your Skill Name

Brief one-sentence description of what this Skill provides.

## Quick Start

Show the most common use case immediately:

```language
# Quick example that demonstrates the primary operation
```

## Instructions

Provide clear, step-by-step guidance for Claude:

1. [First specific action to take]
2. [Second specific action to take]
3. [Expected outcome or verification step]

## Examples

### Example 1: [Common scenario name]

```language
# Code example for common scenario
```

### Example 2: [Another scenario name]

```language
# Code example for another scenario
```

## Best Practices

- Key principle or guideline
- Important consideration
- Common pitfall to avoid

## Requirements

If dependencies are needed:

```bash
# Installation commands
pip install package-name
npm install package-name
```

List any prerequisites:
- Prerequisite 1
- Prerequisite 2
```

---

## Real Example: Git Commit Helper

Here's a complete working example:

```yaml
---
name: commit-helper
description: Generate conventional commit messages from git diffs. Use when writing commits, reviewing staged changes, or when the user asks for commit message help.
---

# Git Commit Helper

Generates clear, conventional commit messages following best practices.

## Quick Start

```bash
# Stage your changes first
git add .

# I'll review the diff and suggest a commit message
git diff --staged
```

## Instructions

When the user needs a commit message:

1. Run `git diff --staged` to see what changed
2. Generate a commit message with:
   - Type prefix (feat, fix, docs, refactor, test, chore)
   - Summary line under 50 characters
   - Detailed body explaining what and why
3. Suggest 2-3 variations if the change could be described different ways

## Examples

### Example 1: New Feature

```
feat: add user authentication

Implement JWT-based authentication to secure API endpoints.
Adds login/logout routes and token validation middleware.
```

### Example 2: Bug Fix

```
fix: prevent duplicate form submissions

Add debouncing to submit button to prevent race conditions
when users double-click. Includes 500ms cooldown period.
```

### Example 3: Refactoring

```
refactor: extract validation logic to shared utilities

Move repeated validation code from 5 route handlers into
reusable validation functions. No behavior changes.
```

## Best Practices

- Use present tense ("add" not "added")
- Be specific about what changed
- Explain why if it's not obvious from what
- Keep summary line under 50 characters
- Include scope if working in monorepo (feat(api): add endpoint)

## Requirements

- Git repository with staged changes
- Understanding of conventional commit format
```

---

## Tips for Using This Template

1. **Replace all bracketed placeholders** with actual content
2. **Delete sections you don't need** - not every Skill needs all sections
3. **Add sections if needed** - templates are starting points, not constraints
4. **Keep it focused** - one Skill = one capability
5. **Test your examples** - verify all code examples actually work
6. **Be specific in descriptions** - use exact trigger terms users would say
