---
name: rca-classical-methods
description: Classical root cause analysis techniques for quality improvement and incident investigation. Covers 5 Whys (with Card's 2017 critique and boundary conditions), Ishikawa/fishbone diagrams, Fault Tree Analysis (FTA), Failure Modes and Effects Analysis (FMEA), Cause Mapping, and Doggett's method-selection framework. Use when investigating a failure, running a post-incident analysis, building a fishbone, calculating fault tree cut sets, running an FMEA pass, or deciding which classical technique fits the problem. Not suitable alone for complex socio-technical failures — escalate to rca-systems-theoretic or rca-causal-inference when the incident has multiple interacting causal chains.
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/rca-classical-methods/SKILL.md
superseded_by: null
---
# Classical RCA Methods

Classical root cause analysis techniques are the inherited toolkit of quality and reliability engineering. They are best understood as a *family* with different strengths and known failure modes — not as interchangeable recipes. This skill teaches when to reach for each one, how to run it rigorously, and when to stop and escalate to a more capable method.

## The six techniques at a glance

| Technique | Origin | Best for | Known weakness |
|---|---|---|---|
| **5 Whys** | Toyota Production System (Sakichi Toyoda, Taiichi Ohno) | Simple, linear, single-cause problems on the shop floor | Forces single pathway, non-reproducible across analysts (Card 2017) |
| **Fishbone (Ishikawa)** | Kaoru Ishikawa, 1960s | Brainstorming categorized contributing factors | Can produce unwieldy diagrams, no intrinsic prioritization |
| **Fault Tree Analysis (FTA)** | Bell Labs, Minuteman ICBM (1960s) | Safety-critical systems with quantifiable failure probabilities | Requires known failure modes upfront, expensive to build |
| **FMEA** | U.S. military (MIL-P-1629, 1949); automotive (AIAG) | Proactive design review, risk prioritization via RPN | RPN ordinal-math is statistically unsound (Bowles 2003) |
| **Cause Mapping** | ThinkReliability | Multi-pathway causal narratives without imposing linearity | Tooling-dependent, visual sprawl |
| **Doggett's framework** | A. Mark Doggett (2005) | *Choosing* among the above based on problem characteristics | It is a meta-method, not an analysis technique itself |

## Technique 1 — The 5 Whys (with boundary conditions)

### What it is

Iterative questioning that walks backward from a symptom to a causal chain. Originally formalized by Taiichi Ohno within the Toyota Production System as "the basis of Toyota's scientific approach" (Ohno, 1988). Ohno's canonical example:

```
Problem: A machine stopped.
Why 1: A fuse blew because of overload.
Why 2: The bearing lubrication was inadequate.
Why 3: The lubrication pump wasn't pumping enough.
Why 4: The pump shaft was worn and rattling.
Why 5: There was no strainer attached, and metal scraps got in.
```

### Why it often fails

Alan J. Card's 2017 critique in *BMJ Quality & Safety* is the definitive takedown and must be understood before using this technique:

1. **Gross oversimplification.** Real incidents branch, converge, and interact; 5 Whys forces a single linear path.
2. **Single-pathway forcing.** One chain gets pursued, all others are invisible.
3. **Single root-cause assumption.** Complex incidents arise from the *alignment* of many contributing factors; insisting on one root cause is ideological, not empirical.
4. **Distal-link fallacy.** There is no empirical basis for the claim that the most distant link is the most effective intervention point.
5. **Inter-rater reliability failure.** Different analysts applying 5 Whys to the same incident reach different roots. This is a fundamental repeatability problem.

Card's recommendation for healthcare: **abandon 5 Whys** in favor of fishbone and multi-causal diagrams. Teruyuki Minoura, former Toyota managing director, independently called the technique "too basic" for adequate root-cause depth.

### When you may still use it

- The problem is *known* to be linear and single-cause (shop-floor equipment, simple software bugs where one variable change reproduces the failure).
- As an *entry-level probe*, explicitly chained into a fishbone or cause map for downstream widening.
- Never as the sole technique for patient safety, aviation, nuclear, or complex distributed systems.

### Running it rigorously

```
1. State the problem in observable terms. No causes, no blame.
2. Ask "why" — answer with a *factual* antecedent, not an opinion.
3. Before accepting an answer, ask: "Are there other reasons this could happen?"
   If yes, branch. You are no longer doing 5 Whys; you are building a cause map.
4. Continue until the chain reaches an actionable factor — NOT a preset depth of 5.
5. Require two independent analysts to reach the same chain. If they do not,
   the method has failed for this incident; escalate to Fishbone or STAMP.
```

## Technique 2 — Fishbone / Ishikawa diagram

### What it is

A cause-and-effect diagram that organizes contributing factors into categories attached to a spine leading to the effect (the incident). Kaoru Ishikawa developed it in the 1960s at Kawasaki Heavy Industries as part of TQM.

### The category spines

Six M's (manufacturing):
- **Man** (people, training, fatigue, communication)
- **Machine** (equipment, tools, technology)
- **Method** (process, procedure, workflow)
- **Material** (raw materials, inputs, data quality)
- **Measurement** (metrics, instruments, calibration)
- **Milieu / Mother Nature** (environment, ambient conditions)

Four P's (service industries): Policies, Procedures, People, Plant.

Eight P's (marketing): Product, Price, Place, Promotion, People, Process, Physical Evidence, Performance.

For software incidents, a modern adaptation used by SRE teams:
**Code, Config, Data, Dependency, Infrastructure, Process, People, Environment.**

### Construction steps

1. Write the effect (the problem) on the right-hand side with an arrow pointing to it.
2. Draw the spine and the category ribs.
3. For each rib, brainstorm contributing factors. Keep asking "why" at each factor to drill into sub-causes.
4. Mark each factor by evidence strength: **known**, **likely**, **hypothesis**, **ruled out**.
5. Cluster factors across ribs that share a common deeper cause — these are your candidate root causes.

### Evidence from Barsalou & Starzynska (2023)

Empirical survey of 43 Polish industrial organizations found Ishikawa was "by far the quality tool used most with 5 Whys, far exceeding all other quality tools combined." This validates the industry-standard pattern of **5 Whys as probe + Fishbone as map** rather than treating them as alternatives.

## Technique 3 — Fault Tree Analysis (FTA)

### What it is

A top-down deductive technique for tracing a specified undesired event ("top event") back through combinations of lower-level events and basic causes. Invented at Bell Labs in 1962 for the Minuteman ICBM and standardized in NUREG-0492 and IEC 61025.

### Notation

- **Top event** — the failure of interest (always a single event)
- **AND gate** — all inputs must occur for the output to occur
- **OR gate** — any input triggers the output
- **Basic events** — leaves that cannot be decomposed further (often with known failure-rate data)
- **Undeveloped events** — known but not decomposed due to scope
- **External events** — assumed inputs (e.g., "power supply failure")

### Quantitative FTA

1. Compute the **minimal cut sets** — smallest combinations of basic events whose joint occurrence causes the top event. Algorithms: MOCUS, FTREX, BDD.
2. Assign failure probabilities to each basic event (from reliability data).
3. Compute the top-event probability using cut-set summation or Binary Decision Diagrams.
4. Run **importance analysis** — Fussell-Vesely, Birnbaum, Risk Reduction Worth — to rank contributions.

### When to use

- Safety-critical, quantitative, regulator-facing (nuclear, aerospace, medical devices).
- Failure modes are reasonably well enumerated.
- You need a defensible probabilistic top-event estimate.

### When not to use

- Unknown-unknowns problem: a failure mode you haven't enumerated can't be in the tree.
- Software systems with combinatorial state spaces.
- Incidents dominated by organizational and human factors (use STAMP or HFACS instead).

## Technique 4 — Failure Modes and Effects Analysis (FMEA)

### What it is

A proactive, forward-looking technique: list every way a component or process step can fail, and rate each failure mode on three axes. Developed by the U.S. military in 1949 (MIL-P-1629), adopted by NASA for Apollo, and institutionalized in automotive via the AIAG FMEA Handbook.

### The RPN (Risk Priority Number)

```
RPN = Severity × Occurrence × Detection
```

- **Severity (S):** 1–10, how bad the effect is if it happens.
- **Occurrence (O):** 1–10, how often it happens.
- **Detection (D):** 1–10, how hard it is to catch before impact. *Higher = harder to detect*, not lower.

### The math is ordinally unsound

Bowles (2003) and later work demonstrate that multiplying ordinal ranks produces nonsense distances: the difference between RPN 120 and 125 is not meaningful, and two failure modes with the same RPN can have wildly different action priorities. AIAG's 2019 handbook replaces RPN with **Action Priority (AP)** — a lookup table that partitions S/O/D combinations into High/Medium/Low action categories without ordinal arithmetic.

**Modern guidance:** Use AP tables, not RPN, for any new FMEA. If a tool still emits RPN, ignore it and read the S/O/D triplet directly.

### The 20-year healthcare evidence

The 20-year scoping review (Paper 5 in our local research) found FMEA widely adopted in hospital settings but with poor follow-through on corrective actions. FMEA that stops at the risk table is a paperwork exercise; FMEA that drives design changes and monitoring is a risk-reduction engine.

### Running an FMEA

1. Scope the system or process. Bound what is in and out.
2. Decompose into components/steps.
3. For each element, enumerate failure modes ("how can this fail").
4. For each mode, list effects — local and system-level.
5. List causes (link into fishbone or FTA here).
6. Rate S/O/D and compute AP.
7. Assign corrective actions to every High AP and review Medium AP.
8. Track corrective-action closure. The FMEA is alive until the actions close.

## Technique 5 — Cause Mapping

### What it is

A ThinkReliability technique that builds a cause-and-effect map without forcing linearity. You write the incident as a problem, then ask "why did this happen" and attach *all* causes that jointly produced it with AND/OR logic, recursing outward. The result resembles a fault tree but is built inductively from incident narrative rather than deductively from a top event.

### Why teams like it

- Handles multi-causal incidents natively.
- Ties each cause to evidence (an attached document, log, interview quote).
- Actions are attached to specific causes, so you can see which causes are actually being addressed by your remediations.

### Practical tips

- Distinguish **causes** (things that contributed) from **solutions** (what you did).
- Do not collapse independent causes into a single box for tidiness — that reintroduces the 5 Whys flaw.
- Require evidence before any box is marked "confirmed."

## Technique 6 — Doggett's method-selection framework

A. Mark Doggett (2005, *Quality Management Journal*) published the first published framework for choosing an RCA technique based on problem characteristics. The decision matrix:

| Factor | 5 Whys | Fishbone | FTA | FMEA | Cause Map |
|---|---|---|---|---|---|
| Simple, linear | **✓** | ✓ | — | — | ✓ |
| Multi-factor | — | **✓** | ✓ | — | **✓** |
| Quantitative | — | — | **✓** | **✓** | — |
| Proactive (pre-failure) | — | — | ✓ | **✓** | — |
| Reactive (post-failure) | ✓ | **✓** | ✓ | — | **✓** |
| Brainstorming-friendly | ✓ | **✓** | — | — | ✓ |
| Evidence-linked | — | — | ✓ | ✓ | **✓** |

Use the framework as a sanity check before reaching for a familiar tool: "Is this problem actually shaped like a 5 Whys?"

## Combining techniques

The strongest classical RCA workflow chains techniques together:

```
1. Incident narrative → 5 Whys probes (rough causal chains)
2. Probes → Fishbone (structured contributing factors)
3. Fishbone → Cause Map (evidence-linked, multi-causal)
4. Critical components → FMEA (prospective prevention)
5. Safety-critical paths → FTA (quantified probabilities)
```

This chain upgrades rigor as evidence accumulates and never stops at a single technique.

## When to escalate beyond classical methods

Classical techniques assume the system is decomposable into components whose failure modes can be enumerated. Escalate to a different skill when:

- The incident is **socio-technical** — decisions across organizational boundaries contributed. → `rca-systems-theoretic` (STAMP/STPA).
- The incident is **statistical** — failure depends on joint distribution of many variables. → `rca-causal-inference` (Pearl, Bayesian networks).
- The incident is **human-factors dominated** — crew performance, fatigue, culture. → `rca-human-factors` (HFACS, Just Culture).
- The system is a **distributed microservice mesh** — trace-based causality and service dependency graphs. → `rca-distributed-systems`.

## Checklist before closing an RCA

- [ ] Problem statement is observable and blame-free.
- [ ] At least two independent analysts reached consistent conclusions.
- [ ] Multi-causal structure represented (not a single linear chain).
- [ ] Every identified cause is linked to concrete evidence.
- [ ] Corrective actions are assigned, owned, and scheduled.
- [ ] The analysis identifies both *active* failures and *latent* conditions.
- [ ] A follow-up verification date is on the calendar.

## References

- Card, A. J. (2017). The problem with '5 Whys'. *BMJ Quality & Safety*, 26(8), 671–677. DOI: 10.1136/bmjqs-2016-005849
- Barsalou, M., & Starzynska, B. (2023). Inquiry into the Use of Five Whys in Industry. *Quality Innovation Prosperity*, 27(1).
- Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press.
- Ishikawa, K. (1990). *Introduction to Quality Control*. 3A Corporation.
- Vesely, W. E., Goldberg, F. F., Roberts, N. H., & Haasl, D. F. (1981). *Fault Tree Handbook*. NUREG-0492.
- Bowles, J. B. (2003). An assessment of RPN prioritization in a failure modes effects and criticality analysis. In *Annual Reliability and Maintainability Symposium*.
- Doggett, A. M. (2005). Root cause analysis: A framework for tool selection. *Quality Management Journal*, 12(4), 34–45.
- AIAG & VDA (2019). *Failure Mode and Effects Analysis – FMEA Handbook*. Automotive Industry Action Group.
