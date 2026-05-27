---name: crispr-offtarget-predictor
description: Predicts potential off-target sites for a given sgRNA sequence using mismatch analysis.
license: MIT
metadata:
  author: BioKernel Team
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - run_shell_command

keywords:
  - crispr-prediction
  - automation
  - biomedical
measurable_outcome: execute task with >95% success rate.
---"

# CRISPR Off-Target Predictor

This skill identifies potential off-target binding sites for a specific sgRNA sequence. It helps researchers assess the specificity of their CRISPR design.

## When to Use This Skill

*   Designing new CRISPR experiments.
*   Validating sgRNA specificity before synthesis.
*   Analyzing potential safety risks in gene editing protocols.

## Core Capabilities

1.  **Mismatch Scoring**: Calculates mismatch penalties for potential sites.
2.  **PAM Validation**: Filters targets based on PAM (Protospacer Adjacent Motif) compatibility.
3.  **Risk Assessment**: Categorizes off-targets as Low, Medium, or High risk.

## Workflow

1.  **Input**: sgRNA sequence (20nt) and PAM (e.g., NGG).
2.  **Analysis**: Scans a reference library (mocked for this version) for similar sequences.
3.  **Output**: List of potential off-targets with locations and risk scores.

## Example Usage

**User**: "Check sgRNA 'GAGTCCGAGCAGAAGAAGAA' for off-targets."

**Agent Action**:
```bash
python3 Skills/Genomics/CRISPR_Prediction/impl.py --sequence GAGTCCGAGCAGAAGAAGAA --pam NGG
```
