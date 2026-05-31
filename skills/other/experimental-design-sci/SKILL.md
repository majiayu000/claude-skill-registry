---
name: experimental-design-sci
description: Experimental design principles for scientific inquiry. Covers variable identification and control, control groups (positive and negative), randomization, blinding, sample size and power, replication strategies, factorial designs, quasi-experimental approaches, and common design pitfalls. Use when designing, reviewing, or teaching about controlled experiments in any scientific discipline.
type: skill
category: science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/science/experimental-design-sci/SKILL.md
superseded_by: null
---
# Experimental Design

Experimental design is the art and science of creating tests that can actually answer the question being asked. A well-designed experiment isolates the variable of interest, controls for confounds, produces data with enough precision and statistical power to discriminate between competing explanations, and does so within ethical and practical constraints. A poorly designed experiment wastes time, money, and trust.

**Agent affinity:** mcclintock (experiment design), wu (measurement precision)

**Concept IDs:** sci-controlled-experiments, sci-experimental-controls, sci-variables-types, sci-replication-reliability

## The Design Toolbox at a Glance

| # | Design Element | Purpose | Key question |
|---|---|---|---|
| 1 | Variable identification | Clarify what changes and what is measured | What is the IV? What is the DV? What is held constant? |
| 2 | Control groups | Provide a baseline for comparison | What does "no treatment" look like? |
| 3 | Randomization | Eliminate systematic assignment bias | Are subjects assigned to conditions by chance? |
| 4 | Blinding | Eliminate observer and subject bias | Do participants/observers know which condition they are in? |
| 5 | Sample size & power | Ensure the experiment can detect real effects | How many subjects are needed to detect an effect of size X? |
| 6 | Replication | Establish reliability | Can the result be reproduced? |
| 7 | Factorial design | Test multiple variables and their interactions | Do variables interact, or do they act independently? |
| 8 | Quasi-experimental design | Handle situations where true randomization is impossible | How do we make causal claims without random assignment? |

## Element 1 -- Variable Identification

Every experiment has three categories of variables:

**Independent variable (IV):** The factor deliberately manipulated by the experimenter. In a drug trial, this is the drug vs. placebo. In a plant growth study, this might be the wavelength of light.

**Dependent variable (DV):** The factor measured as the outcome. In the drug trial, this might be blood pressure. In the plant study, this might be stem height after 14 days.

**Controlled variables (CVs):** All other factors held constant across conditions. In the plant study: soil type, pot size, watering schedule, temperature, photoperiod, seed source.

**The single-variable rule:** Change one thing at a time. If two variables change simultaneously and the outcome changes, you cannot determine which variable caused the change. This is the most fundamental design principle and the most commonly violated.

**Exception:** Factorial designs deliberately change multiple variables, but they are designed to detect both individual effects and interaction effects. The single-variable rule applies to simple experiments; factorial designs are a structured relaxation of it.

## Element 2 -- Control Groups

A control group receives no treatment (or a baseline treatment) so that the experimental group's outcome can be compared against something.

**Negative control:** A condition expected to produce no effect. If the negative control shows an effect, something is wrong with the experimental setup (contamination, measurement error, uncontrolled variable).

**Positive control:** A condition expected to produce a known effect. If the positive control fails to show the expected effect, the experimental system is not working (wrong concentration, dead cells, broken instrument).

**Placebo control:** In studies involving human subjects, participants in the control group receive an inert treatment (sugar pill, sham procedure) identical in appearance to the real treatment. This controls for the placebo effect -- the tendency for subjects to improve simply because they believe they are being treated.

**Why controls matter:** Without a control group, an observed outcome is uninterpretable. "The plants grew 15 cm" means nothing. "The plants grew 15 cm compared to 8 cm in the control group under identical conditions except for the experimental variable" means something.

## Element 3 -- Randomization

Random assignment of subjects to conditions prevents systematic differences between groups that could confound the results.

**Simple randomization:** Flip a coin or use a random number generator. Works well for large samples.

**Stratified randomization:** First divide subjects into subgroups (strata) by a known confound (e.g., sex, age bracket, prior condition), then randomize within each stratum. Ensures balanced representation.

**Block randomization:** Create blocks of a fixed size (e.g., 4), with each block containing an equal number of treatment and control assignments in random order. Prevents long runs of the same assignment.

**Why randomization matters:** Without it, subject assignment may correlate with unmeasured variables. If the experimenter (consciously or unconsciously) assigns healthier-looking plants to the treatment group, the treatment will appear to work even if it does nothing.

## Element 4 -- Blinding

**Single-blind:** The subject does not know which condition they are in, but the experimenter does. Prevents subject bias (placebo effect, performance anxiety).

**Double-blind:** Neither the subject nor the experimenter measuring outcomes knows which condition the subject is in. Prevents both subject and observer bias.

**Triple-blind:** Subjects, experimenters, and data analysts are all blinded. The data analyst does not know which group is treatment and which is control until after the analysis is complete.

**When blinding is impossible:** Some interventions cannot be blinded (surgery vs. no surgery, exercise vs. no exercise). In these cases, blinding the outcome assessor (the person measuring the DV) is still valuable.

## Element 5 -- Sample Size and Statistical Power

**Power** is the probability that the experiment will detect a real effect if one exists. Conventionally, power = 0.80 (80% chance of detecting a real effect).

**Sample size** determines power. Too few subjects = low power = the experiment may miss a real effect (Type II error, false negative). Too many subjects = wasted resources (though never a statistical error).

**Power analysis** calculates the required sample size given:
- Expected effect size (how large is the difference you want to detect?)
- Significance level (alpha, typically 0.05)
- Desired power (typically 0.80)
- Variability in the measurement (standard deviation)

**Rule of thumb:** If you do not do a power analysis, you are guessing at sample size. If you are guessing, you are probably guessing low.

## Element 6 -- Replication

**Within-study replication:** Multiple independent measurements under each condition. This is required, not optional. A single measurement per condition is an anecdote.

**Between-study replication:** Independent researchers repeating the same experiment. This is the gold standard for establishing that a result is real and not an artifact of one laboratory's particular conditions, equipment, or biases.

**The replication crisis:** Many published scientific findings have failed to replicate (estimates range from 30% to 70% in some fields). Contributing factors: small sample sizes, p-hacking, publication bias toward positive results, insufficient methodological detail. The response: pre-registration (declaring hypotheses and analysis plans before running the experiment), open data, and increased emphasis on replication studies.

## Element 7 -- Factorial Design

When two or more independent variables are of interest, a factorial design tests all combinations:

**2x2 factorial example:** Testing the effect of fertilizer type (A vs. B) and watering frequency (daily vs. weekly) on plant growth.

| | Daily watering | Weekly watering |
|---|---|---|
| **Fertilizer A** | Condition 1 | Condition 2 |
| **Fertilizer B** | Condition 3 | Condition 4 |

This design answers three questions simultaneously:
1. Does fertilizer type matter? (main effect of fertilizer)
2. Does watering frequency matter? (main effect of watering)
3. Does the effect of fertilizer depend on watering frequency? (interaction effect)

Factorial designs are more efficient than running separate experiments for each variable, and they reveal interactions that single-variable experiments cannot detect.

## Element 8 -- Quasi-Experimental Design

When true randomization is impossible (you cannot randomly assign people to smoking vs. non-smoking, or cities to pollution levels), quasi-experimental designs provide partial control:

**Natural experiments:** An event creates treatment and control groups without experimenter intervention (e.g., a factory closes, allowing comparison of air quality before and after).

**Interrupted time series:** Repeated measurements before and after an intervention, with the pre-intervention trend serving as the control.

**Matched controls:** Each treatment subject is paired with a control subject matched on relevant confounds (age, sex, baseline condition).

**Regression discontinuity:** Subjects are assigned to treatment based on a cutoff score (e.g., students above/below a test threshold receive different interventions). Comparing subjects just above and just below the cutoff approximates random assignment near the boundary.

**Limitation:** Quasi-experimental designs can establish association and temporal precedence, but causal claims are weaker than those from true experiments because unmeasured confounds may explain the results.

## Common Design Pitfalls

| Pitfall | Why it fails | Fix |
|---|---|---|
| No control group | Cannot attribute outcome to treatment | Always include a control |
| Confounded variables | Two variables change together | Isolate variables or use factorial design |
| Non-random assignment | Groups differ systematically | Randomize or use matched controls |
| Inadequate sample size | Low power, unreliable estimates | Conduct power analysis before starting |
| Pseudoreplication | Treating non-independent measurements as independent | Identify the true unit of replication |
| P-hacking | Testing multiple hypotheses until one is "significant" | Pre-register hypotheses and analysis plans |
| Survivorship bias | Analyzing only subjects who completed the study | Use intention-to-treat analysis |
| Hawthorne effect | Subjects change behavior because they know they are observed | Use blinding and unobtrusive measures |

## Cross-References

- **mcclintock agent:** Primary agent for experimental design tasks. Draws on this skill for design principles.
- **wu agent:** Precision measurement. Wu refines the measurement protocols that this skill's designs require.
- **feynman-s agent:** Methodological evaluation. Uses this skill's criteria when assessing experimental rigor.
- **scientific-method skill:** The overarching framework within which experimental design operates.
- **data-analysis-sci skill:** Statistical methods used to analyze the data that experiments produce.

## References

- Fisher, R. A. (1935). *The Design of Experiments*. Oliver and Boyd.
- Campbell, D. T., & Stanley, J. C. (1963). *Experimental and Quasi-Experimental Designs for Research*. Houghton Mifflin.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*. 2nd edition. Lawrence Erlbaum.
- Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin.
- Open Science Collaboration. (2015). "Estimating the reproducibility of psychological science." *Science*, 349(6251), aac4716.
