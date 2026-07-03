---
name: verification-before-completion
description: Requires fresh, actually-run evidence before any claim that a task is complete. Use when about to tell the user a task, feature, or fix is done, complete, finished, working, or ready, or about to report a DONE or passing status.
---

# Verification Before Completion

## Overview

A completion claim is a claim about reality, not a description of effort spent. Saying "this works," "tests pass," "the fix is done," or "it's ready" asserts something true about the current state of the code — it is not a report that time was spent trying to make it true. That assertion carries the same evidentiary bar as any other factual claim: something was actually run, its result was actually read, and the result actually supports the sentence being said out loud.

Writing careful code, reasoning through it, and believing it correct are all real activities, but none of them is the thing being claimed. Only running the check that exercises the claim, and reading what it reports, closes the gap between effort and fact.

## When to Use

Apply this before any sentence to the user that asserts a present-tense state of the work rather than describing an action taken:

- "This works" / "it's fixed" / "the bug is gone"
- "Tests pass" / "the suite is green" / "everything passes"
- "It builds" / "it compiles cleanly"
- "The feature is done" / "ready to ship" / "good to merge"
- Any status reported as DONE, PASSING, or COMPLETE

**When NOT to use:**

- Describing an action taken, not asserting its correctness — "I added a null check to the parser" is a description; "the parser is now correct" is a claim, and only the second needs this rule
- A mid-task status update that makes no completion claim ("still in progress on the retry logic")
- A change with genuinely no checkable surface — pure prose edits, comment wording, a rename with no attached behavior — where the honest move is naming that plainly rather than inventing a check that does not exist

## The Procedure

Before saying a task, feature, or fix is done, complete, finished, working, or ready, or reporting a DONE or passing status, work through these in order.

### Step 1: Name the proving action, explicitly

Before claiming anything, identify what would actually prove it: a test suite, a build, a lint pass, running the changed code path with realistic input, re-reading an edited file end to end, or reproducing the exact failure that was supposedly resolved. Name it as a concrete, specific thing — "the three tests covering the retry path" is stronger than "the test suite"; "called the endpoint with the malformed payload from the report and got a 400" is stronger than "I tried it."

If nothing can prove the claim — the change has no checkable surface at all — say that plainly: "this is a comment-only change; there is nothing to run that would confirm it." That is a legitimate answer. Claiming completion by default, because no check occurred to run, is not.

### Step 2: Run it after the last edit, and read all of it

Run the named action after the last relevant change to the code — not before it. A check run against an earlier version of the code proves nothing about the version now sitting in front of the reader; any edit made after the last run invalidates that run for the claim being made now.

Read the full output and the exit code, not a tail or a summary. "No errors" glimpsed near the bottom of a scrollback is not the same as confirming the run actually finished and returned success — a truncated read misses failures that scrolled past, a process that hung before completing, or a nonzero exit hiding behind a clean-looking last line. Treat the exit code as a fact to check, not an impression to form from how the text looked.

### Step 3: Do not hedge in place of running it

"Should work," "probably passes," "I'm fairly confident this is correct," and "this looks right" describe a feeling, not a result. None of them substitutes for having run the proving action from Step 1. If it has not been run, the honest statement is exactly that — "I have not run this yet" — rather than dressing up the absence of evidence in confident-sounding language. A hedge and an unrun check communicate the same underlying fact; only one of them says so plainly.

### Step 4: State exactly what was verified

Report the claim at the scope the evidence actually supports. Partial evidence is not completion evidence:

- "3 of 4 checks passed" is not "tests pass"
- "it compiled" is not "it works"
- "the common case succeeded" is not "it handles everything the claim covers," when the claim implies cases that were never exercised

Say what was run, what passed, and what was left unchecked, rather than rounding any of that up to "done." A precise partial statement serves the reader better than an inflated complete one, and holds up better when something surfaces later that the rounded-up version quietly skipped.

## Freshness, Not Redundancy

Fresh evidence means the check still holds for the code as it stands right now: if anything relevant changed since a check last ran, that check needs to run again before it can support today's claim. It does not mean every check gets rerun before every claim regardless of whether anything changed — a check that already passed, against code that has not moved since, does not need to be repeated purely to feel more certain. Repeating a check that nothing invalidated adds ceremony, not information.

The working rule: re-run a check when the code it covers has changed since it last ran; skip re-running a check that already passed against code that is still exactly what it was when it passed. What matters is whether the covered surface changed, not how much time elapsed or how many exchanges happened in between — a check from an hour ago is still fresh if nothing touched what it covers, and a check from one edit ago is already stale if that edit landed inside its surface.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident it works" | Confidence describes an internal state, not the code. It is not evidence, and it does not substitute for running the check. |
| "I already checked this earlier in the session" | Only holds if nothing touched the covered code since. If any edit landed after that check, it is stale for this claim — run it again. |
| "Re-running takes too long" | The wrong claim is what actually costs time — a false "it works" costs far more than the seconds the check takes to run. |
| "The change is small / obviously correct" | Small changes cause real regressions constantly; "obviously correct" is precisely the belief that goes unexamined right up until it isn't. |
| "The user is in a hurry" | Urgency changes how much gets checked, not whether the claim matches what was actually checked. State the narrower, truthful claim faster instead of the broad unverified one. |
| "It compiled, so it probably runs fine" | Compiling and behaving correctly are separate properties. If only the compile step ran, say "it compiles" — not "it works." |
| "I read through the code and it's clearly right" | Reading code is not running it. Static confidence and runtime behavior diverge in exactly the cases most worth checking. |

## Red Flags

- Saying "done," "fixed," "working," or "passing" without naming what was actually run to check it
- Reporting a summary line ("no errors," "all green") in place of having read the full output
- Claiming success on the strength of a run that happened before the most recent edit
- Hedged phrasing ("should work," "looks right," "probably fine") standing in for a check that was never run
- Rounding a partial result up to full success ("3 of 4 passed" reported as "it passes")
- Treating "nothing looked obviously wrong" as equivalent to "confirmed working"
- Skipping the check because the deadline or the user's tone implies urgency
- Reusing an earlier result without first confirming nothing relevant changed since it ran

## Verification

Before making any completion claim, confirm:

- [ ] The specific action that proves this claim is named, not a vague generic
- [ ] It was run after the last relevant edit, not before
- [ ] The full output was read, not a tail or a summary
- [ ] The exit code, or equivalent pass/fail signal, was actually checked, not assumed
- [ ] If reusing an earlier result, nothing relevant has changed since that check ran
- [ ] The claim's wording matches the evidence's actual scope, with no partial result rounded up
- [ ] No hedging phrase stands in for a check that was never actually run
- [ ] If no check exists for this change, that absence is stated plainly instead of assuming completion by default
