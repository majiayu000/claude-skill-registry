---
name: medication-reconciliation
description: Compare patient pre-admission medication lists with inpatient orders to automatically identify omitted or duplicated medications and improve medication safety.
license: MIT
skill-author: AIPOCH
---
# Medication Reconciliation

Compare patient pre-admission medication lists with inpatient orders to automatically identify omitted or duplicated medications and improve medication safety.

> **Medical Disclaimer:** This tool is for reference only. Final medication decisions must be confirmed by qualified medical staff. All patient data must comply with applicable data protection regulations (e.g., HIPAA).

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## When to Use

- Use this skill when comparing pre-admission medication lists against inpatient orders to detect omissions or duplicates.
- Use this skill when generating structured reconciliation reports for clinical handover or pharmacy review.
- Do not use this skill as a substitute for pharmacist or physician review of medication orders.

## Workflow

1. **PHI Check:** Before processing, prompt the user to confirm data has been de-identified: "Please confirm that the input files have been de-identified or that you have authorization to process this patient data under applicable regulations (e.g., HIPAA) before proceeding."
2. Confirm patient ID, pre-admission medication list, and inpatient orders are available.
3. Validate that both input files are well-formed and patient IDs match.
4. Run the reconciliation script or apply the manual comparison path.
5. Return a structured report separating continued, discontinued, new, and duplicate medications.
6. **Dose-change detection:** When a drug appears in both lists with different dose strings, flag it as `dose_changed` with a warning: "Dose change detected — verify with prescribing physician before proceeding."
7. Flag warnings for critical drug classes (anticoagulants, hypoglycemics, antihypertensives, antiepileptics).
8. If inputs are incomplete, state exactly which fields are missing and request only the minimum additional information.

## Usage

```text
# Basic usage
python scripts/main.py --pre-admission pre_meds.json --inpatient orders.json --output report.json

# Use example data
python scripts/main.py --example

# Verbose output
python scripts/main.py --pre-admission pre_meds.json --inpatient orders.json --verbose
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--pre-admission` | file path | Yes | JSON file of pre-admission medications |
| `--inpatient` | file path | Yes | JSON file of inpatient orders |
| `--output` | file path | No | Output report path (default: stdout) |
| `--example` | flag | No | Run with built-in example data |
| `--verbose` | flag | No | Include detailed matching rationale |

## Output Format

The reconciliation report separates results into:
- `continued` — medications present in both lists (same drug, same dose)
- `dose_changed` — same drug present in both lists but with different dose strings (⚠️ requires physician verification)
- `discontinued` — pre-admission medications absent from inpatient orders
- `new_medications` — inpatient orders not in pre-admission list
- `duplicates` — same drug appearing multiple times
- `warnings` — critical drug class alerts

**Dose-change example:**
```json
{
  "dose_changed": [
    {
      "drug": "Metformin",
      "pre_admission_dose": "500mg",
      "inpatient_dose": "1000mg",
      "warning": "Dose change detected — verify with prescribing physician before proceeding."
    }
  ]
}
```

## Scope Boundaries

- This skill compares structured medication data; it does not interpret clinical appropriateness.
- This skill does not access live pharmacy systems or EHR databases.
- This skill does not replace pharmacist verification or physician sign-off.

## Stress-Case Rules

For complex multi-constraint requests, always include these explicit blocks:

1. Assumptions
2. Inputs Used
3. Reconciliation Result
4. Warnings and Critical Flags
5. Risks and Manual Checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate medication data, citations, or execution outcomes.

## Input Validation

This skill accepts: pre-admission medication lists and inpatient order files (JSON format) for a single patient encounter.

If the request does not involve medication list comparison — for example, asking to prescribe medications, interpret drug interactions clinically, or access live EHR systems — do not proceed with the workflow. Instead respond:
> "medication-reconciliation is designed to compare pre-admission and inpatient medication lists to flag omissions and duplicates. Your request appears to be outside this scope. Please provide structured medication input files, or use a more appropriate clinical tool."

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
