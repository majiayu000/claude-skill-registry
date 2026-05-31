---
name: paper-writing-bench
description: Reverse-engineer raw materials (Sparse idea, Dense idea, experimental log) from an existing AI research paper to build a benchmark case for evaluating paper-writing pipelines. Replicates the PaperWritingBench dataset construction procedure from arXiv:2604.05018 §3 / App. C. TRIGGER when the user asks to "build a benchmark case from this paper", "reverse-engineer raw materials", or "evaluate my pipeline against PaperWritingBench".
---

# PaperWritingBench (§3)

Faithful implementation of the PaperWritingBench dataset construction
procedure from PaperOrchestra (Song et al., 2026, arXiv:2604.05018, §3 and
App. C, F.2).

The original benchmark contains 200 papers (100 CVPR 2025 + 100 ICLR 2025).
For each paper, the authors reverse-engineer the (I, E) tuple by stripping
narrative flow from the original PDF using the three prompts in App. F.2.
You can use this skill to reverse-engineer your own benchmark cases from
any paper PDF.

## What this skill does

Given an existing AI research paper (PDF or markdown extract), produce:

- `idea.md` (Sparse variant) — high-level concept note, no math, no
  experimental results
- `idea.md` (Dense variant) — detailed technical proposal with LaTeX
  equations and variable definitions, but still no experimental results
- `experimental_log.md` — exhaustive raw experimental setup, numeric data,
  and qualitative observations, with all narrative references stripped

These three files form a complete (I, E) input pair for the
paper-orchestra pipeline. You can then run the pipeline and compare its
output to the original paper using `paper-autoraters`.

## Inputs

- A paper PDF or extracted markdown text. The paper uses MinerU
  (Wang et al., 2024) for PDF→markdown extraction; you (the host agent)
  should use whatever PDF extractor your environment provides.
- For controlled experiments, you may also extract figures separately
  (PDFFigures 2.0 in the paper).

## Outputs

- `bench/<paper_id>/idea_sparse.md` — Sparse variant
- `bench/<paper_id>/idea_dense.md` — Dense variant
- `bench/<paper_id>/experimental_log.md` — Experimental log

## Workflow

For each paper, run three independent LLM calls using the verbatim prompts
below:

### 1. Sparse idea generation

Load `references/sparse-idea-prompt.md`. Pass the paper text (or
markdown extract) as `{paper_content}`. The prompt instructs the model to:

- Stop extracting at empirical verification (no Experiments / Results / Comparisons)
- Use first-person future tense ("We propose to explore...")
- Avoid LaTeX math; describe components by function
- Anonymize authors and titles

Output: `idea_sparse.md` with the four sections (Problem Statement, Core
Hypothesis, Proposed Methodology high-level, Expected Contribution).

### 2. Dense idea generation

Load `references/dense-idea-prompt.md`. Same input. The prompt instructs
the model to:

- Preserve mathematical formulations using LaTeX
- Define every variable used in equations
- Include specific architectural choices and dimensions
- Same exclusion zone (no experiments)

Output: `idea_dense.md` with the four sections (Problem Statement, Core
Hypothesis, Proposed Methodology detailed, Expected Contribution).

### 3. Experimental log generation

Load `references/experimental-log-prompt.md`. Same input. The prompt
instructs the model to:

- Use past-tense persona ("We ran...", "The results were...")
- Strip all references to figure/table numbers
- Deconstruct tables into raw numeric data
- Log figure findings as factual observations
- Anonymize authors

Output: `experimental_log.md` with sections for Setup, Raw Numeric Data,
and Qualitative Observations.

## Critical rules from the prompts

These are excerpted from App. F.2. The host agent MUST honor them:

- **No citations.** None of the three outputs may contain `\cite`,
  reference numbers, or author names from the source paper.
- **No URLs.** Strip all hyperlinks.
- **Anonymize.** Author identities, affiliations, acknowledgements all
  removed.
- **Self-contained.** Each file must make sense without the original paper.
- **No experimental leakage in idea files.** The Sparse and Dense ideas
  must stop where empirical verification begins. They describe what will
  be done, not what was done.
- **No table/figure references in experimental log.** No "as shown in
  Table 1", "see Fig. 5". The downstream paper-orchestra pipeline will
  generate its own figures and tables — the log must not assume any
  particular ones exist.
- **100% numeric accuracy in experimental log.** This becomes the ground
  truth for the section-writing-agent and content-refinement-agent's
  hallucination check.

## How the bench is used

After producing `(idea_sparse.md, idea_dense.md, experimental_log.md)` for
a paper:

1. Pick a variant (Sparse or Dense) — the paper ablates both, with Dense
   producing more rigorous methodology and Sparse exercising the system's
   robustness on under-specified inputs.
2. Drop the chosen `idea.md`, plus `experimental_log.md`, plus a
   `template.tex` for the target conference, plus a
   `conference_guidelines.md`, into a paper-orchestra workspace.
3. Run the pipeline.
4. Compare the generated paper against the original using
   `paper-autoraters` (citation F1, lit review quality, SxS paper quality).

## Resources

- `references/bench-overview.md` — the 200-paper bench, venue cutoffs, sizes
- `references/sparse-idea-prompt.md` — verbatim from App. F.2
- `references/dense-idea-prompt.md` — verbatim from App. F.2
- `references/experimental-log-prompt.md` — verbatim from App. F.2
