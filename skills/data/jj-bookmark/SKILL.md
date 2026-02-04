---
name: jj:bookmark
description: "Create a jj bookmark for the current commit with a descriptive name"
---

# Create Bookmark

Create a jj bookmark for the current commit with a descriptive name.

## Process

1. Run `jj log -r ::@ --limit 10` to see recent commits and understand the work theme
2. Generate a short, descriptive name (2-4 words, kebab-case, no slashes)
3. Create the bookmark:
   - If `@` is empty: `jj bookmark create john/<name> -r @-`
   - If `@` has changes: `jj bookmark create john/<name>`

## Naming Examples

| Work Description | Bookmark Name |
|-----------------|---------------|
| Adding user authentication | `john/add-user-auth` |
| Fixing token refresh bug | `john/fix-token-refresh` |
| Refactoring database config | `john/refactor-db-config` |
| Adding rate limiting | `john/add-rate-limiting` |
