---
name: Solo Decision Framework
description: This skill should be used when the user asks to "decide what to build", "prioritize features", "choose an approach", "evaluate options", "should I build this", "what should I ship next", or needs help making product/implementation decisions quickly without overthinking.
version: 0.1.0
---

# Solo Decision Framework

A pragmatic rubric for solo founders to make quick decisions about what to build and how to build it.

## Purpose

Help solo founders make product and implementation decisions quickly using the LIC rubric (Lift, Impact, Conviction). Cut through analysis paralysis and focus on shipping.

## When to Use This Skill

Use when the user needs to:
- Decide which feature to build next
- Choose between implementation approaches
- Prioritize competing options
- Evaluate whether to build something
- Determine scope (MVP vs full-featured)
- Make build vs buy vs manual decisions

**Do NOT use for tech stack decisions** unless explicitly asked. Assume solo founders already know their tools.

## The LIC Rubric

Score each option 1-5 on three criteria:

### 🏋️ Lift - Implementation Effort
How much work to ship this?

- **5 pts**: Ship in 1-2 days, straightforward
- **3 pts**: 1-2 weeks, moderate complexity
- **1 pt**: Months of work, very complex

### 💥 Impact - Potential Value
How meaningful if it works?

- **5 pts**: Game changer, drives revenue/retention
- **3 pts**: Clear improvement, users notice
- **1 pt**: Minor, barely noticeable

### 🎯 Conviction - Confidence Level
How confident in the expected impact?

- **5 pts**: Strong evidence, validated, customers asking
- **3 pts**: Logical sense, some signal
- **1 pt**: Pure guess, no validation

**Maximum: 15 points per option**

## Decision Process

Follow these steps:

1. **Clarify the decision** - What exactly are we deciding?
2. **List 2-4 options** - Concrete approaches (ask if unclear)
3. **Score each option** - Apply LIC rubric
4. **Sum totals** - Calculate scores (max 15 each)
5. **Recommend winner** - Pick highest score
6. **Provide next step** - One concrete action

## Output Format

```
### Decision: [What we're deciding]

**Options:**
1. [Name] - [brief description]
2. [Name] - [brief description]
3. [Name] - [brief description]

---

**Option 1: [Name]**
- 🏋️ Lift: X/5 - [one line reasoning]
- 💥 Impact: X/5 - [one line reasoning]
- 🎯 Conviction: X/5 - [one line reasoning]
- **TOTAL: X/15**

**Option 2: [Name]**
- 🏋️ Lift: X/5 - [one line reasoning]
- 💥 Impact: X/5 - [one line reasoning]
- 🎯 Conviction: X/5 - [one line reasoning]
- **TOTAL: X/15**

[Repeat for remaining options]

---

### ✅ Ship this: [Winning option]

**Why:** [2-3 sentences explaining the pragmatic choice]

**Next step:** [One concrete action to take now]

**Revisit if:** [Specific signal to reconsider]
```

## Decision Heuristics

Apply these rules when scores are close or unclear:

- **Tied scores?** → Choose lower lift (ship faster)
- **Low conviction (<3)?** → Validate before building
- **High lift + high impact?** → Look for ways to reduce scope
- **High conviction + low impact?** → Probably not worth it
- **Quick win available?** → Ship it for momentum

## Common Decision Types

### WHAT to Build
- Feature prioritization
- Build new vs improve existing
- Scope decisions (MVP vs complete)
- Add complexity vs stay simple
- Customer requests evaluation

### HOW to Build
- Implementation approach
- Quick solution vs robust
- Manual process vs automated
- Big release vs incremental
- Error handling depth

## Principles

- **Bias toward shipping**: Speed matters when solo
- **Revenue wins**: Prioritize what drives money
- **Conviction matters**: Low confidence = validate first
- **Your time is finite**: Every hour is an opportunity cost
- **Good enough ships**: Perfect scores aren't the goal

## Examples

**Good uses:**
- "Should I build a referral program or improve onboarding?"
- "Should I add team features or focus on solo users?"
- "Quick hack or robust solution for this export feature?"
- "Should I build this integration customers requested?"

**Not for tech stack:**
- "Should I use Postgres or MongoDB?" (only if explicitly asked)
- "React or Vue?" (assume they know their stack)
- "Which hosting provider?" (not our focus)

Apply the rubric to help the user make their decision now.
