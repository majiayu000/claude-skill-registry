---
name: experiment-workflow
description: Run thesis experiments from ideation through publication. Use when brainstorming research questions, writing specs, executing experiments, or polishing for thesis.
---

# Experiment Workflow

This skill covers the lifecycle of a research experiment from initial idea to thesis publication.

## Workflow stages

1. **Ideation** — Capture and deconfuse the research question
2. **Specification** — Plan execution with clear success criteria
3. **Execution** — Implement, run, analyze (OODA loop)
4. **Polishing** — Prepare artifacts, code, and writeup for thesis

Agents typically work on one stage (~80% of sessions). You can proceed through multiple stages in one session, but results tend to be subpar—these are long-horizon tasks, and agents excel at medium-horizon work.

## Where things live

| Artifact | Location |
|----------|----------|
| Tracking table | `packages/latex_viterbo/experiments.md` |
| Experiment code | `packages/python_viterbo/src/viterbo/experiments/<label>/` |
| Specification | `<experiment folder>/SPEC.md` |
| Rust-only specs | `packages/rust_viterbo/docs/<label>.md` (rare) |
| Polished writeups | `packages/latex_viterbo/chapters/appendix-detailed-experiments.tex` |
| Plots/figures | `packages/latex_viterbo/assets/<label>/` |
| Data artifacts | `packages/python_viterbo/data/<label>/` |

**Polished writeups** go in a single growing file (`appendix-detailed-experiments.tex`). Each experiment becomes a `\section{<label>}`. If the file gets unwieldy, we can split to folder + `\input` later.

**Labels** unify everything: the experiment folder name, thesis section label, tracking table row, and asset folder all use the same label (e.g., `counterexample-hko`, `dimension-5-probing`).

## Stage 1: Ideation

**Goal:** Turn a vague idea into a clear, answerable research question.

**Process:**
1. Write down the question in plain language
2. Deconfuse: What exactly would a "yes" or "no" answer look like?
3. Identify what's already known (prior work, related experiments in the thesis)
4. Note what's still unclear or needs Jörn's input

**Artifact:** New row in `packages/latex_viterbo/experiments.md`:

```markdown
| label | Ideation | The research question | Any notes |
```

Mark as `[proposed]` until Jörn approves. No folder needed yet—just the tracking entry.

## Stage 2: Specification

**Goal:** Plan execution with enough detail that another agent could implement it.

**Process:**
1. Define success/failure criteria explicitly
2. Identify required inputs (data, algorithms, dependencies)
3. Sketch implementation approach
4. Estimate what artifacts will be produced
5. Note which thesis section(s) this feeds into (if known)

**Artifact:** Create the experiment folder and write `SPEC.md`:

```
packages/python_viterbo/src/viterbo/experiments/<label>/
└── SPEC.md
```

Update tracking table status to "Specified".

**SPEC.md should include:**
- Research question (copied from tracking table)
- Inputs: what data/code is needed
- Method: implementation approach
- Success criteria: what outcome means "it worked"
- Expected outputs: data files, plots, metrics

## Stage 3: Execution

**Goal:** Implement and run the experiment, producing results.

This is standard work: analyze requirements, write code, run it, interpret outputs. Use the OODA loop—observe, orient, decide, act—adapting on the fly while paying attention to outer context. Most agents know how to do this given a clear spec.

**Context for execution agents:**
- See `python-conventions` skill for experiment code structure
- See `rust-conventions` skill if modifying algorithms
- SPEC.md in the experiment folder has success criteria

**Artifact:** Working code, data artifacts, preliminary results. Update tracking table status to "Executed" or "In progress".

## Stage 4: Polishing

**Goal:** Prepare everything for thesis publication.

**Process:**
1. Clean up code (lint, tests, docstrings where non-obvious)
2. Finalize data artifacts with clear naming
3. Generate publication-quality plots/tables → `packages/latex_viterbo/assets/<label>/`
4. Write experiment section in `appendix-detailed-experiments.tex` with interpretation
5. Self-review against the thesis's high standards
6. Update tracking table status to "Polished" or "Complete"

**Done when:** Passes your self-review against thesis standards. Jörn reviews as fallback for complex interpretations or if thesis standards were misunderstood.

## Abandoned / Failed / Superseded experiments

Experiments don't always succeed. When abandoning:

1. Update tracking table: status → "Abandoned" / "Failed" / "Superseded by X"
2. Clean up code: remove dead implementation, but keep a stub with:
   - The original SPEC.md (or summary of it)
   - Brief explanation of why abandoned (saves future agents time)
3. Optionally note in thesis appendix if the failure is instructive

## Approval markers

Use `[proposed]` for agent-proposed content awaiting Jörn's review.

**Critical:** Never write "approved" markers without Jörn's explicit approval. Ambiguous responses ("sounds fine") do not count as approval.

Only Jörn removes `[proposed]` markers.

## Handoff between stages

When finishing a stage:
1. Update the tracking table with current status
2. Ensure SPEC.md (if exists) reflects current state
3. Commit changes with clear message referencing the label (e.g., "counterexample-hko: complete specification")
4. If blocked or needing input, note it explicitly in SPEC.md or tracking table

[proposed]
