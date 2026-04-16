---
name: paper-writing
description: "Workflow 3: Full paper writing pipeline. Orchestrates paper-plan → paper-figure → figure-spec/paper-illustration/mermaid-diagram → paper-write → paper-compile → auto-paper-improvement-loop to go from a narrative report to a polished, submission-ready PDF. Use when user says \"写论文全流程\", \"write paper pipeline\", \"从报告到PDF\", \"paper writing\", or wants the complete paper generation workflow."
argument-hint: [narrative-report-path-or-topic]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Workflow 3: Paper Writing Pipeline

Orchestrate a complete paper writing workflow for: **$ARGUMENTS**

## Overview

This skill chains five sub-skills into a single automated pipeline:

```
/paper-plan → /paper-figure → /paper-write → /paper-compile → /auto-paper-improvement-loop
  (outline)     (plots)        (LaTeX)        (build PDF)       (review & polish ×2)
```

Each phase builds on the previous one's output. The final deliverable is a polished, reviewed `paper/` directory with LaTeX source and compiled PDF.

In this hybrid pack, the pipeline itself is unchanged, but `paper-plan` and `paper-write` use Orchestra-adapted shared references for stronger story framing and prose guidance.

## Constants

- **VENUE = `ICLR`** — Target venue. Options: `ICLR`, `NeurIPS`, `ICML`, `CVPR`, `ACL`, `AAAI`, `ACM`, `IEEE_JOURNAL` (IEEE Transactions / Letters), `IEEE_CONF` (IEEE conferences). Affects style file, page limit, citation format.
- **MAX_IMPROVEMENT_ROUNDS = 2** — Number of review→fix→recompile rounds in the improvement loop.
- **REVIEWER_MODEL = `gpt-5.4`** — Model used via Codex MCP for plan review, figure review, writing review, and improvement loop.
- **AUTO_PROCEED = true** — Auto-continue between phases. Set `false` to pause and wait for user approval after each phase.
- **HUMAN_CHECKPOINT = false** — When `true`, the improvement loop (Phase 5) pauses after each round's review to let you see the score and provide custom modification instructions. When `false` (default), the loop runs fully autonomously. Passed through to `/auto-paper-improvement-loop`.
- **ILLUSTRATION = `figurespec`** — Architecture/illustration generator for Phase 2b: `figurespec` (default, deterministic JSON→SVG via `/figure-spec`, best for architecture/workflow/topology), `gemini` (AI-generated via `/paper-illustration`, best for qualitative method illustrations; needs `GEMINI_API_KEY`), `mermaid` (Mermaid syntax via `/mermaid-diagram`, free, best for flowcharts), or `false` (skip Phase 2b, manual only).

> Override inline: `/paper-writing "NARRATIVE_REPORT.md" — venue: NeurIPS, illustration: gemini, human checkpoint: true`
> IEEE example: `/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL`

## Inputs

This pipeline accepts one of:

1. **`NARRATIVE_REPORT.md`** (best) — structured research narrative with claims, experiments, results, figures
2. **Research direction + experiment results** — the skill will help draft the narrative first
3. **Existing `PAPER_PLAN.md`** — skip Phase 1, start from Phase 2

The more detailed the input (especially figure descriptions and quantitative results), the better the output.

## Pipeline

### Phase 1: Paper Plan

Invoke `/paper-plan` to create the structural outline:

```
/paper-plan "$ARGUMENTS"
```

**What this does:**
- Parse NARRATIVE_REPORT.md for claims, evidence, and figure descriptions
- Build a **Claims-Evidence Matrix** — every claim maps to evidence, every experiment supports a claim
- Design section structure (5-8 sections depending on paper type)
- Plan figure/table placement with data sources
- Scaffold citation structure
- GPT-5.4 reviews the plan for completeness

**Output:** `PAPER_PLAN.md` with section plan, figure plan, citation scaffolding.

**Checkpoint:** Present the plan summary to the user.

```
📐 Paper plan complete:
- Title: [proposed title]
- Sections: [N] ([list])
- Figures: [N] auto-generated + [M] manual
- Target: [VENUE], [PAGE_LIMIT] pages

Shall I proceed with figure generation?
```

- **User approves** (or AUTO_PROCEED=true) → proceed to Phase 2.
- **User requests changes** → adjust plan and re-present.

### Phase 2: Figure Generation

Invoke `/paper-figure` to generate data-driven plots and tables:

```
/paper-figure "PAPER_PLAN.md"
```

**What this does:**
- Read figure plan from PAPER_PLAN.md
- Generate matplotlib/seaborn plots from JSON/CSV data
- Generate LaTeX comparison tables
- Create `figures/latex_includes.tex` for easy insertion
- GPT-5.4 reviews figure quality and captions

**Output:** `figures/` directory with PDFs, generation scripts, and LaTeX snippets.

> **Scope:** `paper-figure` covers data plots and comparison tables. Architecture diagrams, pipeline figures, and method illustrations are handled in Phase 2b below.

#### Phase 2b: Architecture & Illustration Generation

**Skip this step entirely if `illustration: false`.**

If the paper plan includes architecture diagrams, pipeline figures, audit cascades, or method illustrations, invoke the appropriate generator based on the `illustration` parameter:

**When `illustration: figurespec`** (default) — invoke `/figure-spec`:
```
/figure-spec "[architecture/workflow description from PAPER_PLAN.md]"
```
- Deterministic JSON → SVG vector rendering (editable, reproducible)
- Best for: system architecture, workflow pipelines, audit cascades, layered topology
- Output: `figures/*.svg` + `figures/*.pdf` (via rsvg-convert) + `figures/specs/*.json`
- No external API, runs fully local

**When `illustration: gemini`** — invoke `/paper-illustration`:
```
/paper-illustration "[method description from PAPER_PLAN.md or NARRATIVE_REPORT.md]"
```
- Claude plans → Gemini optimizes → Nano Banana Pro renders → Claude reviews (score ≥ 9)
- Best for: qualitative method illustrations, natural-style diagrams, result grids
- Output: `figures/ai_generated/*.png`
- Requires `GEMINI_API_KEY` environment variable

**When `illustration: mermaid`** — invoke `/mermaid-diagram`:
```
/mermaid-diagram "[method description from PAPER_PLAN.md]"
```
- Generates Mermaid syntax diagrams (flowchart, sequence, class, state, etc.)
- Best for: lightweight flowcharts, state machines, simple sequence diagrams
- Output: `figures/*.mmd` + `figures/*.png`
- Free, no API key needed

**When `illustration: false`** — skip entirely. All non-data figures must be created manually (draw.io, Figma, TikZ) and placed in `figures/` before Phase 3.

**Choosing the right mode:**
- Formal architecture / workflow / topology figures → `figurespec` (default)
- Method concept illustrations with natural style → `gemini`
- Quick flowchart / state machine → `mermaid`
- Full manual control → `false`

These are complementary, not mutually exclusive: you can run multiple generators for different figures in the same paper by re-invoking with different `illustration` overrides.

**Checkpoint:** List generated vs manual figures.

```
📊 Figures complete:
- Data plots (auto, Phase 2): [list]
- Architecture/illustrations (auto, Phase 2b, mode=<illustration>): [list]
- Manual (need your input): [list]
- LaTeX snippets: figures/latex_includes.tex

[If manual figures needed]: Please add them to figures/ before I proceed.
[If all auto]: Shall I proceed with LaTeX writing?
```

### Phase 3: LaTeX Writing

Invoke `/paper-write` to generate section-by-section LaTeX:

```
/paper-write "PAPER_PLAN.md"
```

**What this does:**
- Write each section following the plan, with proper LaTeX formatting
- Insert figure/table references from `figures/latex_includes.tex`
- Build `references.bib` from citation scaffolding
- Clean stale files from previous section structures
- Automated bib cleaning (remove uncited entries)
- De-AI polish (remove "delve", "pivotal", "landscape"...)
- GPT-5.4 reviews each section for quality

**Output:** `paper/` directory with `main.tex`, `sections/*.tex`, `references.bib`, `math_commands.tex`.

**Checkpoint:** Report section completion.

```
✍️ LaTeX writing complete:
- Sections: [N] written ([list])
- Citations: [N] unique keys in references.bib
- Stale files cleaned: [list, if any]

Shall I proceed with compilation?
```

### Phase 4: Compilation

Invoke `/paper-compile` to build the PDF:

```
/paper-compile "paper/"
```

**What this does:**
- `latexmk -pdf` with automatic multi-pass compilation
- Auto-fix common errors (missing packages, undefined refs, BibTeX syntax)
- Up to 3 compilation attempts
- Post-compilation checks: undefined refs, page count, font embedding
- Precise page verification via `pdftotext`
- Stale file detection

**Output:** `paper/main.pdf`

**Checkpoint:** Report compilation results.

```
🔨 Compilation complete:
- Status: SUCCESS
- Pages: [X] (main body) + [Y] (references) + [Z] (appendix)
- Within page limit: YES/NO
- Undefined references: 0
- Undefined citations: 0

Shall I proceed with the improvement loop?
```

### Phase 4.5: Proof Verification (theory papers only)

**Skip this phase if the paper contains no theorems, lemmas, or proofs.**

```
if paper contains \begin{theorem} or \begin{lemma} or \begin{proof}:
    Run /proof-checker "paper/"
    This invokes GPT-5.4 xhigh to:
    - Verify all proof steps (hypothesis discharge, interchange justification, etc.)
    - Check for logic gaps, quantifier errors, missing domination conditions
    - Attempt counterexamples on key lemmas
    - Generate PROOF_AUDIT.md with issue list + severity

    If FATAL or CRITICAL issues found:
        Fix before proceeding to improvement loop
    If only MAJOR/MINOR:
        Proceed, improvement loop may address remaining issues
else:
    skip — no proofs, no action
```

### Phase 4.7: Paper Claim Audit

**Skip if no result files exist (e.g., survey/position papers with no experiments).**

```
if results/*.json or results/*.csv or outputs/*.json exist:
    Run /paper-claim-audit "paper/"
    Fresh zero-context reviewer compares every number in the paper
    against raw result files. Catches rounding inflation, best-seed
    cherry-pick, config mismatch, delta errors.

    If FAIL:
        Fix mismatched numbers before improvement loop
    If WARN:
        Proceed, but flag for manual verification
else:
    skip — no experimental results to verify
```

### Phase 5: Auto Improvement Loop

Invoke `/auto-paper-improvement-loop` to polish the paper:

```
/auto-paper-improvement-loop "paper/"
```

**What this does (2 rounds):**

**Round 1:** GPT-5.4 xhigh reviews the full paper → identifies CRITICAL/MAJOR/MINOR issues → Claude Code implements fixes → recompile → save `main_round1.pdf`

**Round 2:** GPT-5.4 xhigh re-reviews with conversation context → identifies remaining issues → Claude Code implements fixes → recompile → save `main_round2.pdf`

**Typical improvements:**
- Fix assumption-model mismatches
- Soften overclaims to match evidence
- Add missing interpretations and notation
- Strengthen limitations section
- Add theory-aligned experiments if needed

**Output:** Three PDFs for comparison + `PAPER_IMPROVEMENT_LOG.md`.

**Format check** (included in improvement loop Step 8): After final recompilation, auto-detect and fix overfull hboxes (content exceeding margins), verify page count vs venue limit, and ensure compact formatting. Location-aware thresholds: any main-body overfull blocks completion regardless of size; appendix overfulls block only if >10pt; bibliography overfulls block only if >20pt.

### Phase 5.5: Final Paper Claim Audit (MANDATORY submission gate)

After `/auto-paper-improvement-loop` finishes, **rerun** `/paper-claim-audit` before the final report whenever the paper contains numeric claims and machine-readable raw result files exist.

Use the same detectors as Phase 4.7:
- numeric-claim regex over `paper/main.tex` and `paper/sections/*.tex`
- raw-evidence file search in `results/`, `outputs/`, `experiments/`, and `figures/` for `.json`, `.jsonl`, `.csv`, `.tsv`, `.yaml`, or `.yml`

This phase is **mandatory** if both detectors are positive. It blocks the final report.
If numeric claims exist but no raw result files are found, stop and warn the user before declaring the paper complete.
If no numeric claims exist, skip.

```bash
NUMERIC_CLAIMS=$(rg -n -e '[0-9]+(\.[0-9]+)?\s*(%|\\%|±|\\pm|x|×)' \
  -e '(accuracy|BLEU|F1|AUC|mAP|top-1|top-5|error|loss|perplexity|speedup|improvement)' \
  paper/main.tex paper/sections 2>/dev/null || true)

RAW_RESULT_FILES=$(find results outputs experiments figures -type f \
  \( -name '*.json' -o -name '*.jsonl' -o -name '*.csv' -o -name '*.tsv' -o -name '*.yaml' -o -name '*.yml' \) 2>/dev/null | head -200)

if [ -n "$NUMERIC_CLAIMS" ] && [ -n "$RAW_RESULT_FILES" ]; then
    Run /paper-claim-audit "paper/"
    If FAIL:
        Fix mismatched numbers before the final report
elif [ -n "$NUMERIC_CLAIMS" ]; then
    Stop and warn: the paper contains numeric claims but no raw evidence files were found
fi
```

**Empirical motivation:** in our April 2026 NeurIPS run, the final paper claimed `w ∈ {0,1,2,3}` for the width-tradeoff experiment but the raw JSON had `w ∈ {0,1,2,3,4,5}`. The crossing-point tolerance was claimed as `0.05%` but the actual relative error was `0.0577%`. Both were caught only after manual `paper-claim-audit` invocation in the final round; the improvement loop did not detect them.

### Phase 6: Final Report

```markdown
# Paper Writing Pipeline Report

**Input**: [NARRATIVE_REPORT.md or topic]
**Venue**: [ICLR/NeurIPS/ICML/CVPR/ACL/AAAI/ACM/IEEE_JOURNAL/IEEE_CONF]
**Date**: [today]

## Pipeline Summary

| Phase | Status | Output |
|-------|--------|--------|
| 1. Paper Plan | ✅ | PAPER_PLAN.md |
| 2. Figures | ✅ | figures/ ([N] auto + [M] manual) |
| 3. LaTeX Writing | ✅ | paper/sections/*.tex ([N] sections, [M] citations) |
| 4. Compilation | ✅ | paper/main.pdf ([X] pages) |
| 5. Improvement | ✅ | [score0]/10 → [score2]/10 |

## Improvement Scores
| Round | Score | Key Changes |
|-------|-------|-------------|
| Round 0 | X/10 | Baseline |
| Round 1 | Y/10 | [summary] |
| Round 2 | Z/10 | [summary] |

## Deliverables
- paper/main.pdf — Final polished paper
- paper/main_round0_original.pdf — Before improvement
- paper/main_round1.pdf — After round 1
- paper/main_round2.pdf — After round 2
- paper/PAPER_IMPROVEMENT_LOG.md — Full review log

## Remaining Issues (if any)
- [items from final review that weren't addressed]

## Next Steps
- [ ] Visual inspection of PDF
- [ ] Add any missing manual figures
- [ ] Submit to [venue] via OpenReview / CMT / HotCRP
```

## Output Protocols

> Follow these shared protocols for all output files:
> - **[Output Versioning Protocol](../shared-references/output-versioning.md)** — write timestamped file first, then copy to fixed name
> - **[Output Manifest Protocol](../shared-references/output-manifest.md)** — log every output to MANIFEST.md
> - **[Output Language Protocol](../shared-references/output-language.md)** — note: paper-writing always outputs English LaTeX for venue submission

## Key Rules

- **Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.
- **Don't skip phases.** Each phase builds on the previous one — skipping leads to errors.
- **Checkpoint between phases** when AUTO_PROCEED=false. Present results and wait for approval.
- **Manual figures first.** If the paper needs architecture diagrams or qualitative results, the user must provide them before Phase 3.
- **Compilation must succeed** before entering the improvement loop. Fix all errors first.
- **Preserve all PDFs.** The user needs round0/round1/round2 for comparison.
- **Document everything.** The pipeline report should be self-contained.
- **Respect page limits.** If the paper exceeds the venue limit, suggest specific cuts before the improvement loop.

## Composing with Other Workflows

```
/idea-discovery "direction"         ← Workflow 1: find ideas
implement                           ← write code
/run-experiment                     ← deploy experiments
/auto-review-loop "paper topic"     ← Workflow 2: iterate research
/paper-writing "NARRATIVE_REPORT.md"  ← Workflow 3: you are here
                                         submit! 🎉

Or use /research-pipeline for the Workflow 1+2 end-to-end flow,
then /paper-writing for the final writing step.
```

## Typical Timeline

| Phase | Duration | Can sleep? |
|-------|----------|------------|
| 1. Paper Plan | 5-10 min | No |
| 2. Figures | 5-15 min | No |
| 3. LaTeX Writing | 15-30 min | Yes ✅ |
| 4. Compilation | 2-5 min | No |
| 5. Improvement | 15-30 min | Yes ✅ |

**Total: ~45-90 min** for a full paper from narrative report to polished PDF.
