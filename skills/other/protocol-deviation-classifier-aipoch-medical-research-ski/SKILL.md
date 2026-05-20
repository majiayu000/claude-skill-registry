---
name: protocol-deviation-classifier
description: Classify clinical trial protocol deviations as major or minor based on GCP/ICH E6 guidelines, assessing impact on subject safety, data integrity, and scientific validity.
license: MIT
skill-author: AIPOCH
---

# Protocol Deviation Classifier

Clinical trial protocol deviation classification tool. Based on GCP and ICH E6 guidelines, automatically determines whether deviations are "major" or "minor" and generates regulatory-ready reports.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py classify --description "Subject visit delayed by 2 days" --type "Visit Window"
python scripts/main.py batch --input deviations.json --output report.json
```

## When to Use

- Classify a clinical trial protocol deviation as major or minor
- Generate deviation reports that meet GCP/ICH E6/FDA/EMA regulatory requirements
- Batch-process deviation lists from a JSON file
- Assess multi-dimensional impact (safety, data integrity, scientific validity)

## Workflow

1. Confirm the deviation description, type, and severity factors before proceeding.
2. Validate that the request is a clinical trial deviation classification task; stop early if not.
3. Run `scripts/main.py classify` (single) or `scripts/main.py batch` (bulk) with available inputs.
4. Return a structured result separating classification, rationale, regulatory basis, and recommended actions.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <classification goal>
Inputs Available : <list what was provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any classification that can be made safely>
Blocked Steps    : <what could not be completed and why>
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Deviation Classification Standards

### Major / Critical Deviation

| Category | Examples |
|---|---|
| Informed Consent | Procedures without consent; expired/incorrect consent forms |
| Inclusion/Exclusion | Enrolling ineligible subjects |
| Investigational Product | Overdose, contraindicated concomitant medication, randomization error |
| Safety | Missing SAE/SUSAR reports, delayed reporting |
| Blinding | Unauthorized unblinding |
| Data Integrity | Falsified/fabricated data, systematic missing critical data |
| Prohibited Operations | Violating key protocol procedures, missing key efficacy assessments |

### Minor Deviation

| Category | Examples |
|---|---|
| Visit Window | Slightly exceeding visit window (within a few days) |
| Sample Collection | Minor timing deviations in non-critical samples |
| Questionnaire | Quality-of-life forms submitted a few days late |
| Data Recording | Delays in non-critical data, spelling/formatting errors |
| Documentation | Delays in source document signatures |

## Classification Rules

- Any dimension rated **High** → Major Deviation
- Safety = Medium AND (Data or Science ≥ Medium) → Major Deviation
- All other cases → Minor Deviation

## CLI Usage

```bash
# Single deviation
python scripts/main.py classify \
  --description "Subject visit delayed by 2 days" \
  --type "Visit Window"

# Batch from file
python scripts/main.py batch --input deviations.json --output report.json

# Interactive
python scripts/main.py interactive

# Impact assessment
python scripts/main.py assess \
  --description "Subject accidentally took double dose" \
  --safety-impact high --data-impact medium --scientific-impact medium
```

## Input / Output Format

→ Full schema details: [references/io_schema.md](references/io_schema.md)

## Regulatory Basis

- ICH E6(R2) / E6(R3) Good Clinical Practice
- FDA 21 CFR Part 312; FDA Guidance on Oversight of Clinical Investigations
- EMA Reflection Paper on Risk Based Quality Management
- NMPA Good Clinical Practice for Drug Clinical Trials

## Input Validation

This skill accepts: clinical trial protocol deviation descriptions with at least a deviation description and type field. Severity factors (safety_impact, data_impact, scientific_impact) are required for the `assess` subcommand.

If the request does not involve clinical trial deviation classification — for example, asking to classify adverse events, analyze efficacy data, or perform general medical coding — do not proceed. Instead respond:

> "`protocol-deviation-classifier` is designed to classify clinical trial protocol deviations per GCP/ICH E6. Your request appears to be outside this scope. Please provide a deviation description and type, or use a more appropriate tool."

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate classifications, citations, data, or execution outcomes.

## Output Requirements

Every final response must include:

1. **Objective** — what was classified and why
2. **Inputs Received** — deviation description, type, severity factors used
3. **Assumptions** — any inferred values
4. **Classification Result** — Major or Minor, with confidence score
5. **Alternative Classification** — if confidence < 0.85, provide the alternative classification with rationale for both options
6. **Rationale** — regulatory basis cited
7. **Risks and Limits** — caveats, manual review needs
8. **Next Checks** — recommended follow-up actions

## Notes

1. This tool provides classification recommendations; final determination must be confirmed by clinical QA personnel.
2. Serious/critical deviations must be reported to sponsor and ethics committee immediately.
3. Regularly review deviation trends and implement CAPA.
4. Classification standards may vary by regulatory agency, trial type, and protocol.
5. **Batch re-runs produce new event IDs** each time (datetime-based). For deterministic IDs, use `--id-prefix` with a stable prefix derived from the input batch hash.

## Dependencies

- Python 3.8+
- No third-party dependencies (pure Python standard library)
