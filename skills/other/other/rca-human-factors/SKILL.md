---
name: rca-human-factors
description: Human-factors root cause analysis for incidents involving operators, crews, clinicians, or any human actors. Covers James Reason's Swiss Cheese Model and active/latent failure taxonomy, HFACS (Human Factors Analysis and Classification System), Just Culture algorithm (Marx/GAIN), Crew Resource Management (CRM) findings, and high-reliability organization (HRO) principles. Use when investigating incidents in aviation, healthcare, nuclear operations, emergency response, or any context where "operator error" is a tempting but shallow explanation and the real question is what organizational and design factors made the error foreseeable.
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/rca-human-factors/SKILL.md
superseded_by: null
---
# Human-Factors RCA

"The root cause was human error" is almost never a useful investigation finding. It stops the inquiry exactly where it should begin. This skill teaches the frameworks that treat human performance as a window into the system that produced it — so you end up redesigning the system rather than retraining the operator.

## Why "human error" is a symptom, not a cause

Sidney Dekker's principle (2014, *The Field Guide to Understanding "Human Error"*): if your RCA concludes with a person doing something wrong, you are roughly 20% through the investigation. The next 80% is the question: *why was that action reasonable from where the person was standing, with the information they had, under the pressures they faced?*

This reframing is not soft on accountability. It is the opposite: it refuses to let organizational design off the hook by letting the nearest human take the blame.

## Framework 1 — Reason's Swiss Cheese Model

James Reason (*Managing the Risks of Organizational Accidents*, 1997) proposed that defenses against accidents are arranged in layers, each with weaknesses ("holes"). An accident occurs when holes in successive layers align and a hazard passes through all defenses.

### The slices

1. **Organizational influences** — culture, resource allocation, policies, incentive structures.
2. **Unsafe supervision** — inadequate oversight, planned inappropriate operations, failure to correct known problems.
3. **Preconditions for unsafe acts** — environmental factors, fatigue, stress, poor communication, inadequate tools.
4. **Unsafe acts** — errors (slips, lapses, mistakes) and violations (routine, exceptional, sabotage).

### Active vs. latent failures

- **Active failures** — unsafe acts at the sharp end by operators in direct contact with the system. Immediate and visible.
- **Latent failures** — dormant conditions introduced upstream by decisions of designers, managers, and policymakers. May lie dormant for years before combining with a local trigger.

**Reason's insight:** latent failures are the more productive focus for investigation because they affect many future incidents, not just the one you're investigating. Fixing the sharp-end operator fixes one accident; fixing the latent condition fixes the class.

### Perneger's 2005 validation

Perneger's cross-sectional study of 159 healthcare quality professionals found widespread *misunderstanding* of the Swiss Cheese Model even among practitioners who used it weekly. Common errors:

- Treating "slices" as *sequential* (slice 1 must hold or we go to slice 2) when they are actually parallel layered defenses.
- Treating "holes" as *fixed* when they are dynamic, opening and closing with operational conditions.
- Treating "arrows" as a single trajectory when hazards can traverse multiple paths simultaneously.
- Treating active errors as the *only* causes when latent conditions usually dominate.

**Takeaway:** use the model but verify that your team's mental model of it is correct. Test understanding before running the framework.

## Framework 2 — HFACS (Human Factors Analysis and Classification System)

HFACS was developed by Shappell and Wiegmann at the U.S. Naval Safety Center (2000) as a taxonomy for classifying human-factors contributors to aviation mishaps. It is a direct operationalization of Reason's Swiss Cheese Model.

### The HFACS hierarchy

```
Organizational Influences
├── Resource Management
├── Organizational Climate
└── Organizational Process

Unsafe Supervision
├── Inadequate Supervision
├── Planned Inappropriate Operations
├── Failure to Correct a Known Problem
└── Supervisory Violations

Preconditions for Unsafe Acts
├── Environmental Factors
│   ├── Physical Environment
│   └── Technological Environment
├── Condition of Operators
│   ├── Adverse Mental States
│   ├── Adverse Physiological States
│   └── Physical/Mental Limitations
└── Personnel Factors
    ├── Crew Resource Management
    └── Personal Readiness

Unsafe Acts
├── Errors
│   ├── Decision Errors
│   ├── Skill-Based Errors
│   └── Perceptual Errors
└── Violations
    ├── Routine
    └── Exceptional
```

### How to apply HFACS

1. Extract every contributing factor from the incident narrative.
2. Classify each factor into exactly one HFACS category (with forced-choice rules).
3. Tally classifications — look for patterns across many incidents.
4. Corrective actions must target categories with high incident density, not one-off causes.

### Why it works

HFACS forces investigators to look beyond the proximate unsafe act. A well-run HFACS analysis on an aviation incident typically finds 3–5 latent conditions for every active error. Over a fleet of incidents, the taxonomy produces patterns that drive systemic interventions.

### HFACS variants

- **HFACS-ME** (maintenance environment)
- **HFACS-MI** (military operations)
- **HFACS-RR** (rail) — adapted for rail incident investigation
- **HFACS-HC** (healthcare) — adapted for clinical settings

Use the variant matched to your domain, or adapt the generic framework with domain-specific sub-categories.

## Framework 3 — Just Culture algorithm

The Just Culture concept, developed by David Marx (Outcome Engenuity) and adopted by the Global Aviation Information Network (GAIN), provides a decision algorithm for distinguishing the kind of unsafe act that calls for:

- **Console** (the actor was in the hands of an unsafe system)
- **Coach** (at-risk behavior drift needs course correction)
- **Discipline** (reckless or intentional violation)

### The three behaviors

| Behavior | Definition | Response |
|---|---|---|
| **Human error** | Unintended deviation from what was planned | Console; analyze system |
| **At-risk behavior** | Behavioral choice that increases risk where risk is unrecognized or believed justified | Coach; remove incentive |
| **Reckless behavior** | Conscious disregard of substantial and unjustifiable risk | Discipline |

### The Marx algorithm for a specific action

For each person involved in an unsafe act, walk through these questions in order:

1. **Impairment test.** Was the person impaired (drugs, alcohol, medical condition)? If yes → discipline (or medical).
2. **Foresee-ability test.** Would a professional in the same role at that moment have seen the risk? If no → human error, console.
3. **Alternate-action test.** Was there a clearly better alternative? If no → human error, console.
4. **Substitution test.** Would three similarly-situated peers have taken the same action? If yes → system problem, console.
5. **History test.** Is this a pattern of drift, or a single lapse? Pattern → at-risk, coach. Single → human error.
6. **Recklessness test.** Did the person knowingly disregard a substantial and unjustifiable risk? If yes → reckless, discipline.

A well-run Just Culture investigation protects operators from punitive responses to system-induced errors while maintaining accountability for reckless behavior. The algorithm is not a license to excuse everything — it is a disciplined classifier.

### Counterexample: punitive response undoes reporting

Organizations that punish human error destroy their own incident-reporting systems: operators learn to hide errors, and latent conditions accumulate invisibly. This is well-documented in aviation (pre-ASRS era), healthcare (pre-AHRQ PSOs), and nuclear (pre-INPO). Just Culture is an organizational survival mechanism, not moral philosophy.

## Framework 4 — CRM (Crew Resource Management)

Crew Resource Management emerged from the 1979 NASA workshop on flight-crew errors and the 1978 United 173 crash (fuel exhaustion due to captain's preoccupation with a landing-gear indicator). Its premise: technical skill is not enough; the crew as a team must manage communication, workload, and decision-making under stress.

### Core CRM topics

- **Authority gradient management** — flattening excessive authority gradients so first officers will challenge captains.
- **Closed-loop communication** — standard readback protocols.
- **Assertiveness training** — giving junior crew permission and protocols to speak up.
- **Workload management** — delegation, task prioritization, fatigue awareness.
- **Situation awareness** — shared mental model of the current operational state.
- **Error management** — acknowledging that errors will happen and building trap/recover loops.

### Paper 4 finding (our research)

The meta-analytic review of CRM training found consistent positive effects on aviation safety metrics (40–60% reduction in crew-related incidents after mature CRM adoption) but much smaller effects in healthcare, where CRM-style training was often delivered without the authority-gradient-flattening cultural change that makes it work. **CRM training without culture change is classroom theatre.**

### Healthcare CRM: TeamSTEPPS

AHRQ's TeamSTEPPS program adapted CRM for clinical settings. Key additions:

- **SBAR** (Situation-Background-Assessment-Recommendation) communication protocol.
- **CUS** (Concerned, Uncomfortable, Safety issue) escalation phrases.
- **Two-challenge rule** — if you raise a concern and it's dismissed, you're obligated to raise it again before acting.
- **Briefs / huddles / debriefs** — short structured team alignments at shift start, mid-shift, and shift end.

## Framework 5 — HRO principles

High-reliability organizations — aircraft carriers, nuclear power plants, wildland firefighting crews, air traffic control — operate complex systems with very low accident rates despite enormous intrinsic hazard. Weick and Sutcliffe (*Managing the Unexpected*, 2015) identified five cultural practices common to HROs:

1. **Preoccupation with failure.** Small anomalies are treated as precursors and investigated seriously. "Near miss" is a diagnostic tool, not a report to file.
2. **Reluctance to simplify.** Teams maintain skeptical, detailed, nuanced interpretations of what's happening. Categorical labels are resisted.
3. **Sensitivity to operations.** Leaders have direct contact with the sharp end. "Management by walking around" is cultural.
4. **Commitment to resilience.** Teams assume that something will go wrong and invest in the capacity to recover. Drill and rehearse recovery procedures.
5. **Deference to expertise.** Decision-making migrates to whoever has the best information in the moment, regardless of rank. Hierarchies flatten during operations and reassert for planning.

These five practices are not incident-investigation techniques, but they describe the organizational substrate in which human-factors RCA actually produces change. Without them, findings get filed and the same incident recurs.

## Integration pattern

```
Incident occurs
  │
  ▼
Just Culture triage
  ├── Discipline (rare) — proceed to HR process
  ├── Coach (at-risk) — document drift pattern, feedback
  └── Console (most cases) — proceed to RCA
  │
  ▼
HFACS taxonomy — classify contributing factors
  │
  ▼
Swiss Cheese mapping — identify latent conditions at each layer
  │
  ▼
CRM / teamwork analysis — was this a coordination failure?
  │
  ▼
HRO principle check — which cultural practices were absent?
  │
  ▼
Corrective actions — target latent conditions and organizational practices,
not operator retraining (unless retraining addresses a genuine skill gap)
```

## Anti-patterns to avoid

### Anti-pattern 1 — Countermeasure theater

After an incident, the organization announces "additional training" and "updated procedures." Nothing else changes. The operator who had the incident is retrained, feels ashamed, and the next operator makes the same error six months later. Recovery: ask "what would make this error physically impossible or immediately correctable," not "how do we remind people to be careful."

### Anti-pattern 2 — Paperwork apology

A lengthy incident report is filed. It is not read, it is not connected to any corrective action, and it is discovered during the next incident when someone notices the two are related. Recovery: treat the report as a work item with owners and deadlines, not an archive artifact.

### Anti-pattern 3 — Normalizing deviance

The team notices the system runs hot but doesn't fail. Hot operation becomes normal. When it eventually fails, the team discovers the safety margin was gone for months. Diane Vaughan (*The Challenger Launch Decision*, 1996) named this "normalization of deviance" — the drift of acceptance of anomalies. Recovery: re-anchor the team to first-principles safety limits periodically, not observed operating ranges.

### Anti-pattern 4 — Blame the new person

A new operator is involved in an incident; the finding is "insufficient experience" and the corrective action is additional training before solo duty. This conceals the reality that the system is not safe for *any* operator during the learning curve, and the same incident will recur with the next new hire. Recovery: redesign the onboarding or the task itself.

## Checklist before closing a human-factors RCA

- [ ] The operator's action has been reconstructed *from where they were standing*, with the information they had.
- [ ] Latent conditions are identified at each Swiss Cheese layer (not just the sharp-end acts).
- [ ] HFACS taxonomy has been applied — categories are named, not inferred.
- [ ] Just Culture triage has been performed for every actor.
- [ ] Corrective actions are system-level, not retraining-only.
- [ ] The report would be acceptable to a Just Culture review board.
- [ ] The narrative is blame-free while still naming what happened.
- [ ] The findings feed forward into proactive hazard analysis (STPA, FMEA) for related systems.

## References

- Reason, J. (1997). *Managing the Risks of Organizational Accidents*. Ashgate.
- Reason, J. (2000). Human error: Models and management. *BMJ*, 320(7237), 768–770.
- Shappell, S. A., & Wiegmann, D. A. (2000). The human factors analysis and classification system–HFACS. *DOT/FAA/AM-00/7*.
- Marx, D. (2001). *Patient Safety and the "Just Culture": A Primer for Health Care Executives*. Columbia University.
- Perneger, T. V. (2005). The Swiss cheese model of safety incidents: Are there holes in the metaphor? *BMC Health Services Research*, 5, Article 71.
- Dekker, S. (2014). *The Field Guide to Understanding "Human Error"* (3rd ed.). Ashgate.
- Weick, K. E., & Sutcliffe, K. M. (2015). *Managing the Unexpected: Sustained Performance in a Complex World* (3rd ed.). Wiley.
- Vaughan, D. (1996). *The Challenger Launch Decision*. University of Chicago Press.
- Helmreich, R. L., Merritt, A. C., & Wilhelm, J. A. (1999). The evolution of Crew Resource Management training in commercial aviation. *International Journal of Aviation Psychology*, 9(1), 19–32.
- AHRQ. (2013). *TeamSTEPPS 2.0 Pocket Guide*. Agency for Healthcare Research and Quality.
