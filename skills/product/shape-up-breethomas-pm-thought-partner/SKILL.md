---
name: shape-up
description: Shape work using the Shape Up methodology (Ryan Singer, Basecamp). Walk through the 4-step shaping process to create pitches ready for betting. Distinguishes between established product mode (fixed time, variable scope) and new product mode (looser constraints). Use when planning cycle work, writing pitches, or coaching PMs on shaping.
---

# Shape Up - Shaping Workflow

## Core Philosophy

**Fixed time, variable scope.**

Shape Up inverts traditional estimation:
- You don't estimate how long something takes, then ask for that time
- You decide how much time something is worth, then shape to fit

**Shaped work has three properties:**
1. **Rough** - Visibly unfinished, leaves room for creativity
2. **Solved** - Main elements connected, clear direction
3. **Bounded** - Explicit appetite and no-gos

**The shaper's job:** Define work at the right abstraction level - neither too vague (leaves team lost) nor too detailed (constrains team creativity).

**See:** `skills/shape-up/references/methodology.md` for the full philosophy.

---

## Entry Point

When this skill is invoked, start with:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SHAPE UP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What are you working on?

  1. Shape new work
     → Walk through the 4-step process
     → Output: Pitch ready for betting

  2. Review an existing pitch
     → Challenge boundaries, rabbit holes, no-gos
     → Output: Feedback and improvements

  3. Quick pitch (I know what I want)
     → Skip the coaching, just format
     → Output: Pitch document

  4. Not sure where to start
     → Tell me about the raw idea
     → I'll help figure out if it's ready to shape

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Parse intent from context:**
- If user mentions "pitch" or "shape" a specific feature → Flow 1 (Shape New)
- If user pastes or describes an existing pitch → Flow 2 (Review)
- If user uses `--pitch` flag → Flow 3 (Quick Pitch)
- If user describes a vague idea or problem → Flow 4 (Explore First)

**Command-line shortcuts:**
- `/shape` → Show entry point
- `/shape "feature idea"` → Start Flow 1 with context
- `/shape --review` → Start Flow 2
- `/spec --pitch` → Start Flow 3 (quick pitch format only)
- `/shape --established` → Flow 1 with established product mode
- `/shape --new-product` → Flow 1 with new product mode

---

## Product Mode Check

Before starting the shaping workflow, determine the context:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PRODUCT MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Which mode are you in?

  A. Established product
     → Core features, existing users
     → Fixed time, variable scope (full rigor)
     → Circuit breaker applies

  B. New product / exploration
     → Validating concepts, finding fit
     → Looser constraints, faster iteration
     → Goal: learn, not ship

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Mode affects rigor:**

| Aspect | Established | New Product |
|--------|-------------|-------------|
| Appetite | Strict (1-2 weeks or 6 weeks) | Flexible ("a few days to explore") |
| Rabbit holes | Must be identified and patched | Flag but accept more unknowns |
| No-gos | Explicit and enforced | Directional, may evolve |
| Output | Pitch ready for betting table | Pitch as working document |

---

## Flow 1: Shape New Work

### Step 1: Set Boundaries

**Ask about appetite first:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 1: Set Boundaries
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How much time is this problem worth?

  • Small batch (1-2 weeks)
    → Well-understood, limited scope
    → Quick win or focused fix

  • Big batch (6 weeks)
    → New capability, more unknowns
    → Meaningful user value

What's your appetite?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Then dig into the problem:**

Questions to ask:
1. **What's the raw idea?** (The surface-level request)
2. **What's the actual friction?** (Dig deeper - why does this matter?)
3. **Who experiences this?** (Specific users/personas)
4. **What do they do today?** (Current workaround or pain)

**Challenge weak problem definitions:**
- "Customers want X" → "What's broken that makes them want X?"
- "We need to improve Y" → "What specifically is wrong with Y?"
- "Add a feature for Z" → "What friction does Z solve?"

**Capture:**
- Appetite: [Small batch / Big batch]
- Problem: [Specific friction, who, when]
- Baseline: [What users do today]

### Step 2: Find the Elements

**Guide through solution sketching:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 2: Find the Elements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now let's sketch the solution. Keep it rough.

Questions:
• Where does this fit in the existing product?
• How do users access it?
• What are the main elements/components?
• How do they connect?

Would you like to:
  1. Breadboard it (workflow/screens)
  2. Fat marker sketch it (visual layout)
  3. Just describe it (I'll help structure)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If breadboarding:**
Help structure as: Places → Affordances → Connections

**If sketching:**
Remind: Keep it rough. Thick lines. No details.

**Challenge over-specification:**
- "Here's my wireframe..." → "Let's step back. What are the key elements?"
- Detailed UI → "This is too concrete. What decisions are we making?"

**Capture:**
- Solution sketch (breadboard or fat marker)
- Key elements and how they connect
- Main user flows

### Step 3: Address Risks

**Walk through de-risking:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 3: Address Risks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let's find the rabbit holes before they find you.

Walk me through the solution step by step:
• What happens first?
• Then what?
• What could go wrong?
• What's the riskiest part technically?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Questions to probe:**
1. Does this require unprecedented technical work?
2. Are there parts assumed to fit without validation?
3. Are hard decisions being deferred to the team?
4. What edge cases could blow up scope?

**For each risk identified:**
- Can we patch it now? (Make a decision/trade-off)
- Can we cut it? (Move to no-gos)
- Must we flag it? (Add to rabbit holes section)

**Challenge "it'll be fine" thinking:**
- "The team will figure it out" → "What specifically will they figure out?"
- "It's probably straightforward" → "Walk me through the implementation"

**Capture:**
- Rabbit holes (risks to flag)
- Patches made (trade-offs decided)
- No-gos (explicitly out of scope)

### Step 4: Write the Pitch

**Compile the 5 ingredients:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 STEP 4: Write the Pitch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let me compile everything into a pitch.

The 5 ingredients:
  1. Problem - Why this matters
  2. Appetite - How much time it's worth
  3. Solution - What we'll build (rough)
  4. Rabbit Holes - Known risks
  5. No-Gos - What we're NOT doing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Generate pitch using template from:** `skills/shape-up/references/pitch-template.md`

**Output the pitch, then ask:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PITCH READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Generated pitch document]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What's next?

  • Copy to your pitch doc
  • Create Linear issue from this pitch
  • Review and refine further
  • Shape another feature
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Flow 2: Review Existing Pitch

**When user provides a pitch to review:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PITCH REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'll review this pitch against Shape Up principles.

Checking:
  ☐ Problem - Is the friction specific and real?
  ☐ Appetite - Is time budget explicit?
  ☐ Solution - Rough but solved?
  ☐ Rabbit Holes - Are risks identified?
  ☐ No-Gos - Are boundaries explicit?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Review criteria:**

| Element | Pass | Fail |
|---------|------|------|
| Problem | Specific friction, named users, evidence | Vague "customers want X" |
| Appetite | Explicit time budget (1-2 weeks or 6 weeks) | No time constraint or "ASAP" |
| Solution | Breadboard/sketch, elements connected | Wireframes OR just words |
| Rabbit Holes | Technical risks flagged with mitigation | "Should be straightforward" |
| No-Gos | Explicit exclusions listed | Nothing marked as out of scope |

**Output review:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PITCH REVIEW RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem:     [✓ / ✗] [Brief assessment]
Appetite:    [✓ / ✗] [Brief assessment]
Solution:    [✓ / ✗] [Brief assessment]
Rabbit Holes:[✓ / ✗] [Brief assessment]
No-Gos:      [✓ / ✗] [Brief assessment]

Overall: [Ready for betting / Needs work]

Recommendations:
• [Specific improvement 1]
• [Specific improvement 2]
• [Specific improvement 3]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Flow 3: Quick Pitch

**For experienced users who know what they want:**

Skip the coaching, just ask the minimum questions:

1. What's the problem? (1-2 sentences)
2. What's the appetite? (Small batch or big batch)
3. What's the solution? (Key elements)
4. Any known risks?
5. What's explicitly out?

**Generate pitch immediately** using `skills/shape-up/references/pitch-template.md`

---

## Flow 4: Explore First

**When the idea isn't ready to shape:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NOT READY TO SHAPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This idea might not be ready to shape yet.

Signs it's too early:
• Can't articulate specific friction
• Don't know who has the problem
• Solution is completely unclear
• No evidence it matters

What would help:
• Talk to users experiencing the friction
• Find evidence (support tickets, analytics, interviews)
• Prototype to learn, not to ship

Would you like to:
  1. Dig deeper into the problem now
  2. Plan discovery work first
  3. Shape anyway (accept higher risk)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Integration with Linear MCP

**If Linear MCP is available:**

- Offer to create Linear issue from pitch
- Fetch existing issues for context
- Check team/project for pitch placement

**If Linear MCP not available:**

- Output pitch as markdown
- User can copy to their system

---

## Integration with Other Commands

**`/spec --pitch`** → Routes to Flow 3 (Quick Pitch)

**`/four-risks`** → Complements Step 3 (rabbit hole identification)

**`/now-next-later`** → Betting table output maps to NOW column

---

## Common Shaping Mistakes to Challenge

| Mistake | Challenge |
|---------|-----------|
| "Customers want X" | "What friction makes them want X?" |
| No appetite stated | "How much time is this worth? Small or big batch?" |
| Detailed wireframes | "This is too concrete. What are the key elements?" |
| "Team will figure it out" | "What specifically will they figure out?" |
| No no-gos | "What are you explicitly NOT building?" |
| "Should be straightforward" | "Walk me through the implementation" |

---

## Resources

- `skills/shape-up/references/methodology.md` - Full methodology
- `skills/shape-up/references/techniques.md` - Breadboarding, fat marker, de-risking
- `skills/shape-up/references/pitch-template.md` - 5 ingredients with examples
- [Shape Up (free book)](https://basecamp.com/shapeup)
