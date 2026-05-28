---
name: review-structure
description: Repo-wide structural-maintainability review — code-judo restructurings, 1k-line file guard, anti-spaghetti branching, canonical-layer enforcement, anti-magic abstractions, explicit type/boundary contracts.
disable-model-invocation: true
---

# Structural-Maintainability Review

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Above all, this skill should push the reviewer to be **ambitious** about code structure. Do not merely identify local cleanup opportunities. Actively search for "code judo" moves: restructurings that preserve behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant.

The structural lens is **repo-wide**: read any file in the codebase as needed (Read/Grep/Bash) to judge whether canonical helpers already exist, whether file-size budgets are honored, and whether the change makes the codebase easier or harder to live with.

## Hard gates (sequence)

Advance only when each **pass condition** is objectively satisfied (artifact path, tool output, or labeled capture — not "I checked it mentally"):

| Gate | Pass condition |
|------|----------------|
| **G1 — Changed-file list** | `git diff --name-only` (or equivalent) returns a non-empty list *or* you exit with an explicit "no changed files" message; the list is recorded before any review step begins. |
| **G2 — Full file reads** | Every file in scope has been opened with `Read`; for each file you record the path and line count (e.g. `src/foo.ts — 342 lines`). Do **not** proceed to findings until all reads are logged. |
| **G3 — Canonical-helper and 1k-line claims verified** | Any finding that asserts "no canonical helper exists" must cite a `Grep` artifact showing the search pattern and result. Any finding that asserts a file exceeds 1 000 lines must cite a `wc -l` or `Read` line-count artifact. Findings lacking these artifacts are **blocked** from the report. |

## Core Prompt

Start from this baseline:

> Perform a deep structural review of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce spaghetti code, improve succinctness and legibility.
> Be ambitious — if there is a clear path to improving the implementation that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Non-Negotiable Additional Standards

Apply the baseline prompt above, plus these explicit review rules:

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for opportunities to reframe the change so that whole branches, helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code feel inevitable in hindsight.
   - Assume there is often a "code judo" move available: a re-organization that uses the existing architecture more effectively and makes the change dramatically simpler and more elegant.
   - If you see a path to delete complexity rather than rearrange it, push hard for that path.

1. **Do not let a PR push a file from under 1k lines to over 1k lines without a very strong reason.**
   - Treat this as a strong code-quality smell by default.
   - Prefer extracting helpers, subcomponents, modules, or local abstractions instead of letting a file sprawl past 1000 lines.
   - If the diff crosses that threshold, explicitly ask whether the code should be decomposed first.
   - Only waive this if there is a compelling structural reason and the resulting file is still clearly organized.

2. **Do not allow random spaghetti growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows.
   - If a change adds "weird if statements in random places", treat that as a design problem, not a stylistic nit.
   - Prefer pushing the logic into a dedicated abstraction, helper, state machine, policy object, or separate module instead of tangling an existing path.
   - Call out changes that make the surrounding code harder to reason about, even if they technically work.

3. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while the structure becomes meaningfully cleaner, push for the cleaner version.
   - Do not rubber-stamp "it works" implementations that leave the codebase messier.
   - Strongly prefer simplifications that remove moving pieces altogether over refactors that merely spread the same complexity around.

4. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a code-quality problem.
   - Be skeptical of generic mechanisms that hide simple data-shape assumptions.
   - Flag thin abstractions, identity wrappers, or pass-through helpers that add indirection without buying clarity.

5. **Push hard on type and boundary cleanliness when they affect maintainability.**
   - Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer type boundary could exist.
   - Prefer explicit typed models or shared contracts over loosely-shaped ad-hoc objects.
   - If a branch relies on silent fallback to paper over an unclear invariant, ask whether the boundary should be made explicit instead.

6. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths or implementation details leaking through APIs.
   - Prefer existing canonical utilities/helpers over bespoke one-offs.
   - Push code toward the right package, service, or module instead of normalizing architectural drift.

7. **Treat unnecessary sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.**
   - If independent work is serialized for no good reason, ask whether the flow should run in parallel instead.
   - If related updates can leave state half-applied, push for a more atomic structure.
   - Do not over-index on micro-optimizations, but do flag avoidable orchestration complexity that makes the implementation more brittle.

## Primary Review Questions

For every meaningful change, ask:

- Is there a "code judo" move that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, or helper layers are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Did a previously cohesive module become more coupled, more stateful, or harder to scan?
- Is this logic living in the right file and layer?
- Did this change enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or missing helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is this abstraction actually earning its keep, or is it just a wrapper?
- Did the diff introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Is this logic living in the canonical layer, or did the diff leak details across a boundary?
- Is this orchestration more sequential or less atomic than it needs to be?

## What to Flag Aggressively

Apply rules 0–7 above, and escalate especially when you see:

- Refactors that move code around but fail to reduce the number of concepts a reader must hold in their head.
- Copy-pasted logic instead of extracted helpers.
- Narrow edge-case handling implemented in the middle of an already busy function.
- Refactors that technically pass tests but make the code less modular or less readable.
- "Temporary" branching that is likely to become permanent debt.

## Preferred Remedies

When you identify a code-quality problem, prefer suggestions like:

- Delete a whole layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear instead of getting centralized.
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a helper or pure function.
- Split a large file into smaller focused modules.
- Move feature-specific logic behind a dedicated abstraction.
- Replace condition chains with a typed model or explicit dispatcher.
- Separate orchestration from business logic.
- Collapse duplicate branches into a single clearer flow.
- Delete wrappers that do not meaningfully clarify the API.
- Reuse the existing canonical helper instead of introducing a near-duplicate.
- Make type boundaries more explicit so the control flow gets simpler.
- Move the logic to the package/module/layer that already owns the concept.
- Parallelize independent work when that also simplifies the orchestration.
- Restructure related updates into a more atomic flow when partial state would be harder to reason about.

Do not be satisfied with "maybe rename this" feedback when the real issue is structural.
Do not be satisfied with a merely cleaner version of the same messy idea if there is a plausible path to a much simpler idea.

## Review Tone

Be direct, serious, and demanding about quality.
Do not be rude, but do not soften major maintainability issues into mild suggestions.
If the code is making the codebase messier, say so clearly.
If the implementation missed an opportunity for a dramatic simplification, say that clearly too.

## Output Expectations

Prioritize findings in this order:

1. Structural code-quality regressions
2. Missed opportunities for dramatic simplification / code-judo restructuring
3. Spaghetti / branching complexity increases
4. Boundary / abstraction / type-contract problems that make the code harder to reason about
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

Do not flood the review with low-value nits if there are larger structural issues.
Prefer a smaller number of high-conviction comments over a long list of cosmetic notes.

## Approval Bar

Do not approve merely because behavior seems correct. The bar is: no violation of rules 0–7 above, and no clear structural regression.

Treat as presumptive blockers unless the author can justify them clearly:

- the PR preserves incidental complexity when a plausible code-judo move would delete it (rule 0)
- the PR pushes a file from below 1000 lines to above 1000 lines (rule 1)
- the PR adds ad-hoc branching that makes an existing flow more tangled (rule 2)
- the PR adds an unnecessary abstraction, wrapper, or cast-heavy contract (rules 4–5)
- the PR duplicates an existing helper or puts logic in the wrong layer (rule 6)

If those conditions are not met, leave explicit, actionable feedback and push for a cleaner decomposition.

## Step 1: Identify Changed Files

Capture the command output (or equivalent) as your authoritative changed-file set before reviewing. The structural lens applies to changes in any language — do not filter by extension.

```bash
BASE=$(for ref in main origin/main master origin/master; do
         git rev-parse --verify "$ref" >/dev/null 2>&1 && { echo "$ref"; break; }
       done)
if [ -z "$BASE" ]; then
  echo "error: no main/master ref found (checked main, origin/main, master, origin/master)." >&2
  exit 1
fi
MERGE_BASE=$(git merge-base HEAD "$BASE") || {
  echo "error: git merge-base HEAD $BASE failed." >&2
  exit 1
}
git diff --name-only "$MERGE_BASE..HEAD"
```

If the list is empty, state that explicitly and do not invent structural findings.

## Output Format

```markdown
## Review Summary

[1-2 sentence overview of structural findings]

## Issues

### Critical (Blocking)

1. [FILE:LINE] ISSUE_TITLE
   - Issue: Description of the structural problem
   - Why: Why this matters (maintainability, spaghetti growth, missed code-judo move)
   - Fix: Specific recommended restructuring

### Major (Should Fix)

2. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Minor (Nice to Have)

N. [FILE:LINE] ISSUE_TITLE
   - Issue: ...
   - Why: ...
   - Fix: ...

### Informational (For Awareness)

N. [FILE:LINE] SUGGESTION_TITLE
   - Suggestion: ...
   - Rationale: ...

## Good Patterns

- [FILE:LINE] Pattern description (preserve this)

## Verdict

Ready: Yes | No | With fixes 1-N (Critical/Major only; Minor items are acceptable)
Rationale: [1-2 sentences]
```

## Rules

- Read repo-wide (Read/Grep/Bash) before claiming a canonical helper does not exist
- Number every issue sequentially (1, 2, 3...)
- Include FILE:LINE for each issue
- Separate Issue/Why/Fix clearly
- Categorize by actual severity
- Prefer fewer high-conviction structural findings over many cosmetic notes
- The Verdict ignores Minor and Informational items — only Critical and Major block approval
