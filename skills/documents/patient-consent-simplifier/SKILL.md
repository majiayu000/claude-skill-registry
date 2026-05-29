---
name: patient-consent-simplifier
description: Simplify informed consent documents into patient-friendly language while maintaining regulatory compliance (FDA 21CFR50, ICH-GCP, HIPAA) and required legal elements.
license: MIT
skill-author: AIPOCH
---
# Patient Consent Simplifier

Transform complex informed consent documents into patient-friendly language while maintaining regulatory compliance and ethical standards.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --text "Audit validation sample with explicit methods, findings, and conclusion."
```

## When to Use

- Use this skill when simplifying informed consent documents for clinical trials or medical procedures.
- Use this skill when adapting research summaries for lay audiences or patients with limited health literacy.
- Do not use this skill to remove required legal elements, downplay significant risks, or produce documents that bypass regulatory review.

## Workflow

1. **Sensitive Data Check:** Before processing, check whether the input document contains patient identifiers (name, DOB, MRN, address). If found, emit a mandatory warning: "This document appears to contain patient PII/PHI. Ensure the document has been de-identified or that you have authorization to process it before proceeding."
2. Confirm the input document, target reading level, and whether legal elements must be preserved.
3. Validate that the request is for consent simplification, not legal drafting or regulatory submission.
4. Apply simplification rules: break long sentences, replace jargon, use active voice, maintain required elements.
5. Assess readability and check compliance against required elements checklist.
6. Return the simplified document with a readability report and compliance status.
7. If inputs are incomplete, state which fields are missing and request only the minimum additional information.

## Usage

```text
# Simplify from text
python scripts/main.py --text "Lumbar puncture will be performed under sterile conditions..."

# Simplify from file
python scripts/main.py --input consent_form.pdf --output simplified_consent.pdf --target-grade 8

# Check compliance only
python scripts/main.py --input document.pdf --check compliance
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--input` | file path | No | Input consent document (PDF or text) |
| `--text` | string | No | Inline consent text to simplify |
| `--output` | file path | No | Output file path |
| `--target-grade` | integer | No | Target reading grade level (default: 8) |

## Target Reading Levels

- General population: 8th grade
- Vulnerable populations: 6th grade
- Health literacy challenges: 4th–5th grade

## Required Consent Elements (must be preserved)

Purpose of research · Procedures · Risks and discomforts · Benefits · Alternatives · Confidentiality · Compensation · Contact information · Voluntary participation

## Simplification Rules

- Break sentences longer than 20 words
- Replace medical jargon with common terms
- Use active voice and second person ("you")
- Add visual aid placeholders where appropriate
- Never remove required legal elements

## Stress-Case Rules

For complex multi-constraint requests, always include these explicit blocks:

1. Assumptions
2. Simplification Applied
3. Readability Report
4. Compliance Status
5. Risks and Limits

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate compliance status or remove legally required consent elements.

## Input Validation

This skill accepts: informed consent documents or text passages for readability simplification, with a target reading level and compliance preservation requirement.

If the request does not involve consent document simplification — for example, asking to draft new legal consent forms from scratch, provide regulatory legal advice, or simplify non-consent documents — do not proceed with the workflow. Instead respond:
> "patient-consent-simplifier is designed to simplify existing informed consent documents for patient readability while preserving regulatory compliance. Your request appears to be outside this scope. For drafting new consent forms, consult your institution's IRB template library or a regulatory affairs specialist. Please provide a consent document or text, or use a more appropriate tool."

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
