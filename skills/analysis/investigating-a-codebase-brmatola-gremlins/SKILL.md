---
name: investigating-a-codebase
description: Use when planning or designing features and need to understand current codebase state, find existing patterns, or verify assumptions about what exists - prevents hallucination by grounding plans in reality
---

# Investigating a Codebase

## Overview

Understand current codebase state to ground planning and design decisions in reality, not assumptions. Find existing patterns, verify design assumptions, and provide definitive answers about what exists and where.

## When to Use

**Use for:**
- Verifying design assumptions before implementation ("Design assumes auth.ts exists - verify")
- Finding existing patterns to follow ("How do we currently handle API errors?")
- Locating features or code ("Where is user authentication implemented?")
- Understanding component architecture ("How does the routing system work?")
- Confirming existence definitively ("Does feature X exist or not?")
- Preventing hallucination about file paths and structure

**Don't use for:**
- Information available in external docs (use internet research)
- Questions answered by reading 1-2 specific known files (use Read directly)
- General programming questions not specific to this codebase

## Core Investigation Workflow

1. **Start with entry points** - main files, index, package.json, config
2. **Use multiple search strategies** - Glob patterns, Grep keywords, Read files
3. **Follow traces** - imports, references, component relationships
4. **Verify don't assume** - confirm file locations and structure
5. **Report definitively** - exact paths or "not found" with search strategy

## Verifying Design Assumptions

When given design assumptions to verify:

1. **Extract assumptions** - list what design expects to exist
2. **Search for each** - file paths, functions, patterns, dependencies
3. **Compare reality vs expectation** - matches, discrepancies, additions, missing
4. **Report explicitly**:
   - ✓ Confirmed: "Design assumption correct: auth.ts:42 has login()"
   - ✗ Discrepancy: "Design assumes auth.ts, found auth/index.ts instead"
   - + Addition: "Found logout() not mentioned in design"
   - - Missing: "Design expects resetPassword(), not found"

**Why this matters:** Prevents implementation plans based on wrong assumptions about codebase structure.

## Quick Reference

| Task | Strategy |
|------|----------|
| **Where is X** | Glob likely names → Grep keywords → Read matches |
| **How does X work** | Find entry point → Follow imports → Read implementation |
| **What patterns exist** | Find examples → Compare implementations → Extract conventions |
| **Does X exist** | Multiple searches → Definitive yes/no → Evidence |
| **Verify assumptions** | Extract claims → Search each → Compare reality vs expectation |

## Investigation Strategies

**Multiple search approaches:**
- Glob for file patterns across codebase
- Grep for keywords, function names, imports
- Read key files to understand implementation
- Follow imports and references for relationships
- Check package.json, config files for dependencies

**Don't stop at first result:**
- Explore multiple paths to verify findings
- Cross-reference different areas of codebase
- Confirm patterns are consistent not one-off
- Follow both usage and definition traces

**Verify everything:**
- Never assume file locations - always verify with Read/Glob
- Never assume structure - explore and confirm
- Document search strategy when reporting "not found"
- Distinguish "doesn't exist" from "couldn't locate"

## Reporting Findings

**Lead with direct answer:**
- Answer the question first
- Supporting details second
- Evidence with exact file paths and line numbers

**Provide actionable intelligence:**
- Exact file paths (src/auth/login.ts:42), not vague locations
- Relevant code snippets showing current patterns
- Dependencies and versions when relevant
- Configuration files and current settings
- Naming, structure, and testing conventions

**Handle "not found" confidently:**
- "Feature X does not exist" is valid and useful
- Explain what you searched and where you looked
- Suggest related code as starting point
- Report negative findings prevents hallucination

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assuming file locations | Always verify with Read/Glob before reporting |
| Stopping at first result | Explore multiple paths to verify findings |
| Vague locations ("in auth folder") | Exact paths (src/auth/index.ts:42) |
| Not documenting search strategy | Explain what was checked when reporting "not found" |
| Confusing "not found" types | Distinguish "doesn't exist" from "couldn't locate" |
| Skipping design assumption comparison | Explicitly report: confirmed/discrepancy/addition/missing |
| Reporting assumptions as facts | Only report what was verified in codebase |
