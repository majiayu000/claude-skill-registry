---
name: soft-predict-future
description: >
  Activate this skill for ANY future-oriented question. Triggers include: "Will [X]?",
  "Who will win [X]?", "What happens to [X]?", "Can [X] succeed?", "What's the future of X?",
  foresight analysis, scenario planning, STEEEP analysis, futures cone, prediction requests,
  or any question about a future outcome. Year is NOT required — the engine infers the horizon.
  Also activate when the user says "predict", "forecast", "what are the odds", "scenario analysis",
  or asks about competitive races, technology adoption, geopolitical shifts, or market dominance.
  REQUIRES web search to be enabled — if web search is unavailable, tell the user before proceeding.
---

# Soft Predict Future — Foresight Engine

Activate when the user asks any future-oriented question — "Will [X]?", "Who will win [X]?", "What happens to [X]?", "Can [X] succeed?", or any question about a future outcome. **Year is NOT required.** Also activate on: foresight analysis, scenario analysis, STEEEP, futures cone, or any prediction request.

---

## Try Asking

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRY ASKING  (year optional — engine infers the horizon)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ Who will win — Google or Perplexity?
■ Will OpenAI or Anthropic dominate the AI race?
■ Will India become the global AI leader?
■ Will crypto replace banks?
■ Will remote work become permanent?
■ Will EVs dominate Indian cities by 2032?
■ Will UPI become Southeast Asia's default payment rail by 2028?
■ Will Europe lead the green energy transition by 2035?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **Soft Predict Future** uses Claude's native reasoning + web search. Outputs are structurally correct and fast. For deterministic, auditable scoring say: **"Run hard predict future: [your question]"**

---

## The 9-Step Pipeline

Execute ALL steps in order. Never skip. Never combine. Show your work at each step.

---

### Step 1 — Validate Input

Apply exactly 5 binary rules. If ANY rule fails, stop and explain why. Do not proceed.

**Rule 1 — Entity Reality:** Does the entity actually exist in the real world? Fail if fictional, hypothetical, or unnamed.

**Rule 2 — System Existence:** Is the domain observable and researchable? Fail if purely philosophical or metaphysical.

**Rule 3 — Time Horizon:** Is the outcome observable within a 2–30 year window? A specific year is NOT required. If no year is given, infer the most reasonable horizon from the question's nature:
- Competitive race / market dominance questions → 3–10 years (Strategic)
- Technology adoption questions → 5–15 years (Strategic)
- Geopolitical / societal shift questions → 10–20 years (Civilizational)
- Company survival / near-term outcome → 2–5 years (Operational/Strategic)

Fail ONLY if the implied timescale is geological, post-human, or clearly beyond 30 years.

After applying Rule 3, state the inferred horizon (e.g. "2026–2033" or "2028–2038").

**Rule 4 — Signal Availability:** Could real-world evidence plausibly exist? Fail if classified, purely speculative, or unpublished.

**Rule 5 — Minimum Specificity:** Is the question specific enough to produce distinct scenario outcomes? Fail if trivially true for any answer.

Output:
```
VALIDATION
Rule 1 Entity Reality:      PASS / FAIL — [reason]
Rule 2 System Existence:    PASS / FAIL — [reason]
Rule 3 Time Horizon:        PASS / FAIL — [reason] | Inferred horizon: [YYYY–YYYY]
Rule 4 Signal Availability: PASS / FAIL — [reason]
Rule 5 Specificity:         PASS / FAIL — [reason]
Result: PROCEED / STOP
```

---

### Step 2 — Collect Signals

Run exactly 6 web searches. Collect a minimum of 18 signals total. Do not proceed with fewer than 18.

**Search 1:** Current state — `"[topic] current status [year]"`
**Search 2:** Growth indicators — `"[topic] growth data market size [year]"`
**Search 3:** Barriers and headwinds — `"[topic] challenges barriers risks"`
**Search 4:** Policy and regulation — `"[topic] government policy regulation"`
**Search 5:** Technology or infrastructure enablers — `"[topic] technology infrastructure investment"`
**Search 6:** Historical precedent — `"[topic] historical analogue similar transition"`

For each signal, classify all 6 attributes:

| Attribute | Values |
|---|---|
| direction | supporting / opposing / wildcard / neutral |
| steeep_category | Social / Technological / Economic / Environmental / Ethical / Political |
| temporal_layer | Operational (0–3yr) / Strategic (3–10yr) / Civilizational (10+yr) |
| source_type | primary / secondary / opinion |
| recency_days | integer |
| has_evidence | true / false (contains a number, date, or measurable fact) |

Present signals in a table with all 6 columns filled for every row.

---

### Step 3 — Score Signals

Score every signal individually using this formula:

```
score = recency_weight × reliability_weight × type_weight × evidence_multiplier
```

Cap at 1.0. Round to 2 decimal places.

**Recency weights:**
- 0–90 days: 1.00 · 91–365 days: 0.80 · 1–3 years: 0.60 · 3+ years: 0.40 · unknown: 0.50

**Reliability weights:**
- Primary (government/official): 1.00
- Established news (Reuters, Bloomberg, FT, ET): 0.90
- Industry report (McKinsey, Gartner, NASSCOM): 0.85
- Analyst commentary: 0.70 · Opinion/blog/social: 0.50 · Unknown: 0.40

**Type weights:**
- Supporting: 1.00 · Opposing: 1.00 · Neutral: 0.60 · Wildcard: 1.30

**Evidence multiplier:**
- DATA / STATISTIC: × 1.20 · EVENT / INCIDENT: × 1.00 · ANALYSIS / OPINION: × 0.70

Apply regional multiplier after base score:
```
final_score = min(1.0, base_score × regional_multiplier[steeep][temporal])
```

Show scoring table: Signal | recency_w | reliability_w | type_w | evidence_mult | base_score | regional_mult | final_score

---

### Step 4 — Extract Structural Drivers

A **driver** is the deep structural force that explains WHY a cluster of signals exists. Signals are observable. Drivers are causal.

After scoring, group signals by STEEEP category. For each cluster of 3+ signals in the same category, identify the underlying driver.

Extract exactly **3 top drivers**, ranked by the sum of final_scores of the signals they explain.

For each driver state:
- **Name:** 3–5 word label (e.g. "India DPI Infrastructure Advantage")
- **Force:** One sentence — the structural reality this driver represents
- **Signals it explains:** List the signal IDs it accounts for
- **Temporal reach:** Operational / Strategic / Civilizational
- **Stability:** LOCKED (unlikely to change in 10yr) / SHIFTING (could change in 3–5yr) / FRAGILE (could reverse in 1–2yr)

Output:
```
STRUCTURAL DRIVERS
D1 [Name] — [Force]
   Explains: [signal list] | Temporal: [layer] | Stability: [tier]

D2 [Name] — [Force]
   Explains: [signal list] | Temporal: [layer] | Stability: [tier]

D3 [Name] — [Force]
   Explains: [signal list] | Temporal: [layer] | Stability: [tier]
```

Drivers feed directly into scenario writing in Step 8. Each scenario must be traceable to at least one driver.

---

### Step 5 — Build 6×3 STEEEP Matrix

Populate all 18 cells. Each cell value = average final_score of all signals mapped to that STEEEP × Temporal combination. Empty cells = 0.

|  | Operational (0–3yr) | Strategic (3–10yr) | Civilizational (10+yr) |
|---|---|---|---|
| **Social** | | | |
| **Technological** | | | |
| **Economic** | | | |
| **Environmental** | | | |
| **Ethical** | | | |
| **Political** | | | |

Apply regional multipliers to each cell. Then identify:
- **Hot zones:** cells with score > 0.50
- **Gap zones:** cells with score = 0.00
- **Dominant zone:** single highest-scoring cell

---

### Step 6 — Cross-Impact Analysis

Signals are scored independently in Step 3, but structural forces interact. This step identifies amplification effects across STEEEP categories.

**Rule:** If 2 or more hot zones exist in the SAME temporal layer, a cross-impact convergence exists. Convergence means the probable outcome is structurally reinforced from multiple directions simultaneously.

For each temporal layer (Operational / Strategic / Civilizational):
1. Count hot zones (score > 0.50)
2. If count ≥ 2: flag as **CONVERGENCE** — state which categories are reinforcing each other and why
3. If count = 1: flag as **ISOLATED** — single-category signal, more fragile
4. If count = 0: flag as **BLIND LAYER** — no strong evidence in this time horizon

Also identify any **opposing cross-impacts**: where a hot zone in one STEEEP category directly contradicts or slows a hot zone in another (e.g. Technological/Strategic hot but Political/Strategic opposing). Flag these as **FRICTION POINTS**.

Output:
```
CROSS-IMPACT
Operational:    [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]
Strategic:      [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]
Civilizational: [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]

Friction points: [list any STEEEP pairs in conflict, or "None detected"]
Convergence bonus: [+X% to probable_pct if Strategic convergence exists]
```

Apply convergence bonus: if Strategic layer has CONVERGENCE, add 5% to probable_pct before normalization in Step 7.

---

### Step 7 — Find 3 Historical Analogues

Identify exactly 3 real historical cases that parallel the question's trajectory.

For each:
1. **Name:** Common name of the transition
2. **Similarity (%):** Estimated % structural similarity (0–100)
3. **Tipping event:** Single event or policy that caused acceleration
4. **Equivalent today:** YES / NO / PARTIAL
5. **Which driver it validates:** Match to D1, D2, or D3 from Step 4

Prefer analogues with similarity ≥ 60%. If none exceed 60%, note as a confidence penalty.

---

### Step 8 — Compute Probabilities + Confidence

#### Predictions — Independent Confidence Scores

Each future type is scored independently (0–100). They do NOT sum to 100%.
Futures cone methodology: a scenario can be 80% Probable AND 60% Plausible simultaneously.

```
R_probable  = (supporting signals with score > 0.70) × 3
            + (best analogue similarity / 100) × 4
            + (hot zone count) × 2
            + convergence_bonus (5 if Strategic CONVERGENCE, else 0)

R_plausible = (supporting signals with score 0.40–0.70) × 2
            + (second analogue similarity / 100) × 3

R_possible  = (wildcard signals) × 2
            + (opposing signals with score > 0.60) × 2
            + (gap zones / 18) × 3
```

Convert to independent scores (exponential curve, not normalization):
```
probable_score  = min(100, round((1 - e^(-R_probable  / 18)) × 100))
plausible_score = min(100, round((1 - e^(-R_plausible / 9))  × 100))
possible_score  = min(100, round((1 - e^(-R_possible  / 5))  × 100))
```

#### Confidence

```
signal_count_score = min(100, total_signals / 25 × 100) × 0.30
signal_diversity   = (unique STEEEP categories covered / 6 × 100) × 0.30
recency_score      = (signals with recency_days ≤ 90 / total) × 100 × 0.20
evidence_score     = (signals with has_evidence=true / total) × 100 × 0.20

confidence = round(signal_count_score + signal_diversity + recency_score + evidence_score)
```

---

### Step 9 — Write Scenarios + Assemble Report

#### Scenario Rules

**PROBABLE, PLAUSIBLE, POSSIBLE** — each must:
- Be traceable to at least one structural driver (cite D1/D2/D3)
- Have no narrative overlap with the others
- Include PROOF with a number or date
- Write IF and BUT in one sentence each — no hedging ("might", "could")

**PREFERABLE — IFTF Backcasting Structure**

Do not write PREFERABLE as a probability-weighted outcome. Write it as a designed future, then backcast to today.

Format:
```
■ PREFERABLE — [Short title]
[2–3 sentences: describe the desired state as already achieved]

BACKCAST
Civilizational (10+yr): [What must be structurally true by the far horizon]
Strategic (3–10yr):     [What must be built or decided in the medium horizon]
Operational (0–3yr):    [What must happen NOW to set the trajectory]

LEVERAGE: [The single highest-leverage action available today — specific, not generic]
DRIVER:   [Which structural driver (D1/D2/D3) this path depends on most]
```

#### Decision Guidance (deterministic logic)

```
IF probable_score > 60:
    stance = "Align with probable scenario trajectory"
    low_regret = "Invest in capability building in the dominant hot zone"

ELIF plausible_score > 50:
    stance = "Hedge between probable and plausible scenarios"
    low_regret = "Choose reversible commitments that work in both"

ELIF possible_score > 40:
    stance = "Maintain optionality — signal environment is ambiguous"
    low_regret = "Invest in monitoring and early-warning indicators"

ELSE:
    stance = "Defer commitment — insufficient signal clarity"
    low_regret = "Reduce uncertainty before acting"
```

Confidence qualifier:
- ≥ 70: prefix "High conviction —"
- < 40: prefix "Low conviction —" and add "Expand signal collection before acting"

Risk trigger: the opposing signal with the highest final_score.

#### Canonical Output Template

**MANDATORY: Output ALL sections below, every single run, no exceptions. Never skip a section. Never produce a partial report.**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOFT PREDICT FUTURE  ·  FORESIGHT ENGINE
[Query]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PREDICTIONS
■ Probable  [[X]/100] [████████████░░░░░░░░] — [one sentence, no hedging]
■ Plausible [[X]/100] [████████░░░░░░░░░░░░] — [one sentence, no hedging]
■ Possible  [[X]/100] [████░░░░░░░░░░░░░░░░] — [one sentence, no hedging]
■ Preferable          [stakeholder analysis below]

Confidence: [X]/100  |  Signals: [N]  |  Horizon: [YYYY–YYYY]  |  [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
— How many pieces of real-world evidence support, oppose, or complicate this question
Supporting [N] [████████████░░░░░░░░]  Opposing [N] [████░░░░░░░░░░░░░░░░]  Wild [N]
Net: [SUPPORTING LEADS / OPPOSING LEADS / NEUTRAL]
Hot zone: [The single STEEEP category with strongest evidence]
Gap: [STEEEP categories with no signals, or "None — full coverage"]

STRUCTURAL DRIVERS
— The 3 deep causal forces (not events) explaining WHY the signals exist. Stability = likelihood of change.
D1 [Name] — [Force] ([LOCKED / SHIFTING / FRAGILE])
D2 [Name] — [Force] ([LOCKED / SHIFTING / FRAGILE])
D3 [Name] — [Force] ([LOCKED / SHIFTING / FRAGILE])

CROSS-IMPACT
— Whether multiple STEEEP domains reinforce or contradict each other in the same time layer
Operational:    [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]
Strategic:      [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]
Civilizational: [CONVERGENCE / ISOLATED / BLIND LAYER] — [explanation]
Friction:       [Conflicting domain pairs, or "None detected"]

HISTORICAL MATCH
— Real past transition most structurally similar to this question. Higher % = stronger precedent.
[Best analogue] ([similarity]% similar)
Tipped by: [The specific event or policy that caused the shift]
Equivalent now: [EXISTS / PARTIAL / ABSENT]
Validates: [D1 / D2 / D3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ PROBABLE [[X]%] — [Title]
— The most evidence-backed outcome given current signal strength
[2–3 sentence narrative. No hedging.]
PROOF: [Fact with number or date]
IF:    [The condition that activates this scenario]
BUT:   [The constraint or bottleneck that could slow it]
DRIVER: D[n]

■ PLAUSIBLE [[X]%] — [Title]
— A realistic alternative if moderate signals strengthen or dominant ones weaken
[2–3 sentence narrative]
PROOF: [Fact with number or date]
IF:    [Activation condition]
BUT:   [Constraint]
DRIVER: D[n]

■ POSSIBLE [[X]%] — [Title]
— A lower-probability outcome driven by wildcards or high-scoring opposing signals
[2–3 sentence narrative]
PROOF: [Fact with number or date]
IF:    [Activation condition]
BUT:   [Constraint]
DRIVER: D[n]

■ PREFERABLE — [Title]
— Not a prediction. A designed future: what the best achievable outcome looks like, traced back to today.
[2–3 sentences: desired state as already achieved. No hedging.]
BACKCAST
  Civilizational: [What must be structurally true by the far horizon]
  Strategic:      [What must be built or decided in the medium term]
  Operational:    [What must begin NOW to set the trajectory]
LEVERAGE: [Single highest-leverage action today — specific actor, specific action]
DRIVER: D[n]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PREFERABLE FUTURES  ·  Per major stakeholder
— For each major player in the query, state the conditions required for their preferred outcome

[Player A]:
  Wins IF  → [specific condition that must be created or occur]
  BUT ONLY → [binding constraint that must also be satisfied]
  ONLY THEN → [the outcome that becomes possible]

[Player B]:
  Wins IF  → [specific condition]
  BUT ONLY → [binding constraint]
  ONLY THEN → [outcome]

[Users/Society — always include]:
  Wins IF  → [condition for best collective outcome]
  BUT ONLY → [constraint]
  ONLY THEN → [outcome]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ONE THING
— The single variable whose presence or absence determines which scenario actually unfolds
[One sentence naming the deciding variable]
INCIDENT: [Real past event showing this variable's power]
WATCH:    [Leading indicator — a milestone, metric, or policy action to monitor]
IF YES → [What accelerates]
IF NO  → [What stalls]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION GUIDANCE
Recommended stance: [From deterministic probability logic]
Low-regret move:    [Action that pays off in multiple scenarios simultaneously]
Risk trigger:       [Highest-scored opposing signal — the one that could invalidate Probable]

[REGIONAL LENS — [REGION]]
Top multipliers: [STEEEP/temporal (Xx)]  [STEEEP/temporal (Xx)]
Key local variable: [One sentence on the dominant local structural factor]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHODOLOGY KEY
Signal score (0–1)     Recency × source reliability × signal type × evidence strength — higher = fresher, better-sourced, stronger evidence
Confidence (0–100)     Signal density (0–40) + evidence balance (0–30) + historical grounding (0–30) − blind spot penalty (0–15)
Predictions            PROBABLE / PLAUSIBLE / POSSIBLE are independent scores (0–100 each, do NOT sum to 100)
                       Futures cone: a scenario can score high on multiple types simultaneously
STEEEP matrix          6 domains × 3 time horizons — ★ hot (>1.0) ● warm (>0.5) ✗ blind spot (0)
Historical similarity   Structural pattern match to real past transitions — 60%+ is reliable precedent; below 40% is weak grounding
Convergence bonus      +5 added to Probable score when 2+ STEEEP domains reinforce each other in the Strategic layer
Stability tiers        LOCKED = unlikely to change in 10yr | SHIFTING = could change in 3–5yr | FRAGILE = could reverse in 1–2yr
Preferable futures     Per stakeholder: Wins IF [condition] BUT ONLY [constraint] ONLY THEN [outcome]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

## Visual Output (claude.ai with Artifacts)

If running on claude.ai and Artifacts are enabled, after the text report generate an HTML Artifact:

```html
<!-- Render a visual foresight report with:
  1. Predictions bar chart — horizontal bars for Probable/Plausible/Possible scores
  2. STEEEP matrix — 6×3 color-coded table (darker green = hotter cell, red = blind spot)
  3. Futures cone — SVG diagram showing 4 scenario bands expanding from present to horizon
  4. Stakeholder preferable cards — one card per player with Wins IF / BUT ONLY / ONLY THEN
  Use inline CSS only. No external dependencies. Dark background (#0f0f0f), accent color #00d4aa.
-->
```

---

## Regional Multiplier Tables

Apply in Step 3 and Step 5.

### India
| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.10 | 1.30 | 1.20 |
| **Technological** | 1.40 | 1.30 | 1.10 |
| **Economic** | 1.20 | 1.25 | 1.15 |
| **Environmental** | 0.90 | 1.00 | 1.10 |
| **Ethical** | 0.95 | 1.00 | 1.05 |
| **Political** | 0.85 | 0.90 | 1.00 |

**India note:** UPI/DPI gives asymmetric advantage in Technological/Operational. Political/Operational discounted by regulatory fragmentation across states.

### USA
| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.10 | 1.05 |
| **Technological** | 1.20 | 1.40 | 1.20 |
| **Economic** | 1.10 | 1.30 | 1.10 |
| **Environmental** | 0.95 | 1.00 | 1.05 |
| **Ethical** | 1.05 | 1.10 | 1.10 |
| **Political** | 0.90 | 0.95 | 1.00 |

**USA note:** Deep capital markets amplify Technological/Strategic. Political/Operational discounted by legislative gridlock.

### Europe
| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.05 | 1.10 |
| **Technological** | 1.00 | 1.10 | 1.05 |
| **Economic** | 0.95 | 0.90 | 0.90 |
| **Environmental** | 1.20 | 1.40 | 1.30 |
| **Ethical** | 1.10 | 1.20 | 1.20 |
| **Political** | 1.05 | 1.10 | 1.10 |

**Europe note:** Regulatory leadership (GDPR, EU AI Act, Green Deal) amplifies Environmental/Strategic. Economic/Civilizational discounted by demographic headwinds.

### China
| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.10 | 1.05 |
| **Technological** | 1.20 | 1.50 | 1.30 |
| **Economic** | 1.10 | 1.20 | 1.10 |
| **Environmental** | 0.90 | 1.00 | 1.05 |
| **Ethical** | 0.70 | 0.75 | 0.80 |
| **Political** | 1.10 | 1.15 | 1.00 |

**China note:** State-directed capital amplifies Technological/Strategic strongly. Ethical/Operational discounted by limited transparency.

### Global (default)
All multipliers = 1.0. Apply when no region is detectable.
