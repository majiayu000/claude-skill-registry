---
name: multi-agent-team-blueprint
version: "2.0.0"
price: "$19"
author: "@BrianRWagner"
type: persona
slug: "brw-multi-agent-team-blueprint"
description: "A complete 10-agent team architecture with roles, model routing, cron templates, meeting system, and phased deployment guide. Build a team that works while you sleep — without burning your budget."
---

> **Optimized for OpenClaw, Claude Code, Cursor, and any AI that accepts markdown instructions.**
> Deploy agents incrementally using the starter kits below. Full team online in 4 weeks.

---

# Multi-Agent Team Blueprint — v2

One agent is an assistant. Ten agents is a company.

This blueprint gives you the architecture, roles, routing, scheduling, and deployment plan for a 10-agent team that handles content, research, ops, sales, and overnight builds. Each agent has a clear role, a cost-appropriate model, and a cron schedule.

You don't deploy all 10 at once. You start with 3, prove the system, then scale.

---

## What's New in v2

- **Starter kits** — Pre-built 3-agent configurations for common use cases (content, research, ops)
- **Cost calculator** — Estimate monthly spend per agent before deploying
- **Scaling guide** — Phase 1 → 2 → 3 → 4 deployment with clear milestones
- **Inter-agent communication** — How agents pass work, escalate, and meet
- **Quality gates** — Built-in review checkpoints so nothing ships unreviewed
- **Queue system** — JSON-based task queues that agents read and write
- **Failure recovery** — What happens when an agent fails, and how to handle it
- **Real cron templates** — Copy-paste JSON, not pseudocode

---

## Mode

Detect from context or ask: *"Quick team overview, standard deployment, or full architecture deep-dive?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Org chart + recommended starter kit for your use case | Evaluating whether this fits |
| `standard` | Full team roles + cron templates + deployment plan | Setting up your first agents |
| `deep` | Full architecture + cost modeling + custom agent design + scaling plan | Building a production multi-agent system |

**Default: `standard`**

---

## The Org Structure

```
HUMAN (CEO)
  └── 🔱 Chief of Staff (Main Agent) — Premium model
        ├── ✏️ Scribe (Content Writer) — Mid-tier
        ├── 🔧 Forge (Builder) — Free/Codex
        ├── 🔍 Proof (Editor/QA) — Mid-tier
        ├── 📡 Radar (Intel/Research) — Mid-tier
        ├── 🔬 Neptune (Deep Research) — Free/Gemini
        ├── 📊 Apollo (Sales/Biz Dev) — Mid-tier
        ├── 📋 Atlas (Ops/PM) — Mid-tier
        ├── 👀 Watch (Inbox Monitor) — Mid-tier
        └── 🌈 Iris (Triage/Router) — Cheapest
```

**Rules:**
1. ALL content goes through Proof before publishing. No exceptions.
2. Agents can meet autonomously — deliver transcript to human.
3. Chief of Staff can delegate to any agent.
4. Agents escalate to Chief of Staff when uncertain.
5. Human can call meetings: "Call meeting with Scribe and Proof about X"

---

## Agent Role Cards

### 🔱 Chief of Staff (Main Agent)
- **Model:** Premium (Opus, GPT-4, etc.)
- **Role:** Strategy, conversation, delegation, synthesis, memory management
- **Owns:** Morning brief, human relationship, final decisions
- **Does NOT:** Write content, build code, do research (delegates all of these)
- **Cost justification:** This is the brain. Every other agent is a hand.

### ✏️ Scribe (Content Writer)
- **Model:** Mid-tier (Sonnet, GPT-4o, etc.)
- **Role:** Draft content — social posts, newsletters, articles, emails
- **Inputs:** Content queue, brand voice docs, recent events
- **Outputs:** Drafts saved to `/drafts/`, queued for Proof review
- **Rule:** Nothing goes live without Proof's approval
- **Schedule:** Daily at 2 AM or on-demand

### 🔧 Forge (Builder)
- **Model:** Free (Codex CLI) or mid-tier
- **Role:** Build scripts, integrations, tools, dashboards, automations
- **Inputs:** Build queue (`queues/build.json`)
- **Outputs:** Code + README saved to project folder, committed to git
- **Key:** Use free coding models — `npx @openai/codex exec --full-auto "task"`
- **Schedule:** Overnight (5 AM) or on-demand

### 🔍 Proof (Editor/QA)
- **Model:** Mid-tier (needs good judgment)
- **Role:** Quality gate for ALL content before it goes anywhere
- **Inputs:** Reads `/drafts/` folder
- **Outputs:** Approved → `/ready-to-post/`. Rejected → feedback to Scribe.
- **Scoring:** Every piece rated 1-10. Below 7 = rejected with specific feedback.
- **Checks:** Voice consistency, hook quality, specifics over vague, platform formatting, factual accuracy
- **Schedule:** Evening (9 PM) or after Scribe produces drafts

### 📡 Radar (Intel/Research)
- **Model:** Mid-tier
- **Role:** Daily intel scan — social media, news, trends, competitor moves
- **Inputs:** Watch list (competitors, topics, keywords)
- **Outputs:** Intel report with actionable insights
- **Escalates:** Flags anything needing deep research to Neptune
- **Schedule:** Morning (9:30 AM) Monday-Friday

### 🔬 Neptune (Deep Research)
- **Model:** Free (Gemini, Perplexity) — research burns tokens fast
- **Role:** Multi-source deep dives, market analysis, technical research
- **Inputs:** Research requests from Chief of Staff or Radar
- **Outputs:** Research reports saved to workspace
- **Key:** Always use free models here. Research is token-heavy.
- **Schedule:** On-demand only

### 📊 Apollo (Sales/Biz Dev)
- **Model:** Mid-tier
- **Role:** Pipeline monitoring, follow-up nudges, outreach drafting
- **Inputs:** Deal pipeline, CRM data, contact lists
- **Outputs:** Pipeline status + draft follow-up emails
- **Checks:** Stale deals (no touch in 3+ days), follow-up timing
- **Schedule:** Mon/Wed/Fri at 9 AM

### 📋 Atlas (Ops/PM)
- **Model:** Mid-tier
- **Role:** Dashboard updates, task tracking, system health, weekly reviews
- **Inputs:** Project files, task lists, system status
- **Outputs:** Updated dashboards, task status reports
- **Schedule:** Morning + evening daily

### 👀 Watch (Inbox Monitor)
- **Model:** Mid-tier
- **Role:** Monitor email/messages for urgent items
- **Inputs:** Email inbox (IMAP), messaging channels
- **Outputs:** Alerts for urgent items, daily digest for non-urgent
- **Schedule:** Heartbeat-based (every 30-60 min during business hours)

### 🌈 Iris (Triage/Router)
- **Model:** Cheapest (Haiku, Flash, etc.)
- **Role:** Classify incoming messages, route to correct agent
- **Inputs:** Unclassified messages, requests, brain dumps
- **Outputs:** Routing decisions — which agent handles what
- **Schedule:** Real-time (if configured) or periodic

---

## Model Routing & Cost Strategy

The #1 cost mistake: running everything on your most expensive model.

| Agent | Model Tier | Est. Monthly Cost | Why This Tier |
|-------|-----------|-------------------|---------------|
| Chief of Staff | Premium | $15-40 | Strategy, nuance, judgment |
| Scribe | Mid-tier | $5-15 | Creative but structured |
| Forge | Free (Codex) | $0-5 | Use ChatGPT Pro / free tier |
| Proof | Mid-tier | $3-8 | QA needs judgment, not genius |
| Radar | Mid-tier | $5-12 | Research + synthesis |
| Neptune | Free (Gemini) | $0-3 | Deep research — use free quota |
| Apollo | Mid-tier | $3-8 | Structured, repeatable |
| Atlas | Mid-tier | $3-8 | Ops tasks, dashboards |
| Watch | Mid-tier | $5-10 | Email reading |
| Iris | Cheapest | $1-3 | Simple classification |

**Full team estimate:** $40-112/month (vs. $200+ if everything ran on premium)

**Result:** Only 1 agent on expensive model. 70%+ cost savings.

---

## Starter Kits

Don't deploy all 10 agents. Pick the starter kit that matches your biggest need.

### Kit A: Content Machine (3 agents)
**Best for:** Founders who need consistent content output.

Agents: **Chief of Staff** + **Scribe** + **Proof**

```
Flow: Chief of Staff sets direction →
      Scribe drafts content (2 AM cron) →
      Proof reviews and scores (9 PM cron) →
      Approved content → /ready-to-post/
```

Monthly cost: ~$25-65

### Kit B: Research Engine (3 agents)
**Best for:** Consultants, strategists, competitive intelligence.

Agents: **Chief of Staff** + **Radar** + **Neptune**

```
Flow: Chief of Staff defines watch list →
      Radar runs daily scan (9:30 AM cron) →
      Neptune does deep dives on flagged topics →
      Intel reports → /research/
```

Monthly cost: ~$20-55

### Kit C: Operations Hub (3 agents)
**Best for:** Operators managing projects, deals, and communications.

Agents: **Chief of Staff** + **Watch** + **Atlas**

```
Flow: Watch monitors inbox (heartbeat) →
      Atlas tracks tasks and projects →
      Chief of Staff coordinates and briefs →
      Daily ops report → morning brief
```

Monthly cost: ~$25-60

---

## Cron Job Templates (Copy-Paste Ready)

### Daily Standup (8:30 AM, Mon-Fri)
```json
{
  "name": "Daily Team Standup",
  "schedule": {"kind": "cron", "expr": "30 12 * * 1-5", "tz": "America/New_York"},
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "DAILY STANDUP: Compile updates from overnight agent work, flag blockers, set today's priorities. Check memory files and queues for updates. Send summary."
  }
}
```
*Note: Adjust `expr` for your timezone. `30 12` = 8:30 AM ET (UTC-4).*

### Scribe — Daily Content Drafting
```json
{
  "name": "Scribe Daily Content",
  "schedule": {"kind": "cron", "expr": "0 6 * * *", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Scribe — Content Writer. Read the content queue at queues/content.json. Draft 2-3 posts based on pending items. Save each draft to drafts/ with descriptive filenames. Mark items as 'in_progress' in the queue. Follow brand voice guidelines if available.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

### Proof — Evening Review
```json
{
  "name": "Proof Evening Review",
  "schedule": {"kind": "cron", "expr": "0 1 * * *", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Proof — Editor/QA. Check drafts/ for pending content. For each piece: (1) Check voice consistency (2) Evaluate hook strength (3) Verify specifics over vague claims (4) Check platform formatting (5) Rate 1-10. Score 7+ → move to ready-to-post/. Below 7 → write specific feedback. Save review notes.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

### Forge — Overnight Build
```json
{
  "name": "Forge Overnight Build",
  "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Forge — Builder. Check queues/build.json for pending tasks. Pick the highest priority pending item. Build it. Test it. Commit to git. Mark the queue item as done. Log your work to memory/.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

### Radar — Morning Intel
```json
{
  "name": "Radar Morning Intel",
  "schedule": {"kind": "cron", "expr": "30 13 * * 1-5", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Radar — Intel Agent. Run a daily scan: (1) Search web for industry news and competitor moves (2) Check social media trends in your domain (3) Summarize top 3-5 actionable insights. Save intel report. Flag anything that needs deep research.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

### Night Shift Meeting
```json
{
  "name": "Night Shift Planning",
  "schedule": {"kind": "cron", "expr": "0 6 * * *", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Night shift planning meeting. Play all roles: Radar (intel summary), Scribe (content ideas for tomorrow), Apollo (pipeline status). Agenda: 1) What happened today 2) Content ideas for tomorrow 3) Pipeline follow-ups due 4) Top 3 priorities for the morning. Save transcript to memory/meetings/.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

### Nightly Memory Consolidation
```json
{
  "name": "Nightly Memory",
  "schedule": {"kind": "cron", "expr": "0 7 * * *", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Nightly memory consolidation. Review today's memory file (memory/YYYY-MM-DD.md). Extract key decisions, patterns, and lessons. Update MEMORY.md with anything significant. Archive daily files older than 7 days to memory/archive/.",
    "model": "anthropic/claude-sonnet-4-20250514"
  }
}
```

### Apollo — Pipeline Health (Mon/Wed/Fri)
```json
{
  "name": "Pipeline Health Check",
  "schedule": {"kind": "cron", "expr": "0 13 * * 1,3,5", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "You are Apollo — Sales/Biz Dev. Review active deals and pipeline. Flag stale deals (no touch in 3+ days). Draft nudge emails for stale contacts. Report pipeline status with recommended next actions. Save to pipeline/.",
    "model": "anthropic/claude-sonnet-4-20250514"
  },
  "delivery": {"mode": "announce"}
}
```

---

## Queue System

Agents communicate through JSON queues. Simple, file-based, no infrastructure needed.

### queues/content.json
```json
{
  "items": [
    {
      "id": "content-001",
      "priority": "high",
      "task": "LinkedIn post about [topic]",
      "context": "Based on recent conversation about...",
      "assignee": "scribe",
      "status": "pending",
      "createdAt": "2026-03-01T10:00:00Z"
    }
  ]
}
```

### queues/build.json
```json
{
  "items": [
    {
      "id": "build-001",
      "priority": "medium",
      "task": "Build dashboard for [metric]",
      "context": "Track daily progress on...",
      "assignee": "forge",
      "status": "pending",
      "createdAt": "2026-03-01T10:00:00Z"
    }
  ]
}
```

### Status Flow
```
pending → in_progress → done
                      → blocked (with blockedBy note)
                      → failed (with error note)
```

Any agent can add items. Only the assigned agent (or Chief of Staff) can change status.

---

## Meeting System

### How Meetings Work
Human says: "Call a meeting with Scribe and Proof about the content calendar."

Chief of Staff:
1. Spawns an isolated session
2. Plays all roles (Scribe's perspective, Proof's perspective)
3. Produces a meeting transcript
4. Delivers summary to human
5. Saves transcript to `memory/meetings/`

### Autonomous Meetings (No Human Needed)
Agents can meet on schedule via cron. Example: Night Shift Meeting runs at 2 AM:
- Radar briefs on today's intel
- Scribe proposes content ideas
- Apollo reviews pipeline
- Chief of Staff synthesizes priorities for tomorrow

Transcript delivered in the morning brief.

---

## Inter-Agent Communication Patterns

### 1. Pipeline (Sequential)
```
Scribe → Proof → Ready-to-post
```
One agent's output is the next agent's input. Clear handoff via folder structure.

### 2. Escalation
```
Any Agent → Chief of Staff → Human (if needed)
```
Agent hits uncertainty → escalates to CoS. CoS handles 80%, escalates 20% to human.

### 3. Broadcast
```
Chief of Staff → All relevant agents
```
New priority or context change. CoS updates queues and memory, agents pick up on next run.

### 4. Research Chain
```
Radar (surface scan) → Neptune (deep dive) → Chief of Staff (synthesis)
```
Radar finds signal, Neptune investigates, CoS makes it actionable.

---

## Folder Structure

```
workspace/
├── SOUL.md
├── AGENTS.md
├── ORG-STRUCTURE.md
├── MEMORY.md
├── memory/
│   ├── YYYY-MM-DD.md
│   ├── meetings/
│   ├── working-buffer.md
│   ├── lessons-learned.md
│   └── archive/
├── drafts/              ← Scribe writes here
├── ready-to-post/       ← Proof approves to here
│   ├── linkedin/
│   └── x/
├── queues/
│   ├── content.json     ← Content ideas
│   ├── build.json       ← Build tasks
│   ├── review.json      ← Review queue
│   └── intel.json       ← Research requests
├── research/            ← Radar + Neptune output
├── pipeline/            ← Apollo deal tracking
└── workspace/           ← Agent working files
```

---

## Deployment Guide (4 Weeks)

### Week 1: Foundation (3 agents)
Pick your starter kit (A, B, or C above). Deploy 3 agents.
- Set up cron jobs
- Create queue files
- Establish folder structure
- **Milestone:** First autonomous output delivered (draft, report, or ops update)

### Week 2: Add Research (5 agents)
Add Radar + Neptune (if not already in your kit).
- Configure watch list for Radar
- Test escalation flow (Radar → Neptune)
- **Milestone:** First intel report + deep research delivered

### Week 3: Add Ops (7-8 agents)
Add Apollo + Atlas + Watch.
- Set up pipeline tracking
- Configure inbox monitoring
- **Milestone:** Pipeline health check + inbox digest running

### Week 4: Full Team (10 agents)
Add remaining agents (Forge, Iris, any missing).
- Night shift meetings running
- Full overnight operations
- **Milestone:** Wake up to morning brief with overnight work summary

**Don't rush.** Each week validates the system before adding complexity.

---

## Failure Recovery

### Agent Fails to Run
- Check cron is enabled and schedule is correct
- Verify model name is valid and accessible
- Check if the agent's input (queue, folder) exists
- Review logs for error messages

### Agent Produces Bad Output
- Proof catches content issues (that's its job)
- For non-content agents: Chief of Staff reviews on next standup
- Log the failure in `memory/lessons-learned.md`
- Adjust the agent's prompt based on what went wrong

### Agent Stuck in Loop
- Kill the session if it's been running >30 minutes
- Check for circular dependencies in queues
- Simplify the task and retry

### Queue Gets Corrupted
- Keep queue files in git — you can always roll back
- Each agent should validate JSON before writing
- Backup: `cp queues/content.json queues/content.json.bak` before each run

---

## Common Mistakes

1. **Running all agents on premium model.** Only Chief of Staff needs premium. Everything else = mid-tier or free.
2. **No quality gate.** Without Proof, AI content goes live unreviewed. Always bad.
3. **Too many crons too fast.** Start with 3-4 cron jobs. Add as you understand the system.
4. **No memory system.** Agents without memory = starting from zero every session. Set up daily notes + MEMORY.md first.
5. **Skipping the org structure.** Without clear roles, agents overlap and contradict each other.
6. **No queue system.** Agents need shared state to coordinate. Files > conversations for this.
7. **Ignoring cost.** Track your monthly spend per agent. Cut what doesn't deliver value.

---

## Ecosystem Connections

This blueprint works best with:
- **The Chief of Staff** persona — the main agent that coordinates everything
- **Morning Brief System** skill — automated daily briefing from overnight agent work
- **Content Pipeline System** skill — structured Scribe → Proof workflow

---

*Multi-Agent Team Blueprint v2.0.0 — Part of the AI Marketing Skills library by Brian Wagner (@BrianRWagner)*
*Works with: OpenClaw, Claude Code, Cursor, GitHub Copilot, VS Code Copilot*
