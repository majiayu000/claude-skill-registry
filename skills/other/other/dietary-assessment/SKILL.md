---
name: dietary-assessment
description: Methods for assessing what people actually eat — 24-hour recall, food frequency questionnaires, diet diaries, biomarkers, duplicate-plate studies, and controlled feeding. Covers the relative strengths and biases of each instrument, how to choose among them for a given question, and how to interpret results in the presence of measurement error. Use when a user wants to estimate population-level intake, individual-level intake, or evaluate the plausibility of a dietary claim that depends on how intake was measured.
type: skill
category: nutrition
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/nutrition/dietary-assessment/SKILL.md
superseded_by: null
---
# Dietary Assessment

"What do people actually eat?" is harder to answer than it looks. Every large claim about diet and health depends on answering it for thousands of people over months or years, and every instrument that attempts to do so has known biases. This skill catalogs the common instruments, documents the biases each one introduces, and gives heuristics for choosing the right tool for a question and reading the resulting numbers with appropriate skepticism.

**Agent affinity:** lind (controlled-trial design), ancel-keys (population-scale dietary assessment)

**Concept IDs:** nutrition-assessment-methods, nutrition-study-design, nutrition-measurement-error

## The instrument menu

### 24-hour dietary recall

**What it is.** A trained interviewer walks the participant through everything eaten and drunk in the previous 24 hours, prompting with portion-size aids and a multi-pass protocol (quick list, meal structure, forgotten-foods probe, detail pass, final review). The USDA Automated Multiple-Pass Method is the reference implementation.

**Strengths.** Open-ended; captures foods not on any predefined list. Short-term memory is more accurate than long-term. With multiple non-consecutive recalls, can estimate usual intake with statistical modeling (the National Cancer Institute method).

**Weaknesses.** A single recall does not represent habitual intake; day-to-day variability is large. Portion-size estimation is imprecise without aids. Respondents still underreport energy — roughly 10–15% on average in the AMPM, better than FFQ but not negligible.

**When to use.** Short-term energy-balance studies, nutrient-intake estimates for large surveys (NHANES uses two recalls per participant), situations where the food list is unknown in advance.

### Food frequency questionnaire (FFQ)

**What it is.** A structured questionnaire asking how often the respondent has eaten each of 100–150 foods over a reference period (typically the past year), with optional portion-size questions.

**Strengths.** Cheap, rapid, low respondent burden. Well-suited to ranking people for relative-risk epidemiology. Historically the instrument of choice for cohort studies like Nurses' Health, EPIC, and the Harvard cohorts.

**Weaknesses.** Underreporting of total energy intake is routinely 20–30% and is not random — foods perceived as unhealthy are differentially underreported. Long reference period strains memory. The food list constrains what can be reported. Portion-size estimation over a year is nearly impossible. FFQ-based studies with small effect sizes should be read with substantial skepticism.

**When to use.** Large cohort studies focused on ranking, not absolute intake. Do not use for clinical or individual-level assessment.

### Weighed food diary

**What it is.** The participant weighs and records every food and drink consumed for a period (typically 3–7 days), ideally with a digital scale.

**Strengths.** More accurate than recall for the days actually recorded. Portion sizes are measured, not estimated.

**Weaknesses.** High respondent burden; compliance drops over time. Recording changes behavior — participants simplify their diets to make recording easier. Still does not represent habitual intake unless multiple diaries are collected.

**When to use.** Shorter-duration metabolic studies where burden can be tolerated; validation studies for other instruments.

### Duplicate-plate study

**What it is.** The participant serves and eats a normal meal, then plates an identical second serving that is collected and chemically analyzed. This removes the estimation step from recall.

**Strengths.** Nutrient content is measured directly from the actual food eaten. Excellent for trace-element studies where food database uncertainty is large.

**Weaknesses.** Extremely burdensome; participants know they are being measured. Expensive. Used in specialized contexts only.

**When to use.** Trace-element studies, contamination studies, validation of nutrient databases.

### Biomarkers of intake

**What it is.** Biological samples (urine, blood, hair, adipose) are measured for compounds that reflect recent or longer-term intake of specific nutrients or foods.

**Examples.**

- **Doubly labeled water** — gold-standard measure of total energy expenditure and, in weight-stable subjects, energy intake. Participant drinks water labeled with deuterium and oxygen-18; their differential excretion rates reveal CO2 production, which reflects energy expenditure.
- **24-hour urinary nitrogen** — recovers ~80% of protein intake; used to validate protein recall.
- **24-hour urinary potassium** — recovers potassium intake reasonably well; biomarker for fruit and vegetable consumption.
- **Adipose tissue fatty acids** — reflect longer-term fat intake, especially for fatty acids the body cannot synthesize.
- **Plasma carotenoids** — biomarker for fruit and vegetable intake.

**Strengths.** Objective — no reliance on respondent memory. Resistant to motivated underreporting.

**Weaknesses.** Expensive. Not available for every nutrient. Some biomarkers are short-term (plasma) and some long-term (adipose); interpretation depends on which.

**When to use.** Validation of dietary instruments. Specific-nutrient studies where the biomarker is well-characterized. Situations where motivated reporting bias is expected.

### Controlled feeding study

**What it is.** The study provides all food to participants for a defined period. Intake is known exactly. Typically conducted in metabolic wards for full control, or as provided-meal studies for less control but more generalizability.

**Strengths.** Intake is known, not estimated. Ideal for mechanism studies, metabolic endpoints, short-term clinical outcomes.

**Weaknesses.** Expensive. Short duration (rarely more than 4–8 weeks, sometimes longer in ward settings). Artificial — people do not eat prescribed diets in real life, and observed responses may not persist when participants return to self-selected diets.

**When to use.** When the research question is about metabolic mechanism or short-term clinical endpoint. When a controlled comparison of two dietary patterns is essential and observational confounding would be fatal.

## Choosing an instrument — decision protocol

### Step 1 — What is the question?

- Is the question about **population-level intake patterns**? → 24-hour recall (NHANES-style), ideally with multiple recalls and NCI usual-intake modeling.
- Is the question about **individual-level adequacy** for a clinical assessment? → Multiple 24-hour recalls or a weighed diary, supplemented with biomarkers if available.
- Is the question about **long-term intake and chronic disease** in a cohort? → FFQ, understanding that ranking is the realistic goal and absolute intake is not.
- Is the question about **a specific metabolic response to a dietary change**? → Controlled feeding, ideally inpatient.
- Is the question about **validating a self-report instrument**? → Biomarker study.

### Step 2 — What is the target measurement accuracy?

If the hypothesized effect size is small (e.g., a 10% difference in relative risk), the instrument's measurement error must be substantially smaller than the effect. FFQ-based studies with small effect sizes cannot be distinguished from noise. If the effect is large (e.g., scurvy cured vs. not cured), even crude instruments suffice.

### Step 3 — Will the population comply?

High-burden instruments (weighed diary, controlled feeding, duplicate plate) drop motivated participants disproportionately, biasing the sample. Lower-burden instruments (FFQ) retain more participants but produce noisier data.

## Worked example — reading an FFQ-based relative-risk claim

A 2016 cohort study reports that participants in the highest quintile of "red meat intake" (measured by FFQ) have a 16% higher risk of colorectal cancer than those in the lowest quintile.

How should the department read this claim?

1. **Instrument fit.** FFQ is standard for long-term cohort studies, so the instrument choice is defensible. However, red meat is one of the foods most susceptible to misclassification: participants conflate beef with ground beef, processed meats with unprocessed, and may differentially underreport after health warnings.
2. **Effect size vs. measurement error.** The 16% relative-risk difference is at the edge of what FFQ studies can reliably detect. The confidence interval will likely span 1.05–1.30; the point estimate is plausible but fragile.
3. **Confounding.** Red-meat consumers differ from non-consumers in exercise, smoking, education, income, and other cancer risk factors. Even with adjustment, residual confounding is substantial in this range.
4. **Replication.** Has this been replicated in other cohorts with similar methodology? Is the effect consistent across cohorts? Does it replicate in controlled feeding (which can address mechanism but not the cancer outcome directly)?
5. **Report.** "This is plausible but not definitive evidence of a small effect. The IARC classification of red meat as probably carcinogenic rests on this body of work. The effect is small enough that individual dietary decisions should weight it against other factors."

## Worked example — an FFQ-vs-biomarker discrepancy

A study validates an FFQ against doubly labeled water in 450 women. The FFQ estimates mean energy intake at 1,720 kcal/day. Doubly labeled water estimates total energy expenditure (and, in weight-stable subjects, intake) at 2,350 kcal/day.

**Reading.** The FFQ underestimates intake by 630 kcal — about 27%. This is consistent with known underreporting in FFQs. The practical implication: this FFQ cannot be used to estimate absolute intake. It may still be useful for ranking people, but only if the underreporting is proportional across participants. Further analysis would examine whether underreporting differs systematically by BMI (it usually does — heavier participants underreport more), education, or diet quality.

## Assessment protocol for a "what should I eat" question

The dietary assessment skill does not answer "what should I eat." It answers "how would we know what you are eating." When a user asks the former question, the appropriate response is to identify the measurement goal and collect data with an instrument fit to the goal:

1. **Clarify the purpose.** Is the user asking about caloric intake, specific nutrients, dietary patterns, or disease risk? Different purposes require different instruments.
2. **Choose the instrument.** Apply the decision protocol above.
3. **Document the measurement error.** Every assessment should report the expected accuracy range for the chosen instrument.
4. **Interpret within measurement error.** A user asking whether 85% RDA for iron is adequate should be told that their instrument probably has 15–25% measurement error, so the answer depends on whether the true value is closer to 70% or 100%.

## Routing heuristics

- Questions about **epidemiology study methodology** → lind or ancel-keys.
- Questions about **how calories are measured** → atwater.
- Questions about **clinical nutritional assessment** → clinical protocols out of this skill; direct to a dietetics team.
- Questions about **whether a widely reported dietary claim is solid** → ancel-keys or marion-nestle depending on whether the claim is methodological or political.

## Common failure modes

- **Reporting an FFQ-based absolute intake** as if it were the truth. It is almost always an underestimate.
- **Comparing two cohorts using different instruments** as if the numbers were comparable.
- **Using a single 24-hour recall** to characterize a person's habitual diet.
- **Skipping biomarker validation** for studies whose effect size is small.
- **Using controlled feeding to generalize to free-living diets** without acknowledging the extrapolation.

## Further reading

- Thompson and Subar, 2017, *Nutrition in the Prevention and Treatment of Disease*, chapter on dietary assessment methods
- Freedman et al., 2014, *Pooled results from 5 validation studies of dietary self-report instruments using recovery biomarkers for energy and protein intake*
- NCI method for usual-intake estimation
- Institute of Medicine, *Dietary Reference Intakes: Applications in Dietary Assessment*
