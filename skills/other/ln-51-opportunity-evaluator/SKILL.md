---
name: ln-51-opportunity-evaluator
description: "Evaluates new product directions using current demand, acquisition, competition, economics, and validation evidence. Use before commitment; not for backlog or implementation planning."
---

# Opportunity Evaluator

Evaluate product opportunities before implementation commitment. Start from observable demand and a reachable acquisition path, eliminate weak candidates early, and recommend one low-cost validation step without manufacturing market precision.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Product and constraints | User context plus existing product, analytics, customer, and strategy documents | Establishing audience, assets, channels, economics, and non-goals | State assumptions and request only consequential missing intent |
| Current demand and acquisition | Web research, trend or marketplace data, communities, reviews, ads, directories, and primary customer evidence | Every external market claim that affects elimination or recommendation | Mark the signal unavailable; never infer a number from search-result count |
| Competition and pricing | Competitor product pages, pricing, release history, distribution channels, reviews, and public filings where relevant | Establishing substitutes, willingness-to-pay signals, and credible differentiation | Use qualitative evidence with explicit confidence |
| Feasibility and validation cost | Existing capabilities, public APIs, regulations, platform rules, and current official documentation | Comparing the cheapest credible experiment and major blockers | Label estimates and name the evidence still required |

Keep the evaluation read-only. Do not create project files, roadmaps, Epics, Stories, implementation plans, campaigns, listings, advertisements, or customer outreach.

## Evidence Classes

| Class | Meaning |
|---|---|
| `MEASURED` | Direct analytics, transactions, experiments, or instrumented observations with known method and date |
| `REPORTED` | A primary source reports a value or behavior, but the underlying measurement is not independently available |
| `ESTIMATED` | A stated model based on explicit inputs and assumptions |
| `INFERRED` | A qualitative conclusion from observable proxies |
| `UNKNOWN` | Evidence is unavailable, stale, incomparable, or too weak to support a decision |

Do not turn `REPORTED`, `ESTIMATED`, or `INFERRED` evidence into a measured market size, search volume, conversion rate, revenue, or willingness-to-pay claim. Date every external source and distinguish the event date from the publication date when they differ.

## Checklist

### 1. Frame the Decision

- [ ] Resolve the existing product or capability, target users, decision horizon, available assets, geographic or regulatory scope, constraints, and explicit non-goals.
- [ ] Accept user-supplied candidates or generate a bounded set of materially distinct opportunities from product context and current signals; do not create cosmetic variants of one idea.
- [ ] Define what would justify deeper validation: identifiable user and problem, observable demand, reachable channel, credible value exchange, differentiating wedge, and affordable experiment.
- [ ] Separate discovery of a new direction from prioritization of already committed work or implementation planning.
- [ ] Record assumptions that can reverse the recommendation and identify which are discoverable through research versus user intent.

### 2. Collect One Evidence Bundle per Candidate

- [ ] Identify who experiences the problem, how they solve it today, what triggers active search or purchase, and what evidence shows the pain is recurring or costly.
- [ ] Find a reachable acquisition channel and its mechanism: query, marketplace category, integration ecosystem, community, partner, outbound audience, or another observable path.
- [ ] Inspect direct competitors, substitutes, do-nothing behavior, pricing, positioning, distribution, review complaints, and evidence of continued investment or abandonment.
- [ ] Examine economic signals without inventing unit economics: price anchors, budget owner, purchase frequency, switching cost, delivery cost, platform fees, and support burden.
- [ ] Identify implementation, data, dependency, regulation, trust, distribution, and operational blockers that affect the cost of a validation experiment.
- [ ] Capture source, date, evidence class, scope, confidence, contradiction, and the candidate decision each signal can change.
- [ ] Stop researching a candidate once the evidence is sufficient to eliminate it or additional sources cannot change its status.

### 3. Apply Evidence-First Elimination

- [ ] Eliminate a candidate when no specific user problem, observable demand signal, reachable channel, credible value exchange, or feasible validation path can be established.
- [ ] Treat competition as evidence of demand and constraints, not an automatic rejection; require a concrete wedge against substitutes and the do-nothing option.
- [ ] Do not use universal thresholds for search volume, competitor count, ARPU, market size, or MVP duration.
- [ ] Preserve candidates with weak public data as `UNKNOWN` rather than labeling them invalid when a cheap primary experiment can resolve the uncertainty.
- [ ] Record the decisive evidence and falsification condition for every eliminated candidate so rejection is reproducible.
- [ ] Only after external viability, ask whether the owner is willing and able to pursue the audience, channel, operating model, and validation effort; do not infer personal interest.

### 4. Compare Survivors and Choose the Next Experiment

- [ ] Compare survivors on evidence strength, problem severity, channel reachability, differentiation, economics, validation cost, strategic fit, and reversibility without collapsing them into a fake composite score.
- [ ] Preserve meaningful disagreements and sensitivity: show which assumption would cause another candidate to become preferable.
- [ ] Select one primary recommendation only when its evidence is materially stronger for the stated goal; otherwise return `INCONCLUSIVE`.
- [ ] Define the cheapest credible validation experiment that tests the weakest decisive assumption through observed behavior rather than stated purchase intent alone.
- [ ] Specify experiment audience, channel, offer or prototype, success and failure evidence, budget or time boundary, safety constraints, and stop rule without pretending to know the result.
- [ ] Prefer reversible tests such as concierge delivery, prototype usage, pricing or preorder intent with appropriate disclosure, channel response, or integration demand before implementation commitment.

### 5. Validate and Report

- [ ] Recheck every consequential external claim against a current primary source or label it with the weaker evidence class and limitation.
- [ ] Separate facts, estimates, inferences, owner preferences, and unresolved unknowns in the final result.
- [ ] Use `RECOMMEND <candidate>` only when the candidate has a credible demand signal, reachable channel, differentiating path, plausible value exchange, and executable validation experiment.
- [ ] Use `INCONCLUSIVE` when evidence cannot distinguish the leading candidates or a cheap experiment is required before choosing.
- [ ] Use `BLOCKED` when the decision lacks product context, candidate scope, lawful research access, or a safe validation boundary.
- [ ] Return one recommendation or an explicit inconclusive result, eliminated and deferred candidates with reasons, the next experiment, source limitations, and residual risks without creating files or implementation work.

## Output Contract

```markdown
# Opportunity Evaluation

**Verdict:** RECOMMEND <candidate> | INCONCLUSIVE | BLOCKED

## Decision context
- Product, audience, constraints, candidates, and assumptions

## Evidence comparison
| Candidate | Demand | Reachable channel | Competition and wedge | Economics | Validation cost | Confidence |
|---|---|---|---|---|---|---|
| ... | evidence class + source | ... | ... | ... | ... | ... |

## Eliminated and deferred candidates
| Candidate | Status | Decisive evidence or unresolved unknown | Resolution or falsification condition |
|---|---|---|---|
| ... | ELIMINATED / UNKNOWN | ... | ... |

## Recommendation and next validation experiment
Primary choice or reason for inconclusive result, experiment contract, stop rule, and decision-changing evidence.

## Source limitations and residual risks
Stale, unavailable, contradictory, estimated, or inferred evidence and unresolved owner choices.
```
