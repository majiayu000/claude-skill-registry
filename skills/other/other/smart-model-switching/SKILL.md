---
name: smart-model-switching
description: >-
  Auto-route tasks to the cheapest Claude model that works correctly.
  Three-tier progression: Haiku → Sonnet → Opus. Classify before responding.
  HAIKU (default): factual Q&A, greetings, reminders, status checks, lookups,
  simple file ops, heartbeats, casual chat, 1-2 sentence tasks.
  ESCALATE TO SONNET: code >10 lines, analysis, comparisons, planning, reports,
  multi-step reasoning, tables, long writing >3 paragraphs, summarization,
  research synthesis, most user conversations.
  ESCALATE TO OPUS: architecture decisions, complex debugging, multi-file
  refactoring, strategic planning, nuanced judgment, deep research, critical
  production decisions. Rule: If a human needs >30 seconds of focused thinking,
  escalate. If Sonnet struggles with complexity, go to Opus. Save 50-90% on
  API costs by starting cheap and escalating only when needed.
author: "OpenClaw Community"
version: 1.0.0
homepage: https://clawhub.com
metadata:
  openclaw:
    emoji: "💰"
---

# Smart Model Switching

**Three-tier Claude routing: Haiku → Sonnet → Opus**

Start with the cheapest model. Escalate only when needed. Save 50-90% on API costs.

## The Golden Rule

> If a human would need more than 30 seconds of focused thinking, escalate from Haiku to Sonnet.
> If the task involves architecture, complex tradeoffs, or deep reasoning, escalate to Opus.

## Cost Reality

| Model | Input | Output | Relative Cost |
|-------|-------|--------|---------------|
| Haiku | \$0.25/M | \$1.25/M | 1x (baseline) |
| Sonnet | \$3.00/M | \$15.00/M | 12x |
| Opus | \$15.00/M | \$75.00/M | 60x |

**Bottom line:** Wrong model selection wastes money OR time. Haiku for simple, Sonnet for standard, Opus for complex.

---

## 💚 HAIKU — Default for Simple Tasks

**Stay on Haiku for:**
- Factual Q&A — "what is X", "who is Y", "when did Z"
- Quick lookups — definitions, unit conversions, short translations
- Status checks — calendar, file reads, session monitoring
- Heartbeats — periodic checks, HEARTBEAT_OK responses
- Memory & reminders — "remember this", "remind me to..."
- Casual conversation — greetings, small talk, acknowledgments
- Simple file ops — read, list, basic writes
- One-liner tasks — anything answerable in 1-2 sentences

### NEVER do these on Haiku
- ❌ Write code longer than 10 lines
- ❌ Create comparison tables
- ❌ Write more than 3 paragraphs
- ❌ Do multi-step analysis
- ❌ Write reports or proposals

---

## 💛 SONNET — Standard Work (The Workhorse)

**Escalate to Sonnet for:**

### Code & Technical
- Code generation — write functions, build features, scripts
- Code review — PR reviews, quality checks
- Debugging — standard bug investigation
- Documentation — README, comments, user guides

### Analysis & Planning  
- Analysis & evaluation — compare options, assess trade-offs
- Planning — project plans, roadmaps, task breakdowns
- Research synthesis — combining multiple sources
- Multi-step reasoning — "first... then... finally"

### Writing & Content
- Long-form writing — reports, proposals, articles (>3 paragraphs)
- Creative writing — blog posts, descriptions, copy
- Summarization — long documents, transcripts
- Structured output — tables, outlines, formatted docs

---

## ❤️ OPUS — Complex Reasoning Only

**Escalate to Opus for:**

### Architecture & Design
- System architecture decisions
- Major codebase refactoring
- Design pattern selection with tradeoffs
- Database schema design

### Deep Analysis
- Complex debugging (multi-file, race conditions)
- Security reviews
- Performance optimization strategy
- Root cause analysis of subtle bugs

### Strategic & Creative
- Strategic planning — business decisions, roadmaps
- Nuanced judgment — ethics, ambiguity, competing values
- Deep research — comprehensive multi-source analysis

---

## 🔄 Implementation

### For Subagents
\`\`\`javascript
// Routine monitoring
sessions_spawn(task="Check backup status", model="haiku")

// Standard code work  
sessions_spawn(task="Build the REST API endpoint", model="sonnet")

// Architecture decisions
sessions_spawn(task="Design the database schema for multi-tenancy", model="opus")
\`\`\`

### For Cron Jobs
\`\`\`json
{
  "payload": {
    "kind": "agentTurn",
    "model": "haiku"
  }
}
\`\`\`
Always use Haiku for cron unless the task genuinely needs reasoning.

---

## 📊 Quick Decision Tree

\`\`\`
Is it a greeting, lookup, status check, or 1-2 sentence answer?
  YES → HAIKU
  NO ↓

Is it code, analysis, planning, writing, or multi-step?
  YES → SONNET  
  NO ↓

Is it architecture, deep reasoning, or critical decision?
  YES → OPUS
  NO → Default to SONNET, escalate if struggling
\`\`\`

---

## 📋 Quick Reference Card

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                  SMART MODEL SWITCHING                      │
│                  Haiku → Sonnet → Opus                      │
├─────────────────────────────────────────────────────────────┤
│  💚 HAIKU (cheapest)                                        │
│  • Greetings, status checks, quick lookups                  │
│  • Factual Q&A, definitions, reminders                      │
│  • Simple file ops, 1-2 sentence answers                    │
├─────────────────────────────────────────────────────────────┤
│  💛 SONNET (standard)                                       │
│  • Code > 10 lines, debugging                               │
│  • Analysis, comparisons, planning                          │
│  • Reports, proposals, long writing                         │
├─────────────────────────────────────────────────────────────┤
│  ❤️ OPUS (complex)                                          │
│  • Architecture decisions                                   │
│  • Complex debugging, multi-file refactoring                │
│  • Strategic planning, deep research                        │
├─────────────────────────────────────────────────────────────┤
│  💡 RULE: If a human needs > 30 sec thinking → escalate     │
│  💰 COST: Haiku 1x → Sonnet 12x → Opus 60x                  │
└─────────────────────────────────────────────────────────────┘
\`\`\`

---

*Built for Claude-only setups with Haiku, Sonnet, and Opus.*
*Inspired by save-money skill, extended with three-tier progression.*
