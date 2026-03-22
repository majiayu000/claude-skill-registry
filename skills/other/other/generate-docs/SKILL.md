---
name: generate-docs
description: |
  Use this skill to generate, update, or improve documentation. Triggered by
  "write docs", "generate documentation", "update README", "document this code".
argument-hint: "[file, function, or module]"
allowed-tools: "Read, Write, Edit, Grep, Glob"
context: fork
---

# Documentation Generator

Generate clear, accurate documentation for the specified code.

## Target

`$ARGUMENTS`

!`ls -la $ARGUMENTS 2>/dev/null || echo "Scanning for files..."`

## Instructions

1. Read all relevant source files for the target
2. Identify what needs documentation:
   - Public functions, classes, and methods
   - Module purpose and exports
   - Configuration options
   - Usage examples

3. Choose the appropriate format:
   - **JSDoc/TSDoc** for TypeScript/JavaScript functions
   - **docstring** for Python
   - **godoc** for Go
   - **README.md** for modules/repos
   - **API.md** for REST API endpoints

4. Write documentation that includes:
   - **Purpose** — what it does (1-2 sentences)
   - **Parameters** — name, type, description, whether required
   - **Returns** — type and description
   - **Throws** — what errors can occur
   - **Example** — minimal working example
   - **Notes** — gotchas, performance notes, deprecations

## JSDoc Example

```typescript
/**
 * Fetches a paginated list of users matching the given filters.
 *
 * @param filters - Search criteria to narrow results
 * @param filters.role - Optional role filter ('admin' | 'user' | 'guest')
 * @param filters.active - When true, returns only active accounts
 * @param page - 1-based page number (default: 1)
 * @param pageSize - Results per page, max 100 (default: 20)
 * @returns Paginated result with users and total count
 * @throws {ValidationError} When pageSize exceeds 100
 * @throws {DatabaseError} When the query times out
 *
 * @example
 * const result = await getUsers({ role: 'admin', active: true });
 * console.log(result.total, result.users);
 */
```

## Rules

- Do NOT fabricate behavior — only document what the code actually does
- Keep examples minimal but runnable
- If the code is confusing, note it and suggest a refactor
- Update existing docs rather than creating duplicates
- For READMEs: include install, usage, configuration, and contributing sections

$ARGUMENTS
