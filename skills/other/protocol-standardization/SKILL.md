---
name: protocol-standardization
description: Standardize fragmented experimental steps into reproducible protocol documents when you need method organization, lab SOP drafting, or cross-operator reproducibility; missing parameters must be explicitly marked as "To be supplemented/Not provided".
license: MIT
skill-author: AIPOCH
---

## When to Use

- You have messy notes (chat logs, notebook fragments, bullet points) and need a formal, reproducible experimental protocol.
- You are preparing a lab SOP for standardization across multiple operators or sites.
- You need to convert exploratory/iterative experimental steps into a structured method for documentation or publication support.
- You are onboarding new team members and must clarify steps, parameters, and checkpoints without inventing missing information.
- You are auditing an existing method to identify missing critical parameters and quality-control points.

## Key Features

- Converts fragmented experimental steps into a standardized protocol structure (prep → execution → closing).
- Enforces parameter completeness for reproducibility (e.g., temperature, time, concentration, volume, mixing/rotation speed).
- Prohibits fabrication: any unknown or uncertain information is explicitly labeled as **"To be supplemented/Not provided"**.
- Unifies units, terminology, and step formatting for consistency.
- Adds operational checks: logical order, safety notes, and waste disposal requirements.
- Supports structured output using reusable templates (see `assets/protocol_template.md`).
- Provides format guidance and checklists via `references/guide.md`.

## Dependencies

- None (documentation-only skill; no runtime dependencies specified).

## Example Usage

### Input (raw experimental notes)

**Goal:** Protein precipitation and cleanup (example)

**Materials/Reagents**
- Sample lysate: 200 µL
- Acetone (pre-chilled): volume not recorded
- Microcentrifuge tubes
- Centrifuge

**Steps (as recorded)**
1. Add acetone to lysate, mix.
2. Put at cold temperature for a while.
3. Spin down, remove supernatant.
4. Dry pellet, then resuspend.

### Output (standardized protocol)

**Title:** Protein Precipitation by Cold Acetone (Standardized Protocol)

**Purpose**
- Precipitate proteins from lysate for downstream analysis.

**Materials/Reagents**
- Sample lysate: 200 µL
- Acetone (pre-chilled): **To be supplemented/Not provided** (final ratio/volume)
- Microcentrifuge tubes
- Centrifuge (model/rotor: **To be supplemented/Not provided**)

**Equipment**
- Microcentrifuge capable of: **To be supplemented/Not provided** (×g or rpm)
- Temperature control (ice bath / 4°C fridge / cold room): **To be supplemented/Not provided**

**Procedure**

**A. Preparation**
1. Label microcentrifuge tubes with sample IDs.
2. Pre-chill acetone to **To be supplemented/Not provided** (e.g., -20°C) and prepare a cold incubation environment (**To be supplemented/Not provided**).

**B. Execution**
3. Add pre-chilled acetone to 200 µL lysate at a ratio of **To be supplemented/Not provided** (e.g., 4:1 acetone:lysate).
4. Mix by **To be supplemented/Not provided** (vortex/inversion) for **To be supplemented/Not provided** (time).
5. Incubate at **To be supplemented/Not provided** (temperature) for **To be supplemented/Not provided** (time).
6. Centrifuge at **To be supplemented/Not provided** (×g or rpm) for **To be supplemented/Not provided** (time) at **To be supplemented/Not provided** (temperature).
7. Carefully remove and discard the supernatant without disturbing the pellet.

**C. Closing**
8. Air-dry pellet for **To be supplemented/Not provided** (time) until residual solvent is removed (do not overdry if resuspension is required).
9. Resuspend pellet in **To be supplemented/Not provided** (buffer type and volume) by **To be supplemented/Not provided** (pipetting/vortexing) for **To be supplemented/Not provided** (time).

**Critical Parameters to Supplement**
- Acetone:lysate ratio (or acetone volume)
- Incubation temperature and duration
- Centrifugation force/time/temperature
- Pellet drying time
- Resuspension buffer and volume

**Quality Control / Checkpoints**
- Pellet presence after centrifugation: **Expected** (yes/no criteria to be supplemented)
- Supernatant clarity: **To be supplemented/Not provided**
- Resuspension completeness: **To be supplemented/Not provided**

**Safety & Waste Disposal**
- Acetone handling: **To be supplemented/Not provided** (PPE/ventilation requirements)
- Solvent waste disposal route: **To be supplemented/Not provided**

**Suggested Output Location**
- `outputs/ProteinPrecipitation_Acetone.txt` (example naming)

## Implementation Details

- **Workflow Structure**
  1. **Step Review:** Collect all steps/materials; classify into preparation, execution, and closing phases.
  2. **Parameter Completion:** Identify required parameters (time, temperature, concentration, volume, mixing/rotation speed, centrifugation force, etc.).  
     - If missing/uncertain, do **not** infer; mark as **"To be supplemented/Not provided"** and list fields requiring supplementation.
  3. **Standardization and Organization:** Rewrite into a consistent protocol format; unify units and terminology.
  4. **Output Check:** Validate logical sequence and operability; add safety and waste disposal notes.

- **Parameter Rules**
  - Never fabricate values.
  - Use consistent units (e.g., °C, min, mL/µL, mM, ×g or rpm).
  - Explicitly surface “critical control points” (steps where parameter deviations affect outcomes).

- **Templates and References**
  - Protocol template: `assets/protocol_template.md`
  - Output formats, checklists, and key checkpoints: `references/guide.md`

- **Output Path and Naming**
  - Default output directory: `outputs/`
  - Naming convention: `{Experiment_Info_Abbreviation}.txt`