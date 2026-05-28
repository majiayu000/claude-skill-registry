---
name: repo-conventions-check
description: |
  MANDATORY before adding files to any repo. Enforces checking existing patterns
  and confirming with the user before starting work. Use when: (1) adding new files,
  (2) adding new skills, (3) creating PRs, (4) any structural changes.
  BLOCKS progress until conventions are verified and user confirms the plan.
category: workflow
user-invocable: true
---

# Repo Conventions Check

**MANDATORY** before adding any files or making structural changes to a repository.

## Blocking Condition

Before adding ANY new file or directory, you MUST:

1. **Find existing examples** of similar files
2. **State the correct location** based on those examples
3. **Tell the user your plan** and wait for confirmation
4. **Send updates** during work

If you skip any step: **BLOCKED**

## Workflow

### Step 1: Find Existing Patterns

Before adding a file, search for similar existing files:

```bash
# For skills
ls -la .claude/skills/ | head -10
find . -name "SKILL.md" -type f | head -10

# For any file type
find . -name "*.ts" -type f | head -10
find . -type d -name "similar-name" | head -10
```

### Step 2: State the Location

Tell the user explicitly:

```
Based on existing skills in .claude/skills/, I will add the new skill to:
  skills/my-new-skill/SKILL.md

NOT in packages/skills/skills/ (generated output; do not edit).
```

### Step 3: Confirm Before Starting

**DO NOT START WORK** until you've told the user:
- What you're going to do
- Where files will go
- What the PR will contain

Wait for their confirmation or correction.

### Step 4: Send Updates

During work, send updates every few minutes:
- What you just did
- What you're doing next
- Any issues or questions

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "I know where it goes" | You were wrong last time | Check existing patterns |
| "It's obvious" | Clearly it wasn't | Confirm with user |
| "I'll tell them after" | Too late to fix mistakes | Tell them BEFORE |
| "They're busy" | Silence is worse | Brief update is fine |
| "It's a small change" | Small mistakes compound | Follow the process |

## Examples

### Wrong (BLOCKED)

```
User: Add a new skill for X

*immediately creates files without checking*
*puts skill in wrong location*
*doesn't tell user what's happening*
```

### Correct

```
User: Add a new skill for X

Me: I'll add this skill. First let me check where existing skills live...

*runs: ls .claude/skills/*

Existing skills are in .claude/skills/. I'll create:
  .claude/skills/x-skill/SKILL.md

Does that look right? I'll start once you confirm.

User: yes

Me: Starting now. I'll update you in a few minutes.

*does work*

Me: Done. Created the skill and pushed to branch feature/x-skill.
Creating PR now.
```

## Enforcement

This skill chains with other skills:
- **Before** any file creation: repo-conventions-check MUST run
- **Before** any PR: verify locations match existing patterns
- **During** work: send updates via available channels

## Self-Check

Before completing any task that adds files:

1. Did I check existing patterns?
2. Did I tell the user my plan?
3. Did I wait for confirmation?
4. Did I send updates during work?

If any answer is "no": **STOP and fix it.**
