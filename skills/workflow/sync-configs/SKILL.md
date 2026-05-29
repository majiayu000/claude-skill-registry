---
name: sync-configs
description: |
  SYNC-CONFIGS
---

---
description: Sync Claude Code configuration to Codex CLI and Gemini CLI
---

# SYNC-CONFIGS

Synchronize your AI-assisted development workflow configuration from Claude Code (canonical source) to Codex CLI and Gemini CLI.

## Your Mission

Read Claude Code configuration and generate adapted versions for Codex and Gemini, ensuring consistent philosophy and workflow while respecting each tool's unique strengths.

## Process

### 1. Audit Current State

First, examine what exists:

```bash
# Claude Code (source)
ls -la ~/.claude/CLAUDE.md
ls ~/.claude/commands/*.md | wc -l
ls ~/.claude/skills/*/SKILL.md | wc -l

# Codex CLI (target)
cat ~/.codex/AGENTS.md | wc -l
ls ~/.codex/prompts/*.md 2>/dev/null | wc -l

# Gemini CLI (target)
cat ~/.gemini/GEMINI.md | wc -l
ls ~/.gemini/commands/*.toml 2>/dev/null | wc -l
```

### 2. Generate AGENTS.md for Codex

Adapt the core philosophy from CLAUDE.md into AGENTS.md format. Key adaptations:

**Structure**:
- AGENTS.md should be concise but complete
- Include Ousterhout framework
- Include persona definitions
- Include red flags checklist
- Reference Codex-specific tools (rg, ast-grep)

**Content to port**:
- Software Design Philosophy section
- Complexity Management principles
- Module Design guidance
- Red flags (Manager/Util/Helper, pass-throughs, etc.)
- Persona vocabulary (Carmack, Jobs, Torvalds, Hara, Ousterhout)

**Write to**: `~/.codex/AGENTS.md`

### 3. Generate GEMINI.md for Gemini

Create a comprehensive GEMINI.md (currently empty). Key adaptations:

**Structure**:
- Similar depth to CLAUDE.md
- Leverage Gemini strengths: shell interpolation `!{cmd}`, multimodal, Google grounding
- Include full Ousterhout framework
- Include persona definitions

**Content to port**:
- Full Software Design Philosophy
- Complexity Management
- Module Design
- Red flags checklist
- Persona vocabulary
- Tool usage guidance (adapted for Gemini capabilities)

**Write to**: `~/.gemini/GEMINI.md`

### 4. Sync Agents (New: 15 agents)

Sync all 15 agents (8 specialists + 7 personas) to Codex and Gemini:

**For Codex** (`~/.codex/agents/`):
- Create `.md` files for each agent
- Keep full agent personality, philosophy, and checklists
- Adapt tool references (use `rg`, `ast-grep` instead of Claude-specific tools)
- Full sync - preserve all content, examples, red flags

**For Gemini** (`~/.gemini/system-instructions/`):
- Create `.txt` files for each agent
- Convert to natural language system instructions
- Full personality transfer - all quotes, philosophy, checklists
- Adapt format but preserve depth (multi-paragraph system instructions work great)

**Agents to sync**:

*Domain Specialists:*
1. complexity-archaeologist.md → agents/complexity-archaeologist.md + system-instructions/complexity-archaeologist.txt
2. data-integrity-guardian.md → agents/data-integrity-guardian.md + system-instructions/data-integrity-guardian.txt
3. api-design-specialist.md → agents/api-design-specialist.md + system-instructions/api-design-specialist.txt
4. test-strategy-architect.md → agents/test-strategy-architect.md + system-instructions/test-strategy-architect.txt
5. error-handling-specialist.md → agents/error-handling-specialist.md + system-instructions/error-handling-specialist.txt
6. state-management-analyst.md → agents/state-management-analyst.md + system-instructions/state-management-analyst.txt
7. dependency-health-monitor.md → agents/dependency-health-monitor.md + system-instructions/dependency-health-monitor.txt
8. documentation-quality-reviewer.md → agents/documentation-quality-reviewer.md + system-instructions/documentation-quality-reviewer.txt
9. infrastructure-guardian.md → agents/infrastructure-guardian.md + system-instructions/infrastructure-guardian.txt

*Master Personas:*
10. grug.md → agents/grug.md + system-instructions/grug.txt
11. carmack.md → agents/carmack.md + system-instructions/carmack.txt
12. jobs.md → agents/jobs.md + system-instructions/jobs.txt
13. torvalds.md → agents/torvalds.md + system-instructions/torvalds.txt
14. ousterhout.md → agents/ousterhout.md + system-instructions/ousterhout.txt
15. fowler.md → agents/fowler.md + system-instructions/fowler.txt
16. beck.md → agents/beck.md + system-instructions/beck.txt

**Codex format** (`.md` - keep full content):
```markdown
# Agent Name

Philosophy quote...

## Core Concepts

[Full agent content preserved]

## Review Checklist

- [ ] Check 1
- [ ] Check 2
...
```

**Gemini format** (`.txt` - natural language system instruction):
```
You are [Agent Name]. [Philosophy quote]

Your role: [description]

When reviewing code, you:
- [Checklist item 1]
- [Checklist item 2]
...

[Full philosophy section in narrative form]

Red flags to watch for:
- [Flag 1]
- [Flag 2]
...

[All wisdom quotes and examples in natural language]
```

**CRITICAL**: Both formats get 100% of content. Format changes, depth stays identical.

### 5. Port Core Commands

Identify commands that should exist in all three tools:

**Core workflow** (always sync):
- prime, spec, plan, execute, ship
- ultrathink, carmack, aesthetic
- quality-check, triage, observe
- flesh, architect, debug

**Claude-specific** (don't sync):
- Commands that heavily use subagents
- Commands that depend on Claude-specific skills

**Adaptation rules**:

For **Codex** (prompts/*.md):
- Keep markdown format
- Add YAML frontmatter with name, description, aliases, enabled
- Reference Codex tools (rg, ast-grep, gemini CLI for research)
- Remove Claude-specific skill references

For **Gemini** (commands/*.toml):
- Convert to TOML format
- Use shell interpolation: `!{cat TODO.md}`, `!{ls -F}`
- Use `{{args}}` for arguments
- Keep prompts concise but complete

### 6. Apply Sync Policy

**SYNC** (must be consistent across all 3 CLIs):
- Ousterhout principles as default lens
- Red flags checklist
- **All 15 agent personalities** (8 specialists + 7 personas)
- Persona definitions and philosophies
- Core workflow commands
- Commit/PR standards
- Testing philosophy
- Code review checklists

**DIVERGE** (preserve tool strengths):
- **Claude**: Full subagent ecosystem via Task tool, skill library, MCP integrations, parallel agent composition
- **Codex**: Reasoning effort settings, simpler execution model, direct agent `.md` files
- **Gemini**: Shell interpolation `!{cmd}`, multimodal analysis, Google grounding, system instruction `.txt` files

### 7. Generate Sync Report

Output a clear report:

```markdown
## Sync Report

### Base Configuration
- AGENTS.md: [UPDATED/CREATED/UNCHANGED] - [line count] lines
- GEMINI.md: [UPDATED/CREATED/UNCHANGED] - [line count] lines

### Agents Synced (15 total)

| Agent | Codex (.md) | Gemini (.txt) | Notes |
|-------|-------------|---------------|-------|
| complexity-archaeologist | ✅ | ✅ | |
| data-integrity-guardian | ✅ | ✅ | |
| api-design-specialist | ✅ | ✅ | |
| test-strategy-architect | ✅ | ✅ | |
| error-handling-specialist | ✅ | ✅ | |
| state-management-analyst | ✅ | ✅ | |
| dependency-health-monitor | ✅ | ✅ | |
| documentation-quality-reviewer | ✅ | ✅ | |
| infrastructure-guardian | ✅ | ✅ | |
| grug | ✅ | ✅ | Full personality preserved |
| carmack | ✅ | ✅ | Full personality preserved |
| jobs | ✅ | ✅ | Full personality preserved |
| torvalds | ✅ | ✅ | Full personality preserved |
| ousterhout | ✅ | ✅ | Full personality preserved |
| fowler | ✅ | ✅ | Full personality preserved |
| beck | ✅ | ✅ | Full personality preserved |

### Commands Synced

| Command | Codex | Gemini | Notes |
|---------|-------|--------|-------|
| ultrathink | ✅ | ✅ | |
| execute | ✅ | ✅ | Carmack + Ousterhout composition preserved |
| plan | ✅ | ✅ | Grug complexity review preserved |
| simplify | ✅ | ✅ | 4-agent composition preserved |
| debug | ✅ | ✅ | Specialist routing preserved |
| spec | ✅ | ✅ | Jobs + domain experts preserved |
| groom | ✅ | ✅ | 15-agent parallel audit preserved |
| ... | | | |

### Commands Skipped (Claude-specific)
- [command]: [reason - e.g., depends on Task tool subagent spawning]

### Manual Attention Needed
- [any issues or warnings]

### Next Steps
1. Review generated files in ~/.codex/agents/ and ~/.gemini/system-instructions/
2. Test agent invocation in Codex and Gemini
3. Test commands in each tool
4. Run `/sync-configs` again after adding new agents or modifying commands
```

## Adaptation Guidelines

### Philosophy Adaptation

When porting philosophy content:

1. **Preserve the core** - Ousterhout principles, complexity focus, red flags
2. **Adapt the examples** - Use tool-appropriate references
3. **Maintain the tone** - Concise, direct, zero fluff
4. **Include personas** - Define Carmack/Jobs/Torvalds/Hara/Ousterhout vocabulary

### Command Adaptation

When porting commands:

1. **Preserve ALL richness** - Same personas, examples, red flags, philosophy, output formats
2. **Adapt the mechanics** - Shell interpolation for Gemini, tool refs for Codex
3. **NEVER strip content** - Gemini TOML should have identical depth to Claude md (only format changes)
4. **Test the output** - Verify commands work in target tool

**CRITICAL**: The Gemini TOML format can hold just as much content as Claude markdown. Converting format does NOT mean reducing content. A 400-line Claude command should become a 400-line Gemini command. Every persona quote, every red flag, every example must transfer.

**Anti-pattern to AVOID**: Stripping rich Claude prompts down to bare-bones Gemini commands. This destroys the prompt engineering that makes commands effective.

### TOML Format for Gemini

**CORRECT (Rich, complete prompt engineering):**

```toml
description = "Deep critical evaluation of plans for simplicity and system health"
prompt = """
# ULTRATHINK

> **THE MASTERS OF SIMPLICITY**
>
> **Steve Jobs**: "Simple can be harder than complex..."
> **John Ousterhout**: "The most fundamental problem in computer science is problem decomposition..."
> **John Carmack**: "It's done when it's right..."

You're an IQ 155 principal architect who's seen 50+ systems collapse under their own complexity...

## Your Mission
[Full mission with context question]

## The Ousterhout Framework

### 1. Complexity Analysis
[Full framework with bullet points, red flags]

### 2. Module Depth Evaluation
[Full evaluation criteria with formula, examples]

[... ALL sections from Claude version ...]

## Red Flags Checklist
- [ ] Shallow modules
- [ ] Information leakage
[... complete list ...]

## Output Format
[Full structured output template]

## Philosophy
[Rich closing philosophy section]
"""
```

**WRONG (Stripped down, lost all value):**

```toml
description = "Evaluate plans"
prompt = """
# ULTRATHINK

> Simple is better

Review the plan for issues.

## Process
1. Check complexity
2. Find problems
3. Report findings
"""
```

The first example preserves all prompt engineering. The second destroys it. **Always use the first pattern.**

## When to Run

- After adding/modifying agents in ~/.claude/agents/
- After significant changes to Claude Code commands
- After adding new skills you want everywhere
- After updating CLAUDE.md philosophy sections
- After modifying agent personalities or review checklists
- Periodically to catch drift (monthly)

## Example Sync

Running `/sync-configs` should:

1. Read ~/.claude/CLAUDE.md → generate adapted AGENTS.md and GEMINI.md
2. Read all 15 agents from ~/.claude/agents/*.md → generate:
   - ~/.codex/agents/*.md (full content, adapted tool refs)
   - ~/.gemini/system-instructions/*.txt (natural language format)
3. Read ~/.claude/commands/ultrathink.md → generate:
   - ~/.codex/prompts/ultrathink.md (adapted)
   - ~/.gemini/commands/ultrathink.toml (converted)
4. Read ~/.claude/commands/groom.md → generate:
   - ~/.codex/prompts/groom.md (15-agent composition adapted)
   - ~/.gemini/commands/groom.toml (15-agent invocation patterns converted)
5. Report what changed (agents, commands, configs)

The goal: run `codex` or `gemini` and get the same quality bar, same philosophy, same 15-agent perspectives, same workflow - just adapted for each tool's strengths.
