---
name: Pair Programming
version: "1.0.0"
description: AI-assisted pair programming with multiple modes (driver/navigator/switch), real-time verification, quality monitoring, and comprehensive testing. Supports TDD, debugging, refactoring, and learning sessions. Features automatic role switching, continuous code review, security scanning, and performance optimization with truth-score verification.
category: development
tags:
  - pair-programming
  - collaboration
  - tdd
  - code-review
  - quality
author: Smith Horn
---

# Pair Programming

Collaborative AI pair programming with intelligent role management, real-time quality monitoring, and comprehensive development workflows.

## Behavioral Classification

**Type**: Interactive Exploration

This skill engages in ongoing dialogue throughout the programming session. Expect frequent interaction and collaboration as we work together.

**Interaction Pattern**:
- I'll ask clarifying questions as we code
- Role switching prompts at intervals (in switch mode)
- Continuous feedback on code quality
- Real-time suggestions and reviews

---

## What This Skill Does

This skill provides professional pair programming capabilities with AI assistance, supporting multiple collaboration modes, continuous verification, and integrated testing.

**Key Capabilities:**
- **Multiple Modes**: Driver, Navigator, Switch, TDD, Review, Mentor, Debug
- **Real-Time Verification**: Automatic quality scoring with rollback on failures
- **Role Management**: Seamless switching between driver/navigator roles
- **Testing Integration**: Auto-generate tests, track coverage, continuous testing
- **Code Review**: Security scanning, performance analysis, best practice enforcement
- **Session Persistence**: Auto-save, recovery, export, and sharing

---

## Prerequisites

**Required:**
- Claude Flow CLI installed (`npm install -g claude-flow@alpha`)
- Git repository (optional but recommended)

**Recommended:**
- Testing framework (Jest, pytest, etc.)
- Linter configured (ESLint, pylint, etc.)
- Code formatter (Prettier, Black, etc.)

---

## Quick Start

### Basic Session
```bash
# Start simple pair programming
claude-flow pair --start
```

### TDD Session
```bash
# Test-driven development
claude-flow pair --start \
  --mode tdd \
  --test-first \
  --coverage 90
```

### Expert Refactoring
```bash
# High-quality refactoring session
claude-flow pair --start \
  --agent senior-dev \
  --focus refactor \
  --verify \
  --threshold 0.98
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Modes](./modes.md) | Driver, Navigator, Switch, TDD, Review, Mentor, Debug modes |
| [Commands](./commands.md) | All in-session commands with aliases |
| [Configuration](./configuration.md) | Config files, profiles, environment variables |
| [Examples](./examples.md) | Real-world session examples |

---

## Quick Reference

### Available Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **Driver** | You write code, AI navigates | Learning, familiar features |
| **Navigator** | AI writes code, you direct | Rapid prototyping, generation |
| **Switch** | Alternating roles at intervals | Long sessions, knowledge sharing |
| **TDD** | Test-driven development | Building with tests |
| **Review** | Continuous code review | Quality focus |
| **Mentor** | Learning-focused | Learning priority |
| **Debug** | Problem-solving | Fixing issues |

### Essential Commands

| Command | Alias | Purpose |
|---------|-------|---------|
| `/suggest` | `/s` | Get improvement suggestions |
| `/explain` | `/e` | Explain code |
| `/test` | `/t` | Run tests |
| `/review` | `/r` | Code review |
| `/commit` | `/c` | Commit with verification |
| `/switch` | `/sw` | Switch roles |
| `/status` | `/st` | Session status |

### Session Control

```bash
# Check status
claude-flow pair --status

# Pause session
/pause [--reason <reason>]

# Resume session
/resume

# End session
claude-flow pair --end [--save] [--report]
```

### Quality Thresholds

| Metric | Error | Warning | Good | Excellent |
|--------|-------|---------|------|-----------|
| **Truth Score** | <0.90 | 0.90-0.95 | 0.95-0.98 | >0.98 |
| **Coverage** | <70% | 70-80% | 80-90% | >90% |
| **Complexity** | >15 | 10-15 | 5-10 | <5 |

### Built-in Agents

| Agent | Expertise | Style |
|-------|-----------|-------|
| `senior-dev` | Architecture, patterns, optimization | Thorough |
| `tdd-specialist` | Testing, mocks, coverage | Test-first |
| `debugger-expert` | Debugging, profiling, tracing | Analytical |
| `junior-dev` | Learning, basics, documentation | Educational |

---

## Session Templates

```bash
# Quick templates
claude-flow pair --template refactor  # High verification (0.98)
claude-flow pair --template feature   # Standard verification (0.95)
claude-flow pair --template debug     # Problem-solving focus
claude-flow pair --template learn     # Mentor mode, slow pace
```

---

## Best Practices

### Session Practices
1. **Clear Goals** - Define session objectives upfront
2. **Appropriate Mode** - Choose based on task type
3. **Enable Verification** - For critical code paths
4. **Regular Testing** - Maintain quality continuously
5. **Session Notes** - Document important decisions
6. **Regular Breaks** - Take breaks every 45-60 minutes

### Mode Selection
- **Driver Mode**: When learning, controlling implementation
- **Navigator Mode**: For rapid prototyping, generation
- **Switch Mode**: Long sessions, balanced collaboration
- **TDD Mode**: Building with tests
- **Review Mode**: Quality focus
- **Mentor Mode**: Learning priority
- **Debug Mode**: Fixing issues

---

## Related Commands

- `claude-flow pair --help` - Show help
- `claude-flow pair config` - Manage configuration
- `claude-flow pair profile` - Manage profiles
- `claude-flow pair templates` - List templates
- `claude-flow pair agents` - List available agents
