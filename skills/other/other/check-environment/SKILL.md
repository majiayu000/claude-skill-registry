---
name: check-environment
description: Verify development environment is ready
user-invocable: true
---

# Environment Check

Verify your development environment is ready for Director Mode.

---

## Checks Performed

### 1. Director Mode Dependencies

| Tool | Purpose | Check | Required |
|------|---------|-------|----------|
| git | Version control | `git --version` | Yes |
| python3 | Hook config merging (install.sh) | `python3 --version` | Yes |
| jq | JSON processing in hooks | `jq --version` | Yes |

### 2. Claude Code Version

```bash
claude --version
```
Minimum: **2.0.0+**

### 3. Project-Specific Tools

Auto-detect project type and check relevant tools:

| Project Type | Detected By | Tools to Check |
|---|---|---|
| Node.js | `package.json` | `node --version`, `npm --version` or `pnpm --version` |
| Python | `requirements.txt`, `pyproject.toml` | `python3 --version`, `pip --version` |
| Rust | `Cargo.toml` | `rustc --version`, `cargo --version` |
| Go | `go.mod` | `go version` |
| Java | `pom.xml`, `build.gradle` | `java --version`, `mvn --version` or `gradle --version` |

### 4. Director Mode Installation

- [ ] `.claude/` directory exists
- [ ] `.claude/skills/` populated (31 skills expected)
- [ ] `.claude/agents/` populated (14 agents expected)
- [ ] `.claude/hooks/` populated (5 hook scripts expected)
- [ ] `.claude/settings.local.json` has hooks configured
- [ ] `CLAUDE.md` exists

### 5. Git Status

- [ ] Inside git repository
- [ ] Clean working tree (or note uncommitted changes)

---

## Output Format

```markdown
## Environment Check Results

### Director Mode Dependencies
- [x] git: 2.39.0
- [x] python3: 3.11.0
- [x] jq: 1.7

### Claude Code
- [x] Version: 2.1.76

### Project Tools (Node.js detected)
- [x] node: 20.10.0
- [x] pnpm: 8.12.0

### Director Mode Installation
- [x] .claude/ directory exists
- [x] 31 skills installed
- [x] 14 agents installed
- [x] 5 hooks installed
- [x] settings.local.json configured
- [x] CLAUDE.md exists

### Git Status
- [x] Git repository initialized
- [ ] Warning: 3 uncommitted changes

### Summary
**Status**: Ready
```

---

## Follow-up Actions

| Issue | Action |
|-------|--------|
| Missing python3 | Install Python 3: `brew install python3` (macOS) or `apt install python3` (Linux) |
| Missing jq | Install jq: `brew install jq` (macOS) or `apt install jq` (Linux) |
| Missing git | Install git for your OS |
| Missing node | Install Node.js LTS: https://nodejs.org |
| Old Claude Code | Run `claude update` |
| No .claude/ | Run install script: `./install.sh .` |
| Hooks not configured | Re-run install or check `.claude/settings.local.json` |
| No CLAUDE.md | Run `/project-init` or `/claude-md-template` |
