---
name: jobs-theory
description: Clarify what job your product actually does for people. Use when uncertain about value proposition, preparing customer interviews, writing positioning/copy, or deciding what to build. Interactive and output-focused - produces job statements, interview scripts, and opportunity analysis rather than lecturing theory.
---

# Jobs Theory Skill

Help builders get clarity on what their product actually does for people, fast.

## Core Idea

People don't buy products - they "hire" them to make progress in their lives. Understanding the job reveals:
- What you're really competing with (often not who you think)
- Why people switch (or don't)
- How to message so it resonates
- What to build next

## Workflows

### 1. Job Discovery

**Use when:** "What job does my product actually do?"

**Approach:** Ask the user about their product, then help them articulate the job through guided questions.

**Questions to ask:**
1. "What does your product do? Describe it simply."
2. "Think of your best user - someone who loves it. What were they doing *before* they found you?"
3. "What triggered them to look for a solution? What was the struggling moment?"
4. "When they use your product, what progress are they making?"
5. "How would they feel if they couldn't use it anymore? What would they do instead?"

**Output:** Job statement in this format:
```
When [situation/trigger], I want to [motivation/action], so I can [desired outcome].
```

Plus the functional, emotional, and social dimensions:
- **Functional:** What they're trying to get done
- **Emotional:** How they want to feel
- **Social:** How they want to be perceived

### 2. Forces Analysis

**Use when:** "Why aren't people switching?" or "Why do people churn?"

**Approach:** Map the four forces that drive (or block) switching behavior.

> For detailed framework, read `references/forces-of-progress.md`

**Questions to ask:**
1. "What's painful or frustrating about their current situation?" (Push)
2. "What's attractive about your solution?" (Pull)
3. "What might make them nervous about switching?" (Anxiety)
4. "What habits or familiarity keeps them with the old way?" (Habit)

**Output:** Forces diagram showing:
```
PROGRESS →
  Push of current situation: [...]
  Pull of new solution: [...]

← RESISTANCE
  Anxiety of new solution: [...]
  Habit of current behavior: [...]
```

Plus recommendations: Which force to amplify or reduce.

### 3. Competition Mapping

**Use when:** "Who am I really competing with?"

**Approach:** Identify what else gets "hired" for the same job - often non-obvious alternatives.

**Key insight:** Competition isn't other products in your category. It's anything that gets the job done.

**Examples:**
- Milkshake's competition: bananas, bagels, boredom (not other milkshakes)
- Zoom's competition: emails, phone calls, flying to meetings (not just other video tools)
- Netflix's competition: sleep, social media, video games (not just other streaming)

**Questions to ask:**
1. "What job does your product do?" (from Job Discovery)
2. "What do people use *before* they find you?"
3. "What would they do if your product disappeared tomorrow?"
4. "What do non-users do to get this job done?"

**Output:** Competition map showing direct competitors, indirect alternatives, and non-consumption.

### 4. Interview Prep

**Use when:** "I'm about to talk to customers" or "Help me understand my users"

**Approach:** Generate a switch interview script focused on the timeline of their decision.

> For detailed technique, read `references/switch-interview.md`

**Output:** Customized interview script using the timeline approach:
1. First thought - when did they first realize they needed something?
2. Passive looking - what did they notice without actively searching?
3. Active looking - when did they start seriously evaluating?
4. Deciding - what made them choose?
5. Consuming - first use experience
6. Satisfaction - did it deliver on the job?

See `assets/templates/interview-questions.md` for the full script template.

### 5. Opportunity Scoring

**Use when:** "What should I build next?" or "Where's the biggest opportunity?"

**Approach:** Use importance vs. satisfaction to find underserved jobs.

**Formula:**
```
Opportunity = Importance + (Importance - Satisfaction)
```

High importance + low satisfaction = opportunity.

**Process:**
1. List the outcomes users want when doing the job
2. Rate each: How important is this? (1-10)
3. Rate each: How satisfied are they with current solutions? (1-10)
4. Calculate opportunity score
5. Prioritize highest scores

**Output:** Ranked list of opportunities with scores.

### 6. Job Story Writing

**Use when:** "Help me write user stories" or "I need to spec a feature"

**Approach:** Convert job insights into actionable job stories for product development.

**Format:**
```
When [situation],
I want to [motivation],
So I can [expected outcome].
```

**Key difference from user stories:**
- User stories: "As a [persona], I want [feature], so that [benefit]"
- Job stories: Focus on situation and motivation, not persona and feature

**Why job stories work better:**
- Personas are made up; situations are real
- Features are solutions; motivations reveal the actual need
- Opens design space instead of prescribing implementation

**Output:** Set of job stories ready for product/engineering.

## Quick Reference

### Job Statement Formula
```
When [situation/trigger], I want to [motivation], so I can [outcome].
```

### The Four Forces
| Force | Direction | Question |
|-------|-----------|----------|
| Push | → Progress | What's wrong with current situation? |
| Pull | → Progress | What's attractive about new solution? |
| Anxiety | ← Resistance | What's scary about switching? |
| Habit | ← Resistance | What's comfortable about status quo? |

### Three Job Dimensions
- **Functional:** The practical task they're trying to accomplish
- **Emotional:** How they want to feel during and after
- **Social:** How they want to be perceived by others

### Competition Levels
1. **Direct:** Same product category
2. **Indirect:** Different category, same job
3. **Non-consumption:** Doing nothing, workarounds

## Reference Files

- `references/forces-of-progress.md` - Deep dive on push, pull, anxiety, habit
- `references/switch-interview.md` - Timeline interview technique

## Templates

- `assets/templates/interview-questions.md` - Full interview script
