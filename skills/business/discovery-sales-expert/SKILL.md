---
name: discovery-sales-expert
description: |
  Unified discovery and sales execution expert consolidating 38 Questions,
  CVM White Glove methodology, email patterns, and stage playbooks.
  Use when: discovery calls, pipeline execution, email drafting, stage transitions
  Triggers on: "discovery call", "38 questions", "volume commitment", "white glove",
               "follow-up email", "proposal", "stage transition", "win-back",
               "implementation", "test-to-ramp", "GRI", "outreach"
---

# Discovery/Sales Expert

Unified expert for B2B shipping sales discovery, pipeline execution, and revenue realization.

## Quick Reference

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| 38 Questions | Discovery structure | Every discovery call |
| CVM White Glove | Revenue realization | Stages 03-07 |
| YOU vs AI Mapping | Task delegation | Stage transitions |
| Email Patterns | Communication | Follow-ups, outreach |
| Practice Gym Rubrics | Self-evaluation | Post-call scoring |

## Core Philosophy

**"White Glove = You Don't Leave"** - Sales stays shoulder-to-shoulder through implementation weeks 2-4, where deals "slide into the ditch" if not actively managed.

**"AI drafts, YOU decide timing and personal touches."** - AI handles research, drafts, templates. Human handles judgment, relationships, sending.

## Decision Rules Summary

### Stage Transition Rules
```
IF discovery complete AND all 38Q sections scored → Move to Rate Creation
IF rate card approved AND volume commitment verbal → Move to Proposal
IF proposal sent AND test framework agreed → Move to Setup Docs
IF implementation live AND week 2 performance good → Enforce ramp commitment
```

### Response Selection Rules
```
IF no response after 3 days → Use 2-sentence soft check-in
IF no response after 7 days → Send unprompted value-add analysis
IF no response after 14 days → Decision point (push/pause/escalate)
IF won deal → Monthly business reviews, quarterly volume audits
IF lost deal → 90-day win-back sequence
```

### White Glove Jump-In Rules
```
IF contradiction detected → "Let me jump in here to level-set..."
IF volume bait & switch → "Hold on, we agreed to [X]. What's changed?"
IF "start small and ramp" → Address root concern + offer support
IF customer avoiding volume discussion → Red flag, investigate
```

## Reference Files

| File | Load When | Contents |
|------|-----------|----------|
| `00-decision-rules.md` | Always | IF-THEN rules for all scenarios |
| `01-38-questions-framework.md` | Discovery calls | Full 38Q with scoring |
| `02-stage-playbook.md` | Stage transitions | Actions per stage |
| `03-email-templates.md` | Email drafting | Proven patterns |
| `04-you-vs-ai-mapping.md` | Task planning | M/AI split by stage |
| `05-known-failures.md` | Before actions | Mistakes to prevent |

## Integration Points

### Source Skills (Reference, don't duplicate)
- `.claude/skills/cvm-white-glove-sales-process/` - CVM methodology
- `.claude/skills/december-pipeline-priming/` - GRI campaign
- `.claude/skills/ai-native-workflow/` - Swipe files, task mapping
- `.claude/skills/nate-jones-deliberate-practice/` - Practice rubrics
- `.claude/brand_scout/` - Research templates

### Commands That Trigger This Expert
- `/brand-scout:scout [Company]` - Lead research
- `/create-followup` - Draft follow-up email
- `/meeting-summary` - Post-call recap
- `/update-deal` - Stage transition
- `/log-activity` - Anchor breadcrumb

## Stage Overview

| Stage | Name | Key Action | Critical Success Factor |
|-------|------|------------|------------------------|
| 01 | Discovery Scheduled | Book call | Pre-call Brand Scout complete |
| 02 | Discovery Complete | Conduct 38Q call | All 5 sections scored |
| 03 | Rate Creation | Lock volume + pricing | Verbal commitment documented |
| 04 | Proposal Sent | Present + follow-up | Test framework agreed |
| 05 | Setup Docs | Pre-implementation | Alignment email sent |
| 06 | Implementation | White Glove execution | On every call, no contradictions |
| 07 | Closed Won | Continuous review | Monthly/quarterly audits |
| 08 | Closed Lost | Document + task | 90-day win-back scheduled |

## Post-Call Learning Capture

After every discovery call, Claude MUST:
1. Score against 38Q rubric (5 sections)
2. Document red flags with mitigation strategies
3. Identify missed sections for follow-up
4. Update expertise.yaml if new pattern discovered

## Golden Email Rules

| Do This | Not This |
|---------|----------|
| Specific time slots | "When are you free?" |
| "I need X to complete Y" | "Just checking in" |
| 2 sentences | 2 paragraphs |
| Post-meeting recap + action | Assume they remember |
| Easy yes/no question | Open-ended asks |

## Red Flags to Watch

- Vague volume control answers (can't quantify addressable %)
- "Let's start small and ramp" without defined timeline
- Multiple decision-makers with unclear authority
- IT/integration team not involved in discovery
- No clear pain point driving change
- Customer avoiding volume commitment discussions
- Gap between test agreement and actual volume
- New stakeholders introducing different expectations

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Discovery → Rate | 100% | Every complete discovery moves forward |
| Test-to-Ramp Conversion | >80% | Successful tests convert to full volume |
| Volume Variance | <15% | Actual vs committed at 90 days |
| Win-Back Success | >10% | Closed Lost that re-engage |
| Email Reply Rate | >30% | Follow-up emails get responses |
