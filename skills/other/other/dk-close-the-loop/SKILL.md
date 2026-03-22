---
name: dk-close-the-loop
description: "Iteratively improve any output by running a structured observe-hypothesize-change-rerun loop. Uses an organized scratch directory to prevent context blowup — the conversation stays thin while iterations accumulate on disk. Use when an output (reflection, plan, prompt, pipeline result) isn't good enough and needs systematic refinement. Triggers on: 'close the loop', 'this output isn't good enough', 'iterate on this', 'refine this output', 'improve this reflection', or /dk-close-the-loop."
argument-hint: "[scratch_dir] [description of what to improve]"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-close-the-loop — Iterative Output Refinement

You have an open loop: something produced output, the output isn't good enough, and you need to systematically improve it. This skill closes that loop.

The core discipline: **everything lives on disk, not in conversation context.** The scratch directory is the organized record of what was tried, what worked, and why. Subagents read from disk, write to disk, and report back in 2-3 line summaries. The main conversation only holds the current hypothesis and verdict — never full outputs.

## Context

<loop_context> $ARGUMENTS </loop_context>

If the context above is empty or unclear, ask the user:
1. What produced the output? (command, prompt, pipeline step)
2. What's wrong with it? (vague is ok — "it's not good enough" is a valid start)
3. Where should the scratch directory live? (suggest `temp_reflections/` or `temp_loop/`)

## The Scratch Directory

This is the product. Not temp files — the organized log of the refinement process.

```
<scratch_dir>/
├── loop.md                # Live loop state (see template below)
├── baseline/
│   ├── output.md          # Original output that needs improvement
│   ├── critique.md        # Structured critique of what's wrong
│   └── run_command.txt    # Exact command/process that produced the output
├── iter-1/
│   ├── hypothesis.md      # What to change and why
│   ├── changes.md         # What was actually changed (with file paths and diffs)
│   ├── output.md          # New output after changes
│   ├── comparison.md      # Before vs after, structured
│   └── verdict.md         # Better / worse / mixed — with evidence
├── iter-2/
│   └── ...
└── summary.md             # Written when loop closes
```

### loop.md template

This file is the single source of truth for where the loop is. Read it at the start of every iteration. Update it after every verdict.

```markdown
# Close-the-Loop: [short description]

## Target
What we're improving: [one line]
Run command: [the exact command to re-run]
Quality signal: [how we know it's better — specific, measurable if possible]

## Current State
Iteration: [N]
Best so far: [baseline | iter-N]
Status: [observing | hypothesizing | changing | running | comparing | closed]

## Hypothesis Log
- iter-1: [hypothesis] → [verdict: better/worse/mixed]
- iter-2: [hypothesis] → [verdict]
- ...

## What We've Learned
- [Accumulated insights that carry forward — things that definitely help or definitely don't]

## Next
[What to try next, or "CLOSED: [reason]"]
```

## The Loop

### Phase 0: SET UP (first invocation only)

1. Create the scratch directory structure
2. Capture the baseline output — either from the user's clipboard/description, or by running the command
3. Write `run_command.txt` with the exact command that produces the output
4. Write `loop.md` with initial state
5. Proceed to Phase 1

### Phase 1: OBSERVE

Delegate critique to a subagent (sonnet). The subagent reads the current output and produces a structured critique. The main conversation does NOT read the full output — only the critique summary.

```
Task(model: sonnet, subagent_type: general-purpose)

Read <scratch_dir>/[baseline or iter-N]/output.md

Produce a structured critique:
1. STRENGTHS: What's working well (keep these)
2. WEAKNESSES: What's not working, ranked by impact
3. MISSING: What should be there but isn't
4. EXCESS: What's there but shouldn't be (noise, fluff, wrong focus)
5. ROOT ISSUE: The single biggest thing to fix (not a list — pick one)

Write your critique to <scratch_dir>/[baseline or iter-N]/critique.md
Return a 3-line summary: the root issue, the top weakness, and one strength to preserve.
```

### Phase 2: HYPOTHESIZE

Based on the critique summary (not the full output), form a hypothesis. This happens in the main conversation — it's a judgment call, not mechanical work.

Write to `<scratch_dir>/iter-N/hypothesis.md`:

```markdown
# Hypothesis for Iteration N

## What to change
[Specific change — which file, which prompt section, which config value]

## Why this should help
[Connect the change to the root issue from the critique]

## What to watch for
[Side effects — things that might get worse when this gets better]

## Estimated impact
[High / Medium / Low — on the specific quality signal defined in loop.md]
```

The hypothesis must be specific enough that someone else could apply the change without seeing the conversation. "Make the prompt better" is not a hypothesis. "Add a structured output format requirement to the reflection prompt because the current output is unstructured prose that's hard to evaluate" is a hypothesis.

### Phase 3: CHANGE

Apply the changes described in the hypothesis. This could be:
- Editing a prompt file
- Changing a config value
- Modifying code that processes/generates the output
- Adjusting parameters (model, temperature, max tokens)

Log what changed in `<scratch_dir>/iter-N/changes.md`:

```markdown
# Changes for Iteration N

## Files modified
- `path/to/file.py` — [what changed, 1 line]
- `path/to/prompt.md` — [what changed, 1 line]

## Diffs
[Actual diffs or before/after snippets for each change]
```

### Phase 4: RUN

Execute the command from `run_command.txt` to produce new output. Capture the output to `<scratch_dir>/iter-N/output.md`.

If the run command involves `odin exec`, `odin reflect`, or similar commands that can't run inside Claude Code, provide the user with copy-paste commands and wait for them to paste the output back. Note this in loop.md's status.

If the run command is something that CAN run (a Python script, a test, an API call), run it directly.

### Phase 5: COMPARE

Delegate comparison to a subagent (sonnet). The subagent reads ONLY the two outputs — it does not see the hypothesis or changes. This keeps the comparison unbiased.

```
Task(model: sonnet, subagent_type: general-purpose)

Compare these two outputs for quality. You do not know which is "old" or "new."

Output A: <scratch_dir>/[previous best]/output.md
Output B: <scratch_dir>/iter-N/output.md

Quality signal: [from loop.md]

Produce:
1. WINNER: A or B or TIE (on the specific quality signal)
2. EVIDENCE: 3-5 specific examples showing why
3. TRADE-OFFS: Did anything get worse in the winner?
4. CONFIDENCE: How clear is the difference? (obvious / marginal / unclear)

Write to <scratch_dir>/iter-N/comparison.md
Return: winner + confidence + one-line evidence summary
```

### Phase 6: VERDICT

Based on the comparison summary, update loop state:

Write `<scratch_dir>/iter-N/verdict.md`:
```markdown
# Verdict: Iteration N

Result: [BETTER / WORSE / MIXED]
Confidence: [obvious / marginal / unclear]
Evidence: [1-2 lines from comparison]
Keep: [what to preserve from this iteration]
Revert: [what to undo if anything]
```

Update `loop.md`:
- Increment iteration
- Update "best so far"
- Add to hypothesis log
- Add to "what we've learned"
- Set "next" — either another hypothesis or CLOSED

### When to close the loop

Close when any of these are true:
- The quality signal is met (output is good enough)
- 3 consecutive iterations show no improvement (diminishing returns)
- The user says to stop
- The cost of another iteration exceeds the expected improvement

Write `<scratch_dir>/summary.md`:

```markdown
# Loop Summary: [description]

## Result
Started: [date]
Iterations: [N]
Best: [iter-N]
Status: [closed — quality met / closed — diminishing returns / closed — user stopped]

## What worked
- [Changes that improved output, with evidence]

## What didn't work
- [Changes that didn't help or made things worse]

## Final state
Run command: [the command with all improvements applied]
Output quality: [assessment against the original quality signal]

## If reopening later
Read iter-[best]/output.md for the current best.
The key changes that got us here: [1-2 sentences].
The remaining weakness: [if any].
```

## Context Management Rules

These are non-negotiable — they're the entire point of using a scratch directory:

1. **Never paste full outputs into the conversation.** They live on disk. Subagents read them from disk. The main conversation sees only summaries.

2. **Never hold more than one iteration's hypothesis + verdict in conversation.** If you need to reference earlier iterations, re-read loop.md — it has the condensed history.

3. **Subagents are stateless.** Each subagent gets pointed at specific files on disk. They don't inherit conversation context. This is a feature — it prevents context buildup.

4. **loop.md is the resumption point.** If the conversation compacts or a new session starts, loop.md + the iteration folders contain everything needed to continue.

5. **The user sees summaries, not data.** After each phase, report to the user in 2-3 lines: what happened, what the verdict was, what's next. They can dig into the scratch directory if they want details.
