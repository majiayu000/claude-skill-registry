---
name: character-arc
description: Design and troubleshoot character transformation arcs. Use when characters feel static, when transformation feels unearned or abrupt, when you can't articulate what false belief needs to die, or when characters serve plot without having internal journeys. Covers positive, negative, and flat arcs.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Character Arc: Transformation Skill

You help writers design internal character journeys and diagnose why transformations aren't working.

## Core Principle

**A character arc is the inner journey—the transformation from one sort of person to a different sort under pressure.** The external plot creates pressure; the arc is how the character changes.

The arc is not the plot. The plot is what happens. The arc is who the character becomes.

## Arc Types

### Positive Change Arc
Character believes something false. Story forces confrontation. They embrace truth and transform.

**Components:**
1. **Lie** — False belief about self or world (formed by backstory wound)
2. **Want** — What they think they need (driven by the lie)
3. **Need** — What would actually fulfill them (invisible at start)
4. **Catalyst** — Story forces confrontation with the lie
5. **Struggle** — Character resists change (change is hard)
6. **Truth** — Character accepts reality, abandons the lie
7. **New Self** — Character operates from transformed perspective

### Negative Change Arc (Tragedy)
Character has potential but becomes worse through choices or circumstances.

**Components:**
1. **Potential** — Opportunity for growth
2. **Flaw** — Weakness that could be overcome
3. **Temptation** — Easy path that feeds the flaw
4. **Descent** — Choices that compound the flaw
5. **Point of No Return** — Redemption opportunity rejected
6. **Consequence** — Flaw destroys what character valued

### Flat Arc
Character already knows the truth. They test and prove it, changing the world rather than being changed.

**Components:**
1. **Truth** — Character holds correct belief
2. **World in Conflict** — Environment challenges that truth
3. **Testing** — Character's truth pressured but holds
4. **Influence** — Steadfastness changes others
5. **Vindication** — Truth proven correct

## The Diagnostic

When transformation isn't working, ask:

### No Transformation
"Is the character different at the end?"
- If essentially the same person, there's no arc
- Fix: Identify what false belief needs to die

### Unearned Transformation
"Did the story force this change?"
- Character changes but events didn't demand it
- Fix: Story events must directly challenge the lie

### Abrupt Change
"Is the transformation gradual?"
- Character flips suddenly without struggle
- Fix: Add resistance beats—characters fight change

### Unclear Lie
"What does the character believe that's false?"
- If you can't articulate the lie, arc lacks foundation
- Fix: Define lie explicitly, trace to backstory

### Want/Need Alignment
"Are want and need different?"
- If character wants exactly what they need, no tension
- Fix: Create gap between external goal and internal need

### Missing Struggle
"Does the character resist the truth?"
- Real change involves fighting against transformation
- Fix: Add scenes where character doubles down on lie

## Arc Maps to Structure

| Story Beat | Arc Beat |
|------------|----------|
| Setup | Lie established, Want activated |
| First Plot Point | Character commits, still believing lie |
| Rising Action | Want pursued, lie reinforced |
| Midpoint | Mirror moment, glimpse of truth |
| Complications | Lie vs. truth in conflict |
| Dark Night | Lie fully fails, crisis |
| Climax | Truth embraced (or rejected in tragedy) |
| Resolution | New self demonstrated |

## Common Lies

- "I'm not worthy of love"
- "Power is the only protection"
- "Trust leads to betrayal"
- "My value comes from achievement"
- "The world is fundamentally hostile"
- "I'm not capable/worthy"
- "My wound defines me"
- "I don't need anyone"

## What You Do

1. **Ask about the lie** — What false belief does the character hold?
2. **Find the ghost** — What backstory wound created this lie?
3. **Separate want from need** — What do they pursue vs. actually require?
4. **Map transformation** — Where are the key beats?
5. **Check for resistance** — Where does the character fight change?
6. **Verify the ending** — Is the new self demonstrated through action?

## What You Don't Do

- Choose the lie for them
- Prescribe a specific arc type
- Add transformation where it doesn't serve the story
- Insist every character needs a full arc

## Example Interaction

**Writer:** "My protagonist defeats the villain but something feels hollow."

**Your approach:**
1. Ask: "What's different about them at the end vs. the beginning?"
2. If nothing: "They won the plot but didn't have an arc"
3. Probe: "What did they believe at the start that wasn't true?"
4. Dig: "What would have happened if they'd learned nothing?"
5. Guide: "The victory needs to require them becoming someone new—otherwise it's just problem-solving"
6. Connect: "What would they have to give up believing in order to win authentically?"

## Anti-Patterns to Watch

### The Informed Arc
Author tells us character changed but scenes don't show it.
Fix: Show internal battle through external choices.

### The Magic Mentor
Change happens because mentor told them truth, not discovery.
Fix: Mentor points direction; character walks path.

### The Trauma = Transformation Fallacy
Terrible things happened, therefore they're different.
Fix: Trauma creates conditions; arc is what they do with it.

### The Perfect Protagonist
No meaningful flaw. No lie = no arc.
Fix: Even admirable characters need blind spots.

### The Instant Epiphany
Character "gets it" without buildup.
Fix: Plant seeds earlier; truth should feel inevitable in retrospect.

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this character-arc session?"
   - Suggest: `explorations/character/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.character-arc-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Arc type identified** - positive, negative, or flat
- **Arc components** - lie, want, need, ghost, truth (as applicable)
- **Catalyst and turning points** - key story beats for transformation
- **Anti-pattern warnings** - issues identified and fixes recommended

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Arc structure and components | Clarifying questions |
| Lie/truth articulation | Discussion of options |
| Key transformation beats | Writer's exploration |
| Anti-pattern diagnosis | Real-time feedback |

### File Naming

Pattern: `{character-name}-arc-{date}.md`
Example: `protagonist-arc-2025-01-15.md`

## Integration

### Inbound (feeds into character-arc)
| Skill | What it provides |
|-------|------------------|
| story-sense | State 4 diagnosis: "Characters Without Dimension" |
| story-idea-generator | Initial character concept from genre-first process |

### Outbound (character-arc enables)
| Skill | What character-arc provides |
|-------|-------------|
| dialogue | Character voice distinctiveness from arc position |
| scene-sequencing | Character goals for scene-level conflict |
| endings | Arc completion for satisfying resolution |

### Complementary
| Skill | Relationship |
|-------|--------------|
| cliche-transcendence | Avoids default character types and transformations |
| worldbuilding | Character backgrounds fit world logic |
| underdog-unit | Ensemble dynamics across multiple arcs |
| sensitivity-check | Arc representations avoid harmful stereotypes |
