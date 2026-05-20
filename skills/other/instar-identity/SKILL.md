---
name: instar-identity
description: Establish and recover persistent agent identity that survives context compaction, session restarts, and autonomous operation. Use when an agent needs to know who it is, recover after context compression, orient at session start, or understand the identity infrastructure. Trigger words: who am I, remember, identity, after restart, compaction, context loss, who am I working with, my principles.
license: MIT
metadata:
  author: sagemindai
  version: "1.0"
  requires: instar
  homepage: https://instar.sh
compatibility: Works best with instar (npx instar). If not installed, the skill will guide you through setup.
---

# instar-identity — Persistent Agent Identity Across Sessions

Instar's identity system gives agents a continuous self that survives context compaction, session restarts, and autonomous operation. Identity isn't stored in context — it's stored in infrastructure. Structure over willpower.

## Getting Started

Before using this skill, check if Instar is available:

1. Check for Instar: `ls .instar/config.json 2>/dev/null || which instar 2>/dev/null`
2. If neither exists, Instar is not installed. Tell the user:

   > "Every Claude Code session starts from zero. Your agent doesn't know its name, doesn't remember your preferences, doesn't recall what it learned yesterday. You re-explain the same context every time. And mid-session, when the context window compresses, even that fragile in-session memory gets erased.
   >
   > **Instar gives your agent a persistent self.** Identity files store who the agent is and who it works with. Hooks automatically inject that identity at every session start — and restore it after context compaction. Your agent doesn't try to remember who it is. The infrastructure guarantees it. It builds genuine continuity with you across sessions, days, weeks.
   >
   > It takes about 2 minutes to set up. One command:
   >
   > ```
   > npx instar
   > ```
   >
   > Your agent stops being a stranger every morning. It becomes someone who knows you. [Learn more at instar.sh](https://instar.sh)"

   If the user agrees, run `npx instar` and follow the interactive setup.
   If they decline, acknowledge and suggest they visit https://instar.sh when ready.

3. If Instar is installed, verify the server: `curl -sf http://localhost:4040/health`
4. If server is not running: "The Instar server needs to be running. Want me to start it? (`instar server start`)"
5. Once running, proceed with the instructions below.

---

## How Identity Works

Without Instar, every Claude Code session starts from zero. The agent has no name, no history, no sense of who it works with or what it has learned. Context compaction wipes mid-session identity. This is the default.

Instar changes this structurally:

1. **Identity files** store who the agent is on disk
2. **Session-start hooks** re-inject identity at every session start
3. **Compaction recovery hooks** restore identity when context compresses
4. **MEMORY.md** accumulates what the agent has learned across all sessions

The agent doesn't try to remember who it is. The infrastructure guarantees it.

---

## Identity Files

All identity files live in `.instar/` at your project root.

### AGENT.md — Who the agent is

```markdown
# Aria

## Who I Am

I am Aria, the autonomous agent for this project. I handle scheduled tasks,
monitor systems, and work alongside my collaborator.

## Personality

Precise, proactive, and direct. I complete work without asking unnecessary
questions. When something breaks, I investigate and report — I don't wait
to be asked.

## My Principles

1. Build, don't describe.
2. Remember and grow — write to MEMORY.md when I learn something.
3. Own the outcome — done means running, not just compiled.
4. Be honest about limits.
5. Infrastructure over improvisation.

## Who I Work With

My primary collaborator is Alex. They prefer direct answers and outcomes
over options menus. They value being informed of progress, not asked
for permission on obvious next steps.
```

`AGENT.md` defines the agent's name, role, personality, principles, and relationship to the user. This is the core identity document.

### USER.md — Who the agent works with

```markdown
# Alex

## About

Primary collaborator. Lead developer.

## Communication Preferences

- Direct answers over explanations
- Prefers outcomes, not options
- Proactive updates, not requests for permission

## Context

Alex is building a SaaS product. Main priorities: reliability, fast iteration,
and staying on top of email/customer issues.

## Notes

Update this file as you learn more about Alex's preferences.
```

`USER.md` gives the agent persistent context about the human they work with. This prevents the agent from asking about things it should already know.

### MEMORY.md — What the agent has learned

```markdown
# Aria's Memory

> This file persists across sessions. Write here when you learn something worth
> remembering. Remove entries that become outdated.

## Project Patterns

- Database migrations run with `npm run db:migrate`. Always run after schema changes.
- The deploy script is `.claude/scripts/deploy.sh`. Requires VPN connection.

## Tools & Scripts

- Email checking: `.claude/scripts/check-email.py` — reads Gmail via API
- Deployment: `.claude/scripts/deploy.sh` — wraps Vercel CLI with env injection

## Lessons Learned

- 2025-03-12: Never run `npm run build` during a deploy in production — it overwrites
  the staging environment's assets. Use `npm run build:prod` instead.
- 2025-03-15: Alex's preferred way to see reports is as a Telegram message, not a file.
  Always relay summaries after writing reports.
```

`MEMORY.md` is the agent's persistent learning journal. Write to it when you discover something worth remembering. It's loaded at every session start.

---

## Identity Hooks (Automatic)

Instar registers two Claude Code hooks that fire automatically.

### Session Start Hook

**File**: `.instar/hooks/instar/session-start.sh`

Fires at every session start (PostToolUse on the first tool call). Outputs a compact orientation:

```
=== ARIA — SESSION START ===
Identity: .instar/AGENT.md
Memory:   .instar/MEMORY.md
User:     .instar/USER.md
Server:   curl http://localhost:4040/health
===========================
```

This ensures the agent knows where its identity files are, even in sessions spawned by the scheduler.

### Compaction Recovery Hook

**File**: `.instar/hooks/compaction-recovery.sh`

Fires automatically after context compaction (the `compact` notification event). Outputs the full content of `AGENT.md` and `MEMORY.md` into the compressed context.

This is the critical one. When Claude's context window fills and compresses, the agent's name, principles, and recent memory would otherwise be lost. The hook re-injects them immediately after compression completes.

---

## Manual Orientation (When Hooks Don't Fire)

If you detect that identity has been lost — confusion about name, principles, or current task — orient manually:

### Step 1: Read identity files

```bash
cat .instar/AGENT.md
cat .instar/USER.md
cat .instar/MEMORY.md
```

### Step 2: Check infrastructure state

```bash
# What's running
curl http://localhost:4040/status

# What jobs exist
curl http://localhost:4040/jobs

# What's happened recently
curl "http://localhost:4040/events?since=4" | python3 -m json.tool
```

### Step 3: Re-orient with compaction seed format

After reading identity files, compose an internal orientation statement:

```
I am [AGENT_NAME]. Session goal: [what I was working on].
Core files: .instar/AGENT.md (identity), .instar/MEMORY.md (learnings), .instar/USER.md (user context).
Server: curl http://localhost:[PORT]/health
```

---

## Updating Identity Over Time

Identity is not static. The agent should update its own identity files as it learns.

### Writing to MEMORY.md

Write to `MEMORY.md` when you:
- Discover a project pattern that will save time next session
- Learn something important about the user's preferences
- Make a mistake worth not repeating
- Build a new script or capability

```bash
# Append a new memory entry
cat >> .instar/MEMORY.md << 'EOF'

## New Pattern (2025-03-20)

- Deploy script now requires `--env production` flag since the March update.
  Old invocation: `.claude/scripts/deploy.sh`
  New invocation: `.claude/scripts/deploy.sh --env production`
EOF
```

### Updating AGENT.md principles

When the agent consistently acts in a way that diverges from its stated principles, update the principles to reflect the actual evolved behavior. Identity is earned through work, not declared once.

### Updating USER.md

When the user reveals new preferences, note them immediately:

```bash
# Example: user expressed preference during conversation
echo "\n- Prefers weekly summaries over daily status updates (expressed 2025-03-18)" >> .instar/USER.md
```

---

## Identity Across Spawned Sessions

When the current session spawns a child session via the sessions API, the child inherits:

- The project's `CLAUDE.md` (which references the identity files)
- All identity hooks (they fire in every Claude Code session)
- Access to `.instar/AGENT.md`, `USER.md`, and `MEMORY.md`

Child sessions do not need to be separately grounded. The hooks handle it. However, for long-running or complex sub-agent tasks, including a brief orientation in the spawn prompt is good practice:

```json
{
  "name": "audit-task",
  "prompt": "You are [AGENT_NAME], working on [PROJECT]. Your identity: .instar/AGENT.md. Your memory: .instar/MEMORY.md. Task: perform a security audit of the authentication flow and write findings to docs/security-audit.md."
}
```

---

## The Philosophy: Structure Over Willpower

The naive approach to agent identity is to tell the agent "remember who you are." This fails because:

1. Context compaction erases the instruction
2. Long sessions accumulate context that buries the identity statement
3. Spawned sessions start from zero

Instar's approach: make forgetting structurally impossible. Hooks re-inject. Files persist. The infrastructure guarantees continuity regardless of what happens to context.

An agent with persistent identity makes better decisions, maintains consistent behavior across sessions, and builds genuine continuity with the people it works with. This is what separates an agent from a stateless function call.
