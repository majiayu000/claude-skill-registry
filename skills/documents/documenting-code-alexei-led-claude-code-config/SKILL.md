---
name: documenting-code
description: Update project documentation based on recent changes. Use when user says "update docs", "document", "add documentation", "update readme", "write docs", or wants to improve documentation.
user-invocable: true
context: fork
allowed-tools:
  - Task
  - TodoWrite
  - AskUserQuestion
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# Documentation Update

Update project documentation to reflect current code state.

**Use TodoWrite** to track these 5 phases:

1. Determine documentation scope
2. Analyze recent changes
3. Spawn docs-keeper agent
4. Update documentation
5. Verify and report

---

## Phase 1: Determine Scope

Use AskUserQuestion:

| Header    | Question                            | Options                                                                                                                                                                                                        |
| --------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Doc scope | What documentation should I update? | 1. **Auto-detect** - Scan for outdated docs based on recent changes 2. **README** - Update project README 3. **API docs** - Update API/function documentation 4. **All** - Comprehensive documentation refresh |

## Phase 2-4: Spawn docs-keeper Agent

Spawn **docs-keeper** agent with documentation prompt:

```
Task with docs-keeper agent:
"Update documentation for this project.

## Your Task

1. Analyze current state:
   - Run `git diff --name-only HEAD~5` for recent changes
   - Find existing docs: `find . -name '*.md' -o -name 'doc.go'`
   - Check project structure and dependencies

2. Scope: {user's choice from Step 1}

3. Update focus:
   - Accurate function/method documentation
   - README sections matching current state
   - API endpoint documentation
   - Architecture notes if significant changes

4. Verify:
   - No broken links
   - Code examples compile/run
   - Markdown renders correctly

## Output Format

DOCUMENTATION UPDATE
====================
Updated:
- file.md (what changed)
- pkg/doc.go (added GoDoc)

Verified: All links valid, examples compile"
```

## Phase 4: Research Best Practices (If Needed)

Use Context7 for documentation patterns:

```
mcp__context7__query-docs for GoDoc, Sphinx, or framework-specific docs
```

## Phase 5: Present Summary

Report what was updated and verified.

**Execute documentation update now.**
