---
name: Medical Scribe
slug: medical-scribe
description: Medical documentation, clinical note generation, and healthcare information organization for providers and patients
category: domain
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "document patient encounter"
  - "create SOAP note"
  - "medical documentation"
  - "clinical summary"
  - "patient history"
  - "discharge summary"
tags:
  - healthcare
  - medical-records
  - clinical-documentation
  - HIPAA
  - patient-care
---

# Medical Scribe

Professional medical documentation assistant designed to help healthcare providers create accurate, comprehensive clinical notes while maintaining focus on patient care. This skill generates structured medical documentation following industry-standard formats (SOAP, APSO, admission notes, discharge summaries), organizes patient information, and ensures documentation meets regulatory and billing requirements.

The Medical Scribe excels at transforming conversational patient encounters into properly formatted clinical notes, capturing relevant history and physical exam findings, documenting clinical decision-making, organizing complex medical information, and creating patient-friendly summaries. It's valuable for physicians, nurse practitioners, physician assistants, and other clinical providers across specialties.

**Critical Compliance Notice:** This skill is a documentation tool only. All clinical documentation must be reviewed, edited, and signed by the treating provider. Users are responsible for HIPAA compliance, protecting patient privacy, and ensuring accuracy of all medical records. Never include actual patient identifiers (names, MRNs, dates of birth) when using this tool.

## Core Workflows

### Workflow 1: SOAP Note Generation

**Purpose:** Create comprehensive, billing-compliant SOAP (Subjective, Objective, Assessment, Plan) notes from patient encounters.

**Input Methods:**
- Voice dictation transcript
- Bullet point encounter notes
- Free-form provider narrative
- Structured interview responses

**Steps:**
1. **Subjective Section**
   - Chief complaint (CC)
   - History of present illness (HPI)
     - Location, quality, severity, duration, timing, context, modifying factors, associated signs/symptoms
   - Review of systems (ROS)
   - Past medical history (PMH)
   - Medications and allergies
   - Family history (FH)
   - Social history (SH)

2. **Objective Section**
   - Vital signs
   - Physical examination findings by system
   - Relevant lab/imaging results
   - Mental status examination (if applicable)

3. **Assessment Section**
   - Primary diagnosis/diagnoses with ICD-10 codes
   - Differential diagnoses
   - Clinical reasoning and decision-making
   - Patient complexity and acuity

4. **Plan Section**
   - Diagnostic workup ordered
   - Treatment plan (medications, procedures, therapies)
   - Patient education provided
   - Follow-up instructions
   - Referrals
   - Time-based elements for billing (if applicable)

**Quality Checks:**
- All HPI elements documented
- ROS covers 10+ systems for comprehensive exam
- Physical exam documented by systems
- Assessment clearly linked to findings
- Plan addresses each problem
- Billing level supported by documentation

**Output Formats:**
- Standard SOAP note
- EMR-ready format (Epic, Cerner, etc.)
- Billing-optimized version with E/M level justification
- Patient-friendly summary (after-visit summary style)

### Workflow 2: Admission & Discharge Documentation

**Purpose:** Create complete hospital admission histories and discharge summaries.

**Admission Note (H&P):**
1. **Identification** - Age, sex, reason for admission
2. **Chief Complaint** - Why patient is being admitted
3. **History of Present Illness** - Detailed narrative of current condition
4. **Past Medical History** - Chronic conditions, surgeries, hospitalizations
5. **Medications** - Home medications with doses
6. **Allergies** - Drug and other allergies with reactions
7. **Family History** - Relevant hereditary conditions
8. **Social History** - Occupation, living situation, substances, support system
9. **Review of Systems** - Complete 14-point ROS
10. **Physical Examination** - Complete head-to-toe exam
11. **Labs/Imaging** - Admission workup results
12. **Assessment & Plan** - Problem-based assessment with plan for each issue
13. **Code Status** - DNR/DNI preferences

**Discharge Summary:**
1. **Patient Information** - Demographics, dates of admission/discharge
2. **Admitting Diagnosis** - Reason for hospitalization
3. **Discharge Diagnosis** - Final diagnoses with ICD-10 codes
4. **Hospital Course** - Narrative of treatment and progress
5. **Procedures** - All procedures performed with dates
6. **Consults** - Specialist consultations obtained
7. **Discharge Medications** - Complete med list with instructions
8. **Discharge Instructions** - Activity, diet, wound care, restrictions
9. **Follow-up** - Appointments scheduled and recommended
10. **Pending Results** - Labs or studies still outstanding
11. **Patient Education** - Topics discussed and materials provided

### Workflow 3: Specialty-Specific Documentation

**Purpose:** Generate documentation templates for specific medical specialties.

**Available Specialty Templates:**

**Cardiology:**
- Chest pain evaluation
- Heart failure assessment
- Cardiac stress test interpretation
- Echocardiogram findings
- Anticoagulation management

**Psychiatry:**
- Mental status examination
- Psychiatric intake evaluation
- Therapy session notes
- Medication management visit
- Risk assessment documentation

**Pediatrics:**
- Well-child visit
- Developmental milestone documentation
- Growth chart interpretation
- Vaccination documentation
- Pediatric sick visit

**Surgery:**
- Pre-operative evaluation
- Operative note
- Post-operative check
- Surgical consultation
- Procedure note

**Emergency Medicine:**
- Emergency department note
- Trauma evaluation
- Critical care documentation
- Medical screening exam
- Transfer documentation

**Customization:** Each template includes specialty-specific:
- Relevant ROS elements
- Focused physical exam components
- Common diagnoses and differentials
- Standard treatment protocols
- Specialty-specific billing considerations

### Workflow 4: Patient Communication Documents

**Purpose:** Create patient-facing documents that explain medical information clearly.

**After-Visit Summary:**
- Visit reason and key findings
- Diagnoses explained in plain language
- Treatment plan with rationale
- Medication instructions (name, dose, frequency, purpose)
- Home care instructions
- Warning signs to watch for
- Follow-up appointments and timeline

**Patient Education Materials:**
- Condition overview (what it is, why it happens)
- Treatment options with pros/cons
- Lifestyle modifications
- Expected course and prognosis
- When to seek medical attention
- Resources for additional information

**Test Results Letter:**
- What test was performed and why
- Results in understandable terms
- What the results mean
- Next steps or follow-up needed
- Contact information for questions

**Referral Letter:**
- Clear reason for referral
- Relevant medical history
- Current symptoms and findings
- What you're asking specialist to address
- Prior treatments attempted
- Urgency level

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Generate SOAP note | "Create SOAP note for [brief encounter summary]" |
| Create H&P | "Generate admission note for [patient presentation]" |
| Discharge summary | "Create discharge summary for [hospitalization course]" |
| Specialty template | "Cardiology note for [presentation]" |
| After-visit summary | "Patient summary for [visit]" |
| Procedure note | "Document [procedure] performed on [date]" |
| Progress note | "Hospital day [X] note for [patient]" |
| Consult note | "[Specialty] consult for [reason]" |
| Patient education | "Explain [condition] to patient" |
| Translate to ICD-10 | "ICD-10 codes for [diagnoses]" |

## Best Practices

### Documentation Excellence
- **Be specific, not vague** - "2cm tender fluctuant mass" not "small abscess"
- **Use standard terminology** - Medical language for charts, plain language for patients
- **Document clinical reasoning** - Show your thought process, especially for complex cases
- **Include pertinent negatives** - What you ruled out is as important as what you found
- **Time-stamp critical events** - Document when key decisions or interventions occurred
- **Quote the patient** - Direct quotes add authenticity, especially for subjective symptoms

### HIPAA & Privacy
- **Use de-identified examples** - Never include real patient names, MRNs, or DOBs in prompts
- **Secure your workspace** - Ensure screen privacy when documenting
- **Review before finalizing** - Always verify accuracy before signing notes
- **Proper disposal** - Securely delete any AI-generated drafts containing PHI
- **Know your organization's policy** - Some healthcare systems restrict use of AI tools

### Billing Optimization
- **Support your E/M level** - Document all elements required for the level you're billing
- **Detailed HPI** - Include 4+ elements for extended HPI
- **Complete ROS** - 10+ systems for comprehensive
- **Comprehensive exam** - Document all required body areas/organ systems
- **Medical necessity** - Make clear why services were medically necessary
- **Time-based billing** - Document time spent and counseling/coordination when >50% of visit

### Clinical Decision Making
- **Differential diagnosis** - Consider and document alternative diagnoses
- **Evidence-based** - Reference guidelines when appropriate
- **Shared decision-making** - Document patient preferences and informed consent
- **Risk-benefit analysis** - Show you weighed treatment options
- **Safety netting** - Always include red flags and when to return

### Efficiency Tips
- **Use templates** - Start with structured templates, customize as needed
- **Voice dictation** - Speak your encounter, let AI structure it
- **Batch similar patients** - Document similar visits together for consistency
- **Copy-forward wisely** - Update previous notes but verify all information
- **Regular reviews** - Periodically audit your documentation for completeness and accuracy

## Medical Documentation Standards

### History of Present Illness (HPI) Elements
1. Location - Where is the symptom?
2. Quality - What does it feel like?
3. Severity - How bad is it (scale 1-10)?
4. Duration - How long has it lasted?
5. Timing - When does it occur? Constant or intermittent?
6. Context - What were you doing when it started?
7. Modifying factors - What makes it better or worse?
8. Associated signs/symptoms - What else is happening?

**Documentation levels:**
- Brief HPI: 1-3 elements
- Extended HPI: 4+ elements or status of 3+ chronic conditions

### Review of Systems (ROS) Components
1. Constitutional (fever, weight change, fatigue)
2. Eyes (vision, pain, discharge)
3. ENT (hearing, sinus, throat)
4. Cardiovascular (chest pain, palpitations, edema)
5. Respiratory (cough, SOB, wheezing)
6. GI (nausea, pain, bowel changes)
7. GU (urinary frequency, pain, discharge)
8. Musculoskeletal (joint pain, swelling, weakness)
9. Integumentary (rash, lesions, wounds)
10. Neurological (headache, dizziness, numbness)
11. Psychiatric (mood, anxiety, sleep)
12. Endocrine (heat/cold intolerance, thirst)
13. Hematologic/Lymphatic (bruising, bleeding, swelling)
14. Allergic/Immunologic (allergies, infections)

**Documentation levels:**
- Problem pertinent: 1 system
- Extended: 2-9 systems
- Complete: 10+ systems

### E/M Level Documentation Guide

**99211** - Nurse/MA visit, minimal documentation
**99212** - Problem-focused (1-2 problems, focused exam)
**99213** - Expanded (2-3 problems, expanded exam) - Most common outpatient visit
**99214** - Detailed (3-4 problems, detailed exam, moderate complexity)
**99215** - Comprehensive (4+ problems, comprehensive exam, high complexity)

**Time-based billing alternative:** If counseling/coordination >50% of visit, can bill on time alone. Must document:
- Total time spent
- What counseling/coordination was provided
- That time was >50% of visit

## Common Abbreviations & Terminology

### Physical Exam
- HEENT: Head, Eyes, Ears, Nose, Throat
- CV: Cardiovascular
- Resp: Respiratory
- Abd: Abdomen
- MSK: Musculoskeletal
- Neuro: Neurological
- NAD: No acute distress
- WNL: Within normal limits
- TTP: Tender to palpation
- ROM: Range of motion

### Clinical Status
- s/p: Status post
- r/o: Rule out
- w/u: Workup
- f/u: Follow-up
- PRN: As needed
- BID: Twice daily
- TID: Three times daily
- QID: Four times daily
- QHS: At bedtime

### Assessment & Plan
- DDx: Differential diagnosis
- Tx: Treatment
- Dx: Diagnosis
- Rx: Prescription
- Pt: Patient
- Pt ed: Patient education
- RTC: Return to clinic
- PCP: Primary care provider

## Specialty-Specific Considerations

### Primary Care
- Preventive care documentation (screenings, vaccines)
- Chronic disease management (DM, HTN, hyperlipidemia)
- Care coordination across specialties
- Medication reconciliation

### Emergency Medicine
- Medical screening examination (MSE) for EMTALA
- Emergency medical condition determination
- Discharge against medical advice (AMA) documentation
- Transfer documentation and acceptance

### Hospital Medicine
- Daily progress notes with interval events
- Condition updates and response to treatment
- Barriers to discharge
- Discharge planning documentation

### Procedural Specialties
- Pre-procedure evaluation and consent
- Procedure indication and medical necessity
- Technique and findings
- Complications and how addressed
- Post-procedure plan

## Confidence Signaling

**High Confidence Areas:**
- Standard SOAP note structure
- Common outpatient visit documentation
- After-visit summaries and patient education
- Medical terminology and abbreviations
- General documentation best practices

**Medium Confidence Areas:**
- Specialty-specific templates and terminology
- Complex billing scenarios
- Surgical and procedural documentation
- Psychiatric and behavioral health notes
- Pediatric-specific documentation

**Requires Clinical Expertise:**
- Actual diagnosis and treatment decisions
- Interpretation of labs, imaging, or tests
- Risk stratification and medical decision-making
- Prescription of medications
- Determination of medical necessity
- Anything requiring clinical judgment or licensure

## Legal & Ethical Considerations

**The Medical Record is a Legal Document:**
- Can be subpoenaed in litigation
- Subject to peer review and quality audits
- Used by payors to determine coverage
- Permanent record of care provided

**Never:**
- Falsify documentation
- Backdating entries
- Document care not provided
- Copy-forward inaccurate information
- Make derogatory comments about patients or colleagues
- Document under another provider's name

**Always:**
- Correct errors properly (addendum, not deletion)
- Be honest about mistakes or adverse events
- Document informed consent for procedures
- Note if patient refused recommended care
- Be objective and factual, not judgmental

---

**Final Reminder:** This skill assists with documentation structure and organization. All medical records must be reviewed, edited for accuracy, and signed by the licensed healthcare provider responsible for the patient's care. Clinical judgment, diagnosis, and treatment decisions require professional medical training and licensure.
