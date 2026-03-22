---
name: managing-specimen-integrity
description: Evaluates specimen adequacy and rejection criteria with pre-analytical quality documentation. Use when assessing specimen quality, documenting rejection reasons, or managing pre-analytical errors.
tags:
  - management
  - pathology
metadata:
  author: casemark
  practice_areas:
    - Pathology
    - Laboratory Medicine
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---

# Managing Specimen Integrity

Evaluates specimen adequacy and rejection criteria with pre-analytical quality documentation.

## Why This Skill Exists

Pre-analytical errors account for 46-68% of all laboratory errors, and specimen integrity failures are the leading cause. A hemolyzed potassium specimen, a clotted coagulation tube, an unlabeled surgical specimen, or an improperly transported microbiology culture can each produce misleading results that drive incorrect clinical decisions. The economic cost is substantial: recollection disrupts clinical workflows, delays diagnosis, and in some cases (neonatal, oncology, difficult-access patients) recollection may be impossible or harmful.

CLIA 42 CFR 493.1242 requires laboratories to establish specimen submission and handling instructions and define criteria for specimen rejection. CAP accreditation (GEN.40490-40530 series) mandates documented acceptance/rejection criteria, specimen labeling requirements (two patient identifiers), and processes for managing non-conforming specimens. The Joint Commission patient safety goals reinforce two-identifier specimen labeling. This skill provides a systematic framework for evaluating specimen integrity and managing pre-analytical quality.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

1. **Specimen type** — Blood (tube type), urine, tissue, body fluid, swab, or other? Default: blood specimen.
2. **Test(s) ordered** — What analytes are requested? Different tests have different integrity requirements. Default: comprehensive metabolic panel.
3. **Issue identified** — Hemolysis, lipemia, icterus, clotting, underfill, mislabel, wrong tube, delayed transport, temperature excursion, or other? Default: hemolysis.
4. **Patient context** — Difficult draw (neonatal, dialysis, oncology), repeated collection issue, stat/urgent request? Default: routine adult.
5. **Collection site** — Was the specimen drawn from an IV line, port, or direct venipuncture? Default: direct venipuncture.
6. **Time since collection** — How long has the specimen been in transit or storage? Default: < 2 hours.
7. **Recollection feasibility** — Can a new specimen be obtained without significant burden? Default: yes.

### Documents to Request

- Specimen requisition form with two identifiers
- Collection time and collector identity
- Transport conditions (temperature, time in transit)
- Tube type and anticoagulant verification
- Hemolysis/lipemia/icterus index from analyzer (if quantified)
- Institutional specimen acceptance/rejection criteria policy
- Test-specific specimen requirements (stability, tube type, volume)
- Non-conforming specimen log

---

## Step 1: Specimen Identification and Labeling Verification

Verify specimen labeling per CAP and Joint Commission requirements:

**Minimum labeling requirements (CAP GEN.40490):**
- Two unique patient identifiers (name + DOB, name + MRN, or equivalent)
- Date of collection
- Time of collection (required for time-sensitive analytes)
- Collector identification
- Specimen source/type (for non-blood specimens)

**Rejection criteria for labeling deficiencies:**

| Deficiency | Action |
|---|---|
| No label on specimen | REJECT — no exceptions. Specimen cannot be relabeled after leaving the patient. |
| One identifier only | REJECT — recollect. Two identifiers are non-negotiable per Joint Commission NPSG. |
| Label on container but not on tube | REJECT — the tube itself must be labeled, not just an accompanying form. |
| Discrepancy between label and requisition | HOLD — contact collector for resolution before processing. |
| Illegible label | HOLD — contact collector for verification; reject if unresolvable. |

**Exception**: Surgical pathology and cytology specimens may have a reconciliation process per CAP ANP.11700, but the two-identifier requirement still applies.

---

## Step 2: Specimen Condition Assessment

Evaluate the physical condition of the specimen:

### Hemolysis Index (Chemistry Analyzers)

| H-Index | Hemolysis Level | Affected Analytes | Action |
|---|---|---|---|
| H < 50 | None/slight | None significantly | Process normally |
| H 50-100 | Mild | Potassium (+), LDH (+), AST (+), iron (+) | Report with comment for mildly affected analytes |
| H 100-200 | Moderate | K, LDH, AST, iron, total bilirubin, phosphorus | Reject affected analytes; report unaffected |
| H > 200 | Gross | Most chemistry analytes affected | Reject specimen; recollect |

### Lipemia Index

| L-Index | Lipemia Level | Affected Analytes | Action |
|---|---|---|---|
| L < 150 | None/slight | None significantly | Process normally |
| L 150-300 | Moderate | Electrolytes (pseudohyponatremia), some enzymes | Report with comment |
| L > 300 | Gross | Many analytes affected by light scattering | Ultracentrifuge or reject |

### Icterus Index

| I-Index | Icterus Level | Affected Analytes | Action |
|---|---|---|---|
| I < 20 | None/slight | None significantly | Process normally |
| I 20-40 | Moderate | Creatinine (Jaffe method), some enzymatic assays | Report with comment |
| I > 40 | Marked | Multiple analytes affected | Report with interference note |

---

## Step 3: Tube Type and Volume Verification

Confirm correct tube type and adequate fill volume:

**Common tube types and requirements:**

| Tube Color (Cap) | Additive | Tests | Minimum Fill |
|---|---|---|---|
| Light blue (citrate) | 3.2% sodium citrate | PT, PTT, fibrinogen, coag factors | 90% fill (9:1 blood:citrate ratio); underfill produces falsely prolonged results |
| Lavender (EDTA) | K2EDTA or K3EDTA | CBC, differential, reticulocyte, HbA1c | Minimum 0.5 mL for CBC |
| Green (heparin) | Lithium heparin or sodium heparin | Stat chemistry, ammonia | Per tube manufacturer |
| Gold/red (SST/no additive) | Clot activator +/- gel | Routine chemistry, serology, drug levels | Allow 30 min clotting before centrifugation |
| Gray (NaF/oxalate) | Sodium fluoride/potassium oxalate | Glucose, lactate | Per tube manufacturer |

**Rejection criteria for tube/volume issues:**

| Issue | Action |
|---|---|
| Citrate tube < 90% filled | REJECT for coagulation tests. Insufficient fill alters the blood:citrate ratio. |
| Clotted EDTA specimen | REJECT for CBC. Platelet count will be falsely low. |
| Wrong tube type for test | REJECT — do not attempt to process. |
| Specimen drawn from IV line without discard | REJECT — risk of dilution or contamination with IV fluids. |

---

## Step 4: Stability and Transport Assessment

Evaluate whether specimen stability requirements were met:

**Critical stability windows:**

| Analyte/Test | Room Temp Stability | Refrigerated Stability | Special Requirements |
|---|---|---|---|
| Potassium | 4 hours (separate from cells) | 24 hours (after separation) | Must centrifuge within 1 hour; pseudohyperkalemia if delayed |
| Glucose (no NaF) | 30 minutes | 2 hours | Glycolysis reduces glucose ~7%/hour at room temp |
| Ammonia | 15 minutes on ice | 15 minutes on ice | Must be transported on ice and centrifuged immediately |
| Blood gas (ABG) | 15 minutes (plastic syringe) | 30 minutes (glass syringe, ice) | Air bubbles invalidate pO2/pCO2 |
| Lactic acid | 15 minutes on ice | 15 minutes on ice | Tourniquet time and fist clenching cause false elevation |
| Coagulation (PT, PTT) | 4 hours at RT (uncentrifuged) | 24 hours (centrifuged, frozen) | Do not refrigerate uncentrifuged citrate tubes |
| CSF cell count | 1 hour | 1 hour | WBCs lyse rapidly; process stat |

---

## Step 5: Non-Conforming Specimen Management and Documentation

When a specimen is rejected or has quality issues, follow a structured process:

1. **Document the issue**: Record the specific non-conformance (hemolysis, clot, mislabel, etc.) in the LIS.
2. **Notify the collector/ordering provider**: Per institutional policy, communicate the rejection reason and recollection instructions.
3. **Partial reporting**: When possible, report unaffected analytes from the specimen and reject only those analytes affected by the integrity issue. Add interpretive comments.
4. **Log the non-conformance**: Enter into the non-conforming specimen tracking system for trending.
5. **Trend analysis**: Review non-conformance data monthly. Identify patterns by collector, unit, specimen type, or time of day. Target QI interventions to reduce the most common and impactful errors.
6. **Education and feedback**: Provide targeted education to collection staff when trends are identified. Document training and re-competency assessment.

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

1. Was specimen labeling verified against the two-identifier requirement before any testing?
2. Were hemolysis, lipemia, and icterus indices quantified and applied to analyte-specific rejection criteria?
3. Was tube type confirmed as correct for all ordered tests?
4. Were stability requirements assessed based on collection time and transport conditions?
5. Was the non-conforming specimen documented in the tracking system with collector notification?

---

## Quality Audit

- [ ] Two patient identifiers verified on specimen label
- [ ] Collection date, time, and collector identity documented
- [ ] Hemolysis/lipemia/icterus index quantified by analyzer
- [ ] Analyte-specific rejection thresholds applied (not blanket rejection)
- [ ] Tube type correct for all ordered tests
- [ ] Citrate tube fill volume verified (>= 90% for coagulation)
- [ ] Specimen transported within stability requirements
- [ ] Temperature-sensitive specimens transported on ice when required
- [ ] Non-conforming specimen logged with specific rejection reason
- [ ] Collector/provider notified of rejection with recollection instructions
- [ ] Monthly trending of non-conformance data performed
- [ ] QI interventions documented for identified trends
- [ ] Institutional acceptance/rejection criteria policy current and accessible
- [ ] Staff competency for specimen assessment documented annually

---

## Guidelines

- Never process an unlabeled specimen regardless of urgency — this is a non-negotiable patient safety requirement per CAP and Joint Commission
- Quantify hemolysis, lipemia, and icterus using the analyzer's serum index system rather than visual estimation; visual assessment is unreliable and not auditable
- Apply analyte-specific rejection thresholds rather than blanket specimen rejection; many analytes are unaffected by mild hemolysis, and rejecting the entire panel wastes clinical resources
- For citrate tubes (coagulation testing), reject any tube less than 90% filled; the altered blood-to-citrate ratio produces unreliable PT and PTT results regardless of how "close" the fill appears
- Separate serum/plasma from cells within 1 hour of collection for potassium and other cell-sensitive analytes; delayed separation is the most common cause of pseudohyperkalemia
- Track non-conforming specimens by collector, unit, and specimen type; use the data for targeted quality improvement rather than punitive action
- When recollection is impossible or poses significant patient burden (neonatal, difficult access), consult with the laboratory director about reporting with appropriate qualifiers and comments
- Review and update institutional acceptance/rejection criteria at least annually and whenever new tests or specimen types are introduced
