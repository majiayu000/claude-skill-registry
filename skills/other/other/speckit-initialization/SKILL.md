---
name: speckit-initialization
description: |
  Ensures Spec-Kit-Plus workflow is properly initialized before autonomous builds.
  Use when: (1) /sp.autonomous fails to create directories, (2) .specify/ or .claude/
  is missing, (3) starting a fresh project, (4) "directory not found" errors during
  workflow. Provides directory structure creation and template copying patterns.
author: Claude Code (Claudeception)
version: 1.0.0
date: 2025-01-21
---

# Spec-Kit-Plus Initialization

## Problem

The `/sp.autonomous` command assumes directories already exist. When run on a fresh
project, it fails to create the required `.specify/` and `.claude/` directory
structures, causing the workflow to fail or behave unexpectedly.

## Context / Trigger Conditions

Use this skill when:
- Running `/sp.autonomous` on a new project with no existing structure
- Error: "directory not found" or "no such file or directory"
- Workflow state is inconsistent or corrupted
- `.specify/` or `.claude/` directories don't exist
- Starting any project that will use the autonomous workflow

## Solution

### CRITICAL RULES (NEVER VIOLATE)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  FORBIDDEN ACTIONS - NEVER DO THESE                                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  ✗ NEVER create: skill-lab/, workspace/, temp/, output/                   ║
║  ✗ NEVER create: .claude/ inside another directory                        ║
║  ✗ NEVER overwrite existing .claude/skills/ contents                      ║
║  ✗ NEVER ignore existing directories - USE them                           ║
║  ✗ NEVER regenerate skills that already exist                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Step 1: Check What ALREADY EXISTS

```bash
# Check BEFORE doing anything
CLAUDE_EXISTS="false"
SPECIFY_EXISTS="false"
SKILL_COUNT=0

if [ -d ".claude" ]; then
    CLAUDE_EXISTS="true"
    SKILL_COUNT=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l)
    echo "✓ .claude/ exists with $SKILL_COUNT skills - WILL USE IT"
fi

if [ -d ".specify" ]; then
    SPECIFY_EXISTS="true"
    echo "✓ .specify/ exists - WILL USE IT"
fi
```

### Step 2: Create ONLY Missing Directories

```bash
# Only create .specify if it doesn't exist
if [ "$SPECIFY_EXISTS" = "false" ]; then
    mkdir -p .specify/templates
    mkdir -p .specify/validations
    mkdir -p .specify/features
fi

# Only create .claude if it doesn't exist
if [ "$CLAUDE_EXISTS" = "false" ]; then
    mkdir -p .claude/skills
    mkdir -p .claude/agents
    mkdir -p .claude/commands
    mkdir -p .claude/rules
    mkdir -p .claude/logs
    mkdir -p .claude/build-reports
fi
```

### Step 3: Initialize Workflow State

```bash
cat > .specify/workflow-state.json << 'EOF'
{
  "phase": 0,
  "status": "initialized",
  "project_type": "unknown",
  "timestamp": "2025-01-21T00:00:00Z",
  "features": [],
  "completed_phases": []
}
EOF
```

### Step 4: Copy Template (If Available)

```bash
TEMPLATE_DIR="/path/to/template/repo"

# Copy all configurations
cp -r "$TEMPLATE_DIR/.claude/skills/"* .claude/skills/ 2>/dev/null || true
cp -r "$TEMPLATE_DIR/.claude/agents/"* .claude/agents/ 2>/dev/null || true
cp -r "$TEMPLATE_DIR/.claude/rules/"* .claude/rules/ 2>/dev/null || true
cp -r "$TEMPLATE_DIR/.claude/commands/"* .claude/commands/ 2>/dev/null || true
cp "$TEMPLATE_DIR/CLAUDE.md" ./ 2>/dev/null || true
cp "$TEMPLATE_DIR/.mcp.json" ./ 2>/dev/null || true
```

## Verification

After initialization, verify:

```bash
# Check directories exist
ls -la .specify/
ls -la .claude/

# Check workflow state
cat .specify/workflow-state.json

# Check skill count
find .claude/skills -name "SKILL.md" | wc -l
```

Expected output:
- `.specify/` contains: templates/, validations/, features/, workflow-state.json
- `.claude/` contains: skills/, agents/, commands/, rules/, logs/
- Skill count should be > 0 if template was copied

## Commands

| Command | Purpose |
|---------|---------|
| `/q-init` | Initialize project structure |
| `/q-reset` | Reset workflow state |
| `/q-status` | Check current state |
| `/sp.autonomous` | Full autonomous build |

## Notes

- Always run `/q-init` BEFORE `/sp.autonomous` on fresh projects
- The sp.autonomous command now includes Phase 0.0 that auto-initializes
- If copying from template, ensure paths are correct for your system
- MCP servers in `.mcp.json` may need path adjustments

## Root Cause

The original `/sp.autonomous` command had Phase 0 (PRE-CHECK) that only checked
if directories existed but didn't create them. This was fixed by adding Phase 0.0
(INITIALIZATION) that creates directories if they don't exist.

## Prevention

Always include initialization logic at the start of autonomous workflows:
1. Check if structure exists
2. Create if missing
3. Then proceed with detection/resume logic
