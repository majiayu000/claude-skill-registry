---
name: goal-tracking-expert
description: |
  Self-improving CVM goal tracking expert with automatic learning.
  Use when: running /cvm-goals, checking pipeline health, stage analysis, goal calculations
  Triggers on: "cvm-goals", "goal tracking", "stage entry", "micro-actions",
               "pipeline health", "rubric", "composite score", "weekly goals",
               "monthly goals", "quarterly goals", "funnel metrics", "archetype"
---

# Goal Tracking Expert

Self-improving expert for CVM (Customer Value Management) goal tracking, pipeline metrics, and sales funnel analysis.

## Quick Reference

| Item | Value |
|------|-------|
| Full Funnel Pattern | 15/6/4/4/3/2/1/1 |
| Weekly → Monthly | × 4.3 |
| Weekly → Quarterly | × 13 |
| Quarterly Distribution | Q1=15%, Q2=23%, Q3=28%, Q4=34% |

## Core Decision Rules

### Stage Metric Selection
```
IF metric = "new_leads" → Use Contacts API (NOT Deals)
IF metric = pipeline stage → Use hs_v2_date_entered_[stageid] property
NEVER count deals currently IN stage → ALWAYS count deals that ENTERED stage in period
```

### Goal Status Thresholds
```
IF actual/target >= 90% → on_track (green)
IF actual/target >= 70% → behind (yellow)
IF actual/target >= 50% → at_risk (orange)
IF actual/target < 50% → critical (red)
```

### Red Stage Response
```
IF stage shows red → Look up micro-actions in 02-micro-actions-lookup.md
IF Stage 1 green + Stages 2-4 red → Outreach bottleneck (not sourcing)
Execute next incomplete micro-action → Log to HubSpot → Re-check
```

## Reference Files

| File | Load When | Contents |
|------|-----------|----------|
| `00-decision-rules.md` | Always | IF-THEN rules for all goal tracking decisions |
| `01-stage-entry-queries.md` | HubSpot queries | Stage entry property names, query templates |
| `02-micro-actions-lookup.md` | Red stage detected | Stage-by-stage micro-actions, WIP limits |
| `03-goal-calculations.md` | Goal math needed | Weekly/monthly/quarterly formulas, archetypes |
| `04-known-failures.md` | Before any calculation | Mistakes to prevent with prevention patterns |

## Integration Points

### Source Files (DO NOT duplicate - reference these)
- `.claude/config/cvm_goals_2026.yaml` - Team config, stages, archetypes
- `.claude/config/reps/brett_walker.yaml` - Personal goals, weekly pattern
- `.claude/config/GOAL_MICRO_ACTIONS.md` - Micro-actions reference
- `.claude/agents/goal_tracker.py` - Operational code with STAGE_ENTRY_PROPS

### Commands That Trigger This Expert
- `/cvm-goals weekly` - Weekly goal dashboard
- `/cvm-goals monthly` - Monthly goal dashboard
- `/cvm-goals` - Default to weekly

## Learning Capture (Post /cvm-goals)

After every `/cvm-goals` run, check for:
1. **New patterns discovered** - Add to expertise.yaml learned_behaviors.successes
2. **Calculation corrections made** - Add to expertise.yaml learned_behaviors.failures
3. **Edge cases encountered** - Document in 04-known-failures.md

Update `expertise.yaml` version when learning occurs:
- Patch version (1.0.X) for new learnings
- Minor version (1.X.0) for new patterns
- Major version (X.0.0) for structural changes

## ADHD Execution Loop

When `/cvm-goals` shows red stages:
```
1. /cvm-goals weekly → See dashboard with red indicators
2. Find red stage → Look up micro-actions (02-micro-actions-lookup.md)
3. Execute single micro-action → Log to HubSpot
4. Repeat until stage turns green or WIP limit reached
```

## Diagnostic Patterns

| Pattern | Diagnosis | Action |
|---------|-----------|--------|
| Stage 1 green, Stages 2-4 red | Outreach bottleneck | Focus on follow-ups, not sourcing |
| All stages red | Systemic issue | Check data integrity, review archetype |
| Stage 1 red only | Lead generation gap | Brand Scout, prospecting |
| Late stages red | Conversion issue | Review proposals, follow-up cadence |
