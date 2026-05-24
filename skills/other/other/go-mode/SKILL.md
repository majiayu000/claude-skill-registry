---
name: go-mode
description: Autonomous goal execution — give a goal, get a plan, confirm, execute, report. You steer, Claude drives.
version: 2.0.0
author: BrianRWagner
tags: [autonomy, planning, execution, goal-setting, productivity]
homepage: https://github.com/BrianRWagner/ai-marketing-claude-code-skills
---

# 🎯 Go Mode — Autonomous Goal Execution

Give me a goal. I'll plan it, confirm with you, execute it, and report back. You steer — I drive.

## Mode

Detect from context or ask: *"Just do it, plan first, or plan + phase approvals?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 1-line plan → you confirm → execute | Simple tasks, clear goals |
| `standard` | Full plan → you confirm → execute → report (default) | Most tasks |
| `deep` | Full plan → risk review → confirm each phase → execute → report | High-stakes or multi-system tasks |

**Default: `standard`** — use `quick` for simple, clear goals. Use `deep` when mistakes would be expensive to undo.

---

## How It Works

```
GOAL → PLAN → CONFIRM → EXECUTE → REPORT
```

### Phase 1: PLAN
When given a goal, break it down:

1. **Parse the goal** — What's the desired outcome? What does "done" look like?
2. **Break into steps** — Ordered task list, each step concrete and actionable
3. **Identify tools** — Which skills, APIs, agents, or CLI tools are needed?
4. **Estimate effort** — Time per step, total duration, API costs if applicable
5. **Flag risks** — What could go wrong? What needs human approval?

Output a structured plan:

```
## 🎯 Goal: [restated goal]

### Definition of Done
[What success looks like]

### Plan
| # | Step | Tool/Skill | Est. Time | Cost | Risk |
|---|------|-----------|-----------|------|------|
| 1 | ... | ... | ... | ... | ... |

### Total Estimate
- **Time:** X minutes
- **API Cost:** ~$X.XX
- **Human Checkpoints:** [list]

### Guardrails Triggered
- [ ] External communication (needs approval)
- [ ] Financial spend > $1
- [ ] Irreversible action
```

### Phase 2: CONFIRM
Present the plan and wait for approval:

- **"Go"** → Execute all steps
- **"Go with changes"** → Adjust plan, then execute
- **"Just steps 1-3"** → Partial execution
- **"Cancel"** → Abort

**Never skip confirmation.** This is the human's steering wheel.

### Phase 3: EXECUTE
Run each step sequentially:

1. **Announce** the current step: "Step 2/5: Researching competitor pricing..."
2. **Execute** using the identified tool/skill
3. **Checkpoint** after each major step — brief status update
4. **Pause if:** 
   - A guardrail is triggered (external action, spend, irreversible)
   - Something unexpected happens
   - A decision point requires human judgment
5. **Adapt** — If a step fails, try alternatives before escalating

### Phase 4: REPORT
When all steps complete:

```
## ✅ Goal Complete: [goal]

### What Was Done
- Step 1: [result]
- Step 2: [result]
- ...

### Outputs
- [List of files, links, artifacts created]

### What Was Learned
- [Insights discovered during execution]

### Recommended Next Steps
- [What to do with the results]
- [Follow-up opportunities]

### Stats
- Total time: Xm
- API calls: X
- Est. cost: $X.XX
```

## Guardrails

### Always Ask Before:
- ✉️ Sending emails, DMs, or messages to anyone
- 📢 Posting to social media (Twitter, LinkedIn, etc.)
- 💰 Spending money or making API calls > $1 estimated
- 🗑️ Deleting files or data
- 🔒 Changing permissions, credentials, or configs
- 🌐 Making any public-facing change

### Auto-Proceed On:
- ✅ Reading files, searching the web
- ✅ Creating drafts (not publishing)
- ✅ Organizing or summarizing information
- ✅ Running analysis or calculations
- ✅ Creating files in the workspace

### Budget Caps
- **Default per-goal budget:** $5 API spend max
- **Per-step timeout:** 5 minutes (escalate if stuck)
- **Total goal timeout:** 60 minutes (checkpoint and ask to continue)
- Human can override any cap at confirm time

## Available Tools & Skills Reference

When planning, draw from this toolkit:

### Research & Information
| Tool | Use For |
|------|---------|
| `web_search` | Quick web lookups |
| `web_fetch` | Read full web pages |
| `qmd search` | Search Obsidian vault knowledge base |
| `content-research-writer` skill | Deep research + writing |
| `research-coordinator` skill | Multi-source research |

### Content Creation
| Tool | Use For |
|------|---------|
| `content-atomizer` skill | Turn 1 piece → 13+ posts |
| `direct-response-copy` skill | Sales copy |
| `seo-content` skill | SEO articles |
| `newsletter` skill | Newsletter editions |
| `email-sequences` skill | Email flows |
| `nano-banana` skill | Image generation (Gemini) |

### Marketing & Strategy
| Tool | Use For |
|------|---------|
| `positioning-angles` skill | Find hooks that sell |
| `keyword-research` skill | SEO keyword strategy |
| `business-prospecting` skill | Lead research |
| `landing-page-design` skill | Landing pages |
| `page-cro` skill | Conversion optimization |

### Communication
| Tool | Use For |
|------|---------|
| `bird` CLI | Twitter/X (read, post, reply) |
| Gmail | Email (read, send) |
| Notion | Pages and databases |
| Telegram | Messaging |

### Development
| Tool | Use For |
|------|---------|
| `exec` | Shell commands |
| `codex` | Code generation (GPT) |
| `claude` | Code generation (Claude) |
| File tools | Read, write, edit files |

## Example Goals

### 1. Competitor Analysis → Comparison Page
```
Goal: "Research our top 3 competitors in the AI assistant space and build a comparison page"

Plan:
1. Identify top 3 competitors (web search) — 5min
2. Research each: pricing, features, reviews — 15min
3. Build comparison matrix — 10min
4. Write comparison page copy — 15min
5. Create visual comparison table — 5min
Total: ~50min, ~$0.50 API cost
```

### 2. Content Repurposing Pipeline
```
Goal: "Take my latest blog post and turn it into a week of social content"

Plan:
1. Read and analyze the blog post — 2min
2. Extract key themes and quotes — 5min
3. Generate 5 Twitter threads — 15min
4. Generate 5 LinkedIn posts — 15min
5. Create 3 image prompts + generate visuals — 10min
6. Build content calendar — 5min
Total: ~52min, ~$1.00 API cost
```

### 3. Lead Research Sprint
```
Goal: "Find 20 potential clients in the SaaS space who might need our marketing services"

Plan:
1. Define ideal client profile — 5min
2. Search for SaaS companies (web) — 15min
3. Research each company's marketing gaps — 20min
4. Score and rank prospects — 10min
5. Build outreach-ready prospect list — 10min
6. Draft personalized intro messages [NEEDS APPROVAL] — 15min
Total: ~75min, ~$0.75 API cost
```

### 4. SEO Content Sprint
```
Goal: "Create 3 SEO-optimized blog posts for our target keywords"

Plan:
1. Review target keyword list — 2min
2. Research top-ranking content for each keyword — 15min
3. Create outlines using SEO skill — 10min
4. Write article 1 — 15min
5. Write article 2 — 15min
6. Write article 3 — 15min
7. Add internal links and meta descriptions — 10min
Total: ~82min, ~$2.00 API cost
```

### 5. Launch Prep Checklist
```
Goal: "Prepare everything needed to launch our new product next Tuesday"

Plan:
1. Audit what exists (landing page, emails, social) — 10min
2. Identify gaps — 5min
3. Write launch email sequence (3 emails) — 20min
4. Create social media posts (Twitter, LinkedIn) — 15min
5. Generate launch graphics — 10min
6. Build launch day timeline — 5min
7. Draft press/outreach messages [NEEDS APPROVAL] — 15min
Total: ~80min, ~$2.50 API cost
```

### 6. Weekly Review & Planning
```
Goal: "Review this week's metrics, summarize wins/losses, and plan next week's priorities"

Plan:
1. Pull metrics from available sources — 10min
2. Summarize key wins — 5min
3. Identify what didn't work — 5min
4. Review upcoming calendar — 5min
5. Propose next week's top 3 priorities — 10min
6. Create actionable task list — 5min
Total: ~40min, ~$0.25 API cost
```

## Usage

Just tell the agent your goal in natural language:

> "Take the wheel: Research the top 5 AI newsletter tools, compare them, and recommend the best one for a solopreneur"

> "Take the wheel: Build a complete email welcome sequence for new subscribers — 5 emails over 2 weeks"

> "Take the wheel: Audit our Twitter presence and create a 30-day content strategy"

The agent will plan, confirm, execute, and report. You stay in control at every checkpoint.

## Principles

1. **Transparency** — Always show the plan before executing
2. **Safety** — Never take external actions without approval
3. **Efficiency** — Use the cheapest/fastest tool for each step
4. **Resilience** — Try alternatives before giving up
5. **Accountability** — Report everything that was done
6. **Respect time** — Estimate honestly, checkpoint if running long
