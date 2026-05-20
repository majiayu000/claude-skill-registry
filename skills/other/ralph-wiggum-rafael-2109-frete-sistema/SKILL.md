---
name: ralph-wiggum
description: |
  Executa loops autonomos de desenvolvimento via tecnica Ralph Wiggum.
  Usar quando: (1) Iniciar loop Ralph na sessao atual, (2) Usuario diz "/ralph-loop",
  (3) Explicar a tecnica Ralph Wiggum, (4) Configurar estrutura Ralph para um projeto,
  (5) Usuario menciona "autonomous loop", "I'm in danger" ou "ralph".
---

# Ralph Wiggum Technique

The Ralph Wiggum technique is an AI development methodology using autonomous loops to reduce development effort. Named after the Simpsons character ("I'm in danger!").

## Available Commands

### /ralph-loop (or skill:ralph-wiggum:ralph-loop)
Start Ralph loop in current Claude Code session.

### /help (or skill:ralph-wiggum:help)
Explain Ralph Wiggum technique and available commands.

### /cancel-ralph (or skill:ralph-wiggum:cancel-ralph)
Cancel active Ralph loop.

## Quick Start

1. **Create specs**: Add requirement specs to `.claude/ralph-loop/specs/` directory
2. **Run planning**: `./ralph-loop.sh plan 3` (3 iterations)
3. **Run building**: `./ralph-loop.sh 10` (10 iterations)

## Three Phases, Two Prompts, One Loop

| Phase | Prompt | Purpose |
|-------|--------|---------|
| 1 | (human) | Define requirements, create specs |
| 2 | PROMPT_plan.md | Gap analysis: specs vs code → IMPLEMENTATION_PLAN.md |
| 3 | PROMPT_build.md | Implement, test, commit, push |

## Loop Mechanics

### Outer Loop (Bash)
```bash
while :; do cat PROMPT.md | claude ; done
```

Each iteration:
1. Feeds prompt to Claude
2. Agent completes ONE task
3. Updates IMPLEMENTATION_PLAN.md
4. Commits and exits
5. Loop restarts with fresh context

### Inner Loop Control
- **Planning mode**: Gap analysis only, no implementation
- **Building mode**: Implement, test, commit, push

## Key Principles

1. **Context efficiency**: One task per iteration
2. **Backpressure**: Tests/lints reject invalid work
3. **Deterministic setup**: Same files loaded each loop
4. **Self-correction**: Plan is disposable, regenerate when wrong

## Key Terminology

| Term | Definition |
|------|------------|
| **JTBD** | Job-to-Be-Done - high-level user need |
| **Topic of Concern** | Distinct aspect within a JTBD |
| **Spec** | Requirements doc (`.claude/ralph-loop/specs/FILENAME.md`) |
| **Task** | Unit of work from specs vs code comparison |

## When to Regenerate Plan

- Ralph goes off track (implementing wrong things)
- Plan feels stale or doesn't match current state
- Too much clutter from completed items
- Significant spec changes made
- Confused about what's actually done

## File Structure

```
project/.claude/ralph-loop/
├── ralph-loop.sh          # Loop script
├── PROMPT_build.md        # Build instructions
├── PROMPT_plan.md         # Plan instructions
├── AGENTS.md              # Operational guide
├── IMPLEMENTATION_PLAN.md # Task list (generated)
└── specs/                 # Requirements
```

## Security Warning

Running with `--dangerously-skip-permissions` exposes:
- API keys
- SSH keys
- Browser cookies

**Always use Docker** (see `docker-compose.ralph.yml`):
```bash
docker-compose -f docker-compose.ralph.yml run ralph
./ralph-loop.sh plan 3
```

## Language Patterns

Key phrases that signal proper Ralph behavior:
- "study" (not "read" or "look at")
- "don't assume not implemented"
- "using parallel subagents"
- "Ultrathink"
- "capture the why"
- "keep it up to date"

## References

- See [references/workflow.md](references/workflow.md) for detailed workflow
- See [scripts/init_ralph_project.py](scripts/init_ralph_project.py) to initialize structure
