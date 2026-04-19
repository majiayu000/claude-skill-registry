---
name: user-interview
description: "Guide for conducting Torres-style story-based user interviews with bias mitigation and JTBD lens."
---

# User Interview Guide

Discover opportunities through customer stories. Source: Torres (CDH), Kahneman, Christensen (JTBD).

## Pre-Interview (Mandatory)

1. **Run `/bias-check`** before designing questions
2. Review current OST -- what are you trying to learn?
3. Design questions that are story-based and past-tense

## Question Design Rules

### ALWAYS Ask (story-based, past behavior)
- "Tell me about the last time you [tried to accomplish X]..."
- "Walk me through what happened when [situation]..."
- "What did you do when [problem occurred]?"
- "How did that make you feel?" (emotional dimension -- JTBD)
- "What did other people think about that?" (social dimension -- JTBD)

### NEVER Ask (hypothetical, opinion, leading)
- "Would you use a feature that...?" (hypothetical)
- "Do you think X is a good idea?" (opinion)
- "Don't you find it frustrating when...?" (leading)
- "On a scale of 1-10, how important is...?" (abstract)
- "What features would you want?" (solution-space, not problem-space)

## During Interview

### Three Mindsets (Brown)
- **Curiosity**: Ask from genuine interest. "Walk me through..." not "What are your pain points?"
- **Skepticism**: Probe beneath surface responses. "Why does your team call this a 'power user'?" Challenge assumptions without being adversarial.
- **Humility**: "Can you say that again so I get it right?" Don't assume immediate comprehension.

**Master the pause**: Wait 3-5 seconds after each response before your next question. Silence often prompts the real insight.

### Listening
- Listen for hiring/firing language (JTBD)
- Note emotional reactions (tone, hesitation, enthusiasm)
- Follow up on surprises -- "That's interesting, tell me more about..."
- Don't pitch or defend -- you're here to learn, not sell
- Watch for the **say-do gap**: people describe intended behavior, not actual behavior. Ask the same question multiple ways to cross-check.

## Post-Interview Snapshot
Create immediately after each interview:
- 3-5 key quotes (verbatim)
- Opportunities identified (needs/pain points/desires)
- Surprises (things you didn't expect)
- JTBD dimensions observed (functional/emotional/social)
- Biases to watch for in interpretation
- **Scenarios extracted** (see below)

### Scenario Extraction (Hoskins)

Interviews are where scenarios are born. After each interview, look for narratives that contain Hoskins' four elements:

1. **Persona**: The interviewee's role, context, constraints, goals — captured naturally in the conversation
2. **Means**: How they interact with existing tools/processes — captured in "walk me through" questions
3. **Motive**: Why they're doing this — captured in JTBD dimensions (functional, emotional, social)
4. **Simulation**: The story itself — the "last time you tried to..." narrative IS the simulation

Draft a scenario entry for `canvas/scenarios.yml` from any interview story that is rich enough. Not every interview produces a scenario — only extract when all four elements are present. A partial story is an opportunity, not a scenario.

*Source: Hoskins, "Attention to Users Is All You Need" (SAP talk, April 2026) — "Scenarios are the fundamental primitive of product thinking."*

### Closing

Always end with: **"Is there anything else you'd like to share that I didn't ask about?"**

This is where the most surprising insights surface. The interviewee has been primed by the structured questions and now has permission to surface what's actually on their mind.

*Source: Brown (EightShapes), NNGroup, IxDF.*

## Output
- Update canvas/opportunities.yml with new evidence
- Update canvas/user-needs.yml
- Update canvas/jobs-to-be-done.yml
- Update canvas/scenarios.yml with extracted scenarios (if four elements present)
- Add snapshot to product-journal.md
