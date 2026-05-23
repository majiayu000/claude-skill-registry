---
name: git-ops
description: Safe git operations including commits, branches, merges, worktrees, and conflict resolution. Use when user wants to commit and push changes, manage branches, resolve conflicts, or create isolated workspaces. Activates when user says "commit", "push", "merge", "branch", "pull", "rebase", "worktree", "conflict", or similar git workflow requests.
---

# Git Operations

**Stage all changes, create conventional commits, manage branches safely, and resolve conflicts with systematic approaches.**

## When to Use

Automatically activate when the user:
- Explicitly asks to commit and push ("commit and push", "push these changes")
- Mentions saving work to remote ("save to github", "push to remote")
- Needs to create or manage branches ("create a feature branch", "switch branches")
- Encounters merge conflicts ("fix conflicts", "resolve merge")
- Wants isolated workspace for parallel work ("create worktree for feature X")
- Asks to finish development ("finish this branch", "complete development")
- Mentions rebasing, pulling, or other git operations

## What It Does

### 1. Commit and Push Workflow
- Stages all changes
- Generates conventional commit message (or uses provided message)
- Pushes to remote branch (with -u for new branches)
- Shows PR link for GitHub repos
- Validates before each step

### 2. Branch Management
- Create feature branches from latest main
- List and manage active branches
- Delete branches safely (with verification)
- Switch between branches
- Rename branches

### 3. Merge and Rebase
- Merge branches with conflict detection
- Rebase with safety checks
- Handle merge conflicts systematically
- Preview changes before merge/rebase

### 4. Isolated Worktrees
- Create parallel workspaces for simultaneous development
- Automatically verify .gitignore configuration
- Setup development environment in worktree
- List and manage active worktrees
- Clean up worktrees after completion

### 5. Conflict Resolution
- Identify conflicted files
- Show conflict markers
- Guide manual resolution
- Verify resolution before commit

## Approach

### Smart Commit Message Generation

When user doesn't provide a message, analyze staged changes to generate conventional commit:

**Steps:**
1. Analyze changed files (`git diff --cached --name-only`)
2. Determine commit type:
   - `feat`: New feature (default)
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `test`: Test updates
   - `chore`: Dependencies, config changes
   - `refactor`: Code restructuring
3. Extract scope from directory/component (first changed file path)
4. Generate description in imperative mood ("Add", not "Added")
5. Keep under 90 characters

**Example analysis:**
```
Changed: src/auth/login.ts, src/auth/password.ts
Type: feat
Scope: auth
Message: feat(auth): add password reset functionality
```

### Worktree Safety

**Critical verification for project-local worktrees:**

1. Check if worktree directory is in `.gitignore`
2. If NOT in `.gitignore`:
   - Add pattern: `.worktrees/` or `worktrees/`
   - Commit immediately
   - Then proceed
3. This prevents accidental commits of worktree contents

**Process:**
```bash
# Verify .gitignore
if ! grep -q "^\.worktrees/$\|^worktrees/$" .gitignore; then
  echo ".worktrees/" >> .gitignore
  git add .gitignore
  git commit -m "chore: add worktree directory to gitignore"
fi

# Create worktree
git worktree add .worktrees/feature-name -b feature/feature-name
```

### Conflict Resolution Strategy

1. **Identify conflicts**: Run `git status` to list conflicted files
2. **Show markers**: Display conflict markers with context
3. **Guide resolution**: Explain each side of conflict
4. **Verify**: Check file has no remaining markers
5. **Stage and commit**: Add resolved file and complete merge

## Example Interactions

### Simple Commit and Push
```
User: "Push these changes"

Skill:
1. Runs git status to see changes
2. Stages all with git add .
3. Analyzes diff to generate message
4. Commits with: feat(auth): add login endpoint
5. Pushes with git push
6. Shows: "Successfully pushed to origin/feature-x"
```

### Creating Feature Branch with Worktree
```
User: "Set up a worktree for the authentication feature"

Skill:
1. Verifies .worktrees/ in .gitignore (adds if needed)
2. Creates: git worktree add .worktrees/auth -b feature/auth
3. Runs: cd .worktrees/auth && npm install
4. Runs tests to verify clean baseline
5. Reports: "Ready to work in .worktrees/auth/"
```

### Resolving Merge Conflict
```
User: "Fix the conflicts"

Skill:
1. Identifies conflicted files: git status
2. Shows markers with context
3. Guides through each conflict
4. User resolves in editor
5. Verifies no remaining markers
6. Stages and completes merge
```

## Tools Used

- **bash scripts**: Smart commit message generation, worktree management
- **git commands**: All core git operations with safety validation
- **gh cli**: GitHub-specific operations (PR creation, branch management)
- **Read/Write**: Verify .gitignore, update configuration
- **Bash evaluation**: Execute git commands with error handling

## Success Criteria

- ✅ All changes committed with meaningful message
- ✅ Commits follow conventional commit format
- ✅ Changes pushed successfully to remote
- ✅ New branches created with `-u` flag
- ✅ No local changes remain after push
- ✅ Worktree directory verified in .gitignore
- ✅ Merge conflicts resolved completely
- ✅ Pre-commit validation prevents errors
- ✅ PR link shown for GitHub repos
- ✅ User understands next steps

## Integration

Works well with:
- **feature-planning**: Commits implementation tasks after planning
- **test-fixing**: Commits test fixes automatically
- **code-review**: Commits feedback implementation
- **branch-management**: Integrates with branch workflows

## Safe Operations Checklist

✅ Always run `git status` first  
✅ Review changes before committing  
✅ Use `git diff` to preview  
✅ Verify branch before pushing  
✅ Use `git push -u` for new branches  
✅ Confirm before destructive operations  
✅ Test in isolated worktree when risky  
✅ Keep commits atomic and focused  

## Common Patterns

### Commit and Push in One Step
```bash
bash scripts/smart_commit.sh
```

### Commit with Custom Message
```bash
bash scripts/smart_commit.sh "feat(api): add user endpoint"
```

### Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Create Worktree for Development
```bash
git worktree add .worktrees/feature-name -b feature/feature-name
cd .worktrees/feature-name
npm install  # or appropriate setup
```

### Finish Development Branch
```bash
# Option 1: Merge locally
git checkout main
git pull
git merge feature/your-feature
npm test
git push

# Option 2: Create PR
git push -u origin feature/your-feature
gh pr create --title "feat: description"

# Clean up worktree (if used)
git worktree remove .worktrees/feature-name
```
