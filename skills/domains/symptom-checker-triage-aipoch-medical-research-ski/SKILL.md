---
name: symptom-checker-triage
description: Suggest triage levels (Emergency, Urgent, Outpatient) based on red flag symptoms using a rule-based engine. For AI-assisted decision support only — not a substitute for professional medical diagnosis.
license: MIT
skill-author: AIPOCH
---

# Symptom Checker Triage

Analyzes symptom descriptions and suggests triage levels (Emergency / Urgent / Outpatient) based on red flag identification. Provides rationale and recommended next steps. For AI-assisted decision support only.

## Quick Check

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py "Chest pain, difficulty breathing, lasting 30 minutes"
python scripts/main.py "Headache, fever 38.5 degrees, vomiting" --verbose
```

## When to Use

- Triage a patient symptom description to Emergency, Urgent, or Outpatient level
- Identify red flag symptoms in a clinical or research context
- Generate structured triage output for documentation or downstream processing

## Workflow

1. Confirm the symptom description is provided as natural language text.
2. Validate that the request is a symptom triage task; stop early if not.
3. Run `scripts/main.py` with the symptom string or use `--interactive` mode.
4. Return a structured result with triage level, red flags, rationale, and disclaimer.
5. If execution fails or inputs are incomplete, switch to the Fallback Template below.

## Fallback Template

If `scripts/main.py` fails or required fields are missing, respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective        : <triage goal>
Inputs Available : <symptom description provided>
Missing Inputs   : <list exactly what is missing>
Partial Result   : <any triage assessment that can be made safely>
Blocked Steps    : <what could not be completed and why>
Disclaimer       : This is AI-assisted advice only. Seek professional medical care.
Next Steps       : <minimum info needed to complete>
───────────────────────────────────────
```

## Stress-Case Output Checklist

For complex multi-constraint requests, always include these sections explicitly:

- **Assumptions**: symptom keywords matched, confidence threshold applied
- **Constraints**: rule-based engine only; no differential diagnosis
- **Risks**: false positives and false negatives are possible; always defer to clinician
- **Unresolved Items**: ambiguous symptoms requiring clarification

## CLI Usage

```bash
# Direct symptom input
python scripts/main.py "Chest pain, radiating to left arm, sweating"

# Interactive mode
python scripts/main.py --interactive

# Verbose output
python scripts/main.py "Headache, fever" --verbose

# JSON output
python scripts/main.py "Abdominal pain, right lower quadrant tenderness" --json
```

## Output Format

```json
{
  "triage_level": "emergency|urgent|outpatient",
  "confidence": 0.85,
  "red_flags": ["Chest pain", "Difficulty breathing"],
  "reason": "Chest pain with difficulty breathing may indicate myocardial infarction or pulmonary embolism",
  "recommendation": "Go to emergency department immediately",
  "department": "Emergency/Cardiology",
  "warning": "This is AI-assisted advice and cannot replace professional medical diagnosis"
}
```

## Triage Levels

| Level | Description | Action |
|---|---|---|
| emergency | Life-threatening red flags present | Call emergency services or go to ED immediately |
| urgent | Serious but not immediately fatal | Seek care within 2–4 hours |
| outpatient | Non-urgent | Schedule outpatient appointment |

## Red Flag Categories

→ Full red flags reference: [references/red_flags.md](references/red_flags.md)

Key categories: Cardiovascular, Respiratory, Neurological, Gastrointestinal, Trauma/Poisoning, Obstetric.

## Disclaimer

> **Important**: This tool provides AI-assisted triage suggestions only. It **cannot replace professional medical diagnosis**. If in doubt, seek medical care immediately. Call emergency services in life-threatening situations.

## Input Validation

This skill accepts: natural language symptom descriptions in English or Chinese for triage level suggestion.

If the request does not involve symptom triage — for example, asking to diagnose a specific disease, prescribe medication, interpret lab results, or perform general medical Q&A — do not proceed. Instead respond:

> "`symptom-checker-triage` is designed to suggest triage levels based on symptom red flags. Your request appears to be outside this scope. Please provide a symptom description, or use a more appropriate tool. This tool does not provide diagnoses or treatment recommendations."

## Error Handling

- If no symptom description is provided, request it explicitly.
- If the task goes outside documented scope (diagnosis, prescription), stop immediately.
- If `scripts/main.py` fails, use the Fallback Template above.
- Do not fabricate triage levels, red flag matches, or medical advice.

## Output Requirements

Every final response must include:

1. **Objective** — what symptom set was triaged
2. **Inputs Received** — symptom description used
3. **Assumptions** — keyword matching applied, confidence threshold
4. **Triage Result** — level, red flags identified, rationale
5. **Risks and Limits** — AI-only, not a diagnosis, false positive/negative risk
6. **Next Checks** — always recommend professional medical evaluation

## Dependencies

- Python 3.8+
- No third-party dependencies (rule-based engine, standard library only)
