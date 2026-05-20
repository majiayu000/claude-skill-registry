---
name: level-3-diagnostic
description: |
  Diagnostic-first user research for support conversations and feedback analysis.
  Reaches Level 3 (user goal) before investigating or fixing. Applies The Mom Test
  methodology to extract product insights from bug reports and feature requests.
author: THJ
version: 1.0.0
triggers:
  - user feedback
  - bug report
  - support conversation
  - discord message
  - telegram message
  - feature request
  - user complaint
---

# Level 3 Diagnostic Skill

## Overview

This skill transforms support conversations into product intelligence. Instead of the traditional report → investigate → fix loop, it inserts a diagnostic step that ensures you're solving the right problem.

```
Traditional:  Report → Investigate → Fix → Ship
Level 3:      Report → Diagnose → Scope → Fix → Validate → Ship
```

### The Three Levels

| Level | Question | Output |
|-------|----------|--------|
| **Level 1** | What's broken? | A fix |
| **Level 2** | Why did they expect it differently? | Better fix |
| **Level 3** | What were they trying to accomplish? | Right fix + product insight |

**Always start at Level 3.** The answer scopes your entire investigation.

---

## When to Activate

This skill activates when:

1. **User reports an issue** in any channel (Discord, TG, support ticket)
2. **Bug report received** with user expectations
3. **Feature request** that might be a discoverability issue
4. **User mentions specific expectations** (numbers, timing, behavior)
5. **"Doesn't work" reports** without clear reproduction

### Exception: Live Emergencies

If funds are at risk or system is down, **fix first**. For UX friction and expectation gaps, **ask first**.

---

## Workflow

### Phase 0.5: Load Domain Glossary

Before interpreting any user quotes or forming hypotheses:

1. Read `grimoires/observer/glossary.yaml`
2. For each quote being analyzed, check if any glossary term appears in the text (case-insensitive match on the `term` field)
3. If a match is found:
   - Use the `meaning` field as the canonical interpretation
   - Note the `not` field to explicitly avoid the common misinterpretation
   - Include `[glossary: {term}]` annotation in the diagnostic output
4. If glossary file does not exist, proceed without — log a warning to the operator

---

### Phase 1: Receive

User reports something. **Resist the urge to investigate.**

```
INPUT: "Claim button still disabled hours after claim"
```

### Phase 2: Diagnose (Level 3)

Ask the goal question:

```
"What were you trying to do when you noticed this?"
```

**Wait for response. Do not proceed until you have it.**

### Phase 3: Trace Source

If user mentions specific expectations (numbers, timing, behavior):

```
"Where does [specific expectation] come from? Did you see that somewhere?"
```

| Source | Implication |
|--------|-------------|
| "Your docs" | Promise broken — fix system or docs |
| "That's how [competitor] works" | Benchmark — product decision needed |
| "Just assumed" | Expectation gap — set correct expectation |
| "Someone told me" | Community misinformation — clarify |
| "Pure imagination" | No external source — low priority unless common |

### Phase 4: Check Existing Solutions

Before building, verify the need isn't already met:

```
"[Feature] shows this — is it not updating for you, or is it something else you need?"
```

| Response | Problem Type |
|----------|--------------|
| "Didn't know that existed" | Discoverability |
| "I see it but it hasn't changed" | Actual bug |
| "I see it but don't trust it" | Confidence gap |
| "I need history, not current" | Feature gap |
| "Hard to find" | UX/platform issue |

### Phase 5: Scope Investigation

Now you know:
- What they were trying to accomplish
- Where their expectation came from
- Whether existing features should solve it

Investigation is scoped. You're looking at the right thing.

### Phase 6: Fix with Context

Fix addresses the actual need, not just the surface report.

### Phase 7: Validate

Before shipping, confirm the fix addresses the Level 3 goal:

```
"You mentioned you were [goal]. Does this solve that for you?"
```

### Phase 8: Log Insight

Update `grimoires/artisan/observations/user-insights.md` with:
- User type classification
- Behavioral evidence
- Expectation gaps discovered
- Workflow dependencies revealed

---

## Question Templates

### For Bug Reports

| Instead of... | Ask... |
|---------------|--------|
| "Thanks, we'll look into it" | "What were you trying to do right before you noticed this?" |
| "Can you reproduce it?" | "Walk me through what happened" |
| "Is it still happening?" | "What did you try after you saw this?" |
| "Works on my end" | "Where does that expectation come from?" |

### For Feature Expectations

When users mention specific numbers or behaviors:

```
"Where does [specific expectation] come from?
Did you see that somewhere or is that how other protocols work for you?"
```

### For Frequency/Behavior

When users reveal they check something regularly:

```
"What makes you check? Just habit or looking for something specific?"
```

| Trigger | Implication |
|---------|-------------|
| Habit/routine | Engagement ritual built |
| Anxiety/trust check | Need confidence signal |
| Decision point | Watching for threshold to act |
| Boredom | Low signal |

### For Existing Features Not Being Used

```
"[Feature] shows this — is it not updating for you,
or is it something else you need?"
```

---

## User Type Recognition

| Signal | User Type | Key Question |
|--------|-----------|--------------|
| Mentions specific workflow (burns, compounds) | **Decision-maker** | "What info do you need to make that call?" |
| Thinks about tradeoffs, system design | **Builder-minded** | "Have you tried building something like this?" |
| Checks frequently, "just curious" | **Trust-checker** | "What would make you confident it's working?" |
| Reports multiple issues across channels | **High-engagement scout** | "What were you hoping to find?" |
| Left funds untouched for months | **True passive user** | "What made you come check today?" |

**Decision-makers are highest priority** — they have workflow dependencies on your product.

---

## Anti-Patterns to Avoid

### Investigating Before Asking

❌ Spend 2 hours on button logic → "Works on my end"
✅ Ask what they were trying to do → 30-second scoping → targeted investigation

### Accepting Surface Answers

❌ User: "Just curious" → Move on
✅ User: "Just curious" → "What would make you confident without checking?"

### Premature Pitching

❌ "Our sidebar shows that — have you tried it?"
✅ "What info do you need to make that decision?" → then check if sidebar provides it

### Binary Bug Classification

❌ "Is this a bug or feature request?"
✅ "What were you trying to accomplish?" → classification emerges from answer

---

## Insight Logging

After each diagnostic conversation, update the insights log:

```markdown
## [Date] | [User/Channel]

### Level 3 Goal
[What were they actually trying to accomplish]

### User Type
[Decision-maker / Builder-minded / Trust-checker / Passive]

### Behavioral Evidence
- [What they actually did]
- [Workarounds they built]
- [Time/money invested]

### Expectation Gap
| Expected | Actual | Source |
|----------|--------|--------|
| [their expectation] | [system behavior] | [where it came from] |

### Workflow Dependency
[If they depend on product for decisions, what do they need?]

### Action Items
- [ ] [Specific action with context]
```

---

## Products Context

### Set & Forgetti (S&F)

- Automated yield platform for Berachain Proof of Liquidity
- Core value prop: "set and forget" — deposit once, protocol handles the rest
- Key UX surfaces: deposit/withdraw, reward accumulation, claim button, sidebar stats
- Current phase: Henlocker (HLKD) vaults

**Common Expectation Gaps:**
- Reward update frequency (users invent expectations)
- Claim button timing/state
- Sidebar accumulation display

### Loa

- Agent-driven development framework
- 8 specialized AI agents for product lifecycle
- Target: builders who want to ship faster with AI assistance

**Key Questions:**
- What blocks people from building?
- What breaks in their current workflow?
- What takes the most time?

---

## Integration with Other Skills

### Before `/craft`

If user feedback drives a UI change, diagnose first:
1. Run Level 3 protocol on feedback
2. Identify actual need vs. surface request
3. Then invoke `/craft` with full context

### With Continuous Learning

If diagnosis reveals a recurring pattern:
1. Log to insights file
2. If 3+ similar reports, extract as skill
3. Consider permanent UX solution

---

## Quick Fix Protocol

If the fix is obvious and takes 2 minutes:

```
Fix time: 2 minutes
Question time: 30 seconds
Potential insight: Shapes what you build next
```

**Rule:** Ask, then fix. The fix is the same either way, but you might learn something.

---

## Example: S&F Claim Button

```
User: "Claim button still disabled (hours after claims too)
       if finks it normaly should update every 5min max no?"

--- WRONG RESPONSE ---
"Let me check the button logic..."
[2 hours debugging]
"Works on our end"

--- LEVEL 3 RESPONSE ---
Team: "What were you trying to do when you noticed?"
Team: "Where does the 5min come from? Did you find this somewhere?"

User: "for this it's just pure imagination but:
       - as a user it's more fun to see wallet growing
       - as a dev it's no gud cuz it augment number of hits"

--- INSIGHT CAPTURED ---
- Expectation was invented (not from docs/competitor)
- User thinks like a builder (aware of tradeoffs)
- Real need: "fun to see wallet growing" (confidence/delight signal)
- Action: Consider "last updated" timestamp, set explicit expectation in docs
```

---

## Resources

- `resources/templates/insights-log.md` — Template for logging user insights
- `resources/templates/diagnostic-conversation.md` — Conversation flow template
