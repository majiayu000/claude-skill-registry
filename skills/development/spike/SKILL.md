---
name: spike
description: Implement N approaches as separate branches, then compare side-by-side. Removes "implementation effort" as a variable from the decision.
args:
  - name: -n N
    description: Number of spike branches to implement (default 4)
---

# Spike

You can't compare approaches in the abstract. Implement each one, see how they feel in real code, then decide. This removes speculation and replaces it with evidence.

## Why This Works

Design discussions stall on hypotheticals. Implementing each approach takes the guesswork out. You get exact line counts, real dependency changes, actual lint/compile errors that reveal hidden constraints, and the visceral feel of reading the code.

## On Activation

1. **Select** — Choose N approaches to implement.
2. **Prepare** — Identify the base branch and files to modify.
3. **Implement** — One branch per approach, fully working.
4. **Verify** — Each branch compiles and passes lint.
5. **Compare** — Side-by-side table of discriminating dimensions.

## Phase 1: Select

Identify exactly N approaches. Sources include `/synthesize` output, `/brainstorm` rankings, a user-specified list, or freeform description.

If the user hasn't specified which approaches, ask via `AskUserQuestion`.

For each approach, define a branch name (`spike/<descriptive-name>`), which option(s) it implements, and a one-line summary. Present the plan before implementing.

Some brainstorm options are **complementary** — combine them into a single branch when they strengthen each other rather than competing.

## Phase 2: Prepare

1. **Read all files** that will be modified across branches. Load them once — they're the same starting point for every branch.
2. **Note the base branch** — all spike branches fork from here.
3. **Identify the verification command** (`make format lint`, `cargo clippy`, `npm run lint`, etc.). Ask if unclear.

## Phase 3: Implement

Work through branches **sequentially** (they modify the same files). For each: check out the base branch, create `spike/<name>`, implement fully.

**Fully** means: all code changes, updated imports and call sites, updated doc comments. No stubs, no TODOs. The implementation should be complete enough to merge if the team chose this approach.

**Handle errors as they come.** Lint failures and compile errors are expected — they reveal hidden constraints. Fix them and note them for the comparison.

**Equal effort across all branches.** If you spend extra time making one branch elegant, you're biasing the comparison.

## Phase 4: Verify

After implementing each branch, run the verification command. Fix failures (the fix is data), re-run until clean, then commit. Every branch must compile and pass lint before moving to the next.

## Phase 5: Compare

Present a side-by-side comparison table. Choose dimensions that **discriminate** — if all branches score the same on a dimension, drop it. The right dimensions come from the problem domain, not a generic checklist.

**Don't pick a winner.** The comparison table is the deliverable. The user has the full picture now. Ask:

> "What do you want to do with these?"

## Anti-patterns

- **Stubs instead of implementations** — "TODO: implement this" is not a spike. The point is to feel the real code.
- **Skipping verification** — A branch that doesn't compile can't be compared fairly.
- **Generic comparison dimensions** — "Complexity: medium" is useless. Use specific, measurable dimensions.
- **Picking the winner** — Let the human decide. You removed the implementation effort barrier; now let them apply judgment.
- **Forgetting to return to base** — Each branch forks from the same base. Always check out the base between branches.

## Defaults

- N = 4 if `-n` not specified
- Branch prefix: `spike/`
- If N > 6, warn that implementation time may be excessive, but comply

---

The user has approaches to compare. Implement N spike branches. Start with Phase 1: Select the approaches.
