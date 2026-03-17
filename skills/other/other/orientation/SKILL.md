---
name: orientation
description: Orients agents in new projects by scanning entry documents and discovering capabilities. Use at session start, when entering unfamiliar territory, or when asking "what can you do" or "where do I start".
---

# Orientation

Before you can act wisely, you must understand where you are.

## Philosophy

### Why Orient?

The danger isn't ignorance—it's **false confidence**.

An agent that dives into action without understanding context will:
- Make assumptions that don't hold
- Solve the wrong problem
- Miss crucial constraints
- Repeat mistakes others already learned from

Orientation isn't bureaucracy. It's the difference between a surgeon who reads the chart and one who doesn't.

```
The First Law of Orientation:
├── You don't know what you don't know
├── Projects have hidden assumptions
├── Context shapes correct action
└── Reading first costs minutes; mistakes cost hours
```

### What Orientation Is (And Isn't)

Orientation is **reconnaissance**, not deep investigation.

```
Orientation answers:      Orientation doesn't answer:
├── What is this?         ├── How does this work? (→ dive)
├── What matters here?    ├── What should we build? (→ engineering)
├── Who came before?      ├── Is this code correct? (→ validation)
└── Where should I look?  └── What needs fixing? (→ housekeeping)
```

Orientation points you in the right direction. Other skills take you there.

## Core Concepts

### Entry Points

Every project has documents that reveal its nature. Priority order:

```
Agent-specific (highest signal):
├── CLAUDE.md     → Written for you
├── AGENTS.md     → Written for any agent
└── .claude/      → Claude-specific config

Project docs (context):
├── README.md     → What this is
├── CONTRIBUTING.md → How to work here
└── docs/         → Deeper knowledge

Structure signals (implicit):
├── package.json / pyproject.toml / Cargo.toml → Stack
├── .github/workflows/ → CI/CD exists
└── docker-compose.yml → Containerized
```

### Skills Discovery

Skills live in predictable locations:

```
Project-level:          User-level:
├── .claude/skills/     ├── ~/.claude/skills/
├── .cursor/skills/     ├── ~/.cursor/skills/
└── .agents/skills/     └── ~/.agents/skills/
```

Each skill has a `SKILL.md` with frontmatter describing when to use it.

### Memory Context

If `.memory/` exists, past agents left knowledge:

```
.memory/
├── context.md    → Current state, active concerns
├── notes/        → What was learned
├── decisions/    → Why things are this way
└── sessions/     → What happened before
```

Read `context.md` first—it's the handoff from previous sessions.

## The Orientation Process

```
1. SCAN: What documents exist?
      ↓
2. READ: What do they say about working here?
      ↓
3. DISCOVER: What skills and memory are available?
      ↓
4. ASSESS: What's the project type and health?
      ↓
5. REPORT: Summarize findings, suggest starting points
```

### Output Format

After orientation, provide:

```markdown
## Project Overview
[1-2 sentences: what this is]

## Key Entry Points
- CLAUDE.md: [what it tells you]
- README: [what it tells you]

## Available Skills
| Skill | When to use |
|-------|-------------|
| [name] | [trigger] |

## Project Type
- Stack: [technologies]
- Notable: [CI, Docker, etc.]

## Suggested Starting Points
1. [Based on context]
2. [Based on context]
```

## Health Diagnosis

Part of orientation is noticing what's missing:

| Finding | Implication |
|---------|-------------|
| No CLAUDE.md or AGENTS.md | Future agents will struggle |
| Stale docs (>6 months) | Information may be wrong |
| Empty .memory/ | No institutional knowledge preserved |
| Missing README | Project purpose unclear |

When issues exist, note them and suggest `housekeeping` for resolution.

Orientation is read-only—it diagnoses but doesn't treat.

## Integration

```
orientation
     │
     ├─► "How does X work?" ──► dive
     ├─► "What should we build?" ──► engineering
     ├─► "Ready to commit" ──► refining
     ├─► "Docs need updating" ──► housekeeping
     └─► "What happened before?" ──► memory
```

## Understanding, Not Rules

| Tension | Resolution |
|---------|------------|
| Speed vs Thoroughness | Match depth to unfamiliarity. New project? Read everything. Familiar? Skim for changes. |
| Comprehensive vs Focused | Start broad (what is this?), narrow to relevant (what matters for my task?). |
| Reading vs Doing | Orientation is fast. Skipping it feels faster but costs more in mistakes. |

The goal isn't to check boxes. It's to build enough mental model to act wisely.

## Reference

See `reference/` for:
- [examples.md](reference/examples.md) - Sample orientation reports
