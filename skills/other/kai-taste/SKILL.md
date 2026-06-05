---
name: kai-taste
description: "Audit or design generative AI interfaces against three diagnostic pillars (deterministic-stochastic balance, interaction density, visual cohesion). Treats taste as a measurable control system, not subjective preference. Use when: 'taste audit', 'score this UI', 'design quality', 'interaction density', 'visual cohesion', 'refiner layer', 'correction cost', 'why does this feel off', 'polish this', 'design review', or building any user-facing AI product."
---

# Design Taste: Engineering Framework

Taste is a control system that converts stochastic model output into reliable user outcomes with minimal correction cost. It is not subjective preference — it has measurable proxies, diagnosable failure modes, and an engineering protocol.

**Two modes:**
- **Audit** — score an existing UI, product, or generated output against the Three Pillars
- **Design** — apply taste principles when building new features or interfaces

**Iron law:** Taste must remain subordinate to function. The moment the system's correction vector dominates the user's intent vector, the product crosses from high-fidelity to high-friction.

---

## The Three Pillars

Every generative AI product sits in a 3-dimensional taste space. Score each pillar independently.

| Pillar | What It Measures | Control Knobs | Bad Signal |
|--------|-----------------|---------------|------------|
| **Deterministic-Stochastic Balance** | Where entropy is injected in the pipeline — where the system is creative vs reproducible | Entropy budgeting across phases, multi-sample + rerank, structured outputs (schema), tool calls as determinism anchors | User says "why did it change?" or fights the AI's personality |
| **Interaction Density** | Affordances per cognitive load unit — the cost-per-outcome ratio | Progressive disclosure, correction as first-class UI, Chat-to-Canvas transition for persistent artifacts | User manages the interface more than their task |
| **Visual Cohesion** | Perceptual grammar consistency across outputs and states | Design tokens + component grammar, semantic structure before styling, affordance protection (buttons look like buttons) | Output looks "dropped in from another system" |

These pillars form a feedback system — adjusting one shifts the feasible region of the other two.

**For detailed 1-10 scoring criteria:** Read `references/pillar-rubrics.md`

---

## Failure Modes

Too much taste is a system failure. Scan for all 8 modes during every audit.

| Failure Mode | Detection Signal | Antidote |
|-------------|-----------------|----------|
| **Stochastic Over-Constraint** | Revision entropy increases; users fight the AI's "personality" instead of steering it | Re-calibrate entropy injection points; let user steer creative vs deterministic |
| **Density Paralysis** | Choice overload; user's mental model fragments (Hick's Law violation) | Progressive disclosure; layer density spatially, not all at once |
| **Cohesion Rigidity** | Output locked in narrow aesthetic band; system fights user when intent diverges | Allow visual escape hatches; parameterize cohesion |
| **Oracle Polish** | Users over-trust because surface coherence bleeds into perceived correctness (halo effect) | Confidence-aware UI; expose uncertainty; never smooth caveats |
| **Affordance Collapse** | Users miss actions; can't tell content from controls (flat design trap) | Buttons must look like buttons; test discoverability with real users |
| **Interaction Ceremony** | Time-to-value inflated by forced wizards, confirmations, tone selectors | Remove any step that doesn't reduce correction cost; measure TTV |
| **Trust Distortion** | Users accept outputs because they *sound* right, not because they verified | Calibrate confidence to reliability; never use persona polish to mask uncertainty |
| **Metric Gaming** | Proxies improve but product quality degrades (Goodhart's Law) | Pair every metric with a counter-metric; run periodic qualitative audits |

---

## North Star Metrics

Taste is an unobservable latent variable. Measure these proxies instead.

| Metric | Formula | Plain English | Bad Looks Like |
|--------|---------|--------------|----------------|
| **Refinement Velocity** | `Vr = 1 / n_prompts` | Fewer prompts to accepted final state | User needs 5+ turns to get something usable |
| **Correction Density** | `Dc = manual_edits / generated_tokens` | How much cleanup is needed | Heavy post-generation editing on every output |
| **Kinetic Friction** | `Fk = t_action - t_render` | Time between seeing output and first meaningful action | Too fast (no thinking, oracle trust) or too slow (navigation overhead) |
| **Time-to-Value** | Seconds to first artifact surviving >30s without modification | How quickly users get something useful | Slow first output; high churn in first session |
| **Correction Effort** | Edit distance between generated and accepted output | Total cleanup cost | Output requires heavy reformatting to become usable |
| **Dismissal Rate** | % of AI suggestions ignored, collapsed, or dismissed | Relevance + intrusion control | System is noisy; users suppress it to work |
| **Clarification Burden** | Average turns before a stable artifact exists | Interaction density tax | Users spend turns explaining instead of building |

**Moderate kinetic friction is optimal.** Too low = oracle trust (users accept without thinking). Too high = navigation overhead eats productivity. Target the zone where users think, then act.

---

## Routing: Which Reference to Read

| Situation | Action |
|-----------|--------|
| **Scoring a pillar in detail** | Read `references/pillar-rubrics.md` for 1-10 criteria with observable evidence |
| **Building something new (Design mode)** | Read `references/refiner-protocol.md` for the 10-step Refiner Layer |
| **Want the theoretical "why"** | Read `references/theory-foundations.md` for information theory, neuroscience, cognitive load |
| **Auditing a live URL** | Use browse daemon: `$B goto <url>`, `$B snapshot -i -a`, `$B screenshot` |
| **Auditing code or mockups** | Read files directly, score against pillar rubrics |

---

## Audit Mode Protocol

Use this when scoring existing work.

### Step 1: Identify the Subject

What are we auditing?
- **Live URL** — use browse daemon for snapshots (take at mobile 375px, tablet 768px, desktop 1440px)
- **Code** — read the source files and rendered output
- **Mockup / design file** — read or screenshot the design
- **Generated output** — evaluate the content directly

### Step 2: Score Each Pillar (1-10)

Read `references/pillar-rubrics.md` for detailed scoring criteria. Quick reference:

**Deterministic-Stochastic Balance:**
- Where is entropy injected? Is it phase-aware (exploration vs execution)?
- Are structured outputs used where reliability matters?
- Can users toggle between creative and deterministic modes?

**Interaction Density:**
- How many turns/clicks to reach first useful output?
- Is correction cheap (edit-in-place, diffs) or expensive (re-prompt from scratch)?
- Are advanced controls hidden by default (progressive disclosure)?
- Is state persistent (canvas/artifact) or ephemeral (chat)?

**Visual Cohesion:**
- Does output render through a component grammar or raw text?
- Are affordances visible (buttons, links, actions clearly distinguishable)?
- Is typography, spacing, and hierarchy consistent across all states?
- Does generated content look native to the surrounding UI?

### Step 3: Scan Failure Modes

Check all 8 failure modes from the table above. For each, mark Present/Absent with evidence.

### Step 4: Measure Available Metrics

Which north star metrics can you compute from observation?
- Count turns to acceptance (Refinement Velocity)
- Estimate edit distance (Correction Density)
- Time the gap between render and first action (Kinetic Friction)

### Step 5: Output the Scorecard

```markdown
## Taste Audit: [Subject]
**Date:** [date]
**Auditor:** [name/agent]

### Pillar Scores
| Pillar | Score | Key Finding | Recommended Fix |
|--------|:-----:|-------------|-----------------|
| Deterministic-Stochastic Balance | /10 | | |
| Interaction Density | /10 | | |
| Visual Cohesion | /10 | | |
| **Composite** | **/30** | | |

### Failure Mode Scan
| Mode | Present? | Evidence | Severity |
|------|:--------:|----------|:--------:|
| Stochastic Over-Constraint | | | |
| Density Paralysis | | | |
| Cohesion Rigidity | | | |
| Oracle Polish | | | |
| Affordance Collapse | | | |
| Interaction Ceremony | | | |
| Trust Distortion | | | |
| Metric Gaming | | | |

### Metrics (if measurable)
| Metric | Observed Value | Assessment |
|--------|:--------------:|------------|
| Refinement Velocity | | |
| Correction Density | | |
| Kinetic Friction | | |
| Time-to-Value | | |

### Prioritized Fixes
| P | Fix | Pillar | Impact |
|:-:|-----|--------|:------:|
| 0 | | | |
| 1 | | | |
| 2 | | | |

### Grade
- 25-30 = **A** (taste is a competitive asset)
- 20-24 = **B** (solid, minor gaps)
- 15-19 = **C** (functional but friction-heavy)
- 10-14 = **D** (taste is actively hurting the product)
- <10   = **F** (taste is absent or harmful)

**Overall: [Grade]**
```

### Step 6: Prioritize Fixes

Map findings to P0 (blocking UX) / P1 (significant friction) / P2 (polish). Fix P0s before shipping.

---

## Design Mode Protocol

Use this when building new features or interfaces.

### Step 1: Define the Taste Contract

Translate quality goals into **testable constraints**, not adjectives:
- What must be reproducible? (deterministic zones)
- Where is creativity allowed? (stochastic zones)
- What must never happen? (hard constraints)
- Reading level, verbosity ceiling, required sections, prohibited moves
- Citation rules, formatting grammar, interaction rules

### Step 2: Pre-Score Against Three Pillars

Before building, predict where you'll land on each pillar. Identify the target score band and what observable criteria you need to hit.

### Step 3: Apply the Refiner Layer

Read `references/refiner-protocol.md` for the full 10-step protocol. Summary:
1. Define taste contract as constraints, not adjectives
2. Separate divergence (exploration) from convergence (refinement)
3. Generate structured intent representation before drafting
4. Draft into intermediate representation, not directly into final UI
5. Run critic pass with explicit rubrics
6. Refine via diffs, not rewrites
7. Anchor truth with tools, then re-render
8. Compile to UI using component grammar
9. Guarantee correction affordances at the surface
10. Instrument taste as feedback loops

### Step 4: Pre-Mortem Failure Modes

Run through all 8 failure modes as a pre-mortem: which could this design fall into?
- If adding polish: check for Oracle Polish and Cohesion Rigidity
- If adding features: check for Density Paralysis and Interaction Ceremony
- If reducing friction: check for Agency Collapse (IKEA effect loss)
- If showing confidence: check for Trust Distortion

### Step 5: Plan Metrics Instrumentation

Decide which north star metrics you will track and how:
- Log time-to-first-value
- Track edit operations per session
- Count regenerations and diff rejections
- Monitor dismissal rates
- Pair every metric with a counter-metric (Goodhart protection)

### Design Checklist

Run before shipping any user-facing AI feature:

**Deterministic-Stochastic Balance**
- [ ] Entropy injection points identified (where creative, where locked)
- [ ] Structured outputs enforced for downstream actions
- [ ] Tool calls used for factual queries instead of model guessing
- [ ] Multi-sample + rerank for quality-sensitive outputs
- [ ] User can toggle between exploration and execution modes

**Interaction Density**
- [ ] Default path is shallow (progressive disclosure)
- [ ] Correction is cheap (edit-in-place, scoped refine, accept/reject diffs)
- [ ] Advanced controls contextual, not upfront
- [ ] Persistent artifacts used for multi-step work (not buried in chat)
- [ ] State externalized as manipulable objects

**Visual Cohesion**
- [ ] Outputs compile through component grammar (not raw text to UI)
- [ ] Semantic structure enforced before styling (headings, sections, callouts)
- [ ] Affordance protection (buttons look like buttons, links look like links)
- [ ] Design tokens consistent across all output states
- [ ] Generated content indistinguishable from hand-authored content in the same UI

**Anti-Failure-Mode Gates**
- [ ] Uncertainty is signaled, not smoothed (anti-Oracle Polish)
- [ ] User can override/escape system suggestions (anti-Cohesion Rigidity)
- [ ] No forced steps that don't reduce correction cost (anti-Interaction Ceremony)
- [ ] Trust calibrated to actual reliability (anti-Trust Distortion)
- [ ] Selective friction preserves user agency (anti-Agency Collapse)

---

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Taste is subjective, can't be scored" | Taste has measurable proxies: correction cost, time-to-value, dismissal rate |
| "More polish = more taste" | Oracle Polish is a failure mode. Polish that outpaces reliability destroys trust |
| "Minimize all friction" | Selective friction (IKEA effect) builds ownership. Remove friction only where it doesn't reduce understanding |
| "The model output IS the product" | The model is a probabilistic component. The Refiner Layer makes it feel authored |
| "Chat is good enough" | Chat serializes multi-dimensional state into a 1D stream. Canvas externalizes memory |
| "Make it beautiful and it's tasteful" | Cohesion Rigidity and Affordance Collapse are both beauty-caused failures |
| "Users want everything instantly" | Optimal pacing is layered: immediate ack (0.1s), provisional structure (1s), deferred commitment (seconds) |
| "Show confidence to build trust" | Uncalibrated confidence creates the Uncanny Valley of Agency. Transparency builds trust |

---

## Source Material

For the full 40,000-word theoretical foundation, see:
- `taste/taste.md` — Foundation taxonomy, North Star metric, 5-step Refiner
- `taste/chatgpt_taste.md` — Engineering framework, 10-step Refiner, proxy metrics
- `taste/deep-research-report.md` — Neuroscience, cognitive load, agency, RLDF spec
- `taste/AI Design Taste_ A Systems Approach.md` — Information theory, SDEs, style weights
- `taste/Engineering AI Design Taste Framework.md` — Operationalization, failure modes, synthesis
