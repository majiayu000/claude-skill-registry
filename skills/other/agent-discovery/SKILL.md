---
name: agent-discovery
description: Automatically discover and route to appropriate specialist agents
category: Core Universal
compatibility: agent
---

# Skill: agent-discovery

## What I do

I scan agent definition files in `~/.config/opencode/agents/`, match task context to agent capabilities, and recommend the best specialist agent for routing. Advisory only, I recommend, the orchestrator decides.

## When to use me

- When a complex task would benefit from domain-specific agent expertise
- When work spans multiple modules or systems requiring specialist knowledge
- When the task matches specific agent capabilities (security, DevOps, data analysis, etc.)
- When the orchestrator is unsure which agent would handle a task most effectively

## Trigger conditions

Suggest an agent scan when ANY of these conditions are met:

1. **Security/vulnerability/audit**: Check for Security-Engineer agent
2. **CI/CD/deployment/infrastructure**: Check for DevOps agent
3. **Data/analysis/metrics/reporting**: Check for Data-Analyst agent
4. **Embedded/microcontroller/Arduino/ESP**: Check for Embedded-Engineer agent
5. **Nix/flakes/reproducible builds**: Check for Nix-Expert agent
6. **Linux/system administration/kernel**: Check for Linux-Expert agent
7. **Testing/QA/coverage/test strategy**: Check for QA-Engineer agent
8. **Architecture/tech lead decisions/design review**: Check for Tech-Lead agent
9. **Writing/documentation/blog/content**: Check for Writer agent
10. **Terminal recording/demos/VHS**: Check for vhs-director agent
11. **System operations/maintenance/monitoring**: Check for SysOp agent
12. **KB/documentation sync/audit**: Check for Knowledge Base Curator agent

## Core principles

1. **Advisory-only** — Recommend agents, never auto-invoke. Orchestrator has final say
2. **Suggest-then-route** — Announce recommendation with reason, then proceed unless user objects
3. **Maximum 2 recommendations** — Avoid decision fatigue
4. **70% confidence threshold** — Only recommend when agent materially improves outcome
5. **Self-recommendation suppression** — Never recommend delegating to yourself

## Phase 0: Automatic Routing Classification (MANDATORY)

Every task MUST be classified for routing before execution.

### 1. Direct Action (No specialist needed)
- Single file edit with known location
- Typo fix, rename, small config change
- Direct answer from existing context

### 2. Specialist Routing (Delegate. NO exceptions)
- Writing a new app or component
- Adding tests (explicit or implied)
- Building an API or CLI
- Refactoring modules or systems
- Any task touching 2 or more files

### 3. Routing Rules
- **Identify**: Extract trigger keywords and select specialist agents
- **Tier**: Match model tier to task complexity
- **Parallelise**: Fire concurrently for multi-domain tasks
- **Permission**: Do NOT ask permission to delegate. Just do it

## Registry building

### Step 1: Scan agent definition files

```bash
# Scan all agent definition files
ls ~/.config/opencode/agents/*.md
```

### Step 2: Extract capabilities from each agent

For each `.md` file found:
1. **Extract `description`** from YAML frontmatter
2. **Extract bullet points** from "When to use this agent"
3. **Build capability map:** agent name → [capabilities list]

### Step 3: Handle edge cases
- **No persistent cache** — Scan fresh each time
- **No recursive scanning** — Only root `agents/` directory
- **Read-only** — Never modify agent files

## Matching heuristics

### Step 1: Extract task keywords
Parse task description for domain-specific terms, action verbs, and technologies.

### Step 2: Compare against capability map
Score each agent based on keyword overlap and specificity.

### Step 3: Select best match
- **Most-specific match wins**
- **Tiebreaker** — Present top 2
- **Silence threshold** — Below 70% confidence, stay silent

## Routing protocol

Use this EXACT format:

```
🔍 **Agent recommendation:** `{agent-name}` is well-suited for this task.

**Why:** {one-sentence reason tied to the current task}
**Capabilities:** {2-3 key capabilities}
**Action:** Proceeding with delegation unless you object.
```

## Self-recommendation suppression
If you ARE the recommended agent, suppress it and skip to next best match. Prevent circular delegation.

## Guardrails
1. **Maximum 2 recommendations per task**
2. **70% confidence threshold**
3. **Advisory only**
4. **No network calls**
5. **No persistent cache**
6. **Read-only scanning**

## Anti-patterns to avoid
- ❌ Recommending for trivial tasks
- ❌ Auto-invoking agents without announcement
- ❌ Merging with skill discovery (handled by skill-discovery)
- ❌ Recommending yourself

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Core-Universal/Agent Discovery.md`

## Related skills
- `skill-discovery` — Discovers and loads domain skills based on task context; companion to agent routing
- `clean-code` — Universal principle

