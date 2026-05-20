---
name: managing-cardiac-devices
description: Interprets pacemaker and ICD interrogation data with programming optimization documentation. Use when reviewing device interrogations, managing pacemaker settings, or documenting ICD therapies.
tags:
  - management
  - cardiology
metadata:
  author: casemark
  practice_areas:
    - Cardiology
    - Interventional Cardiology
    - Electrophysiology
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---

# Managing Cardiac Devices

Interprets pacemaker and ICD interrogation data with programming optimization documentation.

## Why This Skill Exists

Over 1.2 million cardiac implantable electronic devices (CIEDs) are implanted annually worldwide. Device interrogation data contains critical information about arrhythmia events, lead function, battery status, and therapy delivery that directly impacts patient safety. Failure to recognize lead malfunction, inappropriate ICD shocks, or suboptimal pacing parameters can result in syncope, cardiac arrest, or unnecessary therapies that degrade quality of life.

The HRS (Heart Rhythm Society) Expert Consensus on CIED management mandates systematic interrogation review, remote monitoring enrollment, and structured follow-up. This skill ensures every device check is documented completely with actionable findings.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

1. What device type is implanted — single-chamber pacemaker, dual-chamber pacemaker, ICD, CRT-D, CRT-P, or leadless pacemaker? (default: "Device type not specified")
2. What is the device manufacturer and model? (default: "Manufacturer unknown")
3. What was the indication for implantation? (default: "Indication not documented")
4. When was the device implanted or last generator change? (default: "Implant date unknown")
5. Is this a routine interrogation, symptom-driven check, or remote monitoring alert? (default: "Routine follow-up")
6. Has the patient reported any symptoms — palpitations, syncope, shocks, dizziness? (default: "No symptoms reported")
7. Is there a prior interrogation available for comparison? (default: "No prior report available")
8. Is the patient on antiarrhythmic medications? (default: "Medication list not provided")

### Documents to Request

- Complete device interrogation printout (all pages including EGMs)
- Prior interrogation report for comparison
- Current device programming summary
- Remote monitoring transmissions (last 3 months)
- 12-lead ECG with and without magnet application
- Echocardiogram (LVEF for ICD/CRT assessment)
- Current medication list (antiarrhythmics, anticoagulants)
- Operative report from implant or last revision

---

## Step 1: Battery and Lead Parameter Assessment

**Battery Status Evaluation:**

| Status | Definition | Action |
|--------|-----------|--------|
| BOL (beginning of life) | Full battery voltage | Routine follow-up |
| MOL (middle of life) | Adequate remaining battery | Routine follow-up |
| ERI (elective replacement indicator) | Battery nearing depletion | Schedule generator replacement within 3 months |
| EOL/EOS (end of life/service) | Critical battery depletion | Urgent generator replacement; device may revert to VVI |

**Lead Parameter Thresholds:**

| Parameter | Atrial Lead | RV Lead | LV Lead (CRT) |
|-----------|------------|---------|---------------|
| Pacing threshold | < 1.5 V @ 0.4 ms | < 1.5 V @ 0.4 ms | < 3.5 V @ 0.5 ms |
| Sensing (P/R wave) | > 1.5 mV | > 5.0 mV | N/A (unipolar) |
| Impedance | 200–1500 Ω | 200–1500 Ω | 200–1500 Ω |

**Lead Malfunction Red Flags:**
- Threshold > 5 V or sudden rise > 1 V from baseline → lead dislodgement, micro-fracture, or fibrosis
- Impedance < 200 Ω → insulation breach
- Impedance > 2000 Ω → lead fracture
- Sensing drop > 50% → lead dislodgement or tissue changes

---

## Step 2: Pacing Function Assessment

**Pacing Mode Nomenclature (NBG Code):**
- Position I: chamber paced (A, V, D)
- Position II: chamber sensed (A, V, D)
- Position III: response to sensing (I = inhibited, T = triggered, D = dual)
- Position IV: rate modulation (R)
- Position V: multisite pacing (for CRT)

**Common Pacing Modes:**

| Mode | Typical Indication |
|------|-------------------|
| AAI(R) | Sinus node dysfunction with intact AV conduction |
| VVI(R) | Atrial fibrillation with slow ventricular response |
| DDD(R) | Sinus node dysfunction or AV block with sinus rhythm |
| DDI(R) | Paroxysmal AF with AV block (avoids tracking) |

**Assess:**
- Percent atrial pacing (% AP) — high AP in DDD may suggest sinus node disease
- Percent ventricular pacing (% VP) — minimize RV pacing if LVEF preserved (algorithms: MVP, AAISafeR, RYTHMIQ)
- Rate response settings — appropriateness for patient's activity level
- Mode switch episodes — frequency and appropriateness (AF/flutter detection)

---

## Step 3: Arrhythmia Episode Review (ICD/CRT-D)

**Episode Classification:**

| Zone | Typical Rate (bpm) | Typical Therapy |
|------|-------------------|-----------------|
| VT Monitor | 130–170 | Monitor only, no therapy |
| VT-1 | 170–200 | ATP × 3, then cardioversion |
| VT-2/VF | > 200 | ATP during charging, then defibrillation |
| SVT discriminators | Variable | Withhold therapy if SVT confirmed |

**For Each Stored Episode, Document:**
1. Date and time
2. Heart rate at onset and during episode
3. Rhythm classification by device (VT, VF, SVT, noise)
4. Whether device classification was correct (review EGMs)
5. Therapy delivered (ATP, cardioversion, defibrillation) and result
6. Whether therapy was appropriate or inappropriate

**Inappropriate Shock Causes:**
- Atrial fibrillation with rapid ventricular response
- Sinus tachycardia (exercise)
- Lead noise / oversensing (T-wave oversensing, lead fracture artifact)
- Electromagnetic interference
- Double-counting (RBBB counting R and R' as separate events)

---

## Step 4: CRT Optimization (CRT-D/CRT-P)

**Biventricular Pacing Assessment:**
- Target: ≥ 98% biventricular pacing
- Common reasons for low BiV%: frequent PVCs, AF with fast rate, loss of LV capture, inappropriate AV delay

**Optimization Parameters:**
- AV delay optimization: guided by echo (Ritter method or iterative LVOT VTI)
- VV delay optimization: simultaneous vs. LV-first (typically 0–40 ms LV pre-excitation)
- Monitor for LV lead dislodgement: rising threshold, phrenic nerve stimulation, loss of capture

**CRT Response Assessment:**
- Responder: ≥ 5% improvement in LVEF and/or ≥ 1 NYHA class improvement
- Super-responder: LVEF normalizes (> 50%)
- Non-responder: check BiV%, lead position (lateral/posterolateral preferred), AV/VV timing, AF burden, scar burden

---

## Step 5: Documentation and Follow-Up Plan

**Structured Interrogation Report Must Include:**
1. Device type, manufacturer, model, serial number
2. Battery status with estimated longevity
3. Lead parameters: threshold, sensing, impedance (each lead)
4. Pacing percentages (atrial and ventricular)
5. Arrhythmia episode summary with EGM review conclusions
6. Therapy summary (ATP events, shocks — appropriate vs. inappropriate)
7. Programming changes made and rationale
8. Remote monitoring status confirmation
9. Next scheduled follow-up

**Follow-Up Intervals (HRS Recommendations):**
- In-person: every 6–12 months
- Remote monitoring: every 3 months (or per manufacturer protocol)
- Post-implant: 2–12 weeks wound check + first interrogation
- ERI/EOL: monthly until generator change
- After any therapy or alert: urgent evaluation

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

1. Are battery status and estimated longevity documented?
2. Are all lead parameters within acceptable ranges or flagged?
3. Have all stored arrhythmia episodes been reviewed and classified as appropriate/inappropriate?
4. Is the biventricular pacing percentage reported for CRT devices?
5. Are programming changes documented with clinical rationale?

---

## Quality Audit

- [ ] Device type, manufacturer, model documented
- [ ] Battery voltage and estimated longevity stated
- [ ] All lead thresholds, sensing amplitudes, and impedances recorded
- [ ] Lead parameters compared to prior interrogation
- [ ] Pacing mode and percentages documented
- [ ] Rate response settings reviewed for appropriateness
- [ ] All arrhythmia episodes reviewed with EGM analysis
- [ ] Inappropriate therapies identified and programming adjusted
- [ ] CRT biventricular pacing percentage reported (if applicable)
- [ ] CRT optimization status documented (AV/VV timing)
- [ ] Remote monitoring enrollment confirmed
- [ ] Programming changes listed with rationale
- [ ] Follow-up interval and plan documented
- [ ] Patient symptoms correlated with device data

---

## Guidelines

1. Always review stored electrograms (EGMs) for every episode — device rhythm classification is not always correct.
2. High ventricular pacing percentage (> 40%) in patients with preserved LVEF should prompt evaluation for pacing-induced cardiomyopathy and possible CRT upgrade.
3. For inappropriate shocks, identify the cause before reprogramming — T-wave oversensing, lead fracture, and SVT each require different solutions.
4. In CRT non-responders, ensure BiV pacing is ≥ 98% before concluding CRT failure — AF, PVCs, and loss of LV capture are correctable causes.
5. MRI-conditional devices require specific protocols — confirm device and all leads are MRI-conditional, program to MRI mode, and interrogate immediately post-scan.
6. Patients with ICDs who are at end of life should be offered deactivation of shock therapies as part of goals-of-care discussions — document clearly.
7. Remote monitoring reduces time to clinical decision for arrhythmias, lead failures, and battery alerts — enrollment is a Class I recommendation.
8. Never discharge a patient with an ERI/EOL device without a scheduled generator replacement — document the surgical plan and date.
