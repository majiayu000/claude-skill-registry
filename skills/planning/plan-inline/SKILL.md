---
name: plan-inline
description: Create TDD implementation plans directly from inline instructions. Use when you have a feature request, task description, or implementation idea that doesn't need to be added to TODO.md first. Supports codebase exploration and MCP integration.
argument-hint: <detailed task description>
allowed-tools: Read, Edit, Write, Glob, Grep, Task, mcp__gdrive__gdrive_search, mcp__gdrive__gdrive_read_file, mcp__gdrive__gdrive_list_folder, mcp__gdrive__gdrive_get_pdf, mcp__gdrive__gsheets_read, mcp__Railway__check-railway-status, mcp__Railway__get-logs, mcp__Railway__list-deployments, mcp__Railway__list-services, mcp__Railway__list-variables, mcp__gemini__gemini_analyze_pdf
disable-model-invocation: true
---

Create a TDD implementation plan directly from inline instructions in $ARGUMENTS.

## Purpose

- Convert inline task descriptions into actionable TDD implementation plans
- Skip the TODO.md intermediary when task is already well-defined
- Explore codebase to understand existing patterns and find relevant files
- Use MCPs to gather additional context (Drive files, spreadsheets, deployments)
- Generate detailed, implementable plans with full file paths

## When to Use

Use `plan-inline` instead of `plan-todo` when:
- The user provides a clear feature request or task description directly
- The task doesn't need to be tracked in TODO.md backlog
- Quick planning without backlog management overhead

Use `plan-todo` instead when:
- Working from existing backlog items
- Managing multiple items that should be tracked

## Pre-flight Check

**Before doing anything**, read PLANS.md and check for incomplete work:
- If PLANS.md has content but NO "Status: COMPLETE" at the end → **STOP**
- Tell the user: "PLANS.md has incomplete work. Please review and clear it before planning new items."
- Do not proceed.

If PLANS.md is empty or has "Status: COMPLETE" → proceed with planning.

## Arguments

$ARGUMENTS should contain the task description with context:
- What to implement or change
- Expected behavior
- Any constraints or requirements
- Related files if known

Example arguments:
- `Add a function to validate CUIT numbers with modulo 11 algorithm`
- `Create a new route /api/retry that retries failed documents`
- `Update resumen_tarjeta extraction to handle Naranja card format`

## Context Gathering

**IMPORTANT: Do NOT hardcode MCP names or folder paths.** Always read CLAUDE.md to discover:

1. **Available MCP servers** - Look for the "MCP SERVERS" section to find:
   - Google Drive MCP for file access (`gdrive_search`, `gdrive_read_file`, `gsheets_read`, etc.)
   - Railway MCP for deployment context (`get-logs`, `list-deployments`, `list-services`, `list-variables`)
   - Gemini MCP for prompt testing (`gemini_analyze_pdf`)

2. **Folder structure** - Look for "FOLDER STRUCTURE" section to understand:
   - Where documents are stored
   - Naming conventions for folders

3. **Project structure** - Look for "STRUCTURE" section to understand:
   - Source code organization
   - Test file locations
   - Where to add new files

4. **Spreadsheet schemas** - Look for "SPREADSHEETS" section or read SPREADSHEET_FORMAT.md

## Workflow

1. **Read PLANS.md** - Pre-flight check
2. **Read CLAUDE.md** - Understand TDD workflow, agents, project rules, available MCPs
3. **Parse $ARGUMENTS** - Understand what needs to be implemented
4. **Explore codebase** - Use Glob/Grep/Task to find relevant files and understand patterns
5. **Gather MCP context** - If the task relates to:
   - Document processing → Check Drive files, spreadsheet schemas
   - Deployment → Check service status, recent logs
   - Extraction issues → Check current prompts, test with Gemini MCP
6. **Generate plan** - Create TDD tasks with test-first approach
7. **Write PLANS.md** - Overwrite with new plan

## Codebase Exploration Guidelines

**When to explore:**
- Always explore to find existing patterns before creating new code
- Find related tests to understand testing conventions
- Locate where similar functionality already exists

**How to explore:**
- Use Glob for finding files by pattern: `src/**/*.ts`, `**/*.test.ts`
- Use Grep for finding code: function names, type definitions, error messages
- Use Task with `subagent_type=Explore` for broader questions about the codebase

**What to discover:**
- Existing functions that could be reused or extended
- Test file conventions and patterns
- Type definitions to reuse
- Similar implementations to follow as templates

## PLANS.md Structure

```markdown
# Implementation Plan

**Created:** YYYY-MM-DD
**Source:** Inline request: [Summary of $ARGUMENTS]

## Context Gathered

### Codebase Analysis
- **Related files:** [files found through exploration]
- **Existing patterns:** [patterns to follow]
- **Test conventions:** [how tests are structured in this area]

### MCP Context (if applicable)
- **MCPs used:** [which MCPs were consulted]
- **Findings:** [relevant information discovered]

## Original Plan

### Task 1: [Name]
1. Write test in [file].test.ts for [function/scenario]
2. Run test-runner (expect fail)
3. Implement [function] in [file].ts
4. Run test-runner (expect pass)

### Task 2: [Name]
1. Write test...
2. Run test-runner...
3. Implement...
4. Run test-runner...

## Post-Implementation Checklist
1. Run `bug-hunter` agent - Review changes for bugs
2. Run `test-runner` agent - Verify all tests pass
3. Run `builder` agent - Verify zero warnings
```

## Task Writing Guidelines

Each task must be:
- **Self-contained** - Full file paths, clear descriptions
- **TDD-compliant** - Test before implementation
- **Specific** - What to test, what to implement
- **Ordered** - Dependencies resolved by task order
- **Context-aware** - Reference patterns and files discovered during exploration

Good task example:
```markdown
### Task 1: Add validateCuit function
1. Write test in src/utils/validation.test.ts for validateCuit
   - Test valid CUIT returns true (use existing test fixtures)
   - Test invalid checksum returns false
   - Test invalid format returns false
   - Follow existing validation function patterns
2. Run test-runner (expect fail)
3. Implement validateCuit in src/utils/validation.ts
   - Use modulo 11 algorithm
   - Follow existing function signature patterns
4. Run test-runner (expect pass)
```

Bad task example:
```markdown
### Task 1: Add CUIT validation
1. Add function
2. Test it
```

## MCP Usage Guidelines

**Google Drive MCP** - Use when task involves:
- Document processing or extraction
- Spreadsheet column changes
- File organization or naming
- Understanding current document formats

**Railway MCP** - Use when task involves:
- Deployment configuration
- Environment variables
- Service logs for debugging context

**Gemini MCP** - Use when task involves:
- Prompt improvements
- Extraction accuracy
- Test prompt variations before planning changes

## Rules

- **Refuse to proceed if PLANS.md has incomplete work**
- **Explore codebase before planning** - Find patterns to follow
- **Use MCPs when relevant** - Gather context from external systems
- Every task must follow TDD (test first, then implement)
- No manual verification steps - use agents only
- Tasks must be implementable without additional context
- Always include post-implementation checklist
- Do NOT modify TODO.md (this skill bypasses backlog management)

## CRITICAL: Scope Boundaries

**This skill creates plans. It does NOT implement them.**

1. **NEVER ask to "exit plan mode"** - This skill doesn't use Claude Code's plan mode feature
2. **NEVER implement code** - Your job ends when PLANS.md is written
3. **NEVER ask ambiguous questions** like "should I proceed?" or "ready to continue?"
4. **NEVER start implementing** after writing the plan, even if user says "yes" to something

## Termination

When you finish writing PLANS.md, output this exact message and STOP:

```
✓ Plan created in PLANS.md

Next step: Run `plan-implement` to execute this plan.
```

Do not ask follow-up questions. Do not offer to implement. Just output the message and stop.
