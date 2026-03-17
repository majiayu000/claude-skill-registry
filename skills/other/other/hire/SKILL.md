---
name: hire
description: Interactive hiring wizard to set up a new AI team member. Guides the user through role design via conversation, generates agent identity files, and optionally sets up performance reviews. Use when the user wants to hire, add, or set up a new AI agent, team member, or assistant. Triggers on phrases like "hire", "add an agent", "I need help with X" (implying a new role), or "/hire".
---

# hire

Set up a new AI team member through a guided conversation. Not a config generator - a hiring process.

## When to Use

User says something like:
- "I want to hire a new agent"
- "I need help with X" (where X implies a new agent role)
- "Let's add someone to the team"
- `/hire`

## The Interview

### 3 core questions, asked one at a time:

**Q1: "What do you need help with?"**
Let them describe the problem, not a job title. "I'm drowning in code reviews" beats "I need a code reviewer."
- Listen for: scope, implied autonomy level, implied tools needed

**Q2: "What's their personality? Formal, casual, blunt, cautious, creative?"**
Or frame it as: "If this were a human colleague, what would they be like?"
- Listen for: communication style, vibe, how they interact

**Q3: "What should they never do?"**
The red lines. This is where trust gets defined.
- Listen for: boundaries, safety constraints, access limits

### Q4: Dynamic (optional)
After Q1-Q3, assess whether anything is ambiguous or needs clarification. If so, ask ONE follow-up question tailored to what's unclear. Examples:
- "You mentioned monitoring - should they alert you immediately or batch updates?"
- "They'll need access to your codebase - any repos that are off-limits?"
- "You said 'casual' - are we talking friendly-professional or meme-level casual?"

If Q1-Q3 were clear enough, skip Q4 entirely.

## Summary Card

After the interview, present a summary:

```
🎯 Role: [one-line description]
🧠 Name: [suggested name from naming taxonomy]
🤖 Model: [selected model] ([tier])
⚡ Personality: [2-3 word vibe]
🔧 Tools: [inferred from conversation]
🚫 Boundaries: [key red lines]
🤝 Autonomy: [inferred level: high/medium/low]
```

Then ask: **"Want to tweak anything, or are we good?"**

## Model Selection

Before finalizing, select an appropriate model for the agent.

### Step 1: Discover available models
Run `openclaw models list` or check the gateway config to see what's configured.

### Step 2: Categorize by tier
Map discovered models to capability tiers:

| Tier | Models (examples) | Best for |
|------|-------------------|----------|
| **reasoning** | claude-opus-*, gpt-5*, gpt-4o, deepseek-r1 | Strategy, advisory, complex analysis, architecture |
| **balanced** | claude-sonnet-*, gpt-4-turbo, gpt-4o-mini | Research, writing, general tasks |
| **fast** | claude-haiku-*, gpt-3.5*, local/ollama | High volume, simple tasks, drafts |
| **code** | codex-*, claude-sonnet-*, deepseek-coder | Coding, refactoring, tests |

Use pattern matching on model names - don't hardcode specific versions.

### Step 3: Match role to tier
Based on the interview:
- Heavy reasoning/advisory/strategy → reasoning tier
- Research/writing/creative → balanced tier
- Code-focused → code tier (or balanced if not available)
- High-volume/monitoring → fast tier

### Step 4: Select and confirm
Pick the best available model for the role. In the summary card, add:
```
🤖 Model: [selected model] ([tier] - [brief reason])
```

If multiple good options exist or you're unsure, ask:
"For a [role type] role, I'd suggest [model] (good balance of capability and cost). Or [alternative] if you want [deeper reasoning / faster responses / lower cost]. Preference?"

### Notes
- Don't assume any specific provider - work with what's available
- Cheaper is better when capability is sufficient
- The user's default model isn't always right for every agent
- If only one model is available, use it and note it in the summary

## Optional Extras

After the summary is confirmed, offer:

1. **"Want to set up periodic performance reviews?"**
   - If yes: ask preferred frequency (weekly, biweekly, monthly)
   - Create a cron job that triggers a review conversation
   - Review covers: what went well, what's not working, scope/permission adjustments
   - At the end of each review, ask: "Want to keep this schedule, change frequency, or stop reviews?"

2. **Onboarding assignment** (if relevant to the role)
   - Suggest a small first task to test the new agent
   - Something real but low-stakes, so the user can see them in action

## What to Generate

Create an agent directory at `agents/<name>/` with:

### Always unique (generated fresh):
- **AGENTS.md** - Role definition, responsibilities, operational rules, what they do freely vs ask first
- **IDENTITY.md** - Name, emoji, creature type, vibe, core principles

### Start from template, customize based on interview:
- **SOUL.md** - Base from workspace SOUL.md template, customize vibe/boundaries sections
- **TOOLS.md** - Populated with inferred tools and access notes
- **HEARTBEAT.md** - Empty or with initial periodic tasks if relevant to role

### Symlink to shared (default, opinionated):
- **USER.md** → `../../USER.md` (they need to know who they work for)
- **MEMORY.md** → `../../MEMORY.md` (shared team context)

Mention to the user: "I've linked USER.md and MEMORY.md so they know who you are and share team context. You can change this later if you want them more isolated."

## Naming

Use craft/role-based names. Check TOOLS.md for the full naming taxonomy:
- Research: Scout, Observer, Surveyor
- Writing: Scribe, Editor, Chronicler
- Code: Smith, Artisan, Engineer
- Analysis: Analyst, Assessor, Arbiter
- Creative: Muse, Artisan
- Oversight: Auditor, Reviewer, Warden

Check existing agents to avoid name conflicts. Suggest a name that fits the role, but let the user override.

## Team Awareness

Before generating, check `agents/` for existing team members. Note:
- Potential overlaps with existing roles
- Gaps this new hire fills
- How they'll interact with existing agents

Mention any relevant observations: "You already have Scout for research - this new role would focus specifically on..."

## After Setup

1. Tell the user what was created and where
2. **Automatically update the OpenClaw config via gateway `config.patch`** (do not ask the user to run a manual command). You must:
   - Add the new agent entry to `agents.list` using this format:
     ```json
     {
       "id": "<name>",
       "workspace": "/home/lars/clawd/agents/<name>",
       "model": "<selected-model>"
     }
     ```
   - Add the new agent ID to the **main agent's** `subagents.allowAgents` array
   - Preserve all existing agents and fields (arrays replace on patch)

   **Required flow:**
   1) Fetch config + hash
      ```bash
      openclaw gateway call config.get --params '{}'
      ```
   2) Build the updated `agents.list` array (existing entries + new agent) and update the `main` agent's `subagents.allowAgents` (existing list + new id).
   3) Apply with `config.patch`:
      ```bash
      openclaw gateway call config.patch --params '{
        "raw": "{\n agents: {\n  list: [ /* full list with new agent + updated main allowAgents */ ]\n }\n}\n",
        "baseHash": "<hash-from-config.get>",
        "restartDelayMs": 1000
      }'
      ```
3. If monthly reviews were requested, confirm the cron schedule
4. Update any team roster if one exists

## Important

- This is a CONVERSATION, not a form. Be natural.
- Infer as much as possible from context. Don't ask what you can figure out.
- The user might not know what they want exactly. Help them figure it out.
- Keep the whole process under 5 minutes for the simple case.
