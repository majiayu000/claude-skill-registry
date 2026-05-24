---
name: two-agent-harness
description: This skill sets up a complete two-agent development system based on the "Effective Harnesses for Long-Running Agents" research. It creates initializer-agent (for project planning) and coding-agent (for incremental implementation), along with enforcement hooks and progress tracking infrastructure. Use when users ask to "set up two-agent system", "install agent harness", "configure Opus delegation", or want to implement the two-agent architecture pattern.
---

# Two-Agent Harness System Setup

This skill installs a complete two-agent development architecture that separates planning from implementation. Based on the research paper "Effective Harnesses for Long-Running Agents", it enables Claude Code to handle complex, multi-session projects with proper progress tracking and state recovery.

## System Overview

The two-agent harness creates a workflow where:
- **Opus** (you) orchestrates and delegates - never implements directly
- **Initializer Agent** (sonnet) breaks down projects into 200+ trackable features
- **Coding Agent** (sonnet) implements features one at a time with quality assurance

## Auto-Setup Process

To set up the complete two-agent system, execute the setup script:

```bash
bash ~/.claude/skills/two-agent-harness/scripts/setup-two-agent-system.sh
```

This script will automatically:
1. Create agent definitions in `~/.claude/agents/`
2. Install enforcement hooks in `~/.claude/hooks/`
3. Add reference documentation to `~/.claude/REFRENCE/TWO-AGENT-HARNESS/`
4. Configure `~/.claude/CLAUDE.md` with delegation instructions
5. Validate the installation

## What Gets Installed

### Agents (`~/.claude/agents/`)

| Agent | Model | Purpose |
|-------|-------|---------|
| `initializer-agent` | sonnet | Breaks down complex tasks into feature-list.json with 200+ features |
| `coding-agent` | sonnet | Implements features systematically, one at a time |

### Hooks (`~/.claude/hooks/`)

| Hook | Event | Action |
|------|-------|--------|
| `pre-tool-guard.sh` | PreToolUse | Blocks Opus from editing src/ files, updates heartbeat |
| `post-tool-guard.sh` | PostToolUse | Reminds about progress updates after code changes |
| `session-progress-check.sh` | SessionStart | Detects pending features and abnormal exits |
| `verify-coding-agent.sh` | SubagentStop | Verifies coding-agent updated progress files |
| `session-end.sh` | SessionEnd | Marks session complete for recovery detection |

### Reference Documentation (`~/.claude/REFRENCE/TWO-AGENT-HARNESS/`)

Nine comprehensive guides covering:
- Framework overview and philosophy
- Agent specifications
- Feature tracking system
- Hook system
- Git integration
- Session workflow
- Testing strategy
- File structure

## Post-Installation Usage

### Starting a New Project

```
User: "Initialize this as a new project with comprehensive feature breakdown"
Opus: [Invokes initializer-agent via Task tool]
Result: Creates feature-list.json with 200+ features, init.sh, and progress tracking
```

### Implementing Features

```
User: "Implement the next feature"
Opus: [Invokes coding-agent via Task tool]
Result: Implements one feature, updates progress, commits changes
```

### Delegation Rules

| Situation | Agent to Use |
|-----------|--------------|
| New project, complex breakdown | `initializer-agent` |
| Implement feature from feature-list | `coding-agent` |
| Need codebase understanding | `Explore` (built-in) |
| Quick fix (<5 min), explicit request | Do directly (say "quick fix" or "direct edit") |

## Bypass Keywords

When you need to bypass the enforcement hooks, include these keywords in your prompt:
- `"quick fix"` - Single line change
- `"direct edit"` - User explicitly requested direct editing
- `"no progress"` - No feature-list.json exists yet

## Project Progress Files

When a project is initialized, these files are created in `.claude/progress/`:

- `feature-list.json` - Comprehensive feature breakdown with status tracking
- `session-state.json` - Session state for recovery detection
- `claude-progress.txt` - Human-readable progress log

## Templates

The skill includes templates for new projects in `assets/templates/`:
- `feature-list-template.json` - Starting point for feature breakdown
- `session-state-template.json` - Initial session state
- `init-template.sh` - Environment setup script

## Troubleshooting

### Agents Not Appearing in Task Tool
Verify agents are in `~/.claude/agents/`:
```bash
ls -la ~/.claude/agents/
```

### Hooks Not Triggering
Check hook configuration in `~/.claude/settings.json` and verify hooks are executable:
```bash
chmod +x ~/.claude/hooks/*.sh
```

### Recovery After Crash
If a session ended abnormally, the `session-progress-check.sh` hook will detect it on next startup and prompt you to invoke `coding-agent` for recovery.

## Reference Documentation

For detailed information, see the reference files:
- `references/two-agent-framework-overview.md` - Full system design
- `references/initializer-agent-spec.md` - Initializer agent details
- `references/coding-agent-spec.md` - Coding agent details
- `references/hook-system.md` - Hook configuration and behavior
- `references/feature-tracking-system.md` - Progress tracking details
- `references/session-workflow.md` - Session lifecycle management
