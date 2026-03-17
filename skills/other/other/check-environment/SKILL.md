---
name: check-environment
description: Verify development environment is ready
user-invocable: true
---

# Environment Check

Verify your development environment is ready for Director Mode.

---

## Checks Performed

### 1. Essential Tools

| Tool | Purpose | Check |
|------|---------|-------|
| git | Version control | `git --version` |
| node | JavaScript runtime | `node --version` |
| npm/pnpm | Package manager | `npm --version` |

### 2. Claude Code Version

```bash
claude --version
```
Minimum: **2.0.0+**

### 3. Project Structure

- [ ] `package.json` exists
- [ ] `.gitignore` exists
- [ ] Source directory exists

### 4. Git Status

- [ ] Inside git repository
- [ ] Clean working tree
- [ ] On feature branch

---

## Output Format

```markdown
## Environment Check Results

### Essential Tools
- [x] git: 2.39.0
- [x] node: 20.10.0
- [x] pnpm: 8.12.0

### Claude Code
- [x] Version: 2.1.3 (up to date)

### Project Structure
- [x] package.json found
- [x] .gitignore found
- [x] src/ directory found

### Git Status
- [x] Git repository initialized
- [ ] Warning: 3 uncommitted changes

### Summary
**Status**: Ready (with warnings)
```

---

## Follow-up Actions

| Issue | Action |
|-------|--------|
| Missing git | Install git |
| Missing node | Install Node.js LTS |
| No package.json | Run `npm init` |
| Old Claude Code | Update Claude Code |
