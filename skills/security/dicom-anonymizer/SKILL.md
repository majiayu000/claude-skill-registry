---
name: dicom-anonymizer
description: De-identify DICOM medical images by removing PHI tags for research sharing, with audit logging and study-linkage preservation support.
license: MIT
skill-author: AIPOCH
---
# DICOM Anonymizer

Structured DICOM de-identification support for research preparation workflows.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/smoke_test.py
```

## When to Use

- Prepare imaging data for research sharing
- Batch-anonymize DICOM folders while preserving study linkage
- Review whether a workflow still needs manual PHI QA
- Generate audit logs for compliance documentation

## Workflow

1. Confirm the input type, output target, batch needs, and whether study linkage must be preserved.
2. Check whether the request is asking for script execution, audit-log planning, or a manual anonymization checklist.
3. Use the packaged script for supported local workflows; if dependencies or files are missing, provide a bounded fallback rather than claiming successful anonymization.
4. Return the anonymization plan or result with assumptions, preserved identifiers, and remaining manual QA requirements.
5. If the request exceeds supported scope, stop and state the specific boundary.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--input`, `-i` | string | Yes | - | Input DICOM file or directory |
| `--output`, `-o` | string | Yes | - | Output DICOM file or directory |
| `--batch`, `-b` | flag | No | false | Enable directory processing |
| `--preserve-studies` | flag | No | false | Preserve study linkage with pseudonyms |
| `--keep-tags` | string | No | - | Comma-separated tags to preserve |
| `--remove-private` | flag | No | true | Remove private tags |
| `--audit-log`, `-a` | string | No | - | Optional JSON audit log path |
| `--overwrite` | flag | No | false | Allow overwriting output files |

## Usage

```bash
# Single file
python scripts/main.py --input scan.dcm --output anonymized.dcm

# Batch directory
python scripts/main.py --input ./dicoms/ --output ./anon/ --batch --preserve-studies

# With audit log
python scripts/main.py --input scan.dcm --output anon.dcm --audit-log audit.json

# Keep specific tags
python scripts/main.py --input scan.dcm --output anon.dcm --keep-tags "PatientAge,StudyDate"
```

## Returns

- Anonymized DICOM artifact or bounded execution plan
- Summary of preserved and anonymized identifiers
- Explicit reminder of remaining QA steps before external release

## Scope Boundaries

- Supports DICOM de-identification workflows, not legal certification
- Does not remove burned-in image annotations from pixel data
- Does not replace institutional privacy review or release approval
- **De-anonymization is not supported:** SHA-256 hashing used for PHI values is a one-way operation by design. Original patient data cannot be recovered from anonymized files. If you need to trace back to original data, consult your institutional data governance office before anonymizing.

## De-anonymization Requests

If asked to recover original patient data or reverse anonymization, respond:
> "Anonymization performed by this tool is irreversible by design. PHI values are replaced using one-way SHA-256 hashing — the original data is not retained by this tool and cannot be recovered. If you need access to the original patient data, contact your institutional data governance or privacy office."

## Stress-Case Rules

For complex requests, always include these blocks:

1. Assumptions
2. Hard Constraints
3. Anonymization Path
4. Residual PHI Risks
5. Manual QA Before Release

## Input Validation

This skill accepts requests involving DICOM anonymization, PHI-tag removal, research export preparation, or audit-log planning for medical images.

If the user's request does not involve DICOM de-identification — for example, asking to diagnose from images, convert image formats unrelated to PHI removal, or certify HIPAA compliance — do not proceed with the workflow. Instead respond:
> "dicom-anonymizer is designed to support DICOM de-identification workflows for research preparation. Your request appears to be outside this scope. Please provide a DICOM input path and output target, or use a more appropriate tool for your task."

## References

- [references/phi_tags.json](references/phi_tags.json) — PHI-related DICOM tags used by the packaged workflow
- [references/audit-reference.md](references/audit-reference.md) — Supported scope, audit commands, and fallback boundaries

## Output Requirements

Every final response must include:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks
