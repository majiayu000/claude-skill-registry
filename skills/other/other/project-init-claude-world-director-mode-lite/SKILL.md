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

1. Check existing setup: `ls -la .claude/`
2. Detect language (package.json, requirements.txt, Cargo.toml, go.mod)
3. Detect framework from dependencies
4. Map project structure

### Phase 2: CLAUDE.md Setup

Read `.claude/agents/claude-md-expert.md` and create project-specific CLAUDE.md:

```markdown
# [Project Name] - Project Instructions

## Overview
[Auto-detected from package.json or README]

## Tech Stack
- Language: [detected]
- Framework: [detected]

## Commands
- dev: [detected]
- test: [detected]
- build: [detected]
```

### Phase 3: MCP Configuration

**Essential MCP:**
```bash
claude mcp add --scope project memory -e MEMORY_FILE_PATH=./.claude/memory.json -- npx -y @modelcontextprotocol/server-memory
```

### Phase 4: Hooks Setup

Create Auto-Loop stop hook in `.claude/hooks/`

### Phase 5: Review Expert Agents

List available experts for reference:
- `claude-md-expert.md` - CLAUDE.md design
- `mcp-expert.md` - MCP configuration
- `agents-expert.md` - Custom agents
- `skills-expert.md` - Custom skills
- `hooks-expert.md` - Automation hooks

### Phase 6: Summary

Output completed setup and next steps.

---

## Quick Mode

Minimal setup (skip MCP and expert review):
1. Phase 1: Analysis
2. Phase 2: Basic CLAUDE.md
3. Phase 4: Auto-Loop hook

---

## Next Steps After Init

1. Review and customize `CLAUDE.md`
2. Run `/workflow` to start developing
3. Use `/auto-loop` for autonomous TDD
