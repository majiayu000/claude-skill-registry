---
name: minimum-viable-agentic
description: Guide creation of minimum viable agentic layer for a codebase. Use when starting agentic coding in a new project, bootstrapping essential components, or creating the minimal scaffolding for agent success.
allowed-tools: Read, Grep, Glob
---

# Minimum Viable Agentic Layer Skill

Guide teams through creating the essential agentic layer components to start agentic coding.

## When to Use

- Starting agentic coding in a new project
- Adding agentic layer to existing codebase
- Understanding bare minimum requirements
- Quick-starting agentic automation

## Core Concept

> "For your minimum viable agentic layer, you really only need these pieces: AI developer workflow directory, prompts, and plans."

## Minimum Viable Structure

```text
project/
├── specs/                    # Plans for agents
│   └── (generated plans go here)
├── .claude/
│   └── commands/            # Agentic prompts
│       ├── chore.md         # Chore planning
│       └── implement.md     # Implementation HOP
└── adws/                    # AI Developer Workflows
    ├── adw_modules/
    │   └── agent.py         # Core execution
    └── adw_chore_implement.py  # Gateway script
```

Total: 4-5 files to bootstrap.

## Implementation Workflow

### Step 1: Create Directory Structure

```bash
mkdir -p specs
mkdir -p .claude/commands
mkdir -p adws/adw_modules
```

### Step 2: Create Chore Template

`.claude/commands/chore.md`:

```markdown
# Chore Planning

Create a detailed plan for this chore task.

## Task
$ARGUMENTS

## Output
Create a spec file at: specs/chore-{adw_id}-{name}.md

Include:
- Task description
- Files to modify
- Step-by-step implementation
- Validation criteria
```

### Step 3: Create Implement HOP

`.claude/commands/implement.md`:

```markdown
# Implementation

Implement the plan provided.

## Plan File
$ARGUMENTS

Read the plan file and implement each step.
Report changes with git diff --stat when complete.
```

### Step 4: Create Agent Module

`adws/adw_modules/agent.py`:

- Claude Code subprocess execution
- Request/response data models
- Output file handling
- Error handling

### Step 5: Create Gateway Script

`adws/adw_chore_implement.py`:

- Accept chore description
- Execute /chore to generate plan
- Execute /implement with plan
- Report results

## Validation Checklist

After setup, verify:

- [ ] `specs/` directory exists
- [ ] `.claude/commands/chore.md` exists
- [ ] `.claude/commands/implement.md` exists
- [ ] `adws/adw_modules/agent.py` exists
- [ ] Gateway script runs successfully

## Time Investment

| Phase | Time | Activities |
| --- | --- | --- |
| Setup | 2 hours | Directory structure, basic templates |
| Agent module | 2-4 hours | Core execution code |
| Gateway script | 1-2 hours | First composed workflow |
| **Total** | **5-8 hours** | **MVP complete** |

## Scaling Path

After MVP, add progressively:

1. **Week 2**: Add /bug and /feature templates
2. **Week 3**: Add hooks for automation
3. **Week 4**: Add triggers for scheduling
4. **Week 5**: Add worktree isolation
5. **Week 6+**: Add full SDLC workflows

## Key Memory References

- @agentic-layer-structure.md - Full structure reference
- @gateway-script-patterns.md - Script patterns
- @template-engineering.md - Template design

## Output Format

```markdown
## Minimum Viable Agentic Layer Setup

**Project:** {name}
**Status:** Ready for Implementation

### Files to Create

1. **specs/** (directory)
   - Will contain generated plans

2. **.claude/commands/chore.md**
   - Chore planning template
   - Generates specs from descriptions

3. **.claude/commands/implement.md**
   - Implementation HOP
   - Executes generated plans

4. **adws/adw_modules/agent.py**
   - Core agent execution
   - Subprocess handling
   - Output management

5. **adws/adw_chore_implement.py**
   - Gateway script
   - Composes chore + implement

### Implementation Order
1. Create directories
2. Add chore.md template
3. Add implement.md template
4. Create agent.py module
5. Create gateway script
6. Test end-to-end

### Estimated Time
5-8 hours to production-ready MVP
```

## Common Mistakes

- Over-engineering MVP (too many templates too soon)
- Skipping agent.py (trying to call claude directly)
- No error handling in gateway scripts
- Not organizing output files consistently

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
