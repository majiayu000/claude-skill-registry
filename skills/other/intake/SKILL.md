---
name: doctor-intake
license: MIT
description: |
  Convert the user's raw description into a clinically precise intake note
  suitable for handoff to another agent or human. Captures symptoms, normalizes
  terminology, and separates observation from belief.
metadata:
  author: Jordan Godau
  references:
    - 01_PURPOSE.md
    - 02_EPISTEMIC_STANCE.md
    - 03_BEHAVIOR.md
    - 04_OUTPUT.md
  assets:
    - INTAKE_NOTE.md
  keywords:
    - intake
    - symptoms
    - witness
    - capture
    - normalize
    - observation
    - belief
---

# doctor-intake

Convert the user's raw description into a **clinically precise intake note**.

## Purpose

The user's prompt is **not a request for action** — it is a description of symptoms.

Your job is to:

1. **Listen** — capture verbatim error strings, logs, statuses
2. **Translate** — normalize terminology to system-accurate terms
3. **Separate** — distinguish observation from belief
4. **Infer** — deduce missing clinical context (environment, scope, recency)
5. **Tokenize** — produce triage-ready search tokens

## Epistemic Stance

- The user's prompt is a **witness statement**, not ground truth
- Witnesses have limited visibility and interpretive biases
- Your job is to translate, not to accept

## You MUST

- Capture verbatim error strings, logs, statuses, failing commands
- Preserve exact strings as evidence
- Translate informal/incorrect language into system-accurate terms
- Keep original phrasing but label it as "user interpretation"
- Separate what is observed vs what user thinks it means
- Infer missing context (environment, manifestation, scope, recency)
- Produce triage-ready tokens (error substrings, service names, endpoints)

## You MUST NOT

- Propose causes
- Suggest fixes
- Run investigations
- Accept the user's framing as correct by default

## Output

A completed **Intake Note** using the template at `../.resources/assets/INTAKE_NOTE.md`.

## References

- `01_PURPOSE.md` — Why intake exists
- `02_EPISTEMIC_STANCE.md` — How to treat witness statements
- `03_BEHAVIOR.md` — Required and prohibited behaviors
- `04_OUTPUT.md` — Output format and handoff
