---
name: scientific-method
description: The scientific method as an epistemological framework for producing reliable knowledge. Covers observation, question formation, hypothesis construction, experimental testing, data analysis, conclusion, and communication -- not as a rigid sequence but as an iterative cycle of inquiry. Includes falsifiability criteria, the role of replication, and the distinction between science, non-science, and pseudoscience. Use when teaching, applying, or evaluating the process of scientific inquiry at any level.
type: skill
category: science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/science/scientific-method/SKILL.md
superseded_by: null
---
# The Scientific Method

The scientific method is not a recipe. It is a discipline of thought -- a set of practices that, taken together, produce knowledge more reliable than any individual could produce alone. Its power comes not from any single step but from the cycle: observe, question, hypothesize, test, analyze, conclude, communicate, and then observe again, with each pass refining the previous one.

**Agent affinity:** feynman-s (methodology evaluation), darwin (classification and routing)

**Concept IDs:** sci-observation-skills, sci-scientific-questions, sci-hypothesis-formation, sci-scientific-curiosity

## The Method as a Cycle

The scientific method is often taught as a linear sequence: observe, question, hypothesize, experiment, analyze, conclude. This is misleading. In practice, the method is a cycle -- conclusions from one investigation become observations that generate new questions. The "steps" are not sequential stages but recurring activities that scientists move between fluidly.

```
   Observe
      |
      v
   Question <-------+
      |              |
      v              |
   Hypothesize       |
      |              |
      v              |
   Test              |
      |              |
      v              |
   Analyze           |
      |              |
      v              |
   Conclude ---------+
      |
      v
   Communicate
```

The arrow from "Conclude" back to "Question" is the most important arrow in the diagram. Science is iterative. Every answer is provisional and generates new questions.

## Component 1 -- Observation

Scientific observation is not passive looking. It is deliberate, systematic attention to the natural world with the intent to notice patterns, anomalies, and regularities.

**Qualitative observation** describes properties without numbers: color, texture, behavior, arrangement. "The leaves on the north side of the tree are larger" is a qualitative observation.

**Quantitative observation** measures properties with numbers and units: "The north-facing leaves average 8.3 cm in length (n=30, SD=1.2 cm) compared to 5.7 cm for south-facing leaves (n=30, SD=0.9 cm)."

Both are valuable. Qualitative observation often comes first and guides what to measure quantitatively. The danger is stopping at qualitative observation when quantitative data are needed to discriminate between explanations.

**Key skill:** Recording observations in real time rather than from memory. Human memory edits observations toward expectations. A field notebook or data sheet completed during observation is more reliable than a summary written afterward.

## Component 2 -- Question Formation

A scientific question is one that can be investigated through observation or experimentation. Not all questions are scientific:

| Question | Scientific? | Why / why not |
|---|---|---|
| "Does fertilizer X increase tomato yield?" | Yes | Testable through controlled experiment |
| "What is the speed of sound in water at 20C?" | Yes | Measurable |
| "Is classical music better than jazz?" | No | "Better" is a value judgment, not an empirical claim |
| "Why is there something rather than nothing?" | Not directly | No observation could distinguish "something" from "something that looks like something" |
| "Do heavier objects fall faster than light ones (in a vacuum)?" | Yes | Testable, and famously tested |

**The refinement process:** Initial questions are usually too broad. "What affects plant growth?" becomes "Does the wavelength of light affect the growth rate of Arabidopsis thaliana seedlings?" The refinement is not a loss of ambition -- it is a gain in testability.

## Component 3 -- Hypothesis Construction

A hypothesis is a testable prediction, not a guess. It makes a specific claim about what will happen under specified conditions, and it must be possible for the prediction to be wrong. This is the falsifiability criterion.

**Strong hypothesis form:** "If [independent variable is changed in this way], then [dependent variable will change in this way], because [mechanism or reasoning]."

**Example:** "If Arabidopsis seedlings are grown under blue light (450 nm) instead of red light (650 nm), then their stem elongation rate will decrease by at least 20%, because blue light activates cryptochrome photoreceptors that suppress stem elongation."

The "because" clause is not always required at the introductory level, but it separates a prediction from a guess. A prediction connected to a mechanism is stronger because it explains, not just predicts.

**The null hypothesis:** In statistical testing, the null hypothesis (H0) states that there is no effect or no difference. The alternative hypothesis (H1) states that there is an effect. The experiment tests H0. If the data are inconsistent with H0 beyond a threshold (the significance level, typically alpha = 0.05), H0 is rejected in favor of H1. The logic is: assume the boring explanation is true, then see whether the data make the boring explanation untenable.

## Component 4 -- Experimental Testing

An experiment is a controlled observation designed to test a hypothesis. The key elements:

**Independent variable:** The factor deliberately changed by the experimenter. There should be exactly one per experiment (or the experiment must be designed to detect interactions if multiple are changed, e.g., factorial design).

**Dependent variable:** The factor measured as the outcome. This is what the hypothesis predicts will change.

**Controlled variables:** All other factors held constant so they cannot explain the outcome. The more carefully controlled, the stronger the claim that the independent variable caused the observed change.

**Control group:** A condition where the independent variable is not applied (or is applied at a baseline level). The control group provides the comparison against which the experimental group is measured.

**Positive control:** A condition known to produce the expected effect. Verifies that the experimental system is working. If the positive control fails, the experiment cannot be interpreted.

**Negative control:** A condition known to produce no effect. Verifies that the measurement system is not producing false positives.

**Replication:** Each condition must be tested on multiple independent samples. A single measurement is an anecdote. Replicated measurements reveal variability, which is necessary for statistical inference.

**Randomization:** Assignment of subjects to conditions should be random to prevent systematic bias.

## Component 5 -- Data Analysis

Raw data are not conclusions. Analysis transforms measurements into evidence. The level of analysis depends on the question:

**Descriptive statistics:** Mean, median, standard deviation, range. These summarize what was measured.

**Inferential statistics:** t-tests, ANOVA, chi-square, regression. These assess whether observed differences are likely to be real or likely to be noise.

**Graphical analysis:** Scatter plots, bar charts, line graphs. Visual patterns are often more informative than summary statistics.

**The p-value:** The probability of observing data at least as extreme as the actual data, assuming the null hypothesis is true. A small p-value (conventionally p < 0.05) suggests the data are unlikely under H0. It does NOT mean:
- The probability that H0 is true is 5%
- The effect is large or important
- The experiment is well-designed

P-values report surprise, not truth. A small p-value from a poorly designed experiment is meaningless.

**Effect size:** How large is the observed difference, in meaningful units? A drug that lowers blood pressure by 0.1 mmHg with p < 0.001 is statistically significant but clinically meaningless. Effect size answers "so what?" in a way that p-values cannot.

## Component 6 -- Conclusion

A scientific conclusion states what the evidence supports, no more and no less.

**The conclusion should:**
- State whether the hypothesis was supported or refuted by the data
- Quantify the evidence (effect size, confidence interval)
- Acknowledge limitations (what the experiment could not control, what alternative explanations remain)
- Distinguish correlation from causation when appropriate
- Suggest follow-up experiments to address remaining questions

**The conclusion should NOT:**
- Overstate the evidence ("this proves that...")
- Ignore contradictory data
- Extend beyond the tested conditions ("since fertilizer X works on tomatoes, it will work on all plants")
- Confuse absence of evidence with evidence of absence

**The honesty standard (Feynman):** "The first principle is that you must not fool yourself -- and you are the easiest person to fool." A scientific conclusion is honest about what was found, including null results and anomalies.

## Component 7 -- Communication

Science that is not communicated does not contribute to collective knowledge. Scientific communication follows conventions designed to enable replication and evaluation:

**Lab report / paper structure:** Introduction (why the question matters), Methods (what was done, in enough detail to replicate), Results (what was found, with data), Discussion (what it means, including limitations).

**Peer review:** Before publication, scientific papers are evaluated by independent experts who assess methodology, analysis, and conclusions. Peer review is imperfect but remains the best available filter for scientific quality.

**Reproducibility:** The methods section must be detailed enough that another scientist can repeat the experiment independently. If they cannot, the result is anecdotal, not scientific.

## Falsifiability and Demarcation

Karl Popper (1959, *The Logic of Scientific Discovery*) argued that the defining feature of science is falsifiability: a statement is scientific if and only if it makes predictions that could, in principle, be shown wrong by observation. This criterion separates:

- **Science:** "If I drop this ball, it will accelerate at 9.8 m/s^2 toward Earth." Testable, falsifiable.
- **Non-science (legitimate but outside science):** "Beethoven's 9th Symphony is the greatest musical achievement of Western civilization." A value judgment, not an empirical claim.
- **Pseudoscience:** "This crystal heals ailments through vibrational energy aligned with the body's chakras." Uses scientific-sounding language but makes no falsifiable prediction.

Falsifiability is necessary but not sufficient. A claim can be falsifiable but unfalsified, or falsifiable and falsified (and therefore wrong). The point is that science subjects itself to the possibility of being wrong.

## Common Misconceptions

| Misconception | Reality |
|---|---|
| "The scientific method is a fixed sequence of steps" | It is an iterative cycle. Scientists jump between components as needed. |
| "A theory is just a guess" | A scientific theory is a well-tested explanatory framework (e.g., germ theory, evolutionary theory, plate tectonics). |
| "Science proves things" | Science provides evidence that supports or refutes hypotheses. Proof belongs to mathematics and logic. |
| "If an experiment fails, it's useless" | A well-designed experiment that refutes a hypothesis is as valuable as one that supports it. |
| "Correlation equals causation" | Correlation is a necessary but not sufficient condition for causation. Controlled experiments establish causation. |
| "Scientists are perfectly objective" | Scientists are human and subject to bias. The method (controls, replication, peer review) compensates for individual bias. |

## Cross-References

- **feynman-s agent:** Methodological evaluation. Uses this skill as the reference framework for assessing scientific rigor.
- **mcclintock agent:** Experimental design. Implements the "Test" component with specific design expertise.
- **wu agent:** Measurement. Implements the precision requirements of the "Data Analysis" component.
- **goodall agent:** Field observation. Implements the "Observation" component for systems that cannot be brought into the laboratory.
- **experimental-design-sci skill:** Detailed experimental design beyond what this overview covers.
- **data-analysis-sci skill:** Statistical methods referenced in the Data Analysis component.

## References

- Popper, K. (1959). *The Logic of Scientific Discovery*. Routledge.
- Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.
- Feynman, R. P. (1974). "Cargo Cult Science." Caltech commencement address.
- Sagan, C. (1995). *The Demon-Haunted World: Science as a Candle in the Dark*. Random House.
- National Research Council. (2012). *A Framework for K-12 Science Education*. National Academies Press.
- American Association for the Advancement of Science. (1993). *Benchmarks for Science Literacy*. Oxford University Press.
