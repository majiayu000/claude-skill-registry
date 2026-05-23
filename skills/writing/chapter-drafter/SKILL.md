---
name: chapter-drafter
description: Autonomously draft and polish chapters through multi-skill editorial passes. Use when you have a complete outline and want to produce a polished first draft with iterative refinement.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  orchestrates:
    - scene-sequencing
    - character-arc
    - cliche-transcendence
    - dialogue
    - prose-style
  pass_order:
    - scene-sequencing
    - character-arc
    - cliche-transcendence
    - dialogue
    - prose-style
  pass_weights:
    scene-sequencing: 35
    character-arc: 25
    cliche-transcendence: 15
    dialogue: 15
    prose-style: 10
  max_iterations: 3
  global_max_iterations: 50
---

# Chapter Drafter: Orchestrator Skill

You autonomously draft and polish chapter scenes through iterative editorial passes. Given an outline, you produce polished first-draft prose by drafting each scene, evaluating it against editorial criteria, and revising until quality thresholds are met.

## Core Principle

**Orchestration is iteration with hierarchy.** Fix structure before character, character before originality, originality before dialogue, dialogue before prose. Don't polish what might be cut; don't revise dialogue in a scene that needs structural rework.

---

## Prerequisites

Before invoking this skill, ensure:

1. **Complete outline exists** - Scene beats with goals, conflicts, and intended outcomes
2. **Characters defined** - Lie/want/need, voice patterns, arc positions
3. **World established** - Setting details sufficient for scene work
4. **Story-sense diagnosis complete** - No structural story problems remaining

**Do NOT use this skill if:**
- Outline is still in flux
- Character arcs undefined
- Story-sense would diagnose structural problems

---

## The Orchestration Loop

```
FOR each scene in chapter outline:

    1. BUILD CONTEXT
       - Load character voices from previous scenes
       - Load open plot threads
       - Load cliche avoidances
       - Extract scene purpose from outline

    2. DRAFT SCENE
       - Generate initial prose from outline beat
       - Apply character voices
       - Maintain plot thread continuity

    3. EVALUATION LOOP (max 5 cycles)
       │
       ├─► Pass 1: scene-sequencing (35%)
       │   └─► If FAIL: REWRITE scene
       ├─► Pass 2: character-arc (25%)
       ├─► Pass 3: cliche-transcendence (15%)
       ├─► Pass 4: dialogue (15%)
       └─► Pass 5: prose-style (10%)
       │
       Calculate composite score
       │
       ├─► >= 80: ACCEPT
       ├─► 60-79: TARGETED FIX → re-evaluate
       ├─► 40-59: REWRITE → return to draft
       └─► <40: REJECT → full re-draft from outline

    4. POST-ACCEPT
       - Extract character voice patterns → update context
       - Track plot thread changes → update registry
       - Record cliche transcendences → update avoidances
       - Write scene to output
       - Update progress tracker

END FOR
```

---

## Pass Criteria

### Pass 1: Scene-Sequencing (35% weight)

Evaluates Goal-Conflict-Disaster structure and pacing.

| Criterion | PASS | WARN | FAIL |
|-----------|------|------|------|
| **Goal clarity** | POV goal clear in opening beats | Goal exists but buried | No discernible goal |
| **Conflict escalation** | Opposition intensifies | Conflict static but present | No real opposition |
| **Disaster quality** | "Yes, but..." or "No, and..." | Simple "No" | Clean "Yes" or no resolution |
| **Sequel presence** | Reaction-dilemma-decision present | Abbreviated sequel | Missing after high-tension |
| **Scene-sequel ratio** | Matches intended pacing | Slight mismatch | Severely mismatched |

**Critical:** If scene-sequencing FAILS, do NOT proceed to other passes. Structural problems invalidate downstream evaluation.

### Pass 2: Character-Arc (25% weight)

Evaluates transformation consistency and arc progress.

| Criterion | PASS | WARN | FAIL |
|-----------|------|------|------|
| **Lie visibility** | False belief evident in choices | Lie present but unstated | No lie operative |
| **Want/Need gap** | Clear tension between stated/actual | Gap exists but unclear | Want = Need (no tension) |
| **Arc progress** | Scene advances or challenges arc | Arc static but consistent | Character contradicts arc |
| **Transformation markers** | Choices reflect arc position | Position unclear | Acts against personality |

### Pass 3: Cliche-Transcendence (15% weight)

Evaluates originality via orthogonality test.

| Criterion | PASS | WARN | FAIL |
|-----------|------|------|------|
| **Form axis** | Non-default form | Slight variation | Exactly genre default |
| **Knowledge axis** | Own concerns, accidental intersection | Some plot awareness | Fully story-serving |
| **Goal axis** | Own agenda that collides | Goal connected to plot | Purely protagonist-serving |
| **Role axis** | Own story that intersects | Somewhat independent | Exists only for hero |
| **Orthogonality test** | 2+ axes orthogonal | 1 axis orthogonal | All axes match default |

### Pass 4: Dialogue (15% weight)

Evaluates voice distinctiveness, subtext, and function.

| Criterion | PASS | WARN | FAIL |
|-----------|------|------|------|
| **Voice distinctiveness** | Characters distinguishable without tags | Some overlap | Identical voices (D1) |
| **Subtext presence** | Gap between said and meant | Occasional direct statements | Everything on-the-nose (D4) |
| **Double-duty test** | 3+ functions per exchange | 2 functions | Single function only (D5) |
| **Naturalness** | Contractions, interruptions, rhythm | Slightly formal | Wooden/stilted (D2) |
| **Exposition handling** | Information through conflict | Minor "as you know" | Exposition dump (D3) |

### Pass 5: Prose-Style (10% weight)

Evaluates sentence-level craft.

| Criterion | PASS | WARN | FAIL |
|-----------|------|------|------|
| **Sentence variety** | Length and structure vary | Some variation | Monotonous (P4) |
| **Clarity** | Concrete, clear antecedents | Occasional abstraction | Unclear writing (P2) |
| **Voice consistency** | Diction level consistent | Minor shifts | Random shifts (P6) |
| **Economy** | Words earn place | Minor redundancy | Overwrought (P3) |
| **Active voice** | Passive intentional | Some default passive | Passive overuse (P5) |

---

## Composite Scoring

Each pass produces a score from 0-100:
- All PASS = 100
- Each WARN = -15
- Each FAIL = -40

**Composite = SUM(pass_score × pass_weight)**

| Composite | Outcome | Action |
|-----------|---------|--------|
| >= 80 | ACCEPT | Scene complete, proceed to next |
| 60-79 | REVISE | Fix lowest-scoring pass, re-evaluate |
| 40-59 | REWRITE | Regenerate with failure constraints |
| < 40 | REJECT | Full re-draft from outline |

---

## Iteration Limits

| Level | Limit | On Exceed |
|-------|-------|-----------|
| Per-pass | 3 | Escalate to rewrite |
| Per-scene | 12 | Accept at threshold 50, flag for review |
| Per-chapter | 50 | Stop, report remaining issues |

**Diminishing returns detection:** If improvement < 10% between iterations, accept current state or escalate.

---

## Context Accumulation

Maintain across scenes:

### Character Voices
After each scene, extract and store:
- Vocabulary patterns per character
- Sentence rhythm patterns
- Directness level
- Verbal tics and avoidances

Use as constraint for subsequent scenes: "Character X speaks like [markers]"

### Plot Threads
Track:
- **Open threads** - Introduced, not resolved
- **Closed threads** - Resolved this chapter
- **Foreshadowing** - Planted for future payoff

Each scene checks:
- No contradiction with established facts
- Open threads acknowledged or advanced
- At least one element progresses

### Cliche Avoidances
After cliche-transcendence pass, record:
- Which defaults were avoided
- How they were transcended
- New elements that feel fresh

Use as constraint: "Already transcended [X], maintain freshness"

---

## Progress Tracker

Use the progress tracker template to persist state:

```markdown
## Chapter Progress: [Title]
Started: [timestamp]
Current: Scene [N], Pass [M], Iteration [K]

### Scenes
| Scene | Status | Pass | Iterations | Score | Issues |
|-------|--------|------|------------|-------|--------|

### Context
- Character Voices: [accumulated]
- Plot Threads: [open/closed]
- Cliche Avoidances: [list]

### Change Log
- [timestamp] [change]
```

---

## Revision Strategy

### Targeted Fix (score 60-79)
1. Identify lowest-scoring pass
2. Extract specific failure criteria
3. Generate minimal fix addressing that criterion
4. Re-evaluate that pass + downstream passes
5. If pass improves, recalculate composite

### Rewrite (score 40-59)
1. Preserve scene goal from outline
2. Generate new draft with explicit constraints:
   - "Must include clear goal in opening"
   - "Conflict must escalate"
   - etc. based on failures
3. Re-run full evaluation loop

### Reject (score < 40)
1. Return to outline beat
2. Re-draft from scratch
3. Treat as new scene (reset iterations)

---

## Conflict Resolution

When fixing one pass breaks another:

1. **Detect:** Re-run all passes after any fix
2. **Compare:** Did any pass regress?
3. **Prioritize:** Higher-weight pass wins ties
4. **Seek synthesis:** Can fix satisfy both?
5. **Accept trade-off:** If irreconcilable, accept per hierarchy

**Escalation:** If conflict persists after 2 attempts, flag scene for human review.

---

## Anti-Patterns

### The Infinite Polisher
**Pattern:** Keeps iterating because one criterion is at WARN.
**Fix:** WARN is acceptable. Accept at threshold after iteration limit.

### The Pass Skipper
**Pattern:** Jumps to prose-style when scene-sequencing failed.
**Fix:** Hard gate on structural passes. FAIL blocks progression.

### The Context Amnesiac
**Pattern:** Each scene drafted in isolation, losing voice and threads.
**Fix:** Explicit context loading before each scene draft.

### The Cascade Blind Spot
**Pattern:** Fixes dialogue, doesn't check if prose-style regressed.
**Fix:** Always re-evaluate current pass + downstream after any fix.

### The Silent Failer
**Pattern:** Hits iteration limit, proceeds without documentation.
**Fix:** Log all limit exits with categorized remaining issues.

---

## Output Persistence

### Progress Tracker
- **Location:** `context/chapter-drafter/[chapter]-progress.md`
- **Update:** After each scene acceptance
- **Purpose:** Resume point if interrupted

### Scene Output
- **Location:** `drafts/[story]/[chapter]/scene-[N].md`
- **Update:** On scene acceptance
- **Purpose:** Accumulated draft prose

### Context State
- **Location:** `context/chapter-drafter/[chapter]-context.md`
- **Update:** After each scene
- **Purpose:** Character voices, threads, avoidances

---

## Integration

### Inbound (feeds into chapter-drafter)
| Skill | What it provides |
|-------|------------------|
| outline-collaborator | Scene beats with goal-conflict-disaster |
| character-arc | Lie/want/need for each character |
| worldbuilding | Setting details for scene work |
| story-sense | Confirmation structure is solid |

### Outbound (chapter-drafter produces)
| Output | Next step |
|--------|-----------|
| Draft chapter | revision (for full manuscript revision) |
| Flagged scenes | Human review |
| Context state | Next chapter drafting |

---

## Example Invocation

**Input:** Chapter outline with 5 scene beats

**Process:**
1. Load outline, confirm prerequisites
2. Initialize progress tracker
3. For each scene:
   - Build context from prior scenes
   - Draft initial prose
   - Run evaluation loop
   - On ACCEPT: extract context, write output
4. Complete: 5 polished scenes, flagged issues documented

**Output:**
- 5 scene files in `drafts/[story]/[chapter]/`
- Progress tracker showing all iterations
- Context file for next chapter
- List of any flagged issues for human review
