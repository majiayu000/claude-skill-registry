---
name: workflow-help
description: "Interactive guide to workflow system: agents, skills, routing, execution patterns."
effort: low
user-invocable: true
argument-hint: "[<topic>]"
allowed-tools:
  - Read
  - Grep
  - Glob
routing:
  triggers:
    - "how does routing work"
    - "what skills exist"
    - "system help"
    - "explain workflow"
    - "I am stuck"
    - "toolkit help"
  category: meta-tooling
  pairs_with:
    - workflow
    - do
---

# Workflow Help Skill

## Overview

This skill operates as an educational guide for repository workflows. It answers questions about how the agent/skill/routing architecture works, what tools and components are available, and when to use each workflow phase (brainstorm, plan, execute). The skill prioritizes accuracy over speed by reading actual SKILL.md and agent files rather than relying on memory.

---

## Instructions

### Phase 1: UNDERSTAND THE QUESTION

**Goal**: Determine exactly what the user wants to know about.

Parse the user's topic and $ARGUMENTS. Common categories:
- `brainstorm` / `plan` / `execute` - Workflow phases
- `skills` / `agents` / `hooks` - Component types
- `routing` / `do` - How routing works
- `subagent` - Subagent-driven execution
- No argument - Provide system overview

**Constraint (Over-Engineering Prevention)**: Answer only what was asked. Do not dump the entire system architecture when the user asks about one skill. Scope your response to the question asked, then offer to explain related concepts.

**Gate**: Topic identified. Proceed only when you know what to explain.

### Phase 2: GATHER ACCURATE INFORMATION

**Goal**: Read actual files before explaining anything.

**Step 1: Get authoritative data from the catalog script**

This constraint (Accuracy Over Speed) is non-negotiable. Counts and listings come from `scripts/list-capabilities.py`, which reads the generated INDEX files — deterministic, single source of truth. Match the question to the right subcommand:

| Question | Command | Output |
|----------|---------|--------|
| Overview / "how many skills/agents?" | `python3 scripts/list-capabilities.py summary` | Skills / Pipelines / Agents counts |
| "what skills exist [in category X]?" | `python3 scripts/list-capabilities.py skills [--category X] --brief` | Count; drop `--brief` for the full name/trigger/description table |
| "what agents exist?" | `python3 scripts/list-capabilities.py agents --brief` | Count; drop `--brief` for the full table |
| "tell me about <name>" | `python3 scripts/list-capabilities.py show <name>` | Type, description, triggers, category, file path for a skill/agent/pipeline |
| Fuzzy lookup / "is there a skill for X?" | `python3 scripts/list-capabilities.py search <query>` | Ranked name/trigger/description matches across skills, pipelines, agents |

`--category X` filters skills by keyword in name or description (e.g. `voice`, `game`, `kubernetes`); agents filter by exact category field. `show <name>` exits 1 when the name is absent — fall back to `search <name>` to suggest the closest match.

**Step 2: Read the actual file for deep questions**

The script gives authoritative counts, names, and one-line descriptions. For anything deeper — phases, gates, capabilities, when-to-use — read the file the script names in its `File:` field:

- For a specific skill: `Read skills/{path-from-show}/SKILL.md`
- For a specific agent: `Read agents/{agent-name}.md`
- For routing overview: Check the /do router configuration

Extract: name, description, version, what it CAN and CANNOT do, how to invoke it, related skills or agents.

**Staleness**: `summary`, `skills`, and `agents` exit 2 and print a stderr warning when source files are newer than the INDEX. If you see that warning, tell the user to regenerate: `python3 scripts/generate-skill-index.py` (skills) or `python3 scripts/generate-agent-index.py` (agents), then re-run.

**Constraint (No Fabrication)**: If a skill or agent does not exist, say so rather than inventing capabilities. If a skill or agent was recently deleted or merged, search with Glob for similar names and suggest the closest match.

**Gate**: Information gathered from actual files, not memory. Proceed only when gate passes.

### Phase 3: EXPLAIN CLEARLY

**Goal**: Present information in the format most useful for the user's question.

**For system overview**, lead with live counts from `python3 scripts/list-capabilities.py summary`, then present the execution architecture:

```
Router (/do) -> Agent (domain expert) -> Skill (methodology) -> Script (execution)
```

Then show key workflow:
1. BRAINSTORM - Clarify requirements, explore approaches
2. WRITE-PLAN - Break into atomic, verifiable tasks
3. EXECUTE - Direct or subagent-driven execution
4. VERIFY - Run tests, validate changes

**For specific components**, use this format:

```markdown
## [Component Name]
**Type**: Skill / Agent / Hook
**Invoke**: /command or skill: name
**Purpose**: One-sentence description
**Key Phases/Capabilities**: Bulleted list
**Related**: Links to related components
```

**For "when to use what"**, use a decision table:

| You Want To... | Use This |
|----------------|----------|
| Start a new feature | `/do implement [feature]` |
| Debug a bug | `/do debug [issue]` |
| Review code | `/do review [code]` |
| Execute an existing plan | `skill: subagent-driven-development` |
| Create a PR | `/pr-workflow` |

**Constraint (Show Real Examples)**: Reference actual skill names, commands, and file paths from this repository. Use tables for lists when presenting available skills, agents, and commands. Include invocation syntax for each component mentioned. Apply progressive disclosure: start with overview, offer deeper detail on request. Cross-reference related skills and agents when explaining one component.

**Step: Offer next steps**

After explaining, ask if the user wants to:
- Learn about a related component
- Actually execute a workflow (route to appropriate skill)
- See more detail on a specific aspect

**Constraint (Route When Appropriate)**: If user actually wants to execute a workflow, detect the execution intent and route to the correct skill instead of explaining it. For example, if user asks "how do I debug X" meaning "debug X for me", recognize the intent is execution and route to systematic-debugging, not an explanation of the debugging process.

**Gate**: User's question answered with information from actual files.

---

## Error Handling

### Error: "Skill or Agent Not Found"
Cause: User asked about a component that does not exist or was renamed
Solution:
1. Search with Glob for similar names
2. Check if it was recently deleted or merged
3. Suggest the closest matching component

### Error: "User Wants Execution, Not Explanation"
Cause: User asked "how do I debug X" meaning "debug X for me"
Solution:
1. Recognize the intent is execution, not education
2. Route to the appropriate skill (e.g., systematic-debugging)
3. Do not explain the debugging process; invoke it

### Error: "Stale INDEX"
Cause: `scripts/list-capabilities.py` exited 2 with a stderr warning — source files are newer than the generated INDEX
Solution:
1. Tell the user to regenerate: `python3 scripts/generate-skill-index.py` and/or `python3 scripts/generate-agent-index.py`
2. Re-run the catalog command; the counts now reflect current files
3. For deep content, read the file fresh rather than relying on cached descriptions

---

## References

### Core Constraints Embedded in Workflow

This skill is built on five hardcoded constraints that must always apply:

1. **CLAUDE.md Compliance**: Read and follow repository CLAUDE.md before answering any question
2. **Accuracy Over Speed**: Get counts and listings from `scripts/list-capabilities.py` (deterministic, INDEX-backed); read the actual SKILL.md and agent file for any deeper detail. Describe components from these sources, not from memory.
3. **Show Real Examples**: Reference actual skill names, commands, and file paths from this repository
4. **No Fabrication**: If a skill or agent does not exist, say so rather than inventing capabilities
5. **Route When Appropriate**: If user actually wants to execute a workflow, route to the correct skill instead of explaining it

The skill's default behaviors reinforce accuracy:
- Scope to the specific question asked (over-engineering prevention)
- Use tables for presenting lists of skills, agents, and commands
- Include invocation syntax for every component mentioned
- Apply progressive disclosure: start with overview, deepen on request
- Cross-reference related components when explaining one

Optional advanced modes (disabled by default):
- Full Architecture Dump: Explain the entire Router → Agent → Skill → Script pipeline
- Comparison Mode: Compare two skills or agents side-by-side
- Troubleshooting Guide: Help diagnose why a skill or route isn't working as expected

