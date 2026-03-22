---
name: skill-discovery
description: "Scan and catalog all available skills, agents, commands, hooks, and rules in the project. Use this skill whenever someone asks 'what skills are available', 'list agents', 'show me the registry', 'update the skill catalog', 'what can I use', 'what tools do I have', or any question about discovering, listing, or inventorying the project's AI capabilities. Also trigger when generating prompts that need to know what skills exist, or when setting up a new session and wanting to confirm available tooling."
---

# Skill Discovery

Scan and catalog all available skills, agents, commands, hooks, and rules in the project. Produces a structured `skills-registry.json` and presents a formatted summary.

## Steps

### Step 1: Run the Scanner

Execute the registry scanner script from the repo root:

```bash
cd "D:/ailocal/acm-ai" && bash .claude/skills/skill-discovery/scripts/scan_registry.sh
```

This generates `skills-registry.json` at the repo root with a full inventory of all capabilities.

### Step 2: Read the Generated Registry

Read the generated file:

```
D:/ailocal/acm-ai/skills-registry.json
```

### Step 3: Present a Formatted Summary

Present the results grouped by type. Use this format:

```
## Skills Registry Summary
Scanned at: <scanned_at>

### Skills (<count> total)
| Name | Description | Location | Platforms |
|------|-------------|----------|-----------|
| pydantic-models-py | Create Pydantic models... | .claude/skills/... | claude-code |
| ...  | ...          | ...      | ...       |

### Commands (<count> total)
| Name | Description |
|------|-------------|
| start | Start development services |
| ...  | ...         |

### Hooks (<count> total)
| Name | Trigger |
|------|---------|
| pre-tool-use.sh | PreToolUse |
| ...             | ...        |

### Rule Categories (from CLAUDE.md)
- Project Overview
- Essential Commands
- Architecture
- ...
```

### Step 4: Filter if Requested

If the user asks to filter (e.g., "show me debugging skills", "list only frontend skills"):

- Filter `skills` array by matching keywords against `name` and `description` fields
- Present the filtered subset using the same table format
- Note how many skills were hidden: "Showing 3 of 12 skills (filtered by 'debug')"

## Quick Reference

The following skills are available in this project (populated after first scan):

| Name | One-line Description |
|------|---------------------|
| `pydantic-models-py` | Create Pydantic v2 models following multi-model pattern |
| `acm-observability` | ACM-AI 6-tool observability stack reference |
| `systematic-debugging` | Structured debugging process before proposing fixes |
| `dispatching-parallel-agents` | Dispatch 2+ independent tasks in parallel |
| `subagent-driven-development` | Execute plans via focused sub-agents |
| `planning-with-files` | Persistent markdown-based planning for session continuity |
| `verification-before-completion` | Verify work before claiming completion |
| `skill-discovery` | This skill — scan and catalog all AI capabilities |

> Run the scanner to get the full up-to-date list including all installed skills.

## Notes

- Skills can live in `.claude/skills/` (Claude Code) or `.agents/skills/` (agent platform) or both
- Skills with `also_at` entries appear in multiple registries — they are the same skill
- The registry is regenerated on each scan; commit `skills-registry.json` to track changes over time
- Hooks are found in `.claude/hooks/` — they run automatically based on trigger type
- Commands are in `commands/` (surreal-commands worker handlers, not slash commands)
