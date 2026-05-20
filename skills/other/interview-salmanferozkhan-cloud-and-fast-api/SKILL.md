---
name: interview
description: |
  This skill conducts discovery conversations to understand user intent and agree on approach before taking action. It should be used when the user explicitly calls /interview, asks for recommendations, needs brainstorming, wants to clarify, or when the request could be misunderstood. Prevents building the wrong thing by uncovering WHY behind WHAT.
---

# Interview Skill

Prevent building the wrong thing. Discover user's intent (WHY), validate assumptions, and agree on approach (WHAT) before taking action.

## What This Skill Does

- Discovers INTENT behind surface requests (WHY they want it)
- Surfaces and validates AI's assumptions before acting
- Explores solution options informed by intent
- Reaches mutual agreement on both problem and solution
- Works for any context: software, documents, brainstorming, automation

## What This Skill Does NOT Do

- Follow rigid scripts
- Skip to implementation without understanding
- Accept surface requests without exploring intent
- Make assumptions without validating them

---

## Core Problem This Skill Solves

**AI builds the wrong thing because it:**
1. Takes surface requests literally without understanding intent
2. Makes hidden assumptions it never validates
3. Proceeds without confirming alignment

**This skill ensures:**
1. Intent (WHY) is discovered, not just request (WHAT)
2. Assumptions are surfaced and validated
3. Both problem and solution are agreed before proceeding

---

## The WHY + WHAT Model

```
Surface WHAT → Discover WHY → Surface Assumptions →
Informed WHAT → Agree on Both → Proceed
```

| Phase | Purpose | Example |
|-------|---------|---------|
| **Surface WHAT** | Capture initial request | "Add dark mode" |
| **Discover WHY** | Uncover intent/problem | "Eye strain for night workers" |
| **Surface Assumptions** | Expose AI's hidden assumptions | "Assuming web app, not mobile" |
| **Informed WHAT** | Solution options based on WHY | "Dark mode + auto-brightness + schedule" |
| **Agree on Both** | Confirm problem AND solution | "Solving eye strain via dark mode with auto-switch" |

---

## When to Trigger

| Trigger | Example |
|---------|---------|
| Explicit invocation | `/interview`, "let's clarify" |
| Request could be misunderstood | Ambiguous, complex, or multi-part requests |
| Recommendations needed | "What should I use for..." |
| Brainstorming | "Help me think through..." |
| High-stakes work | Where wrong output wastes significant effort |

**Don't over-trigger**: Simple, clear requests don't need full discovery.

---

## Discovery Flow

### Before Starting

Gather available context before asking questions:

| Source | Gather |
|--------|--------|
| **Conversation** | User's stated request, prior context |
| **Available Context** | Information already shared in session |
| **Skill References** | Question patterns from `references/` |

### 1. Surface WHAT

Capture the initial request clearly.

```
"Let me make sure I understand - you're asking for [X]?"
```

### 2. Discover WHY

**This is the critical step most AI skips.**

Go beyond WHAT to understand WHY:

| Ask | To Discover |
|-----|-------------|
| "What problem does this solve?" | The real need |
| "Why now?" | Urgency and context |
| "What happens if we don't do this?" | Stakes and priority |
| "Who benefits and how?" | Users and value |
| "What led to this request?" | Background and triggers |

**Techniques for WHY:**

**Laddering** - Dig into abstract goals:
```
"Dark mode" → "Why?" → "Eye strain" → "Why an issue?" → "Night shift workers"
```

**5 Whys** - Uncover root need:
```
"Export feature" → Why? → "Share reports" → Why? → "Stakeholder reviews" → Root need
```

**Structuring Clarifications**:

When presenting multiple questions, distinguish must-know from nice-to-know:

```
## Required Clarifications
1. [Critical question - blocks progress]
2. [Critical question - affects core approach]

## Optional Clarifications (if relevant)
3. [Nice-to-know - can assume reasonable default]

Note: Keep to 1-4 questions per round. Build on answers.
```

### 3. Surface Assumptions

**This prevents "builds wrong thing."**

AI always makes assumptions. Surface them explicitly:

```
"I'm assuming:
- This is for [platform/context]
- Users are [type]
- We need to support [X] but not [Y]
- [Other assumption]

Are these correct?"
```

**Common hidden assumptions:**
- Technology/platform
- User expertise level
- Scale/performance needs
- Integration requirements
- What's in vs out of scope

### 4. Informed WHAT

Now that WHY is clear, explore WHAT options:

```
"Given that you need [WHY], we could:
1. [Option A] - [trade-off]
2. [Option B] - [trade-off]
3. [Option C] - [trade-off]

Which fits your intent best?"
```

**Key**: Options should address the WHY, not just the surface WHAT.

### 5. Agree on Both

Confirm understanding of BOTH problem and solution:

```
## Understanding

**Problem (WHY)**: [What we're solving and why it matters]

**Solution (WHAT)**: [What we'll build/do]

**Key decisions**:
- [Decision 1]
- [Decision 2]

**Not included**: [Explicit scope boundaries]

Does this capture it correctly?
```

**Only proceed after explicit confirmation.**

---

## Depth Check

How do you know understanding is deep enough?

### Surface Understanding (NOT enough)
- Can repeat what user asked for
- Know the immediate request
- Haven't explored why

### Deep Understanding (ENOUGH)
- [ ] Know WHY they want it, not just WHAT
- [ ] Know what problem it solves
- [ ] Assumptions are surfaced and validated
- [ ] Know who benefits and how
- [ ] Know what's explicitly out of scope
- [ ] Could explain it to someone else accurately
- [ ] User confirmed understanding is correct

**Test**: If you proceeded now and built something, would user say "yes, that's what I meant" or "no, you misunderstood"?

---

## Assumption Categories

Surface assumptions in these areas:

| Category | Example Assumptions |
|----------|---------------------|
| **Context** | Platform, environment, existing systems |
| **Users** | Who they are, expertise level, needs |
| **Scale** | Volume, performance requirements |
| **Scope** | What's included vs excluded |
| **Quality** | Standards, constraints, requirements |
| **Timeline** | Urgency, phases, dependencies |

---

## Anti-Patterns

| Anti-Pattern | What Happens | Fix |
|--------------|--------------|-----|
| Skip WHY | Build wrong solution | Always ask why before how |
| Hidden assumptions | Surprise misalignment | Surface and validate explicitly |
| Accept surface request | Miss real need | Dig deeper with laddering/5 whys |
| Proceed without confirm | Waste effort | Get explicit "yes, proceed" |
| Over-question simple requests | Annoy user | Match depth to complexity |

---

## Tool Adaptation

Use whatever tools are available:

| Goal | Approach |
|------|----------|
| Ask questions | Interactive tools if available, otherwise conversation |
| Research context | Web search if needed and available |
| Present options | Structured choices if available |

The skill describes WHAT to do. The agent uses available tools.

---

## Output: Understanding Summary

Match formality to situation:

**Quick** (simple requests):
```
Got it: [WHAT] to solve [WHY]
Proceeding with [approach]. Confirm?
```

**Standard** (most cases):
```
## Understanding

**Problem (WHY)**: [Intent and problem being solved]
**Solution (WHAT)**: [What we'll do]
**Key points**: [Important details]
**Not included**: [Scope boundaries]

Ready to proceed?
```

**Detailed** (complex work):
See `references/summary-templates.md`

---

## Quick Reference

```
1. Surface WHAT → "You're asking for X?"
2. Discover WHY → "What problem does this solve?"
3. Surface assumptions → "I'm assuming A, B, C - correct?"
4. Informed WHAT → "Given WHY, we could do X, Y, or Z"
5. Confirm both → "So we're solving [WHY] by doing [WHAT]?"
6. Proceed → Only after explicit confirmation
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/question-patterns.md` | Techniques for discovering WHY and surfacing assumptions |
| `references/anti-patterns.md` | Common mistakes that lead to building wrong thing |
| `references/summary-templates.md` | Output formats for different situations |
