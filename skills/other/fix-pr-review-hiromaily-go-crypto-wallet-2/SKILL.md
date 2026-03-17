---
name: fix-pr-review
description: Address PR review comments by selecting appropriate skills based on modified files. Use when fixing review feedback on pull requests.
---

# Fix PR Review Workflow

Workflow for addressing review comments on pull requests.

## Prerequisites

- PR number is required
- Use `git-workflow` Skill for commit conventions

## Process Overview

```
1. Fetch PR details
2. Get review comments
3. Classify by file type
4. Load appropriate development skill
5. Fix each comment
6. Run verification
7. Push changes
```

## Step 1: Fetch PR Information

```bash
# Get PR details
gh pr view {pr_number}

# Get PR diff to see modified files
gh pr diff {pr_number} --name-only

# Get review comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

## Step 2: Classify by Modified Files

| Files Modified | Development Skill |
|----------------|-------------------|
| `internal/`, `pkg/`, `cmd/`, `*.go` | `go-development` |
| `apps/ripple-lib-server/`, `*.ts` | `typescript-development` |
| `apps/erc20-token/contracts/`, `*.sol` | `solidity-development` |
| `scripts/`, `*.sh` | `shell-scripts` |
| `Makefile`, `make/*.mk` | `makefile-update` |
| `tools/atlas/`, `*.sql`, `*.hcl` | `db-migration` |
| `docs/`, `*.md` | `docs-update` |

## Step 3: Load Development Skill

Based on classification, load the appropriate skill:

| Skill | Path |
|-------|------|
| Go | `.claude/skills/go-development/SKILL.md` |
| TypeScript | `.claude/skills/typescript-development/SKILL.md` |
| Solidity | `.claude/skills/solidity-development/SKILL.md` |
| Shell | `.claude/skills/shell-scripts/SKILL.md` |
| Makefile | `.claude/skills/makefile-update/SKILL.md` |
| Database | `.claude/skills/db-migration/SKILL.md` |
| Docs | `.claude/skills/docs-update/SKILL.md` |

## Step 4: Address Comments

### Priority Order

1. **Security** - Address security concerns first
2. **Functionality** - Fix bugs or logic issues
3. **Code Quality** - Style, naming, documentation

### Comment Categories

| Category | Action |
|----------|--------|
| Bug fix requested | Fix the issue, add test if applicable |
| Refactoring suggestion | Apply if improves readability |
| Style/naming | Follow project conventions |
| Documentation | Add/update comments |
| Question | Respond in code comment or PR |

## Step 5: Run Verification

Run verification commands from the loaded development skill:

### Go Files

```bash
make go-lint && make tidy && make check-build && make gotest
```

### TypeScript Files

```bash
cd apps/ripple-lib-server && npm run lint && npm run build && npm test
```

### Shell Scripts

```bash
make shfmt
```

### Multiple Languages

If PR modifies multiple file types, run all applicable verification commands.

## Step 6: Commit and Push

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
fix(scope): address PR review comments

- Fix: [specific fix 1]
- Fix: [specific fix 2]
- Update: [update description]
EOF
)"

# Push to update PR
git push
```

## Common Review Patterns

### Error Handling (Go)

**Review comment**: "Missing error context"

```go
// Before
return err

// After
return fmt.Errorf("failed to create wallet: %w", err)
```

### Logging Security

**Review comment**: "Don't log sensitive data"

```go
// Before
log.Info("Processing key", "key", privateKey)

// After
log.Info("Processing key", "keyID", keyID)
```

### Code Duplication

**Review comment**: "Extract to helper function"

```go
// Before: Duplicated code in multiple places

// After: Create helper function
func helperFunction(params) result {
    // extracted logic
}
```

## Related Skills

- `go-development` - Go code changes
- `typescript-development` - TypeScript changes
- `shell-scripts` - Shell script changes
- `git-workflow` - Branch and commit workflow
