---
name: using-agentops
description: 'Meta skill explaining the AgentOps workflow. Auto-injected on session start. Covers RPI workflow, Knowledge Flywheel, and skill catalog.'
---

# AgentOps Workflow

You have access to the AgentOps skill set for structured development workflows.

## The RPI Workflow

```
Research → Plan → Implement → Validate
    ↑                            │
    └──── Knowledge Flywheel ────┘
```

### Research Phase

```bash
/research <topic>      # Deep codebase exploration
/knowledge <query>     # Query existing knowledge
```

**Output:** `.agents/research/<topic>.md`

### Plan Phase

```bash
/pre-mortem <spec>     # Simulate failures before implementing
/plan <goal>           # Decompose into trackable issues
```

**Output:** Beads issues with dependencies

### Implement Phase

```bash
/implement <issue>     # Single issue execution
/crank <epic>          # Autonomous single-agent execution
/swarm [--agents N]     # Parallel multi-agent execution
```

**Output:** Code changes, tests, documentation

### Validate Phase

```bash
/vibe [target]         # Code validation (security, quality, architecture)
/post-mortem           # Extract learnings after completion
/retro                 # Quick retrospective
```

**Output:** `.agents/learnings/`, `.agents/patterns/`

## Phase-to-Skill Mapping

| Phase | Primary Skill | Supporting Skills |
|-------|---------------|-------------------|
| **Research** | `/research` | `/knowledge`, `/inject` |
| **Plan** | `/plan` | `/pre-mortem` |
| **Implement** | `/implement` | `/crank` (single-agent), `/swarm` (multi-agent) |
| **Validate** | `/vibe` | `/retro`, `/post-mortem` |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/research` | Deep codebase exploration |
| `/pre-mortem` | Failure simulation before implementing |
| `/plan` | Epic decomposition into issues |
| `/implement` | Execute single issue |
| `/crank` | Autonomous single-agent execution |
| `/swarm` | Parallel multi-agent execution (Agent Farm) |
| `/vibe` | Code validation |
| `/retro` | Extract learnings |
| `/post-mortem` | Full validation + knowledge extraction |
| `/beads` | Issue tracking operations |
| `/bug-hunt` | Root cause analysis |
| `/knowledge` | Query knowledge artifacts |
| `/complexity` | Code complexity analysis |
| `/doc` | Documentation generation |

## Knowledge Flywheel

Every `/post-mortem` feeds back to `/research`:

1. **Learnings** extracted → `.agents/learnings/`
2. **Patterns** discovered → `.agents/patterns/`
3. **Research** enriched → Future sessions benefit

## Natural Language Triggers

Skills auto-trigger from conversation:

| Say This | Runs |
|----------|------|
| "I need to understand how auth works" | `/research` |
| "Check my code for issues" | `/vibe` |
| "What could go wrong with this?" | `/pre-mortem` |
| "Let's execute this epic" | `/crank` |
| "Spawn agents to work in parallel" | `/swarm` |

## Issue Tracking

AgentOps uses beads for git-native issue tracking:

```bash
bd ready              # Unblocked issues
bd show <id>          # Issue details
bd close <id>         # Close issue
bd sync               # Sync with git
```
