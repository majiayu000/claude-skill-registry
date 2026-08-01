---
name: feature-dev
description: Take one new feature slice from idea to reviewed, committed code in a single guided pass — scope it into the smallest shippable slice, build it test-first with strict TDD, review and fix the diff, then commit it. Chains slice → test-driven-development → the built-in /code-review → git-commit. Not for reviewing an existing PR, upgrades, or open-ended design questions.
argument-hint: "[feature or slice to build]"
disable-model-invocation: true
---

# Feature Development

You are helping a developer take **one feature slice** from a rough idea to reviewed, committed code. This is not autonomous coding — it's a guided workflow that borrows its backbone from systematic feature development but threads four disciplines through it: **slicing** to define the work, **TDD** to build it, **code review** to harden it, and a clean **commit** to land it.

The workflow's whole reason for existing is to resist the pull toward premature code. Each phase earns the right to the next: you don't slice until you understand the feature, you don't build until the slice is sharp, you don't consider it done until the diff has been reviewed, and you don't commit until it's green. Hold that line — the value is in the sequence, not any single step.

**Scope discipline:** this workflow refines and builds exactly **one slice**. If the work is actually an epic — several independently shippable pieces — you'll surface that during framing and help the user pick the single slice to build now. Building more than one slice in a pass defeats the point; the payoff is a tight loop of shape → build → review on a small, real increment.

**Leanness discipline:** a small slice does not guarantee a small diff. Slicing controls _what_ ships; it does nothing to stop the implementation from bloating with speculative abstractions, options nothing uses yet, defensive branches no test demands, or gold-plating. Those are a separate failure mode, and this workflow fights them separately. The target is a **production-code diff under ~300 lines** (excluding comments and blank lines; test code does not count against this ceiling, though bloated tests are their own smell). Treat that number as a design constraint you carry from Phase 3 onward, not a gate you discover at the end.

Use `TodoWrite` to track the phases so the user can see where they are.

---

## Phase 1: Frame the work

**Goal:** understand what the user wants to build, and confirm it's a single slice before investing in anything else.

Initial request: `$ARGUMENTS`

If the feature is unclear, ask what they're building — the problem it solves, who it's for, what "done" looks like. Keep it short; the `slice` skill will interrogate scope properly in Phase 3, so here you only need enough to explore the codebase intelligently.

Then make an explicit call on size. Ask yourself (and the user, if it's genuinely ambiguous): **is this one slice, or an epic hiding several?** A slice is something a real user can touch and a stakeholder can see value in, shippable on its own.

- **One slice** → confirm your understanding in a sentence or two and move to Phase 2.
- **An epic** → say so plainly. Help the user name the pieces briefly, then ask which single slice to build in this pass. Do not try to build them all. If they want the full epic broken down rigorously first, that's the `slice` skill's Path B on its own — point them there and stop.

---

## Phase 2: Explore the codebase

**Goal:** ground the slice in how this codebase actually works, so the acceptance criteria are realistic and the implementation follows existing conventions instead of inventing new ones.

This matters most in a mature Rails app: the right slice and the right tests depend on where similar features live, what the testing conventions are, and which abstractions already exist. Skipping this leads to slices that ignore reality and code that fights the grain of the app.

Match the effort to the feature. For a small, well-understood change, a few targeted reads inline are enough — don't spin up subagents to rediscover something you can see in one file. For anything touching unfamiliar territory or spanning layers, launch 2–3 general-purpose subagents in parallel (via the Task tool) as codebase explorers — give each the brief in `references/code-explorer.md` plus a different angle to cover:

- Find features similar to this one and trace their implementation end to end.
- Map the architecture and conventions for the area this slice touches (models, controllers, jobs, views, wherever it lands).
- Identify the testing patterns relevant to this work — the framework (RSpec or Minitest), how tests are structured across the layers (end-to-end/system, request or controller, model/unit), and what factories or fixtures exist.

Ask each explorer to return the 5–10 files most worth reading. When they return, **read those files yourself** before proceeding — the subagents build the map, but you need the detail in context to slice and test well.

Close the phase with a short summary of the patterns and conventions that will shape the slice: where the code will live, what it should look like, what to reuse.

---

## Phase 3: Shape the slice

**Goal:** turn the framed feature into one sharp, well-defined slice with real acceptance criteria.

**Invoke the `slice` skill** (Skill tool, `slice`) and let it run the conversation. Because Phase 1 already established this is a single slice, `slice` should sharpen it into one job story (its Path A) rather than break an epic apart. Feed it what you learned in Phases 1–2 so the conversation starts warm instead of from zero.

What you need out of this phase is the deliverable `slice` produces: a job story with a clear **"ships when"** and a concrete list of **acceptance criteria** — happy path, edge cases, and error states. Those acceptance criteria are not paperwork; they become the failing tests in Phase 4. Push (or let `slice` push) until each criterion is specific and verifiable — "a user can X and sees Y" — because a vague criterion produces a vague test that proves nothing.

Do not move on until the user is satisfied the slice is genuinely the smallest thing that delivers real value. If slicing reveals the work is bigger than one slice after all, return to the Phase 1 decision: pick one slice, defer the rest.

Close the phase with a rough **size budget** for the implementation: given what Phase 2 revealed about where this code will live and what it can reuse, does the slice look buildable in under ~300 lines of production code? If it clearly can't — it spans many layers, or every acceptance criterion drags in new machinery — that is often a signal the slice is still too big, not that the budget is wrong. Interrogate it now, while re-slicing is cheap. If the size is genuinely justified by essential complexity, name that expectation here so it's a considered decision rather than a surprise in Phase 5.

---

## Phase 4: Build it test-first

**Goal:** implement the slice with strict, outside-in TDD, driven by the acceptance criteria.

**Invoke the `test-driven-development` skill** (Skill tool, `test-driven-development`) and follow it without shortcuts. Hand it the slice's acceptance criteria as the specification: each criterion is a behavior that needs a failing test before any production code exists.

The two skills fit together naturally — `slice` produced the observable behaviors, and TDD drives them outside-in: start with a high-level test for the "ships when" behavior — a system or feature test — let its failure push you down through the lower layers (request/controller, then model), and write minimal code at each layer. The acceptance criteria are your checklist; the slice is done when every one of them is covered by a test you watched fail and then pass, and the suite is green with pristine output.

Honor the Iron Law from that skill: no production code without a failing test first. If you catch yourself wanting to skip ahead "just this once," that's exactly the moment the discipline is paying off.

**Keep the implementation lean while you build.** TDD's "write the minimal code to pass the current test" is your best defense against a bloated diff — take it literally. Concretely, as you work through the criteria:

- Don't introduce an abstraction (a service object, a concern, a base class, a config option) until a _second_ caller actually needs it. One caller is not a pattern.
- Don't add error handling, branches, or parameters that no failing test demands. If it isn't driven by a criterion, it isn't in scope for this slice.
- Reuse what Phase 2 surfaced instead of building parallel machinery. The leanest diff leans on code that already exists.

**Size checkpoint before review.** When every acceptance criterion is green, measure the production diff against the ~300-line budget before moving on:

```
git diff --stat "$(git merge-base HEAD main)"...HEAD -- ':(exclude)test' ':(exclude)spec'
```

(Use whichever base branch the slice was cut from, and adjust the excludes to this app's test directories. This counts added lines including comments and blanks, so discount those by eye — you want the real production-code figure.)

If you're at or under budget, move to review. If you're over, do **not** just proceed — make an explicit, written call among three options and tell the user which one applies:

- **Accidental complexity** — over-abstraction, dead flexibility, code no criterion demanded. Simplify it now, before review. This is the common case and the whole reason for the checkpoint.
- **Essential complexity** — the slice genuinely spans enough layers that the code can't be smaller without losing behavior. Legitimate, but say _why_ in one or two sentences; an unexplained large diff is indistinguishable from a bloated one.
- **The slice was too big** — if the size traces back to scope rather than implementation, the honest fix is upstream. Return to the Phase 1/3 decision, ship the smaller piece, and defer the rest.

This is an advisory checkpoint, not a hard gate — a justified large diff is allowed to proceed. What's not allowed is drifting past 300 lines without noticing. Once the size is either under budget or a considered decision, the slice is built — move to review.

---

## Phase 5: Review the diff

**Goal:** catch the bugs, quality issues, and convention violations that TDD alone won't surface, then fix them before the slice is considered shippable.

TDD proves the slice does what the acceptance criteria demanded — it does not prove the code is simple, secure, or idiomatic. That's what this phase is for, and it runs against the **diff for this slice** (the changes since the branch point).

Run Claude Code's built-in code review over the slice and let it apply the fixes automatically:

```
/code-review high --fix
```

- The **level** sets how hard the review looks. `high` is the right default for a focused single-slice diff — drop to `medium` for a trivial change, or raise to `xhigh`/`max` for security-sensitive or subtle logic where a missed issue is expensive.
- **`--fix`** applies the fixes for confirmed findings directly instead of only reporting them, which is what we want here — the slice should come out of this phase already corrected.

`/code-review` already hunts for simplification and reuse opportunities, so it's a natural second pass on leanness after the Phase 4 checkpoint — if the diff came in near or over budget, weigh its simplification findings accordingly rather than waving them through.

The built-in review already filters to high-confidence findings and verifies them before it acts, so there's no separate confidence pass to run. `references/code-review.md` documents the standard it applies — the ≥ 80 confidence bar, the Critical vs. Important severity split, and what counts as a false positive — if you want to understand what it's weighting or need to fall back to a manual review when the command isn't available.

Because `--fix` edits code outside the red-green-refactor loop, **re-run the full suite once it finishes** — using whatever test command this app uses (the one you identified in Phase 2, e.g. `bin/rails test`, `bundle exec rspec`, or the app's Rake task) — to confirm the slice is still green and nothing regressed.

If a fix changed behavior that isn't yet covered by a test, add the missing test — failing first, per Phase 4 — so the correction is locked in and can't silently regress later. Then briefly summarize what the review changed: what it fixed, anything it flagged but deliberately left, and confirmation the suite is green.

---

## Phase 6: Summary

**Goal:** close the loop.

Mark the todos complete and give a short summary:

- **What shipped** — the slice, in one line the user could paste into a PR description.
- **Acceptance criteria** — confirm each is met and tested.
- **Key decisions** — anything notable from slicing, testing, or review.
- **Files changed** — the diff at a glance, with the production-code line count against the ~300 budget. If it ran over, restate the one-line justification from the Phase 4 checkpoint.
- **Next steps** — if this was one slice of a larger epic, name the slices still waiting.

---

## Phase 7: Commit the slice

**Goal:** land the finished, reviewed slice in version control as a clean commit.

**Invoke the `git-commit` skill** (Skill tool, `git-commit`). The whole point of this workflow is that everything in the working tree is _one coherent slice_, so `git-commit` should land it as a single atomic commit rather than splitting it — the model, its migration, the controller, the view, and the tests all tell one story. The exception is anything genuinely independent that snuck in (an unrelated cleanup, a drive-by fix from the review); let `git-commit` make that call and split those out.

Feed it the slice's "ships when" line as context so the commit message explains _why_ the slice exists, not just what changed. If the review in Phase 5 flagged a risk or a deliberate trade-off, mention it so that lands in the message too.

`git-commit` stops at creating commits — it does not push and does not open a PR. That's intentional; leave the branch ready for the user to push and open the PR themselves. Depending on install, the skill may be listed as `rails-consultant:git-commit`.

---

## Notes on the disciplines

The pieces this workflow orchestrates are each rigorous on their own; your job is to run them in sequence and keep the handoffs clean, not to water them down.

- `slice` is Socratic — it leads the user to define the work through questions. Let it. Don't pre-answer for them.
- `test-driven-development` is strict about order. Don't let the momentum of a clear slice tempt you into writing code before the test.
- The built-in `/code-review --fix` does the reviewing and fixing; your responsibility after it runs is to make sure the suite is still green and that any behavior it changed is covered by a test. A green suite is the signal the slice is actually shippable, not just that the review finished.
- `git-commit` makes the atomic-commit call itself. Because a slice is one coherent change, expect a single commit — don't pre-split the work for it, but do hand it the "ships when" context so the message explains the why.

Depending on how the plugin was installed, `slice`, `test-driven-development`, and `git-commit` may appear namespaced as `rails-consultant:slice`, `rails-consultant:test-driven-development`, and `rails-consultant:git-commit` — invoke whichever name the Skill tool lists. If any of the four skills isn't available at all, follow its `SKILL.md` directly (`~/.claude/skills/<name>/SKILL.md`, or the plugin's `skills/<name>/SKILL.md`) rather than skipping the phase — the sequence is the point.
