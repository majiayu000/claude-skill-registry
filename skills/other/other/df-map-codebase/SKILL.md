---
name: df:map-codebase
description: |
  Analyze codebase with parallel mapper agents to produce .planning/codebase/ documents and CLAUDE.md.
  Use when the user wants to understand, analyze, or map an existing codebase.
  Triggers on: "understand this codebase", "map the code", "analyze architecture", "what does this codebase look like?", "explore the code structure"
argument-hint: "[optional: specific area to map, e.g., 'api' or 'auth']"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Write
  - Task
---

<objective>
Analyze existing codebase using parallel df-codebase-mapper agents to produce structured codebase documents, then synthesize a prescriptive CLAUDE.md.

Each mapper agent explores a focus area and **writes documents directly** to `.planning/codebase/`. The orchestrator only receives confirmations, then reads the 8 docs to generate CLAUDE.md with coding rules that Claude Code auto-loads every session.

Output: .planning/codebase/ folder with 8 structured documents + CLAUDE.md at project root.
</objective>

<execution_context>
@~/.claude/devflow/workflows/map-codebase.md
</execution_context>

<context>
Focus area: $ARGUMENTS (optional - if provided, tells agents to focus on specific subsystem)

**Load project state if exists:**
Check for .planning/STATE.md - loads context if project already initialized

**This command can run:**
- Before /df:new-project (brownfield codebases) - creates codebase map first
- After /df:new-project (greenfield codebases) - updates codebase map as code evolves
- Anytime to refresh codebase understanding
</context>

<when_to_use>
**Use map-codebase for:**
- Brownfield projects before initialization (understand existing code first)
- Refreshing codebase map after significant changes
- Onboarding to an unfamiliar codebase
- Before major refactoring (understand current state)
- When STATE.md references outdated codebase info

**Skip map-codebase for:**
- Greenfield projects with no code yet (nothing to map)
- Trivial codebases (<5 files)
</when_to_use>

<process>
1. Check if .planning/codebase/ already exists (offer to refresh or skip)
2. Create .planning/codebase/ directory structure
3. Spawn 4 parallel df-codebase-mapper agents:
   - Agent 1: tech focus → writes STACK.md, INTEGRATIONS.md
   - Agent 2: arch focus → writes ARCHITECTURE.md, STRUCTURE.md
   - Agent 3: quality focus → writes CONVENTIONS.md, TESTING.md, PATTERNS.md
   - Agent 4: concerns focus → writes CONCERNS.md
4. Wait for agents to complete, collect confirmations (NOT document contents)
5. Verify all 8 documents exist with line counts
6. Synthesize CLAUDE.md from all 8 docs (prescriptive coding rules, marker-based merge)
7. Commit codebase map + CLAUDE.md
8. Offer next steps (typically: /df:new-project or /df:plan-objective)
</process>

<success_criteria>
- [ ] .planning/codebase/ directory created
- [ ] All 8 codebase documents written by mapper agents
- [ ] Documents follow template structure
- [ ] Parallel agents completed without errors
- [ ] CLAUDE.md generated at project root with prescriptive coding rules
- [ ] CLAUDE.md uses <!-- DEVFLOW:START/END --> markers (preserves user content on re-run)
- [ ] User knows next steps
</success_criteria>
