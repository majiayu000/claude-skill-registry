---
name: learn-from-this
description: |
  When a session contains a significant failure, misunderstanding, or repeated
  mistake, analyse the root cause and draft a new skill that would have prevented
  it. The skill library should grow from real failures, not hypothetical
  improvements. Every painful debugging session is a skill waiting to be written.
allowed-tools: |
  bash: cat, ls, grep
  file: read, write
---

# Learn From This

<purpose>
The best skills come from real pain. When something goes wrong - wasted hours,
misunderstood requirements, broken code that looked correct - there's a lesson
embedded in that failure. This skill extracts that lesson and encodes it as a
new skill, so the same mistake becomes impossible to repeat.
</purpose>

## Why This Matters

<philosophy>
Most skill libraries are written in advance, based on what someone THINKS will
be useful. They're theoretical. Abstract. Generic.

The best skills are written AFTER failure, based on what actually went wrong.
They're specific. Battle-tested. Born from real pain.

This skill is meta: it creates other skills. The skill library becomes a
living document of hard-won lessons. Every entry is a scar that healed into
armour.
</philosophy>

## When To Activate

<triggers>
Trigger at session end or mid-session when you observe:

**Wasted Time:**
- Spent >30 minutes on something that should have taken 5
- Went down a wrong path and had to backtrack significantly
- Debugged something that had an obvious cause (in hindsight)

**Misunderstandings:**
- Built the wrong thing because requirements weren't clarified
- Made assumptions that turned out to be wrong
- Solved an XY problem instead of the real problem

**Repeated Patterns:**
- Made the same type of mistake twice in one session
- Hit a failure mode you've seen before
- Caught yourself doing something you know is bad practice

**Near Misses:**
- Almost deployed broken code to production
- Almost deleted important data
- Caught a bug at the last second

**User Frustration:**
- User had to repeat themselves
- User expressed frustration at wasted time
- Conversation got contentious or confused
</triggers>

## Instructions

### Step 1: Identify The Failure

What specifically went wrong?

```
Failure Analysis:

What happened:
  [Specific description of the failure]

What should have happened:
  [The correct outcome]

Time/effort wasted:
  [Rough estimate]

Root cause:
  [Why did this actually happen?]
```

### Step 2: Find The Pattern

Is this a general pattern or a one-off?

Questions to ask:
- Could this happen again in a different context?
- Is this a Claude failure mode or a human-Claude interaction failure?
- What was the earliest point this could have been caught?
- What trigger could have detected this situation?

### Step 3: Draft The Skill

```markdown
---
name: [kebab-case-name]
description: |
  When [trigger condition that would have caught this],
  [action that would have prevented the failure].
  [Why this matters in one sentence].
allowed-tools: |
  [only what's needed]
---

# [Skill Name]

<purpose>
[One paragraph: what problem this prevents, born from real experience]
</purpose>

## When To Activate

[Specific triggers based on the failure pattern]

## Instructions

[Steps to prevent the failure]

## NEVER

[Anti-patterns that led to the failure]

## ALWAYS

[Behaviours that would have prevented it]

## The Failure That Spawned This Skill

[Brief description of the original failure - keeps it grounded]
```

### Step 4: Validate The Skill

Before adding to the library:

```
Skill Validation:

Would this skill have prevented the original failure?
  [ ] Yes - clear trigger and action
  [ ] Partially - helps but doesn't fully prevent
  [ ] No - need to rethink

Is the trigger specific enough to activate?
  [ ] Yes - clear condition
  [ ] No - too vague, won't trigger reliably

Is it general enough to be useful again?
  [ ] Yes - pattern will recur
  [ ] No - too specific to this one case

Does a similar skill already exist?
  [ ] No - new pattern
  [ ] Yes - maybe enhance existing skill instead
```

### Step 5: Propose Addition

```
New Skill Proposal:

Name: [skill-name]

Born from: [brief description of the failure]

Would have prevented: [specific outcome]

Skill file:
[full SKILL.md content]

Add to library?
```

## Examples

### Example 1: From "Built Wrong Thing" Failure

**The Failure:**
User asked to "add authentication." I built a full OAuth2 implementation.
User wanted a simple username/password. Wasted 2 hours.

**The Pattern:**
I assumed complexity when simplicity was wanted. Didn't ask "what kind?"

**The Skill:**

```markdown
---
name: how-fancy
description: |
  When a task has multiple complexity levels (auth, database, UI),
  ask which level before implementing. Don't assume enterprise
  when simple is wanted. Don't assume simple when robust is needed.
  One question saves hours.
allowed-tools: |
  file: read
---

# How Fancy?

<purpose>
Tasks like "add auth" or "set up database" have wildly different
implementations based on needs. A question takes 10 seconds. The
wrong assumption wastes hours.
</purpose>

## When To Activate

Before implementing anything with multiple complexity tiers:
- Authentication (basic, session, OAuth, SSO)
- Database (SQLite, Postgres, distributed)
- Caching (memory, Redis, CDN)
- UI (simple, animated, accessible)

## Instructions

Ask:

"Before I start: what level of [X] do you need?

Simple: [description]
Standard: [description]
Robust: [description]

This determines the approach."

## The Failure That Spawned This Skill

Built full OAuth2 when user wanted username/password. 2 hours wasted.
```

### Example 2: From "Didn't Test Edge Case" Failure

**The Failure:**
Wrote function, said "done", user tried empty string, it crashed.
Basic edge case I should have tested.

**The Pattern:**
Declared victory without testing obvious edge cases.

**The Skill:**
This failure contributed to the `prove-it` skill. Instead of creating
a new skill, the lesson was: existing skill wasn't being followed.

Lesson: Sometimes failures mean "use existing skill" not "create new skill."

### Example 3: From "Lost Context" Failure

**The Failure:**
Long session, 50+ messages. User referenced decision from message #12.
I had forgotten and contradicted it. User frustrated.

**The Pattern:**
In long sessions, I lose track of earlier decisions and context.

**The Skill:**

```markdown
---
name: breadcrumbs
description: |
  In sessions longer than 20 messages, periodically summarise:
  key decisions made, current state, remaining work. Combat
  context degradation. Keep a trail back to important moments.
allowed-tools: |
  file: read
---

# Breadcrumbs

<purpose>
Long conversations degrade context. Decisions made early get
forgotten. Users repeat themselves. The fix: explicit checkpoints
that summarise the trail so far.
</purpose>

## When To Activate

Every ~15-20 messages in an ongoing session, or when:
- Starting a new phase of work
- User seems to be repeating something
- You're unsure if something was already decided

## Instructions

Drop a breadcrumb:

"Quick checkpoint:

Decisions so far:
- [Key decision 1]
- [Key decision 2]

Current state:
- [What's done]
- [What's in progress]

Next up:
- [What's remaining]

Anything I'm forgetting?"

## The Failure That Spawned This Skill

Message 50 of a long session. Contradicted a decision from message 12.
User had to re-explain. Frustration ensued.
```

## Meta: This Skill Improving Itself

If this skill fails to capture a lesson properly, that itself is a failure
to learn from. The skill should be updated based on its own shortcomings.

Questions to ask periodically:
- Are the skills being generated actually useful?
- Are they too specific? Too generic?
- Is the trigger-action format working?
- What failures are slipping through?

## NEVER

- Create skills for one-off flukes (must be a pattern)
- Create skills that duplicate existing ones
- Create skills too vague to trigger
- Let a painful failure pass without extracting the lesson
- Blame the user when the failure was yours

## ALWAYS

- Be honest about what went wrong
- Find the root cause, not the symptom
- Write skills specific enough to trigger
- Include the origin failure (keeps it grounded)
- Consider enhancing existing skills before creating new ones

## The Failure That Spawned This Skill

Every skill in this library that wasn't written after real failure.
The theoretical ones are weaker than the battle-tested ones.
This skill ensures future additions come from real pain.
