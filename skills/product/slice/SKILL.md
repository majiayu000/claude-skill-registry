---
name: slice
description: Turn a feature into well-defined, independently shippable slices — whether it's an epic that needs breaking apart or a single story that needs sharpening into a job story
argument-hint: "[feature description]"
disable-model-invocation: true
---

## Phase 1: Understand the Work

If no feature is specified, open with:

**"What are you building? Describe the feature or capability — big or small."**

Wait for their answer before proceeding.

Once the feature is known, ask three things — conversationally, not as a form:

**"Before we slice this, I need to understand it. Three things:**

**Who is this for — specifically? Not 'users', but which person, in which moment, with which need.**

**What does done look like? When this ships, what can that person do that they can't do today?**

**What's the part you're least sure about — technically, or in terms of what the user actually needs?"**

Wait for their answers. Listen for: vagueness about the user (a sign the scope isn't understood), vagueness about done (a sign it will expand), and what they flag as uncertain (that's where the risk lives).

If their answers are vague, ask one follow-up before moving on. Do not proceed to slicing on work you don't understand.

---

## Phase 2: Shape the Slices — Socratically

Based on the size and complexity of the feature, take one of two paths. Do not announce which path you're taking — just follow the one that fits.

### Path A: The feature is already small

If the feature is a single, focused piece of work, help them sharpen it into a well-defined job story. Read `~/.claude/skills/slice/examples/job-stories.md` for the job story format. Guide them with:

- "What's the specific situation the user is in when they need this? Not just 'using the app' — what moment triggers the need?"
- "What do they want to do in that moment — and why does it matter to them?"
- "How would you know this is done? What can the user do that they couldn't before — something you could demonstrate in 30 seconds?"

Push on scope:

- "Is this actually one thing, or are you sneaking two things in? Could any part of this ship on its own?"
- "Is there a simpler version that still solves the user's problem in that moment?"

Push on acceptance criteria:

- "How would you verify this actually works? What are the specific things you'd check — the happy path, the edge cases, the error states?"
- "If you handed this to someone who's never seen the feature, what checklist would they need to confirm it's done?"

If pushing reveals that the feature is actually multiple slices, switch to Path B.

### Path B: The feature is large

Guide them to find the slices themselves, one question at a time.

Start here:

**"What's the absolute minimum a user would need to get any value from this at all — the smallest thing that's real, not a prototype?"**

This is the walking skeleton (thoughtbot / XP). It's almost always smaller than they think. Read `~/.claude/skills/slice/examples/full-stack-slices.md` to understand the principle: cut vertically through the stack, not horizontally. Push on it:

- "Could a user actually do something with that, or is it just plumbing?"
- "Is that one slice, or are you combining two things that could ship separately?"
- "If you shipped only that, what feedback could you get from a real user?"

Once the first slice is clear, work outward:

- "What's the next most important thing — not the next most obvious thing to build, but the next most valuable to the user?"
- "What's the riskiest assumption — the thing that, if you're wrong, changes everything? Should that be a slice?"
- "Is there anything in here that only exists to support another feature, not the user? That's probably not a slice."
- "Which slices depend on each other, and which are actually independent?"

As each slice takes shape, push on acceptance criteria:

- "How would you verify this slice works? What specific things would you check — happy path, edge cases, error states?"
- "If you handed this to someone who's never seen the feature, what checklist would they need to confirm it's done?"

Keep pushing until they've named the full set. Validate each slice against two tests — ask them:

1. "Can this ship independently — could it go to production on its own without the others?"
2. "Can a user or stakeholder see the value — is this end-to-end, or is it a layer?"

If a slice fails either test, it's either too big or it's not a slice.

---

## Phase 3: Deliverable

### For a single slice

Produce a job story. Read `~/.claude/skills/slice/examples/job-stories.md` for the format:

---

**[Short name]**
**When** [specific situation the user is in], **I want** [what they need to do] **so** [the outcome that matters to them].
**Ships when:** [The observable behavior that marks it done — what a user can do, not what the code does.]
**Acceptance criteria:**

- [ ] [Specific, verifiable condition — the happy path]
- [ ] [Edge case or boundary condition]
- [ ] [Error state or failure handling, if applicable]
      **Risk / learning:** [What this slice tests or de-risks, or "Low risk" if straightforward.]

---

Close with:

**"Is this actually the smallest thing that delivers real value — or did you sneak scope into it?"**

### For multiple slices

Guide the sequencing:

**"Now order them. First: what ships first, and why — not what's easiest to build, but what delivers the most learning or value earliest?"**

Ask:

- "Which slice would tell you the most about whether this is heading in the right direction?"
- "Which slice has the most technical risk — is it early enough in the sequence?"
- "If you ran out of budget after two slices, which two would you want to have shipped?"

When sequencing is agreed, produce the deliverable. Read `~/.claude/skills/slice/example.md` for a complete example of the expected format and quality. Format each slice as a job story:

---

**Slice [N]: [Short name]**
**When** [specific situation the user is in], **I want** [what they need to do] **so** [the outcome that matters to them].
**Ships when:** [The observable behavior that marks it done — what a user can do, not what the code does.]
**Acceptance criteria:**

- [ ] [Specific, verifiable condition — the happy path]
- [ ] [Edge case or boundary condition]
- [ ] [Error state or failure handling, if applicable]
      **Depends on:** [Any prior slice it requires, or "none".]
      **Risk / learning:** [What this slice tests or de-risks.]

---

After the full list, give a one-paragraph sequencing rationale: why this order, what it de-risks early, and what it leaves for later.

Close with:

**"Look at your first slice. Is it actually the smallest thing that delivers real value — or did you sneak scope into it?"**

Wait for their answer. Respond with one short paragraph: what their answer reveals about how they naturally scope work, and whether they tend to start too big or too small.

## Tone

Collaborative but rigorous. Slicing is a thinking tool, not a planning ceremony. Push back on slices that are too big, too vague, or not actually end-to-end. The test is always: could a real user touch this, and could a stakeholder see the value? If not, it's not a slice yet.
