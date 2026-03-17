---
name: quests
description: Track and guide humans through complex multi-step real-world processes. Use when a user needs help with a bureaucratic, legal, technical, or any multi-step procedure that requires organized tracking, step-by-step guidance, and progress monitoring. Triggers on requests like "help me with this process", "guide me through", "track this project", "create a quest", or any complex task that benefits from being broken into manageable steps presented one at a time. Also triggers for existing quests: "how's my quest going", "what's next on [process]", "update my progress". This is for multi-session/multi-day processes, not simple one-off tasks. The quest replaces scattered memory files — it IS the memory for long-running processes.
---

# Quests — Guided Process Framework

A standardized framework for AI agents to track and guide humans through complex long-term tasks. The quest is the **single source of truth** — context, decisions, contacts, risks, and progress live inside the quest, not scattered across memory files.

## Philosophy

- **One step at a time**: `quest next` shows only the current task — no overwhelm
- **Quest as memory**: `quest context` gives the agent everything needed in minimal tokens
- **Living document**: Steps can be added, removed, reordered, and modified at any time
- **Human-friendly**: `quest brief` generates summaries suitable for messaging

## CLI: `skills/quests/scripts/quest.py` (symlink as `quest`)

Data stored at `$WORKSPACE/data/quests.json`. Quest IDs are auto-generated from names (slugified).

### Conventions

- **Auto-resolution**: When only one quest is active, the quest argument is optional
- **Fuzzy matching**: Quests match by exact ID, ID prefix, or name substring
- **Optional args**: `quest done` with no step completes the current active step

### Quick Start
```bash
quest new "Fix car" --priority high --deadline 2026-06-01
quest add car "Get documents" --desc "Gather all paperwork"
quest substep car 1 "Find insurance certificate"
quest learn car "Tax exemption requires 12 months abroad"
quest decide car "Use contract dates as proof" --reason "No PERE registration"
quest contact car "Agency" --phone "555-1234" --role "Tax office"
quest next car                    # Present current step to human
quest done car 1.1                # Mark substep done
quest context car                 # Reload full context (~1K tokens)
```

### Resuming a Quest (New Session)
```bash
quest list                        # Find active quests
quest context myquest             # Load full state — replaces reading memory files
quest next myquest                # Present current step to human
```

### Commands Reference

**Quest lifecycle:**
- `new <name> [--desc] [--priority low|medium|high] [--deadline DATE] [--tags a,b]`
- `list [--all]` — list active (or all including archived)
- `delete <quest> [--archive]` — archive is reversible, delete is permanent

**Steps (fully flexible):**
- `add <quest> <title> [--desc]` — append a step
- `insert <quest> <position> <title> [--desc]` — insert at specific position
- `remove <quest> <step>` — remove a step or substep (e.g. `3` or `2.1`)
- `substep <quest> <step> <title>` — add substep to a step
- `done [quest] [step]` — complete step/substep (auto-advances to next)
- `skip [quest] [step]` — skip a step
- `block <quest> <step> <reason>` — mark step as blocked
- `unblock <quest> <step>` — unblock
- `edit <quest> [step] [--title] [--desc]` — edit step or quest-level fields
- `reorder <quest> <step> <position>` — move step to new position

**Context & Memory** (the core feature):
- `learn <quest> <fact>` — record a key fact (quest-level, affects all steps)
- `decide <quest> <decision> [--reason]` — record a decision with rationale
- `risk <quest> <concern>` — flag a risk or concern
- `note <quest> <step> <text>` — add a note to a specific step (step-level)
- `summarize <quest> <text>` — update the high-level context summary
- `context [quest] [--json]` — compact context dump (~500-1500 chars)
- `brief [quest]` — human-friendly summary for async messaging
- `log [quest] [-n LIMIT]` — timestamped activity log

> **`learn` vs `note`**: Use `learn` for facts that affect the whole quest ("Tax exemption requires 12 months"). Use `note` for step-specific info ("Carlos said he has the CoC already").

**Metadata:**
- `meta <quest> [--priority] [--deadline] [--tags a,b] [--remove]`
- `contact <quest> [name] [--phone] [--email] [--role] [--url]` — add or list contacts
- `link <quest> [url] [--label]` — add or list reference links

**Templates:**
- `template save <quest> [template_name]` — save quest structure as reusable template
- `template list` — list available templates
- `template use <template> [quest_name]` — create new quest from template

**Display:**
- `next [quest]` — current step only (for presenting to human)
- `show [quest] [-v]` — full quest with all steps and context
- `status [quest]` — quick progress overview

**Export:**
- `export <quest> [--file path]` — markdown export
- `json [quest]` — raw JSON (all quests if no arg)

## Agent Guidelines

### When (Not) to Create a Quest
- **Create**: Multi-session processes, bureaucratic tasks, anything >3 steps spanning multiple days
- **Don't create**: Simple one-off tasks, quick lookups, things that fit in one conversation

### Starting a New Quest
1. Create with `quest new` — set priority and deadline if known
2. Add 5-12 steps with `quest add` (use substeps for granularity)
3. Record initial facts with `quest learn`
4. Add contacts, links, and risks as discovered
5. Present first step with `quest next`

### Session Resumption
At the start of any session involving an existing quest:
1. `quest list` — check what's active
2. `quest context <id>` — reload full state (replaces reading memory files)
3. `quest next <id>` — see where the human left off

### During the Process
- Record everything: facts (`learn`), decisions (`decide`), risks (`risk`)
- Update summary with `quest summarize` as understanding evolves
- Add/remove/reorder steps freely as the process changes
- Use `quest brief` when messaging the human asynchronously (WhatsApp/Discord recap)
- Use `quest next` in interactive conversation

### Presenting to Humans
- **Always use `quest next`** — never show the full step list unprompted
- When human completes something → `quest done` → auto-advances
- When blocked → `quest block` with clear reason
- When human provides info → `quest learn` or `quest note`

### Multiple Active Quests
Auto-resolution only works with one active quest. When multiple are active, always specify the quest ID explicitly.

### Quest Completion
When all steps are done, the quest auto-completes. Consider:
- `quest export <quest> --file` to save a permanent record
- `quest template save` if the process might repeat
- `quest delete <quest> --archive` to clean up while preserving data

### Token Efficiency
- `quest context` outputs ~500-1500 chars with full situational awareness
- No need for separate memory files, trackers, or project docs
- The quest IS the memory — facts, decisions, contacts, risks, all in one place
- Use `quest context --json` for structured programmatic access
