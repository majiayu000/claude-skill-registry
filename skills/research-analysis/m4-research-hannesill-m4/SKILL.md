---
name: m4-research
description: Start a structured clinical research session. Triggers on "/research", "start research", "new study", "analyze cohort", "investigate hypothesis", "research question", or when users describe clinical research goals. Interviews the user, then produces a rigorous research plan.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: both
  category: research-workflow
  validated: true
---

# M4 Clinical Research Workflow

This skill guides you through a structured clinical research session. It ensures scientific rigor from hypothesis formation through analysis execution.

## When This Skill Activates

- User invokes `/research` command
- User describes research intent: "I want to study...", "Can we analyze...", "What's the mortality rate for..."
- User mentions cohort analysis, hypothesis testing, or comparative studies

## Phase 1: Research Interview

**Before writing any queries, interview the user to establish:**

### 1. Research Question
Ask: "What specific clinical question are you trying to answer?"

Good questions are:
- Specific and answerable with available data
- Clinically meaningful
- Novel or confirmatory of existing findings

Help refine vague questions:
- "Are sicker patients dying more?" → "Is day-1 SOFA score independently associated with 30-day mortality in sepsis patients?"

### 2. Study Design
Ask: "What type of study is this?"

- **Descriptive**: Characterize a population (demographics, distributions)
- **Comparative**: Compare groups (exposed vs unexposed, treatment A vs B)
- **Predictive**: Build or validate a prediction model
- **Exploratory**: Hypothesis-generating analysis

### 3. Outcome Variable
Ask: "What is your primary outcome?"

Common outcomes and how to define them:
- **In-hospital mortality**: `hospital_expire_flag` in admissions table
- **30-day mortality**: Compare `dod` to discharge time + 30 days
- **ICU length of stay**: `los` in icustays, be wary of survivor bias
- **Ventilation duration**: Requires careful definition (see m4 skills)
- **Readmission**: Subsequent `hadm_id` for same `subject_id`

### 4. Exposure/Intervention
Ask: "What exposure or intervention are you studying?"

For treatment comparisons:
- How is treatment defined? (any use vs duration vs dose)
- When is exposure status determined? (admission, 24h, 48h)
- What's the comparator? (no treatment, alternative treatment)

### 5. Population (Inclusion/Exclusion)
Ask: "Who should be included in this study?"

Standard considerations:
- First ICU stay only? (avoid correlated observations)
- Age restrictions? (pediatric exclusion common)
- Minimum ICU stay? (be careful of immortal time bias)
- Specific diagnoses? (how defined - ICD codes have limitations)

### 6. Confounders
Ask: "What factors might confound your results?"

Common confounders in ICU research:
- Age, sex, comorbidities
- Illness severity (SOFA, APACHE, SAPS)
- Admission type (medical vs surgical vs trauma)
- Hospital/unit effects

### 7. Dataset Selection
Ask: "Which dataset should we use?"

- **mimic-iv**: Full MIMIC-IV (requires access)
- **mimic-iv-demo**: 100 patients, good for testing queries
- **mimic-iv-note**: MIMIC-IV with clinical notes
- **eicu**: Multi-center ICU data (different schema)

---

## Phase 2: Draft Research Protocol

After the interview, produce a structured research plan:

```markdown
## Research Protocol: [Title]

### Research Question
[Specific, answerable question]

### Hypothesis
[If applicable - null and alternative]

### Study Design
[Descriptive/Comparative/Predictive/Exploratory]

### Dataset
[Selected dataset with justification]

### Population
**Inclusion Criteria:**
- [Criterion 1]
- [Criterion 2]

**Exclusion Criteria:**
- [Criterion 1]
- [Criterion 2]

### Variables
**Primary Outcome:** [Definition and how measured]
**Exposure:** [Definition and timing]
**Covariates:** [List with definitions]

### Analysis Plan
1. [Step 1]
2. [Step 2]
...

### Potential Biases & Limitations
- [Known limitation 1]
- [Known limitation 2]

### M4 Skills to Use
- [Relevant skill 1]: [Why]
- [Relevant skill 2]: [Why]
```

---

## Phase 3: Scientific Integrity Guardrails

**Apply these checks throughout the analysis:**

### Bias Prevention

**Immortal Time Bias**
- Define exposure at a FIXED time point (admission, 24h, 48h)
- Never use "ever received during stay" for treatments
- Use landmark analysis when appropriate

**Selection Bias**
- Report all exclusions with counts (CONSORT diagram)
- Analyze whether excluded patients differ
- Avoid conditioning on post-treatment variables

**Information Leakage**
- ICD codes are assigned at DISCHARGE - don't use for admission predictions
- Length of stay is only known at discharge
- Labs/vitals must be timestamped appropriately

**Confounding by Indication**
- Treatments are given to sicker patients
- Always adjust for severity (SOFA, APACHE, SAPS)
- Consider propensity scores for treatment comparisons

### Statistical Rigor

**Multiple Comparisons**
- Pre-specify primary outcome
- Apply Bonferroni/FDR correction for secondary analyses
- Report all analyses performed, not just significant ones

**Sample Size**
- Report cohort sizes at each step
- Be cautious with small subgroups
- Consider power for planned comparisons

**Missing Data**
- Report missingness rates for all variables
- Consider imputation vs complete case analysis
- Perform sensitivity analyses

### Reproducibility

**Query Documentation**
- Save all SQL queries with timestamps
- Document data versions used
- Note any manual data cleaning steps

**Analysis Trail**
- Number analyses sequentially
- Distinguish exploratory from confirmatory
- Record decision points and rationale

---

## Phase 4: Using M4 Skills

**Match skills to research needs:**

### Severity Scores
Use when adjusting for baseline illness severity:

| Skill | When to Use |
|-------|-------------|
| `sofa-score` | Organ dysfunction assessment, Sepsis-3 criteria |
| `apsiii-score` | Comprehensive severity with mortality prediction |
| `sapsii-score` | Alternative to APACHE, mortality prediction |
| `oasis-score` | When labs unavailable (uses vitals only) |
| `sirs-criteria` | Historical sepsis definition, comparison studies |

### Cohort Definitions
Use when defining study populations:

| Skill | When to Use |
|-------|-------------|
| `sepsis-3-cohort` | Sepsis studies (SOFA >= 2 + suspected infection) |
| `first-icu-stay` | Avoid correlated observations |
| `suspicion-of-infection` | Infection timing (antibiotics + cultures) |

### Clinical Concepts
Use when defining exposures or outcomes:

| Skill | When to Use |
|-------|-------------|
| `kdigo-aki-staging` | AKI as outcome or covariate |
| `vasopressor-equivalents` | Standardize vasopressor doses |
| `baseline-creatinine` | AKI baseline reference |
| `gcs-calculation` | Neurological status |

### Data Quality
Use when building queries:

| Skill | When to Use |
|-------|-------------|
| `clinical-research-pitfalls` | Review for common errors |
| `mimic-table-relationships` | Understanding joins |
| `mimic-eicu-mapping` | Cross-dataset queries |

### Code Execution
Use for complex analyses:

| Skill | When to Use |
|-------|-------------|
| `m4-api` | Multi-step analysis, large results, statistical tests |

---

## Example Interview Flow

**User**: "I want to study if early vasopressor use affects mortality in sepsis"

**AI Interview**:

1. **Research Question**: "Let me help refine this. By 'early', do you mean within 1 hour, 6 hours, or 24 hours of sepsis onset? And by 'mortality', do you mean in-hospital, 28-day, or 90-day?"

2. **Study Design**: "This is a comparative study - you're comparing early vs. late/no vasopressor use. We'll need to carefully define the comparison groups to avoid immortal time bias."

3. **Outcome**: "Let's use 28-day mortality so we capture both in-hospital and post-discharge deaths."

4. **Exposure**: "I recommend defining 'early' as vasopressor initiation within 6 hours of suspected infection onset (using the suspicion-of-infection skill). The comparison group would be those who received vasopressors >6h or never."

5. **Population**: "I suggest: adult patients (>=18), first ICU stay, meeting Sepsis-3 criteria. Exclude patients who died within 6 hours (immortal time) and those on vasopressors at admission."

6. **Confounders**: "We should adjust for: age, SOFA score at sepsis onset, admission source, comorbidities. I recommend using propensity score matching given this is an observational treatment comparison."

7. **Dataset**: "Let's use mimic-iv. The demo dataset is too small for treatment effect studies."

---

## Common Research Patterns

### Pattern: Mortality Risk Factors
```
1. Define cohort (first-icu-stay)
2. Extract baseline characteristics
3. Calculate severity (sofa-score or apsiii-score)
4. Define mortality outcome
5. Multivariable regression
```

### Pattern: Treatment Effect
```
1. Define cohort and time zero
2. Define exposure window (fixed time)
3. Extract confounders at baseline
4. Propensity score matching
5. Compare outcomes
```

### Pattern: Cohort Description
```
1. Define cohort
2. Demographics, comorbidities
3. Severity scores
4. Treatments received
5. Outcomes (mortality, LOS, complications)
```

---

## Red Flags to Watch For

Stop and reconsider if you see:

- **"Patients who survived to receive..."** → Immortal time bias
- **"Using ICD codes to identify patients at admission"** → Information leakage
- **"Complete cases only (N drops from X to Y)"** → Selection bias
- **"Treatment group had higher mortality"** → Confounding by indication
- **"We found 47 significant associations"** → Multiple comparisons
- **"Small sample size but p < 0.05"** → Underpowered, likely false positive

---

## After Analysis Completion

1. **Summarize findings** with effect sizes and confidence intervals
2. **Acknowledge limitations** explicitly
3. **Suggest validation** on independent data (e.g., eICU if used MIMIC)
4. **Provide reproducibility info**: queries used, cohort flow, data version
