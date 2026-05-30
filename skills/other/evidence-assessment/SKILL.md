---
name: evidence-assessment
description: Evaluating the quality, provenance, and relevance of evidence that supports or undermines a claim. Covers source credibility, sampling quality, study design, levels of evidence (anecdote to meta-analysis), base rate integration, distinguishing primary from secondary sources, and calibrating belief to evidence strength. Use when the question is not whether an argument is valid but whether its premises are actually supported by the available data.
type: skill
category: critical-thinking
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/critical-thinking/evidence-assessment/SKILL.md
superseded_by: null
---
# Evidence Assessment

Valid reasoning from false premises proves nothing. Evidence assessment is the discipline of testing whether the premises of an argument are actually supported by the data, what kind of data would be decisive, and how much confidence the available evidence warrants. This skill covers the evaluation of sources, study designs, sampling, levels of evidence, and the integration of new evidence with prior knowledge.

**Agent affinity:** elder (structural reconstruction of evidence claims), tversky (base rates, inductive strength), kahneman-ct (evidence evaluation under System 1/2)

**Concept IDs:** crit-evidence-quality, crit-sourcing, crit-burden-of-proof, crit-scientific-literacy

## The Assessment Toolbox at a Glance

| # | Operation | Question answered |
|---|---|---|
| 1 | Source identification | Where did this claim come from? |
| 2 | Primary vs. secondary | Is this the original source or a report of it? |
| 3 | Source credibility | Does the source have relevant expertise and a track record? |
| 4 | Funding and conflicts | Who paid for this? What do they stand to gain? |
| 5 | Sample quality | How were the data collected and from whom? |
| 6 | Study design | Observational? Experimental? Randomized? |
| 7 | Levels of evidence | Where does this study sit in the evidence hierarchy? |
| 8 | Reproducibility | Has this result been replicated? |
| 9 | Scope check | What does the evidence actually show vs. what is being claimed? |
| 10 | Base rate integration | How does this update against prior probability? |

## The Levels of Evidence Hierarchy

Not all evidence is created equal. Roughly from weakest to strongest:

| Level | Type | Strength | Examples |
|---|---|---|---|
| 1 | Anecdote / testimonial | Very weak | "My cousin took X and felt better" |
| 2 | Expert opinion | Weak (unless grounded) | An authority says it's true |
| 3 | Case report | Weak | Single clinical observation |
| 4 | Case series | Weak | A handful of similar cases reported together |
| 5 | Cross-sectional / correlational study | Moderate | Survey data showing X and Y co-occur |
| 6 | Case-control study | Moderate | Retrospective comparison of cases to controls |
| 7 | Cohort study (prospective) | Moderate-strong | Follow a population forward over time |
| 8 | Randomized controlled trial (single) | Strong | Random assignment, controlled conditions |
| 9 | Meta-analysis / systematic review | Strongest | Pooled data from multiple RCTs with appropriate weighting |

**Key discipline.** The level of evidence should match the confidence of the claim. A single anecdote may be worth noting but cannot support "X causes Y." A meta-analysis can support stronger claims.

## Operation 1 — Source Identification

**Pattern:** Trace the claim to its origin. Who first said it? Where was it published? When?

**Worked example.** A tweet says, "Studies show that 8 glasses of water a day improves cognitive performance by 23%." The 23% is suspiciously precise. Trace it: the tweet cites a blog post, which cites a news article, which mentions "a study" without linking. Go find the actual study. Often, it does not exist, or the actual finding is much weaker ("effects on a specific subtest of working memory in a 15-person study").

**Discipline.** Refuse to cite or propagate a claim whose original source you have not seen.

## Operation 2 — Primary vs. Secondary Sources

**Primary source.** The original document — the research paper, the dataset, the eyewitness account, the legal ruling, the historical artifact.

**Secondary source.** A report, summary, interpretation, or citation of the primary source. Textbooks, news articles, review papers, and blog posts are usually secondary.

**Why it matters.** Secondary sources introduce errors. A claim filtered through three secondary sources typically loses nuance, acquires hedges or loses them, and drifts from the original. For high-stakes claims, go to the primary.

## Operation 3 — Source Credibility

Assess credibility along multiple dimensions:

- **Expertise.** Does the source have relevant training and experience in this specific area?
- **Track record.** Has the source been accurate in the past? Accountable for errors?
- **Institutional standing.** Is the source affiliated with institutions that impose quality controls (peer review, editorial standards, professional accountability)?
- **Incentives.** Does the source benefit from the claim being true?
- **Willingness to be wrong.** Does the source publicly update when evidence changes?

**Common mistake.** Treating credentials as a substitute for evaluation. An expert in one field is not automatically credible in another. A Nobel laureate in physics speaking about nutrition should be evaluated on the same terms as anyone else speaking about nutrition.

## Operation 4 — Funding and Conflicts of Interest

A source's funding or affiliations do not automatically invalidate their claims, but they do raise the bar for independent verification. Studies funded by industries with a stake in the outcome show systematically different results on average.

**Worked example.** A study funded by a food industry group finds no evidence linking its product to a health outcome. This does not prove the study wrong, but it raises the question of whether an independently funded replication would find the same result.

**Discipline.** Always note funding sources. Treat results from conflicted sources as weaker evidence than equivalent results from independent sources. Ask for replication in independent labs before accepting policy-relevant claims.

## Operation 5 — Sample Quality

For claims based on samples (surveys, studies, polls):

| Question | What to check |
|---|---|
| Sample size | Larger is better, with diminishing returns; 1,500 for population surveys is typical |
| Randomness | Was the sample drawn randomly from the target population? |
| Representativeness | Does the sample match the population in age, gender, region, etc.? |
| Self-selection | Did respondents choose to participate? (Major bias source) |
| Response rate | What fraction of those contacted actually responded? |
| Attrition | How many dropped out by the end of a longitudinal study? |

**Worked example.** "In our online poll, 82% of respondents support policy X." Online polls are not random samples. Respondents self-select. This result is close to uninformative about the general population and should never be cited as "public opinion."

## Operation 6 — Study Design

Not all studies answer the same kind of question with the same strength.

- **Observational.** Record what happens without intervening. Can establish correlation but confounds are hard to rule out.
- **Quasi-experimental.** Comparison groups are used but assignment is not random. Better than pure observation, still subject to selection effects.
- **Randomized controlled trial (RCT).** Participants are randomly assigned to treatment or control. Randomization neutralizes confounds on average. The gold standard for causal claims.
- **Natural experiment.** An external event creates something like random assignment (e.g., a policy change in one state but not another). Useful when RCTs are impossible.

**Key insight.** The phrase "studies show" does most of its rhetorical work by hiding the study design. A news story claiming "studies show X" may be reporting a single observational study with severe confounds. Always ask: what was the study design?

## Operation 7 — Scope Check

Compare what the evidence shows to what is being claimed. The most common overreach patterns:

- **From correlation to causation.** A correlation between X and Y does not establish that X causes Y.
- **From animal models to humans.** A rat study does not establish a human effect.
- **From small trial to general recommendation.** A 40-person pilot study does not support population-level advice.
- **From surrogate outcome to patient outcome.** Drug X lowers a biomarker; does it actually prevent the disease?
- **From laboratory to real world.** Tightly controlled conditions may not generalize to clinical or everyday settings.

**Worked example.** A study finds that a chemical kills cancer cells in a petri dish. The headline reads "New cancer cure discovered." Nothing in the study shows the chemical works in a living human being, at a safe dose, delivered through a feasible route. The scope of the claim has overreached the evidence by several levels.

## Operation 8 — Reproducibility and Replication

A single study is weak evidence. A finding that has been independently replicated in different labs, with different samples, using different methods, is much stronger.

- **Has this finding been replicated?** If not, treat it as provisional.
- **How many times and where?** One failed replication may be methodological; several is a warning.
- **Is there a meta-analysis?** Pooled results across multiple studies are more reliable than any single study.
- **Is the finding the expected effect size?** If different replications show different magnitudes, the original estimate may be inflated (publication bias, p-hacking).

## Operation 9 — Base Rate Integration

Any new evidence must be integrated with prior probability. The same piece of evidence can mean very different things depending on the base rate.

**Worked example (medical testing).** A test for a rare disease has 99% sensitivity and 95% specificity. A patient tests positive. What's the probability they have the disease?

If the disease affects 1 in 1,000 people:
- 1 true positive (99% of 1)
- ~50 false positives (5% of 999)
- Post-test probability ~2%

If the disease affects 1 in 10 people:
- ~99 true positives (99% of 100)
- ~45 false positives (5% of 900)
- Post-test probability ~69%

Same test, wildly different interpretations. Base rate matters.

## Operation 10 — Burden of Proof

The burden of proof lies with whoever is making a claim, not with whoever is questioning it. Extraordinary claims require extraordinary evidence (the Sagan standard).

- **Weak claims need weak evidence.** "It rained yesterday" needs only a memory or a weather report.
- **Ordinary claims need ordinary evidence.** "Coffee contains caffeine" needs a chemistry reference.
- **Extraordinary claims need extraordinary evidence.** "This herb cures cancer" needs multiple independent RCTs.

**Common mistake.** Shifting the burden. "Prove that it doesn't work" is not a valid response to "it has not been shown to work." The burden remains on the proponent.

## Standard Assessment Procedure

When evaluating a claim in the wild:

1. **Find the source.** Trace the claim to its origin.
2. **Determine type.** Primary or secondary? Peer-reviewed or not?
3. **Check credibility.** Expertise, track record, conflicts of interest.
4. **Examine the method.** Sample quality, study design, scope.
5. **Check level of evidence.** Where does this sit in the hierarchy?
6. **Check for replication.** Has anyone else found the same thing?
7. **Check scope.** Does the conclusion overreach the evidence?
8. **Integrate base rates.** How does this update against prior probability?
9. **Calibrate confidence.** Match belief strength to evidence strength.
10. **State what you accept and why.**

## When to Use

- Reading a news story with a scientific claim
- Evaluating a policy position that cites evidence
- Reviewing a research paper in your own or an adjacent field
- Deciding how much weight to give a surprising result
- Teaching students to distinguish strong from weak empirical claims

## When NOT to Use

- Pure logical questions where evidence is not at stake — use `logical-reasoning`
- Normative or ethical questions where "evidence" is not the right standard
- Personal preferences and aesthetic judgments

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| "Studies show" without citation | No verifiable source | Refuse to rely on claims you cannot trace |
| Treating a single study as final | Single studies often do not replicate | Wait for or look for replications |
| Ignoring conflicts of interest | Funding biases results on average | Note the conflict; weight the evidence accordingly |
| Overreaching scope | Premise supports less than the conclusion claims | Restrict the claim to what the evidence actually shows |
| Neglecting base rates | Evidence value depends on prior probability | Always ask: how common is this really? |
| Cherry-picking studies | One favorable study does not reflect the literature | Seek systematic reviews or meta-analyses |

## Cross-References

- **tversky agent:** Base rate neglect and its corrections.
- **elder agent:** Structural elements of reasoning — "information" is one element that this skill evaluates.
- **kahneman-ct agent:** Slow, System 2 evaluation of evidence vs. fast System 1 credulity.
- **argument-evaluation skill:** Evidence assessment tests whether an argument's premises are true.
- **cognitive-biases skill:** Biases that distort evidence evaluation.
- **logical-reasoning skill:** How evidence-based premises feed into valid inferences.

## References

- Goldacre, B. (2008). *Bad Science*. Fourth Estate.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine*, 2(8), e124.
- Sackett, D. L., Rosenberg, W. M., Gray, J. A., Haynes, R. B., & Richardson, W. S. (1996). "Evidence Based Medicine: What It Is and What It Isn't." *BMJ*, 312, 71-72.
- Open Science Collaboration (2015). "Estimating the reproducibility of psychological science." *Science*, 349(6251).
- Sagan, C. (1996). *The Demon-Haunted World*. Ballantine Books.
- Higgins, J. P. T. et al. (eds.) (2022). *Cochrane Handbook for Systematic Reviews of Interventions*.
