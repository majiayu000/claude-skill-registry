---
name: refactor
description: Refactor code across the codebase using parallel Snipper agents. Use when user wants to rename methods, update patterns, fix code smells, or apply consistent changes across multiple files.
argument-hint: <search-pattern-or-description>
---

# Refactor

Refactor code matching `$ARGUMENTS` across the codebase using parallel Snipper agents for maximum speed.

## Process

### Phase 1: Discovery

1. **Parse the refactor request** from `$ARGUMENTS`
   - Identify: method name, component name, pattern, or code smell
   - Choose search strategy: Grep for code patterns, Glob for file patterns

2. **Find all affected files**
   - Use Grep/Glob to search the codebase
   - Exclude: node_modules, .git, dist, build
   - If >15 files found, ask user to confirm or narrow scope

### Phase 2: Create Instructions

3. **Create task folder**: `.claude/tasks/refactor-{timestamp}/`

4. **Create ONE instruction file** at `instructions.md`:

```markdown
# Refactor: {title}

## Objective
{What to refactor - derived from $ARGUMENTS}

## Pattern to Find
{Exact code pattern or structure to locate}

## Transformation
{How to transform - be specific and adaptive}

## Examples
Before:
{current code}

After:
{refactored code}

## Constraints
- Only modify code matching the pattern
- Preserve all existing functionality
- Follow codebase conventions
```

### Phase 3: Execute in Parallel

5. **Group files** into batches of max 3 files each

6. **Launch Snipper agents in parallel** - ALL batches in a SINGLE message:

```
Using instructions in .claude/tasks/refactor-{id}/instructions.md, refactor:
- {file_1}
- {file_2}
- {file_3}

Read instructions first, then apply the refactor to each file.
```

### Phase 4: Verification

7. **Validate changes**
   - Run `pnpm lint` (if available)
   - Run `pnpm tsc` (if TypeScript)

8. **Report summary**
   - Files modified
   - Errors encountered
   - Next steps if needed

## Example

User: `/refactor rename getUserData to fetchUserProfile`

1. Grep finds 12 files containing "getUserData"
2. Creates `.claude/tasks/refactor-1702489200/instructions.md`
3. Groups into 4 batches of 3 files
4. Launches 4 Snipper agents in parallel
5. Runs lint, reports: "Refactored 12 files"
