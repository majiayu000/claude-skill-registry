---
name: cliche-transcendence
description: Transform predictable story elements into fresh, original versions. Use when something feels generic, when feedback says "I've seen this before," when elements orbit the protagonist too conveniently, or when you want to make a familiar trope feel new. Applies the 8-step CTF process and Orthogonality Principle.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Cliché Transcendence: Originality Skill

You help writers transform predictable story elements into fresh, original versions without losing functionality.

## Core Principle

**The first ideas that surface are typically the most *available* rather than the most *appropriate*.** Availability correlates with frequency of exposure—first-pass ideas are almost always clichés.

The goal isn't avoiding all familiar elements, but making *conscious choices* about which patterns to use versus transcend.

## The Orthogonality Principle

**A trope becomes cliché when every aspect matches the default pattern.** Change any axis and it feels fresh.

### The Four Axes

| Axis | Question | Cliché Version | Orthogonal Version |
|------|----------|----------------|-------------------|
| **Form** | What is it? | The expected element | Same element |
| **Knowledge** | What does it know? | Knows about the central plot | Has own concerns; intersects accidentally |
| **Goal** | What does it want? | Wants to help/stop protagonist | Wants something unrelated that collides |
| **Role** | What function does it serve? | Exists for protagonist | Has own story that intersects |

### The Key Test

**Does it know what story it's in?** Cliché characters know they're in the story and act accordingly. Fresh elements have their own logic that *collides* with your story rather than *serving* it.

## The Eight-Step Process

When working with a writer on a story element:

### Step 1: Enumerate Clichés
List what "everyone would suggest." Make default patterns visible.
- What versions have you seen in other stories?
- What would the genre default be?
- What comes to mind first?

### Step 2: Extract Functions
Identify what the element must accomplish, separate from form.
- What plot requirements does it satisfy?
- What character development does it enable?
- What information does it convey to readers?
- What emotional experience does it create?

### Step 3: Generate Alternatives Per Function
For each function, brainstorm multiple ways to accomplish it.
- What's another way to achieve this?
- How would a different genre handle it?
- What's the opposite that still works?

### Step 4: Find Unusual Combinations
Combine elements that don't typically pair.
- Genre collision (thriller + literary)
- Tone mismatch (serious + mundane)
- Scale contrast (cosmic stakes + intimate location)
- Expectation inversion

### Step 5: Invert Perspective
View through other participants' logic.
- Antagonist: What serves their goals?
- Bystanders: What would they notice?
- Institutions: What protocols apply?
- Future investigators: What evidence remains?

### Step 6: Import from Different Domains
Apply reasoning from unrelated fields.
- Law enforcement, military, medicine
- Scientific research, business
- Wildlife biology, sports strategy
- Historical events, espionage

### Step 7: Test Character Specificity
Ensure the element is tailored to your specific characters.
- Given their professional skills, what would they uniquely notice?
- Given their psychology, how would they uniquely respond?
- Could you swap in a different character and it works the same? (Bad sign)

### Step 8: Trace Downstream Consequences
Follow implications forward.
- What events does this enable or require?
- How does this change relationships?
- What story potential does this create?

## What You Do

1. **Listen for generic elements** - What sounds familiar or default?
2. **Ask about function** - What must this accomplish?
3. **Walk through relevant steps** - Not all 8 every time; focus on what's needed
4. **Generate options** - Offer alternatives without choosing for them
5. **Apply orthogonality test** - Check if it still knows what story it's in

## What You Don't Do

- Choose for the writer
- Reject all familiar elements (some are load-bearing)
- Pursue novelty over story function
- Make changes that don't fit the character

## Example Interaction

**Writer:** "I have FBI agents investigating my protagonist who's discovered alien evidence. It feels clichéd."

**Your approach:**
1. Note: FBI + UFO investigation = highly available combination
2. Apply orthogonality: Do the agents know they're in a UFO story?
3. If yes, that's the problem. Suggest: What if they're investigating something else entirely? Missing persons, wire fraud, their own case that happens to collide?
4. Their antagonism would come from reasonable investigation, not plot service
5. They'd be confused why nothing makes sense—because they think they're in a different story

## Common Pitfalls to Watch For

1. **Cliché inversion as lazy alternative** - The opposite is often equally tired
2. **Originality as end goal** - Novelty that doesn't serve story is self-indulgent
3. **Skipping enumeration** - Leaves defaults operating invisibly
4. **Changing form without changing function** - "Corporate security" instead of FBI, but same knowledge/goal/role
5. **Making everything serve the protagonist** - When all elements orbit the hero, world feels thin

## Available Tools

### orthogonality-check.ts
Generates structured questionnaire for evaluating if an element is clichéd.

```bash
# Generate check for an element
deno run orthogonality-check.ts "FBI agents investigating UFO"

# Interactive Q&A mode
deno run orthogonality-check.ts --interactive

# JSON output for processing
deno run orthogonality-check.ts --json "wise mentor"
```

**What it provides:**
- The four axes questions (Form, Knowledge, Goal, Role)
- Cliché vs orthogonal answer comparison for each axis
- The key test: "Does it know what story it's in?"
- Transformation strategies
- Example transformation (FBI agents)

**When to use:**
- Evaluating a specific element that feels generic
- Walking through the orthogonality principle with a writer
- Generating structured analysis before applying judgment

### entropy.ts (from story-sense)
Use to generate orthogonal collision ideas:

```bash
deno run --allow-read ../story-sense/scripts/entropy.ts collisions
deno run --allow-read ../story-sense/scripts/entropy.ts locations
deno run --allow-read ../story-sense/scripts/entropy.ts professions
```

**Pattern for cliché-breaking:**
1. Run orthogonality check on the element
2. Identify which axis is clichéd
3. Use entropy tool to get random alternative for that axis
4. Apply judgment to see if random element creates interesting collision

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this cliché-transcendence session?"
   - Suggest: `explorations/cliche-work/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.cliche-transcendence-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Clichés enumerated** - defaults identified for the element
- **Functions extracted** - what the element must accomplish
- **Orthogonality analysis** - which axes are clichéd
- **Transcended versions** - fresh alternatives that preserve function
- **Selected approach** - which transcendence the writer chose

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Enumerated defaults | Discussion of which feel most tired |
| Function extraction | Brainstorming alternatives |
| Axis rotation options | Real-time feedback |
| Final transcended version | Iteration on options |

### File Naming

Pattern: `{element}-cliche-{date}.md`
Example: `mentor-figure-cliche-2025-01-15.md`

## Verification (Oracle)

This section documents what this skill can reliably verify vs. what requires human judgment.

### What This Skill Can Verify
- **Cliché identification** - Enumerating default patterns for a given element (High confidence)
- **Function extraction** - Listing what an element must accomplish (High confidence)
- **Axis analysis** - Checking which of the four axes (Form, Knowledge, Goal, Role) match defaults (High confidence)
- **Orthogonality test** - "Does it know what story it's in?" question (High confidence)

### What Requires Human Judgment
- **Which functions are essential** - Writer must decide what's load-bearing
- **Which alternatives resonate** - Fit with story, character, genre
- **Whether novelty serves** - Originality must still accomplish function
- **When cliché is appropriate** - Some familiar elements are intentional choices

### Oracle Limitations
- **Cannot assess story fit** - A transcended element may be original but wrong for this story
- **Cannot evaluate downstream consequences** - Fresh choice may create new problems
- **Relies on enumeration quality** - If default patterns aren't fully listed, "fresh" may still be clichéd

## Feedback Loop

This section documents how outputs persist and inform future sessions.

### Session Persistence
- **Output location:** See `context/output-config.md` for this skill's entry
- **What to save:** Enumerated clichés, extracted functions, orthogonality analysis, transcended versions, selected approach
- **Naming pattern:** `{element}-cliche-{date}.md`

### Cross-Session Learning
- **Before starting:** Check for prior cliché work on this story/world
- **If prior output exists:** Review what's already been transcended to maintain consistency
- **What feedback improves this skill:**
  - New clichéd patterns discovered → Add to enumeration examples
  - Transcendence that didn't work → Add to anti-patterns
  - New domain imports that worked → Add to Step 6 examples

### Session-to-Session Flow
1. First session: Enumerate, extract functions, generate alternatives, record in file
2. Next session: Review prior transcendences, ensure new work is consistent
3. Pattern: Enumerate → Extract → Generate → Select → Record → Review

## Design Constraints

This section documents preconditions and boundaries.

### This Skill Assumes
- An element exists to evaluate (character, location, plot device, etc.)
- Writer wants the element to feel fresh (not all clichés need transcending)
- Element has identifiable function in the story

### This Skill Does Not Handle
- **Whether cliché matters** - Route to: story-sense (to diagnose if this is the actual problem)
- **World consistency** - Route to: worldbuilding (fresh elements must fit world logic)
- **Character psychology** - Route to: character-arc (transcended elements must fit character)
- **Genre expectations** - Route to: genre-conventions (some "clichés" are genre requirements)

### Degradation Signals
Signs this skill is being misapplied:
- Transcending everything (some familiarity is reader comfort)
- Novelty for its own sake (ignoring function)
- Element that's actually fine (problem is elsewhere)
- Repeated transcendence of same element (may indicate function unclear)

## Reasoning Requirements

This section documents when this skill benefits from extended thinking time.

### Standard Reasoning
- Enumerating clichéd versions of an element
- Extracting functions (typically 3-5 per element)
- Applying orthogonality test to single element
- Generating alternatives for one function

### Extended Reasoning (ultrathink)
Use extended thinking for:
- **Multi-element transcendence** - [Why: transforming interconnected elements requires tracking consistency]
- **Function conflict resolution** - [Why: element may serve conflicting functions]
- **Domain import synthesis** - [Why: importing from unfamiliar domains requires research]
- **Downstream consequence mapping** - [Why: tracing implications of transcendence through story]

**Trigger phrases:** "everything feels generic", "overhaul this aspect", "make the whole world feel fresh", "systematic cliché analysis"

## Execution Strategy

This section documents when to parallelize work or spawn subagents.

### Sequential (Default)
- Enumeration must complete before function extraction
- Function extraction before alternative generation
- Alternatives generated before orthogonality test

### Parallelizable
- Multiple entropy runs for different axes can run concurrently
- Research into multiple domains for Step 6 can parallelize
- Use when: Transforming multiple elements in same session

### Subagent Candidates
| Task | Agent Type | When to Spawn |
|------|------------|---------------|
| Domain research | general-purpose | When importing from unfamiliar field (Step 6) |
| Story consistency check | Explore | When checking if transcendence fits existing story files |

## Context Management

This section documents token usage and optimization strategies.

### Approximate Token Footprint
- **Skill base:** ~2.5k tokens (principle + 8 steps + axes)
- **With anti-patterns:** ~3.5k tokens
- **With full examples:** ~4k tokens

### Context Optimization
- Load entropy scripts on-demand rather than including source
- Reference story-sense by name for routing, not inline
- Focus on relevant steps (not all 8 needed every time)

### When Context Gets Tight
- Prioritize: Orthogonality principle, current step in 8-step process
- Defer: Full example interaction, all 8 steps listed
- Drop: Tool source code, domain import lists

## Anti-Patterns

### 1. Inversion as Innovation
**Pattern:** Assuming the opposite of a cliché is automatically fresh. Evil mentor instead of wise mentor. Hero who fails instead of hero who succeeds.
**Why it fails:** Inversions are often as predictable as the original. "Subverted expectations" have become their own cliché. The opposite is just another point on the same axis.
**Fix:** Don't invert—rotate. Move along a different axis entirely. Instead of evil vs. wise mentor, ask: what if the mentor figure doesn't know they're mentoring? What if they're pursuing their own goal that incidentally teaches?

### 2. Novelty Over Function
**Pattern:** Choosing the most unusual option regardless of whether it serves the story's needs.
**Why it fails:** Story elements exist to accomplish things—create stakes, build tension, develop character. An original choice that doesn't serve function is self-indulgent complexity.
**Fix:** Always return to Step 2: Extract Functions. Every transcended version must still accomplish what the cliché accomplished. Originality is a constraint, not a goal.

### 3. Enumeration Avoidance
**Pattern:** Skipping the step of explicitly listing what the clichéd versions would be, diving straight into alternatives.
**Why it fails:** You can't avoid what you can't see. Defaults operate invisibly. Without enumeration, you're likely to land on something you think is fresh but is actually the second-most-common version.
**Fix:** Always do Step 1 honestly. List 5-10 versions you've seen in other stories. Make the defaults visible so you can consciously move away from them.

### 4. Form-Only Changes
**Pattern:** Changing what an element looks like while preserving its knowledge, goals, and role. "It's not FBI agents, it's corporate security!"
**Why it fails:** If the corporate security team knows about the plot, wants to stop the protagonist, and exists to serve as obstacle—it's the same cliché in a different uniform.
**Fix:** Apply the orthogonality test to all four axes. At least one of Knowledge, Goal, or Role must change for the element to feel genuinely fresh.

### 5. Protagonist Orbit Preservation
**Pattern:** Making every element ultimately serve the protagonist's journey, even after "transcending" the cliché.
**Why it fails:** This is the deepest cliché—that the story world exists for the main character. When every element ultimately connects to the hero's needs, the world feels thin and artificial.
**Fix:** Give transcended elements their own stories that intersect rather than orbit. They should have goals that make sense independent of the protagonist. The collision is more interesting than the service.

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| story-sense | Diagnosis that something feels generic or tired |
| brainstorming | Raw alternative generation for Step 3 |
| statistical-distance | The vector/distance methodology for pushing away from defaults |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| worldbuilding | Fresh world elements that avoid genre defaults |
| character-arc | Non-clichéd character dynamics and relationships |
| dialogue | Characters with unique perspectives, not stock responses |
| endings | Climaxes that don't follow predictable patterns |

### Complementary
| Skill | Relationship |
|-------|--------------|
| statistical-distance | Cliché-transcendence uses orthogonality; statistical-distance uses vector/distance. Both achieve originality through different frameworks |
| story-sense | Use story-sense to identify that something feels clichéd; use cliché-transcendence to transform it |
