---
name: clean-code
description: Use when writing or reviewing functions, classes, naming, or non-trivial logic (≥3 lines)
---

# Writing Clean Code

## Overview

**Code is read far more often than it is written, so optimize the artifact for the next reader.** This skill is a small set of decisions to apply when you write a new function, name a new entity, or touch a non-trivial block of logic. Each decision pairs with a check a reviewer (human or agent) could apply by reading the diff.

## When to invoke

Invoke when you're about to:

- Add a new function, method, class, struct, or module
- Name a new entity that other code will reference (variable, function, type, file)
- Modify ≥3 lines of non-trivial logic — branching, loops, conditional dispatch, or anything that reads as "behavior" rather than "wiring"
- Add or replace a comment block of more than one line
- Copy-paste a block of logic from elsewhere in the codebase
- Review code for readability, naming, duplication, or structural quality

If you're unsure whether the change is non-trivial, ask: *would a reviewer pause on this hunk to think about it?* If yes, invoke.

### Non-triggers — do NOT invoke for

- Typo fixes or one-line bug fixes where the change is obvious
- Config edits — JSON, YAML, TOML, dotfiles, lock files, env files
- Test code (use `testing-discipline` instead)
- Refactoring existing code (use `before-you-refactor` instead)
- Mechanical edits — running a formatter, sorting imports, renaming a single local variable in one function
- Generated code

## The clean-code decisions

Each decision pairs with a **check** — a property a reviewer can verify by reading the diff.

1. **Reach simplicity by removing, not adding.** (KISS) *(Homer, 97/75.)* The reflex when code misbehaves is to add another variable, branch, or comment. Try the opposite — delete a line and see what breaks. Bad code that is close to working is worth saving; bad code that is far from working should be discarded and retyped from memory.
   *Check:* you tried deleting at least one line you initially wrote on this hunk, and the code is better for what survived.

2. **Reason about each block in short sections.** *(Kimchi, 97/15.)* Write code in chunks — a single line up to under ten — that you could defend to a sceptical peer. The endpoints of each section should be describable as state properties (a generalized pre/postcondition or invariant). When you intend to reason about the code, the structure improves on its own: smaller scopes, fewer mutable globals, narrower interfaces, getters that don't leak internal state.
   *Check:* you can describe, in one sentence, what state holds at the start and end of each block of ten or fewer lines.

3. **Find examples in domain terms before writing the function.** *(Braithwaite, 97/94.)* A function with an `int` parameter has billions of input cases; a function with a `LibertyCount = {1,2,3,4}` parameter has four. Pick the types that make the function checkable by example, then write it.
   *Check:* every parameter that could be a domain type is one (or there's a named reason it's not — measured perf, language limitation, deferred to a tracked issue).

4. **One reason to change per unit.** *(Martin, 97/76.)* The Single Responsibility Principle (SRP): a function, class, or module should have one reason to change. An `Employee` class with `calculatePay`, `reportHours`, and `save` has three reasons to change and three sets of dependents who suffer for each. Split along axes of change, not axes of "things that share a noun." See `before-you-refactor` for when to *trigger* a split on existing code.
   *Check:* the responsibility of each function/class/module fits in one sentence with no "and also."

5. **Treat layout as a tool for the reader, not for the parser.** *(Freeman, 97/13.)* Standardize accidental complexity (formatter handles the basics) so domain content stands out. Use line breaks to express intention. Compact, scannable code beats sparse ceremonial code on every metric the reader cares about.
   *Check:* removing any blank line in the hunk would either obscure intent or prove it wasn't doing work.

6. **Names match the domain; no name relies on local context.** *(Sommerlad, 97/62 — distilled.)* Context evaporates the moment the reader is somewhere else in the file. Names carry their meaning with them.
   *Check:* every new name reads correctly when the reviewer encounters it for the first time, with the surrounding lines hidden.

7. **Comment only what the code cannot say.** *(Henney, 97/17.)* A comment that restates what the code does adds nothing. A comment that contradicts the code is worse than nothing — wrong comments survive forever because no compiler catches them. The legitimate space is *why this approach, not what it does*.
   *Check:* every comment in the hunk explains *why*, not *what*; comments that describe the code itself are deleted, and the underlying name or extraction is improved instead.

8. **Each piece of knowledge has one authoritative representation.** *(Smith, 97/30; performance-angle credit Pepperdine, 97/91.)* DRY applies to data, logic, and process. Copy-paste duplication is the easy case to spot; the harder case is parallel implementations of the same business rule that drift apart over time. (Bonus from 97/91: a hot path concentrated in one place shows up clearly in a profile; spread across copies, each looks like noise.) Occasional duplication for a measured performance reason is fine; speculative duplication is not.
   *Check:* no business rule is implemented in two places without a named reason; if it is, the reason is recorded inline or in the commit message.

### Long-term mindset vs YAGNI — the tension

"Write for long-term support" and "remove anything you don't need" sound contradictory and aren't. **Long-term thinking is about clarity, not predictive feature engineering.** Invest in good names, small functions, honest comments, removed dead code, tests that pin behavior. Don't invest in speculative parameters, configuration knobs, abstraction layers, or "extension points" for hypothetical future maintainers — that's 97/75/97/39 territory. The test: would I want to *read* this code in two years (long-term thinking) versus would I want to *have already written* this extra layer (speculation; cut it).

## Red Flags

| Thought | Reality |
|---|---|
| "I'll add another flag/variable to make it work." | The reflex to add is what produced the mess. Try removing instead — delete a line and see what breaks. (97/75) |
| "It's a long function, but splitting it would be artificial." | A function with multiple reasons to change is not one function. Split along the axes of change, not "looks tidy." (97/76) |
| "I'll comment what the code is doing so the reader follows along." | Restating the code in prose adds noise. Rename, extract, or simplify until the code says what the comment was going to. (97/17) |
| "I'll leave the old block commented out in case we need it." | Commented-out code goes stale immediately and isn't executable. Version control remembers; the file shouldn't. (97/17, 97/62) |
| "It's only duplicated twice — extracting feels premature." | Two copies become five. The cost of extracting now is small; finding all copies of a buggy rule later is not. (97/30, 97/91) |
| "I'll use `int`/`string` for now — we can wrap it later." | The native type opens billions of input cases that no test will ever cover. A domain type collapses the function to something checkable. (97/94) |
| "The variable name is short — context makes it obvious." | Context evaporates the moment the reader is somewhere else. Names carry their meaning with them. (97/62) |
| "Every function on this class belongs together — they all touch `Order`." | Sharing a noun isn't a single responsibility. Ask what changes for what reason; if the answers differ, split. (97/76) |
| "I'll add this configuration knob in case someone wants to override it." | Speculative knobs are how simple code becomes complex. Default to the simplest thing that works; add the knob when a real caller arrives. (97/75) |
| "I'll add this hook now in case we need it later." | YAGNI: speculation predicts the future poorly, and the unused hook adds maintenance cost forever. Add it when the second caller asks. (97/39) |

## What "done" looks like

- [ ] Each function or method has one reason to change, expressible in one sentence with no "and also."
- [ ] No new name in the diff requires the surrounding lines to be understood — names carry their meaning standalone.
- [ ] No dead code, no commented-out blocks, no speculative parameters or configuration knobs.
- [ ] Every comment in the diff says something the code cannot say (every comment that restates the code has been removed and the code improved instead).
- [ ] No primitive parameter where a domain-specific type would shrink the function's input space — or there's a named reason recorded.
- [ ] No business rule is implemented in two places without a recorded reason.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/13 | Code Layout Matters | Steve Freeman |
| 97/15 | Coding with Reason | Yechiel Kimchi |
| 97/17 | Comment Only What the Code Cannot Say | Kevlin Henney |
| 97/30 | Don't Repeat Yourself | Steve Smith |
| 97/75 | Simplicity Comes from Reduction | Paul W. Homer |
| 97/76 | The Single Responsibility Principle | Robert C. Martin |
| 97/91 | WET Dilutes Performance Bottlenecks | Kirk Pepperdine (folded into 97/30 here) |
| 97/94 | Write Small Functions Using Examples | Keith Braithwaite |

See `principles.md` for the long-form distillations and source links.
