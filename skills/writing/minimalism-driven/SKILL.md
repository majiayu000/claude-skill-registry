---
name: minimalism-driven
description: 'Enforce minimalism as doctrine while authoring code: start from the null solution and gate every addition on a named, demonstrated need before it is written. Use when starting an implementation where scope creep, speculative abstraction, or unneeded surface is a risk, or when the user says "minimal", "bare minimum", or "no gold-plating".'
---

# Minimalism-Driven Development

## Overview

Minimalism here is not a preference; it is enforced doctrine. The baseline method normally fires at review time, after the code exists: principle-first minimalism (delete > edit > add), Minimal Sufficient Change, and the Excess / Graft / Sprawl rejection grounds. This skill moves those gates to authoring time: every addition must clear them **before** it is written, not after.

The operating hypothesis is the null solution: the smallest artifact that could possibly satisfy the literal ask, which is often no new code at all (an existing utility, a config change, or a deletion). The burden of proof sits on every departure from null. Code that cannot name the need it serves does not get written.

This is an in-flight posture for producing new code. It is not a post-hoc pass: compressing an existing diff is `simplify`, opportunistic cleanup while touching nearby code is `cleanup-codebase`, and routing compression across domains is `tidy`.

## When to Use

- Starting any implementation whose scope could plausibly grow past the literal ask
- The request is small but the surrounding codebase invites "while I'm here" additions
- Prior work in the area shipped speculative abstractions, dead config, or unused parameters
- The user says "minimal", "bare minimum", "keep it small", or "no gold-plating"

**When NOT to use:**

- Exploratory spikes explicitly framed as throwaway; doctrine gates slow discovery, so apply them when the keeper is written
- The ask itself demands breadth (a full lifecycle feature, a migration): the doctrine still applies per-addition, but the null solution is scoped to the ask, not to zero

## The Process

Copy this checklist when applying the skill:

```
NULL    — [ ] state the null solution before writing any code
NEED    — [ ] name the demonstrated need for each departure from null
GATE    — [ ] pass delete > edit > add and Excess/Graft/Sprawl before writing
PROVE   — [ ] after writing, confirm removal of each element breaks a named need
STOP    — [ ] stop at the literal ask
```

### Step 1: NULL: State the null solution

Before any code, write one or two lines naming the smallest artifact that could satisfy the literal ask. Candidates in order: nothing (the behavior already exists), a deletion, a config or data change, a call to an existing utility, an edit to existing code, new code. Grep for the existing utility before concluding it does not exist.

If you cannot state the null solution compactly, you do not yet understand the ask. Resolve that first.

### Step 2: NEED: Name the need per addition

Every departure from the null solution names the demonstrated need it serves: a failing test, a named requirement from the ask, an observed defect, a real second caller. "We might need it" is not a need. An addition whose need you cannot write in one line is banned until you can.

### Step 3: GATE: Enforce precedence and rejection grounds before writing

For each named need, satisfy it in precedence order. **Delete** code that causes the gap, then **edit** existing code, and only then **add** new code. Adding is the last resort, not the default motion.

A planned addition that trips a ground is not written. Rework the shape until it passes or the need dissolves.

### Step 4: PROVE: Removal test after writing

After the code exists, walk the diff element by element (function, parameter, branch, config key, import) and ask: does removing this break a need named in Step 2? If removal breaks nothing named, remove it now. The diff at the end contains only elements whose absence would fail a named need.

### Step 5: STOP: The literal ask is the finish line

Stop at sufficiency. Adjacent improvements, hardening, and generalization beyond the ask are surfaced as a one-line note, never implemented uninvited. Completeness of imagination is not the target; the ask is.

## Mandates, not suggestions

1. **The null solution is the starting hypothesis.** The burden of proof is on every addition, never on the absence of code.
2. **Delete > edit > add is a precedence order.** Skipping straight to "add" without attempting delete and edit is a doctrine violation, not a style choice.
3. **Every addition names its need before it is written.** Post-hoc justification is rationalization.
4. **The rejection grounds fire pre-write.** Excess, Graft, and Sprawl are authoring gates here, not review findings.
5. **Scope equals the literal ask.** Unrequested features, refactors, and flexibility are Excess regardless of quality.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll need it later" | You will need *something* later; almost never this. Add it when the need is demonstrated. |
| "It's only a few lines" | Lines are not the unit of cost; concepts are. A small speculative surface still taxes every future reader. |
| "This makes it more flexible" | Flexibility with one caller is speculation. The second caller defines the right abstraction; guessing it now gets it wrong. |
| "Writing a new helper is faster than finding the existing one" | That is Graft. The grep costs a minute; the duplicate costs every future change made twice. |
| "The wrapper makes it cleaner" | A wrapper that renames or forwards without removing coupling is Sprawl: ceremony, not cleanliness. |
| "While I'm here…" | The ask is the scope. Note the adjacent improvement in one line and move on. |

## Red Flags

- An abstraction, interface, or factory with exactly one implementation or caller
- A parameter or config key whose value never varies in the codebase
- A new utility written before searching for an existing equivalent
- A diff meaningfully larger than the explanation of the need it serves
- Additions that appeared during implementation with no need named in Step 2
- "Foundation for later" code that no current need exercises

## Verification

After applying minimalism-driven development:

- [ ] The null solution was stated before any code was written
- [ ] Every addition in the diff maps to a need named before it was written
- [ ] Delete and edit were attempted before each add
- [ ] The removal test passed: no element survives whose absence breaks nothing named
- [ ] The diff's scope equals the literal ask; adjacent improvements are notes, not code
