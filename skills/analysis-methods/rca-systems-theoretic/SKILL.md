---
name: rca-systems-theoretic
description: Systems-theoretic approaches to root cause analysis for complex socio-technical systems where linear causal chains fail. Covers Nancy Leveson's STAMP (Systems-Theoretic Accident Model and Process), STPA (System-Theoretic Process Analysis) for hazard analysis, CAST (Causal Analysis based on STAMP) for post-incident investigation, Rasmussen's risk-management framework and dynamic safety model, Hollnagel's FRAM (Functional Resonance Analysis Method), and AcciMap. Use when investigating incidents in healthcare, aviation, nuclear, autonomous systems, distributed microservices, or any system where multiple actors and control loops interact — especially when classical RCA produces a "list of human errors" that leaves the underlying system design unchanged.
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/rca-systems-theoretic/SKILL.md
superseded_by: null
---
# Systems-Theoretic RCA

Classical RCA asks "what component failed?" Systems-theoretic RCA asks "what *control* failed?" The difference is not cosmetic. An incident where no component is individually broken — every actor behaved plausibly, every tool worked as specified — is incomprehensible to classical techniques but natural to systems-theoretic ones.

This skill teaches you to treat incidents as control-structure failures rather than component failures, and to use STAMP-family techniques to find the actual design flaws.

## The paradigm shift

| Classical RCA | Systems-theoretic RCA |
|---|---|
| Incidents are caused by component failures | Incidents are caused by inadequate constraints on system behavior |
| Find the broken part | Find the broken *control loop* |
| Human error is a root cause | Human error is a *symptom* of a control failure upstream |
| Linear causal chains | Feedback loops and emergent behavior |
| "Blame the operator" outcome | "Redesign the feedback mechanism" outcome |

The shift originates in Nancy Leveson's *Engineering a Safer World* (MIT Press, 2011) and her decades of work investigating Challenger, Columbia, Therac-25, and other complex-system accidents.

## Framework 1 — STAMP: Systems-Theoretic Accident Model and Process

### The core claim

Safety is a **control problem**, not a **reliability problem**. A system is safe if and only if it enforces the constraints that keep it in the safe state space. Accidents occur when these constraints are inadequate, missing, or violated — not necessarily because a component broke.

### The STAMP model components

1. **Controlled process** — the physical or logical system being operated.
2. **Controllers** — agents (human, software, automated) that issue control actions.
3. **Control actions** — commands that move the controlled process between states.
4. **Feedback** — information flowing from the controlled process back to the controller.
5. **Process model** — the controller's *internal representation* of the controlled process state.

Accidents occur when the process model diverges from reality and the controller issues an inadequate control action based on the wrong mental model. This is the formal reframing of "situational awareness failure."

### The four types of unsafe control action

STAMP classifies every control failure into one of four categories:

| # | Type | Example |
|---|---|---|
| 1 | A required control action is **not provided** | Pilot doesn't call go-around when needed |
| 2 | An **unsafe control action is provided** | Autopilot engages descent while below glidepath |
| 3 | A control action is provided at the **wrong time or in the wrong order** | Air traffic controller clears aircraft before previous landing cleared runway |
| 4 | A control action is **stopped too early or applied too long** | Medical device infusion continues past intended dose |

### Leveson's ten STAMP principles (from *Engineering a Safer World*)

1. Safety is an emergent property — it cannot be tested into a component.
2. Accidents are caused by inadequate control, not just component failure.
3. Safety constraints must be enforced at every level of the control hierarchy.
4. Human operators adapt their behavior to the actual work environment, not the designed one.
5. Organizations tend to drift toward unsafe states under economic pressure.
6. Human error is a *symptom* of system design, not a cause.
7. Classical hazard-analysis techniques (FTA, FMEA) address only component failures and miss control structure flaws.
8. Process models in controllers' heads diverge from reality over time — feedback must be designed to re-synchronize them.
9. Software safety is a control problem, not a reliability problem.
10. Accident investigation must examine the whole socio-technical control structure, not just the proximate event.

## Framework 2 — STPA: System-Theoretic Process Analysis

STPA is the **proactive hazard-analysis** application of STAMP. Use it before the accident, in place of (or alongside) FTA/FMEA. It has four steps.

### Step 1 — Define the purpose of the analysis

- **Losses:** what are the unacceptable losses? (death, data loss, financial loss, mission failure)
- **Hazards:** system states that can lead to losses given worst-case environment.
- **System-level constraints:** conditions the system must prevent or enforce.

### Step 2 — Model the control structure

Draw the hierarchical control structure: controllers, controlled processes, control actions going down, feedback going up. Include humans, software, and physical components. The structure should look like a nested set of feedback loops.

### Step 3 — Identify unsafe control actions (UCAs)

For each control action, ask: which of the four types of unsafe action could cause a hazard? Produce a UCA table:

| Control Action | Not Provided | Provided | Wrong Time/Order | Stopped/Duration |
|---|---|---|---|---|
| Landing gear extend | H1: aircraft touches down without gear | — | H2: gear extends after flare | — |
| Autopilot disconnect | H3: pilot unaware, manual input clashes | — | — | — |

### Step 4 — Identify loss scenarios

For each UCA, ask: *why* might this happen? This is the step where root causes emerge. Loss scenarios fall into categories:

- **Controller flaws:** wrong process model, inadequate algorithm, missing input.
- **Feedback flaws:** missing, delayed, wrong, or noisy feedback.
- **Control action execution flaws:** command sent but not executed, delayed, wrong.
- **Coordination flaws:** multiple controllers interfering.

### Empirical evidence for STPA

Paper 2 of our systems-theoretic research (quantitative STPA studies) found STPA identifies hazards that FTA/FMEA miss — typically software-related and multi-controller interaction hazards — while also finding most of the hazards classical techniques find. Case studies in aviation (FAA), nuclear (MIT LNS), medical devices, and autonomous vehicles consistently report STPA uncovering scenarios not present in prior FTA.

## Framework 3 — CAST: Causal Analysis based on STAMP

CAST is the **retrospective incident-investigation** application of STAMP. Where STPA looks forward, CAST looks back.

### CAST process

1. **Identify the system and losses.** What happened, what was lost?
2. **Identify system hazards.** What hazardous states led to the loss?
3. **Document the control structure at the time of the accident.**
4. **Analyze each component's role:** What control actions were issued/not issued, and what process model did the controller have?
5. **Examine the context:** environmental, organizational, economic pressures that shaped behavior.
6. **Identify systemic factors:** communication, coordination, design, safety culture.
7. **Recommend improvements to the control structure** — not "operator training" unless training gaps are genuinely the highest-leverage intervention.

### The CAST question discipline

For every human action that contributed to the accident, ask:
- What information did the actor have at that moment?
- What process model did they hold?
- Why was that process model reasonable given their inputs?
- What feedback could have corrected it?
- What pressures shaped their decision?
- What did the system *design* enable or prevent?

A CAST investigation is done when you can explain the accident to someone who believes the operators were competent professionals, and they agree the accident was foreseeable from the control structure.

## Framework 4 — Rasmussen's Dynamic Safety Model

Jens Rasmussen's (1997) risk-management framework describes organizations operating in a space bounded by three boundaries:

```
                 Boundary of economically acceptable workload
                         ↑
         Marginal zone  │
                         │
  Operating ───────────→│← Normal operating range
    point               │
                         │
         Marginal zone  │
                         ↓
                 Boundary of acceptable workload / acceptable performance
                         ↑
         Marginal zone  │
                         │
                         │
                         ↓
                 Boundary of functionally acceptable performance
                         ← Accident
```

Organizations under economic pressure drift toward the acceptable-performance boundary. Safety-management work continually pushes the operating point back from that boundary. Accidents occur when the drift rate exceeds the correction rate.

### How to use Rasmussen's model in an investigation

- Identify the three boundaries for the system at the time of the incident.
- Plot the drift trajectory: how did pressures push the operating point toward the boundary over weeks/months/years before the incident?
- Identify the *countervailing forces* that would have pushed back — were they absent, weak, or overridden?
- The root cause is often the imbalance between pressure and countervailing safety work, not the proximate trigger.

## Framework 5 — FRAM: Functional Resonance Analysis Method

Erik Hollnagel's FRAM (2012, *FRAM: The Functional Resonance Analysis Method*) embraces complexity rather than decomposing it away. Core claim: system performance is the product of interacting functional variabilities, and resonance between normal variabilities can produce abnormal outcomes.

### FRAM function representation

Each function is represented as a hexagon with six aspects:

- **I** (Input)
- **O** (Output)
- **P** (Preconditions)
- **R** (Resources)
- **T** (Time)
- **C** (Control)

### FRAM's contribution

Where STAMP focuses on *inadequate constraints*, FRAM focuses on *variability resonance*. Both can explain the same incident, but FRAM is especially useful when performance variability is inherent and cannot be eliminated (healthcare, emergency response). Hollnagel's **Safety-II** framing extends this: safety is the ability to succeed under varying conditions, not the absence of failure. Invest in what goes right at least as much as in what goes wrong.

## Framework 6 — AcciMap

Jens Rasmussen's earlier technique (1997): a cross-level accident diagram showing how decisions at each organizational level shaped the conditions for the incident.

### The six levels

1. **Government / regulatory** — laws, standards, regulator staffing.
2. **Regulators / industry associations** — enforcement, guidance, audits.
3. **Company management** — budgets, safety policies, incentives.
4. **Technical / operational management** — staffing, scheduling, training.
5. **Physical processes / actor activities** — the people and tools at the sharp end.
6. **Equipment and surroundings** — the physical and environmental conditions.

Draw arrows showing how decisions at higher levels created conditions at lower levels. AcciMap makes organizational contribution visible without requiring formal systems-theoretic training — useful as an entry point for teams new to systems thinking.

## Integration pattern — when to use which

```
Proactive (before the incident):
    STPA for hazard analysis
    FRAM for performance variability understanding
    Rasmussen's model for organizational drift assessment

Reactive (after the incident):
    CAST for control-structure investigation
    AcciMap for organizational-level contribution
    FRAM for performance-variability resonance analysis
```

You can use multiple frameworks on the same incident — each answers different questions. CAST gives you "what control failed," AcciMap gives you "what decisions shaped those controls," FRAM gives you "what variability resonated," Rasmussen gives you "what pressure drove the drift."

## Common classical-RCA mistakes that systems-theoretic techniques correct

| Classical RCA finding | Systems-theoretic reframe |
|---|---|
| "Pilot error — failed to call go-around" | The cockpit feedback design made the hazardous state indistinguishable from normal landing; pilot acted correctly on the information available. |
| "Nurse administered wrong medication" | Medication labels are ambiguous, barcode scanner workflow was bypassed due to workload pressure; the control structure did not enforce the check. |
| "SRE pushed config that broke production" | The deployment control loop had no feedback from canary metrics before global rollout; the controller had no process model of the new config's effect. |
| "Operator ignored alarm" | 200 alarms fired per shift; the operator's alarm-processing capacity was saturated, and the system had no prioritization control. |

Each of these rewrites moves the intervention from "train the human" to "fix the control structure" — a much higher-leverage change.

## HRO principles — the cultural substrate

High-reliability organizations (HROs) — aircraft carriers, nuclear plants, wildland firefighting — share five cultural practices (Weick & Sutcliffe, *Managing the Unexpected*, 3rd ed., 2015):

1. **Preoccupation with failure** — small anomalies are investigated as if they were warnings.
2. **Reluctance to simplify** — complexity is acknowledged, not collapsed into reductive explanations.
3. **Sensitivity to operations** — leaders know what's happening on the shop floor right now.
4. **Commitment to resilience** — recovery capability is developed and rehearsed.
5. **Deference to expertise** — decisions migrate to the person with the best information, regardless of hierarchy.

These are not directly RCA techniques, but they shape the organizational conditions under which systems-theoretic RCA can actually produce change.

## Checklist before closing a systems-theoretic RCA

- [ ] Control structure diagrammed at the time of the incident.
- [ ] Every identified human action is explained in terms of the process model the actor held.
- [ ] The analysis identifies *missing*, *inadequate*, or *violated* safety constraints.
- [ ] Recommendations target control-structure redesign, not operator retraining, unless retraining genuinely addresses a process-model gap.
- [ ] Organizational pressures and drift are represented (Rasmussen or AcciMap).
- [ ] The narrative would make sense to a competent professional in the actor's position.
- [ ] Corrective actions include feedback-loop improvements, not just defensive barriers.

## References

- Leveson, N. G. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press.
- Leveson, N. G., & Thomas, J. P. (2018). *STPA Handbook*. MIT Partnership for Systems Approaches to Safety and Security.
- Leveson, N. G. (2019). *CAST Handbook*. MIT Partnership for Systems Approaches to Safety and Security.
- Rasmussen, J. (1997). Risk management in a dynamic society: A modelling problem. *Safety Science*, 27(2–3), 183–213.
- Hollnagel, E. (2012). *FRAM: The Functional Resonance Analysis Method*. Ashgate.
- Hollnagel, E. (2014). *Safety-I and Safety-II: The Past and Future of Safety Management*. Ashgate.
- Weick, K. E., & Sutcliffe, K. M. (2015). *Managing the Unexpected: Sustained Performance in a Complex World* (3rd ed.). Wiley.
- Reason, J. (1997). *Managing the Risks of Organizational Accidents*. Ashgate.
