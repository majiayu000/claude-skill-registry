---
name: dev-finish
description: Close a dev-cycle session, capture learnings, and optionally commit. Use when development work is complete and ready to wrap up.
---

# Dev Finish - Quality Gate & Close

Complete a dev-cycle session: Code Review → Fix Issues → Commit → PR → Learn → Archive

**Key principle**: We ship quality. Bob and Garry review before we close. Arlo joins when data/analytics are involved.

## Agent Roles in Review

- **Bob**: Code quality, bugs, security, performance, tests
- **Garry**: Requirements match, architecture, completeness
- **Arlo**: Data logic, calculations, patterns, analytics accuracy (when applicable)

## Flow

### 1. Find Active Session

```bash
ls ~/.claude/dev-cycles/active/ | grep "$(basename $(pwd))"
```

If no active session:
- "No active dev-cycle found for this project. Nothing to finish."
- Exit

If found:
- Read session file
- Show summary of what was done

### 2. Generate Diff for Review

Save the full diff to a file for thorough review:

```bash
# Create review directory if needed
mkdir -p ~/.claude/dev-cycles/reviews

# Get project and branch info
PROJECT=$(basename $(pwd))
BRANCH=$(git branch --show-current)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Save full diff to file
git diff main...HEAD > ~/.claude/dev-cycles/reviews/${PROJECT}--${BRANCH}--${TIMESTAMP}.diff

# Also save stat summary
git diff main...HEAD --stat > ~/.claude/dev-cycles/reviews/${PROJECT}--${BRANCH}--${TIMESTAMP}.stat
```

Present summary to Tako:
- Files changed
- Lines added/removed
- Diff saved to: `{path}`

### 3. Code Review (Quality Gate)

**This is critical. We don't ship without review.**

#### Step 1: Bob Reviews Code Quality

Delegate to Bob:
```
"Bob, review this diff file: {diff-path}

Check for:
- Code quality and readability
- Potential bugs or edge cases
- Security issues
- Performance concerns
- Missing error handling
- Test coverage gaps

Be thorough. List issues by severity:
- CRITICAL: Must fix before merge
- WARNING: Should fix
- SUGGESTION: Nice to have"
```

#### Step 2: Arlo Reviews Data Logic (if applicable)

**Include Arlo when the session involves data/analytics/numbers.**

Check session file for `Involves Data/Analytics: yes` or detect from diff:
- Database queries, aggregations
- Calculations, statistics
- Charts, dashboards, reports
- Data transformations
- Financial logic

If data is involved, delegate to Arlo:
```
"Arlo, review the data/analytics aspects of this diff: {diff-path}

Check for:
- Data logic correctness
- Edge cases: nulls, zeros, negatives, empty sets
- Calculation accuracy
- Aggregation logic
- Query efficiency and correctness
- Numbers telling the right story
- Pattern detection logic (if any)

List issues by severity:
- CRITICAL: Data bug, wrong calculations
- WARNING: Edge case not handled
- SUGGESTION: Could be more efficient"
```

#### Step 3: Garry Validates Completeness

Then delegate to Garry:
```
"Garry, review Bob's findings{, Arlo's findings,} and the diff: {diff-path}

Validate:
- Does this match the original requirements from the session?
- Any architectural concerns?
- Anything the reviewers missed?
- Is this ready to ship?"
```

### 4. Address Review Findings

If CRITICAL or WARNING issues found:
```
Code review found issues:

CRITICAL:
- [Issue 1]
- [Issue 2]

WARNING:
- [Issue 3]

Options:
1. Fix issues now (Bob will fix, then re-review)
2. Fix issues manually, then run /finish-dev again
3. Ship anyway (not recommended)
4. Abandon this session
```

If "Fix issues now":
- Bob fixes each issue
- Re-run review on the new diff
- Loop until clean

If review passes:
- "Code review passed. Ready to commit."

### 5. Commit Question

Ask Tako:
```
Ready to commit these changes?

Options:
1. Yes, single commit with message I'll provide
2. Yes, help me write the commit message
3. Yes, multiple commits (per logical change)
4. No, leave uncommitted
5. Already committed during build
```

If committing:
- Follow commit conventions from branch-workflow
- NO Co-Authored-By lines (per Tako's rules)
- Use conventional commit format

### 6. Pull Request Question

Ask Tako:
```
Create a Pull Request?

Options:
1. Yes, create PR now (I'll help write description)
2. Yes, create PR with message I'll provide
3. No, just push the branch
4. No, don't push anything
```

If creating PR:
```bash
# Push branch first
git push -u origin $(git branch --show-current)

# Create PR
gh pr create --title "{title}" --body "{body}"
```

PR body template:
```markdown
## Summary
{Brief description of changes}

## Changes
{Key changes from git diff --stat}

## Testing
{How this was tested}

## Review Notes
{Any context for reviewers}

---
Dev cycle session: {session-file}
```

### 7. Learning Extraction

Analyze the session:
1. Read the session file (discoveries, decisions, blockers)
2. Look at the git diff
3. Review findings from Bob/Garry
4. Consider what went well/poorly

Ask Tako:
```
Let's capture what we learned. I noticed:

- [Observation 1 from session/diff/review]
- [Observation 2]
- [Observation 3]

Questions:
1. What worked well in this session?
2. Any gotchas or things to avoid next time?
3. Any patterns worth remembering?

Which learnings should I save?
- Project-specific → goes to .megg/knowledge.md
- General (applies everywhere) → goes to ~/.megg/knowledge.md
```

For each learning, use megg:
```
mcp__megg__learn with:
- title: Short descriptive title
- type: decision | pattern | gotcha | context
- topics: [relevant tags]
- content: The learning in markdown
- path: Project path for project-specific, or home for global
```

### 8. Archive Session

Move session to completed:
```bash
mv ~/.claude/dev-cycles/active/{session-file} ~/.claude/dev-cycles/completed/
```

Update session file with completion metadata:
```markdown
## Completion
- **Finished**: {timestamp}
- **Final Branch**: {branch-name}
- **Commits**: {commit hashes or "uncommitted"}
- **PR**: {PR URL or "none"}
- **Review Status**: passed | passed-with-warnings | skipped
- **Learnings Captured**: {count}
- **Final Status**: completed | partial | abandoned

## Code Review Summary
{Summary of Bob/Garry findings and resolutions}

## Git Summary
{Output of git diff --stat}

## Learnings Saved
1. [Project] "JWT refresh token pattern" - pattern
2. [Global] "Always test auth flows in isolation" - pattern
```

Clean up review files:
```bash
rm ~/.claude/dev-cycles/reviews/${PROJECT}--${BRANCH}--*.diff
rm ~/.claude/dev-cycles/reviews/${PROJECT}--${BRANCH}--*.stat
```

### 9. Final Summary

Present to Tako:
```
Dev cycle complete!

Summary:
- Session: {description}
- Duration: {start} to {end}
- Branch: {branch}
- Changes: {files changed}, {lines added/removed}
- Review: {passed/passed-with-warnings}
- Commits: {commit info}
- PR: {PR URL or "not created"}
- Learnings: {count} captured ({N} project, {M} global)

Session archived to ~/.claude/dev-cycles/completed/
```

## Edge Cases

### Partial Completion
If not all tasks done:
- Ask: "Not all tasks completed. Finish anyway or continue working?"
- If finish: Still do full review, mark status as "partial"
- If continue: Stay in dev-cycle, don't archive

### Review Finds Major Issues
If review finds architectural problems:
- Stop and discuss with Tako
- May need to revisit the plan
- Option to abandon and start fresh

### No Changes Made
If git shows no changes:
- Skip code review (nothing to review)
- Skip commit/PR questions
- Still capture learnings (discovery learnings are valuable)
- Archive normally

### Already Has PR
If PR already exists for this branch:
```bash
gh pr view --web  # Show existing PR
```
- Skip PR creation
- Ask if want to update PR description

## Example Finish

```
Me: Found active dev-cycle: "User authentication with JWT"

    Session started: 2024-01-15 10:00
    Branch: feat/add-user-auth
    Tasks: 5/5 done

    Saving diff for review...
    - 8 files changed, 342 insertions, 12 deletions
    - Diff saved to: ~/.claude/dev-cycles/reviews/myapp--feat-add-user-auth--20240115-143000.diff

    Starting code review...

[Bob reviews]

Bob: Review complete. Findings:

    CRITICAL: None

    WARNING:
    - src/auth/jwt.ts:45 - Token expiry not validated on refresh

    SUGGESTION:
    - Consider adding rate limiting to login endpoint

[Garry validates]

Garry: Bob's review is thorough. The token expiry issue is valid.
       Architecture looks good. One warning to address.

Me: Code review found 1 warning:
    - Token expiry not validated on refresh

    Options:
    1. Fix now
    2. Fix manually, re-run /finish-dev
    3. Ship anyway
    4. Abandon

User: 1

[Bob fixes, re-reviews]

Me: Fix applied. Re-reviewing...
    Review passed. Ready to commit.

    Commit options?
    1. Single commit, my message
    2. Help write message
    3. Multiple commits
    4. Leave uncommitted
    5. Already committed

User: 2

Me: Suggested commit message:

    feat(auth): add JWT authentication system

    - Add auth middleware for protected routes
    - Implement login/logout endpoints
    - Add refresh token rotation with expiry validation
    - Include comprehensive auth tests

    Use this?

User: yes

Me: Committed: abc1234

    Create Pull Request?
    1. Yes, help write description
    2. Yes, my description
    3. Just push
    4. Don't push

User: 1

Me: Creating PR...

    PR created: https://github.com/user/repo/pull/42

    Now let's capture learnings...

    [Learning extraction continues...]

    Dev cycle complete!
    - Review: passed
    - Commit: abc1234
    - PR: https://github.com/user/repo/pull/42
    - Learnings: 2 captured
```

## Integration

**With megg**: Use `mcp__megg__learn` for learning capture

**With Bob**: Delegate code review and fixes

**With Garry**: Validate review completeness and architectural alignment

**With Arlo**: Data/analytics validation when numbers are involved

**With gh CLI**: Create PRs with `gh pr create`

## When to Include Arlo

Arlo joins the review when the work involves:
- Analytics dashboards or reporting
- Data processing or transformation
- Calculations, aggregations, statistics
- Database queries with numeric results
- Charts, graphs, visualizations
- Pattern detection or anomaly detection
- Financial calculations
- Metrics, KPIs, measurements

Detect from:
1. Session file `Involves Data/Analytics: yes`
2. Diff contains: SQL queries, aggregation functions, chart code, calculation logic
