---
name: done
description: Task completion workflow - run tests, commit/push, update MASTER_PLAN.md status, create SOP if needed. This skill should be used when a task is complete and ready to be finalized. Triggers on "/done", "mark done", "task complete", "finish task".
---

# Task Completion Workflow

Finalize a completed task: verify tests pass, commit changes, update MASTER_PLAN.md, and optionally create an SOP.

## Workflow

### Step 1: Check What Changed

**FIRST**, run git status to see what files were modified:

```bash
git status
git diff --stat
```

**Output to user immediately:**
```
Files changed:
- [list of modified files]
```

### Step 2: Get Task Information

Ask user for task details. Use `AskUserQuestion` tool:

**Questions:**
1. **Task ID** (header: "Task ID")
   - Options: "Tracked task (enter ID)" or "Quick fix (no ID)"

2. **Create SOP?** (header: "Create SOP")
   - Options: "No" (recommended) or "Yes"

**Then ask in plain text:** "What's a brief summary of the changes? (1-2 sentences)"

**IMPORTANT**: Wait for user to provide the summary before proceeding.

### Step 3: Run Tests

Execute test suite:

```bash
npm run test
```

**If tests fail**: STOP immediately. Report failures. Do NOT proceed.

**If tests pass**: Continue.

### Step 4: Update MASTER_PLAN.md (if tracked task)

**Skip this step if user selected "Quick fix (no ID)".**

**CRITICAL**: Tasks appear in **3 locations**. Update ALL of them:

#### 4a. Summary Table (Roadmap section)

```markdown
# Before:
| **TASK-XXX** | **Title** | **P2** | 📋 **PLANNED** | ... |

# After:
| ~~**TASK-XXX**~~ | ✅ **Title** | **P2** | ✅ **DONE** (YYYY-MM-DD) | ... |
```

#### 4b. Subtasks Lists (if applicable)

```markdown
# Before:
- TASK-XXX: Description

# After:
- ~~TASK-XXX~~: ✅ Description
```

#### 4c. Detailed Section (#### headers)

```markdown
# Before:
#### TASK-XXX: Title (📋 PLANNED)

# After:
#### ~~TASK-XXX~~: Title (✅ DONE)
```

#### 4d. Verify All Updated

```bash
grep "TASK-XXX" docs/MASTER_PLAN.md
```

All matches must show strikethrough or ✅ DONE.

### Step 5: Create SOP (if requested)

**Skip if user selected "No" for SOP.**

1. Find next SOP number: `ls docs/sop/SOP-*.md | tail -1`
2. Create `docs/sop/SOP-XXX-<name>.md` using template:

```markdown
# SOP-XXX: [Title]

**Created**: [Date]
**Related Task**: [TASK-ID]
**Status**: Active

## Problem
[What problem does this solve?]

## Solution
[Step-by-step solution]

## Key Files
- `path/to/file.ts` - [what it does]

## Verification
[How to verify the fix works]
```

### Step 6: Commit and Push (MANDATORY)

**This step is NOT optional. ALL changes must be committed and pushed.**

```bash
# Stage all relevant files (NOT .env, credentials, or backup files)
git add <code-files>
git add docs/MASTER_PLAN.md  # if task was tracked
git add docs/sop/SOP-*.md    # if SOP was created

# Commit with proper message
git commit -m "$(cat <<'EOF'
[TASK-XXX] Brief summary from user

- Key change 1
- Key change 2

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Push to remote (triggers deployment)
git push
```

**For quick fixes (no task ID):**
```bash
git commit -m "$(cat <<'EOF'
fix: Brief summary from user

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
git push
```

### Step 7: Verify Deployment

**Wait for CI/CD and confirm:**

```bash
# Check if push triggered CI
gh run list --limit 1
```

### Step 8: Report Completion

**Output this summary to user:**

```
✅ Task Complete

Summary:
- Tests: ✅ Passed
- Commit: [hash] - [message]
- Push: ✅ Pushed to origin/master
- Deployment: ✅ CI/CD triggered
- MASTER_PLAN.md: [Updated / N/A (quick fix)]
- SOP: [Created SOP-XXX / Not needed]
```

---

## Important Rules

1. **NEVER skip tests** - Always run `npm run test` first
2. **NEVER skip commit/push** - Changes must be deployed
3. **ALWAYS collect summary** - Don't proceed without knowing what changed
4. **Update ALL 3 locations** in MASTER_PLAN.md for tracked tasks
5. **Verify with grep** after updating MASTER_PLAN.md
6. **Wait for user input** - Don't assume or skip questions

## Files to NEVER Commit

- `.env*` files
- `credentials*.json`
- `backups/shadow.db`
- `public/shadow-latest.json`
- `stats.html` (generated)
