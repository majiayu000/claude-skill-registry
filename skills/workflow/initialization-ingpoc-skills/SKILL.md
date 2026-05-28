---
name: initialization
description: "Use when starting a new session without feature-list.json, setting up project structure, or breaking down requirements into atomic features. Load in INIT state. Detects project type (Python/Node/Django/FastAPI), creates feature-list.json with priorities, initializes .claude/progress/ tracking."
keywords: init, setup, features, breakdown, project-detection, requirements
---

# Initialization

Project setup and feature breakdown for INIT state.

## Execution Order (MANDATORY)

**Follow this exact sequence. Do NOT skip steps.**

### Step 1: Global Setup (once per machine)

```bash
# Check if global CLAUDE.md exists
[ -f ~/.claude/CLAUDE.md ] || ~/.claude/skills/initialization/scripts/global-init.sh
```

### Step 2: Global Hooks (once per machine)

```bash
# Check and install global hooks
[ -x ~/.claude/hooks/verify-state-transition.py ] || \
    ~/.claude/skills/global-hook-setup/scripts/setup-global-hooks.sh
```

**IMPORTANT**: Load `global-hook-setup` skill if hooks missing.

### Step 3: MCP Servers (once per project)

```bash
# Check and install MCP servers
[ -d mcp/token-efficient-mcp ] || \
    ~/.claude/skills/mcp-setup/scripts/setup-all.sh --non-interactive
```

**IMPORTANT**: Load `mcp-setup` skill if MCP missing.

### Step 4: Project Structure

```bash
~/.claude/skills/initialization/scripts/init-project.sh
```

Creates:

- `.claude/config/project.json` - Project settings
- `.claude/progress/state.json` - State (transitions to INIT)
- `CLAUDE.md` - Project documentation
- `.claude/CLAUDE.md` - Quick reference

### Step 5: Project Hooks (once per project)

```bash
# Check and install project hooks
[ -x .claude/hooks/verify-tests.py ] || \
    ~/.claude/skills/project-hook-setup/scripts/setup-project-hooks.sh --non-interactive
```

**IMPORTANT**: Load `project-hook-setup` skill if hooks missing.

### Step 6: Check Dependencies

```bash
~/.claude/skills/initialization/scripts/check-dependencies.sh
```

Fix any errors before proceeding.

### Step 7: Create Feature List

- Analyze user requirements
- Break down into atomic features (INVEST criteria)
- Create `.claude/progress/feature-list.json`

```bash
~/.claude/skills/initialization/scripts/create-feature-list.sh
```

### Step 8: Initialize Progress

```bash
~/.claude/skills/initialization/scripts/init-progress.sh
```

### Step 9: Verify INIT Complete

```bash
~/.claude/skills/initialization/scripts/verify-init.sh
```

**Must pass all 14 checks before transitioning to IMPLEMENT.**

---

## CLAUDE.md Hierarchy

| File | Scope | Purpose |
|------|-------|---------|
| `~/.claude/CLAUDE.md` | Global | User preferences, skill enforcement |
| `CLAUDE.md` | Project | Project documentation (100-300 lines) |
| `.claude/CLAUDE.md` | Local | Quick reference (<50 lines) |

## Exit Criteria (Code Verified)

```bash
# Project structure initialized
[ -f "CLAUDE.md" ]                      # Project documentation created
[ -f ".claude/CLAUDE.md" ]              # Quick reference created
[ -f ".claude/config/project.json" ]    # Project config
[ -d ".claude/progress/" ]               # Tracking directory

# Feature list created
[ -f ".claude/progress/feature-list.json" ]
jq '.features | length > 0' .claude/progress/feature-list.json
jq '.features[0] | has("id", "description", "priority", "status")' .claude/progress/feature-list.json

# Dependencies verified
scripts/check-dependencies.sh --quiet

# Hooks installed
[ -x "~/.claude/hooks/verify-state-transition.py" ]  # Global hooks
[ -x ".claude/hooks/verify-tests.py" ]                 # Project hooks
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/global-init.sh` | One-time setup for ~/.claude/CLAUDE.md (global preferences) |
| `scripts/init-project.sh` | Initialize .claude/ structure, generate CLAUDE.md files |
| `scripts/detect-project.sh` | Detect Python/Node/Django/etc |
| `scripts/check-dependencies.sh` | Verify MCP, env vars, services, ports |
| `scripts/create-init-script.sh` | Generate init.sh for dev server |
| `scripts/create-feature-list.sh` | Generate feature-list.json |
| `scripts/init-progress.sh` | Initialize .claude/progress/ |
| `scripts/verify-init.sh` | Verify all INIT criteria met |

## References

| File | Load When |
|------|-----------|
| references/feature-breakdown.md | Breaking down requirements |
| references/project-detection.md | Detecting project type |
| references/mvp-feature-breakdown.md | MVP-first tiered feature generation (10/30/200) |

## Assets

| File | Purpose |
|------|---------|
| templates/CLAUDE.project.template.md | Template for CLAUDE.md (project root) |
| templates/CLAUDE.local.template.md | Template for .claude/CLAUDE.md (quick reference) |
| templates/framework-templates/*.md | Framework-specific content (python, node, rust, go) |
| assets/feature-list.template.json | Template for new feature lists |
