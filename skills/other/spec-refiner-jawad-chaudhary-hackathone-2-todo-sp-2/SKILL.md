---
name: spec-refiner
description: Iterate on specs for better code generation. Use when Claude output needs refinement.
---
# SpecRefiner Instructions
Input: Initial spec.md, error/feedback.
Output: Updated spec.md.
Steps:
1. Read current spec.
2. Apply changes (e.g., add error handling).
3. Run script: python {baseDir}/scripts/refine_spec.py <spec_path> <feedback>