---
name: red-blue-validator
version: "2.0"
description: >
  Iterative adversarial stress-testing through Red/Blue team dynamics. Red Team
  generates substantive, steel-manned attacks against propositions; Blue Team
  responds with defenses, mitigations, and hardening. Cycles continue until
  convergence criteria are met, producing a battle-tested proposition.

  PROACTIVELY activate for: (1) High-stakes decisions requiring stress-testing,
  (2) Strategy validation before major commitment, (3) Architecture decision
  hardening, (4) Proposal defense preparation, (5) Security posture review,
  (6) Investment due diligence with adversarial lens.

  Triggers: "red team this", "blue team", "stress test", "attack this plan",
  "find weaknesses", "adversarial review", "devil's advocate", "what could go wrong",
  "poke holes in this", "challenge this decision", "war game this"
---

# Red/Blue Team Validator

> "Find weaknesses before reality does."

Every proposition—whether a decision, strategy, architecture, or plan—has vulnerabilities. This skill systematically exposes them through iterative adversarial cycles. Red Team attacks with substantive, steel-manned challenges. Blue Team defends with mitigations and hardening. The cycle continues until convergence: a battle-tested proposition with documented defenses.

---

## 1. Purpose

### Core Value Proposition

Static analysis misses what adversarial pressure reveals. Red/Blue validation simulates the attacks your proposition will face—from competitors, critics, reality itself—and forces you to build defenses before you need them. The output is not just a risk list, but a hardened proposition that has survived systematic assault.

### Capabilities

| # | Capability | Phase | Value |
|---|-----------|-------|-------|
| 1 | Proposition intake with attack surface mapping | Pre-Round | Define what can be attacked |
| 2 | Experience pool loading (domain failure patterns) | Pre-Round | Avoid reinventing known failures |
| 3 | Multi-category attack generation | Round N: Red | Surface vulnerabilities systematically |
| 4 | Steel-manning attacks to maximum strength | Round N: Red | Ensure attacks are not strawmen |
| 5 | Severity scoring (CRITICAL/HIGH/MEDIUM/LOW) | Round N: Red | Prioritize responses |
| 6 | Defense generation (REFUTE/MITIGATE/ACCEPT/HARDEN) | Round N: Blue | Address each attack |
| 7 | Proposition hardening through iterative refinement | Round N: Blue | Strengthen against attacks |
| 8 | Convergence evaluation with explicit criteria | Round N: Eval | Know when to stop |
| 9 | RISK-ASSESSMENT synthesis (CONTRACT-08) | Post-Round | Standardized output |
| 10 | Hardened proposition generation | Post-Round | Battle-tested version |
| 11 | Attack/defense log compilation | Post-Round | Audit trail |
| 12 | Go/no-go recommendation | Post-Round | Decision support |

---

## 2. When to Use

### Ideal Use Cases

| Scenario | Why Red/Blue Validation Matters |
|----------|--------------------------------|
| **Pre-commitment decision review** | Simulate objections before committing resources |
| **Strategy validation** | War-game competitive responses and market realities |
| **Architecture decision hardening** | Stress-test technical choices before implementation |
| **Proposal defense preparation** | Anticipate and prepare for stakeholder pushback |
| **Investment due diligence** | Adversarial review of financial projections and market assumptions |
| **Security posture assessment** | Systematic attack surface enumeration |
| **Go/no-go decisions** | High-stakes decisions need adversarial pressure |
| **Policy/process validation** | Find edge cases and failure modes |
| **Product launch readiness** | Anticipate market, competitive, and operational challenges |
| **M&A target evaluation** | Adversarial review of synergy claims |

### Anti-Patterns (When NOT to Use)

| Anti-Pattern | Why It's Ineffective | Better Alternative |
|--------------|----------------------|-------------------|
| **Low-stakes decisions** | Over-engineering for trivial choices | Just decide and iterate |
| **Time-critical emergencies** | Fires need extinguishing, not philosophy | Act, then debrief |
| **Already committed** | Adversarial review after commitment creates conflict | Use for future decisions |
| **Early exploration** | Premature to attack ideas still forming | Use after initial validation |
| **Confirmation theater** | Going through motions without genuine adversarial intent | Either commit to true adversarial thinking or skip |
| **Reversible decisions** | Two-way doors don't need siege testing | Save intensity for one-way doors |

---

## 3. Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `subject_type` | enum | **yes** | — | decision \| strategy \| architecture \| plan \| policy \| investment \| security |
| `max_rounds` | integer | no | 3 | Maximum red/blue cycles (1-5) |
| `attack_intensity` | enum | no | standard | light \| standard \| aggressive |
| `attack_categories` | list | no | auto | Categories to probe (see catalog); auto selects by subject_type |
| `convergence_mode` | enum | no | no_new_critical | no_new_critical \| all_addressed \| round_limit |
| `include_experience_pool` | boolean | no | true | Load domain-specific failure patterns |
| `steel_manning_level` | enum | no | standard | minimal \| standard \| maximum |
| `output_mode` | enum | no | full | risk_assessment \| hardened_proposition \| full_log |

### Parameter Effects Matrix

| Parameter | Red Phase Effect | Blue Phase Effect | Convergence Effect |
|-----------|-----------------|------------------|-------------------|
| `attack_intensity: light` | Top 3 attack categories | Quick defenses | max_rounds capped at 2 |
| `attack_intensity: standard` | Top 5 attack categories | Full defense protocol | Normal convergence |
| `attack_intensity: aggressive` | All applicable categories | Exhaustive defense | Requires no_new_critical |
| `steel_manning_level: minimal` | 1-pass attacks | — | Faster rounds |
| `steel_manning_level: standard` | 2-pass steel-manning | — | Normal rounds |
| `steel_manning_level: maximum` | 3-pass with ideological Turing test | — | Thorough rounds |
| `convergence_mode: no_new_critical` | — | — | Stop when 0 new CRITICAL/HIGH |
| `convergence_mode: all_addressed` | — | Must address all | Stop when no ACCEPT responses |
| `convergence_mode: round_limit` | — | — | Stop at max_rounds |

### Auto-Selected Attack Categories by Subject Type

| Subject Type | Default Attack Categories |
|--------------|--------------------------|
| `decision` | ASSUMPTIONS, ALTERNATIVES, REVERSIBILITY, CONSEQUENCES, TIMING |
| `strategy` | COMPETITIVE, MARKET, EXECUTION, DEPENDENCIES, TIMELINE |
| `architecture` | SCALABILITY, SECURITY, DEPENDENCIES, OPERATIONAL, EDGE_CASES |
| `plan` | FEASIBILITY, RESOURCES, TIMELINE, DEPENDENCIES, RISKS |
| `policy` | EDGE_CASES, ENFORCEMENT, UNINTENDED_CONSEQUENCES, POLITICAL |
| `investment` | ECONOMIC, MARKET, EXECUTION, COMPETITIVE, ASSUMPTIONS |
| `security` | ATTACK_SURFACE, VULNERABILITIES, DEPENDENCIES, OPERATIONAL |

---

## 4. Checkpoints

This skill uses interactive checkpoints (see `references/checkpoints.yaml`) to resolve ambiguity:
- **subject_type_classification** — When proposition type is ambiguous
- **attack_intensity_selection** — When attack intensity not specified
- **convergence_mode_selection** — When convergence criteria not specified
- **premature_convergence_check** — When convergence met but warning signs present
- **infinite_loop_risk** — When defenses generate more attacks than they resolve
- **output_mode_selection** — When output format not specified

---

## 5. Iterative Workflow

### Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RED/BLUE TEAM VALIDATOR                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ╔══════════════════════════════════════════════════════════════════════╗   │
│  ║                      PRE-ROUND SETUP                                  ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   ║   │
│  ║  │ Proposition │  │   Attack    │  │ Experience  │                   ║   │
│  ║  │   Intake    │─▶│  Surface    │─▶│    Pool     │                   ║   │
│  ║  │             │  │  Mapping    │  │   Loading   │                   ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘                   ║   │
│  ╚══════════════════════════════════════════════════════════════════════╝   │
│                                  │                                           │
│                                  ▼                                           │
│  ╔══════════════════════════════════════════════════════════════════════╗   │
│  ║                         ROUND N                                       ║   │
│  ║  ┌─────────────┐                    ┌─────────────┐                  ║   │
│  ║  │  RED TEAM   │                    │  BLUE TEAM  │                  ║   │
│  ║  │   ATTACK    │───── Attacks ─────▶│   DEFENSE   │                  ║   │
│  ║  │ (Generate & │                    │ (Respond &  │                  ║   │
│  ║  │ Steel-man)  │                    │  Harden)    │                  ║   │
│  ║  └─────────────┘                    └─────────────┘                  ║   │
│  ║         │                                  │                          ║   │
│  ║         └────────────┬─────────────────────┘                          ║   │
│  ║                      ▼                                                ║   │
│  ║              ┌─────────────┐                                          ║   │
│  ║              │ EVALUATION  │                                          ║   │
│  ║              │ & Converge? │                                          ║   │
│  ║              └─────────────┘                                          ║   │
│  ║                      │                                                ║   │
│  ║           ┌──────────┴──────────┐                                     ║   │
│  ║           ▼                     ▼                                     ║   │
│  ║    [NOT CONVERGED]        [CONVERGED]                                 ║   │
│  ║    → Round N+1            → Exit loop                                 ║   │
│  ╚══════════════════════════════════════════════════════════════════════╝   │
│                                  │                                           │
│                                  ▼                                           │
│  ╔══════════════════════════════════════════════════════════════════════╗   │
│  ║                     POST-ROUND SYNTHESIS                              ║   │
│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   ║   │
│  ║  │    RISK     │  │  Hardened   │  │  Attack/    │                   ║   │
│  ║  │ ASSESSMENT  │  │Proposition  │  │ Defense Log │                   ║   │
│  ║  │(CONTRACT-08)│  │  Output     │  │             │                   ║   │
│  ║  └─────────────┘  └─────────────┘  └─────────────┘                   ║   │
│  ╚══════════════════════════════════════════════════════════════════════╝   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Pre-Round Setup

**Purpose:** Prepare the battlefield—understand what's being tested and load relevant knowledge.

**Steps:**

1. **Proposition Intake**
   - Receive subject (decision, strategy, architecture, plan, etc.)
   - If verbal, request written summary or create one together
   - Extract key claims and assertions to be defended
   - Identify stakeholders and constraints
   - Note: Proposition should be specific enough to attack

2. **Attack Surface Mapping**
   - Identify dimensions available for attack (from attack-vector-catalog)
   - Map proposition claims to attackable surfaces
   - Select attack categories based on `subject_type` or explicit `attack_categories`
   - **See:** `references/attack-vector-catalog.md` for categories

3. **Experience Pool Loading** (if `include_experience_pool: true`)
   - Load domain-specific failure patterns
   - Reference historical failures in similar contexts
   - Prepare anti-patterns to probe
   - **See:** `references/experience-pool-patterns.md` for patterns

4. **Set Parameters**
   - Confirm attack intensity, convergence mode, steel-manning level
   - Estimate expected rounds based on complexity

   **CHECKPOINT: subject_type_classification**
   - If subject_type not specified or ambiguous: **AskUserQuestion**
   - Present subject type options with attack category implications

   **CHECKPOINT: attack_intensity_selection**
   - If attack_intensity not specified: **AskUserQuestion**
   - Present intensity options with effort implications

   **CHECKPOINT: convergence_mode_selection**
   - If convergence_mode not specified: **AskUserQuestion**
   - Present convergence options with trade-offs

**Quality Gate:** Attack Surface Mapped
- [ ] Proposition boundaries explicitly defined
- [ ] Attack categories selected (minimum 3)
- [ ] Experience pool loaded (if enabled)
- [ ] Parameters confirmed

**Output:** Attack-ready proposition with mapped attack surface

---

### Round N: Red Team Phase

**Purpose:** Generate substantive, steel-manned attacks on the proposition.

**Reference:** See `references/red-team-techniques.md` and `references/steel-manning-protocol.md`.

**Steps:**

1. **Attack Generation**

   For each attack category in scope, generate attacks:

   | Technique | When to Use | Expected Yield |
   |-----------|-------------|----------------|
   | **Pre-mortem** | Always | 3-5 attacks |
   | **Inversion** | Strategy, Decision | 2-4 attacks |
   | **Competitor Simulation** | Strategy, Investment | 2-3 attacks |
   | **Stress Test Amplification** | Architecture, Plan | 2-4 attacks |
   | **Devil's Advocate** | Policy, Decision | 2-3 attacks |
   | **Blind Spot Hunter** | All | 1-3 attacks |
   | **Historical Pattern Matching** | All (with experience pool) | 2-4 attacks |
   | **Black Hat Thinking** | Security, Competitive | 3-5 attacks |

   - **See:** `references/red-team-techniques.md` for protocols

2. **Steel-Manning** (per `steel_manning_level`)

   For each attack, strengthen to maximum potency:

   | Level | Passes | Protocol |
   |-------|--------|----------|
   | **minimal** | 1 | Basic attack formulation |
   | **standard** | 2 | + "How can this be more damaging?" |
   | **maximum** | 3 | + Ideological Turing test: "Would a true opponent accept this?" |

   **Steel-manning checklist:**
   - [ ] Attack is specific, not vague
   - [ ] Attack has clear mechanism of harm
   - [ ] Attack includes realistic trigger conditions
   - [ ] Attack would concern a reasonable proponent
   - [ ] Attack is not easily dismissed

   - **See:** `references/steel-manning-protocol.md` for full protocol

3. **Severity Scoring**

   Score each attack using SEVERITY-SCORING (RUBRIC-07):

   | Severity | Definition | Response Urgency |
   |----------|------------|------------------|
   | **CRITICAL** | Blocks primary objective; cannot proceed | Must address in Blue Phase |
   | **HIGH** | Significant impact; major rework required | Should address in Blue Phase |
   | **MEDIUM** | Degrades quality; should fix but can proceed | Address if time permits |
   | **LOW** | Minor issue; cosmetic | Document and monitor |

   Scoring dimensions:
   - **Impact** (0.5 weight): How damaging if attack succeeds?
   - **Likelihood** (0.3 weight): How likely is this attack vector?
   - **Detectability** (0.2 weight): How hard to see this coming?

4. **Attack Documentation**

   For each attack:
   ```
   Attack ID: ATK-[round]-[number]
   Category: [From attack-vector-catalog]
   Target: [What aspect of proposition]
   Statement: [Clear attack formulation]
   Mechanism: [How this would cause harm]
   Severity: [CRITICAL | HIGH | MEDIUM | LOW]
   Steel-manning: [minimal | standard | maximum] - [notes]
   Experience pool match: [Pattern ID if applicable]
   ```

**Quality Gate:** Attacks Substantive
- [ ] Minimum 3 attacks generated
- [ ] At least 2 different attack categories represented
- [ ] Steel-manning applied per level
- [ ] No trivial or easily dismissed attacks
- [ ] Severities assigned with rationale

**Output:** Prioritized attack list for Blue Team

---

### Round N: Blue Team Phase

**Purpose:** Respond to each attack with defenses, mitigations, or proposition hardening.

**Reference:** See `references/blue-team-techniques.md` for defense protocols.

**Steps:**

1. **Attack Triage**

   Prioritize attacks by severity:
   - CRITICAL: Must address this round
   - HIGH: Should address this round
   - MEDIUM: Address if time/capacity permits
   - LOW: Document for monitoring

2. **Defense Generation**

   For each attack, determine response type:

   | Response Type | When to Use | Effect |
   |---------------|-------------|--------|
   | **REFUTE** | Attack is invalid; evidence proves it wrong | Attack dismissed |
   | **MITIGATE** | Attack is valid; add safeguards | Risk reduced |
   | **ACCEPT** | Attack is valid; insufficient mitigation possible | Residual risk documented |
   | **HARDEN** | Modify proposition to eliminate vulnerability | Proposition strengthened |

   Defense techniques:

   | Technique | Response Type | When to Use |
   |-----------|--------------|-------------|
   | **Evidence-Based Refutation** | REFUTE | When data contradicts attack |
   | **Mitigation Design** | MITIGATE | When attack is valid but manageable |
   | **Contingency Planning** | MITIGATE | When fallback is needed |
   | **Monitoring/Detection** | MITIGATE | When early warning helps |
   | **Hardening Protocol** | HARDEN | When proposition can be strengthened |
   | **Risk Transfer** | MITIGATE | When others can absorb risk |
   | **Staged Commitment** | MITIGATE | When phasing reduces exposure |
   | **Kill Switch Design** | MITIGATE | When reversibility is critical |

   - **See:** `references/blue-team-techniques.md` for detailed protocols

3. **Defense Documentation**

   For each defense:
   ```
   Defense ID: DEF-[round]-[number]
   Attack Addressed: ATK-[round]-[number]
   Response Type: [REFUTE | MITIGATE | ACCEPT | HARDEN]
   Defense: [Specific response]
   Evidence/Rationale: [Why this defense works]
   Residual Risk: [ELIMINATED | REDUCED | UNCHANGED]
   Proposition Change: [If HARDEN, what changed]
   ```

4. **Proposition Hardening**

   Apply all HARDEN responses to proposition:
   - Document each modification
   - Track changes between rounds
   - Maintain hardened proposition version

5. **Defense Quality Check**

   For each defense, verify:
   - [ ] Defense actually addresses the attack (not adjacent issue)
   - [ ] REFUTE claims have supporting evidence
   - [ ] MITIGATE responses are actionable
   - [ ] ACCEPT responses have residual risk documented
   - [ ] HARDEN changes don't introduce new vulnerabilities

**Quality Gate:** Attacks Addressed
- [ ] Every attack has a defense response
- [ ] CRITICAL attacks have REFUTE or MITIGATE (not ACCEPT)
- [ ] HIGH attacks have REFUTE, MITIGATE, or documented ACCEPT with rationale
- [ ] Hardening changes documented
- [ ] No hand-waving defenses

**Output:** Defense log with updated (hardened) proposition

---

### Round N: Evaluation Phase

**Purpose:** Determine if another round is needed or convergence achieved.

**Reference:** See `references/convergence-criteria.md` for detailed criteria.

**Steps:**

1. **Assess Round Quality**

   Red Team assessment:
   - Were attacks substantive or rehashes of previous rounds?
   - Are there novel attack angles remaining?
   - Is Red Team finding diminishing returns?

   Blue Team assessment:
   - Were defenses genuine or hand-waving?
   - Are mitigations actionable?
   - Has proposition been strengthened?

2. **Apply Convergence Criteria**

   | Mode | Stop When | Continue When |
   |------|-----------|---------------|
   | `no_new_critical` | Round produced 0 new CRITICAL or HIGH attacks | New CRITICAL or HIGH attacks found |
   | `all_addressed` | No ACCEPT responses remain (all REFUTE/MITIGATE/HARDEN) | Any ACCEPT responses remain |
   | `round_limit` | `max_rounds` reached | Below `max_rounds` |

   **Override conditions** (continue despite convergence):
   - Obvious attack categories not yet explored
   - Blue Team defenses appear inadequate
   - Stakeholder requests additional scrutiny

   **Premature termination signs** (don't stop too early):
   - Less than 2 rounds completed
   - CRITICAL attacks still have ACCEPT responses
   - Key attack categories unexplored

3. **Document Convergence Decision**

   ```
   Round [N] Evaluation:
   - New CRITICAL attacks: [count]
   - New HIGH attacks: [count]
   - ACCEPT responses remaining: [count]
   - Convergence mode: [mode]
   - Decision: [CONTINUE | CONVERGED]
   - Rationale: [explanation]
   ```

4. **Proceed or Exit**

   - If NOT CONVERGED: Increment round, return to Red Phase
   - If CONVERGED: Proceed to Post-Round Synthesis

   **CHECKPOINT: premature_convergence_check**
   - If convergence met but warning signs present: **AskUserQuestion**
   - Warning signs: <2 rounds, CRITICAL ACCEPTs remain, key categories unexplored

   **CHECKPOINT: infinite_loop_risk**
   - If new attacks from defenses exceed previous round: **AskUserQuestion**
   - May indicate fundamental proposition issues

**Quality Gate:** Convergence Evaluated
- [ ] Explicit continue/stop decision documented
- [ ] Rationale provided
- [ ] Override conditions checked
- [ ] Premature termination signs checked

**Output:** Convergence decision with rationale

---

### Post-Round Synthesis

**Purpose:** Compile findings into actionable outputs.

**Reference:** See `templates/` for output formats.

**CHECKPOINT: output_mode_selection**
- If output_mode not specified: **AskUserQuestion**
- Options: risk_assessment, hardened_proposition, full_log

**Steps:**

1. **Compile Attack/Defense Log**

   Consolidate all rounds:
   - All attacks with responses
   - Round-by-round progression
   - Convergence trajectory
   - **See:** `templates/attack-defense-log.md`

2. **Derive RISK-ASSESSMENT (CONTRACT-08)**

   Transform unresolved attacks into risks:

   | Attack Status | Risk Derivation |
   |---------------|-----------------|
   | ACCEPT response | Direct risk: attack remains valid |
   | MITIGATE with residual | Risk: partially addressed |
   | MITIGATE with ELIMINATED | No risk (resolved) |
   | REFUTE | No risk (invalid attack) |
   | HARDEN | No risk (vulnerability removed) |

   Score each derived risk using SEVERITY-SCORING:
   - Include mitigations from Blue Team responses
   - **See:** `templates/risk-assessment-output.md`

3. **Generate Hardened Proposition**

   Compile final version:
   - Original proposition + all HARDEN modifications
   - List of accepted residual risks
   - Battle-tested confidence score
   - Conditions for validity
   - Review triggers
   - **See:** `templates/hardened-proposition-output.md`

4. **Calculate Battle-Tested Confidence**

   Score based on:
   - Rounds completed (more = higher confidence)
   - Attack quality (substantive attacks survived)
   - Defense quality (genuine defenses, not hand-waving)
   - Residual risk profile (fewer ACCEPT = higher confidence)

   | Score | Meaning |
   |-------|---------|
   | 80-100 | High confidence: withstood aggressive scrutiny |
   | 60-79 | Moderate confidence: key challenges addressed |
   | 40-59 | Low confidence: significant risks remain |
   | 0-39 | Very low confidence: fundamental issues unresolved |

5. **Generate Go/No-Go Recommendation**

   | Recommendation | When |
   |----------------|------|
   | **PROCEED** | Low/very low residual risk; proposition battle-tested |
   | **PROCEED_WITH_CAUTION** | Moderate risk; mitigations in place |
   | **SIGNIFICANT_CONCERNS** | High risk; key attacks unresolved |
   | **DO_NOT_PROCEED** | Very high risk; fundamental flaws exposed |

**Quality Gates:**
- [ ] RISK-ASSESSMENT complete with go/no-go
- [ ] All attacks traced to risks or resolutions
- [ ] Hardened proposition documented
- [ ] Battle-tested confidence calculated
- [ ] Attack/defense log compiled

**Output:** RISK-ASSESSMENT (CONTRACT-08), Hardened Proposition, Attack/Defense Log

---

## 5. Attack Vector Catalog

Ten categories of attacks, applicable across subject types:

### 5.1 ASSUMPTIONS

**Definition:** Attacks targeting hidden, unstated, or fragile assumptions.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Hidden assumption exposure** | Unstated beliefs | "You're assuming customers want this feature" |
| **Load-bearing challenge** | Critical assumptions | "If this assumption fails, the whole plan collapses" |
| **Temporal decay** | Time-sensitive assumptions | "This assumption won't hold in 2 years" |
| **Behavioral assumptions** | Human behavior predictions | "You're assuming the team will change behavior" |
| **Counterfactual reversal** | Any assumption | "What if the opposite is true?" |

**Risk Level:** HIGH (often invisible until failure)

### 5.2 DEPENDENCIES

**Definition:** Attacks targeting external or internal dependencies.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **External dependency failure** | Third parties | "What if the vendor goes out of business?" |
| **Technology obsolescence** | Tech dependencies | "This framework may not be maintained in 3 years" |
| **Team capability dependency** | People | "This requires skills the team doesn't have" |
| **Resource availability** | Resources | "What if the budget is cut 30%?" |
| **Single point of failure** | Critical dependencies | "Everything depends on this one system" |

**Risk Level:** HIGH (external factors often uncontrollable)

### 5.3 EDGE_CASES

**Definition:** Attacks targeting boundary conditions and unusual scenarios.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Boundary conditions** | Limits | "What happens at 0? At max capacity?" |
| **Scale extremes** | Very large/small | "Does this work with 1 user? 1 million?" |
| **Timing edge cases** | Timing | "What if these events happen simultaneously?" |
| **Data quality** | Inputs | "What if the input data is garbage?" |
| **Concurrency/race conditions** | Parallel operations | "What if two users do this at the same time?" |

**Risk Level:** MEDIUM (often discoverable through testing)

### 5.4 SCALABILITY

**Definition:** Attacks targeting ability to grow or shrink.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Horizontal scaling limits** | Adding instances | "Can you just add more servers?" |
| **Vertical scaling limits** | Bigger instances | "What if you need 10x the memory?" |
| **Cost scaling non-linearity** | Economics | "Costs grow O(n²) with users" |
| **Operational complexity** | Team capacity | "Can the team manage 50 services?" |
| **Data volume scaling** | Storage/processing | "What happens with 10TB of data?" |

**Risk Level:** HIGH (often not discovered until growth happens)

### 5.5 SECURITY

**Definition:** Attacks targeting security posture and vulnerabilities.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Attack surface exposure** | Entry points | "Every API is an attack vector" |
| **Data breach scenarios** | Data protection | "What if this database is compromised?" |
| **Authentication gaps** | Identity | "How do you prevent unauthorized access?" |
| **Authorization gaps** | Permissions | "Can users access others' data?" |
| **Compliance violations** | Regulations | "Does this violate GDPR?" |

**Risk Level:** CRITICAL (security failures can be catastrophic)

### 5.6 COMPETITIVE

**Definition:** Attacks targeting competitive dynamics.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Competitor response** | Competitive reaction | "What will [competitor] do when they see this?" |
| **Market timing** | Windows | "The market window may close before launch" |
| **Differentiation erosion** | Uniqueness | "This feature can be copied in weeks" |
| **Pricing pressure** | Economics | "Competitor can undercut by 50%" |
| **Acquisition/partnership disruption** | Strategic moves | "What if competitor acquires your key partner?" |

**Risk Level:** HIGH (competitive dynamics are unpredictable)

### 5.7 OPERATIONAL

**Definition:** Attacks targeting day-to-day operations.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Complexity explosion** | Manageability | "This will be impossible to debug" |
| **Incident scenarios** | Failure recovery | "What's the MTTR when this breaks at 3 AM?" |
| **Recovery time** | Resilience | "Can you recover within SLA?" |
| **Monitoring gaps** | Observability | "How would you even know it's failing?" |
| **On-call burden** | Team health | "This will burn out the team" |

**Risk Level:** MEDIUM-HIGH (operational issues compound)

### 5.8 ECONOMIC

**Definition:** Attacks targeting financial viability.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Unit economics failure** | Per-unit costs | "Each customer costs more than they pay" |
| **Cost structure vulnerability** | Fixed costs | "Break-even requires 10x current volume" |
| **Revenue model fragility** | Income sources | "Revenue depends on one customer segment" |
| **Funding/cash flow** | Capital | "You'll run out of runway in 8 months" |
| **Market size overestimation** | TAM/SAM/SOM | "Your market is 1/10th the claimed size" |

**Risk Level:** HIGH (financial failure is existential)

### 5.9 ORGANIZATIONAL

**Definition:** Attacks targeting people and organization.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Capability gaps** | Skills | "No one on the team has done this before" |
| **Key person dependency** | Individuals | "If [person] leaves, this fails" |
| **Cultural resistance** | Adoption | "The organization will reject this change" |
| **Political opposition** | Stakeholders | "[Executive] will block this" |
| **Change management** | Transition | "Users will refuse to migrate" |

**Risk Level:** MEDIUM-HIGH (organizational dynamics are complex)

### 5.10 TEMPORAL

**Definition:** Attacks targeting timing and duration.

| Attack Pattern | Target | Example |
|---------------|--------|---------|
| **Timeline compression** | Deadlines | "What if the deadline is moved up 3 months?" |
| **Timeline extension impact** | Delays | "What if this takes twice as long?" |
| **Market window closure** | Timing | "The opportunity won't exist in 12 months" |
| **Technology obsolescence** | Tech lifecycle | "This technology will be obsolete" |
| **Regulatory timeline** | External deadlines | "Regulation changes in 6 months" |

**Risk Level:** HIGH (timing failures are often unrecoverable)

---

## 6. Convergence Criteria

### Mode Definitions

| Mode | Definition | Best For |
|------|------------|----------|
| `no_new_critical` | Stop when round produces 0 new CRITICAL or HIGH attacks | Most use cases |
| `all_addressed` | Stop when no ACCEPT responses remain | High-stakes decisions |
| `round_limit` | Stop at `max_rounds` regardless | Time-constrained reviews |

### Measurement Methods

**no_new_critical:**
- Count CRITICAL attacks generated this round: must be 0
- Count HIGH attacks generated this round: must be 0
- Attacks that are variants of previous attacks don't count as "new"

**all_addressed:**
- Count ACCEPT responses across all rounds
- Must be 0 (all attacks have REFUTE, MITIGATE, or HARDEN)

**round_limit:**
- Simply check `current_round >= max_rounds`

### Override Conditions (Continue Despite Convergence)

- Obvious attack categories not yet explored
- Stakeholder requests additional rounds
- Blue Team defenses appear superficial
- Recent hardening changes may introduce new vulnerabilities

### Premature Termination Signs (Don't Stop Too Early)

- Less than 2 rounds completed
- CRITICAL attacks still have ACCEPT responses
- Attack quality improving (not diminishing) each round
- Key experience pool patterns not yet probed

---

## 7. Output Specifications

### 7.1 Primary Output: RISK-ASSESSMENT

Compliant with CONTRACT-08 from `artifact-contracts.yaml`.

**See:** `templates/risk-assessment-output.md` for complete XML template.

Key extensions for adversarial validation:
- `<adversarial_summary>` with attack/defense statistics
- Risks traced to source attacks (ATK-X-Y)
- Battle-tested confidence score
- Defense quality assessment

### 7.2 Secondary Output: Hardened Proposition

**See:** `templates/hardened-proposition-output.md` for complete template.

Includes:
- Original proposition vs. battle-tested version
- All modifications with rationale
- Accepted residual risks
- Conditions for validity
- Review triggers

### 7.3 Secondary Output: Attack/Defense Log

**See:** `templates/attack-defense-log.md` for complete template.

Includes:
- Round-by-round attack and defense tables
- Convergence evaluation per round
- Severity distribution
- Resolution statistics

---

## 8. Quality Gates Summary

| # | Gate | Criterion | Phase |
|---|------|-----------|-------|
| 1 | **Attack Surface Mapped** | Proposition boundaries defined, categories selected | Pre-Round |
| 2 | **Experience Pool Loaded** | Domain patterns available (if enabled) | Pre-Round |
| 3 | **Attacks Substantive** | Attacks are non-trivial, steel-manned | Round N: Red |
| 4 | **Attacks Diverse** | At least 2 different categories represented | Round N: Red |
| 5 | **Severities Assigned** | All attacks have severity with rationale | Round N: Red |
| 6 | **All Attacks Addressed** | Every attack has a defense response | Round N: Blue |
| 7 | **Critical Attacks Defended** | CRITICAL/HIGH have REFUTE or MITIGATE | Round N: Blue |
| 8 | **No Hand-Waving** | Defenses are actionable, not vague | Round N: Blue |
| 9 | **Convergence Evaluated** | Explicit continue/stop decision | Round N: Eval |
| 10 | **Risks Derived** | Unresolved attacks become risks | Post-Round |
| 11 | **Go/No-Go Issued** | Clear recommendation | Post-Round |
| 12 | **Hardened Proposition** | Battle-tested version documented | Post-Round |

### Gate Requirements by Intensity

| Gate | Light | Standard | Aggressive |
|------|-------|----------|------------|
| Attack categories | 3 | 5 | All applicable |
| Minimum attacks | 5 | 10 | 15+ |
| Steel-manning level | minimal | standard | maximum |
| Convergence mode | round_limit (2) | no_new_critical | no_new_critical |
| Max rounds | 2 | 3 | 5 |

---

## 9. Behavioral Guidelines

### Red Team Principles

- **Steel-man, don't strawman:** Make attacks as strong as possible
- **Attack the proposition, not the proposer:** Focus on ideas, not people
- **Be creative but realistic:** Novel attacks should be plausible
- **Prioritize ruthlessly:** CRITICAL issues first
- **Use the experience pool:** Don't reinvent known failures
- **Ideological Turing test:** Would a true critic accept this attack?

### Blue Team Principles

- **Defend genuinely, don't dismiss:** Every attack deserves honest consideration
- **Evidence over assertion:** REFUTE claims need proof
- **Actionable mitigations:** MITIGATE responses must be specific
- **Honest acceptance:** If you can't defend, ACCEPT the risk
- **Harden proactively:** Don't wait for attacks to strengthen
- **Avoid defensive denial:** Admitting weakness is strength

### Tone Calibration

| Intensity | Red Team Tone | Blue Team Tone |
|-----------|--------------|----------------|
| **Light** | Collaborative skeptic | Quick sanity check |
| **Standard** | Professional adversary | Thorough defense |
| **Aggressive** | Determined opponent | Comprehensive rebuttal |

---

## 10. Workflow Integration

### Upstream Skills

| Skill | Provides | Use Case |
|-------|----------|----------|
| `assumption-validator` | Assumption inventory | Attack assumptions already surfaced |
| `expert-panel-deliberation` | Multi-perspective input | Diverse attack/defense viewpoints |
| `research-interviewer` | KNOWLEDGE-CORPUS | Domain knowledge for attacks |

### Downstream Skills

| Skill | Receives | Use Case |
|-------|----------|----------|
| `expert-panel-deliberation` | RISK-ASSESSMENT | Panel review of risks |
| `generate-ideas` | Attack gaps | Generate alternatives for failed propositions |

### Skill Chaining Example

```
assumption-validator      → RISK-ASSESSMENT (assumption-derived)
                               ↓
red-blue-validator        → RISK-ASSESSMENT (adversarial-derived)
                               ↓
expert-panel-deliberation → Final recommendation with multi-expert review
```

---

## 11. References

| Document | Purpose |
|----------|---------|
| `references/attack-vector-catalog.md` | 10 attack categories with specific attacks |
| `references/red-team-techniques.md` | 8 attack generation techniques |
| `references/blue-team-techniques.md` | 8 defense techniques |
| `references/steel-manning-protocol.md` | Protocol for maximizing attack strength |
| `references/convergence-criteria.md` | Detailed criteria for stopping |
| `references/experience-pool-patterns.md` | 50+ failure patterns by domain |

### Core Library References

| Library | Element | Usage |
|---------|---------|-------|
| `core/skill-patterns.yaml` | PATTERN-06: ADVERSARIAL-VALIDATE | Workflow pattern |
| `core/artifact-contracts.yaml` | CONTRACT-08: RISK-ASSESSMENT | Output format |
| `core/scoring-rubrics.yaml` | RUBRIC-07: SEVERITY-SCORING | Attack severity |
| `core/technique-taxonomy.yaml` | CAT-UR, CAT-PP | Adversarial techniques |

---

## 12. Templates

| Template | Purpose |
|----------|---------|
| `templates/risk-assessment-output.md` | CONTRACT-08 compliant RISK-ASSESSMENT with adversarial extensions |
| `templates/attack-defense-log.md` | Round-by-round attack/defense documentation |
| `templates/hardened-proposition-output.md` | Battle-tested proposition with modifications |

---

## 13. Examples

### Example 1: Architecture Decision — Microservices Migration

```yaml
input:
  subject: "Migrate payment processing from monolith to microservices"
  subject_type: architecture
  max_rounds: 3
  attack_intensity: standard
  convergence_mode: no_new_critical
  include_experience_pool: true
  steel_manning_level: standard

flow:
  pre_round:
    proposition: "Decompose payment monolith into 5 microservices over 12 months"
    attack_surface:
      - ASSUMPTIONS: Team capability, timeline, complexity estimates
      - DEPENDENCIES: Infrastructure, vendor APIs, data consistency
      - SCALABILITY: Service coordination overhead
      - OPERATIONAL: Debugging distributed systems
      - EDGE_CASES: Partial failures, network partitions
    experience_pool_loaded:
      - "Distributed monolith anti-pattern"
      - "Service boundary misalignment"
      - "Operational complexity explosion"

  round_1:
    red_team:
      attacks:
        - ATK-1-1: "Team has zero production microservices experience"
          Category: ORGANIZATIONAL
          Severity: CRITICAL
          Steel-manned: "Even with training, production microservices require
                        tacit knowledge that only comes from operating them"

        - ATK-1-2: "12-month timeline ignores learning curve and unknowns"
          Category: TEMPORAL
          Severity: HIGH
          Steel-manned: "Industry benchmarks show microservices migrations
                        typically take 2-3x initial estimates"

        - ATK-1-3: "Distributed transactions will break payment consistency"
          Category: EDGE_CASES
          Severity: CRITICAL
          Steel-manned: "Payment systems require ACID guarantees that
                        eventual consistency cannot provide"

        - ATK-1-4: "Debugging distributed payment failures at 3 AM"
          Category: OPERATIONAL
          Severity: HIGH
          Steel-manned: "When payments fail across service boundaries,
                        MTTR could exceed SLA without distributed tracing expertise"

      new_critical: 2
      new_high: 2

    blue_team:
      defenses:
        - DEF-1-1: Response to ATK-1-1
          Type: MITIGATE
          Defense: "Hire 2 senior engineers with microservices experience.
                   Engage architecture consultancy for first 6 months."
          Residual: REDUCED

        - DEF-1-2: Response to ATK-1-2
          Type: HARDEN
          Defense: "Extend timeline to 18 months. Add 3-month buffer for unknowns."
          Proposition Change: "12 months" → "18 months with 3-month buffer"
          Residual: ELIMINATED

        - DEF-1-3: Response to ATK-1-3
          Type: HARDEN
          Defense: "Keep payment processing in single service with ACID guarantees.
                   Only extract non-critical services to microservices."
          Proposition Change: "5 microservices" → "3 microservices + 1 payment service"
          Residual: ELIMINATED

        - DEF-1-4: Response to ATK-1-4
          Type: MITIGATE
          Defense: "Implement distributed tracing (Jaeger) before migration.
                   Establish on-call runbooks. Require observability as launch gate."
          Residual: REDUCED

    evaluation:
      new_critical: 2
      new_high: 2
      convergence_mode: no_new_critical
      decision: CONTINUE
      rationale: "New critical attacks found; continue to Round 2"

  round_2:
    red_team:
      attacks:
        - ATK-2-1: "Hiring 2 senior engineers in 6 months is optimistic"
          Category: ORGANIZATIONAL
          Severity: HIGH
          Steel-manned: "Market for microservices expertise is extremely
                        competitive; 6-month hiring timeline may slip"

        - ATK-2-2: "Distributed tracing adds operational complexity itself"
          Category: OPERATIONAL
          Severity: MEDIUM
          Steel-manned: "Jaeger requires infrastructure, maintenance,
                        and expertise to operate"

        - ATK-2-3: "Service boundary around payments may be wrong"
          Category: ASSUMPTIONS
          Severity: MEDIUM
          Steel-manned: "Without event storming, service boundaries
                        are guesses that may need rework"

      new_critical: 0
      new_high: 1

    blue_team:
      defenses:
        - DEF-2-1: Response to ATK-2-1
          Type: MITIGATE
          Defense: "Begin hiring immediately. Have contingency: extend
                   consultancy or use contractor bridge if hiring slips."
          Residual: REDUCED

        - DEF-2-2: Response to ATK-2-2
          Type: ACCEPT
          Defense: "Accept additional complexity as cost of observability.
                   Allocate 0.5 FTE for observability platform."
          Residual: UNCHANGED (but monitored)

        - DEF-2-3: Response to ATK-2-3
          Type: HARDEN
          Defense: "Conduct event storming workshop before finalizing
                   service boundaries. Add 4 weeks for domain modeling."
          Proposition Change: Add event storming phase
          Residual: ELIMINATED

    evaluation:
      new_critical: 0
      new_high: 1
      convergence_mode: no_new_critical
      decision: CONTINUE (HIGH attack found)

  round_3:
    red_team:
      attacks:
        - ATK-3-1: "Event storming may reveal the migration is unnecessary"
          Category: ASSUMPTIONS
          Severity: MEDIUM
          Steel-manned: "Domain modeling might show modular monolith
                        is sufficient for scaling needs"

        - ATK-3-2: "Consultancy dependency creates knowledge transfer risk"
          Category: DEPENDENCIES
          Severity: MEDIUM
          Steel-manned: "If consultants leave, tacit knowledge leaves with them"

      new_critical: 0
      new_high: 0

    blue_team:
      defenses:
        - DEF-3-1: Response to ATK-3-1
          Type: ACCEPT
          Defense: "Valid point. Event storming is a gate; if it reveals
                   microservices aren't needed, we pivot to modular monolith."
          Residual: UNCHANGED (but this is a feature, not a bug)

        - DEF-3-2: Response to ATK-3-2
          Type: MITIGATE
          Defense: "Require knowledge transfer sessions, documentation
                   deliverables, and pair programming in consultancy contract."
          Residual: REDUCED

    evaluation:
      new_critical: 0
      new_high: 0
      convergence_mode: no_new_critical
      decision: CONVERGED
      rationale: "No new CRITICAL or HIGH attacks. Proposition has been hardened."

  post_round:
    hardened_proposition:
      original: "Migrate payment processing from monolith to 5 microservices
                over 12 months"

      battle_tested: "Migrate to 3 microservices + 1 payment service over
                     18 months (with 3-month buffer), after event storming
                     confirms boundaries. Requires: 2 hired senior engineers,
                     architecture consultancy, distributed tracing infrastructure,
                     0.5 FTE observability platform maintenance."

      modifications:
        - MOD-1: 5 services → 3 + 1 payment (Response to ATK-1-3)
        - MOD-2: 12 months → 18 months + buffer (Response to ATK-1-2)
        - MOD-3: Added event storming prerequisite (Response to ATK-2-3)
        - MOD-4: Added observability infrastructure requirement (Response to ATK-1-4)

      accepted_residual_risks:
        - "Hiring timeline may slip (mitigated by contingency)"
        - "Observability platform adds operational overhead (accepted)"
        - "Event storming may reveal migration unnecessary (feature)"
        - "Consultancy knowledge transfer requires active management"

      battle_tested_confidence: 72
      confidence_rationale: "Proposition survived 3 rounds of substantive attacks.
                           Critical issues addressed through hardening.
                           Residual risks are manageable and monitored."

    risk_assessment:
      total_risks: 4
      critical_risks: 0
      high_risks: 1 (hiring timeline)
      moderate_risks: 3
      risk_profile: MODERATE
      go_no_go: PROCEED_WITH_CAUTION

      recommendation: |
        PROCEED_WITH_CAUTION — The original proposition had critical flaws
        (team capability, payment consistency, timeline). The hardened
        proposition addresses these through:
        - Scoped migration (keeping payments transactional)
        - Extended timeline with buffer
        - Event storming validation gate
        - Observability prerequisites

        Key risks to monitor:
        1. Hiring: Start immediately; have contingency ready
        2. Consultancy knowledge transfer: Contract requirements
        3. Event storming outcome: Be prepared to pivot if boundaries don't hold
```

---

### Example 2: Strategy Validation — Market Expansion

```yaml
input:
  subject: "Expand to European market in Q3 with existing product"
  subject_type: strategy
  max_rounds: 2
  attack_intensity: standard
  convergence_mode: no_new_critical

flow:
  round_1:
    red_team:
      attacks:
        - ATK-1-1: "GDPR compliance timeline is unrealistic"
          Severity: CRITICAL
        - ATK-1-2: "Competitor X already dominates EU market"
          Severity: HIGH
        - ATK-1-3: "Pricing model assumes US willingness-to-pay"
          Severity: HIGH
        - ATK-1-4: "No local sales team or market knowledge"
          Severity: MEDIUM

    blue_team:
      defenses:
        - DEF-1-1: HARDEN - Push launch to Q4; engage GDPR consultancy
        - DEF-1-2: MITIGATE - Focus on underserved segments competitor ignores
        - DEF-1-3: HARDEN - Conduct pricing research; plan EU-specific pricing
        - DEF-1-4: MITIGATE - Partner with EU distributor initially

    evaluation:
      new_critical: 1
      decision: CONTINUE

  round_2:
    red_team:
      attacks:
        - ATK-2-1: "EU distributor takes 40% margin"
          Severity: MEDIUM
        - ATK-2-2: "Underserved segments may be underserved for good reason"
          Severity: MEDIUM

    blue_team:
      defenses:
        - DEF-2-1: ACCEPT - Cost of market entry; build direct sales in Year 2
        - DEF-2-2: MITIGATE - Validate segment with EU market research

    evaluation:
      new_critical: 0
      new_high: 0
      decision: CONVERGED

  post_round:
    hardened_proposition: |
      Launch EU expansion in Q4 (not Q3) with:
      - GDPR compliance verified by consultancy
      - EU-specific pricing based on market research
      - Initial distribution through EU partner
      - Focus on [specific underserved segments]
      - Year 2: Build direct sales capability

    risk_assessment:
      profile: MODERATE
      go_no_go: PROCEED_WITH_CAUTION
```

---

### Example 3: Investment Decision — Series B Funding

```yaml
input:
  subject: "Accept Series B term sheet at $50M valuation"
  subject_type: investment
  max_rounds: 2
  attack_intensity: standard
  convergence_mode: no_new_critical

flow:
  pre_round:
    proposition: "Accept $15M Series B at $50M pre-money valuation from [VC Firm]"
    attack_surface:
      - ECONOMIC: Valuation, dilution, runway
      - ASSUMPTIONS: Growth projections, market size
      - DEPENDENCIES: VC firm reputation, board dynamics
      - COMPETITIVE: Market timing, competitor funding

  round_1:
    red_team:
      attacks:
        - ATK-1-1: "Valuation assumes 3x YoY growth; current trajectory is 1.8x"
          Category: ASSUMPTIONS
          Severity: HIGH
          Steel-manned: "At 1.8x growth, next round valuation math doesn't work;
                        down round likely in 18 months"

        - ATK-1-2: "15-month runway at current burn; need to hit milestones or raise bridge"
          Category: ECONOMIC
          Severity: HIGH
          Steel-manned: "Milestones require growth acceleration you haven't demonstrated"

        - ATK-1-3: "[VC Firm] has reputation for replacing founders at Series C"
          Category: DEPENDENCIES
          Severity: MEDIUM
          Steel-manned: "3 of their last 5 Series B companies had founder transitions"

        - ATK-1-4: "Competitor just raised $40M; will outspend on customer acquisition"
          Category: COMPETITIVE
          Severity: HIGH
          Steel-manned: "Their CAC advantage compounds; market share gap widens"

    blue_team:
      defenses:
        - DEF-1-1: Response to ATK-1-1
          Type: HARDEN
          Defense: "Negotiate milestone-based valuation adjustment; lower initial
                   valuation with ratchet up if growth targets hit"
          Proposition Change: Add milestone ratchet provision

        - DEF-1-2: Response to ATK-1-2
          Type: MITIGATE
          Defense: "Negotiate 18-month runway minimum; reduce burn by 20% through
                   hiring pause; extend runway to 20 months"
          Residual: REDUCED

        - DEF-1-3: Response to ATK-1-3
          Type: MITIGATE
          Defense: "Negotiate founder-friendly protective provisions; 2-year
                   employment agreements; board composition safeguards"
          Residual: REDUCED

        - DEF-1-4: Response to ATK-1-4
          Type: ACCEPT
          Defense: "Competitive pressure is real but unavoidable. Focus on
                   capital-efficient growth and product differentiation over
                   CAC war. This is market reality, not term sheet issue."
          Residual: UNCHANGED

    evaluation:
      new_critical: 0
      new_high: 3
      decision: CONTINUE

  round_2:
    red_team:
      attacks:
        - ATK-2-1: "Milestone ratchet creates misaligned incentives; may optimize
                   for metrics over business health"
          Category: ASSUMPTIONS
          Severity: MEDIUM

        - ATK-2-2: "Hiring pause delays product roadmap; competitive gap widens"
          Category: TEMPORAL
          Severity: MEDIUM

    blue_team:
      defenses:
        - DEF-2-1: Response to ATK-2-1
          Type: MITIGATE
          Defense: "Structure milestones around leading indicators (retention,
                   NPS) not just growth metrics"
          Residual: REDUCED

        - DEF-2-2: Response to ATK-2-2
          Type: ACCEPT
          Defense: "Trade-off accepted; survival > speed. Revisit hiring
                   after 6-month runway checkpoint."
          Residual: UNCHANGED

    evaluation:
      new_critical: 0
      new_high: 0
      decision: CONVERGED

  post_round:
    hardened_proposition: |
      Accept Series B with modifications:
      - Milestone-based valuation: $45M base + $10M ratchet if 2.5x growth
      - 18-month minimum runway commitment
      - Founder protective provisions (2-year agreements, board balance)
      - Hiring pause for 6 months; revisit at runway checkpoint
      - Milestones tied to retention/NPS, not just growth

    risk_assessment:
      total_risks: 4
      risk_profile: MODERATE
      go_no_go: PROCEED_WITH_CAUTION

      recommendation: |
        PROCEED_WITH_CAUTION — Accept modified term sheet. Key risks:
        1. Competitive pressure (accepted as market reality)
        2. Growth trajectory uncertainty (mitigated by ratchet)
        3. Founder/board dynamics (mitigated by provisions)

        Negotiate the hardened terms before signing. Walk away if
        milestone ratchet or protective provisions rejected.
```

---

## 14. Quick Start

### Minimal Invocation

```
Red team this: [paste proposition]
```

### Standard Invocation

```
subject_type: decision
attack_intensity: standard
convergence_mode: no_new_critical

Proposition: [description or document]
```

### Full Parameter Invocation

```
subject_type: architecture
max_rounds: 4
attack_intensity: aggressive
attack_categories: [ASSUMPTIONS, SCALABILITY, SECURITY, OPERATIONAL]
convergence_mode: all_addressed
include_experience_pool: true
steel_manning_level: maximum
output_mode: full

Proposition: [detailed description]

Context:
- Stakes: [why this matters]
- Constraints: [limitations]
- Stakeholders: [who cares]
```
