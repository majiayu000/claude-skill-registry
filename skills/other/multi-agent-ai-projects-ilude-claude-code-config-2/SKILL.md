---
name: multi-agent-ai-projects
description: Guidelines for multi-agent AI and learning projects with lesson-based structures. Activate when working with AI learning projects, experimental directories like .spec/, lessons/ directories, STATUS.md progress tracking, or structured learning curricula with multiple modules or lessons.
---

# Multi-Agent AI Projects

Guidelines for working with multi-agent AI learning projects and experimental codebases.

## CRITICAL: First Actions When Starting or Resuming Work

**Read STATUS.md FIRST** (usually `.spec/STATUS.md` or project root) - Shows current phase, completed lessons, blockers, and resume instructions. This prevents working on wrong lessons or repeating completed work.

Then:
1. Check git status
2. Verify dependencies installed
3. Check lesson-specific .env files

**Auto-activate when:** Project has `.spec/` directory, `lessons/` subdirectory, `STATUS.md`, or lesson-numbered directories.

## Project Structure Recognition

### Common Patterns
- `.spec/` directory - Learning specifications and experimental code
- `lessons/` or similar learning directories
- `STATUS.md` - Progress tracking for learning journey
- Per-lesson or per-module structure
- Self-contained lesson directories

### Typical Lesson Structure
```
lesson-XXX/
├── <name>_agent/          # Agent (agent.py, tools.py, prompts.py, cli.py)
├── .env                   # API keys (gitignored)
├── PLAN.md / README.md    # Lesson docs
├── COMPLETE.md            # Learnings
└── test_*.py              # Tests
```

## Workflow Patterns

### Execution
- Use `uv run python` from lesson directory
- Check lesson README for setup

### API Keys
- Per-lesson `.env` files (never commit)
- Check `.env.example` or `.env.template`

### Dependencies
- `uv sync --group lesson-XXX` for lesson-specific deps
- Check `pyproject.toml` for dependency groups

## Progress Tracking

### STATUS.md Pattern
- **Read before starting work** (most important!)
- Update after completing lessons
- Note blockers and next steps
- Document learnings and insights
- Track which lessons are complete

### Session Management
- **Always check STATUS.md at session start** (FIRST action)
- Update STATUS.md before ending sessions
- Note any experimental findings
- Document what worked and what didn't

## Common Project Types

### Learning Spike Projects
- Focus on exploration and experimentation
- Code may not be production-quality
- Documentation of learnings is important
- Test different approaches
- Iterate quickly

### Multi-Agent Frameworks
- Agent coordination patterns
- Tool usage and integration
- Message passing between agents
- State management across agents
- Router/coordinator patterns

## Quick Reference

**Execution:**
- `uv run python` from lesson directory
- Check per-lesson dependencies

**Documentation:**
- Update STATUS.md with progress
- Document findings in COMPLETE.md
- Note blockers and next steps

---

**Note:** These projects are learning-focused - prioritize understanding and documentation over production perfection. STATUS.md is your single source of truth for project state.
