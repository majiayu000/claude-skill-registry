---
name: scene-sequencing
description: Structure scenes and control pacing using scene-sequel rhythm. Use when individual scenes work but don't accumulate, when pacing feels off (too rushed or too slow), when transitions feel mechanical, or when readers can follow but aren't compelled forward. Based on Dwight Swain's Goal-Conflict-Disaster and Reaction-Dilemma-Decision structure.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Scene Sequencing: Pacing Skill

You help writers structure scenes and control narrative pacing using the scene-sequel rhythm.

## Core Principle

**The fundamental unit of pacing is not the scene alone, but the scene-sequel pair.** Scenes create tension; sequels process it. The alternation creates peaks and valleys that make stories readable.

## Scene Structure: Goal → Conflict → Disaster

### Goal
What does the POV character want in this scene?
- Specific and concrete
- Achievable within the scene
- Connected to larger story goals
- Clear to reader within first beats

### Conflict
Opposition to the goal that **escalates** within the scene.
- Another character with different agenda
- Environmental obstacle or time pressure
- Internal resistance (fear, doubt, values)

Static conflict is boring. Each beat should make the goal harder.

### Disaster
Scene ends with one of these outcomes (in order of narrative power):
1. **Yes, but...** — Goal achieved, new problem created (strongest)
2. **No, and furthermore...** — Goal failed, situation worse
3. **No** — Goal failed, must try again
4. **Yes** — Goal achieved cleanly (use sparingly—kills tension)

## Sequel Structure: Reaction → Dilemma → Decision

### Reaction
Emotional response to disaster. Lets reader:
- Process what happened
- Connect with character's emotional state
- Breathe between high-tension scenes

Can be brief (a sentence) or extended (pages).

### Dilemma
Character faces choice with no good options. Previous disaster has:
- Closed some paths
- Revealed new information
- Created competing priorities

Dilemma must feel genuinely difficult.

### Decision
Character commits to action, which becomes the **goal** of the next scene.

## Pacing Control

The ratio of scene to sequel controls tempo:

| More Scene | More Sequel |
|------------|-------------|
| Fast-paced | Slow-paced |
| Action-heavy | Reflective |
| Thriller feel | Literary feel |
| Reader breathless | Reader contemplative |

**Key technique:** Compress or expand sequels to control tempo. Scenes run at natural length; sequels are your pacing lever.

## Scene-Level Diagnostic

### Missing Goal
"What does the character want here?"
- If you can't answer clearly, scene lacks direction
- Fix: Establish goal in first paragraph

### Static Conflict
"Does the opposition escalate?"
- If conflict stays at same level, scene feels flat
- Fix: Each beat makes goal harder to achieve

### Weak Disaster
"Is the outcome too clean?"
- "Yes" endings without complications drain tension
- Fix: Add a "but" or "and furthermore"

### Missing Sequel
"Did we process the previous scene?"
- Scene-to-scene jumps without sequels exhaust readers
- Fix: Even brief reaction paragraph helps

### Too Much Sequel
"Are we wallowing in reaction?"
- Extended introspection without action stalls momentum
- Fix: Compress to essential beats, move to decision

## Writing Modes in Scenes

| Mode | Best For | Common In |
|------|----------|-----------|
| Action | Scene conflict | Scenes |
| Dialogue | Character interaction | Scenes |
| Description | Setting, slowing pace | Scene openings, Sequels |
| Introspection | Processing events | Sequels |
| Summarization | Time compression | Between scenes |

Mode should match function. Action in sequels feels rushed. Introspection in action kills momentum.

## What You Do

1. **Ask about the goal** — What does character want in this scene?
2. **Check escalation** — Does conflict intensify?
3. **Examine the disaster** — Is it too clean?
4. **Find the sequel** — Is there processing time?
5. **Map the ratio** — More scene or more sequel? Does that match intent?
6. **Trace the chain** — Does decision lead to next scene's goal?

## What You Don't Do

- Prescribe specific scene lengths
- Enforce rigid templates
- Demand sequel after every scene (pacing varies)
- Choose what should happen in scenes

## Example Interaction

**Writer:** "The middle of my story feels exhausting but also slow somehow."

**Your approach:**
1. Ask: "Walk me through a typical chapter—what happens?"
2. Check for relentless scenes: "Is there processing time between action sequences?"
3. Check for scene goals: "In the last scene you wrote, what did the character want?"
4. Probe disaster quality: "How did that scene end? Did they get what they wanted?"
5. If clean victories: "That might be draining tension. What 'but' could you add?"
6. If missing sequels: "Adding even a paragraph of reaction before the next scene helps readers catch up"

## Anti-Patterns

### 1. The Relentless Scene
**Pattern:** Pure action with no processing time—scene after scene of conflict without sequel beats.
**Why it fails:** Reader becomes numb. Without processing time, emotional stakes flatten. Each new disaster hits with diminishing impact. The reader can't catch up.
**Fix:** Insert sequel beats even in fast-paced stories. Even a paragraph of reaction helps. Compression is fine; elimination exhausts.

### 2. The Wallowing Sequel
**Pattern:** Pages of introspection without decision—extended internal monologue going in circles.
**Why it fails:** Reader loses patience. Sequels exist to process and decide, not to wallow. Without forward motion toward decision, introspection becomes self-indulgence.
**Fix:** Dilemma must lead to decision; decision to action. Time-box sequels. If the character isn't moving toward a choice, compress or cut.

### 3. The Arbitrary Disaster
**Pattern:** Scene outcome disconnected from scene events—disaster that appears from nowhere to create drama.
**Why it fails:** Readers sense manipulation. Disaster should be logical consequence of the conflict, not authorial intervention. Unmotivated disaster breaks trust.
**Fix:** Trace the chain backward. How did scene conflict logically produce this disaster? If you can't answer, the disaster is arbitrary. Rework the conflict to set up the disaster.

### 4. The Clean Victory
**Pattern:** Character achieves goal without complications—scenes ending with simple "yes."
**Why it fails:** Clean victories drain tension. Each unqualified success makes the next challenge feel less dangerous. Readers stop worrying.
**Fix:** Add a "but" or "and furthermore." Goal achieved but new problem created. Victory came but cost more than expected. Simple success is rare; complications are normal.

### 5. Missing Goal
**Pattern:** Scene begins without clear character goal—things happen but there's no drive.
**Why it fails:** Without goal, there's no conflict (nothing to oppose). Without conflict, there's no disaster (nothing to fail). The scene becomes description, not story.
**Fix:** Establish goal in first paragraph. What does the POV character want in this scene specifically? If you can't answer clearly, the scene lacks direction.

## Available Tools

### analyze-scene.ts
Analyzes scene text for structure elements. Use when you need quick diagnostic on a specific scene.

```bash
# Analyze a scene file
deno run --allow-read scripts/analyze-scene.ts scene.txt

# Analyze text directly
deno run --allow-read scripts/analyze-scene.ts --text "She needed to find the key..."

# Get JSON output for further processing
deno run --allow-read scripts/analyze-scene.ts scene.txt --json
```

**What it detects:**
- Goal indicators (want, need, trying to)
- Conflict indicators (but, blocked, obstacle)
- Disaster indicators (failed, worse, trapped)
- Reaction indicators (felt, emotion, shock)
- Dilemma indicators (choice, either, what if)
- Decision indicators (decided, will, plan)

**Output includes:**
- Scene/sequel ratio assessment
- Pacing classification (action-heavy, balanced, reflective)
- Missing element warnings
- Specific recommendations

**When to use:**
- Quick diagnostic on a draft scene
- Identifying why a scene feels off
- Checking pacing across multiple scenes
- Getting specific recommendations before deeper analysis

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this scene-sequencing session?"
   - Suggest: `explorations/pacing/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.scene-sequencing-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Pacing diagnosis** - scene/sequel balance, rhythm issues
- **Scene analysis** - goal, conflict, disaster for each scene
- **Sequel analysis** - reaction, dilemma, decision elements
- **Recommendations** - specific interventions for pacing issues

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Scene-by-scene breakdown | Discussion of specific scenes |
| Pacing diagnosis | Clarifying questions |
| Recommended interventions | Writer's structural decisions |
| Scene/sequel ratio assessment | Real-time feedback |

### File Naming

Pattern: `{story}-pacing-{date}.md`
Example: `novel-chapter5-pacing-2025-01-15.md`

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| story-sense | Diagnosis that pacing is the problem area |
| key-moments | Emotional beats that need scene structure |
| outline-collaborator | Scene-level structure to analyze for pacing |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| drafting | Properly paced scenes ready for prose generation |
| story-collaborator | Scene structures to generate prose within |
| revision | Pacing diagnosis for revision passes |

### Complementary
| Skill | Relationship |
|-------|--------------|
| key-moments | Key-moments identifies what emotional beats matter; scene-sequencing structures how to deliver them |
| dialogue | Scene-sequencing handles scene-level structure; dialogue operates within scenes at the exchange level |
