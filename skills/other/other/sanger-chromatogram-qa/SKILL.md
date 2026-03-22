---
name: sanger-chromatogram-qa
description: Assess Sanger sequencing chromatogram quality, detect mixed peaks, confirm variants, and flag samples requiring repeat sequencing.
license: MIT
skill-author: AIPOCH
status: beta
---
# Sanger Chromatogram QA

Quality assessment for Sanger sequencing chromatograms: mixed-peak detection, variant confirmation, and repeat-sequencing recommendations.

## Input Validation

This skill accepts: `.ab1` chromatogram files paired with a reference sequence, optionally with a variant position, for Sanger sequencing quality assessment.

If the request does not involve Sanger chromatogram QA — for example, asking to analyze NGS FASTQ files, perform de-novo assembly, or interpret mass spectrometry data — do not proceed. Instead respond:

> "sanger-chromatogram-qa is designed to assess Sanger sequencing chromatogram quality. Your request appears to be outside this scope. Please provide an .ab1 file and reference sequence, or use a more appropriate tool for your task. For NGS FASTQ analysis, consider FastQC or a dedicated variant calling pipeline."

## When to Use

- Mutation verification after Sanger sequencing
- Clone confirmation (correct insert, correct orientation)
- Genotyping QC (heterozygous vs homozygous calls)
- SNP validation against a reference sequence

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo
```

## Workflow

1. **Validate input first** — confirm the request involves `.ab1` + reference before any processing. Refuse out-of-scope requests immediately.
2. Confirm objective, required inputs, and constraints before proceeding.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--ab1` | Yes | Path to .ab1 chromatogram file |
| `--reference` | Yes | Reference sequence (FASTA or plain string) |
| `--variant-pos` | No | Expected mutation site (1-based position) |

## Returns

- Per-base quality scores and trace summary
- Mixed-peak detection with position and severity
- Variant confirmation (match / mismatch / ambiguous)
- Repeat-sequencing recommendation (Yes / No / Conditional)

**Mixed-peak severity:** When heterozygous SNP detection is requested, the output must include a quantitative severity estimate (secondary peak height as a fraction of primary peak, 0–1 scale). Note: `detect_mixed_signals` is currently a placeholder returning 0. Until BioPython ab1 parsing is implemented (using `Bio.SeqIO.read` with `'abi'` format, detecting positions where secondary peak height exceeds 25% of primary), report this limitation explicitly and provide qualitative guidance based on available trace data.

**Path validation:** If the `--ab1` path contains `../` or resolves outside the workspace, reject with a path traversal warning and exit with code 1.

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
- If the `--ab1` path contains `../` or resolves outside the workspace, reject with a path traversal warning.
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
| File System Access | Read .ab1 input, write output files | Medium |
| Data Exposure | Output files saved to workspace | Low |

## Prerequisites

```bash
pip install -r requirements.txt
```
