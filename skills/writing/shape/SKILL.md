---
name: shape
description: 'Shape work in the Basecamp Shape Up sense — appetite, breadboard, rabbit holes, no-gos. Use when the user says "shape this work", "what is the appetite", "pitch this", "gut check the shape", "fix this pitch", or "does the result match the bet". Shapes bets on work, not prose — turning fragments into an article is writing-shape.'
metadata:
  short-description: 'Shape Up shaping: build, check, repair, verify'
---

# Shape

Shaped work sits at the right abstraction: concrete enough to walk through, abstract enough to leave room. Appetite is a constraint you choose, not an estimate you compute. A shaped pitch has five ingredients — **problem**, **appetite**, **solution**, **rabbit holes**, **no-gos** — drawn at fat-marker altitude: a **breadboard** or rough sketch, never a wireframe, never a slogan.

## Modes [LOAD-BEARING]

### Mode-selection (hybrid)

Auto-detect from the user's phrasing, with slash-arg override:

- Raw idea, `shape this`, `pitch this`, `what's the appetite` → **build-shape**.
- `gut check`, `vibe check`, `does this feel right` → **shape-check**.
- Existing pitch plus `fix`, `is this well shaped`, `reshape` → **to-good-shape**.
- Finished work plus `did we ship the bet`, `match the shape`, results review → **feel-shape**.
- Anything else → **build-shape** (default).
- Explicit override: `/shape build-shape | shape-check | to-good-shape | feel-shape`. The override always wins.

### build-shape

Shape raw work into a pitch:

1. **Set the appetite.** Pick small batch or big batch. The appetite bounds the solution; a solution that exceeds it gets cut, the appetite stands.
2. **Rough the solution.** Draw a breadboard (places, affordances, connections) or a fat-marker sketch. Load `references/breadboarding.md` for the notation and altitude tests before drawing.
3. **Hunt rabbit holes.** Walk the solution end to end; each hole is declared solved-in-principle (state how) or patched out with a stated decision.
4. **Write no-gos.** Name what this bet deliberately excludes.

**Completion criterion:** the pitch has all five ingredients, and the solution sits at fat-marker altitude — a wireframe or task list is over-shaped; a slogan is under-shaped.

### shape-check

Interactive gut check of a pitch with the user, via the AskUserQuestion tool. Question shape:

- One single-select question per axis; answers to one axis never hide inside another.
- The `(Recommended)` option is first and carries the default; picking it accepts the default.
- At most 4 questions per fire; more axes go in sequential batches, dependency order.
- `multiSelect` only for additive picks (optional sub-scopes), never for axis-with-default semantics.

The axes come from the pitch's own ingredients: appetite right-sized? which scope cuts? each unresolved rabbit hole — patch or re-shape? no-go boundaries holding?

**Completion criterion:** every answered axis is folded back into the pitch; unanswered axes are listed as open bets — none silently dropped.

### to-good-shape

Repair a badly shaped pitch. Diagnose first, one line:

- **Over-shaped** — design already done (wireframes, field lists, task tickets). Raise the altitude: redraw as a breadboard (notation in `references/breadboarding.md`), discard the pixel decisions.
- **Under-shaped** — words without a walkthrough, unbounded appetite. Force an appetite and walk one concrete path through the solution.
- **Missing ingredients** — add the absent ones; the other four constrain what the new one can say.

Then rewrite the pitch.

**Completion criterion:** the rewritten pitch passes the build-shape bar (five ingredients, fat-marker altitude); the diagnosis is stated in one line.

### feel-shape

Results-shape-check: compare a finished artifact to the shaped bet, ingredient by ingredient.

- Problem: does the result address the shaped problem?
- Appetite: bet vs actual spend.
- Solution: does the built thing follow the breadboard's places and connections (terms defined in `references/breadboarding.md`)?
- Rabbit holes: which ones bit, and what did they cost?
- No-gos: respected or crossed?

Verdict, exactly one: `shipped-the-bet | scope-crept | under-delivered | different-bet`.

**Completion criterion:** every ingredient has a matched/violated line with evidence, plus the one top-line verdict.
