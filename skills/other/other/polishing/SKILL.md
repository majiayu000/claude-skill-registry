---
name: polishing
description: Polish code changes by recovering context, checking against codebase guidelines, removing AI slop, and running review. Use when finalizing work on a branch before PR.
user-invocable: true
---

# Polishing

A comprehensive workflow for finalizing code changes before creating a PR. This skill ensures code quality, consistency with codebase patterns, and removes common AI-generated artifacts.

## Workflow

### Step 1: Recover Branch Context

Use the Skill tool to invoke `recover-branch-context` to understand what the branch is trying to accomplish.

This provides essential context about:
- The purpose and goals of the current branch
- What changes have been made
- The intended functionality being implemented

### Step 2: Check Against Applicable Guidelines

Scan the `.agents/skills/` directory for skills that might have guidelines relevant to the changed files.

Match skills to the technologies used in the changed files. For example, if React components were changed, look for a React patterns skill; if an ORM was used, look for a relevant ORM skill.

For each applicable skill:
1. Spawn a subagent to review the changed files against those skill's guidelines
2. Report any deviations from the established patterns
3. Fix deviations where appropriate, or note them for discussion

### Step 3: Remove AI Slop

Check the diff against the default branch, and remove all AI generated slop introduced in this branch.

This includes:
- Extra comments that a human wouldn't add or is inconsistent with the rest of the file
- Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase (especially if called by trusted / validated codepaths)
- Casts to `any` to get around type issues
- Any other style that is inconsistent with the file

### Step 4: Final Review

Do a final review of the changes — read through the diff and flag anything that looks off.

### Step 5: Report

Provide a summary of:
- **Branch context recovered**: What the branch is trying to accomplish
- **Guidelines checked and any deviations found**: Which skills were applicable and what patterns were verified or corrected
- **Slop removed**: What AI artifacts were cleaned up
- **Review results**: Any issues surfaced by the final review