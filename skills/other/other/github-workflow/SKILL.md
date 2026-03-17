---
name: github-workflow
description: GitHub issue and progress management for this repo's maintainers - when to create/update issues, how to format updates, and agent identification
---

# GitHub Workflow Skill

## When to Invoke This Skill

**Use this skill BEFORE:**

- Creating a GitHub issue for a new feature
- Posting progress updates to GitHub issues
- Linking documentation to issues
- Closing issues after feature completion

## Core Principle

**GitHub is the coordination hub.** All feature work, progress updates, and PR activity MUST be tracked in GitHub issues with proper agent identification.

---

## 1. GitHub Issue Creation (Feature Kickoff)

### When to Create

After plan approval, BEFORE starting implementation.

### Issue Creation Command

```bash
gh issue create \
  --title "Feature: {Feature Name}" \
  --body "$(cat <<'EOF'
## Overview
{Brief description from INDEX}

## Documentation
- INDEX: [docs/system/INDEX-{feature}.md]
- Design docs: Listed in INDEX

## Phases
- [ ] Phase 1.1: {Phase name}
- [ ] Phase 1.2: {Phase name}
- [ ] Phase 1.3: {Phase name}

## Branch
`feature/desk-{feature-name}`

---
🤖 Created by {agent-name}
EOF
)"
```

### After Issue Creation

1. **Update INDEX frontmatter** with issue number:
   ```yaml
   github_issue: "#123"
   feature_branch: "feature/desk-{feature-name}"
   ```

2. **Commit and push INDEX update**:
   ```bash
   git add docs/system/INDEX-{feature}.md
   git commit -m "Add GitHub issue tracking to INDEX

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   git push -u origin feature/desk-{feature-name}
   ```

3. **Post kickoff comment** with agent identification:
   ```bash
   gh issue comment {issue-number} --body "🚀 **Feature Kickoff**

   **Agent**: {agent-name}
   **Status**: Feature branch created and INDEX updated
   **Next**: Starting Phase 1.1 implementation

   Branch: \`feature/desk-{feature-name}\`"
   ```

---

## 2. GitHub Progress Updates (During Execution)

### Progress Update Checkpoints (MANDATORY)

Sub-agents MUST post updates at these points:

1. **Phase start**
2. **Task completion** (every 30-40% progress OR after major task)
3. **TDD checkpoint** (after invoking /TDD skill)
4. **Playwright test completion** (WITH screenshots)
5. **PR creation** (after EVERY task - see section 3)
6. **PR merge**
7. **Phase completion**

### Template: Phase Start

```bash
gh issue comment {issue-number} --body "🔨 **Phase {X.Y} Started**: {Phase name}

**Agent**: {agent-name}
**Status**: Starting implementation
**Progress**: 0%

**Tasks in this phase**:
1. {Task 1}
2. {Task 2}
3. {Task 3}

See execution log: docs/system/execution/phase{X.Y}-{topic}.md"
```

### Template: Task Completion / Progress Milestone

```bash
gh issue comment {issue-number} --body "📊 **Phase {X.Y} Progress Update**

**Agent**: {agent-name}

## Completed Tasks
- ✅ Task {N}: {Task name}
  - Implementation: {brief description}
  - Tests: {N} tests created/passing
  - Files: {list key files created/modified}
  - Verification: Build ✅, Tests ✅

## In Progress
- 🚧 Task {N+1}: {Task name}
  - Status: {specific status}
  - Blockers: {none or list}

## Next Steps
- ⏭️ Task {N+2}: {Task name}

## Test Summary
- Total tests: {N} ({X} passing, {Y} pending)
- All active tests passing: ✅ {N}/{N}
- Coverage: {key scenarios}

## Verification Evidence
\`\`\`bash
# Most recent verification
$ npm run build && npm run lint && npm test
{paste actual output}
\`\`\`

**Progress**: {percentage}% ({N} of {M} tasks complete)

See detailed log: docs/system/execution/phase{X.Y}-{topic}.md"
```

### Template: TDD Checkpoint

```bash
gh issue comment {issue-number} --body "🧪 **TDD Checkpoint - Phase {X.Y}**

**Agent**: {agent-name}
**Feature**: {Feature being tested}

## Red Phase
- ✅ Created failing test for {feature}
- Test file: \`{test-file-path}\`
- Expected behavior: {description}

## Status
- Test is watching for implementation
- Next: Write minimal code to make test pass (Green phase)

See execution log: docs/system/execution/phase{X.Y}-{topic}.md"
```

### Template: Playwright Tests Complete (WITH Screenshots)

**CRITICAL: Screenshots MUST be committed to repo and referenced via GitHub raw URLs**

```bash
# Step 1: Commit screenshots to repository FIRST
mkdir -p screenshots/phase-{X.Y}
cp ./test-results/screenshots/*.png screenshots/phase-{X.Y}/
git add screenshots/phase-{X.Y}/
git commit -m "test: add E2E screenshots for Phase {X.Y}"
git push

# Step 2: Post update with embedded images
gh issue comment {issue-number} --body "✅ **E2E Tests Passed - Phase {X.Y}**

**Agent**: {agent-name}

## Test Results
- ✅ All {N} tests passing
- Test file: \`tests/{test-file}.spec.js\`
- Duration: {duration}
- Coverage: {scenarios}

## Test Execution Output
\`\`\`
{paste actual npx playwright test output}
\`\`\`

## Screenshots

### {Scenario 1}
![{description}](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/screenshots/phase-{X.Y}/{screenshot1}.png)

### {Scenario 2}
![{description}](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/screenshots/phase-{X.Y}/{screenshot2}.png)

## Verification Evidence
- Build: exit 0 ✅
- Tests: {N}/{N} passed ✅

See full test report: docs/system/execution/phase{X.Y}-{topic}.md"
```

**Why GitHub raw URLs?**
- External collaborators viewing GitHub issues CANNOT see local file paths
- Repository-based approach with raw URLs is the ONLY way to automate screenshot posting via CLI
- Format: `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/screenshots/{filename}.png`

### Template: Phase Completion

```bash
gh issue comment {issue-number} --body "✅ **Phase {X.Y} Complete**

**Agent**: {agent-name}

## Verification
- [x] All tests passing ({N}/{N})
- [x] Build succeeds
- [x] Linting clean
- [x] E2E tests with screenshots posted
- [x] Documentation updated

**Progress**: 100% of Phase {X.Y}
**Overall Feature Progress**: {percentage}%

**Next**: {Next phase description or PR creation}

Updated: docs/system/execution/phase{X.Y}-{topic}.md"
```

---

## 3. Task-Level Status Updates

### Critical Rule

After completing a task, you MUST record status and verification evidence. This can be via GitHub issue comments or local execution docs, depending on how the maintainer runs the project.

### Why Task-Level Updates?

- **Continuous visibility**: Keeps maintainers informed
- **Easier reviews**: Smaller, focused changes
- **Early feedback**: Catch issues before moving forward
- **Clear attribution**: Each task tracked in history

### Task Verification Workflow

**Step 1: Verify Task Complete**

```bash
# Run verification commands (MANDATORY)
npm run build  # Must exit 0
npm run lint   # Must show 0 errors
npm test       # All tests passing (or npx playwright test for E2E)

# Verify screenshots uploaded (for test tasks)
ls screenshots/phase-{X.Y}/  # Should show all screenshots
```

**Step 2: Record Task Status**

You can either:

- Post a GitHub issue comment using the templates above, **or**
- Update the local execution docs (e.g. docs/system/execution/phaseX.Y-topic.md) with the same information.

### Task Status Checklist

**Before marking each task complete:**

- [ ] Task fully implemented
- [ ] All verification commands pass (build, lint, tests)
- [ ] Screenshots uploaded (if applicable)
- [ ] Commits follow message conventions
- [ ] Changes are focused on THIS task only
- [ ] Documentation updated for this task
- [ ] Execution log updated

**After updating status:**

- [ ] Status linked to GitHub issue (if using issues)
- [ ] Verification evidence included
- [ ] Links to INDEX and design docs (where applicable)
- [ ] Agent identification included

---

## 4. Feature Completion & Issue Closure

### Pre-Closure Update

Before closing issue, post final verification:

```bash
gh issue comment {issue-number} --body "🎉 **All Phases Complete**

**Agent**: {agent-name}

## Final Verification
- [x] All tests passing ({N}/{N})
- [x] Build succeeds
- [x] Linting clean
- [x] E2E tests complete with screenshots
- [x] Documentation updated
- [x] As-built documentation generated

**All task updates recorded**: {N}/{N}
"
```

### Close Issue After Merge

```bash
gh issue close {issue-number} --comment "✅ **Feature Completed**

**Agent**: {agent-name}
## Post-Merge Activities
- [x] As-built documentation generated
- [x] User-facing docs updated
-- [x] INDEX status set to 'merged'

## Final Stats
- Phases completed: {N}/{N}
-- Task updates recorded: {N}
- Tests added: {N}
- Files changed: {N}

**As-built doc**: [docs/system/as-builts/{feature}-as-built.md]

Feature complete! 🎉"
```

---

## 5. Agent Identification Requirements

### MANDATORY Rule

**Every GitHub interaction MUST include agent identification.**

### Where to Include Agent Name

1. **Issue creation**: In footer (`🤖 Created by {agent-name}`)
2. **Issue comments**: In header (`**Agent**: {agent-name}`)
3. **PR creation**: In footer (`🤖 Generated by {agent-name}`)
4. **PR merge comments**: In body (`**Agent**: {agent-name}`)

### Agent Name Format

Use the full agent name as defined in your agent configuration:

- `react-mui-frontend-engineer`
- `wiring-agent`
- `supabase-database-architect`
- `playwright-tester`
- `documentation-expert`
- `superpowers:code-reviewer`
- `Claude Code` (for orchestrator-level actions)

### Example with Agent Identification

```bash
gh issue comment 123 --body "📊 **Phase 1.2 Progress Update**

**Agent**: react-mui-frontend-engineer

## Completed Tasks
- ✅ Task 1: Created LeadsList component
...
"
```

---

## 6. Integration with Documentation Framework

### INDEX File Coordination

GitHub issue number MUST be recorded in INDEX frontmatter:

```yaml
---
github_issue: "#123"
feature_branch: "feature/desk-crm-leads"
pr_number: "#456"  # Filled after PR created
---
```

### Reading Issue Number from INDEX

Sub-agents should read the INDEX file to get the issue number:

```javascript
// Example: Read INDEX to get github_issue field
const indexPath = 'docs/system/INDEX-feature-name.md';
// Parse frontmatter to extract github_issue value
// Use that value in gh commands
```

### Execution Log References

All GitHub comments should reference the execution log:

```markdown
See detailed log: docs/system/execution/phase{X.Y}-{topic}.md
```

---

## 7. Common Pitfalls to Avoid

### ❌ Don't:

- Create issues without agent identification
- Post updates without agent name in header
- Skip task-level PRs (they are MANDATORY)
- Use local file paths for screenshots in issues
- Forget to commit screenshots before referencing them
- Close issues without final verification evidence
- Skip PR → issue linking

### ✅ Do:

- Always include `**Agent**: {agent-name}` in issue comments
- Create task PR after EVERY task completion
- Commit screenshots to repo and use GitHub raw URLs
- Link every PR to the GitHub issue with a comment
- Post merge confirmation after PR merges
- Update INDEX with issue/PR numbers
- Keep feature branch alive for multiple task PRs

---

## 8. Workflow Summary (Quick Reference)

```
Feature Start:
  1. Create GitHub issue (with agent ID)
  2. Create feature branch
  3. Update INDEX with issue number
  4. Post kickoff comment

During Execution:
  1. Post phase start comment (with agent ID)
  2. Post task completion updates (with agent ID)
  3. Post TDD checkpoints (with agent ID)
  4. Post Playwright results with screenshots (with agent ID)
  5. Create PR after EVERY task (with agent ID)
  6. Link PR to issue with comment (with agent ID)
  7. Post merge confirmation (with agent ID)
  8. Repeat for each task

Feature Completion:
  1. Post final verification to issue (with agent ID)
  2. Close issue with summary (with agent ID)
  3. Generate as-built documentation
  4. Delete feature branch
```

---

## 9. Skills Integration

This skill integrates with other skills:

- `/TDD` → Post TDD checkpoint to issue after Red phase
- `/VERIFY-BEFORE-COMPLETE` → Include verification evidence in PRs/comments
- `/systematic-debugging` → Reference debug document in issue updates
- `/brainstorming` → Document decisions in issue comments

---

## Skill Type: Rigid

This is a **rigid skill** - follow the templates and workflow exactly. GitHub coordination requires consistency for team-wide coordination and traceability.

---

**Last Updated**: 2026-01-30
**Version**: 1.0
**Skill Type**: Rigid
