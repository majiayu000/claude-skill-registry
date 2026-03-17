---
name: code-evolution
description: Evaluates whether modifications to existing code maintain or degrade design quality. Use when reviewing changes to existing code (diffs, PRs, or recently modified files) to assess whether each change looks designed-in or bolted-on. Not for scanning against a checklist of design smells (use red-flags) or assessing overall design investment (use strategic-mindset).
argument-hint: "[file, module, or PR]"
metadata:
  allowed-tools: Read, Grep
---

# Code Evolution Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file, module, or pull request. Read the target code first, then apply the checks below.

Evaluate whether code modifications maintain or degrade design quality.

## When to Apply

- Reviewing a PR that modifies existing code
- After adding a feature to an existing system
- When code has accumulated patches and feels degraded
- When deciding whether to refactor during a feature change

## Core Principles

### The "Designed This Way" Standard

> "Ideally, when you have finished with each change, the system will have the structure it would have had if you had designed it from the start with that change in mind." — John Ousterhout, _A Philosophy of Software Design_

The design of a mature system is determined more by changes made during its evolution than by any initial conception. Every modifier either continues toward the original trajectory or bends away.

#### Three-Question Test

1. If someone were designing this system from scratch knowing this requirement, what would it look like?
2. Does the modified code match that ideal, or is the change visibly patched on?
3. If not, what's the minimum restructuring to close the gap?

#### The Middle Path

When the ideal refactoring takes three months and you have two hours, the strategic question isn't "can I afford to refactor?" It's "what's the best I can do given my constraints?" That question often surfaces an approach nearly as clean as the ideal, achievable in days, that the smallest-change mindset would never find because it anchors on the current code.

### The "Smallest Possible Change" Trap

There is no neutral gear.

> "If you're not making the design better, you are probably making it worse." — John Ousterhout, _A Philosophy of Software Design_

Each minimal change typically introduces a special case, a dependency, or a conditional that doesn't belong. Once, negligible. Across hundreds of modifications over years, this is how well-designed systems become legacy nightmares.

### Repetition Audit

After a modification, check:

- Was similar code copy-pasted rather than extracted?
- Does the same logic now exist in multiple places?
- Will the next change of this type require edits in multiple locations?

> "If the same piece of code (or code that is almost the same) appears over and over again, that's a red flag that you haven't found the right abstractions." — John Ousterhout, _A Philosophy of Software Design_

#### Two Strategies

1. **Extract and call**: Works best when the method forms a deep abstraction. If the snippet is two lines but requires five parameters, extraction may add more complexity than it removes.
2. **Restructure so the code runs once**: Sometimes better because it eliminates duplication entirely.

_When not to extract_: Code that looks identical can represent two independent decisions that happen to be expressed the same way. Merging them creates artificial coupling.

### Comment Maintenance

Stale comments are worse than missing comments because they actively mislead. Once readers discover comments can't be trusted, they stop reading them entirely.

Five maintenance rules:

1. **Keep comments near the code they describe**: proximity is a maintenance mechanism

2. **Put comments in code, not commit logs**: developers navigate code spatially, not chronologically

   > "Comments belong in the code, not the commit log." — John Ousterhout, _A Philosophy of Software Design_

3. **Document each decision exactly once**: duplicated documentation drifts invisibly
4. **Check the diffs before committing**: verify documentation still matches behavior
5. **Prefer higher-level comments**: abstract comments that describe _what_ and _why_ survive code changes better than detailed _how_ comments. As Ousterhout writes, "the farther a comment is from the code it describes, the more abstract it should be"

### Technical Debt

> "Unlike financial debt, most technical debt is never fully repaid." — John Ousterhout, _A Philosophy of Software Design_

No settlement date, only ongoing interest. It accumulates not through catastrophic decisions but through hundreds of small shortcuts, each locally defensible, collectively corrosive.

### During Modifications

- Debt in the area being modified → fix it now (context is fresh, fix is cheapest)
- Debt elsewhere affecting the modification → document it, fix if feasible
- Never add to the pile. Each modification should reduce debt, not increase it

Refactoring is not a special event. It is the normal expression of strategic programming applied to existing code. Continuous small improvements, not periodic large refactors.

## Review Process

1. **Apply the "designed this way" test**: Does the modification look native or bolted-on?
2. **Check for incremental complexity**: Did the change add special cases, dependencies, parameters, or flags?
3. **Run repetition audit**: Did the change introduce or perpetuate copy-paste?
4. **Verify comment maintenance**: Are all affected comments updated?
5. **Assess debt trajectory**: Is the modification reducing or increasing technical debt?
6. **Recommend**: Specific improvements to make the change feel designed-in

Red flag signals for code evolution are cataloged in **red-flags** (Special-General Mixture, Repetition, Tactical Momentum, Non-obvious Code).
