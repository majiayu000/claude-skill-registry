---name: st-agent
description: A multimodal LLM-based AI agent for deep spatial transcriptomics research, capable of dynamic code generation, visual reasoning, and literature retrieval.
license: MIT
metadata:
  author: LiuLab-Bioelectronics-Harvard
  source: "https://github.com/LiuLab-Bioelectronics-Harvard/STAgent"
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
  - framework: Scanpy, Sqidpy
allowed-tools:
  - run_shell_command
  - read_file
  - web_fetch

keywords:
  - stagent
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# STAgent (Spatial Transcriptomics Agent)

STAgent is a comprehensive agent designed to automate and enhance the analysis of spatial transcriptomics (ST) data. It leverages Large Language Models (LLMs) to bridge the gap between complex ST data and biological insights.

## When to Use This Skill

*   **Data Analysis**: When you need to analyze spatial transcriptomics datasets (e.g., 10x Visium, Xenium).
*   **Visual Reasoning**: When you need to interpret spatial plots, H&E images, or cluster maps.
*   **Code Generation**: When you need to generate Scanpy/Sqidpy code for custom analysis workflows.
*   **Hypothesis Generation**: When you want to generate biological hypotheses based on spatial gene expression patterns.

## Core Capabilities

1.  **Dynamic Code Generation**: Automatically generates and executes Python code for ST data processing (QC, clustering, spatial variable genes).
2.  **Visual Reasoning**: Analyzes spatial plots to identify tissue domains and cellular neighborhoods.
3.  **Literature Retrieval**: Fetches relevant literature to contextualize findings.
4.  **Report Generation**: Produces publication-quality reports summarizing the analysis.

## Workflow

1.  **Ingestion**: Load ST data (H5AD, Spaceranger output).
2.  **Plan**: The agent formulates an analysis plan (e.g., "Identify spatial domains and marker genes").
3.  **Execute**:
    *   Generates Python scripts using standard libraries (Scanpy, Sqidpy).
    *   Executes scripts to produce plots and tables.
4.  **Interpret**: The agent views generated plots and describes the biological significance.

## Example Usage

**User**: "Analyze this human breast cancer ST dataset. Identify the major spatial domains and check for immune cell infiltration."

**Agent Action**:
1.  Writes script to load data and run `sqidpy.gr.spatial_neighbors`.
2.  Runs clustering (Leiden) and generates a spatial scatter plot.
3.  Identifies clusters corresponding to tumor vs. stroma.
4.  Plots marker genes for immune cells (e.g., CD3D, CD19).
5.  Summarizes findings: "Cluster 3 represents the tumor core, while Cluster 5 shows high T-cell infiltration..."