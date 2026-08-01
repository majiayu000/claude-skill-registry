---
name: kai-taste
description: "Audit or design generative AI interfaces against three diagnostic pillars (deterministic-stochastic balance, interaction density, visual cohesion). Treats taste as a measurable control system, not subjective preference. Use when: 'taste audit', 'score this UI', 'design quality', 'interaction density', 'visual cohesion', 'refiner layer', 'correction cost', 'why does this feel off', 'polish this', 'design review', or building any user-facing AI product."
---

# /kai-taste — a scored diagnosis of why an AI product feels off, and what to change

## Objective

Taste treated as a control system: the thing that converts stochastic model output into reliable user outcomes at minimal correction cost. Two modes share one destination — a defensible position in the three-pillar space with evidence behind every claim.

**Audit mode** produces a scored diagnosis of an existing UI, product, or generated output: a number per pillar, a present/absent call on all eight failure modes with the observation that supports it, whichever north-star metrics are computable, and a prioritized fix list.

**Design mode** produces a taste contract for something being built: which zones are deterministic, which are stochastic, what must never happen, and the instrumentation that will show whether the design landed.

**Iron law:** taste stays subordinate to function. The moment the system's correction vector dominates the user's intent vector, the product crosses from high-fidelity to high-friction.

## Done when

Work type `audit-report` — floor **E3/C4/O1** (`harness/eco-floors.yaml`). Design-mode output ships inside the feature it informs, and that feature's own work type governs its floor.

- **E3** — a named human approved the exact scorecard, and every score, failure-mode call, and metric resolves to a recorded observation: a screenshot at a stated viewport, a snapshot, a source file and line, or a session recording.
- **C4** — provenance holds. `banned_word_check` clean, and no score, metric, or claim is estimated. A pillar that cannot be observed is scored as unobserved with the missing evidence named — never averaged in from impression.
- **O1** — every P0 fix names the metric it targets (correction density, time-to-value, dismissal rate, clarification burden), its current value or the reason it cannot be read yet, the threshold that counts as fixed, and an owner.

**Grade bands** on the composite (three pillars, /30): 25–30 = **A**, taste is a competitive asset · 20–24 = **B**, solid with minor gaps · 15–19 = **C**, functional but friction-heavy · 10–14 = **D**, taste is actively hurting the product · below 10 = **F**, taste is absent or harmful.

## Constraints

- **Score all three pillars and scan all eight failure modes every audit.** A partial scan reports a partial product.
- **Read `references/pillar-rubrics.md` before assigning a number.** The 1–10 criteria carry observable evidence requirements; a score without the rubric is a preference.
- **Fixes are ranked P0 (blocking UX) / P1 (significant friction) / P2 (polish). P0s clear before ship.**
- **A taste contract states testable constraints, never adjectives.** Reading level, verbosity ceiling, required sections, prohibited moves, citation rules, formatting grammar, interaction rules — each one checkable.
- **Pair every metric with a counter-metric.** Proxies improve while quality degrades whenever the proxy becomes the target (Goodhart), so periodic qualitative audits sit alongside the numbers.
- **Moderate kinetic friction is the target.** Too low produces oracle trust, where users accept output without thinking. Too high means navigation overhead eats the productivity gain.
- **Polish that outpaces reliability is a defect.** Never smooth a caveat, never use persona polish to mask uncertainty, and never let surface coherence stand in for correctness.
- **Live-URL audits capture all three viewports** — 375px mobile, 768px tablet, 1440px desktop — before any score is assigned.

## Context

| Need | Load / run |
|---|---|
| 1–10 scoring criteria with observable evidence | `references/pillar-rubrics.md` |
| The 10-step Refiner Layer (design mode) | `references/refiner-protocol.md` |
| Information theory, neuroscience, cognitive load — the "why" | `references/theory-foundations.md` |
| Auditing a live URL | Browse daemon: `$B goto <url>` · `$B snapshot -i -a` · `$B screenshot` |
| Auditing code or mockups | Read the source and rendered output directly, score against the rubrics |
| The full theoretical foundation, when a score needs defending | `docs/research/taste/taste.md` (taxonomy, North Star, 5-step Refiner) · `docs/research/taste/chatgpt_taste.md` (engineering framework, proxy metrics) · `docs/research/taste/deep-research-report.md` (neuroscience, cognitive load, agency) · `docs/research/taste/AI Design Taste_ A Systems Approach.md` (information theory, style weights) · `docs/research/taste/Engineering AI Design Taste Framework.md` (operationalization, failure modes) |

**The three pillars.** Every generative AI product sits somewhere in this space; the pillars form a feedback system, so moving one shifts the feasible region of the others.

| Pillar | Measures | Control knobs | Bad signal |
|---|---|---|---|
| **Deterministic-Stochastic Balance** | Where entropy enters the pipeline — where the system is creative vs reproducible | Entropy budgeting per phase, multi-sample + rerank, structured outputs, tool calls as determinism anchors | "Why did it change?" — users fight the AI's personality instead of steering it |
| **Interaction Density** | Affordances per unit of cognitive load — the cost-per-outcome ratio | Progressive disclosure, correction as first-class UI, chat-to-canvas for persistent artifacts | The user manages the interface more than the task |
| **Visual Cohesion** | Perceptual grammar consistency across outputs and states | Design tokens + component grammar, semantic structure before styling, affordance protection | Output looks dropped in from another system |

**Failure modes.** Too much taste is a system failure. Scan for all eight:

| Mode | Detection signal | Antidote |
|---|---|---|
| Stochastic Over-Constraint | Revision entropy rises; users fight the model's personality | Recalibrate entropy injection points; let the user steer creative vs deterministic |
| Density Paralysis | Choice overload; mental model fragments (Hick's Law) | Progressive disclosure; layer density spatially |
| Cohesion Rigidity | Output locked in a narrow aesthetic band; system fights divergent intent | Visual escape hatches; parameterize cohesion |
| Oracle Polish | Surface coherence bleeds into perceived correctness (halo effect) | Confidence-aware UI; expose uncertainty; never smooth caveats |
| Affordance Collapse | Users miss actions; content and controls are indistinguishable | Buttons must look like buttons; test discoverability with real users |
| Interaction Ceremony | Time-to-value inflated by wizards, confirmations, tone selectors | Remove any step that does not reduce correction cost; measure TTV |
| Trust Distortion | Users accept output because it sounds right, unverified | Calibrate confidence to actual reliability |
| Metric Gaming | Proxies improve while product quality degrades (Goodhart) | Counter-metric per metric; periodic qualitative audits |

**North star metrics.** Taste is a latent variable; these are its proxies.

| Metric | Formula | Bad looks like |
|---|---|---|
| Refinement Velocity | `Vr = 1 / n_prompts` | 5+ turns to something usable |
| Correction Density | `Dc = manual_edits / generated_tokens` | Heavy cleanup on every output |
| Kinetic Friction | `Fk = t_action - t_render` | Too fast (oracle trust) or too slow (navigation overhead) |
| Time-to-Value | Seconds to a first artifact surviving 30s unmodified | Slow first output; first-session churn |
| Correction Effort | Edit distance from generated to accepted | Heavy reformatting before it is usable |
| Dismissal Rate | % of suggestions ignored, collapsed, or dismissed | Users suppress the system to get work done |
| Clarification Burden | Turns before a stable artifact exists | Users explain instead of building |

**Design-mode gates**, run before shipping a user-facing AI feature. *Balance:* entropy injection points identified, structured outputs enforced for downstream actions, tool calls for factual queries, multi-sample + rerank where quality matters, user-togglable exploration vs execution. *Density:* shallow default path, cheap correction (edit-in-place, scoped refine, accept/reject diffs), contextual advanced controls, persistent artifacts for multi-step work, state externalized as manipulable objects. *Cohesion:* outputs compile through component grammar, semantic structure before styling, affordance protection, tokens consistent across states, generated content indistinguishable from hand-authored. *Anti-failure:* uncertainty signaled rather than smoothed, user can override or escape suggestions, no step that fails to reduce correction cost, trust calibrated to reliability, selective friction preserved to protect agency.

**Corrections to common assumptions**, worth stating because each one reverses a default instinct:

| Assumption | Reality |
|---|---|
| Taste is subjective and cannot be scored | It has measurable proxies: correction cost, time-to-value, dismissal rate |
| More polish means more taste | Oracle Polish is a failure mode; polish outpacing reliability destroys trust |
| Minimize all friction | Selective friction builds ownership (IKEA effect); remove it only where it does not reduce understanding |
| The model output is the product | The model is a probabilistic component; the Refiner Layer makes it feel authored |
| Chat is good enough | Chat serializes multi-dimensional state into one stream; canvas externalizes memory |
| Make it beautiful and it is tasteful | Cohesion Rigidity and Affordance Collapse are both beauty-caused |
| Users want everything instantly | Optimal pacing is layered: acknowledgment 0.1s, provisional structure 1s, deferred commitment seconds |
| Show confidence to build trust | Uncalibrated confidence creates the uncanny valley of agency; transparency builds trust |

## Escalate when

- A pillar cannot be observed with the access available — say so and score it unobserved rather than inferring.
- Metrics require instrumentation the product does not have, and the fix list depends on them.
- A P0 fix conflicts with a stated product or business constraint.
- The requested polish would raise perceived confidence above measured reliability.
- Audit findings imply changes to a live product surface that nobody has authorized.
