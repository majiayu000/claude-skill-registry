---
name: crispr-design-agent
description: A specialized tool for designing efficient and specific gRNA sequences for CRISPR-Cas9 experiments.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
---

# CRISPR Design Agent

The **CRISPR Design Agent** automates the selection of guide RNAs (gRNAs) for gene editing. It scans DNA sequences for PAM sites, extracts spacers, and scores them based on efficiency rules (GC content, homopolymers).

## When to Use This Skill

*   When designing a CRISPR knockout or knock-in experiment.
*   To find all valid Cas9 target sites in a given DNA sequence.
*   To filter gRNAs by efficiency scores.

## Core Capabilities

1.  **Target Discovery**: Identifies NGG PAM sites.
2.  **Efficiency Scoring**: Calculates scores based on GC content and sequence features.
3.  **Filtering**: Sorts guides by predicted efficacy.

## Workflow

1.  **Input**: Provide a DNA sequence (raw string or FASTA file) and target gene name.
2.  **Process**: The agent scans the sequence and applies scoring logic.
3.  **Output**: Returns a ranked list of gRNA sequences with coordinates and scores.

## Example Usage

**User**: "Find gRNAs for this sequence: ATCG..."

**Agent Action**:
```bash
python3 Skills/Genomics/CRISPR_Design_Agent/crispr_designer.py \
    --sequence "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTGTGAGTGGATCCATTGGAAGGGC" \
    --output guides.json
```

