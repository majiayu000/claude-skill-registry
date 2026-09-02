---
name: shape
description: 'Use when the user says "shape this", "pitch this", "gut check the shape", "fix this pitch", or asks whether a result matches the bet. Shapes work into a fat-marker pitch with five ingredients: problem, appetite, solution, rabbit holes, no-gos. Not for tasks requiring source or remote-system changes; not for detailed implementation plans — use plan.'
---

# Shape

Shaped work is concrete enough to walk through and abstract enough to leave room. Appetite is a constraint you choose, not an estimate you compute. A shaped pitch has five ingredients: **problem**, **appetite**, **solution**, **rabbit holes**, and **no-gos**. Draw it at fat-marker altitude as a **breadboard** or rough sketch, never a wireframe or slogan.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Explicit human says "shape this work" / "what is the appetite" / "pitch this" / "gut check the shape" / "fix this pitch" / "does the result match the bet". |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output only; draws a pitch, gut-check, reshapes, or results-shape-check in chat; creates no files. |
| Done | Shaped pitch returned with five ingredients at fat-marker altitude, or a single verdict on an existing bet. |

## Inputs

- The user's pitch or idea: raw concept, existing shaped document, or finished artifact.
- Slash override for mode: `/shape build-shape | shape-check | to-good-shape | feel-shape`.
- All inputs come from the user's turn or chat context; no external files required.

## Procedure

### Mode selection (auto-detect, override wins)

Route by phrasing:

- Raw idea, `shape this`, `pitch this`, `what's the appetite` → **build-shape**
- `gut check`, `vibe check`, `does this feel right` → **shape-check**
- Existing pitch plus `fix`, `is this well shaped`, `reshape` → **to-good-shape**
- Finished work plus `did we ship the bet`, `match the shape`, results review → **feel-shape**
- Anything else → **build-shape**

Explicit override always wins over auto-detection.

### build-shape

1. **State the problem.** Name the core problem being solved in one or two sentences. The problem frames everything that follows: the appetite, the solution, the no-gos. **Done when:** the problem is stated in the user's terms.
2. **Set the appetite.** Choose small batch or big batch. The appetite bounds the solution; a solution that exceeds it gets cut, the appetite stands. **Done when:** the appetite is chosen and stated.
3. **Rough the solution.** Draw a breadboard (places, affordances, connections). Use the notation below. Draw one sketch per idea; a sketch that needs a legend is over-drawn. **Done when:** the breadboard is drawn with places, affordances, and connections.

   **Breadboard notation** (three elements only):

   - Places: screens, dialogs, states a user can navigate to. Written as underlined names.
   - Affordances: buttons, links, fields, controls. Written as bracketed names.
   - Connections: arrows showing flow between places.

   Worked example, "invoice autopay" bet:

   ```
     Invoice page                Set up autopay             Confirmation
     ------------                --------------             ------------
     invoice total               card on file (y/n)         autopay active note
     [turn on autopay] ───────►  [use card on file] ─────►  [back to invoice]
                                 [enter new card] ──► New card form ──► Confirmation
   ```

   **Fat-marker altitude tests**

   Raise altitude (over-shaped signals): pixel positions, spacing values, exact copy, field lists, column enumerations, task tickets, work breakdown.

   Walk a concrete path (under-shaped signals): no nouns a builder could start from, a goal statement with no places or affordances, an appetite missing or phrased as "as long as it takes".

   Right altitude: a builder could start tomorrow and still owns every design decision inside the lines.

4. **Hunt rabbit holes.** Walk the solution end to end; each hole is declared solved-in-principle (state how) or patched out with a stated decision. **Done when:** every rabbit hole is resolved or patched.
5. **Write no-gos.** Name what this bet deliberately excludes. **Done when:** the no-gos are listed.

### shape-check

Conduct an interactive gut check with the user via the AskUserQuestion tool. Ask one single-select question per axis, and keep the axes separate. Put the `(Recommended)` option first; it carries the default, and choosing it accepts that default. Ask at most 4 questions per fire. If more axes remain, send sequential batches in dependency order. Use `multiSelect` only for additive picks (optional sub-scopes), never for axis-with-default semantics.

Axes: appetite right-sized? which scope cuts? each unresolved rabbit hole, patch or re-shape? no-go boundaries holding?

**Done when:** every axis is answered or the remaining axes are listed as open bets.

### to-good-shape

Diagnose the pitch in one line, then act:

- Over-shaped (design already done: wireframes, field lists, task tickets): raise the altitude, redraw as a breadboard, discard the pixel decisions.
- Under-shaped (words without a walkthrough, unbounded appetite): force an appetite and walk one concrete path through the solution.
- Missing ingredients: add the absent ones; the other four constrain what the new one can say.

Then rewrite the pitch. **Done when:** the pitch is rewritten with all five ingredients at fat-marker altitude.

### feel-shape

Compare a finished artifact to the shaped bet, ingredient by ingredient:

- Problem: does the result address the shaped problem?
- Appetite: bet vs actual spend.
- Solution: does the built thing follow the breadboard's places and connections?
- Rabbit holes: which ones bit, and what did they cost?
- No-gos: respected or crossed?

Emit exactly one verdict: `shipped-the-bet | scope-crept | under-delivered | different-bet`. **Done when:** the single verdict is emitted with per-ingredient evidence.

## Failure and recovery

- Malformed pitch: if the user provides something that cannot be parsed into a pitch, state the failure and ask for clarification. Do not fabricate ingredients.
- No axes for shape-check: if a pitch has no resolvable axes (empty rabbit holes, no appetite), state that and fall back to build-shape to fill the gaps.
- Non-converged feel-shape: if evidence for any ingredient is ambiguous, mark it `unknown` and state it. The verdict must still be emitted.
- No rollback needed: no files written, no state mutated.

## Output

build-shape or to-good-shape: a shaped pitch in chat with five labeled ingredients at fat-marker altitude. shape-check: a revised pitch with every answered axis folded in and unanswered axes listed as open bets. feel-shape: one verdict per ingredient with evidence, plus the single top-line verdict.
