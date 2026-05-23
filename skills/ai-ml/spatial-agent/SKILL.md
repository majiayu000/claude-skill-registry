<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

---
name: 'spatial-agent'
description: 'An agent that interprets spatial transcriptomics data to propose mechanistic hypotheses and analyze tissue organization.'
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - read_file
  - run_shell_command
---


# SpatialAgent

SpatialAgent focuses on the biological interpretation of spatial transcriptomics data, specifically aiming to propose mechanistic hypotheses about tissue organization and cellular interactions.

## When to Use This Skill

*   **Mechanistic Interpretation**: When you have clusters or spatial domains and need to understand *why* they are organized that way.
*   **Cell-Cell Interaction**: To predict and interpret ligand-receptor interactions in a spatial context.
*   **Hypothesis Generation**: To propose biological mechanisms driving the observed spatial heterogeneity.

## Core Capabilities

1.  **Tissue Organization Analysis**: Decodes the structural logic of tissues (e.g., layers, niches).
2.  **Cellular Interaction Prediction**: Identifies potential signaling pathways active at domain boundaries.
3.  **Hypothesis Proposal**: Generates testable biological hypotheses based on spatial data.

## Workflow

1.  **Input Analysis**: Accepts processed ST data (e.g., cluster annotations, DEG lists per spatial domain).
2.  **Knowledge Retrieval**: Queries biological knowledge bases regarding the observed cell types and genes.
3.  **Synthesis**: Constructs a narrative explaining the spatial arrangement (e.g., "The proximity of fibroblasts and tumor cells suggests a desmoplastic reaction mediated by TGF-beta signaling...").

## Example Usage

**User**: "Why are the macrophages located at the boundary of the tumor core in this sample?"

**Agent Action**:
1.  Analyzes the gene expression of macrophages and adjacent tumor cells.
2.  Checks for ligand-receptor pairs (e.g., CSF1-CSF1R).
3.  Proposes: "Macrophages are likely recruited by CSF1 secreted by the tumor cells, forming an immunosuppressive barrier..."


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->