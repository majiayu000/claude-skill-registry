---
name: LLM Council
description: Orchestrate multiple LLMs as a council, generating collective intelligence through peer review and chairman synthesis
version: 1.0.0
dependencies: python>=3.8, python-dotenv, loguru
---

## Overview

LLM Council is a Skill that organizes multiple LLMs as "council members" and generates high-quality responses through a 3-stage process.

### Use Cases

- When you need multiple perspectives for important decisions
- When you want multiple AIs to review code
- When comparing and evaluating design proposals
- When you need objective responses with reduced bias

## 3-Stage Process

1. **Stage 1: Opinion Collection** - Each member (LLM) responds independently
2. **Stage 2: Peer Review** - Anonymized responses are mutually ranked
3. **Stage 3: Synthesis** - Chairman integrates all opinions and reviews into final response

## Quick Start

```bash
# Basic question
python scripts/run.py council_skill.py "What's the optimal caching strategy?"

# With TUI dashboard
python scripts/run.py cli.py --dashboard "What's the optimal caching strategy?"

# Code fix (diff only)
python scripts/run.py council_skill.py --dry-run "Fix the bug in buggy.py"

# Auto-merge
python scripts/run.py council_skill.py --auto-merge "Add error handling"
```

## Command Options

| Option | Description |
|--------|-------------|
| `--dashboard`, `-d` | TUI dashboard for real-time monitoring |
| `--worktrees` | Git worktree mode - each member works independently |
| `--dry-run` | Show diff without merging |
| `--auto-merge` | Auto-merge the top-ranked proposal |
| `--merge N` | Merge member N's proposal |
| `--confirm` | Show confirmation prompt before merge |
| `--no-commit` | Apply changes without staging |
| `--list` | Show conversation history |
| `--continue N` | Continue conversation N |

## Setup

1. Create `scripts/.env` to configure models
2. Install and configure OpenCode CLI
3. Run `python scripts/run.py council_skill.py --setup` for details

## Resources

See `README.md` for more details.
