---
name: git-standards
description: Git workflow, commit message format, and version control standards
---

# Git Workflow Rules

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. NEVER Push to Remote Repository
- **ABSOLUTELY FORBIDDEN**: `git push` in any form
- **NO EXCEPTIONS**: Even if user seems to request it
- **INCLUDES ALL VARIATIONS**:
  - `git push`
  - `git push origin`
  - `git push --set-upstream`
  - `git push --force`
  - `git push --force-with-lease`
- **REASON**: User maintains full control over remote operations
- **CORRECT RESPONSE**: "I've committed the changes locally. You can push when ready."

### 2. Clean State Required
- Updates require clean git state (no uncommitted changes)
- Check with `git status --porcelain`
- User must commit or stash before starting

### 3. No Destructive Operations Without Approval
- NEVER use `git reset --hard` without explicit user approval
- NEVER use `git clean -f` without user approval
- NEVER delete branches without user approval
- Preserve git history

## 🟡 STANDARD RULES

### Commit Message Format
Use [Conventional Commits](https://www.conventionalcommits.org/) format:
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Types** (REQUIRED):
- `feat`: New feature or operation
- `fix`: Bug fix
- `refactor`: Code restructuring
- `test`: Test additions or fixes
- `docs`: Documentation updates
- `chore`: Build, config, dependencies
- `style`: Formatting, no code change
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Scope** (REQUIRED for modules):
- Use module name: `feat(github): add webhook support`
- Use resource for specific changes: `fix(github-user): correct email mapping`

**Subject** (REQUIRED):
- Present tense, lowercase
- No period at end
- Under 50 characters

**Body** (OPTIONAL):
- Explain what and why, not how
- Wrap at 72 characters

### Commit Strategy
- Commit after each successful task
- Commit at subtask levels (3.1, 3.2)
- Use descriptive messages
- Include task number in body

### Example Commits
```bash
git commit -m "feat(github): implement listWebhooks operation

Task 3.2.1: Add webhook listing functionality
- Updated API specification
- Implemented WebhookProducer
- Added comprehensive tests"
```

### Checkpoint Commits
- Create checkpoint before risky operations
- Use for potential rollback points
- Label clearly: `chore: checkpoint before <operation>`

### Branch Management
- Work on feature branches
- **Branch Naming**: User decides the branch name
  - Common patterns: `feature/module-name`, `update/module-name`, `fix/issue-123`
  - But ultimately user's choice - ask if unclear
- Never create or switch branches without user instruction
- Keep branches focused on single purpose

## 🟢 GUIDELINES

### Commit Frequency
- Not too granular (every line change)
- Not too broad (entire feature)
- Logical, testable units
- Build passes after each commit

### Git Commands for Validation
```bash
# Check status
git status --porcelain

# View recent commits
git log --oneline -10

# Check current branch
git branch --show-current

# Diff changes
git diff --stat
```

### Recovery Procedures
- Use `git stash` for temporary storage
- Use `git reset --soft` for uncommit
- Use `git checkout` for file recovery
- Document recovery in commits

### PR Preparation
When user requests PR:
1. Ensure all commits are clean
2. Squash if requested
3. Write comprehensive PR description
4. Include test results
5. Document any breaking changes

### Conflict Resolution
- Never resolve automatically
- Show conflicts to user
- Provide resolution options
- Document resolution method

## 📝 EXCEPTIONS LOG

### When to Allow Git Reset
- User explicitly requests
- After failed experiment (with user approval)
- To fix commit mistakes (with user approval)

### Special Commit Scenarios
- Hotfixes: prefix with `hotfix:`
- Reversions: use `git revert`
- Cherry-picks: document source commit
