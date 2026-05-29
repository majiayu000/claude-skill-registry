---
name: "documentation"
description: "Use when writing clinical notes, documenting sessions, creating treatment plans for insurance/authorization, ensuring HIPAA compliance, or need structured documentation templates. Provides SOAP notes, progress notes (DAP format), and treatment plan templates. HIPAA-compliant guidance included."
---

# Clinical Documentation

## Description

This skill provides templates and guidance for standard clinical documentation formats used in mental health settings. Includes SOAP notes, progress notes, and treatment plan documentation.

**Clinical Context:** Clear, concise documentation supports continuity of care, meets regulatory requirements, and protects both patient and clinician. These templates provide structure while allowing for individualized clinical narrative.

## Available Templates

| Template | Purpose | Setting | Key Sections |
|----------|---------|---------|--------------|
| **SOAP Notes** | Session documentation | All settings | Subjective, Objective, Assessment, Plan |
| **Progress Notes** | Session summaries | Outpatient/residential | Varies by format (DAP, BIRP, GIRP) |
| **Treatment Plan Format** | Treatment planning documentation | All settings | Goals, objectives, interventions, timeline |

## Response Style

- Start with the relevant quick-reference template.
- Ask if the user wants the detailed examples and expanded guidance.

## Quick Reference

| Need | Use |
|------|-----|
| Session note | SOAP or DAP/BIRP/GIRP |
| Treatment plan | Treatment Plan Template |
| Safety issue | Safety Documentation Protocols |

## Interactive Mode (Lightweight)

Use this mode when the clinician asks to build a note step-by-step.

1. Confirm the note type (SOAP, DAP/BIRP/GIRP, or treatment plan) and setting.
2. Ask for required inputs one section at a time and wait for responses.
3. If information is missing or unclear, ask targeted follow-ups.
4. Draft the note and ask for confirmation or edits before finalizing.
5. If safety issues are described, prioritize safety documentation protocols.

## Usage

This skill can be invoked when you need to:
- Document therapy sessions
- Write clinical progress notes
- Format treatment plans
- Meet documentation requirements
- Ensure compliance with standards

**Example requests:**
- "Help me write a SOAP note"
- "I need a progress note template"
- "How do I document this treatment plan?"
- "What should I include in session documentation?"

## Template Details

### SOAP Notes (Standard Clinical Note Format)

**Purpose:** Systematic documentation of clinical encounters ensuring all essential elements are addressed.

**Structure:**

**S - Subjective:**
- Patient's reported symptoms, concerns, experiences
- Relevant quotes
- Changes since last session
- Current stressors

**O - Objective:**
- Observable behaviors
- Mental status examination findings
- Appearance, affect, speech, thought process
- Assessment scores (PHQ-9, GAD-7, etc.)

**A - Assessment:**
- Clinical impressions
- Progress toward goals
- Diagnosis (if applicable)
- Risk assessment summary

**P - Plan:**
- Interventions provided this session
- Homework/between-session activities
- Next session plan
- Any changes to treatment plan
- Safety planning if applicable

**SOAP Writing Guide (Quick):**
- **S:** Brief symptom summary in patient's words, changes since last session, stressors
- **O:** Mental status exam, observed behavior, validated scores (PHQ-9, GAD-7, etc.)
- **A:** Clinical impression, severity, risk assessment, progress toward goals
- **P:** Interventions delivered, homework, follow-up timing, safety plan if needed

**Example (abbreviated SOAP):**
```
S: "I've been less anxious this week but still waking at 3am."
O: MSE WNL, GAD-7 = 11 (moderate), PHQ-9 = 8 (mild)
A: Moderate anxiety with partial response; no SI/HI; risk low
P: CBT worry time, sleep hygiene plan, follow-up in 2 weeks
```

### Progress Note Formats

**DAP Notes (Data, Assessment, Plan):**
- **D - Data:** Combines subjective and objective information
- **A - Assessment:** Clinical impressions and progress
- **P - Plan:** Interventions and next steps

**BIRP Notes (Behavior, Intervention, Response, Plan):**
- **B - Behavior:** Observed client behaviors and presentation
- **I - Intervention:** What the clinician did/provided
- **R - Response:** Client's response to interventions
- **P - Plan:** Future direction

**GIRP Notes (Goals, Intervention, Response, Plan):**
- **G - Goals:** Which treatment goals were addressed
- **I - Intervention:** Techniques/modalities used
- **R - Response:** Client's engagement and response
- **P - Plan:** Next steps and homework

**Brief Examples:**

**DAP Example:**
```
D: Reports panic episodes 2x this week; sleep 5-6 hours; GAD-7=13
A: Moderate anxiety with persistent impairment; risk low
P: Continue CBT, add interoceptive exposure; follow-up in 1 week
```

**BIRP Example:**
```
B: Tearful, low energy, limited eye contact; PHQ-9=16
I: Behavioral activation and cognitive restructuring
R: Engaged, identified 2 pleasant activities
P: Activity schedule; check-in next week
```

**GIRP Example:**
```
G: Goal 1 - reduce avoidance behaviors
I: Exposure hierarchy planning
R: Patient agreed to first two steps
P: Practice exposure twice before next visit
```

### Treatment Plan Documentation

**Purpose:** Formal documentation of treatment goals, objectives, interventions, and timeline.

**Standard Components:**

1. **Identifying Information:**
   - Client demographics
   - Diagnosis(es)
   - Date of plan, review dates

2. **Problem List:**
   - Presenting problems
   - Prioritization

3. **Goals:**
   - Long-term goals (SMART format)
   - Measurable outcomes

4. **Objectives:**
   - Short-term, specific steps toward goals
   - Time-bound

5. **Interventions:**
   - Evidence-based approaches
   - Frequency and duration
   - Modality (individual, group, family)

6. **Progress Measures:**
   - How progress will be tracked
   - Specific assessments or indicators

7. **Review Schedule:**
   - When plan will be reviewed/updated
   - Discharge criteria

**Treatment Plan Template (Concise):**
```
PROBLEM:
DIAGNOSIS:

GOAL:
OBJECTIVE 1:
  Intervention:
  Responsible:
  Target Date:
OBJECTIVE 2:
  Intervention:
  Responsible:
  Target Date:

MEASUREMENT:
REVIEW FREQUENCY:
```

**Example (Condensed):**
```
PROBLEM: Depressive symptoms with functional impairment
DIAGNOSIS: Major Depressive Disorder, Moderate
GOAL: PHQ-9 < 5 within 12 weeks
OBJECTIVE 1: 3 pleasurable activities/week by week 4
  Intervention: Behavioral activation, weekly therapy
  Responsible: Therapist
  Target Date: [Date]
MEASUREMENT: PHQ-9 every 2-4 weeks
REVIEW FREQUENCY: Monthly
```

## Documentation Best Practices

**Best Practices (Expanded):**
- Use objective, behaviorally anchored language
- Document clinical reasoning for key decisions
- Include patient agreement and response to interventions
- Record safety planning steps and resources provided
- Avoid copy-forward without updating details
- Maintain clear separation of facts vs. impressions
- Follow organization and payer documentation rules
See `docs/references/documentation-standards.md` for extended guidance.

**General Principles:**
- Write clearly and concisely
- Use professional, non-judgmental language
- Document facts, not assumptions
- Include both strengths and concerns
- Date and sign all entries
- Correct errors properly (single line, initial, date)

**What to Include:**
- All safety assessments and interventions
- Informed consent discussions
- Consultation with other providers
- Changes to treatment plan
- Patient's response to treatment
- Reasons for clinical decisions

**What to Avoid:**
- Subjective judgments without supporting data
- Stigmatizing language
- Information not relevant to treatment
- Excessive detail about trauma narrative
- Legally problematic statements
- Copying/pasting without updating

**Timeliness:**
- Complete notes promptly (ideally same day)
- Follow agency/regulatory requirements
- Document safety concerns immediately

## Safety Protocols

**Documentation of safety concerns is critical:**

**Required Documentation for Safety Issues:**
- Specific risk assessment findings
- Interventions implemented
- Patient's response
- Follow-up plan
- Consultation obtained
- Resources provided

**Suicide Risk:**
- Document C-SSRS or other formal assessment
- Ideation, intent, plan, means specifics
- Protective factors
- Safety plan created
- Level of care determination rationale
- Follow-up scheduled

**Violence Risk:**
- Threat specifics (target, timeline, means)
- Duty to warn/protect actions taken
- Consultation and supervision
- Law enforcement involvement if applicable

**Child/Elder Abuse:**
- Observations leading to suspicion
- Reporting actions taken
- Report date, time, agency
- Case number if available

**Safety Documentation Protocols (Expanded):**
- Record ideation, intent, plan, means, and recent behaviors
- Document protective factors and reasons for living
- Note consultations, supervision, or collateral contacts
- Include level-of-care decision rationale
- Document crisis resources provided and patient response

## Limitations & Considerations

**Documentation serves multiple purposes:**
- Clinical communication and continuity
- Legal protection
- Regulatory compliance
- Quality improvement
- Reimbursement

**Balance competing demands:**
- Thoroughness vs. efficiency
- Detail vs. readability
- Compliance vs. clinical utility
- Privacy vs. necessary communication

**Legal Considerations:**
- Documentation can be subpoenaed
- Write assuming record could be read in court
- Follow "document defensibly" principle
- Know your jurisdiction's requirements
- Understand HIPAA and privacy regulations

**Cultural Considerations:**
- Avoid cultural assumptions
- Use patient's own language when quoting
- Note cultural factors affecting presentation
- Document cultural adaptations to treatment
- Recognize bias in interpretation

**Electronic Health Records:**
- Follow system-specific requirements
- Use templates thoughtfully (customize, don't just click)
- Maintain security/confidentiality
- Understand copy-forward risks
- Regular review of historical notes for accuracy

**Additional Limitations and Considerations:**
- Documentation requirements vary by jurisdiction and payer
- EHR templates can miss nuance; customize for the case
- Notes can be subpoenaed; write defensibly
- Balance thoroughness with privacy and minimum necessary principle

## References

**Documentation Standards:**
- American Psychological Association. Record Keeping Guidelines. Am Psychol. 2007;62(9):993-1004.
- HIPAA Privacy Rule, 45 CFR Part 160 and Subparts A and E of Part 164
- State-specific licensure board requirements

**Best Practices:**
- Mitchell RW. Documentation in Counseling Records: An Overview of Ethical, Legal, and Clinical Issues. 4th ed. American Counseling Association; 2017.
- Wiger DE, Huntley DK. Essential Interviewing: A Programmed Approach to Effective Communication. Springer; 2020.

**SOAP Note Format:**
- Weed LL. Medical records that guide and teach. N Engl J Med. 1968;278(11):593-600.

**Additional References:**
- APA Record Keeping Guidelines (2007): https://illinoispsychology.org/wp-content/uploads/2015/06/Record-Keeping-Guidelines.pdf
- HIPAA Privacy Rule (HHS): https://www.hhs.gov/hipaa/for-professionals/privacy/index.html

---

**Status:** ✅ Implemented
**Priority:** LOW - Phase 3
**Last Updated:** 2026-02-03
