---
name: before-you-refactor
description: Use when considering, evaluating, or performing a refactor, restructure, cross-file rename, or cleanup
---

# Before You Refactor

## Overview

**Stop. Read the code that already exists. Understand the tests that protect it. Take small steps. Keep the tests green.** This is a **rigid** skill. Run the checklist; don't skip steps. When assessing code (not actively refactoring), steps 1–2 and 6 are the assessment; report findings without editing.

## When to invoke

Invoke when you're about to:

- Refactor existing code (extract function, inline, rename across multiple files, restructure a module)
- "Clean up" code you didn't write
- Rewrite a function or module because the existing one feels ugly, outdated, or wrong
- Replace an existing implementation with a "better" one
- Restructure tests, fixtures, or shared helpers used in more than one place
- Assess whether existing code needs refactoring (reading for smells, coupling, complexity)
- Review a refactoring proposal or PR that restructures code

If you're touching ≥3 lines of existing non-trivial logic to change its **shape** (not its behavior), invoke this skill.

### Non-triggers — do NOT invoke for

- Fixing a one-line bug where the change is obvious and the test exists
- Adding a brand-new function in a brand-new file (use `clean-code` instead)
- Renaming a single local variable inside one function
- Fixing a typo in a comment, string, or doc
- Formatting-only changes (whitespace, import order) handled by a formatter
- Editing config or data files where there's no logic to refactor

If you're not sure whether a change counts as a refactor, **invoke anyway** — the checklist is cheap, the consequence of skipping it is not.

## The pre-refactor checklist

Run every step in order. Do not start editing until step 5 is satisfied.

1. **Read the existing code.** Read it through once, then again. Assume it encodes decisions, bug fixes, and edge-case handling you don't yet understand. *(Attapattu, 97/6.)*
2. **Find the tests that already cover it.** List them. Run them. Confirm they pass on `main` before you change anything. If there are no tests, **stop and add a characterization test that pins down current behavior** before touching the code. *(Attapattu, 97/6 — "Ensure existing tests pass after each iteration.")*
3. **State the goal in one sentence.** "I am restructuring X so that Y." If you can't write that sentence, you don't have a refactor — you have a wish. Stop. Talk to the user.
4. **Check the goal isn't ego or fashion.** Are you refactoring because the code is genuinely blocking work, or because the style offends you, or because there's a newer framework? *Personal preference, ego, and "new tech is shiny" are not valid reasons.* *(Attapattu, 97/6.)* If the answer is fashion, stop and propose the change to the user explicitly with cost and benefit; do not silently rewrite.
5. **Plan the smallest first step.** Refactor in **many small commits, not one massive change.** Each step must keep the tests green. If your plan starts with "first I'll rip out X and then over the next hour I'll …", you're doing it wrong — restart with a smaller first step. *(Attapattu, 97/6; Lewis, 97/24.)*
6. **Identify coupling and complexity hotspots before you cut.** Skim for high fan-in / fan-out classes, long methods, deep inheritance, and hidden globals — these are the tangled spots that turn a small refactor into a big one. Note them; estimate accordingly; tell the user if the cost is now larger than the original ask. *(Pepperdine, 97/74.)*
7. **Confirm you have access to break it safely.** Are you on a branch? Can you commit incrementally? Can you revert? You should never refactor directly on a shared branch or in production. *(Evans, 97/31 — generalized: don't touch what you can't safely revert.)*

## Red Flags

These thoughts mean STOP — restart the checklist:

| Thought | Reality |
|---|---|
| "I'll just rewrite this from scratch — it'll be faster." | Throwing away tested, battle-hardened code throws away every bug fix and edge case it absorbed. The rewrite will rediscover those bugs the slow way. (97/6) |
| "There are no tests, but the change is obvious." | "Obvious" is how production breakages are born. Pin behavior with a characterization test first, then refactor. (97/6) |
| "I'll do it all in one big PR — easier to review." | Big PRs hide bugs and frustrate reviewers. Many small commits keep tests green and changes reviewable. (97/6, 97/24) |
| "The old code is ugly and uses outdated patterns — I should modernize it." | Style is not a refactor goal. New framework / new language / personal preference are not valid reasons. State the actual user-visible benefit or stop. (97/6) |
| "It's just a small cleanup, no need for a checklist." | The small cleanups are exactly where the worst tangles hide. Run the checklist. (97/74) |
| "I'll fix everything I see while I'm in there." | Boy Scout rule says *a little better*, not *perfect*. Bounded improvement only. Write the rest down for later. (97/8) |
| "I can patch it directly on the staging/production server, just this once." | No. Refactors flow through your normal commit → test → review → deploy path. "Just this once" is how outages happen. (97/31) |
| "The tests are failing but it's just flaky — I'll keep going." | Failing tests during a refactor mean the refactor changed behavior. Stop, investigate, fix or revert. Don't push through. (97/6) |
| "Estimating is too hard — I'll figure it out as I go." | Open-ended refactors balloon. Identify the coupling hotspots up front and re-estimate. If it's now bigger than the ask, escalate. (97/74) |
| "I'll just rename some variables — the function isn't *that* long." | If the function scrolls, renaming alone won't help. Extract helpers whose names explain the *why*; the body shrinks to a sequence of named steps. (`Fowler/LongMethod`) |
| "The function does X *and also* Y, but they're related." | If you needed "and also" to describe the unit, it has more than one reason to change — the SRP refactoring trigger. State the unit's responsibility in one sentence; if you can't without "and also," split. See `clean-code` decision 4 for the discipline of writing the result. (97/76) |
| "The same change keeps forcing me to edit the same eight files." | Shotgun surgery: the behavior is conceptually one thing, physically scattered. Move related fields and methods together until the next instance of the change is one file. (`Fowler/ShotgunSurgery`) |
| "This function already takes seven primitives — I'll just add an eighth." | Data clump. The fields are a missing type. Extract a class / dataclass / parameter object before adding the eighth. (`Fowler/DataClumps`) |
| "Everything lives in one file — it's easier to find when it's all together." | Co-location by import convenience is not a single responsibility. If the pieces change for different reasons, split the module along the axes of change. (97/76) |

## What "done" looks like

You are done when **all** of the following are true:

- [ ] The goal sentence from checklist step 3 is satisfied.
- [ ] All tests that passed before the refactor still pass.
- [ ] Any new behavior or new edge case has a new test (write it under TDD per `superpowers/test-driven-development`).
- [ ] No file you touched is left in a half-refactored state — no dead code, no commented-out blocks, no `TODO: finish this`.
- [ ] Each commit on the branch keeps the tests green (you can revert any single commit and the project still builds).
- [ ] If you found tangled spots outside your scope, they are written down (issue, todo, note to the user) — not silently expanded into the PR.
- [ ] You can describe the change to the user in two sentences without saying "and also."

If any box is unchecked, you are not done. Either finish, or revert and re-plan.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/6 | Before You Refactor | Rajith Attapattu |
| 97/8 | The Boy Scout Rule | Robert C. Martin |
| 97/24 | Don't Be Afraid to Break Things | Mike Lewis |
| 97/31 | Don't Touch That Code! | Cal Evans |
| 97/74 | The Road to Performance Is Littered with Dirty Code Bombs | Kirk Pepperdine |
| 97/76 | The Single Responsibility Principle / SRP (refactoring trigger) | Robert C. Martin |
| `Fowler/LongMethod` | Long Method → Extract Function | Martin Fowler |
| `Fowler/FeatureEnvy` | Feature Envy → Move Method | Martin Fowler |
| `Fowler/ShotgunSurgery` | Shotgun Surgery → Move Field / Inline Class | Martin Fowler |
| `Fowler/DataClumps` | Data Clumps → Extract Class / Introduce Parameter Object | Martin Fowler |

See `principles.md` for the long-form distillations, citations, and source links.
