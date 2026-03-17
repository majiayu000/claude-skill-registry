---
name: fork-dev-branch
description: Create a development branch for a given GitHub issue with standardized naming
---

# Fork Dev Branch

This skill instructs AI agents on how to create a development branch for implementing
a GitHub issue. The branch name follows the standard format: `issue-<number>-<brief-title>`.

## Branch Naming Convention

Branches created by this skill must follow this exact format:

```
issue-<number>-<brief-title>
```

Where:
- `<number>`: The GitHub issue number (without the `#` symbol)
- `<brief-title>`: A brief, hyphen-separated description of the issue
  - Lowercase only
  - Use hyphens to separate words
  - Maximum 5 words (preferably 3-4)
  - No special characters except hyphens
  - Must be meaningful and descriptive

**Examples:**
- `issue-42-add-typescript-support`
- `issue-15-fix-precommit-hook`
- `issue-67-create-open-pr-skill`
- `issue-23-refactor-sdk-templates`

## Workflow for AI Agents

When this skill is invoked, the AI agent **MUST** follow these steps:

### 1. Extract and Verify Issue Number

Find the issue number from conversation context:
- Look for explicit references: "for issue #42", "implement #15", etc.
- If not found, check recent issues: `gh issue list --limit 10`
- If still unclear, ask the user: "Which issue number should this branch be for?"
- Accept numbers with or without `#` prefix (e.g., "42" or "#42")

Verify the issue exists and is open:
```bash
gh issue view <issue-number> --json state,title
```

If the issue is closed or doesn't exist, inform the user and abort.

### 2. Generate Branch Title

Fetch the issue details and create a concise branch title:

```bash
gh issue view <issue-number>
```

Convert the issue title to branch format:
- Remove tag prefix (e.g., `[plan][feat]:` → empty)
- Convert to lowercase, replace spaces with hyphens
- Remove special characters (except hyphens)
- Keep 3-5 words maximum

**Title conversion examples:**
- `[plan][feat]: Add TypeScript SDK support` → `add-typescript-support`
- `[bugfix]: Pre-commit hook fails` → `fix-precommit-hook`
- `[agent.skill]: Create open-pr skill` → `create-open-pr-skill`

If unclear or too long, confirm with user before proceeding.

### 3. Create Branch

Create and switch to the new branch:

```bash
git checkout -b issue-<number>-<brief-title>
```

Confirm success:
```
Successfully created and switched to branch: issue-<number>-<brief-title>
```

## Examples

### Example 1: Simple Feature Branch

**Context:** User wants to implement issue #42 for TypeScript SDK support.

**Conversation:**
```
User: Create a dev branch for issue #42
Agent: [Runs gh issue view 42]
Agent: I'll create a branch for issue #42: "Add TypeScript SDK template support"

Suggested branch name: issue-42-add-typescript-support

Creating branch...
[Runs: git checkout -b issue-42-add-typescript-support]

Successfully created and switched to branch: issue-42-add-typescript-support
```

### Example 2: Bugfix Branch

**Context:** User wants to fix issue #15.

**Conversation:**
```
User: fork a branch for #15
Agent: [Runs gh issue view 15]
Agent: I'll create a branch for issue #15: "Pre-commit hook fails to run tests"

Suggested branch name: issue-15-fix-precommit-hook

Creating branch...
[Runs: git checkout -b issue-15-fix-precommit-hook]

Successfully created and switched to branch: issue-15-fix-precommit-hook
```

### Example 3: Error - Invalid Issue Number

**Context:** User provides a non-existent issue number.

**Conversation:**
```
User: Create dev branch for issue 999
Agent: [Runs gh issue view 999]
Agent: Error: Issue #999 not found in this repository.

Please provide a valid issue number.
```
