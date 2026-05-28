---
name: emergency-triage
description: Veterinary emergency triage and initial stabilization guidance based on RECOVER and ACVECC protocols. Use when an animal presents with an acute emergency.
---

# Veterinary Emergency Triage

## Overview

Rapid triage assessment and initial stabilization guidance for veterinary emergencies. Based on RECOVER (Reassessment Campaign on Veterinary Resuscitation) guidelines and ACVECC (American College of Veterinary Emergency and Critical Care) protocols. Prioritizes the most immediately life-threatening conditions.

## When to Use

- Animal presenting with acute, life-threatening signs
- User describes an emergency scenario (collapse, seizure, difficulty breathing, acute abdomen, trauma, toxin ingestion)
- User asks about CPR or resuscitation in animals
- User asks about triage categories or emergency prioritization
- Keywords: emergency, critical, collapse, seizure, dyspnea, GDV, bloat, HBC (hit by car), CPR, crash, code, resuscitation, shock

## Workflow

1. **Assess ABCs** (Airway, Breathing, Circulation) for the species:
   - **Airway:** Patent? Obstructed? Intubation needed?
   - **Breathing:** Rate, effort, pattern. Species-specific normal ranges.
   - **Circulation:** Heart rate, pulse quality, CRT, mucous membrane color, blood pressure if available.

2. **Triage category assignment:**
   - **RED (Immediate):** Cardiopulmonary arrest, respiratory distress, active hemorrhage, GDV, anaphylaxis, status epilepticus
   - **YELLOW (Urgent):** Fractures, moderate dyspnea, urethral obstruction, dystocia, moderate hemorrhage
   - **GREEN (Non-urgent):** Stable lacerations, chronic vomiting/diarrhea, ear infections, skin lesions
   - **BLUE (Expectant/Deceased):** Cardiopulmonary arrest with no response to CPR

3. **Species-specific vital parameter reference:**
   - Dog: HR 60-160 bpm, RR 10-30, Temp 100-102.5F
   - Cat: HR 140-220 bpm in clinical setting (resting: 110-140; stress elevates to 180-220), RR 20-40, Temp 100-102.5F
   - Horse: HR 28-44 bpm, RR 8-16, Temp 99-101.5F
   - (Provide ranges for the relevant species)

4. **RECOVER CPR algorithm** (if cardiac arrest):
   - BLS: Chest compressions 100-120/min, 1 breath every 6 seconds
   - Compress 1/3 to 1/2 chest width
   - Species-specific hand placement (lateral vs. sternal depending on body conformation)
   - ALS: Epinephrine 0.01 mg/kg IV q3-5min, atropine 0.04 mg/kg IV for vagal-mediated arrest
   - Cycle assessment every 2 minutes

5. **Initial stabilization guidance** by presentation type.

## Output Format

```
## Emergency Triage: [Presentation]

**Triage Category:** [RED/YELLOW/GREEN]
**Immediate threats:** [List in priority order]

**Initial stabilization:**
1. [First action]
2. [Second action]
3. [Third action]

**Vital parameter targets for [species]:**
- HR: [target range]
- RR: [target range]
- MAP: [target]

**Do NOT:**
- [Common mistakes to avoid for this presentation]

**Reference:** RECOVER Guidelines, JVECC

**⚠ IF IN DOUBT, GO TO AN EMERGENCY VET NOW. DO NOT WAIT FOR SIGNS TO WORSEN.**
Emergency Poison Control: ASPCA 888-426-4435 | Pet Poison Helpline 855-764-7661
```

## Limitations

- Emergency medicine requires hands-on patient assessment. This skill provides protocol guidance, not patient-specific treatment.
- RECOVER guidelines are primarily validated in dogs and cats. Evidence for other species is more limited.
- Local drug availability and equipment may differ from protocol recommendations.
- This skill is not a substitute for emergency veterinary training.
