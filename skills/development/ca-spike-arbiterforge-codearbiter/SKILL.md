---
name: ca-spike
description: Exploratory spike on a throwaway branch — answer a named question with disposable code. Never merges; exits to a findings note or /ca-feature.
argument-hint: "<question to answer> [timebox]"
---

# /ca-spike — exploratory spike

The sanctioned lane for "I need to write code to find out." Spike code is disposable by contract:
it never merges, never PRs, and never becomes the implementation. What survives a spike is the
*answer*, written down — the code is burned.

## Flow

1. **Name the question** — a spike without a falsifiable question is just freelancing. Restate
   `$ARGUMENTS` as the question the spike answers and the timebox (default: one session). STOP for
   the user's confirmation.
2. **Branch** — create `spike/<slug>` from the current branch. All spike work stays on it.
3. **Explore** — no `tdd`, no plan, no review fleet. Two rules survive even here: no secret leaves
   the approved store, and no irreversible operation (prod data, destructive migration) runs from a
   spike.
4. **Exit — exactly one of:**
   - **Answered** → write the findings to `<project-root>/.codearbiter/spikes/<slug>.md`
     (the question, what was tried, the answer, what it implies), then delete the branch. If the
     answer warrants building, hand the findings to `/ca-feature` — the spike file seeds
     `brainstorming`; the spike code is reference material, never the implementation.
   - **Timebox expired, no answer** → record that too (a dead end is a finding), delete the branch.

## Hard gate

MUST NOT merge or PR a `spike/*` branch — its only exits are a findings file and deletion. MUST NOT
copy spike code into an implementation branch wholesale; implementation re-enters through
`/ca-feature` and `tdd`. Secret-handling and irreversibility rules hold even in a spike. Commits on
a `spike/*` branch are exempt from `commit-gate` — the exemption is safe precisely because nothing
on the branch can ever land.

## When NOT to use

- You already know what to build → `/ca-feature`.
- Diagnosing a defect → `/ca-debug` (investigation with a structured exit).
- A question answerable by reading code or docs → `/ca-btw`.
