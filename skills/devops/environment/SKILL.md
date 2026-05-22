---
name: environment
description: Understanding and maintaining the development environments for this thesis project. Use for environment architecture, troubleshooting, or modifying environment setup.
---

# Environment Skill

**When to use this skill**:
- You need to understand the environment architecture (for troubleshooting, modifications, or curiosity)
- You're modifying or extending the environment setup
- You encounter environment-related errors and need deeper context than error messages provide

**When NOT to use this skill**:
- Normal thesis work (build, test, commit) - error messages explain limitations
- You encounter a "local devcontainer only" error - the error message is sufficient

---

## Environment Architecture

This project supports two environments:

### 1. Local Devcontainer (Jörn's machine)
- **Defined by**: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `scripts/devcontainer-post-create.sh`
- **What it does**: Pre-installs all dependencies (TexLive, Rust, Python, Node.js, etc.) in a Docker image
- **Special features**:
  - Bind mounts for cache persistence (`/srv/devhome/*` → `/home/vscode/*`)
  - Worktrees support (`/workspaces/worktrees` for git worktree isolation)
  - Shared Rust build cache via `CARGO_TARGET_DIR=/workspaces/worktrees/shared/target`

### 2. Claude Code Web Environment
- **Defined by**: Ubuntu 24.04 base with pre-installed language runtimes (see Claude Code docs)
- **What it does**: Provides a clean environment accessible from anywhere via web browser
- **What's pre-installed**: Rust, Python (with uv), Node.js, Git, build-essential
- **What's NOT pre-installed**: TexLive, latexml
- **Key difference**: No devcontainer files run, no bind mounts, no worktrees directory

**Critical limitation (known bug as of Jan 2026):**
- apt-get does NOT work in web environment (DNS blocked by proxy architecture)
- See: [GitHub issue #14538](https://github.com/anthropics/claude-code/issues/14538)
- **Consequence**: TexLive cannot be installed, LaTeX builds are local-only
- **What works**: cargo, uv/pip, npm (HTTP proxy compatible)
- **What doesn't work**: apt-get, dpkg, any system packages

---

## Dependency Installation

### Progressive Disclosure Strategy

**Level 1: Error messages explain the situation**
- Build/lint scripts check for dependencies and print clear errors
- Example: `pdflatex not found (TexLive is local devcontainer only)`

**Level 2: This skill (understanding)**
- Explains environment architecture
- Documents conventions for modifications

**Level 3: Detailed implementation**
- Devcontainer config files (`.devcontainer/*`)
- Reference docs in `references/` subdirectory (if any)

### What's Available Where

| Dependency | Local Devcontainer | Web Environment |
|------------|-------------------|-----------------|
| TexLive (pdflatex, chktex) | Pre-installed in Dockerfile | NOT available (apt-get blocked) |
| latexml | Pre-installed in Dockerfile | NOT available (apt-get blocked) |
| Rust (cargo, rustc) | Pre-installed | Pre-installed |
| Python + uv | Pre-installed | Pre-installed |
| Python packages | `uv sync --extra dev` | `uv sync --extra dev` |

---

## Conventions for Modifying Environments

When you need to add dependencies or modify environment setup:

### 1. Document with Progressive Disclosure
- **CLAUDE.md**: Add one-line note to Environment Dependencies section
- **This skill**: Explain architecture changes if significant
- **Config files**: Keep comments factual, avoid speculation

### 2. Install Script Conventions
If you create install scripts:
- Make scripts idempotent (check before installing)
- Print helpful messages about time/disk usage
- Support `--help` flag
- Point build/lint scripts to install script in error messages

### 3. Never Make False Claims
- Future agents will believe documentation literally
- Example: Don't call a 2GB install "slim"
- Example: Don't say "everywhere" when you mean "in local devcontainer"
- When uncertain, be explicit about what you don't know

### 4. Keep It Simple (KISS)
- Follow standard patterns (cargo, npm, pip/uv; apt-get in local only)
- Don't over-engineer for hypothetical future requirements
- Don't add noise to config files that agents don't need

### 5. Maintain Both Environments
- **Local devcontainer**: Bake dependencies into Dockerfile when reasonable
- **Web environment**: Only cargo/uv/npm work (no apt-get due to DNS bug)
- Test changes in both environments (or document what's untested)

### 6. DRY - Don't Repeat Yourself
- Information should live in ONE canonical place
- Link to that place rather than duplicating
- Exception: Error messages can repeat key info (like "local devcontainer only") for convenience

---

## Common Tasks

### Detecting Which Environment You're In
```bash
# Web environment has this variable
if [[ -n "${CLAUDE_CODE_REMOTE:-}" ]]; then
  echo "Running in web environment"
else
  echo "Running in local environment (or other)"
fi
```

### Adding a New Dependency

**For Python packages** (works in both environments):
1. Add to `packages/python_viterbo/pyproject.toml`
2. Run `uv sync --extra dev`

**For system dependencies** (local devcontainer only):
1. Add to `.devcontainer/Dockerfile`
2. Update build scripts to fail gracefully with clear error in web environment
3. **Update CLAUDE.md**: Add one line to Environment Dependencies section

### Fixing Environment-Specific Issues

Example: Rust builds depend on `CARGO_TARGET_DIR=/workspaces/worktrees/shared/target` in local, but that dir doesn't exist in web.

**Approach**:
1. Identify the constraint (worktrees mount only exists in local)
2. Make it environment-aware (unset CARGO_TARGET_DIR in web, or create dir)
3. Document the difference in this skill if non-obvious
4. Test both environments

---

## Files to Read

- `.devcontainer/Dockerfile` - What's baked into local devcontainer image
- `.devcontainer/devcontainer.json` - Local devcontainer configuration
- `scripts/devcontainer-post-create.sh` - Local environment initialization
- `.claude/CLAUDE.md` - Top-level environment guidance for agents
