---
name: paper-autoraters
description: Run the four paper-quality autoraters from PaperOrchestra (arXiv:2604.05018, App. F.3) — Citation F1 (P0/P1 partition + Precision/Recall/F1), Literature Review Quality (6-axis 0-100 with anti-inflation rules), SxS Overall Paper Quality (side-by-side), and SxS Literature Review Quality (side-by-side). TRIGGER when the user asks to "score this paper draft", "evaluate against the benchmark", "compare two papers", or "run the autoraters".
---

# Paper Autoraters (App. F.3)

Faithful implementation of the four LLM-as-judge autoraters used in
PaperOrchestra (Song et al., 2026, arXiv:2604.05018, §5 and App. F.3).

These are the metrics the paper uses to demonstrate that PaperOrchestra
beats single-agent and AI-Scientist-v2 baselines. Use them to:

1. Score a generated paper against a ground-truth paper.
2. Compare two paper-writing pipelines side-by-side.
3. Validate your own host-agent execution of the paper-orchestra pipeline.

## The four autoraters

| Autorater | What it does | Inputs | Output |
|---|---|---|---|
| **Citation F1 — P0/P1 partition** | Partitions reference list into P0 (must-cite) and P1 (good-to-cite) given the paper text | one paper text + its references list | JSON `{ref_num: "P0"\|"P1"}` |
| **Literature Review Quality** | 6-axis 0-100 score for Intro+Related Work, with anti-inflation hard caps | one paper PDF/text + reference avg citation count | JSON with `axis_scores`, `penalties`, `summary`, `overall_score` |
| **SxS Overall Paper Quality** | Holistic side-by-side preference judgment | two papers (PDF or text) | JSON with `winner` ∈ {paper_1, paper_2, tie} |
| **SxS Literature Review Quality** | Side-by-side preference, Intro+Related Work only | two papers | JSON with `winner` ∈ {paper_1, paper_2, tie} |

The paper uses Gemini-3.1-Pro and GPT-5 as judges, set to temperature 0.0
(Gemini) or default 1.0 (GPT-5, which doesn't allow temperature
adjustment). Use whatever your host LLM is.

## Workflow

### Citation F1 (compute Precision / Recall / F1 vs ground truth)

This is a two-step procedure:

#### Step 1: Partition the reference lists into P0 / P1

For both the ground-truth paper AND the generated paper, run the LLM with
`references/citation-f1-prompt.md`:

```
inputs:
  paper_text:    full paper LaTeX or markdown
  references_str: numbered reference list (e.g., "1. Vaswani et al. (2017)
                  Attention Is All You Need. NeurIPS. 2. He et al. (2016)
                  Deep Residual Learning for Image Recognition. CVPR. ...")

output: JSON {"1": "P0", "2": "P1", "3": "P0", ...}
```

Save both partitions:
- `bench/<paper_id>/gt_partition.json`
- `bench/<paper_id>/gen_partition.json`

#### Step 2: Resolve references to entity IDs and compute F1

The paper uses Semantic Scholar paper IDs to match references between the
two lists. The `compute_f1.py` script does this deterministically given
two input lists:

```bash
python skills/paper-autoraters/scripts/compute_f1.py \
    --gt-partition gt_partition.json \
    --gt-refs gt_refs.json \
    --gen-partition gen_partition.json \
    --gen-refs gen_refs.json \
    --out f1_report.json
```

Where `gt_refs.json` and `gen_refs.json` are lists of `{ref_num,
paper_id, title}` produced by your host's S2-resolution pass (the same
fuzzy match + S2 verification used by `literature-review-agent/scripts/`).

Output JSON contains P0 / P1 / overall Precision, Recall, F1.

### Literature Review Quality (single paper, 6 axes)

Load `references/litreview-quality-prompt.md`. Inputs:

- The full paper PDF (or LaTeX/markdown if your host lacks PDF input)
- `avg_citation_count` for the venue/field (used as the baseline for
  citation count anchoring, e.g., 58.52 for CVPR 2025, 59.18 for ICLR 2025
  per the paper)

The prompt instructs the model to evaluate ONLY the literature-review
function of the paper (Introduction + Related Work / Background sections).
It produces a strict JSON output with per-axis scores and justifications.

Critical anti-inflation rules baked into the prompt:

| Rule | Cap |
|---|---|
| Default expectation | overall 45-70 |
| > 85 requires strong evidence on ALL axes | — |
| > 90 extremely rare (near-survey-level mastery) | — |
| Any axis < 50 → overall rarely > 75 | — |
| Mostly descriptive review | Critical Analysis ≤ 60 |
| Novelty asserted without comparison | Positioning ≤ 60 |
| Sparse/inconsistent citations | Citation Rigor ≤ 60 |
| Citation count < 50% of avg | Coverage ≤ 55 |
| Citation count > 120% of avg | Coverage = "strong" |

Plus penalty table:

| Penalty | Range |
|---|---|
| Overclaiming novelty | -5 to -15 |
| Missing key recent work | -5 to -15 |
| Mostly descriptive review | -5 to -10 |
| Weak gap statements | -5 to -10 |
| Citation dumping | -5 to -10 |

Save the output to `litreview_quality_score.json`. The score JSON is the
same shape used by `content-refinement-agent/scripts/score_delta.py`, so
you can re-use the halt-rule logic to compare iterations.

### SxS Overall Paper Quality (side-by-side, full paper)

Load `references/sxs-paper-quality-prompt.md`. Inputs:

- Two paper PDFs or LaTeX files (call them `paper_1` and `paper_2`)

The prompt produces a JSON with `paper_1_holistic_analysis`,
`paper_2_holistic_analysis`, `comparison_justification`, and
`winner ∈ {paper_1, paper_2, tie}`.

To mitigate LLM positional bias (the paper notes this in §5.4), run the
comparison **twice** with the order swapped:

```
call_1: paper_A → paper_1, paper_B → paper_2  → winner1
call_2: paper_B → paper_1, paper_A → paper_2  → winner2
```

Final outcome: a `win` (both calls agree on paper A), `tie` (one win + one
tie, or two ties), or `loss` (both agree on paper B). The paper uses this
exact ordering protocol.

### SxS Literature Review Quality (side-by-side, Intro+RW only)

Load `references/sxs-litreview-prompt.md`. Same input/output shape as the
SxS paper quality autorater, but the model is instructed to evaluate
**only** the Introduction and Related Work / Background sections of each
paper. Same positional-bias mitigation: run twice, swap order.

## Resources

- `references/citation-f1-prompt.md`        — verbatim P0/P1 partition prompt from App. F.3
- `references/litreview-quality-prompt.md`  — verbatim 6-axis litreview rubric from App. F.3
- `references/sxs-paper-quality-prompt.md`  — verbatim SxS paper-quality prompt from App. F.3
- `references/sxs-litreview-prompt.md`      — verbatim SxS litreview prompt from App. F.3
- `scripts/compute_f1.py` — Precision / Recall / F1 from two partition JSONs
