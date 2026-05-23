---
name: story-sense
description: "Diagnose what any story needs regardless of its current state. This skill should be used when a writer is stuck, evaluating story problems, when narrative feels broken, or when someone asks 'what's wrong with my story?'. Keywords: story, diagnosis, stuck, narrative, plot, character, worldbuilding, revision."
license: MIT
compatibility: Works with any fiction format. Entry point for fiction diagnostics.
metadata:
  author: jwynia
  version: "1.0"
---

# Story Sense: Diagnostic Skill

Identify what state a story is in and what it needs to move forward. This is not a linear process but a diagnostic model: Assess → Diagnose → Intervene → Reassess.

## When to Use This Skill

Use this skill when:
- Writer is stuck and doesn't know why
- Story feels broken but root cause unclear
- Need to evaluate story problems systematically
- Someone asks "what's wrong with my story?"

Do NOT use this skill when:
- Writer wants you to write the story (use story-collaborator)
- Writer wants coaching questions only (use story-coach)
- Publishing/marketing questions (use book-marketing)

## Core Principle

**Story Sense is the ability to know what any story needs, regardless of its current state or intended medium.**

**There's no such thing as "stuck."** There's only:
- Not yet having diagnosed the problem
- Not yet applying the right intervention

## The Story States

### State 0: No Story (Blank Page)
**Symptoms:** Nothing exists yet
**Interventions:** story-idea-generator, elemental genres

### State 1: Concept Without Foundation
**Symptoms:** Have idea but world/characters/plot feel thin
**Interventions:** cliche-transcendence, systemic-worldbuilding, key-moments

### State 2: World Without Life
**Symptoms:** Setting exists but feels like backdrop
**Interventions:** worldbuilding skill suite (belief-systems, economic-systems, governance-systems)

### State 3: Flat Non-Humans
**Symptoms:** Aliens/fantasy species feel like humans in costume
**Interventions:** conlang, species development frameworks

### State 4: Characters Without Dimension
**Symptoms:** Characters serve plot rather than driving it
**Interventions:** character-arc, underdog-unit, positional-revelation

### State 4.5: Plot Without Pacing
**Symptoms:** Scenes work individually but don't accumulate
**Interventions:** scene-sequencing

### State 5: Plot Without Purpose
**Symptoms:** Events happen but don't accumulate meaning
**Interventions:** moral-parallax, key-moments

### State 5.5: Dialogue Feels Flat
**Symptoms:** Characters sound alike, conversations lifeless
**Interventions:** dialogue

### State 5.75: Ending Doesn't Land
**Symptoms:** Story builds well but resolution disappoints
**Interventions:** endings

### State 5.85: Draft Not Progressing
**Symptoms:** Planning done but draft isn't happening
**Interventions:** drafting

### State 5.9: Prose Feels Flat
**Symptoms:** Story works but sentences are functional not memorable
**Interventions:** prose-style

### State 6: Draft Complete, Needs Revision
**Symptoms:** Draft exists but revision feels overwhelming
**Interventions:** revision

### State 7: Ready for Evaluation
**Symptoms:** Story exists but quality uncertain
**Interventions:** sensitivity-check, story-analysis

## Decision Tree

```
Is there anything on the page?
├── NO → story-idea-generator
└── YES → What's the problem?
    ├── Feels generic → cliche-transcendence
    ├── World feels thin → worldbuilding
    ├── Non-humans feel fake → conlang
    ├── Characters flat → character-arc
    ├── Pacing off → scene-sequencing
    ├── Dialogue wooden → dialogue
    ├── Ending weak → endings
    ├── Meaning unclear → moral-parallax
    ├── Draft not progressing → drafting
    ├── Prose flat → prose-style
    └── Draft needs revision → revision
```

## Diagnostic Process

1. **Listen for symptoms** - What are they describing as the problem?
2. **Ask clarifying questions** - Get specific about where they're stuck
3. **Identify the state** - Match symptoms to state list
4. **Name the diagnosis** - Explain what you're seeing
5. **Recommend intervention** - Point to specific skill
6. **Offer next steps** - What should they try first?

## Available Scripts

### entropy.ts
Injects creative randomness from curated lists.

```bash
deno run --allow-read scripts/entropy.ts lies
deno run --allow-read scripts/entropy.ts disasters --count 3
deno run --allow-read scripts/entropy.ts --combo
```

**Lists:** lies, ghosts, disasters, dilemmas, professions, locations, collisions, openings

### functions.ts
Generates characters from abstract story functions.

```bash
deno run --allow-read scripts/functions.ts
deno run --allow-read scripts/functions.ts --setting scifi
deno run --allow-read scripts/functions.ts healer --setting fantasy
```

**Functions:** healer, enforcer, keeper_of_secrets, maker, trader, guide, entertainer, death_worker, transgressor

## Anti-Patterns

### Prescribing Instead of Diagnosing
**Fix:** Always ask clarifying questions before diagnosing.

### Framework Overload
**Fix:** Recommend one intervention. Expand after reassessment.

### Ignoring Writer's Energy
**Fix:** Balance diagnostic accuracy with what energizes the writer.

### Treating Structure as Story
**Fix:** Keep asking "Does this feel right?" alongside structural diagnosis.

## Related Skills

Routes to all fiction skills based on diagnosed state.
