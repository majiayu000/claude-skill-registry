---
name: gogogo
description: Execute the most recent plan issue step-by-step. Use when user types 'gogogo' or when ready to implement a planned feature/fix. Follow the plan, make code changes, test, and create PR.
model: sonnet
---

# GOGOGO - Execute Planned Implementation

## Purpose
Execute the implementation plan step-by-step, following the detailed plan from the most recent "plan:" issue.

## When to Use
- User explicitly types `gogogo`
- After creating a plan with `nnn`
- Ready to implement a planned feature or fix

## Steps

### 1. Find Implementation Issue

Find the most recent plan issue:
```bash
gh issue list --label "plan" --state open --limit 1 --json number,title
```

**If no plan issue found:**
- Tell user: "No plan issue found. Create one with `nnn` first."
- Stop execution

**If plan issue found:**
- Display: "Found plan: #[number] - [title]"
- Load the plan details:
```bash
gh issue view [number]
```

### 2. Prepare Branch

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# If on main, create feature branch
if [ "$CURRENT_BRANCH" = "main" ]; then
  BRANCH_NAME="feat/issue-[number]-[description]"
  git checkout -b $BRANCH_NAME
fi

# Ensure working directory is clean
git status
```

### 3. Execute Implementation

**Follow the plan step-by-step:**

For each phase in the plan:
1. **Announce Phase**: Tell user "Starting Phase X: [phase name]"
2. **Read Required Files**: Use `Read` tool for files mentioned in the phase
3. **Make Changes**: Use `Edit` or `Write` tools as needed
4. **Verify Changes**: Check that changes compile/work
5. **Update Checklist**: Comment on the issue to mark steps complete

**Important:**
- Follow the plan exactly - don't add unplanned features
- Keep changes focused and minimal
- Test after each significant change
- If you discover issues with the plan, ask user before deviating

### 4. Test & Verify

After implementation:
```bash
# Run build (if applicable)
[build-command]

# Run tests (if applicable)
[test-command]

# Manual verification
# Test key scenarios mentioned in the plan
```

**If tests fail:**
- Fix the issues
- Re-run tests
- Don't proceed until tests pass

### 5. Commit & Push

```bash
# Stage all changes
git add -A

# Create descriptive commit
git commit -m "$(cat <<'EOF'
feat: [Brief description from plan]

- What: [Specific changes made]
- Why: [Reason from plan]
- Impact: [What this affects]

Implements #[plan-issue-number]
EOF
)"

# Push to remote
git push -u origin $(git branch --show-current)
```

### 6. Create Pull Request

```bash
gh pr create --title "feat: [Same as commit title]" --body "$(cat <<'EOF'
## Summary
[Brief overview of what was implemented]

## Implementation Details
- [Key change 1]
- [Key change 2]
- [Key change 3]

## Testing
- [x] Build successful
- [x] Tests passing
- [x] Manual testing completed

## Related Issues
Implements #[plan-issue-number]

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 7. Update Plan Issue

Comment on the plan issue:
```bash
gh issue comment [plan-number] --body "✅ Implementation complete!

**PR Created:** #[pr-number]

**What was done:**
- [Summary of implementation]

**Test Results:**
- Build: ✅ Passing
- Tests: ✅ All passing
- Manual: ✅ Verified

Ready for review!"
```

### 8. Report to User

Provide a complete summary:
```
✅ Implementation Complete!

**Plan Issue:** #[plan-number]
**PR Created:** #[pr-number]
**Branch:** [branch-name]

**Changes:**
- [file1]: [what changed]
- [file2]: [what changed]

**Tests:** ✅ All passing
**Build:** ✅ Successful

**Next steps:**
1. Review the PR: [pr-url]
2. Request review from team
3. Merge when approved

⚠️ **IMPORTANT:** Don't merge until user explicitly approves!
```

## Important Notes
- **Follow the Plan**: Don't deviate without asking
- **Test Everything**: Never skip testing
- **Commit Often**: Make logical commits as you progress
- **Safety First**: Follow all git safety rules (no --force)
- **Never Merge**: Only create PR, wait for user approval
- **Ask Questions**: If plan is unclear, ask user before proceeding
- **Update Issue**: Keep the plan issue updated with progress

## Error Handling

**If build fails:**
1. Read error messages carefully
2. Fix the issues
3. Re-run build
4. Continue only when passing

**If plan is incomplete:**
1. Ask user for clarification
2. Update plan issue with questions
3. Wait for user response

**If stuck:**
1. Document what you tried
2. Comment on plan issue with blockers
3. Ask user for guidance

## Success Criteria
- ✅ All plan phases completed
- ✅ All tests passing
- ✅ Build successful
- ✅ PR created (not merged)
- ✅ Plan issue updated
- ✅ User provided with clear summary
