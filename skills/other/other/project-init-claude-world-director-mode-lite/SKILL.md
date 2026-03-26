---
name: project-init
description: Expert-guided project setup with 6 phases
user-invocable: true
---

# Project Initialization

Execute a comprehensive project setup using Expert Agents.

---

## Phases

### Phase 1: Project Analysis

1. Check existing setup: `ls -la .claude/ CLAUDE.md`
2. Detect language and project type:

| File Found | Language | Framework Detection |
|---|---|---|
| `package.json` | Node.js/TypeScript | Check `dependencies` for react, express, next, etc. |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python | Check for django, flask, fastapi, etc. |
| `Cargo.toml` | Rust | Check `[dependencies]` section |
| `go.mod` | Go | Check module imports |
| `pom.xml` / `build.gradle` | Java/Kotlin | Check for spring, android, etc. |
| None of the above | Unknown | Ask user for tech stack |

3. Detect test framework: jest, pytest, cargo test, go test, etc.
4. Map project structure: `find . -type f \( -name "*.ts" -o -name "*.py" -o -name "*.rs" -o -name "*.go" \) | head -20`

**If no project files detected:**
```
This appears to be an empty or new project.
What tech stack would you like to use?
1. Node.js + TypeScript
2. Python
3. Go
4. Rust
5. Other (specify)
```

### Phase 2: CLAUDE.md Setup

Use the claude-md-expert agent to create project-specific CLAUDE.md:

```markdown
# [Project Name] - Project Instructions

## Overview
[Auto-detected from package.json description, README.md, or pyproject.toml]

## Tech Stack
- Language: [detected]
- Framework: [detected]
- Testing: [detected]

## Commands
- dev: [detected from scripts or Makefile]
- test: [detected test command]
- build: [detected build command]
- lint: [detected lint command]

## Development Policies
- Always write tests before implementation (TDD)
- Use conventional commits
- Document public APIs

## Available Commands
/workflow           # Full 5-step development
/auto-loop          # Autonomous TDD loop
/focus-problem      # Analyze problem
/test-first         # TDD cycle
/smart-commit       # Create commit
```

### Phase 3: MCP Configuration (Optional)

Check if MCP is useful for this project:

```bash
# Memory MCP (recommended for larger projects)
claude mcp add --scope project memory \
  -e MEMORY_FILE_PATH=./.claude/memory.json \
  -- npx -y @modelcontextprotocol/server-memory
```

**Skip if:** Small project, prototype, or user declines.

### Phase 4: Hooks Setup

Install the Auto-Loop stop hook for autonomous development:

```bash
# Verify hooks were installed
ls -la .claude/hooks/auto-loop-stop.sh

# If missing, copy from Director Mode Lite source:
# cp /path/to/director-mode-lite/hooks/auto-loop-stop.sh .claude/hooks/
# chmod +x .claude/hooks/auto-loop-stop.sh
```

Verify settings.local.json has the Stop hook configured:
```bash
cat .claude/settings.local.json | grep -A5 "Stop"
```

**If hooks are not configured:** Run the install script again or manually add the Stop hook entry to `.claude/settings.local.json`.

### Phase 5: Review Expert Agents

List available experts for reference:
- `claude-md-expert` - CLAUDE.md design patterns
- `mcp-expert` - MCP server configuration
- `agents-expert` - Custom agent creation
- `skills-expert` - Custom skill/command creation
- `hooks-expert` - Hook automation patterns

### Phase 6: Summary

Output completed setup:

```markdown
## Project Setup Complete

### Detected
- Language: TypeScript
- Framework: Express.js
- Testing: Jest

### Installed
- [x] CLAUDE.md created with project-specific config
- [x] Auto-Loop hooks configured
- [ ] MCP: skipped (optional)

### Next Steps
1. Review and customize `CLAUDE.md`
2. Run `/workflow` to start your first feature
3. Try `/auto-loop "your task"` for autonomous TDD
```

---

## Quick Mode

Minimal setup (skip MCP and expert review):
1. Phase 1: Analysis (detect language + framework)
2. Phase 2: Generate CLAUDE.md
3. Phase 4: Verify hooks
4. Phase 6: Summary with next steps

---

## Next Steps After Init

1. Review and customize `CLAUDE.md`
2. Run `/workflow` to start developing
3. Use `/auto-loop` for autonomous TDD
4. Run `/check-environment` if anything seems wrong
