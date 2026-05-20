---
name: rca-causal-inference
description: Mathematical foundations of root cause analysis using Judea Pearl's Structural Causal Models (SCMs), do-calculus, counterfactual reasoning, Bayesian networks for fault diagnosis, graph-theoretic centrality for fault localization, information-theoretic methods (transfer entropy, mutual information), and Granger causality. Use when the incident involves quantifiable observational data, when you need to distinguish correlation from causation, when you want to compute "what would have happened if we had done X instead," or when building automated fault-detection systems that reason about cause rather than pattern-match on symptoms.
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/rca-causal-inference/SKILL.md
superseded_by: null
---
# Causal-Inference RCA

Most root cause analysis is qualitative — you interview people, draw diagrams, write narratives. That's necessary but insufficient for systems where you have rich observational data and need defensible, reproducible, quantitative causal claims.

This skill teaches the mathematical techniques developed by Pearl, Spirtes, Glymour, and others to reason formally about cause from data: when you can identify a causal effect from observations alone, when you need an intervention, and how to compute what would have happened under a counterfactual.

## The Ladder of Causation

Judea Pearl (*The Book of Why*, 2018) defines three levels of causal reasoning, each requiring strictly more machinery than the last:

| Rung | Activity | Example question | Required |
|---|---|---|---|
| 1 | **Association** | "How often does latency correlate with CPU?" | Joint distribution P(X, Y) |
| 2 | **Intervention** | "What happens to latency if we force CPU=50%?" | do-calculus, do(X) operator |
| 3 | **Counterfactual** | "Given what happened, would latency have stayed normal if CPU had been 50%?" | Structural causal model + observed data |

Most RCA lives implicitly at rung 3 — every "the root cause was X" statement is a counterfactual — but most RCA *tools* can only support rung 1. The gap is where spurious root causes come from.

## Structural Causal Models (SCMs)

An SCM is a triple (U, V, F) where:

- **U** — exogenous variables (unobserved background conditions, modeled as independent random variables)
- **V** — endogenous variables (observed system variables)
- **F** — a set of structural equations, one per endogenous variable, expressing how each variable is generated from its parents and from exogenous noise

Example for a simple latency incident:

```
U = {u_traffic, u_cpu_noise, u_lat_noise}
V = {Traffic, CPU, Latency}
F: Traffic := u_traffic
   CPU     := 0.7 * Traffic + u_cpu_noise
   Latency := 0.3 * CPU + 0.1 * Traffic + u_lat_noise
```

This SCM encodes three claims: Traffic is exogenous, CPU is caused by Traffic plus noise, and Latency is caused by both CPU (primary) and Traffic (direct effect, e.g., queueing). A directed acyclic graph (DAG) corresponds one-to-one:

```
Traffic → CPU → Latency
       ↓________↑
```

### Why the DAG matters

The DAG encodes *which variables can be confounders*. Pearl's do-calculus operates on DAGs to answer: "Given the DAG structure and observational data, can I compute the effect of do(X=x) on Y without running an experiment?" The answer depends on whether a **valid adjustment set** exists — a set of variables that, when conditioned on, blocks all backdoor paths from X to Y.

### Backdoor criterion

A set Z satisfies the backdoor criterion for (X, Y) if:

1. No node in Z is a descendant of X.
2. Z blocks every path between X and Y that contains an arrow into X.

If such a Z exists, then:

```
P(Y | do(X=x)) = Σ_z P(Y | X=x, Z=z) P(Z=z)
```

This is the adjustment formula. It says: to compute the causal effect of X on Y, stratify by Z and average.

### Frontdoor criterion

When no backdoor adjustment set exists (unmeasured confounders), the frontdoor criterion may still rescue you: find a set M such that M is on every directed path X→Y, M is unconfounded with X, and no unblocked backdoor path from M to Y exists. Then:

```
P(Y | do(X=x)) = Σ_m P(m | x) Σ_{x'} P(Y | m, x') P(x')
```

## Counterfactual computation

Given an SCM and observed evidence e = {X=x, Y=y}, compute "would Y have been y' had X been x'?":

1. **Abduction** — use evidence e to update the distribution over U.
2. **Action** — replace the structural equation for X with X := x' (mutilate the graph).
3. **Prediction** — compute P(Y=y') under the modified SCM and updated U.

This is the only known formal procedure for computing individual-level counterfactuals. Every "the root cause was X" claim you want to defend mathematically reduces to a counterfactual computation in a specified SCM.

## Bayesian Networks for fault diagnosis

A Bayesian network is a DAG with a conditional probability table (CPT) at each node. When the CPTs encode *causal* rather than merely *probabilistic* dependencies, the network functions as an SCM for computing effects and counterfactuals.

### Fault-diagnosis workflow

1. Define the variables: symptoms, components, environmental factors.
2. Draw the DAG from domain knowledge (or learn it — see structure learning below).
3. Estimate CPTs from historical incident data or expert elicitation.
4. At incident time, instantiate observed variables as evidence.
5. Compute posterior P(fault | evidence) using variable elimination, junction tree, or MCMC.
6. Rank candidate faults by posterior probability × remediation cost.

### Empirical performance

Paper 2 of our mathematical-foundations research: a comparative evaluation of Bayesian network fault diagnosis across six industrial case studies found classification accuracy of 85–94% when network structure matches the physical process, dropping to 60–70% under structure misspecification. The lesson: the DAG is the hard part. A correct DAG with mediocre CPTs outperforms a wrong DAG with perfect CPTs.

### Structure learning

When you don't know the DAG a priori:

- **Constraint-based** (PC, FCI algorithms by Spirtes, Glymour, Scheines): test conditional-independence claims in the data and rule out edges that contradict them.
- **Score-based** (GES, BIC-scored search): score candidate DAGs by fit + complexity penalty, hill-climb to a local optimum.
- **Hybrid** (MMHC): constraint-based skeleton then score-based orientation.

Structure learning from observational data identifies the DAG only up to Markov equivalence — it cannot distinguish X→Y from Y→X without intervention or temporal order. Use it as a *hypothesis generator*, not as ground truth.

## Graph-theoretic fault localization

When you have a service dependency graph (or any causal graph) and want to localize a fault to a node, centrality measures help.

### Centrality measures

| Measure | Intuition | Best for |
|---|---|---|
| **Degree centrality** | How many neighbors does a node have? | Identifying hubs |
| **Betweenness** | How often does a node lie on shortest paths? | Identifying bottlenecks |
| **Closeness** | How far is a node from all others? | Identifying influential nodes |
| **Eigenvector / PageRank** | How connected are a node's neighbors? | Identifying prestige/importance |
| **Katz** | Weighted walks attenuated by distance | Weighted influence |

### Paper 3 finding (our research)

Graph centrality alone is insufficient for fault localization in microservices — it identifies *structurally* important nodes, but the structurally important node is often not where the fault is. The best-performing methods *combine* centrality with runtime metrics: weight edges by current request rate and latency, then rank by weighted centrality. This marries the static architectural view with the dynamic operational view.

## Information-theoretic methods

When you have high-frequency time series but no reliable DAG, information-theoretic measures can detect statistical coupling without assuming a generative model.

### Transfer entropy

```
TE(X → Y) = H(Y_{t+1} | Y_t^k) - H(Y_{t+1} | Y_t^k, X_t^l)
```

Transfer entropy measures how much the future of Y is predictable from the past of X *beyond* what's already predictable from Y's own past. It's directional, nonparametric, and detects nonlinear coupling.

### Mutual information

```
I(X; Y) = Σ_{x,y} P(x,y) log [P(x,y) / (P(x)P(y))]
```

Symmetric measure of statistical dependence. Not causal by itself — X and Y can have high MI because both depend on a common driver — but useful as a screening tool.

### Paper 4 finding

Transfer entropy substantially outperformed lagged correlation for fault localization in a 24-node industrial chemical process. The key advantage: transfer entropy detects *nonlinear* coupling that linear correlation misses entirely.

## Granger causality

X Granger-causes Y if past values of X help predict Y beyond what past Y values alone provide. Formally, a VAR model:

```
Y_t = Σ_i a_i Y_{t-i} + Σ_j b_j X_{t-j} + ε_t
```

Reject the null that all b_j = 0 using an F-test. If rejected, X Granger-causes Y.

### Caveats

- Granger causality is **predictive**, not **interventional**. It can be misled by a common cause with different lags to X and Y.
- It assumes linearity and stationarity unless you use nonlinear or time-varying variants.
- It works best when combined with physical domain knowledge to prune spurious hits.

## Putting it all together — a causal-inference workflow for RCA

```
Input: an incident with rich telemetry (metrics, traces, logs, events)

Step 1. Scope the question as a causal query.
        "Did X cause Y?" or "What happens to Y under do(X=x)?"

Step 2. Construct (or learn) a DAG of the system.
        — Start from known topology (service map, code dependencies)
        — Augment with structure-learning over telemetry time series
        — Validate against domain experts

Step 3. Check identifiability.
        — Is there a valid backdoor adjustment set for (X, Y)?
        — Is there a valid frontdoor set?
        — If neither, an observational answer is impossible — need an experiment.

Step 4. Estimate the causal effect.
        — Fit CPTs / structural equations from historical data
        — Use doubly-robust estimators when unsure about model form
        — Report uncertainty bands, not point estimates

Step 5. Compute counterfactuals for each candidate root cause.
        — Abduct → Act → Predict
        — Rank candidates by the counterfactual effect on the outcome

Step 6. Validate with an intervention if possible.
        — Canary, chaos experiment, or A/B test
        — Compare observed effect to the SCM's prediction
        — If they disagree, the DAG is wrong
```

## Tools and libraries

| Tool | Purpose | Language |
|---|---|---|
| **DoWhy** (Microsoft) | End-to-end causal inference pipeline | Python |
| **CausalNex** (QuantumBlack) | Bayesian network learning and inference | Python |
| **pgmpy** | Probabilistic graphical models | Python |
| **causal-learn** (CMU) | Causal discovery algorithms | Python |
| **EconML** (Microsoft) | Heterogeneous treatment effects | Python |
| **CausalImpact** (Google) | Bayesian structural time series causal inference | R |
| **Tetrad** (CMU) | Graphical causal modeling and discovery | Java |
| **bnlearn** | Bayesian network learning | R |

## Common pitfalls

### Conditioning on a collider

A collider is a node C with parents X and Y pointing into it (X → C ← Y). Conditioning on C *opens* a path between X and Y even though they're independent marginally. This is how Berkson's paradox and selection bias arise.

**Practical example:** You want to know if slow database queries cause user churn. You condition on "users who filed a support ticket" — but both slow queries and other frustrations cause support tickets. Conditioning on support-ticket-filers introduces spurious correlation.

### Mistaking a mediator for a confounder

If M is on the causal path X → M → Y, conditioning on M *blocks* the effect of X on Y and makes it look like X has no effect. This is the opposite mistake from confounder-adjustment.

### Data dredging for DAGs

Running structure-learning across many variables and picking the DAG with the best score will almost always produce an overfit structure. Pre-register your DAG from domain knowledge before looking at the data.

### Temporal ordering violations

If you use cross-sectional data (one snapshot in time), you cannot distinguish X → Y from Y → X. Use panel data or explicit time stamps.

## When causal inference is the wrong tool

Causal inference works best when:

- The system has many degrees of freedom and you want a quantitative estimate.
- You have rich observational data.
- You can formalize the question.
- The question is about *populations* or *rates*, not a single incident.

It's often the wrong tool for:

- Single-event failure investigation (use CAST or classical methods).
- Safety-critical certification (use FTA, STPA — regulators want interpretable structures).
- Fast-moving incidents (use tracing tools, escalate to causal inference in the postmortem).

## Checklist before closing a causal-inference RCA

- [ ] The causal query is stated formally.
- [ ] The DAG is specified before looking at the data and annotated with domain justification.
- [ ] Identifiability is verified (backdoor / frontdoor / neither).
- [ ] Uncertainty is reported (not a point estimate).
- [ ] Sensitivity analysis: how robust is the conclusion to unmeasured confounders?
- [ ] A validation intervention is proposed (or the reason it is impossible is documented).
- [ ] The counterfactual rationale for each claimed root cause is explicit.

## References

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books.
- Pearl, J., Glymour, M., & Jewell, N. P. (2016). *Causal Inference in Statistics: A Primer*. Wiley.
- Spirtes, P., Glymour, C., & Scheines, R. (2000). *Causation, Prediction, and Search* (2nd ed.). MIT Press.
- Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- Schreiber, T. (2000). Measuring information transfer. *Physical Review Letters*, 85(2), 461–464.
- Koller, D., & Friedman, N. (2009). *Probabilistic Graphical Models: Principles and Techniques*. MIT Press.
- Sharma, A., & Kiciman, E. (2020). DoWhy: An end-to-end library for causal inference. *arXiv:2011.04216*.
