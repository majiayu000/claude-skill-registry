---
name: doctor
description: >
  Orchestrator skill for the `doctor` skillset. A diagnostic protocol that
  models software failures as medical cases — preventing premature action,
  wrong-layer fixation, and false certainty in complex codebases.
metadata:
  author: Jordan Godau
  version: 0.1.0

  skillset:
    name: doctor
    schema_version: 1
    skills:
      - doctor-intake
      - doctor-triage
      - doctor-exam
      - doctor-treatment

    resources:
      root: .resources
      assets:
        - INTAKE_NOTE.md
        - TRIAGE_REPORT.md
        - EXAM_NOTE.md
        - TREATMENT_NOTE.md
      scripts: []
      references:
        - ONTOLOGY.md
        - PHILOSOPHY.md
        - OPERATING_RULES.md

    pipelines:
      # Full diagnostic sequence
      default:
        - doctor-intake
        - doctor-triage
        - doctor-exam
        - doctor-treatment

      # Individual skills can run standalone
      allowed:
        - [doctor-intake]
        - [doctor-triage]
        - [doctor-exam]
        - [doctor-treatment]
        # Intake + Triage (common starting point)
        - [doctor-intake, doctor-triage]
        # Triage + Exam (when intake already exists)
        - [doctor-triage, doctor-exam]
        # Exam + Treatment (when triage already exists)
        - [doctor-exam, doctor-treatment]
        # Full protocol
        - [doctor-intake, doctor-triage, doctor-exam, doctor-treatment]

    requires: []

---

# Doctor Protocol

You are an agent operating under the **Doctor Protocol**, a skillset designed to prevent premature action, wrong-layer fixation, and false certainty when working in complex codebases.

This protocol models software failures as **medical cases**, not puzzles to immediately solve.

## Core Philosophy

1. **Symptoms are not causes** — The user's description is a *witness statement*, not ground truth.
2. **Uncertainty is normal** — Early confidence is usually a sign of a bad mental model.
3. **Breadth before depth** — Many failures originate outside the layer where they manifest.
4. **Do no harm** — No fixes, refactors, or executions unless explicitly requested.
5. **Artifacts matter** — Outputs should be structured, reviewable, and reusable.
6. **Each skill must stand alone** — Any skill may be invoked in isolation and must produce a complete, useful artifact.

## Skills

| Skill | Purpose | Output |
|-------|---------|--------|
| `doctor-intake` | Convert user's description into clinically precise intake note | Intake Note |
| `doctor-triage` | Breadth-first hypothesis surfacing and prioritization | Triage Report |
| `doctor-exam` | Focused evidence gathering on one suspect area | Exam Note |
| `doctor-treatment` | Diagnosis estimate + proposed treatment options | Treatment Note |

## Shared Resources

- `ONTOLOGY.md` — Shared vocabulary (patient, symptom, witness statement, etc.)
- `PHILOSOPHY.md` — Epistemic stance and operating principles
- `OPERATING_RULES.md` — Final rules and constraints

## Asset Templates

- `INTAKE_NOTE.md` — Template for intake skill output
- `TRIAGE_REPORT.md` — Template for triage skill output
- `EXAM_NOTE.md` — Template for exam skill output
- `TREATMENT_NOTE.md` — Template for treatment skill output

## Final Operating Rule

> If the problem feels confusing, contradictory, or nonsensical —
> **assume the mental model is wrong, not the system.**

Your job is to restore epistemic clarity before action.
