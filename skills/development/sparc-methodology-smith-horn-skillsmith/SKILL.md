---
name: sparc-methodology
title: SPARC Development Framework
version: 3.0.0
category: development
description: SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) comprehensive development methodology with multi-agent orchestration
tags:
  - sparc
  - tdd
  - architecture
  - orchestration
  - methodology
  - multi-agent
author: Claude Flow
difficulty: intermediate
prerequisites:
  - Claude Flow MCP server configured
  - Swarm orchestration available
tools_required:
  - mcp__claude-flow__*
  - Bash
  - TodoWrite
related_skills:
  - hooks-automation
  - swarm-orchestration
  - hive-mind-execution
---

# SPARC Development Framework

## Behavioral Classification

**Type**: Guided Decision

This skill guides you through development methodology decisions and then executes based on your choices.

**Decision Points**:
1. Which SPARC mode(s) to use for your task?
2. Swarm topology (hierarchical, mesh, ring, star)?
3. Parallel or sequential execution?
4. Test coverage target?

---

## Overview

SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) is a systematic development methodology integrated with Claude Flow's multi-agent orchestration capabilities. It provides **17 specialized modes** for comprehensive software development, from initial research through deployment and monitoring.

---

## Core Philosophy

SPARC methodology emphasizes:

- **Systematic Approach**: Structured phases from specification to completion
- **Test-Driven Development**: Tests written before implementation
- **Parallel Execution**: Concurrent agent coordination for 2.8-4.4x speed improvements
- **Memory Integration**: Persistent knowledge sharing across agents and sessions
- **Quality First**: Comprehensive reviews, testing, and validation

### Key Principles

1. **Specification Before Code**: Define requirements and constraints clearly
2. **Design Before Implementation**: Plan architecture and components
3. **Tests Before Features**: Write failing tests, then make them pass
4. **Review Everything**: Code quality, security, and performance checks
5. **Document Continuously**: Maintain current documentation throughout

---

## Quick Start

### MCP Tools (Preferred)

```javascript
// Initialize swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 8 }

// Execute a mode
mcp__claude-flow__sparc_mode {
  mode: "coder",
  task_description: "implement user authentication with JWT",
  options: { test_driven: true }
}
```

### CLI (Terminal)

```bash
# List all modes
npx claude-flow sparc modes

# Run specific mode
npx claude-flow sparc run <mode> "task description"

# TDD workflow
npx claude-flow sparc tdd "feature description"

# Full pipeline
npx claude-flow sparc pipeline "task description"
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Development Phases](./phases.md) | 5 SPARC phases from Specification to Completion |
| [Available Modes](./modes.md) | All 17 specialized modes with usage examples |
| [Orchestration Patterns](./patterns.md) | Swarm topologies, coordination patterns |
| [Workflows](./workflows.md) | TDD workflows, common workflows, advanced features |

---

## Available Modes (17 total)

### Core Orchestration
| Mode | Description |
|------|-------------|
| `orchestrator` | Multi-agent task orchestration |
| `swarm-coordinator` | Swarm management for multi-agent workflows |
| `workflow-manager` | Process automation and workflow orchestration |
| `batch-executor` | Parallel task execution for high-throughput |

### Development
| Mode | Description |
|------|-------------|
| `coder` | Autonomous code generation |
| `architect` | System design with Memory coordination |
| `tdd` | Test-driven development |
| `reviewer` | Code review and quality analysis |

### Analysis & Research
| Mode | Description |
|------|-------------|
| `researcher` | Deep research with parallel web searches |
| `analyzer` | Code and data analysis |
| `optimizer` | Performance optimization |

### Creative & Support
| Mode | Description |
|------|-------------|
| `designer` | UI/UX design with accessibility focus |
| `innovator` | Creative problem-solving |
| `documenter` | Documentation generation |
| `debugger` | Systematic debugging |
| `tester` | Comprehensive testing beyond TDD |
| `memory-manager` | Knowledge management |

---

## Activation Methods

### Method 1: MCP Tools (Preferred)

```javascript
mcp__claude-flow__sparc_mode {
  mode: "<mode-name>",
  task_description: "<task description>",
  options: { /* mode-specific options */ }
}
```

### Method 2: NPX CLI

```bash
npx claude-flow sparc run <mode> "task description"
```

### Method 3: Local Installation

```bash
./claude-flow sparc run <mode> "task description"
```

---

## Quick Reference

### Most Common Commands

```bash
npx claude-flow sparc modes                    # List modes
npx claude-flow sparc run <mode> "task"        # Run specific mode
npx claude-flow sparc tdd "feature"            # TDD workflow
npx claude-flow sparc pipeline "task"          # Full pipeline
npx claude-flow sparc batch <modes> "task"     # Batch execution
```

### Most Common MCP Calls

```javascript
// Initialize swarm
mcp__claude-flow__swarm_init { topology: "hierarchical" }

// Execute mode
mcp__claude-flow__sparc_mode { mode: "coder", task_description: "..." }

// Monitor progress
mcp__claude-flow__swarm_monitor { interval: 5000 }

// Store in memory
mcp__claude-flow__memory_usage { action: "store", key: "...", value: "..." }
```

---

## Performance Benefits

**Proven Results**:
- **84.8%** SWE-Bench solve rate
- **32.3%** token reduction through optimizations
- **2.8-4.4x** speed improvement with parallel execution
- **27+** neural models for pattern learning
- **90%+** test coverage standard

---

## Support and Resources

- **Documentation**: https://github.com/ruvnet/claude-flow
- **Issues**: https://github.com/ruvnet/claude-flow/issues
- **NPM Package**: https://www.npmjs.com/package/claude-flow

---

**Remember**: **SPARC = Specification, Pseudocode, Architecture, Refinement, Completion**

---

**Version**: 3.0.0
**Last Updated**: 2025-01-24
