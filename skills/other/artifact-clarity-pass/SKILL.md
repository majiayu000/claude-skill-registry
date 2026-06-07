---
name: artifact-clarity-pass
description: |-
  Use when removing generic filler from code, docs, or handoffs while preserving every load-bearing fact.
  Triggers:
skill_api_version: 1
hexagonal_role: domain
practices:
- code-complete
- refactoring
context_rel:
- kind: shared-kernel
  with: standards
metadata:
  tier: judgment
  stability: stable
  dependencies: []
output_contract: tightened text/code + a slop-removal report (cuts + rationale)
context:
  window: inherit
user-invocable: false
---

# artifact-clarity-pass — cut AI slop down to real signal

Take verbose, generic, hedged, over-explained output and tighten it to what actually
carries meaning. The job is subtraction with judgment: remove the filler, keep every
load-bearing word, fact, edge case, and caveat.

## ⚠️ Critical Constraints

- **Never cut meaning to cut words.** Slop is text that carries no information. A real
  caveat, edge case, or constraint is signal — keep it even if it's long.
  **Why:** the failure mode of de-slopification is deleting a load-bearing "but only if X"
  along with the fluff around it. Removing words is easy; knowing which words mattered is
  the whole skill.
  - WRONG: cut "Note that this fails silently if the file is missing" (lost a real edge case)
  - CORRECT: cut "It's worth noting that, generally speaking, in most cases" (pure filler)

- **Preserve the author's voice and intent, not just the facts.** Tightening is not
  rewriting in your own register. **Why:** a "de-slopified" doc that now sounds like a
  different (still-generic) AI is just re-slopped. Keep their terms, structure, and point —
  remove only the padding around them.

- **Code comments: cut the ones that restate the code; keep the ones that explain *why*.**
  **Why:** `// increment i` is slop; `// off-by-one: API returns 1-indexed pages` is signal.
  - WRONG: delete `// retry on 429 — provider rate-limits bursts above 10/s`
  - CORRECT: delete `// loop over the items` above `for item in items:`

- **Show the cut, don't just make it.** Report what was removed and why so the human can
  veto. **Why:** subtraction feels irreversible; the author must be able to restore a cut
  you misjudged.

## Why This Exists

LLM output trends toward a recognizable texture: hedged, padded, structurally symmetric,
front-loaded with throat-clearing, comment-stuffed, and generic. It reads "fine" and says
little. Left in, it inflates token cost, buries the real point, and signals "an AI wrote
this and nobody read it." Humans rarely cut their own drafts hard enough; an explicit pass
with a checklist of known slop patterns removes far more than ad-hoc editing — without the
over-correction of deleting substance.

## Quick Start

1. Read the target (code or prose) in full first. Identify the **core claim / behavior** —
   what would be lost if this disappeared.
2. Run the slop taxonomy below as a checklist. Mark each candidate cut.
3. For each cut, apply the **keep-test**: *does removing this change what a reader can now
   do or know?* If yes, it's signal — keep. If no, cut.
4. Produce the tightened version + the slop-removal report (`## Output Specification`).

## The Slop Taxonomy (detect these)

### Prose slop
- **Throat-clearing openers:** "It's important to note that", "It's worth mentioning",
  "In today's fast-paced world", "When it comes to X". Delete; start at the claim.
- **Hedge stacking:** "may potentially", "could possibly", "generally tends to often".
  Collapse to one hedge or none. Keep a hedge only where the uncertainty is real and load-bearing.
- **Filler intensifiers:** "very", "really", "quite", "truly", "actually", "basically",
  "simply", "just". Delete unless the word changes the meaning.
- **Restating the prompt / obvious framing:** "As you requested, here is…", "This document
  will cover…". Delete; the content is self-evidently the answer.
- **Symmetric padding:** forced "Firstly… Secondly… In conclusion" scaffolds and a summary
  that repeats the body verbatim. Keep structure only where it aids navigation; cut the
  recap that adds nothing.
- **Generic value-claims:** "this is a powerful tool that can help you", "leverage the full
  potential". Replace with the specific capability or delete.
- **Over-explanation of the obvious:** explaining a well-known term to an audience that
  already knows it. Cut to the level the actual reader needs.

### Code slop
- **Comments that restate code:** `// set x to 5`, `# return the result`. Delete.
- **Redundant docstrings** that re-spell the signature with no contract, units, or failure
  modes. Delete or replace with the real contract.
- **Defensive boilerplate that can't trigger:** null checks on type-guaranteed values,
  try/except around code that doesn't throw. Delete (after verifying it truly can't fire).
- **Ceremony:** needless intermediate variables, no-logic getters/setters, single-call
  wrapper functions that add a hop and no clarity. Inline.
- **Dead scaffolding:** leftover TODO/placeholder comments, commented-out code, example
  blocks that duplicate real usage. Delete.

> **The hard cases (escalate to the keep-test, don't auto-cut):** a comment that looks
> redundant but encodes a *why*; a hedge that's actually a real caveat; a "verbose"
> explanation aimed at a genuinely novice reader; defensive code guarding a real-world
> input. When unsure, keep it and flag it in the report rather than cut.

## Methodology

**Phase 1 — Map the signal.** Read fully; note the core claim/behavior and every real
caveat, edge case, constraint, and "why". These are protected.
→ *Checkpoint:* you can state in one sentence what this text/code does. If not, re-read
before cutting.

**Phase 2 — Mark candidates.** Walk the taxonomy. Mark every slop candidate without yet
deleting. Marking is cheap; mis-deleting is expensive.

**Phase 3 — Apply the keep-test to each candidate.** Cut only what fails it (removing it
changes nothing a reader can do or know). Borderline → keep + flag.
→ *Checkpoint:* re-read the Phase-1 protected items; confirm none were swept up.

**Phase 4 — Tighten what remains.** Merge sentences that say one thing in three. Replace
generic phrasing with the specific. Do not introduce new claims or change behavior.

**Phase 5 — Emit.** Produce the tightened artifact + the report. Diff-check: meaning,
behavior, and voice intact; only padding gone.

## Output Specification

Two outputs:
1. **The tightened text/code**, edited in place (or returned inline if asked).
2. **A slop-removal report** (inline, or `artifact-clarity-pass-report.md` if a file is requested):
   ```
   ## De-slop report
   - removed: <category> — "<excerpt>" (reason: pure filler / restates code / dead)
   - kept (flagged): "<excerpt>" — looked like slop but is a real caveat
   Net: <N> cuts, ~<M> words/lines removed. Meaning & behavior unchanged.
   ```

## Quality Rubric

- **Zero meaning loss:** every fact, edge case, caveat, and behavior in the original is
  present in the output (verify by diffing the Phase-1 protected list against the result).
- **Real reduction:** measurable cut in word/line count, with each cut traceable to a slop
  category in the report (not vibes).
- **Voice preserved:** the output reads like a tightened version of the *same* author, not a
  new generic rewrite (spot-check terms and structure against the source).
- **Code unchanged in behavior:** if code was touched, it still compiles/passes its tests;
  only comments, dead branches, and ceremony were removed.

## Examples

**Prose — before:**
> It's worth noting that, generally speaking, this function is a really powerful and useful
> tool that can potentially help you to validate user input in most cases.

**After:**
> Validates user input. Returns false on empty or malformed values.

*(Cut throat-clearing + hedges + generic value-claim; surfaced the one specific fact — its
contract — that the original buried.)*

**Code — before:**
```python
# This function adds two numbers together and returns the result
def add(a, b):
    # store the sum in a variable
    result = a + b
    return result  # return it
```
**After:**
```python
def add(a, b):
    return a + b
```

**Keep-test save — before:**
```python
total = total + 1  # API pages are 1-indexed, not 0
```
**After:** unchanged. The comment explains a *why* (a real off-by-one trap), not the code.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Output now means less than the original | Cut a load-bearing caveat/edge case | Re-run Phase 1; restore protected items; re-apply keep-test |
| Output sounds like a different author | Rewrote instead of subtracting | Revert to source; cut padding only, keep their terms/structure |
| Code broke after the pass | Deleted a guard that *could* trigger | Restore the guard; only cut defensive code proven unreachable |
| "Nothing to cut" on obviously bloated text | Treated padding as content | Apply the keep-test aggressively: padding fails it by definition |
| Over-cut a beginner doc | Ignored the real audience | Set cut depth to the actual reader's level, not an expert's |

## See Also

- `standards` — the shared kernel for the code/prose quality conventions this skill enforces.
- `bug-hunt` — when tightening reveals a logic problem under the slop, not just verbosity.
