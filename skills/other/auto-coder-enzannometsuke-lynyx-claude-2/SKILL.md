---
description: >
  Autonomous multi-session feature development framework. Use when the user wants to
  systematically implement features from a specification, track progress across sessions,
  and ensure all tests pass before marking features complete. Activated by the /lynyx-agent-kit:auto-coder
  command or when working with feature_list.json files in an .auto-coder directory.
---

# Auto-Coder Skill

A framework for orchestrating autonomous feature development across multiple Claude Code sessions.

## Overview

Auto-coder operates in two phases:

1. **Initializer Phase** (Session 1): Analyzes a project specification and generates a comprehensive `feature_list.json` with test cases ordered by priority and dependency
2. **Coding Phase** (Sessions 2+): Implements features one-by-one, running tests, making git commits, and tracking progress until all features are complete

## State Files

All auto-coder state is persisted in the `.auto-coder/` directory:

| File | Purpose |
|------|---------|
| `feature_list.json` | Source of truth for features, test cases, and completion status |
| `progress.md` | Human-readable log of session activity |

See [FEATURE_SCHEMA.md](FEATURE_SCHEMA.md) for the complete JSON schema.

## Locating Skill Files

To quickly locate the auto-coder skill instruction files (CODER.md, INITIALIZER.md, etc.), use the `skill-file-locator.py` script:

```bash
python ~/.claude/plugins/cache/lynyx-claude/lynyx-agent-kit/<version>/skills/auto-coder/scripts/skill-file-locator.py
```

The script outputs the full path to the skill directory and a tree view of all skill files:

```
~/.claude/plugins/cache/lynyx-claude/lynyx-agent-kit/1.2.1/skills/auto-coder
├── scripts
│   ├── continue.sh
│   └── skill-file-locator.py
├── CODER.md
├── FEATURE_SCHEMA.md
├── INITIALIZER.md
└── SKILL.md
```

**Usage:**

- Default skill: `python skill-file-locator.py` (locates auto-coder skill)
- Custom skill: `python skill-file-locator.py <skill-name>`

Use this script at the start of each coding session to locate and read the appropriate instruction files (CODER.md for coding phase, INITIALIZER.md for initialization phase).

## Phases

### Phase 1: Initialization

Run with `/lynyx-agent-kit:auto-coder init [spec_file]`

For detailed instructions, see [INITIALIZER.md](INITIALIZER.md).

**Summary:**

- Read and analyze the project specification
- Generate `feature_list.json` with features ordered by critical path
- Auto-generate project prefix for task IDs (present to user for approval)
- Initialize project structure and git repository
- Create initial commit
- Rename session: `auto-coder: initialize {PROJECT_NAME}`

### Phase 2: Coding

Run with `/lynyx-agent-kit:auto-coder code`

For detailed instructions, see [CODER.md](CODER.md).

**Summary:**

- Orient to project state (read files, git log)
- Run regression tests on high-priority passing features
- Select next incomplete feature
- Implement and test the feature
- Update `feature_list.json` and commit
- Rename session: `auto-coder: {PROJECT_NAME} | {TASK_ID}`

## Session Management

### Fresh Sessions vs Resume

- **Fresh sessions**: Recommended for starting work on each new feature
- **Resume sessions**: Use `claude --resume <name>` for interrupted work mid-feature

### Session Naming

Sessions are automatically named for easy identification:
- Initializer: `auto-coder: initialize {PROJECT_NAME}`
- Coder: `auto-coder: {PROJECT_NAME} | {TASK_ID}`

### Pause/Resume

1. **To pause**: Exit session with Ctrl+C or Ctrl+D (context preserved)
2. **To resume**: `claude --resume "auto-coder: {PROJECT_NAME} | {TASK_ID}"`
3. **To start fresh**: `claude -p "/lynyx-agent-kit:auto-coder code"` (new session)

## Auto-Continuation

For fully autonomous operation, use a shell loop:

```bash
while true; do claude -p "/lynyx-agent-kit:auto-coder code" || break; sleep 3; done
```

Or use the helper script:

```bash
./plugins/lynyx-agent-kit/skills/auto-coder/scripts/continue.sh
```

## Security Guidance

The following commands are recommended for use during implementation:

**Allowed:**

- File operations: `ls`, `cat`, `head`, `tail`, `wc`, `grep`
- Runtime: `npm`, `node`, `bun`, `python`, `pytest`
- Version control: `git`
- Process management: `ps`, `lsof`, `sleep`, `pkill` (dev processes only)

**Avoid:**

- System modification commands
- Network commands without clear purpose
- Commands affecting files outside the project directory
