---name: cell_agent
description: LLM-driven multi-agent framework for automated single-cell analysis.
keywords:
  - scRNA-seq
  - scanpy
  - annotation
  - autonomous
  - bioinformatics
measurable_outcome: Achieves >85% accuracy in cell type annotation compared to manual curation on standard benchmarks.
license: MIT
metadata:
  author: Artificial Intelligence Group
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command
  - read_file
---"

# CellAgent

CellAgent is a multi-agent system capable of autonomously handling the entire single-cell RNA-seq (scRNA-seq) analysis pipeline. It simulates a team of biological experts to process data, annotate cells, and perform downstream analysis.

## When to Use This Skill

*   **Automated Annotation**: When you have raw scRNA-seq data and need cell type labels without manual curation.
*   **Complex Workflows**: For multi-step analysis (QC -> Clustering -> Annotation -> DE Analysis).
*   **Data Integration**: When merging multiple datasets (e.g., from different batches).

## Core Capabilities

1.  **Planning**: Decomposes analysis goals into executable steps.
2.  **Tool Execution**: Generates and runs Python code for Scanpy/Seurat.
3.  **Self-Correction**: detects errors in execution and attempts to fix them.

## Workflow

1.  **Input**: User query + scRNA-seq data (H5AD).
2.  **Planner**: The Planning Agent breaks the task into sub-tasks.
3.  **Executor**: The Coding Agent writes scripts to execute the plan.
4.  **Reviewer**: Checks the results and logs outputs.

## Example Usage

**User**: "Process this dataset, filter low-quality cells, and annotate clusters."

**Agent Action**:
```bash
# Assuming a wrapper exists or running the main module from the repo
python3 Skills/Genomics/Single_Cell/CellAgent/repo/main.py --data "./data.h5ad" --goal "annotate"
```

## References
-   *Mao et al., 2025*
-   *arXiv 2407.09811*
