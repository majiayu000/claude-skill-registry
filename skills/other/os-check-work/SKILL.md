---
name: os-check-work
description: >-
  ALWAYS invoke this skill when the user asks about work done outside this
  session - "check work", "check the others", "check other sessions" - or to
  accept one: "the session is done, check it", "can we merge it" - in any
  language. You are the receiving party: treat the report as a claim, verify
  each part against machine state, name every gap between claimed and true.
  Verified-ready work merges in the same pass. End with what is left, one
  next step, and any reply another session needs, ready to paste.
allowed-tools:
  - "Read(~/.claude/open-steps/**)"
  - "Bash(gh pr list *)"
  - "Bash(gh pr view *)"
  - "Bash(gh pr checks *)"
  - "Bash(gh pr checks)"
  - "Bash(gh pr diff *)"
  - "Bash(gh pr diff)"
  - "Bash(gh pr merge *)"
---

# os-check-work

You are the receiving party: another session says it finished, and your job
is to find out whether that is true. Reports run optimistic - they are written
by whoever did the work. Triggers live in the description above; one more is
taking over work you did not do.

## Language

Write in the language the user speaks in this session, detected from the
conversation. Code, file names and identifiers stay English.

## The stance

- A report is a claim by the party being assessed, and its adjectives are not
  measurements: "tests are green" vs the count that ran. Ask for the number.
- "Done" is a snapshot: reviews get revoked, branches fall behind, checks flip
  - often with no new commit. Re-read immediately before you act.

## Two modes

Plural is a **sweep**: every sibling session, one line each, statuses only.
Singular - "accept this", a named session or pull request - is an **accept**:
full verification, then acceptance. A sweep that finds verified-ready work
rolls into accepting it - the accept steps run first, never skipped.

## Sweep

One line per session, one call per pull request - the reader skims these and
reads the closing block. No table:

**<name a person recognises (#PR)>** - <product change>; <all done? plus
proof in 2-4 words, or what is missing>; <archive: yes / not yet>.

- Name from the ticket or PR title, never your shorthand; the change for the
  product, not a file list.
- A yes carries its proof ("checks green, review approved"); never a bare yes.
- "All done" ≠ "can archive": finished work can still await acceptance.
- Order: needs-the-user, then broken, then still-working - a running session
  is one word, not a finding.
- No deep verification in a sweep: say what you did not open and what that
  leaves unverified. Never announce your working mode - "cheap checks" is
  bookkeeping.
- A session waiting on an answer gets it in the same pass - see "The reply";
  when that needs the deep read, the reply becomes the do-this-next.
- Name the sessions you could not read, and why.

## Accept - steps 1 to 5 (never per-session inside a sweep)

1. **Find the claim.** Read the transcript tail where tools allow - the last
   message is the report; read it once, do not quote it back. No tools → the
   pull request is the artefact; say so.
2. **Verify each claim at its source.**

   | The session claims | Where the truth lives |
   |---|---|
   | checks are green | `gh pr checks` - counts and states, not the summary word |
   | it was approved | `--json reviewDecision,latestReviews` - revocable on the same commit |
   | no open discussions | the unresolved-thread count, not "I addressed the comments" |
   | ready to merge | `mergeStateStatus` - and again right before merging |
   | tests were added | find them in `gh pr diff` - the most common false report |
   | it stayed in scope | `gh pr diff --name-only` vs the task; flag unasked files |
   | linked to the task | the ticket in branch, title or body |

   Prefer numbers to words. Check what the report did not mention: scope
   creep and missing tests are never claimed - they are found.
3. **Name the gaps** - the deliverable. One line each: `Claimed: … Measured: …`.
   No gaps → say so in one line; a clean intake is a real result.
4. **Accept, hand back, or unblock.**
   - Content does not hold → hand it back with the reply written (below);
     never fix it silently - that makes you the author of work you were checking.
   - Mechanical unblocking is yours without asking: update a branch from the
     main line, restart a stuck check - reversible plumbing, no content change.
   - Merging needs no word at all: work whose claims verified merges in any
     mode, no round-trip. Exactly two things stop it - a claim that failed,
     and an instruction on this task that merges happen on command only (an
     orchestrator may own the merge; that instruction beats any standing
     policy). The verification itself is never skipped.
5. **Clean up.** Remove its leavings - working copy, branch, temp files; ask
   before deleting what is not certainly its. Archive verdict → closing block.

## The reply is part of the pass

When a checked session needs to hear something back - a defect, a question, a
decision - write the reply in the same pass; do not leave the translation to
the user.

```
**To <session name>** - paste this:
<the instruction, verbatim>
```

- Self-contained - the target never read this chat: name the PR, file, gap.
- It speaks as the user: a plain instruction, not a review essay.
- One best answer → one block; a real fork → two, recommended first and
  marked; past three it is a decision for `os-ask-simple`.
- Carry the claimed/measured pair - evidence, not adjectives.

## Ending the pass

Both modes end the same way, always last, nothing after it:

```
| | |
|---|---|
| **Still open** | <what remains, or "nothing"> |
| **Do this next** | <the one action> - <one clause of reasoning> |
| **On your word** | <what you will do once they say it> |
```

- Say whether anything is left, including what waits on the user; a remainder
  past three items goes to `os-whats-next`.
- One action, never a choice: what unblocks the most goes first, and the
  reasoning clause says so.
- Nothing ready is a real answer - "nothing to accept yet, watch X". Never
  invent an action; a step that is not yours → say whose (`os-step-by-step`).
- Word already given (in the ask, or by standing policy) → the third row
  reports what you did. Pass closed everything → run `os-whats-next`.
- Never end on a question mark - you have the measurements, so the opinion.

## Hard rules

1. Never repair another session's work silently - name it, return it.
2. Never accept on the strength of the report alone; detail is not evidence.
3. Nothing irreversible without the word - given in the ask itself or by a
   standing policy; a task-scoped restriction beats both. Merging verified
   work already has that policy: step 4.
4. Re-read state immediately before acting.
5. Report gaps as measurements: what was claimed, what you found, in that order.
6. Say what you could not check - no access is a gap, not absence of problems.
7. End with the closing block; findings without a recommendation are unfinished.

## Known gotchas

- Behind the main line ≠ conflicted: it needs an update, not the author.
- A conflicted branch may have run no checks: nothing-ran looks green.
- Delete a branch only from outside its own working copy.
- Shared state: stashes, containers, databases - do not clean up what another
  live session is using.
- A draft is not a finished session; check the author considers it done.
