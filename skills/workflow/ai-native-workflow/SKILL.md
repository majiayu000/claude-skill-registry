---
name: ai-native-workflow
description: |
  Jeff Su's AI-Native Workflow framework (4 Habits) mapped onto Nebuchadnezzar v3.4 pipeline infrastructure. Use when:
  (1) "swipe file" or "what worked before" - retrieve proven email patterns by stage
  (2) "task mapping" or "M/AI split" or "YOU vs AI" - get decisions for stage transitions
  (3) "breadcrumb" or "anchor this" - link conversations to HubSpot + Git deal folders
  (4) "prompt library" or "battle-tested" - access working slash commands
  (5) "Blue Pill" - customer-facing communication (emails, proposals)
  (6) "Red Pill" - internal analysis (PLD, Brand Scout, Deal Snapshot)
  (7) Stage transitions [00→01], [02→03], [04] follow-ups, [08→09] win-backs
  Triggers on: "ai-native", "4 habits", "swipe", "winning email", "what worked", "task mapping", "YOU vs AI", "blue pill", "red pill"
---

# AI-Native Workflow Skill

> *"I can only show you the door. You're the one that has to walk through it."*

## Overview

Transform pipeline operations into AI-native workflows using Jeff Su's 4 Habits framework, fully integrated with the Nebuchadnezzar v3.4 infrastructure.

**Core Principle:** AI drafts, you decide timing and personal touches.

## The 4 Habits

| Habit | Purpose | Integration Point |
|-------|---------|-------------------|
| **AI Breadcrumbs** | Hyperlink AI chats to workspace | HubSpot Notes + Git `_NOTES.md` |
| **AI Swipe Files** | Provide examples of excellent work | `references/swipe-files/` by stage + mode |
| **AI-First Task Planning** | Map tasks as Manual/AI before projects | `references/task-templates.md` |
| **Prompts Database** | Save working prompts by use case | `references/prompt-library.md` |

---

## Mode System: Blue Pill vs Red Pill

### Blue Pill Mode (Customer-Facing)

External communication that goes to prospects/customers.

| Stage | Swipe File | Content Type |
|-------|------------|--------------|
| [00→01] | `discovery-outreach.md` | Cold outreach, follow-up cadence |
| [04] | `proposal-followups.md` | Day 1/3/7/10/14 follow-ups |
| [08→09] | `winbacks.md` | Re-engagement emails |
| All | `patterns-summary.md` | Golden rules, quick diagnosis |

### Red Pill Mode (Internal Analysis)

Internal work products that stay in the system.

| Analysis Type | Swipe File | Output |
|---------------|------------|--------|
| PLD Analysis | `internal-analysis.md` | Customer Shipping Analysis |
| Transit Report | `internal-analysis.md` | Transit Performance Summary |
| Brand Scout | `internal-analysis.md` | Lead Intelligence Report |
| Discovery Prep | `internal-analysis.md` | Call Prep Sheet |
| Meeting Debrief | `internal-analysis.md` | HubSpot Note |
| Deal Snapshot | `internal-analysis.md` | Pipeline Position |

---

## Workflows

### Swipe File Lookup

When user asks for "winning email" or "what worked" for a stage:

1. Identify pipeline stage ([00], [02], [04], [09], etc.)
2. Determine mode: Blue Pill (external) or Red Pill (internal)
3. Load appropriate swipe file from `references/swipe-files/`
4. Present pattern + verbatim example
5. Adapt to current prospect context

**Quick Routing:**
```
"Need to reach out cold" → discovery-outreach.md
"Proposal follow-up" → proposal-followups.md
"Win them back" → winbacks.md
"Analyze this data" → internal-analysis.md
"What's the pattern?" → patterns-summary.md
```

### Task Mapping (YOU vs AI)

When user needs M/AI decisions for a task:

1. Identify stage transition or activity type
2. Load `references/task-templates.md`
3. Present YOU vs AI grid with granular breakdown
4. Suggest specific tools/commands for AI tasks
5. Identify swipe file for reference

**Example Output:**
```
STAGE: [02]→[03] Discovery Complete → Rate Creation

YOU TASKS:
- Review discovery notes
- Submit rate request
- Follow up with pricing

AI TASKS:
- Draft data request email → /create-followup
- Run shipping analysis → analysis_skill.md
- Generate Customer Shipping Analysis → internal-analysis.md

SWIPE FILE: internal-analysis.md (PLD Analysis pattern)
```

### Breadcrumb Anchoring

When user says "anchor this" or conversation produced reusable output:

1. **Primary anchor**: HubSpot deal notes via `/log-activity`
2. **Secondary anchor**: Git deal folder `_NOTES.md` or `Customer_Relationship_Documentation.md`
3. Cross-link: Include "Full analysis: See [Deal]_Folder/_NOTES.md" in HubSpot

**10-Minute Rule**: If conversation >10 minutes OR produces reusable output → anchor immediately.

**Anchor Destinations by Output Type:**
| Output | Primary | Secondary |
|--------|---------|-----------|
| Email draft | — (it gets sent) | — |
| Meeting debrief | HubSpot Note | Deal folder |
| PLD analysis | Deal folder | HubSpot summary |
| Brand Scout | `Brand Scout Reports/` | HubSpot company |
| Deal snapshot | HubSpot Note | — |

### Prompt Lookup

When user asks "what command for X" or needs a battle-tested prompt:

1. Check `references/prompt-library.md` for command
2. Provide usage syntax and reliability rating
3. Match command to current stage
4. Suggest alternatives if primary doesn't fit

---

## Reference Files

| File | Load When | Mode |
|------|-----------|------|
| `references/swipe-files/discovery-outreach.md` | [00→01] cold outreach | Blue Pill |
| `references/swipe-files/proposal-followups.md` | [04] email follow-ups | Blue Pill |
| `references/swipe-files/winbacks.md` | [08→09] re-engagement | Blue Pill |
| `references/swipe-files/patterns-summary.md` | General "what works" | Both |
| `references/swipe-files/internal-analysis.md` | PLD, Brand Scout, Snapshots | Red Pill |
| `references/task-templates.md` | Task planning, YOU vs AI | Both |
| `references/prompt-library.md` | Command lookup | Both |

---

## Quick Reference

### Swipe File by Stage

| Stage | Blue Pill (External) | Red Pill (Internal) |
|-------|---------------------|---------------------|
| [00] Lead Gen | `discovery-outreach.md` | Brand Scout reports |
| [01] Discovery Scheduled | `discovery-outreach.md` | Discovery Prep Sheet |
| [02] Discovery Complete | `patterns-summary.md` | Meeting Debrief |
| [03] Rate Creation | `patterns-summary.md` | Customer Shipping Analysis |
| [04] Proposal Sent | `proposal-followups.md` | Deal Snapshot |
| [05] Setup Docs | `patterns-summary.md` | — |
| [06] Implementation | — | — |
| [07] Closed Won | — | — |
| [08] Closed Lost | `winbacks.md` | Loss analysis |
| [09] Win-Back | `winbacks.md` | — |

### Core Commands (High Reliability)

```bash
/brand-scout:scout [Company]      # Lead research
/check-lead [Company]             # HubSpot duplicate check
/add-lead [Company]               # Create company + contacts
/cvm-goals weekly                 # Pipeline dashboard
/check-tasks                      # Daily task review
python unified_sync.py 9am        # Morning sync
python unified_sync.py eod        # End-of-day sync
```

### Support Commands (Medium Reliability)

```bash
/create-followup                  # Draft follow-up email
/deal-snapshot [Deal]             # Quick status
/update-deal                      # Stage change
/log-activity                     # Anchor breadcrumb
/meeting-summary                  # Summarize call
/pipeline-health                  # Stage analysis
```

---

## Integration Points

### HubSpot Stage IDs

```
Discovery Scheduled: 1090865183
Discovery Complete: d2a08d6f-cc04-4423-9215-594fe682e538
Rate Creation: e1c4321e-afb6-4b29-97d4-2b2425488535
Proposal Sent: d607df25-2c6d-4a5d-9835-6ed1e4f4020a
Setup Docs: 4e549d01-674b-4b31-8a90-91ec03122715
Implementation: 08d9c411-5e1b-487b-8732-9c2bcbbd0307
Closed Won: 3fd46d94-78b4-452b-8704-62a338a210fb
Closed Lost: 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8
```

### File Paths

```
Deal folders:     [XX-STAGE]_Deal_Name/
Brand Scout:      Brand Scout Reports/
Templates:        Communication-Systems/Templates/
Daily log:        _DAILY_LOG.md
Sync reports:     sync_reports/
```

---

## Existing Skills (Reference, Don't Duplicate)

| Skill | Purpose | When to Use Instead |
|-------|---------|---------------------|
| `brand_scout_skill.md` | Lead research | Deep company research |
| `cvm-white-glove-sales-process` | Stages 02-07 process | 38 Questions framework |
| `december-pipeline-priming` | Q1 campaign templates | GRI-timed outreach |
| `analysis_skill.md` | PLD/shipping analysis | Full 9-tab Excel reports |
| `nate-jones-deliberate-practice` | Artifact evaluation | Self-scoring |

---

## Daily Workflow Integration

**Morning (9am):**
```
1. Run sync: python unified_sync.py 9am
2. Review pipeline health
3. Pick 3 priority actions (YOU decision)
4. Load task-templates.md for YOU vs AI split
5. Execute micro-actions
```

**Throughout Day:**
```
- Before email: Check swipe file for stage
- After call: Anchor meeting debrief (10-min rule)
- When stuck: Check prompt-library.md
```

**End of Day:**
```
1. Run sync: python unified_sync.py eod
2. Anchor any unanchored outputs
3. Clear or reschedule remaining tasks
```

---

## Anti-Patterns

```
NEVER:
- Send AI drafts without review
- Skip checking swipe file before writing
- Invent prompts when battle-tested ones exist
- Let AI outputs disappear (10-minute rule)
- Use Blue Pill patterns for internal analysis
- Use Red Pill patterns for customer emails

ALWAYS:
- Check swipe file BEFORE drafting
- Review and personalize AI drafts
- Anchor outputs within 10 minutes
- Map YOU vs AI before complex tasks
- Match command to current stage
```

---

*Skill Version: 2.0*
*Last Updated: December 2025*
*Framework: Jeff Su's 4 Habits + Nebuchadnezzar v3.3*
