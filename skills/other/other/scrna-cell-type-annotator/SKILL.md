---
name: scrna-cell-type-annotator
description: Auto-annotate cell clusters from single-cell RNA data using marker genes, tissue context, and species-specific reference databases.
license: MIT
skill-author: AIPOCH
status: beta
---
# ScRNA Cell Type Annotator

Automatically annotate cell clusters from scRNA-seq data using marker gene signatures, tissue context, and species-specific references.

## Input Validation

This skill accepts: per-cluster marker gene lists from scRNA-seq experiments, with tissue type and species context, for automated cell type annotation.

If the request does not involve scRNA-seq cluster annotation — for example, asking to perform bulk RNA-seq DEG analysis, run clustering from raw counts, or interpret proteomics data — do not proceed. Instead respond:

> "scrna-cell-type-annotator is designed to annotate cell clusters from single-cell RNA data using marker genes. Your request appears to be outside this scope. Please provide cluster marker lists with tissue and species context, or use a more appropriate tool for your task. For clustering from raw counts, use Seurat or Scanpy preprocessing pipelines."

## When to Use

- Post-clustering annotation of Seurat/Scanpy clusters
- Novel cell type discovery in unexplored tissues
- Cross-study comparison of cell type compositions
- Cell atlas construction and harmonization

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## Workflow

1. **Validate input first** — confirm the request involves scRNA-seq cluster annotation before any processing. Refuse out-of-scope requests immediately.
2. Confirm objective, required inputs, and constraints before proceeding.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--markers` | Yes | DEG marker list per cluster (CSV or JSON) |
| `--tissue` | Yes | Organ/tissue context (e.g., "PBMC", "liver") |
| `--species` | Yes | "human" or "mouse" |
| `--top-n` | No | Top N markers per cluster to use (default: 20) |

## Marker Database Coverage

The built-in marker database covers 6 PBMC immune cell types (T cells, B cells, NK cells, monocytes, dendritic cells, macrophages). For non-immune or non-PBMC tissues:

- Liver, lung, brain, and other tissue-specific markers are not in the built-in database
- The skill will flag clusters as "novel/unresolved" and provide next-step guidance
- For tissue-specific annotation, provide a custom marker file or reference CellMarker/PanglaoDB

The `--tissue` and `--species` parameters are accepted but currently route to the same PBMC-focused database. Tissue-specific routing is a planned enhancement — the script must be updated to load tissue-specific marker dictionaries (e.g., liver, lung, brain) and route based on the `--tissue` argument.

**Path validation:** If the `--markers` path contains `../` or resolves outside the workspace, reject with a path traversal warning and exit with code 1.

## Returns

- Cell type predictions per cluster with top supporting markers
- Confidence levels (High / Medium / Low)
- Alternative cell type suggestions where ambiguous
- Clusters flagged as novel or unresolved

## Fallback Template

If `scripts/main.py` cannot run (missing inputs, environment error), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : <minimum action to unblock>
───────────────────────────────────────
```

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the `--markers` path contains `../` or resolves outside the workspace, reject with a path traversal warning.
- If the task goes outside documented scope, stop immediately — do not attempt partial analysis before refusing.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

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

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python scripts executed locally | Medium |
| Network Access | No external API calls | Low |
| File System Access | Read marker input, write annotation output | Medium |
| Data Exposure | Output files saved to workspace | Low |

## Prerequisites

```bash
pip install -r requirements.txt
```
