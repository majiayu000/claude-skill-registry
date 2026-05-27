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
name: chemistry-agent
description: Autonomous chemical synthesis & analysis
keywords:
  - chemistry
  - synthesis
  - molecules
  - reaction
  - lab-automation
measurable_outcome: Successfully plans valid synthesis routes for 90% of target small molecules.
license: MIT
metadata:
  author: Biomedical OS Team
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
  - write_file
---

# Chemistry Agent

The Chemistry Agent is a specialized module for autonomous chemical reasoning, synthesis planning, and property prediction. It integrates with computational chemistry tools and potentially lab automation hardware.

## When to Use This Skill

*   When you need to design a synthesis route for a molecule.
*   When predicting chemical properties (solubility, toxicity).
*   When analyzing reaction mechanisms.

## Core Capabilities

1.  **Retrosynthesis**: Planning backward from target to starting materials.
2.  **Property Prediction**: Estimating physicochemical properties.
3.  **Reaction Optimization**: Suggesting optimal conditions.

## Example Usage

**User**: "Plan a synthesis route for Aspirin."

**Agent Action**:
```bash
python3 src/chemistry/main.py --target "Aspirin" --task "retrosynthesis"
```


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->