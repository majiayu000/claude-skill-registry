---
name: volcano-plot-script
description: Generate publication-ready R or Python volcano plot scripts from DEG analysis results with customizable thresholds, gene labeling, and color schemes.
license: MIT
skill-author: AIPOCH
---
# Volcano Plot Script Generator

Generate publication-ready volcano plots from differential gene expression (DEG) analysis results. Produces customizable R or Python scripts for high-quality figures.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Visualizing RNA-seq DEG results (DESeq2, edgeR, limma output)
- Identifying significantly up/downregulated genes by threshold
- Highlighting specific genes of interest with labels
- Generating publication-quality figures for manuscripts

## Usage

```bash
python scripts/main.py \
  --input deg_results.csv \
  --output volcano_plot.png \
  --log2fc-thresh 1.0 \
  --pvalue-thresh 0.05 \
  --top-n 10
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--input` | Yes | — | DEG results CSV/TSV file path |
| `--output` | No | volcano_plot.png | Output plot file path |
| `--log2fc-col` | No | log2FoldChange | Column name for log2 fold change |
| `--pvalue-col` | No | padj | Column name for p-value |
| `--gene-col` | No | gene | Column name for gene IDs |
| `--log2fc-thresh` | No | 1.0 | Log2 FC threshold for significance |
| `--pvalue-thresh` | No | 0.05 | P-value threshold |
| `--label-genes` | No | None | File with specific genes to label |
| `--top-n` | No | 10 | Label top N significant genes |
| `--color-up` | No | #E74C3C | Color for upregulated genes |
| `--color-down` | No | #3498DB | Color for downregulated genes |
| `--color-ns` | No | #95A5A6 | Color for non-significant genes |

## Input Format

Required CSV/TSV columns:
- Gene identifier (gene symbol or ENSEMBL ID)
- Log2 fold change values
- Adjusted or raw p-values

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing `--input`, malformed file), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : Ensure --input points to a valid CSV with log2FC and p-value columns
───────────────────────────────────────
```

> **Note:** `--input` is required. Passing a non-CSV string will cause exit code 1. Always validate the input file path before running.

## Output

- Publication-ready volcano plot (PNG/PDF/SVG)
- Customizable Python script
- Optional: labeled significant gene list
- **R Script Generation:** Use `--language r` to generate a ggplot2/ggrepel R script instead of Python. The R output uses `geom_point()` for the scatter plot and `ggrepel::geom_text_repel()` for gene labels.

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced (including all non-default column names and any gene list file used)
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- **NaN p-values:** If NaN values are detected in the p-value column, emit a warning: "Warning: [N] genes have NaN p-values and will be plotted as non-significant."
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts: DEG results tables (CSV/TSV) with log2 fold change and p-value columns for generating volcano plot scripts and figures.

If the request does not involve volcano plot generation — for example, asking to perform DEG analysis, run pathway enrichment, or generate heatmaps — do not proceed. Instead respond:

> "volcano-plot-script is designed to generate volcano plot scripts from DEG results. Your request appears to be outside this scope. Please provide a DEG results CSV with log2FC and p-value columns, or use a more appropriate tool for your task."

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## References

- [Example datasets and templates](references/)

## Prerequisites

```bash
pip install -r requirements.txt
# Python: pandas, matplotlib, seaborn, numpy
# R (optional): ggplot2, dplyr, ggrepel
```
