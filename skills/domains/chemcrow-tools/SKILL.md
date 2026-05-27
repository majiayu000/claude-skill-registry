---
name: chemcrow-tools
description: A production-grade cheminformatics toolkit for analyzing molecular properties, toxicity, and synthetic accessibility.
license: MIT
metadata:
  author: MD BABU MIA
  version: "2.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
---

# ChemCrow Tools

**ChemCrow Tools** provides a comprehensive suite of functions for drug discovery agents. It wraps RDKit (with safe fallbacks) to calculate properties, check Lipinski rules, and screen for toxicity.

## When to Use This Skill

*   When evaluating a candidate molecule for drug-likeness (Lipinski Rule of 5).
*   To check for toxic substructures (PAINS, Ames mutagenicity alerts).
*   To calculate molecular weight, LogP, and TPSA.
*   To estimate synthetic accessibility (SA Score).

## Core Capabilities

1.  **Property Calculation**: MolWt, LogP, TPSA, QED.
2.  **Safety Screening**: Detects toxicophores and PAINS.
3.  **Synthesizability**: Estimates how hard a molecule is to make.

## Workflow

1.  **Input**: Provide a valid SMILES string.
2.  **Analyze**: The tool runs a battery of RDKit descriptors and SMARTS pattern matching.
3.  **Output**: Returns a JSON report with properties and a recommendation.

## Example Usage

**User**: "Analyze the safety and properties of Aspirin."

**Agent Action**:
```bash
python3 Skills/Drug_Discovery/ChemCrow_Tools/chem_tools.py \
    --smiles "CC(=O)OC1=CC=CC=C1C(=O)O" \
    --output aspirin_analysis.json
```

