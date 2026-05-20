---
name: research-methods-psych
description: Research methodology in psychology. Covers experimental design (independent/dependent variables, random assignment, control conditions, between/within-subjects designs), research ethics (informed consent, deception, debriefing, IRB review, APA ethical principles), statistical methods in psychology (null hypothesis significance testing, p-values, effect sizes, confidence intervals, power analysis), and the replication crisis (publication bias, p-hacking, questionable research practices, preregistration, open science). Use when designing psychological research, evaluating study quality, interpreting statistical findings, or discussing methodological rigor in psychology.
type: skill
category: psychology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/psychology/research-methods-psych/SKILL.md
superseded_by: null
---
# Research Methods in Psychology

Psychology's claim to be a science rests on its methods. Unlike philosophy or folk wisdom, psychology makes empirical claims testable through systematic observation and experimentation. This skill covers the experimental method as applied in psychological research, the ethical framework governing human subjects research, the statistical tools used to evaluate evidence, and the ongoing replication crisis that has forced the field to confront its methodological shortcomings.

**Agent affinity:** kahneman (research design, statistical thinking), james (methodological pragmatism, what constitutes evidence)

**Concept IDs:** psych-perception-construction, psych-cognitive-biases, psych-social-influence, psych-learning-theory

## Research Methods at a Glance

| # | Domain | Core Question | Key Concepts |
|---|---|---|---|
| 1 | Experimental design | How do we establish causation? | IV/DV, random assignment, control, confounds |
| 2 | Non-experimental methods | How do we study what we cannot manipulate? | Correlation, observation, case studies, surveys |
| 3 | Research ethics | How do we protect participants? | Informed consent, deception, debriefing, IRB |
| 4 | Statistics in psychology | How do we evaluate evidence? | NHST, effect size, confidence intervals, power |
| 5 | The replication crisis | Can we trust published findings? | Publication bias, p-hacking, preregistration |

## Domain 1 -- Experimental Design

### The logic of experimentation

An experiment establishes causation by manipulating one variable (the independent variable, IV) while holding all other variables constant, and measuring the effect on another variable (the dependent variable, DV). Random assignment to conditions ensures that participant characteristics are distributed evenly across groups, eliminating systematic confounds.

### Key elements

- **Independent variable (IV)** -- the factor the researcher manipulates. Must have at least two levels (e.g., treatment vs. control).
- **Dependent variable (DV)** -- the outcome measured. Must be operationally defined (e.g., "anxiety" measured by the Beck Anxiety Inventory score, not a vague assessment).
- **Random assignment** -- each participant has an equal chance of being assigned to any condition. This is what distinguishes a true experiment from a quasi-experiment.
- **Control condition** -- a comparison group that does not receive the treatment. May be no-treatment, waitlist, active control (alternative treatment), or placebo.
- **Confound** -- a variable that varies systematically with the IV, making it impossible to determine which caused the effect on the DV.

### Between-subjects vs. within-subjects

| Design | Each participant | Advantage | Disadvantage |
|---|---|---|---|
| **Between-subjects** | Experiences one condition | No order effects, no demand characteristics from multiple testing | Needs more participants, individual differences add noise |
| **Within-subjects (repeated measures)** | Experiences all conditions | Each participant serves as their own control, more statistical power | Order effects, practice effects, fatigue |
| **Mixed** | Between on one IV, within on another | Combines advantages | Complexity in analysis and interpretation |

Counterbalancing (varying the order of conditions across participants) controls for order effects in within-subjects designs.

### Factorial designs

When two or more IVs are crossed (every level of each IV is combined with every level of every other IV), the design is factorial. A 2x3 factorial has 6 conditions. Factorial designs reveal main effects (the effect of each IV averaging over others) and interactions (the effect of one IV depends on the level of another). Interactions are often more theoretically interesting than main effects.

### Validity

- **Internal validity** -- confidence that the IV caused the change in the DV. Threatened by confounds, selection bias, maturation, history, and attrition.
- **External validity** -- generalizability to other populations, settings, and times. Threatened by non-representative samples, artificial laboratory settings, and demand characteristics.
- **Construct validity** -- the degree to which the IV and DV actually measure the constructs of interest.
- **Statistical conclusion validity** -- appropriate use of statistical tests, adequate sample size, and correct interpretation of results.

## Domain 2 -- Non-Experimental Methods

### Correlational research

Measures the relationship between two variables without manipulating either. Correlation does not establish causation because of the third-variable problem (an unmeasured variable may cause both) and the directionality problem (does A cause B or B cause A?). Correlation coefficients range from -1 to +1; the sign indicates direction, the magnitude indicates strength.

### Observational methods

- **Naturalistic observation** -- observing behavior in its natural setting without intervention. High ecological validity, low internal validity.
- **Structured observation** -- observing behavior in a controlled setting with standardized procedures (e.g., Ainsworth's Strange Situation).
- **Participant observation** -- the researcher joins the group being studied.

### Case studies

Intensive investigation of a single individual or small group. Invaluable for rare conditions (H.M., Phineas Gage, Genie) and for generating hypotheses, but cannot establish causation or generalize to populations.

### Surveys

Self-report measures administered to large samples. Efficient for gathering data on attitudes, beliefs, and behaviors. Vulnerable to social desirability bias, acquiescence bias, and poorly worded questions.

## Domain 3 -- Research Ethics

### Historical catalysts

- **Nuremberg Code (1947)** -- established voluntary consent as essential, in response to Nazi medical experiments.
- **Tuskegee Syphilis Study (1932-1972)** -- untreated Black men with syphilis were studied for 40 years without informed consent. Led directly to the Belmont Report and modern IRB requirements.
- **Milgram (1963) and Zimbardo (1971)** -- raised questions about psychological harm from research participation.

### APA Ethical Principles

The American Psychological Association's Ethical Principles (2017) include:

1. **Beneficence and nonmaleficence** -- maximize benefits, minimize harm
2. **Fidelity and responsibility** -- establish trust, accept responsibility
3. **Integrity** -- promote accuracy, honesty, truthfulness
4. **Justice** -- fair and equitable access to and benefit from research
5. **Respect for people's rights and dignity** -- protect autonomy, privacy, confidentiality

### Key ethical requirements

- **Informed consent** -- participants must understand the study's purpose, procedures, risks, and their right to withdraw without penalty. Written consent is standard.
- **Deception** -- permitted only when (a) the study cannot be conducted without it, (b) the scientific value justifies it, and (c) participants are debriefed promptly. Milgram's experiments would require extensive justification today.
- **Debriefing** -- after participation, explain the study's true purpose and any deception. Address any distress caused.
- **Institutional Review Board (IRB)** -- independent committee that reviews research proposals for ethical compliance before data collection begins.
- **Confidentiality** -- participant data must be stored securely and reported in ways that prevent identification.

### Vulnerable populations

Research with children, prisoners, cognitively impaired individuals, and other vulnerable populations requires additional safeguards: parental consent plus child assent, independent advocates, and heightened risk-benefit scrutiny.

## Domain 4 -- Statistics in Psychology

### Null Hypothesis Significance Testing (NHST)

The dominant (and controversial) inferential framework in psychology:

1. State a null hypothesis (H0: no effect/no difference) and an alternative hypothesis (H1: there is an effect).
2. Collect data and compute a test statistic (t, F, chi-square, etc.).
3. Calculate the p-value: the probability of obtaining results as extreme as observed, assuming H0 is true.
4. If p < alpha (conventionally .05), reject H0.

### What the p-value is and is not

| p-value IS | p-value IS NOT |
|---|---|
| P(data or more extreme \| H0 is true) | P(H0 is true \| data) |
| A measure of data surprise under H0 | A measure of effect size or practical importance |
| Affected by sample size | A measure of replication probability |

A p-value of .04 does not mean there is a 96% chance the effect is real. It means that if H0 were true, data this extreme would occur about 4% of the time.

### Effect size

Effect size quantifies the magnitude of a finding independently of sample size:

- **Cohen's d** -- standardized mean difference. Small = 0.2, medium = 0.5, large = 0.8.
- **Pearson's r** -- correlation coefficient. Small = .10, medium = .30, large = .50.
- **Odds ratio** -- ratio of odds of an event in two groups. Used in clinical and epidemiological research.
- **Eta-squared** -- proportion of variance explained. Used in ANOVA.

A statistically significant result with a tiny effect size may be practically meaningless. A non-significant result with a large effect size may reflect inadequate sample size.

### Confidence intervals

A 95% confidence interval means: if we repeated the study many times, 95% of the constructed intervals would contain the true parameter value. A confidence interval that does not include zero is equivalent to p < .05 for a two-tailed test. Confidence intervals communicate both the estimate and its precision.

### Power analysis

Statistical power is the probability of detecting a true effect (1 - beta, where beta is the Type II error rate). Convention: power >= .80. Power depends on effect size, sample size, and alpha level. Underpowered studies are likely to produce false negatives or, when they do reach significance, inflated effect sizes (the "winner's curse"). Cohen (1962, 1992) documented that psychology studies are chronically underpowered.

## Domain 5 -- The Replication Crisis

### The problem

The Open Science Collaboration (2015) attempted to replicate 100 published psychology studies. Only 36% of replications reached statistical significance (vs. 97% of originals). Mean effect sizes in replications were half the size of originals. This result, published in *Science*, catalyzed a reckoning across the field.

### Causes

- **Publication bias** -- journals preferentially publish positive results. Studies that fail to find an effect sit in the "file drawer" (Rosenthal, 1979).
- **p-hacking** -- exploiting researcher degrees of freedom (excluding outliers, adding covariates, testing multiple DVs, stopping data collection when p < .05) to produce significant results from noise. Simmons, Nelson, & Simonsohn (2011) showed that these practices can produce p < .05 for a false hypothesis with high probability.
- **HARKing** (Hypothesizing After Results are Known) -- presenting post-hoc findings as if they were predicted a priori. Kerr (1998).
- **Underpowered studies** -- small samples produce noisy estimates, and only the (inflated) significant ones are published.
- **Incentive structure** -- academic careers reward novel, significant findings. Replications and null results are not rewarded.

### Solutions

- **Preregistration** -- publicly specifying hypotheses, methods, and analysis plans before data collection. Prevents p-hacking and HARKing.
- **Registered Reports** -- journals accept or reject studies based on the introduction and method, before results are known. Eliminates publication bias.
- **Open data and open materials** -- sharing data and stimuli enables verification and reanalysis.
- **Large-scale replications** -- Many Labs projects (Klein et al., 2014) coordinate replications across multiple laboratories.
- **Effect size reporting** -- APA Publication Manual (7th ed., 2020) requires effect size reporting alongside significance tests.
- **Bayesian statistics** -- quantify evidence for H1 vs. H0 via Bayes factors, avoiding the binary significant/non-significant framework entirely.

## Cross-References

- **kahneman agent:** Statistical thinking, cognitive biases in research interpretation, and the psychology of judgment under uncertainty that explains why researchers fall prey to p-hacking and HARKing.
- **james agent:** Pragmatic epistemology -- what counts as evidence, the relationship between theory and data, and the history of psychological methodology.
- **piaget agent:** Developmental methodology (longitudinal vs. cross-sectional designs, challenges of studying children).
- **cognitive-psychology skill:** Experimental paradigms (reaction time, signal detection, priming) used to study cognitive processes.
- **social-psychology skill:** Methodological controversies specific to social psychology (Milgram ethics, demand characteristics, ecological validity).
- **behavioral-neuroscience skill:** Neuroimaging methodology (fMRI, EEG, PET) as a complement to behavioral measurement.

## References

- Cohen, J. (1992). A power primer. *Psychological Bulletin*, 112(1), 155-159.
- Kerr, N. L. (1998). HARKing: Hypothesizing after the results are known. *Personality and Social Psychology Review*, 2(3), 196-217.
- Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
- Rosenthal, R. (1979). The file drawer problem and tolerance for null results. *Psychological Bulletin*, 86(3), 638-641.
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science*, 22(11), 1359-1366.
- American Psychological Association. (2017). *Ethical Principles of Psychologists and Code of Conduct*. APA.
- American Psychological Association. (2020). *Publication Manual* (7th ed.). APA.
