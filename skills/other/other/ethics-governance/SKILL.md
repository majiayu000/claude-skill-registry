---
name: ethics-governance
description: Bias detection and mitigation, fairness metrics, privacy frameworks, consent models, transparency requirements, and accountability structures for data science practice. Covers algorithmic bias sources, disparate impact testing, differential privacy, GDPR principles, model cards, datasheets for datasets, responsible AI frameworks, and the organizational governance needed to make ethics actionable. Use when auditing models for bias, designing privacy-preserving systems, establishing governance processes, or evaluating the social impact of data-driven decisions.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/ethics-governance/SKILL.md
superseded_by: null
---
# Ethics and Governance in Data Science

Data science operates on people's data, affects people's lives, and encodes human decisions into automated systems. Ethics in data science is not an afterthought or a compliance checkbox -- it is a design requirement. Ruha Benjamin's concept of the "New Jim Code" names the reality that automated systems can reproduce and amplify existing social inequalities while appearing objective. This skill covers the principles, frameworks, and practices that make ethical data science concrete and actionable.

**Agent affinity:** benjamin (bias audit, fairness analysis, ethical review), nightingale (routing ethics queries), cairo (communicating ethical findings)

**Concept IDs:** data-privacy-consent, data-algorithmic-bias, data-data-ownership, data-responsible-practice

## Sources of Bias

### Where Bias Enters the Pipeline

Bias can enter at every stage of the data science workflow. It is not a property of algorithms alone -- it is a property of the system: data, design decisions, deployment context, and feedback loops.

| Stage | Bias type | Example |
|---|---|---|
| **Problem formulation** | Framing bias | Defining "success" as engagement maximizes addictive behavior |
| **Data collection** | Selection bias | Training a facial recognition system on predominantly light-skinned faces |
| **Data labeling** | Annotation bias | Labelers' cultural assumptions influence what counts as "toxic" speech |
| **Feature engineering** | Proxy bias | ZIP code encodes race due to residential segregation |
| **Model training** | Optimization bias | Minimizing overall error ignores disparate performance across subgroups |
| **Evaluation** | Metric bias | Reporting aggregate accuracy hides poor performance on minority groups |
| **Deployment** | Automation bias | Decision-makers defer to model output without scrutiny |
| **Feedback loops** | Amplification bias | Predictive policing increases patrols in targeted areas, generating more arrests, confirming the model |

### Historical Bias vs. Representation Bias

- **Historical bias:** The world is unequal, and data reflects that inequality. A hiring model trained on historical decisions inherits past discrimination. Even a "perfect" model of biased reality produces biased outputs.
- **Representation bias:** The training data does not represent the deployment population. A speech recognition system trained on American English performs poorly on other dialects. This is not a bug in the algorithm -- it is a gap in the data.

Both are real. Neither is solved by "better algorithms" alone. The fix requires changes to data collection, problem formulation, and deployment monitoring.

## Fairness Metrics

### Impossibility Theorem

Chouldechova (2017) and Kleinberg, Mullainathan, and Raghavan (2016) independently proved that three natural fairness criteria cannot all be satisfied simultaneously when base rates differ between groups:

1. **Calibration:** Among those predicted positive, the fraction truly positive is the same across groups.
2. **Equal false positive rate:** The rate of incorrectly predicting positive is the same across groups.
3. **Equal false negative rate:** The rate of incorrectly predicting negative is the same across groups.

When the base rate (actual positive rate) differs between groups, satisfying any two of these requires violating the third. This is not a technical limitation to be solved -- it is a value judgment about which type of error matters more. The choice must be made explicitly, not hidden inside a loss function.

### Common Fairness Definitions

| Metric | Definition | When appropriate |
|---|---|---|
| **Demographic parity** | P(positive prediction) is equal across groups | When the prediction itself causes differential treatment |
| **Equalized odds** | TPR and FPR are equal across groups | When false positives and false negatives have different costs |
| **Equal opportunity** | TPR is equal across groups (weaker than equalized odds) | When false negatives are the primary concern (e.g., loan approval for qualified applicants) |
| **Predictive parity** | Precision is equal across groups | When the model's positive predictions trigger consequential actions |
| **Individual fairness** | Similar individuals receive similar predictions | When you can define a meaningful similarity metric |
| **Counterfactual fairness** | Prediction would be the same in a counterfactual world where the individual belonged to a different group | When causal reasoning is possible and the causal model is trusted |

### Measuring Disparate Impact

The four-fifths rule (EEOC, 1978): if the selection rate for a protected group is less than 80% of the rate for the most-selected group, there is evidence of adverse impact.

Disparate impact ratio = (selection rate for protected group) / (selection rate for most-selected group)

If this ratio < 0.8, investigate. This is a screening heuristic, not a legal standard -- but it is widely used as a first check.

## Privacy

### Privacy Principles (GDPR Framework)

| Principle | Meaning | Practical implication |
|---|---|---|
| **Lawfulness** | Legal basis for processing | Document the legal basis (consent, legitimate interest, contract, etc.) |
| **Purpose limitation** | Collect for specified purposes only | Do not repurpose data without new consent or legal basis |
| **Data minimization** | Collect only what is necessary | Every field in the dataset should have a documented purpose |
| **Accuracy** | Keep data correct and current | Provide mechanisms for correction; audit data quality |
| **Storage limitation** | Do not keep data longer than needed | Define retention periods; delete when expired |
| **Integrity and confidentiality** | Protect against unauthorized access | Encryption, access controls, audit logs |
| **Accountability** | Demonstrate compliance | Documentation, impact assessments, designated roles |

### Anonymization Techniques

| Technique | How it works | Limitation |
|---|---|---|
| **Suppression** | Remove identifying fields | Remaining fields may be quasi-identifiers |
| **Generalization** | Replace specific values with ranges (age 34 -> 30-39) | Reduces data utility |
| **k-Anonymity** | Every record is indistinguishable from at least k-1 others on quasi-identifiers | Vulnerable to homogeneity and background knowledge attacks |
| **l-Diversity** | Each equivalence class has at least l distinct sensitive values | Better than k-anonymity but still vulnerable |
| **t-Closeness** | Distribution of sensitive attribute in each class is close to overall distribution | Strong but complex to implement |
| **Differential privacy** | Add calibrated noise so no individual's inclusion changes the output significantly | Mathematical guarantee; degrades with composition |

### Differential Privacy

Differential privacy (Dwork, 2006) provides a mathematical guarantee: the output of an analysis is approximately the same whether any individual is in the dataset or not.

The privacy budget epsilon controls the tradeoff: smaller epsilon = stronger privacy = more noise = less accuracy. Epsilon is spent with each query, and it does not regenerate -- this is the composition theorem.

**Practical deployment:** Apple (emoji usage), Google (Chrome usage), US Census (2020). Each chose an epsilon value that balanced utility and privacy for their specific context. There is no universally "correct" epsilon.

## Consent

### Informed Consent Requirements

1. **Purpose:** What the data will be used for, in plain language.
2. **Scope:** What data is collected and how long it is retained.
3. **Rights:** How to access, correct, or delete data.
4. **Risks:** Potential consequences of participation.
5. **Voluntariness:** Participation is optional; no penalty for declining.
6. **Third parties:** Whether data is shared and with whom.

### Consent Models

| Model | Description | Strength | Weakness |
|---|---|---|---|
| **Opt-in** | User actively agrees before data is collected | Respects autonomy | Lower participation rates |
| **Opt-out** | Data is collected by default; user can withdraw | Higher participation | Default bias; many users never opt out |
| **Dynamic consent** | Ongoing, granular control over data uses | Maximum user control | Complex to implement; user fatigue |
| **Broad consent** | Consent for a category of future uses | Enables secondary research | Vague; user may not understand implications |
| **Tiered consent** | Multiple options (e.g., anonymized only, full research use) | User chooses comfort level | More complex consent forms |

### When Consent Is Insufficient

Consent does not make harmful uses ethical. If a system causes disparate impact, user consent to data collection does not excuse the harm. Similarly, consent from one population does not extend to another. Consent is necessary but not sufficient.

## Transparency and Accountability

### Model Cards

Mitchell et al. (2019) proposed model cards as standardized documentation for deployed models:

| Section | Contents |
|---|---|
| **Model details** | Architecture, training data, version, owner |
| **Intended use** | Primary use cases, out-of-scope uses |
| **Factors** | Demographic groups, environmental conditions, instrumentation |
| **Metrics** | Performance metrics overall and disaggregated by group |
| **Training data** | Source, size, preprocessing, known limitations |
| **Evaluation data** | Source, demographics, relationship to deployment population |
| **Ethical considerations** | Known biases, risks, mitigation strategies |
| **Caveats and recommendations** | Known limitations, suggested monitoring |

### Datasheets for Datasets

Gebru et al. (2021) proposed datasheets as standardized documentation for datasets, covering: motivation, composition, collection process, preprocessing, uses, distribution, and maintenance.

**Why this matters:** A model is only as good as its data. Without dataset documentation, users cannot assess whether the data is appropriate for their task.

### Algorithmic Impact Assessment

Before deploying a model that affects people's lives:

1. **Identify affected populations.** Who does this system affect? Who is most vulnerable?
2. **Assess potential harms.** What happens when the model is wrong? Are errors distributed equitably?
3. **Evaluate alternatives.** Is automation necessary? Would a simpler rule or human judgment be more appropriate?
4. **Plan monitoring.** How will you detect degradation, drift, or emerging bias after deployment?
5. **Establish recourse.** How can affected individuals challenge or appeal automated decisions?

## Organizational Governance

### Building an Ethics Practice

Ethics is not a one-time review. It requires ongoing organizational commitment:

- **Ethics review board:** Multidisciplinary group (data scientists, ethicists, domain experts, community representatives) that reviews high-risk projects before deployment.
- **Bias bounty programs:** Internal or external programs that reward finding bias in deployed systems.
- **Incident response:** Process for handling ethical incidents (biased output discovered in production, privacy breach, consent violation).
- **Training:** Regular ethics training for all team members, not just compliance officers.
- **Diverse teams:** Teams with diverse backgrounds are more likely to identify blind spots in data, design, and deployment.

### Responsible AI Frameworks

| Framework | Source | Key contribution |
|---|---|---|
| **Fairness, Accountability, Transparency (FAccT)** | ACM Conference | Academic research community and standards |
| **Responsible AI Practices** | Google | Practical guidelines for industry |
| **Ethics Guidelines for Trustworthy AI** | EU High-Level Expert Group | Seven requirements including human agency, robustness, privacy |
| **Algorithmic Accountability Act** | US proposed legislation | Requires impact assessments for automated critical decisions |
| **Race After Technology** | Ruha Benjamin | Critical examination of how technology reproduces racial inequality |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| "The algorithm is objective" | Algorithms encode human decisions in data, features, and metrics | Audit for bias; algorithms inherit their creators' and data's biases |
| Ethics as compliance checkbox | Checking a box does not prevent harm | Build ethics into the design process, not just the review process |
| Aggregate metrics only | 95% accuracy overall can mask 70% accuracy for a subgroup | Always disaggregate metrics by protected groups |
| Anonymization = privacy | Re-identification is possible from "anonymized" data | Use differential privacy or formal anonymization guarantees |
| "We didn't intend bias" | Intent does not determine impact | Measure impact, not intent |
| Consent theater | Long, unreadable consent forms do not constitute informed consent | Plain language, layered disclosure, genuine choice |

## Cross-References

- **benjamin agent:** Primary agent for bias audit, fairness analysis, and ethical review of data science work products.
- **nightingale agent:** Department chair who routes ethics-related queries and ensures ethical review is integrated into the workflow.
- **cairo agent:** Communicating ethical findings to non-technical stakeholders through visualization and narrative.
- **fisher agent:** Experimental design ethics -- informed consent for A/B tests, stopping rules for harmful treatments.
- **data-visualization skill:** Honest visualization practices that avoid misleading representations.
- **experimental-design-ds skill:** Ethical experimental design, including human subjects considerations.
- **data-wrangling skill:** Data quality and provenance documentation that supports ethical practice.

## References

- Benjamin, R. (2019). *Race After Technology*. Polity Press.
- O'Neil, C. (2016). *Weapons of Math Destruction*. Crown.
- Barocas, S., Hardt, M., & Narayanan, A. (2019). *Fairness and Machine Learning*. fairmlbook.org.
- Dwork, C. (2006). "Differential Privacy." *ICALP*, 1-12.
- Mitchell, M. et al. (2019). "Model Cards for Model Reporting." *Proceedings of FAccT*, 220-229.
- Gebru, T. et al. (2021). "Datasheets for Datasets." *Communications of the ACM*, 64(12), 86-92.
- Chouldechova, A. (2017). "Fair Prediction with Disparate Impact." *Big Data*, 5(2), 153-163.
- Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016). "Inherent Trade-Offs in the Fair Determination of Risk Scores." *Proceedings of ITCS*.
