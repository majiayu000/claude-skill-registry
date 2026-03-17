---
name: smart-commit
description: >
  Automates intelligent Git commits by analyzing unstaged/staged changes, grouping
  files by logical development concern, and committing sequentially with descriptive
  Conventional Commit messages. Includes pre-commit security audit protecting against
  credential leaks and large binary commits. Use when the user says "commit",
  "smart commit", "save changes", "push", "git commit", or similar.
compatibility: Requires git. Works with any agent that can run shell commands.
metadata:
  author: TheWatcher01
  version: "3.0.0"
---

# Smart Commit

Automated, security-aware Git commit workflow. Analyzes changes, groups files logically, and commits with clean Conventional Commit messages.

## Activation Triggers

Activate automatically (no confirmation needed) when the user says:

- "commit", "smart commit", "commiter", "drill baby drill", "push"
- "save changes", "push", "send to GitHub"
- "git commit", "commit all", "commit everything"

## Workflow

### Phase 1 — Security Audit

**MANDATORY before any commit.** Abort on critical findings.

```bash
# 1. Detect secrets and credentials (CRITICAL — block on match)
git diff --cached --name-only | xargs grep -rlE \
  '(PRIVATE KEY|password\s*=|api_key\s*=|secret\s*=|token\s*=|AWS_SECRET|sk-[a-zA-Z0-9]{20,})' \
  2>/dev/null

# 2. Check for sensitive file extensions
git status --porcelain | grep -iE '\.(env|pem|key|p12|pfx|jks|keystore|secret|credentials|htpasswd)$'

# 3. Detect large files (>10MB)
find . -not -path './.git/*' -not -path './node_modules/*' \
  -not -path './.venv/*' -not -path './vendor/*' \
  -size +10M -type f 2>/dev/null

# 4. Verify .gitignore covers essentials
# See references/security-checklist.md for full patterns
```

| Finding                             | Action                                                    |
| ----------------------------------- | --------------------------------------------------------- |
| Secrets/credentials detected        | **BLOCK** — alert user, never commit                      |
| `.env`, `.pem`, `.key` files staged | **BLOCK** — alert user, suggest `.gitignore`              |
| Large binaries (>50MB)              | **WARN** — suggest `.gitignore` or Git LFS                |
| Large files (10-50MB)               | **WARN** — ask user for confirmation                      |
| Missing `.gitignore` patterns       | **FIX** — add essential patterns, include in first commit |

> **NEVER auto-delete user files.** Only warn and suggest actions. File deletion is the user's decision.

### Phase 2 — Analyze Changes

```bash
git status --porcelain
```

Classify each file by its git status:

- `??` → new (untracked)
- `M` → modified
- `A` → added (staged)
- `D` → deleted
- `R` → renamed

### Phase 3 — Group by Concern

Group files into logical commits using **adaptive detection**. The agent MUST inspect the actual project structure — do not assume any framework.

**Grouping strategy** (priority order):

1. **Configuration** — Package manifests, lockfiles, config files, CI/CD, `.gitignore`
2. **Types/Schemas** — Type definitions, interfaces, schemas, models
3. **Libraries/Utils** — Shared code, helpers, utilities
4. **Core Logic** — Components, services, controllers, routes, pages
5. **Styles** — CSS, SCSS, Tailwind, theme files
6. **Tests** — Test files, test configs, fixtures
7. **Documentation** — Markdown, docs, changelogs
8. **Assets** — Images, fonts, static files
9. **Infrastructure** — Docker, Terraform, deployment configs

**Adaptive rules:**

- Inspect the actual directory tree to determine project type
- Group related files together (e.g., component + its test + its styles)
- If a feature touches <5 files across categories, consider a single feature commit
- For detailed patterns per framework, see [references/grouping-patterns.md](references/grouping-patterns.md)

### Phase 4 — Commit Sequentially

Commit in dependency order (config → types → libs → core → rest).

```bash
git add <files>
git commit -m "<type>(<scope>): <description>"
```

**Message format:** [Conventional Commits](https://www.conventionalcommits.org/)

| Type       | When                                     |
| ---------- | ---------------------------------------- |
| `feat`     | New feature or functionality             |
| `fix`      | Bug fix                                  |
| `docs`     | Documentation only                       |
| `style`    | Formatting, whitespace (no logic change) |
| `refactor` | Code restructuring (no behavior change)  |
| `test`     | Adding or updating tests                 |
| `chore`    | Build, config, dependencies, tooling     |
| `perf`     | Performance improvement                  |
| `ci`       | CI/CD configuration                      |

**Message rules:**

- Imperative mood: "add", "fix", "update" (not "added", "fixes")
- Scope is optional but recommended: `feat(auth): add login endpoint`
- Max 72 characters for subject line
- Be specific: `feat(ui): add accordion and badge components` not `feat: add stuff`
- Language: match the project's language convention (default: English)

### Phase 5 — Report & Push

After all commits:

```
✅ Smart Commit complete!

📦 N commits created:

1. chore: update dependencies
   → package.json, pnpm-lock.yaml

2. feat(ui): add button and dialog components
   → src/components/ui/button.tsx
   → src/components/ui/dialog.tsx

🔒 Security: No issues detected
🚀 Push to remote? (Y/n)
```

If user confirms, push to current tracked branch.

## Security Guidelines

> See [references/security-checklist.md](references/security-checklist.md) for the full checklist.

**Hard blocks (NEVER commit):**

- Private keys, API keys, tokens, passwords in code
- `.env` files with real credentials
- Database dumps (`.sql` with data)
- Certificate files (`.pem`, `.p12`, `.pfx`)

**Minimum `.gitignore` patterns:**

```gitignore
# Secrets
.env
.env.*
*.pem
*.key
*.p12

# Dependencies
node_modules/
.venv/
vendor/
__pycache__/

# Build outputs
dist/
build/
*.pyc

# OS files
.DS_Store
Thumbs.db

# Large media (adjust per project)
*.mp4
*.mov
*.zip
*.tar.gz
```

## Edge Cases

| Situation            | Action                                                                |
| -------------------- | --------------------------------------------------------------------- |
| No changes to commit | Report: "Working directory clean"                                     |
| Already staged files | Include in analysis, respect existing staging                         |
| Merge conflicts      | Alert user, abort until resolved                                      |
| Branch behind remote | Warn, suggest `git pull` first                                        |
| Detached HEAD        | Warn user, suggest creating a branch                                  |
| Empty repository     | Handle `git commit` with `--allow-empty` for initial commit if needed |
| Submodules changed   | Group as separate infrastructure commit                               |

## Customization

The skill adapts automatically to any project. For project-specific behavior:

- **Doc tracking**: If the project has `CHANGELOG.md`, suggest updating it
- **Monorepo**: Group by package/workspace, prefix scope with package name
- **Pre-commit hooks**: Respect existing `.pre-commit-config.yaml` or `husky` setup
- **Branch naming**: Follow existing branch conventions for any new branches

## Anti-Patterns

| Don't                        | Do Instead                                         |
| ---------------------------- | -------------------------------------------------- |
| `feat: add everything`       | Split into logical atomic commits                  |
| `update files`               | Describe WHAT changed specifically                 |
| Mix config + features        | Separate concerns into distinct commits            |
| Auto-delete user files       | Warn and suggest, let user decide                  |
| Commit secrets "temporarily" | **NEVER** — secrets in git history persist forever |
| Skip security audit          | **ALWAYS** run Phase 1, even for "quick" commits   |

## References

| File                                                                     | Contents                                 |
| ------------------------------------------------------------------------ | ---------------------------------------- |
| [references/security-checklist.md](references/security-checklist.md)     | Full pre-commit security audit checklist |
| [references/grouping-patterns.md](references/grouping-patterns.md)       | Framework-specific grouping patterns     |
| [references/conventional-commits.md](references/conventional-commits.md) | Conventional Commits quick reference     |
