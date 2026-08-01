---
name: loop-me
description: 'Use when the user wants to design a recurring personal or team workflow: capture loops, write specs in workflows/*.md, and run a stateful askme session until the spec is implementer-ready. Triggers: "loop me", "design a workflow", "automate this recurring task", morning routine, inbox processing.'
argument-hint: "A workflow to design, or nothing to go find one"
---

# Loop Me

Run a stateful `askme` (adversarial) session whose only output is **workflow** specs. Use the askme discipline (relentless, one question at a time, a recommended answer attached to each) aimed at the vocabulary and goal below. Create, edit, and delete specs as the session resolves things.

## Verbalized Sampling

Before the first question in both argument and no-argument paths, run a Verbalized Sampling (VS) pass.

- **If an argument names a workflow**: Sample competing interpretations or goals of that workflow.
- **Otherwise (no argument)**: Sample candidate recurring loops worth specifying.

Output the weighted hypotheses and falsifiers immediately before the first `askme` question:

1. [Weight: X.XX] hypothesis/candidate
   - Falsifier: [observation or scenario that would invalidate this]

2. [Weight: Y.YY] hypothesis/candidate
   - Falsifier: [observation or scenario that would invalidate this]

Synthesize the survivors (highest-weighted hypotheses) into the initial loop candidates and unknowns, integrating them directly into loop discovery. Do not resample unless subsequent answers materially change the survivor set.

## The loop lens

A **loop** is a recurring pattern in the user's life: their career, their week, their morning, a single repeated activity. Picturing a life as loops within loops reveals how predictable its activities really are, which is what makes them worth **delegating**. Use the lens to find loops worth specifying, and propose ones the user hasn't noticed.

A **workflow** is the spec of one loop, made real. You run a workflow on a loop: the loop is its running instantiation. Workflows live in `workflows/*.md` and are the source of truth.

## Vocabulary

A shared language, reached for only when a workflow calls for it, never a checklist. **Mandate nothing structural**: a workflow needs no AI, no checkpoint, and no schedule unless the askme session shows it does.

- **Trigger**: what fires each run: an **event** (a new email, a new issue) or a **schedule** (every morning). Event-triggering is usually the more efficient.
- **Checkpoint**: a human-in-the-loop point where the user is asked to verify or decide. Some workflows have none and run autonomously; some use no AI at all.
- **Push right**: defer the checkpoint as far as it will go. Do maximal work before involving the human, so they are asked once, late, with everything prepared.
- **Brief**: what a checkpoint presents, a tight decision-ready summary (what was produced, why, and a link down to the asset itself), never the raw output. The user reads a brief, not a draft. Speed of review is imperative.

## Definition of done

A workflow spec is done when an implementer agent could build it without asking a single question. Continue the askme session until then; nothing is done while a question remains.

## The workspace

- `workflows/*.md`, one spec per workflow.
- `NOTES.md`, raw notes on the user's world: the tools they use, the channels they process, and their own terminology for both. When it is empty or thin, interview them about their world before specifying anything. Sharpen fuzzy terms into canonical ones as they surface, and record them here.
