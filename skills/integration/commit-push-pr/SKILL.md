---
name: commit-push-pr
description: |
  Boris Cherny Pattern 6: Commit changes, push to remote, create/update PR.
  Automates: git add -> git commit -> git push -> gh pr create.
  Terminal skill (pipeline endpoint) after /synthesis COMPLETE.
user-invocable: true
context: fork
model: opus
version: "3.1.0"
argument-hint: "[commit message] | --workload <slug>"
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000
  PreToolUse:
    - type: command
      command: "/home/palantir/.claude/hooks/git-safety-check.sh"
      timeout: 10000
      matcher: "Bash"

# EFL Pattern Configuration (Terminal Skill - Minimal)
agent_delegation:
  enabled: false
  reason: "Terminal skill - executes directly without delegation"

parallel_agent_config:
  enabled: false
  reason: "Git operations must be sequential"

internal_validation:
  enabled: true
  checks:
    - "Branch is not main/master"
    - "No sensitive files (.env, credentials) staged"
    - "Commit message follows convention"
  max_retries: 2

output_paths:
  l1: ".agent/prompts/{slug}/commit-push-pr/l1_summary.yaml"
  l2: ".agent/prompts/{slug}/commit-push-pr/l2_index.md"
---

# /commit-push-pr - Git Workflow Automation

> **Version:** 3.1.0 | **Type:** Terminal Skill
> **Role:** Commit, push, and create PR in one command
> **Pipeline:** After /synthesis COMPLETE (pipeline endpoint)

## 1. Purpose

Automates the complete git workflow:
1. Analyze staged/unstaged changes
2. Generate or use provided commit message
3. Stage and commit changes
4. Push with upstream tracking
5. Create/update pull request

## 2. Invocation

```bash
/commit-push-pr                              # Auto-generate message
/commit-push-pr "feat: Add auth module"      # Provide message
/commit-push-pr --workload <slug>            # Pipeline completion
```

## 3. L1/L2/L3 Output Format

### L1 Summary (returned to main context)

```yaml
taskId: commit-{timestamp}
agentType: commit-push-pr
status: success
summary: "Committed abc1234, pushed to origin/feature-branch, PR #123 created"

branch: "feature/auth-module"
commitHash: "abc1234"
filesChanged: 5
prUrl: "https://github.com/owner/repo/pull/123"

l2Path: .agent/prompts/{slug}/commit-push-pr/l2_index.md
requiresL2Read: false
nextActionHint: "Pipeline complete"
```

### L2 Report Structure

```markdown
# Commit Summary

**Branch:** feature/auth-module
**Commit:** abc1234
**Message:** feat: Add user authentication flow

## Files Changed
- src/auth/login.py (+42, -10)
- tests/test_auth.py (+25, -0)

## Push Status
Pushed to origin/feature/auth-module

## PR Status
PR #123 created: https://github.com/owner/repo/pull/123
```

## 4. Execution Strategy

### Phase 1: Analyze Changes

```bash
git status                    # View untracked and modified
git diff --cached             # View staged changes
git diff                      # View unstaged changes
git log --oneline -5          # Recent commits for style
```

### Phase 2: Stage and Commit

**Commit Message Format:**
```
<type>: <concise description>

<optional body explaining why>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:** feat, fix, refactor, docs, test, chore, style

### Phase 3: Push to Remote

```bash
git push -u origin $(git branch --show-current)
```

### Phase 4: Create/Update PR

```bash
# Check if PR exists
gh pr view --json state 2>/dev/null

# Create PR if none exists
gh pr create --title "<title>" --body "<body>"
```

## 5. Safety Validations

| Condition | Action |
|-----------|--------|
| Branch is main/master | WARN, ask confirmation |
| Committing .env files | BLOCK unless explicit |
| Committing credentials | BLOCK - security risk |
| Empty commit | SKIP - nothing to commit |

### P6: Git Safety Validation

```javascript
const gitSafetyChecks = {
  maxRetries: 2,
  checks: [
    "branch !== 'main' && branch !== 'master'",
    "!stagedFiles.some(f => f.includes('.env'))",
    "!stagedFiles.some(f => f.includes('credential'))",
    "commitMessage.match(/^(feat|fix|refactor|docs|test|chore|style):/)"
  ],
  onFailure: "BLOCK and prompt user for correction"
};
```

## 6. Pipeline Integration

```
/synthesis (COMPLETE)
    |
    +-- /commit-push-pr <-- THIS SKILL (Terminal)
            |
            +-- Pipeline terminates
```

### Upstream
- /synthesis with COMPLETE status

### Output
- No downstream skill (terminal)

## 7. Handoff Contract

```yaml
handoff:
  skill: "commit-push-pr"
  workload_slug: "{slug}"
  status: "completed"
  timestamp: "2026-01-28T14:35:00Z"
  next_action:
    skill: null
    arguments: null
    required: false
    reason: "Pipeline completed - changes committed and PR created"
```

## 8. Post-Compact Recovery

```javascript
if (isPostCompactSession()) {
  const slug = await getActiveWorkload();
  if (slug) {
    const lastCommit = await Bash("git log -1 --oneline");
    console.log(`Last commit: ${lastCommit}`);
  }
  // Continue with current git state
}
```

---

### Version History

| Version | Change |
|---------|--------|
| 3.1.0 | Cleaned duplicate blocks, normalized frontmatter |
| 3.0.0 | EFL Pattern integration, git-safety-check hook |
| 2.2.0 | Standalone execution, handoff contract |
| 2.1.0 | V2.1.19 spec compatibility |
| 1.1.1 | Initial git workflow automation |
