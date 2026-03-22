---
name: commit
description: Run pre-commit validation before committing. Use for automated hooks, Terraform cleanup, or emoji reference. For simple commits, Claude's native capability suffices.
allowed-tools: Read, Bash(git:*), Bash(pre-commit:*), Bash(uv:*), Bash(pip:*), Bash(find:*), Bash(source:*), Bash(SKIP=*:*)
---

# Commit Skill

Run pre-commit validation and create well-formatted commits with conventional format.

## When to Use

- Pre-commit hooks needed
- Terraform files involved (needs cache cleanup)
- Want emoji reference for commit types

For simple commits without hooks: use Claude's native git capability.

## Usage

```
/commit              # Run pre-commit, then commit
/commit --no-verify  # Skip pre-commit hooks
```

## Project Rule

**No Co-Authored-By lines** - per CLAUDE.md, never include co-authoring footers.

## Workflow

### 1. Pre-commit Validation (unless --no-verify)

**Automatic setup** (silent, no user confirmation):
1. Clean Terraform temporary files:
   ```bash
   find . -type d \( -name ".terraform" -o -name ".terragrunt-cache" \) -exec rm -rf {} + 2>/dev/null
   find . -name ".terraform.lock.hcl" -delete 2>/dev/null
   ```
2. Create virtual environment if needed: `uv venv`
3. Install pre-commit: `uv pip install pre-commit`
4. Install hooks: `pre-commit install`

**Run validation**:
```bash
pre-commit run --all-files
```

If checks fail: analyze errors, provide recommendations, **stop commit process**.

### 2. Commit Format

`<emoji> <type>: <description>`

| Type | Emoji | Use Case |
|------|-------|----------|
| `feat` | ✨ | New feature |
| `fix` | 🐛 | Bug fix |
| `docs` | 📝 | Documentation |
| `refactor` | ♻️ | Code restructuring |
| `perf` | ⚡️ | Performance |
| `test` | ✅ | Tests |
| `chore` | 🔧 | Tooling/config |
| `ci` | 🚀 | CI/CD |
| `security` | 🔒️ | Security fixes |

See `references/emoji-guide.md` for full emoji list.

### 3. Create Commit

```bash
git commit -m "$(cat <<'EOF'
<emoji> <type>: <description>

[Optional body explaining why]
EOF
)"
```

## Pre-commit Failure Fixes

| Category | Fix |
|----------|-----|
| **Terraform validation** | Run `terraform init` in affected directories |
| **Formatting** | Re-run pre-commit (auto-fixes many issues) |
| **Security issues** | Manual review required |
| **KCL formatting** | Run `kcl fmt` in module directory |
| **YAML/JSON syntax** | Manual correction needed |
| **Large files** | Remove or use Git LFS |

**Stop commit process** until issues are resolved.

## Examples

```
✨ feat: add user authentication system
🐛 fix: resolve memory leak in rendering process
📝 docs: update API documentation with new endpoints
♻️ refactor: simplify error handling logic in parser
🔒️ fix: strengthen authentication password requirements
🚀 ci: add KCL validation to CI pipeline
🔧 chore: update Helm chart dependencies
```
