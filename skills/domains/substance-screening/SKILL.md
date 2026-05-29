---
name: "substance-screening"
description: "Use when screening for alcohol or drug use concerns (heavy drinking, cravings, loss of control, withdrawal symptoms, functional impairment), assessing substance use severity, determining level of care, or patient reports substance-related problems. Provides AUDIT-C (alcohol brief) and DAST-10 (drugs comprehensive) assessments."
---

# Substance Use Screening

## Description

This skill helps administer and interpret validated substance use screening instruments. The AUDIT-C assesses alcohol use patterns, while the DAST-10 screens for drug use problems.

**Clinical Context:** These tools help identify problematic substance use, assess severity, and support clinical decision-making about further evaluation or intervention. They are support tools that supplement, not replace, comprehensive substance use assessment.

**IMPORTANT: Screen for BOTH alcohol (AUDIT-C) and drugs (DAST-10).** They often co-occur and require different assessment and treatment approaches.

## Quick Reference: Assessment Selection

| Assessment | Items | Time | Substance | Cutoff | When to Use |
|------------|-------|------|-----------|--------|-------------|
| **AUDIT-C** | 3 | < 1 min | Alcohol only | Men ≥4, Women ≥3 | Universal screening, primary care |
| **DAST-10** | 10 | 2-3 min | Drugs (not alcohol) | ≥3 | Universal screening, any clinical setting |
| **Full AUDIT** | 10 | 3-5 min | Alcohol only | ≥8 | After positive AUDIT-C, comprehensive assessment |

**Recommended approach:** Use AUDIT-C + DAST-10 together for complete substance use screening. See [references/screening-comparison.md](references/screening-comparison.md) for detailed guidance.

### Assessment Selection Decision Tree

```dot
digraph assessment_selection {
    rankdir=TB;
    node [shape=box, style=rounded];

    start [label="Substance Use\nScreening", shape=ellipse];
    both [label="SCREEN BOTH:\nAUDIT-C (alcohol)\n+\nDAST-10 (drugs)", style="filled", fillcolor=lightblue];

    audit_result [label="AUDIT-C\nPositive?", shape=diamond];
    dast_result [label="DAST-10\nPositive?", shape=diamond];

    alcohol_only [label="Alcohol Use\nIssue Only", style="filled", fillcolor=yellow];
    drugs_only [label="Drug Use\nIssue Only", style="filled", fillcolor=yellow];
    both_positive [label="Both Alcohol\nAND Drugs", style="filled", fillcolor=orange];
    neither [label="Negative\nScreens\nRoutine f/u", style="filled", fillcolor=lightgreen];

    full_audit [label="Consider\nFull AUDIT\n(if AUDIT-C ≥6)", shape=box];
    intervention [label="Brief\nIntervention\nor\nReferral", style="filled", fillcolor=lightblue];

    start -> both;
    both -> audit_result;
    audit_result -> dast_result [label="yes"];
    audit_result -> dast_result [label="no"];

    dast_result -> both_positive [label="AUDIT yes\nDAST yes"];
    dast_result -> alcohol_only [label="AUDIT yes\nDAST no"];
    dast_result -> drugs_only [label="AUDIT no\nDAST yes"];
    dast_result -> neither [label="both no"];

    alcohol_only -> full_audit;
    drugs_only -> intervention;
    both_positive -> intervention;
    full_audit -> intervention;
}
```

## Interactive Administration (Optional)

Use this mode when the clinician says "start" or "administer" AUDIT-C and/or DAST-10.

1. Confirm whether to administer AUDIT-C, DAST-10, or both (recommended: both).
2. Explain the time frame and response format for each instrument.
3. Ask one item at a time (verbatim from the asset file) and wait for a response before continuing.
4. Accept numeric or verbal responses; if unclear or out of range, ask for clarification.
5. Record each response and keep running totals (remember DAST-10 Item 3 is reverse scored).
6. After each instrument, calculate totals, interpret severity, and provide next-step guidance.
7. Offer a brief documentation summary if requested.

## Usage

**Example requests:** "Screen for alcohol use", "Administer DAST-10", "Score AUDIT-C", "Interpret substance screening"

## Quick Reference: Severity Levels

### AUDIT-C Interpretation (Alcohol)

**Men:**
- **0-3:** Low risk - Annual rescreening
- **4-5:** Hazardous drinking - Brief intervention
- **6-7:** Harmful/high risk - Brief intervention + full AUDIT, consider referral
- **8-12:** Severe risk - Specialty addiction treatment referral required

**Women:**
- **0-2:** Low risk - Annual rescreening
- **3-4:** Hazardous drinking - Brief intervention
- **5-7:** Harmful/high risk - Brief intervention + full AUDIT, consider referral
- **8-12:** Severe risk - Specialty addiction treatment referral required

### DAST-10 Interpretation (Drugs)

- **0-2:** No/minimal risk - Routine monitoring
- **3-5:** Moderate risk - Comprehensive assessment, consider outpatient treatment
- **6-8:** Substantial risk - Specialty addiction treatment referral required
- **9-10:** Severe risk - Immediate specialty referral, higher level of care

For detailed severity interpretations and treatment recommendations, see [references/severity-levels.md](references/severity-levels.md)

## Assessment Administration

### AUDIT-C (Alcohol Use Disorders Identification Test - Concise)

**Complete details:** [assets/audit-c.md](assets/audit-c.md)

**Items (0-4 each):** 1) Drinking frequency, 2) Drinks per day, 3) Binge drinking frequency

**Scoring:** Total 0-12. Men ≥4, Women ≥3 = positive. **Standard drink:** 12oz beer, 5oz wine, 1.5oz spirits.

**Next Steps:** Below cutoff → annual rescreen. 4-7 (M) or 3-7 (W) → brief intervention, f/u 1-3mo. ≥8 → full AUDIT + referral.

### DAST-10 (Drug Abuse Screening Test - 10 Item)

**Complete details:** [assets/dast-10.md](assets/dast-10.md)

**Format:** 10 Yes/No questions, past 12 months, excludes alcohol/tobacco. Covers use beyond medical reasons, polysubstance, loss of control, blackouts, guilt, family issues, illegal activities, withdrawal, medical complications. Item 3 reverse scored.

**Scoring:** Total 0-10. 1 point per "Yes" (except Item 3). ≥3 = problematic use.

**Next Steps:** 0-2 → monitor. ≥3 → detailed history (substances, frequency, route). Opioids → MAT discussion. Injection use → infectious disease screening.

## Clinical Decision-Making

### Severity to Intervention Pathway

```dot
digraph severity_intervention {
    rankdir=TB;
    node [shape=box, style=rounded];

    audit [label="AUDIT-C\nScore", shape=ellipse];
    dast [label="DAST-10\nScore", shape=ellipse];

    audit_low [label="0-3 (Men)\n0-2 (Women)", shape=box];
    audit_haz [label="4-5 (Men)\n3-4 (Women)", shape=box];
    audit_harmful [label="6-7 (Men)\n5-7 (Women)", shape=box];
    audit_severe [label="≥8", shape=box];

    dast_low [label="0-2", shape=box];
    dast_mod [label="3-5", shape=box];
    dast_sub [label="6-8", shape=box];
    dast_severe [label="9-10", shape=box];

    tx_none [label="Annual\nRescreening", style="filled", fillcolor=lightgreen];
    tx_brief [label="Brief\nIntervention\n(5-15 min)", style="filled", fillcolor=yellow];
    tx_bi_refer [label="Brief Intervention\n+ Full AUDIT\n+ Consider Referral", style="filled", fillcolor=orange];
    tx_specialty [label="Specialty\nAddiction\nTreatment", style="filled", fillcolor=red, fontcolor=white];

    tx_monitor [label="Routine\nMonitoring", style="filled", fillcolor=lightgreen];
    tx_assess [label="Comprehensive\nAssessment\nOutpatient Option", style="filled", fillcolor=yellow];
    tx_refer [label="Specialty Referral\nMAT if Opioids", style="filled", fillcolor=orange];
    tx_immediate [label="Immediate Referral\nHigher LOC", style="filled", fillcolor=red, fontcolor=white];

    audit -> audit_low;
    audit -> audit_haz;
    audit -> audit_harmful;
    audit -> audit_severe;

    dast -> dast_low;
    dast -> dast_mod;
    dast -> dast_sub;
    dast -> dast_severe;

    audit_low -> tx_none;
    audit_haz -> tx_brief;
    audit_harmful -> tx_bi_refer;
    audit_severe -> tx_specialty;

    dast_low -> tx_monitor;
    dast_mod -> tx_assess;
    dast_sub -> tx_refer;
    dast_severe -> tx_immediate;
}
```

For structured clinical decision trees covering screening pathways, treatment selection, withdrawal management, and co-occurring disorders, see [references/clinical-decision-trees.md](references/clinical-decision-trees.md)

**Substance-Specific:** **Opioids:** MAT immediately (buprenorphine, methadone, naltrexone), naloxone for all. **Stimulants:** Behavioral therapies, cardiac/psychiatric evaluation. **Benzodiazepines:** Never abrupt stop (seizure risk), supervised taper required.

## Brief Intervention for Positive AUDIT-C (4-7 range)

**Components (5-15 min):** Provide feedback (compare to low-risk guidelines), assess readiness, set goals, provide resources, follow-up in 1-3 months. **Low-risk limits:** Men ≤14/week, ≤4/day; Women ≤7/week, ≤3/day.

## Safety Protocols

**Approach:** Non-judgmental, confidential. Normalize screening, use non-stigmatizing language.

**Immediate Concerns:** Acute intoxication/withdrawal → medical evaluation. Alcohol/benzodiazepine withdrawal → supervised detox (seizure risk). Opioids → MAT + naloxone. Injection use → infectious disease screening. Suicidal ideation → crisis intervention per [../../docs/references/crisis-protocols.md](../../docs/references/crisis-protocols.md).

**Crisis Resources:** SAMHSA 1-800-662-4357, 988 Lifeline, Text HOME to 741741, Emergency 911

## Documentation

**AUDIT-C template:** [assets/audit-c.md](assets/audit-c.md) - Include 3 items, score, gender/cutoff, result, risk level, brief intervention, follow-up.

**DAST-10 template:** [assets/dast-10.md](assets/dast-10.md) - Include 10 items, score, risk level, substances, red flags (injection/opioids/withdrawal), recommendations, safety, naloxone if needed.

**Standards:** [../../docs/references/documentation-standards.md](../../docs/references/documentation-standards.md)

## Limitations & Considerations

**Support tool, not diagnostic:** Self-report may underestimate use. Requires clinical context interpretation. Cultural factors affect disclosure. Clinical judgment supersedes scores. Use non-judgmental, motivational approach. Avoid stigmatizing language; use "person with substance use disorder," "person in recovery."

**Special Populations:** Pregnancy (immediate perinatal referral), adolescents (use CRAFFT), older adults (lower cutoffs, medication interactions), chronic pain (assess prescription use).

**Comorbidity:** High rates of depression (30-50%), anxiety (20-30%), PTSD (30-50%), suicidal ideation. Screen with ../../depression-screening/, ../../anxiety-screening/, ../../trauma-screening/, ../../suicide-screening/. Integrated treatment required.

## Workflow Integration

**Related workflows:** ../../intake-interview/ (comprehensive intake), ../../treatment-planning/ (substance treatment plans), ../../documentation/ (progress notes). See [../../docs/references/crisis-protocols.md](../../docs/references/crisis-protocols.md) and [../../docs/references/referral-guidelines.md](../../docs/references/referral-guidelines.md).

## Additional Resources

**Detailed guidance:** [references/severity-levels.md](references/severity-levels.md), [references/screening-comparison.md](references/screening-comparison.md), [references/clinical-decision-trees.md](references/clinical-decision-trees.md)

**External:** https://findtreatment.gov (SAMHSA), https://aa.org, https://na.org, https://smartrecovery.org

## References

**AUDIT-C:**
- Bush K, Kivlahan DR, McDonell MB, Fihn SD, Bradley KA. The AUDIT alcohol consumption questions (AUDIT-C): an effective brief screening test for problem drinking. Arch Intern Med. 1998;158(16):1789-1795.
- Bradley KA, DeBenedetti AF, Volk RJ, Williams EC, Frank D, Kivlahan DR. AUDIT-C as a brief screen for alcohol misuse in primary care. Alcohol Clin Exp Res. 2007;31(7):1208-1217.

**DAST-10:**
- Skinner HA. The drug abuse screening test. Addict Behav. 1982;7(4):363-371.
- Yudko E, Lozhkina O, Fouts A. A comprehensive review of the psychometric properties of the Drug Abuse Screening Test. J Subst Abuse Treat. 2007;32(2):189-198.

**Freely available for clinical and research use**
