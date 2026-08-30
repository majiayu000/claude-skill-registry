---
name: os-what-could-go-wrong
description: >-
  ALWAYS invoke this skill before anything hard to undo gets agreed to - a
  contract, a purchase, a migration, a launch, a price change, a
  reorganisation - and whenever the user asks "what could go wrong", "what are
  we missing", "poke holes in this", or for a premortem or a red team, in any
  language. Assumes the decision already failed and works backwards to find
  out why, in a fresh agent that had no hand in making it. Sweeps nine areas
  and shows what each produced, including the empty ones. Ends on one verdict:
  go ahead, go but fix these first, try it small first, think again, do not do
  this.
allowed-tools:
  - "Read(~/.claude/open-steps/**)"
  - "Bash(cat ${CLAUDE_SKILL_DIR}/references/premortem-prompt.md)"
---

# os-what-could-go-wrong

Assume it already failed, then work backwards to find out why - while there is
still time to change it. The attack runs in a fresh agent that had no part in
the decision, because an agent that helped shape one reviews it far too
gently: it defends its own reasoning, and it misses the thing that kills the
plan out of politeness. This skill writes the brief, hands it over, and passes
the answer back without softening it.

`os-ask-simple` screens a choice before the user picks one. This one runs
after the choice is made and before it can no longer be taken back.

## Language

Write in the language the user speaks in this session, detected from the
conversation. Names, figures and identifiers stay as they are. The agent you
dispatch cannot see this conversation and does not inherit the writing style,
so the language has to travel with the handover - see step 2.

## Step 1 - write down what is actually being decided

Find the decision first. Given as text or a document, that is it. Asked at the
end of a discussion, it is the decision the discussion arrived at, and say
which one you took it to be. If neither, ask which decision to attack.

Then fill every line. This is the only thing the fresh agent will ever see.

```
DECISION BRIEF
What will be done: three to seven sentences
What it is for: the problem it solves, and what success looks like, measured
  wherever it can be
The main moves: the money, the people, the systems, the dates
What is fixed: the constraints, plus the surrounding facts that matter
Who it lands on: who and what is affected if this goes wrong
What cannot be undone: which parts are one-way
When we would know: the date success or failure actually gets judged
What we know: facts from documents, data, the repository, past incidents,
  each with where it came from
What we are assuming: every gap nobody could close, written as an assumption
```

Close the gaps in this order, and stop as soon as a gap is closed.

1. **Look it up yourself.** Documents, data, the repository, the last report
   in `~/.claude/open-steps/reports/`, what went wrong last time.
2. **Ask, but earn the ask.** Only a gap where guessing wrong would change the
   verdict is worth the user's attention, and the pack's own rule holds here:
   one question at a time, through `os-ask-simple`. Three is plenty. Nobody
   there to answer, or an answer that would not move the verdict -> skip
   straight to 3.
3. **Write the guess down as a guess.** Put the assumed value in its line,
   mark it `(assumed)`, and repeat it under "What we are assuming".

The brief states facts and open questions. It never makes the case for the
decision: a brief that argues gets a report that agrees.

## Step 2 - hand it to an agent that had no part in it

Pick the depth, say which one in a single line, and carry on. The user can
change it at any point.

| Depth | When |
|---|---|
| **Full** | Hard to undo, or being wrong costs money, trust or data beyond one team |
| **Quick** | Reversible, and cheap to be wrong about, whoever it touches |

When in doubt, Full. The cost of a full look is a few minutes; the cost of a
quick look at a one-way door is the door.

Dispatch one general-purpose agent. Its prompt is these four things in order,
nothing else:

1. the whole analysis prompt - already inlined at the bottom of this skill,
   under "The analysis prompt, verbatim"
2. `MODE: Full` or `MODE: Quick`
3. `LANGUAGE: <the language from above>`
4. the brief

Copy the inlined prompt exactly. Never summarise it or paste part of it. Its
rules are what stop the answer turning into a list of worries, and the writing
rules inside it are the only ones that reach the agent at all.

One agent, not several. Two reports have two verdicts and two candidates for
the single belief nobody is questioning, and merging them is exactly the
editing that step 3 forbids.

## Step 3 - give it to the user straight

Pass the report through as it came. No reassurance the analysis did not earn,
no cushion sentence in front of the verdict, no quietly dropped card because
the user seemed committed. Bad news that arrives late is worth nothing.

Then offer to turn the "Fix before you commit" list into real things: edits to
the plan, tickets, an owner and a date per item, a reminder for each early
warning. That offer is the point of the whole exercise - a premortem nobody
acts on was entertainment.

"Go ahead" is delivered just as plainly. It means the plan was attacked and
held.

## Hard rules

1. **The agent that helped decide never attacks the decision.** Dispatch a
   fresh one every time, even when you already hold the whole thing in
   context. Skipping this does not save a step, it changes the answer.
2. **No quota of risks.** Publish what has a real chain behind it and nothing
   else. Two well-evidenced risks beat six padded ones, and "only two
   survived" is a finding worth saying out loud.
3. **The verdict is decided last and printed first.** Never make the reader
   assemble it from the risks.
4. **Every area of the sweep is accounted for**, including the ones that
   produced nothing. An area nobody mentions and an area nobody checked look
   the same to the reader.
5. **A skipped section keeps its one line saying why.**
6. **A lease and a database migration get the same treatment.** This is not a
   technical review; the nine areas apply to both, and the money and people
   ones are where technical decisions usually actually fail.
7. **"The plan is sound" is a legitimate answer** once the attack has run. It
   is never a substitute for running one.

## Known gotchas

- **No date to be judged by means no premortem.** "It failed" is meaningless
  without "by when". Pick a date that fits the decision, and say you picked it.
- **The brief is where this is won or lost.** The fresh agent sees nothing
  else. The usual failure is a brief missing the one constraint that made the
  decision sensible, which produces a confident report attacking a plan nobody
  proposed.
- **Fewer than three risks reads as a lazy analysis and is often the right
  answer.** The record of what was checked is what tells those apart.
- **Something reversible and cheap does not need this.** Quick look, or say it
  does not need one. Running a full attack on a two-day experiment teaches the
  user to ignore the next one.
- **"Try it small first" is not a soft no.** It means the unknowns are
  testable and worth testing before the money moves.
- **The user may go ahead against all of it.** That is their decision and they
  now have the early warnings. Note it once, set the tripwires up if they want
  them, and do not re-argue the report.

## The analysis prompt, verbatim

The block below is the whole of
[`references/premortem-prompt.md`](references/premortem-prompt.md), inlined
when this skill loads, so no file has to be read at dispatch time. If the
block shows a literal `cat` command instead of the prompt, this harness does
not run inline commands: open that file next to this one and use its full
text.

!`cat ${CLAUDE_SKILL_DIR}/references/premortem-prompt.md`
