---
# VERSION: 1.0.0 (Official Plugin Integration)
name: code-reviewer
description: Automated code review using official Claude Code plugin with 4 parallel agents.
allowed-tools: Read,Write,Bash,Glob,Grep
---

# Code Reviewer (Official Plugin)

Integrates the official Claude Code code-review plugin.

## Quick Start

```bash
/code-review              # Review current changes
/code-review --comment    # Post review as PR comment
```

## Architecture

4 parallel agents with confidence scoring (≥80):

1. Agent #1: CLAUDE.md compliance
2. Agent #2: CLAUDE.md compliance (redundancy)
3. Agent #3: Bug detection (changes only)
4. Agent #4: Git blame/history analysis

## Features

- Multi-agent parallel review
- Confidence-based filtering
- Auto-skip closed/draft/trivial PRs
- Direct GitHub code links

## Integration

Official plugin: `~/.claude-sneakpeek/zai/config/plugins/cache/anthropics/code-review/`

**Author**: Boris Cherny (boris@anthropic.com)
**Version**: 1.0.0
