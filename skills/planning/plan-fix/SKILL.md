---
name: plan-fix
description: Investigate bugs and create TDD fix plans. Use when a bug is reported after file processing (extraction errors, wrong data, missing matches), deployment failures, or prompt-related issues. Supports codebase, deployment, and Gemini prompt investigation.
argument-hint: <bug description with context>
allowed-tools: Read, Edit, Write, Glob, Grep, Task, mcp__gdrive__gdrive_search, mcp__gdrive__gdrive_read_file, mcp__gdrive__gdrive_list_folder, mcp__gdrive__gdrive_get_pdf, mcp__gdrive__gsheets_read, mcp__Railway__check-railway-status, mcp__Railway__get-logs, mcp__Railway__list-deployments, mcp__Railway__list-services, mcp__Railway__list-variables, mcp__gemini__gemini_analyze_pdf
disable-model-invocation: true
---

Investigate bugs and create TDD fix plans in PLANS.md.

## Purpose

- Investigate bugs found after processing files (extraction errors, wrong data, missing matches)
- Debug deployment failures using Railway MCP
- Test and iterate Gemini prompts when extraction issues are suspected
- Create investigation report documenting findings and root cause
- Generate TDD-based fix plan in PLANS.md
- Does NOT implement fixes (integrates with plan-implement)

## Pre-flight Check

**Before doing anything**, read PLANS.md and check if it contains incomplete work:
- If PLANS.md has content but NO "Status: COMPLETE" at the end → **STOP**
- Tell the user: "PLANS.md has incomplete work. Please review and clear it before planning new items."
- Do not proceed.

If PLANS.md is empty or has "Status: COMPLETE" → proceed with investigation.

## Arguments

$ARGUMENTS should contain the bug description with context:
- What happened vs what was expected
- File IDs if relevant (Google Drive file IDs)
- Error messages or unexpected values
- Deployment ID if it's a deployment issue
- Any other context that helps investigation

## Context Gathering

**IMPORTANT: Do NOT hardcode MCP names or folder paths.** Always read CLAUDE.md to discover:

1. **Available MCP servers** - Look for the "MCP SERVERS" section to find:
   - Google Drive MCP for file access (`gdrive_search`, `gdrive_read_file`, `gsheets_read`, etc.)
   - Railway MCP for deployment debugging (`get-logs`, `list-deployments`, `list-services`, `list-variables`)
   - Gemini MCP for prompt testing (`gemini_analyze_pdf`)

2. **Folder structure** - Look for "FOLDER STRUCTURE" section to understand:
   - Where documents are stored
   - Naming conventions for bank folders, card folders, broker folders

3. **Document types** - Look for "DOCUMENT CLASSIFICATION" section to understand:
   - Document type → destination mapping
   - ADVA role in each document type

4. **Spreadsheet schemas** - Look for "SPREADSHEETS" section or read SPREADSHEET_FORMAT.md

## Investigation Workflow

### Step 1: Classify the Bug Type

Based on $ARGUMENTS, determine the bug category:

| Category | Indicators | Primary Tools |
|----------|-----------|---------------|
| **Extraction** | Wrong data extracted, missing fields | Google Drive MCP, Gemini MCP |
| **Deployment** | Service down, build failures, runtime errors | Railway MCP |
| **Matching** | Wrong matches, missing matches | Google Drive MCP, Codebase |
| **Storage** | Data not saved, wrong spreadsheet | Google Drive MCP, Codebase |
| **Prompt** | Consistent extraction errors on specific doc types | Gemini MCP |

### Step 2: Gather Evidence

**For Codebase Issues:**
- Use Grep/Glob for searching the codebase
- Use Task tool with subagent_type=Explore for broader exploration
- Read relevant source files and tests

**For Deployment Issues:**
1. `check-railway-status` - Verify CLI is working
2. `list-services` - Find the affected service
3. `list-deployments` - Get recent deployment IDs and statuses
4. `get-logs` with `logType: "deploy"` - Check deployment logs
5. `get-logs` with `logType: "build"` - Check build logs if deployment failed
6. `list-variables` - Verify environment configuration

**For Document/Drive Issues:**
- `gdrive_search` - Find the problematic file
- `gdrive_read_file` or `gdrive_get_pdf` - Read file contents
- `gsheets_read` - Check spreadsheet data

**For Prompt Issues (when extraction is consistently wrong):**
1. Get the source PDF using `gdrive_get_pdf`
2. Use `gemini_analyze_pdf` to test alternative prompts
3. Compare current prompt output vs expected output
4. Iterate on prompt wording until extraction improves
5. Document the improved prompt for implementation

### Step 3: Document Findings

Write PLANS.md with this structure:

```markdown
# Bug Fix Plan

**Created:** YYYY-MM-DD
**Bug Report:** [Summary from $ARGUMENTS]
**Category:** [Extraction | Deployment | Matching | Storage | Prompt]

## Investigation

### Context Gathered
- **MCPs used:** [list which MCPs were used and why]
- **Files examined:** [list files checked - Drive files, spreadsheets, code files, logs]

### Evidence
[Detailed findings from investigation with specific data points]

### Root Cause
[Clear explanation of why the bug occurs]

## Fix Plan

### Fix 1: [Title matching the issue]
1. Write test in [file].test.ts for [scenario that reproduces the bug]
2. Implement fix in [file].ts

### Fix 2: [Title]
...

## Post-Implementation Checklist
1. Run `bug-hunter` agent - Review changes for bugs
2. Run `test-runner` agent - Verify all tests pass
3. Run `builder` agent - Verify zero warnings
```

## Gemini Prompt Testing Guidelines

When investigating extraction issues:

1. **Get the problematic PDF** using `gdrive_get_pdf`
2. **Read current prompt** from `src/gemini/prompts.ts`
3. **Test with `gemini_analyze_pdf`** using variations of the prompt
4. **Document what works** - Include the improved prompt in the fix plan
5. **Note:** `gemini_analyze_pdf` is for testing ONLY, not production analysis

Example prompt testing workflow:
```
1. Current prompt extracts "fechaCierre" as null
2. Test prompt variation A: "Look for 'Fecha de Cierre' or 'CIERRE'"
3. Test prompt variation B: "The closing date appears near the top of the statement"
4. Variation B correctly extracts the date
5. Add to fix plan: Update prompts.ts with variation B
```

## Railway Debugging Guidelines

When investigating deployment issues:

1. **Check status first** - `check-railway-status` confirms CLI access
2. **List recent deployments** - `list-deployments` with `json: true` for structured data
3. **Get targeted logs** - Use `filter` parameter to search for errors:
   - `filter: "@level:error"` - Find error-level logs
   - `filter: "TypeError"` - Search for specific errors
4. **Check environment** - `list-variables` to verify config

## Rules

- **Refuse to proceed if PLANS.md has incomplete work**
- **Do NOT hardcode MCP names or folder paths** - always read from CLAUDE.md
- **Investigation only** - do not modify source code
- All fixes must follow TDD (test first)
- Include enough detail for another model to implement without context
- Always include post-implementation checklist
- For prompt issues, test multiple variations before recommending changes

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
