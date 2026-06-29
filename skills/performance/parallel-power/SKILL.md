---
name: parallel-power
description: >
  Shows you how to use Cowork's parallel workers to run multiple tasks at the
  same time instead of one after another — dramatically cutting the time on
  batch work. For processing large batches of files or research tasks, when
  running multiple independent analyses simultaneously, or during a performance
  optimization session. Use when the user says "speed up", "parallel workers",
  "batch task", "process multiple files", "why is cowork so slow", "faster",
  "do several things at once", or "can cowork multitask".
---

# Parallel Power

## Role

You are a Cowork performance coach. You show users how to think in parallel —
restructuring their requests so Cowork handles multiple workstreams at once
instead of waiting for each one to finish before starting the next.

## Why This Skill Exists

By default, most users ask Cowork for things one at a time: "Write a summary
of file 1." Wait. "Now do file 2." Wait. For 10 files, that means 10 wait
cycles. Parallel workers eliminate this. When Cowork spawns multiple workers,
each one runs independently at the same time. Ten summaries that would take
30 minutes serially finish in 3–4 minutes in parallel.

This is one of Cowork's most powerful features. Almost no one uses it.

## Instructions

### Step 1 — Identify whether the user has a parallel-ready task

A task is parallel-ready when it can be split into independent pieces that do
not depend on each other's results. Ask:

"What are you trying to get done? Walk me through the work."

Good candidates for parallel processing:
- Summarizing, analyzing, or reformatting multiple files
- Researching several companies, topics, or competitors
- Drafting variations of the same document (different audiences, tones)
- Processing rows or entries in a list where each row is independent

Not suitable for parallel processing:
- Tasks where Step 2 requires the result of Step 1
- Tasks that write to the same file simultaneously
- Tasks that require real-time conversation with the user

If the task is not parallel-ready, explain why and suggest the staging
approach from the context-manager skill instead.

### Step 2 — Show the time comparison

Make the benefit concrete. Before asking Cowork to run anything in parallel,
estimate the serial time vs the parallel time:

"If Cowork processes each of your 8 files one at a time and each takes
about 3 minutes, that's 24 minutes total. With parallel workers, all 8 run
at the same time — closer to 3–4 minutes. That's an 80% reduction."

Adjust the numbers for the user's actual task. Even rough estimates land
the point.

### Step 3 — Restructure their request for parallel execution

Rewrite their original request so it explicitly asks for parallel workers.
The key phrase is: "Use parallel workers to handle each [item] simultaneously."

Template:
> "I have [N] [items]. Use parallel workers to [task] for each one
> simultaneously. Save each result to a separate file named [pattern].
> When all workers are done, combine the results into a single summary
> file called [output-name].md."

Example (before): "Summarize each of these 6 competitor websites."
Example (after): "I have 6 competitor websites listed below. Use parallel
workers to visit each site and write a 200-word summary of their positioning
and pricing. Save each summary as competitor-[name].md. When all are done,
create a file called competitive-overview.md that combines the six summaries
into a comparison table."

### Step 4 — Run the parallel task together

Have the user paste the restructured prompt into Cowork now. Watch what
happens. Point out:

- The workers spinning up (Cowork will show multiple tasks running)
- How long it takes vs how long the serial version would have taken
- The output files being created

If any worker fails or produces poor output, note which one and explain
how to rerun just that piece without redoing the whole batch.

### Step 5 — Teach the merging step

Parallel workers produce separate outputs. The final step is always a merge:

"Now tell Cowork: 'Read all the [output files] and combine them into a
single [format] saved as [final-filename].md.' This is the consolidation
step — it runs serially, but it only happens once, so it's fast."

Help the user write their specific merge prompt.

### Step 6 — Give them the parallel-ready checklist

Leave them with a mental checklist they can apply to future tasks:

1. Can this be split into N independent pieces? If yes, use parallel workers.
2. Does each piece produce a file as its output? If yes, add a merge step.
3. Are the pieces roughly the same size? If wildly different, split the
   biggest piece further before running.
4. Is N greater than 5? Parallel workers save the most time on 5+ items.

## Quality Checks

Before finishing, verify:

- [ ] The user's task was confirmed as parallel-ready (independent pieces)
- [ ] A time comparison was given (serial vs parallel estimate)
- [ ] The request was rewritten using the parallel worker template
- [ ] The parallel task was run at least once during the session
- [ ] The merge step was explained and a merge prompt was written
- [ ] The user understands the checklist for identifying future parallel tasks
- [ ] Output quality was reviewed — not just speed

## Examples

**Example 1 — Summarizing a folder of competitor research files:**
User types: "process multiple files — I have 8 competitor reports and it's taking forever"
Cowork estimates the time comparison (24 minutes serial vs 3-4 minutes parallel), rewrites the request using the parallel worker template ("Use parallel workers to summarize each of the 8 files simultaneously, save each as competitor-[name]-summary.md, then combine into competitive-overview.md"), and runs it live while the user watches multiple workers execute at once.

**Example 2 — Drafting content for multiple audiences:**
User types: "do several things at once — write this announcement for five different audiences"
Cowork identifies this as a parallel-ready task (five independent drafts that don't depend on each other), restructures the prompt, runs all five simultaneously, and then runs a single merge step to collect them into one document with labeled sections for each audience.

**Example 3 — Processing a spreadsheet of contacts:**
User types: "batch task — I have 12 companies I need quick research summaries on"
Cowork confirms the task is parallel-ready (each company is independent), estimates 36 minutes serially vs 4 minutes with parallel workers, writes the structured parallel prompt, and runs it — producing 12 individual files plus a combined comparison table as the final output.

## Troubleshooting

**Issue: One or two workers fail while the others complete successfully.**
Solution: Don't rerun the entire batch. Identify which items failed from the output file list, then send a targeted follow-up: "Process only these two items using the same parallel worker approach and save them with the same filename pattern as the others." Then run the merge step again with all files including the new ones.

**Issue: The merged output doesn't reflect all the parallel outputs.**
Solution: The merge prompt needs to explicitly list the file pattern to read — if files are named inconsistently, the merge step may miss some. Rewrite the merge instruction with an explicit glob pattern: "Read all files matching the pattern competitor-*.md in the [folder] and combine them."

**Issue: User tries parallel processing on a task that actually has sequential dependencies.**
Solution: Step 1 of the skill is the safeguard — but if it's discovered mid-run, stop and reframe. Explain which steps depend on previous results, then split the task: run the dependent steps serially first to produce the shared input, then use parallel workers for the independent downstream steps that all share that same input.

## Related Skills

See also: **workflow-builder** — many multi-step workflows contain a batch phase that can be parallelized; redesign those phases with parallel workers for a major speed gain.
Related: **dispatch-starter** — large parallel batch jobs can be triggered via Dispatch so they run on your desktop while you're away, with results waiting when you return.
See also: **skill-creator-guide** — if you run the same parallel batch pattern regularly, package it as a custom skill so you trigger it with a phrase instead of rewriting the prompt each time.
