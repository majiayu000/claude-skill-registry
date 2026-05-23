---
name: assumption-validator
version: "2.0"
description: >
  Systematically surface, classify, and stress-test assumptions in decisions,
  strategies, and plans. Transforms hidden assumptions into visible, testable
  propositions with load-bearing analysis and counterfactual validation.

  PROACTIVELY activate for: (1) Pre-commitment decision reviews, (2) Strategy
  validation before execution, (3) Investment due diligence, (4) Architecture
  decision records, (5) Product direction pivots, (6) Risk assessments requiring
  assumption audit.

  Triggers: "validate assumptions", "test assumptions", "assumption check",
  "stress test this decision", "what are we assuming", "pre-mortem",
  "what could go wrong", "challenge this plan", "devil's advocate"
---

# Assumption Validator

> "Make hidden assumptions visible; make visible assumptions testable."

Assumptions are the invisible architecture of every decision. This skill provides a systematic methodology for surfacing, classifying, validating, and stress-testing the assumptions that underlie decisions, strategies, plans, and architectures. The output is a RISK-ASSESSMENT artifact that transforms assumption risk into actionable guidance.

---

## 1. Purpose

### Core Value Proposition

Every decision rests on assumptions. Some are explicit and acknowledged. Many are implicit, hidden in the reasoning chain. The most dangerous are structural—embedded in how we frame the problem itself. This skill makes the invisible visible and the untested testable.

### Capabilities

| # | Capability | Phase | Value |
|---|-----------|-------|-------|
| 1 | Extract explicit assumptions from subject documents | 2 | Capture what's acknowledged |
| 2 | Surface implicit assumptions through structured probing | 2 | Reveal hidden dependencies |
| 3 | Identify structural assumptions in problem framing | 2 | Expose framing blind spots |
| 4 | Classify assumptions by type and risk profile | 3 | Enable prioritization |
| 5 | Perform load-bearing analysis for criticality scoring | 3 | Focus on what matters |
| 6 | Map assumption dependencies | 3 | Understand cascade effects |
| 7 | Validate assumptions against available evidence | 4 | Assess confidence levels |
| 8 | Execute counterfactual analysis (what-if scenarios) | 4 | Stress-test under alternatives |
| 9 | Calibrate confidence with epistemic labels | 4 | Communicate uncertainty |
| 10 | Derive risks from unvalidated/invalid assumptions | 5 | Convert to actionable risks |
| 11 | Generate RISK-ASSESSMENT artifact | 5 | Standardized output |
| 12 | Provide go/no-go recommendation | 5 | Decision support |

---

## 2. When to Use

### Ideal Use Cases

| Scenario | Why Assumption Validation Matters |
|----------|-----------------------------------|
| **Pre-commitment decision review** | Before committing resources, surface what you're betting on |
| **Strategy validation** | Strategies often embed untested market/competitive assumptions |
| **Investment due diligence** | Financial decisions rest on projections built on assumptions |
| **Architecture Decision Records (ADRs)** | Technical choices assume certain constraints and capabilities |
| **Product direction pivots** | Pivots invalidate old assumptions; what new ones are introduced? |
| **Risk assessments** | Risks often emerge from assumption failures |
| **Merger & acquisition analysis** | Synergy assumptions are notoriously optimistic |
| **Go-to-market plans** | Market assumptions may not survive contact with reality |
| **Capacity planning** | Growth assumptions drive infrastructure decisions |
| **Vendor selection** | Vendor capabilities are often assumed, not verified |

### Anti-Patterns (When NOT to Use)

| Anti-Pattern | Why It's Ineffective | Better Alternative |
|--------------|----------------------|-------------------|
| **Analysis paralysis** | Validating every assumption delays action forever | Set validation_intensity: light |
| **Reversible decisions** | Over-analyzing easily reversible choices wastes effort | Just decide and iterate |
| **Well-established facts** | Questioning gravity wastes time | Focus on genuine uncertainties |
| **Time-critical emergencies** | Fires need extinguishing, not philosophy | Use judgment, then debrief |
| **Exploratory research** | Early exploration should generate assumptions, not validate them | Use research-interviewer first |

---

## 3. Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `subject_type` | enum | **yes** | — | decision \| strategy \| plan \| architecture \| investment \| product_direction |
| `validation_intensity` | enum | no | standard | light \| standard \| rigorous |
| `assumption_depth` | enum | no | include_implicit | explicit_only \| include_implicit \| full_structural |
| `counterfactual_analysis` | boolean | no | true | Run what-if scenarios for top assumptions |
| `confidence_threshold` | number | no | 0.7 | Minimum confidence for "validated" status (0.0-1.0) |
| `time_horizon` | enum | no | all | short_term \| medium_term \| long_term \| all |

### Parameter Effects Matrix

| Parameter | Effect on Phase 2 | Effect on Phase 3 | Effect on Phase 4 |
|-----------|------------------|------------------|------------------|
| `validation_intensity: light` | 2 surfacing techniques | Top 3 load-bearing only | Evidence check only |
| `validation_intensity: standard` | 4 surfacing techniques | Top 5 load-bearing | Evidence + counterfactual |
| `validation_intensity: rigorous` | All surfacing techniques | All assumptions scored | Full validation battery |
| `assumption_depth: explicit_only` | Document scan only | — | — |
| `assumption_depth: include_implicit` | + Inversion, Five Whys | — | — |
| `assumption_depth: full_structural` | + Frame questioning | — | — |
| `time_horizon: short_term` | — | Filter to 0-6 months | — |
| `time_horizon: long_term` | — | Filter to 2+ years | — |

---

## 4. Five-Phase Workflow

### Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ASSUMPTION VALIDATOR                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   PHASE 1    │    │   PHASE 2    │    │   PHASE 3    │                   │
│  │   Subject    │───▶│  Assumption  │───▶│Classification│                   │
│  │   Intake     │    │  Surfacing   │    │& Prioritize  │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│         │                   │                   │                            │
│         ▼                   ▼                   ▼                            │
│    [Framed         [Raw Assumption      [Prioritized                        │
│     Subject]        Inventory]           List]                              │
│                                                 │                            │
│                                                 ▼                            │
│                          ┌──────────────┐    ┌──────────────┐               │
│                          │   PHASE 5    │◀───│   PHASE 4    │               │
│                          │  Synthesis   │    │  Validation  │               │
│                          │& Risk Assess │    │& Stress Test │               │
│                          └──────────────┘    └──────────────┘               │
│                                 │                   │                        │
│                                 ▼                   ▼                        │
│                          [RISK-ASSESSMENT   [Validated/                     │
│                           CONTRACT-08]       Invalidated]                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Subject Intake & Framing

**Purpose:** Understand what's being validated and establish clear boundaries.

**Steps:**

1. **Receive subject artifact**
   - Accept decision document, strategy brief, plan, ADR, or proposal
   - If verbal, request written summary or create one together
   - Note: Subject should be specific enough to identify assumptions

2. **Extract context metadata**
   - Subject type (decision, strategy, plan, architecture, investment, product_direction)
   - Time horizon (when does this need to succeed?)
   - Stakeholders (whose assumptions might be embedded?)
   - Decision reversibility (high-stakes or easily changed?)

3. **Define validation scope**
   - What's in scope for assumption analysis?
   - What's explicitly out of scope?
   - Are there protected assumptions (e.g., executive mandates)?

4. **Identify information sources**
   - Subject document(s)
   - Supporting materials
   - Domain experts available for consultation
   - Historical precedents

5. **Set validation intensity**
   - Light: Quick scan, top assumptions only
   - Standard: Balanced depth and coverage
   - Rigorous: Exhaustive, all techniques applied

6. **Confirm framing with stakeholder**
   - "We're validating assumptions in [subject] with [intensity] intensity."
   - "Scope includes [X], excludes [Y]."
   - "Time horizon is [Z]."

**Quality Gate:** Subject Framed
- [ ] Subject boundaries explicitly defined
- [ ] Context metadata captured
- [ ] Validation intensity confirmed
- [ ] Information sources identified

**Output:** Framed subject with boundaries and context

---

### Phase 2: Assumption Surfacing

**Purpose:** Extract all assumption types—explicit, implicit, and structural.

**Reference:** See `references/surfacing-techniques.md` for detailed protocols.

**Steps:**

1. **Scan for explicit assumptions**
   - Search subject document for assumption markers:
     - "We assume...", "Given that...", "Assuming..."
     - "This depends on...", "If [condition]..."
     - "We're betting that...", "Our hypothesis is..."
   - Document verbatim with source location
   - **See:** `references/assumption-taxonomy.md` §1 (Explicit)

2. **Probe for implicit assumptions**

   Apply surfacing techniques based on `assumption_depth`:

   | Technique | Question | Yields |
   |-----------|----------|--------|
   | **Inversion** | "What would have to be true for this to fail?" | Hidden dependencies |
   | **Five Whys** | "Why do we believe this? Why? Why?" | Reasoning chain foundations |
   | **Outsider Test** | "What would a skeptic question first?" | Non-obvious assumptions |
   | **Pre-mortem** | "It failed. What assumption was wrong?" | Failure-mode assumptions |
   | **Dependency Mapping** | "What does this depend on?" | Upstream assumptions |

   - **See:** `references/surfacing-techniques.md` for full technique protocols

3. **Surface structural assumptions** (if `assumption_depth: full_structural`)

   | Technique | Question | Yields |
   |-----------|----------|--------|
   | **Frame Questioning** | "Why did we frame this as X not Y?" | Framing assumptions |
   | **Missing Voices** | "Whose perspective is absent?" | Stakeholder blind spots |
   | **Scope Boundary Probe** | "Why is X out of scope?" | Scope assumptions |
   | **Alternative Structures** | "What if we organized around different dimensions?" | Structural alternatives |

   - **See:** `references/assumption-taxonomy.md` §3 (Structural)

4. **Document each assumption**

   For each assumption captured:
   ```
   - ID: A[n]
   - Statement: [Clear, falsifiable statement]
   - Type: EXPLICIT | IMPLICIT | STRUCTURAL
   - Source: [How it was identified]
   - Initial confidence: [0.0-1.0 estimate]
   ```

5. **Check for completeness**
   - Have we covered all sections of the subject document?
   - Have we applied minimum techniques per intensity level?
   - Are there obvious gaps in coverage?

**Quality Gates:**
- [ ] **All Explicit Captured:** Document scan for assumption markers complete
- [ ] **Implicit Probe Done:** At least N surfacing techniques applied (N per intensity)
- [ ] **Structural Check:** Frame questioning performed (if full_structural)

**Output:** Raw assumption inventory (unclassified, unprioritized)

---

### Phase 3: Classification & Prioritization

**Purpose:** Categorize assumptions by type and score criticality for prioritization.

**Reference:** See `references/load-bearing-analysis.md` for scoring framework.

**Steps:**

1. **Assign assumption types**

   Classify each assumption into one or more types:

   | Type | Definition | Risk Level |
   |------|------------|------------|
   | **EXPLICIT** | Directly stated in subject document | Low (acknowledged) |
   | **IMPLICIT** | Required for conclusions but unstated | Medium (hidden) |
   | **STRUCTURAL** | Embedded in problem framing | High (invisible) |
   | **LOAD-BEARING** | If wrong, entire edifice collapses | Critical |
   | **CONTEXTUAL** | About environment/market/conditions | Variable |
   | **BEHAVIORAL** | About how people/systems will act | Medium-High |

   - **See:** `references/assumption-taxonomy.md` for detailed type definitions

2. **Perform load-bearing analysis**

   Score each assumption on four dimensions:

   | Dimension | Scale | Question |
   |-----------|-------|----------|
   | **Dependency (D)** | 1-5 | How many conclusions depend on this? |
   | **Reversibility (R)** | 1-5 | Can we recover if this is wrong? |
   | **Validation Cost (V)** | 1-5 | How hard is it to verify? (inverse) |
   | **Confidence (C)** | 0-1 | How confident are we currently? |

   **Priority Formula:**
   ```
   Priority = (D × (1 - C)) / V
   ```

   High dependency, low confidence, low validation cost = highest priority

   - **See:** `references/load-bearing-analysis.md` for scoring rubrics

3. **Map dependencies**

   For high-priority assumptions:
   - What other assumptions depend on this one?
   - What conclusions would be invalidated if wrong?
   - Are there assumption chains (A depends on B depends on C)?

4. **Identify load-bearing assumptions**

   Flag assumptions where:
   - Priority score > threshold (typically 2.0)
   - OR dependency score = 5 (everything depends on it)
   - OR labeled STRUCTURAL (framing assumptions)

5. **Rank and filter**

   - Sort by priority score descending
   - Per intensity level:
     - Light: Top 3
     - Standard: Top 5
     - Rigorous: All with priority > 1.0

**Quality Gates:**
- [ ] **Types Assigned:** Every assumption has type classification
- [ ] **Load-Bearing Identified:** Top N critical assumptions flagged
- [ ] **Priority Scores:** All assumptions have priority scores

**Output:** Prioritized assumption list with scores and dependencies

---

### Phase 4: Validation & Stress-Testing

**Purpose:** Test assumptions against evidence and counterfactual scenarios.

**Reference:** See `references/validation-methods.md` and `references/what-if-framework.md`.

**Steps:**

1. **Select validation methods per assumption**

   Match methods to assumption characteristics:

   | Assumption Type | Recommended Methods |
   |-----------------|---------------------|
   | EXPLICIT | Evidence check, Cross-validation |
   | IMPLICIT | Counterfactual, Expert challenge |
   | STRUCTURAL | Frame alternatives, Outside perspective |
   | CONTEXTUAL | Historical precedent, Time decay test |
   | BEHAVIORAL | Stakeholder interviews, Incentive analysis |

   - **See:** `references/validation-methods.md` for method protocols

2. **Execute evidence check**

   For each prioritized assumption:

   | Evidence Quality | Weight | Description |
   |------------------|--------|-------------|
   | **Primary source** | 1.0 | Direct measurement, documentation |
   | **Secondary source** | 0.7 | Reported by credible third party |
   | **Expert opinion** | 0.6 | Domain expert judgment |
   | **Inference** | 0.4 | Logical derivation from other facts |
   | **Assumption** | 0.2 | Based on another assumption |

   - Document evidence found (or lack thereof)
   - Note evidence quality and source

3. **Run counterfactual analysis** (if `counterfactual_analysis: true`)

   For top load-bearing assumptions:

   ```
   WHAT-IF: [Assumption] is FALSE

   Immediate impacts:
   - [What breaks immediately?]

   Cascade effects:
   - [What else fails as a consequence?]

   Decision change:
   - [Would the decision/strategy change?]

   Impact magnitude: NEGLIGIBLE | MINOR | MODERATE | MAJOR | CATASTROPHIC
   ```

   - **See:** `references/what-if-framework.md` for structured protocol

4. **Calibrate confidence**

   Assign epistemic labels based on evidence:

   | Label | Confidence | Definition |
   |-------|------------|------------|
   | **VERIFIED** | 0.9-1.0 | Confirmed by direct evidence |
   | **LIKELY** | 0.7-0.9 | Strong indirect evidence |
   | **POSSIBLE** | 0.4-0.7 | Some supporting evidence |
   | **SPECULATIVE** | 0.1-0.4 | Limited evidence, mostly inference |
   | **UNKNOWN** | 0.0-0.1 | Insufficient basis for judgment |

   - **See:** `references/confidence-calibration.md` for calibration techniques

5. **Determine validation status**

   | Status | Criteria |
   |--------|----------|
   | **VALIDATED** | Confidence ≥ `confidence_threshold`, evidence quality ≥ 0.7 |
   | **PARTIAL** | Some evidence, but confidence < threshold |
   | **UNVALIDATED** | No evidence found, or conflicting evidence |
   | **INVALIDATED** | Evidence contradicts assumption |
   | **CONTESTED** | Multiple sources disagree |

6. **Document validation results**

   Per assumption:
   ```
   - Validation status: [status]
   - Confidence: [0.0-1.0]
   - Epistemic label: [label]
   - Evidence summary: [brief]
   - Counterfactual impact: [if run]
   - Validation method(s): [methods used]
   ```

**Quality Gates:**
- [ ] **Top N Validated:** Top assumptions have validation results
- [ ] **Counterfactuals Run:** What-if scenarios for load-bearing assumptions
- [ ] **Confidence Calibrated:** All assumptions have epistemic labels

**Output:** Validated/invalidated assumptions with confidence levels

---

### Phase 5: Synthesis & Risk Assessment

**Purpose:** Compile findings into RISK-ASSESSMENT artifact with actionable recommendations.

**Reference:** See `templates/risk-assessment-output.md` for CONTRACT-08 format.

**Steps:**

1. **Derive risks from assumption status**

   Transform assumption findings into risks:

   | Assumption Status | Risk Derivation |
   |-------------------|-----------------|
   | INVALIDATED | Direct risk: "Assumption X is false" |
   | UNVALIDATED | Risk: "Assumption X may be false (unverified)" |
   | CONTESTED | Risk: "Disagreement on assumption X" |
   | Low confidence | Risk: "Uncertain assumption X (confidence: Y)" |
   | High dependency + any issue | Amplified risk due to cascade |

2. **Score each derived risk**

   Using SEVERITY-SCORING (RUBRIC-07):

   | Dimension | Scale | Weight |
   |-----------|-------|--------|
   | **Impact** | 1-4 (low→critical) | 0.5 |
   | **Likelihood** | 1-4 (rare→certain) | 0.3 |
   | **Detectability** | 1-4 (obvious→hidden) | 0.2 |

   Risk score = weighted sum

3. **Develop mitigation strategies**

   For high-scoring risks:

   | Strategy | When to Use |
   |----------|-------------|
   | **Avoid** | Remove dependency on assumption (redesign) |
   | **Transfer** | Shift risk to party who can validate |
   | **Mitigate** | Add safeguards, monitoring, fallbacks |
   | **Accept** | Document and proceed with awareness |

   Each mitigation should specify:
   - Actions required
   - Residual risk after mitigation
   - Owner and timeline (if applicable)

4. **Assess overall risk profile**

   | Risk Profile | Criteria |
   |--------------|----------|
   | **VERY HIGH** | Multiple critical risks, invalidated load-bearing assumptions |
   | **HIGH** | Critical risk present, or several high risks |
   | **MODERATE** | High risks present but mitigatable |
   | **LOW** | No high/critical risks, most assumptions validated |
   | **VERY LOW** | All key assumptions validated, minor risks only |

5. **Generate go/no-go recommendation**

   | Recommendation | When |
   |----------------|------|
   | **PROCEED** | Low/very low risk, assumptions validated |
   | **PROCEED_WITH_CAUTION** | Moderate risk, mitigations in place |
   | **SIGNIFICANT_CONCERNS** | High risk, key assumptions unvalidated |
   | **DO_NOT_PROCEED** | Very high risk, load-bearing assumptions invalid |

6. **Compile RISK-ASSESSMENT artifact**

   Structure per CONTRACT-08:
   - Subject reference and metadata
   - Assessment method (techniques used, assumptions surfaced)
   - Risk list with scores and mitigations
   - Summary with profile and recommendation

   - **See:** `templates/risk-assessment-output.md` for complete template

7. **Generate supporting artifacts**

   - Assumption Inventory: Complete catalog with validation status
   - Sensitivity Analysis: Impact magnitude per assumption

   - **See:** `templates/assumption-inventory-output.md`
   - **See:** `templates/sensitivity-analysis-output.md`

**Quality Gates:**
- [ ] **Risks Derived:** Assumption-derived risks enumerated
- [ ] **Go/No-Go Issued:** Assessment concludes with recommendation

**Output:** RISK-ASSESSMENT (CONTRACT-08), Assumption Inventory, Sensitivity Analysis

---

## 5. Assumption Taxonomy

Six types of assumptions, ordered by visibility and risk:

### 5.1 EXPLICIT Assumptions

**Definition:** Directly stated in the subject document or explicitly acknowledged.

**Characteristics:**
- Visible in text ("We assume...", "Given that...")
- Author is aware of them
- Often documented in "Assumptions" section

**Detection Heuristics:**
- Text search for assumption markers
- Review formal "Assumptions" sections
- Check footnotes and caveats

**Risk Level:** LOW (already acknowledged)

**Example:**
> "This business case assumes 15% year-over-year growth."

### 5.2 IMPLICIT Assumptions

**Definition:** Required for conclusions but not stated; inferred from reasoning.

**Characteristics:**
- Hidden in the logical chain
- Author may not realize they exist
- Often "obvious" to insiders

**Detection Heuristics:**
- Inversion: "What must be true for this to work?"
- Five Whys: Drill into reasoning
- Outsider test: "What would a newcomer question?"

**Risk Level:** MEDIUM (can be surfaced with effort)

**Example:**
> Document says "Users will migrate to new system"
> Implicit: Users have time/motivation to learn new system
> Implicit: New system is better enough to justify switching cost

### 5.3 STRUCTURAL Assumptions

**Definition:** Embedded in how the problem is framed; invisible to those inside the frame.

**Characteristics:**
- Shape what questions get asked
- Define what's in/out of scope
- Often only visible in hindsight

**Detection Heuristics:**
- Frame questioning: "Why this frame, not another?"
- Missing voices: "Who isn't represented?"
- Scope boundary probe: "Why is X out of scope?"

**Risk Level:** HIGH (often invisible until too late)

**Example:**
> Problem framed as "How do we improve our mobile app?"
> Structural assumption: Mobile app is the right solution
> Missed: Maybe users want a different channel entirely

### 5.4 LOAD-BEARING Assumptions

**Definition:** Assumptions where failure causes the entire plan/decision to collapse.

**Characteristics:**
- Everything depends on them
- Often single points of failure
- May be any of the other types

**Detection Heuristics:**
- Dependency mapping: Trace what relies on what
- Pre-mortem: "What caused total failure?"
- Inversion: "Without X, does anything work?"

**Risk Level:** CRITICAL (single point of failure)

**Example:**
> Strategy depends on "Competitor won't react for 18 months"
> If wrong: Entire competitive positioning collapses

### 5.5 CONTEXTUAL Assumptions

**Definition:** Assumptions about the environment, market, or conditions.

**Characteristics:**
- External to the organization
- Often based on current state
- May change without warning

**Detection Heuristics:**
- Environmental scan: Market, regulatory, technology
- Time decay test: "Will this hold in 1/3/5 years?"
- External dependency check

**Risk Level:** VARIABLE (depends on volatility)

**Example:**
> "Interest rates will remain below 5%"
> "No new regulations in this space"
> "Technology X will become standard"

### 5.6 BEHAVIORAL Assumptions

**Definition:** Assumptions about how people, teams, or systems will act.

**Characteristics:**
- Human/organizational behavior
- Often optimistic
- Frequently wrong

**Detection Heuristics:**
- Stakeholder modeling: "Will they actually do X?"
- Incentive analysis: "Why would they?"
- Historical behavior: "Have they done this before?"

**Risk Level:** MEDIUM-HIGH (humans are unpredictable)

**Example:**
> "Engineering team will adopt new practices"
> "Customers will understand the value proposition"
> "Partners will share data as promised"

---

## 6. Surfacing Techniques Summary

| Technique | Primary Use | Expected Yield | Time |
|-----------|-------------|----------------|------|
| **Document Scan** | Explicit | 3-10 assumptions | 15m |
| **Inversion** | Implicit | 5-15 assumptions | 30m |
| **Five Whys** | Implicit | 3-8 per chain | 20m |
| **Outsider Test** | Implicit | 5-10 assumptions | 20m |
| **Pre-mortem** | Load-bearing | 5-12 assumptions | 30m |
| **Dependency Mapping** | Load-bearing | 3-8 dependencies | 30m |
| **Frame Questioning** | Structural | 2-5 assumptions | 20m |
| **Missing Voices** | Structural | 2-4 assumptions | 15m |
| **Scope Boundary Probe** | Structural | 2-6 assumptions | 15m |
| **Reverse Assumption** | Validation | 1 per assumption | 5m ea |

**See:** `references/surfacing-techniques.md` for detailed protocols.

---

## 7. Validation Methods Summary

| Method | Best For | Evidence Type | Cost |
|--------|----------|---------------|------|
| **Evidence Check** | All | Documentary | Low |
| **Counterfactual** | Load-bearing | Analytical | Medium |
| **Sensitivity Analysis** | Quantitative | Analytical | Medium |
| **Historical Precedent** | Contextual | Comparative | Low |
| **Expert Challenge** | Technical | Opinion | Medium |
| **Cross-Validation** | Critical | Multi-source | High |
| **Stress Test** | Robustness | Analytical | Medium |
| **Time Decay Test** | Contextual | Analytical | Low |

**See:** `references/validation-methods.md` for detailed protocols.

---

## 8. Load-Bearing Analysis Framework

### Scoring Dimensions

| Dimension | Score 1 | Score 3 | Score 5 |
|-----------|---------|---------|---------|
| **Dependency** | Minor detail | Key component | Everything depends |
| **Reversibility** | Easy to pivot | Moderate rework | Catastrophic |
| **Validation Cost** | Trivial to check | Needs effort | Very difficult |

### Priority Calculation

```
Priority = (Dependency × (1 - Confidence)) / Validation Cost
```

**Interpretation:**
- Priority > 3.0: CRITICAL - Validate immediately
- Priority 2.0-3.0: HIGH - Validate before decision
- Priority 1.0-2.0: MEDIUM - Validate if time permits
- Priority < 1.0: LOW - Document and accept

**See:** `references/load-bearing-analysis.md` for complete framework.

---

## 9. Output Specifications

### 9.1 Primary Output: RISK-ASSESSMENT

Compliant with CONTRACT-08 from `artifact-contracts.yaml`.

```xml
<risk_assessment contract="CONTRACT-08">
  <metadata>
    <artifact_id>[unique identifier]</artifact_id>
    <created>[timestamp]</created>
    <subject_reference>[what was assessed]</subject_reference>
    <subject_type>[decision|strategy|plan|architecture|investment|product_direction]</subject_type>
  </metadata>

  <assessment_method>
    <technique>assumption_validation</technique>
    <assumptions_surfaced>[count]</assumptions_surfaced>
    <techniques_applied>[list of surfacing techniques]</techniques_applied>
    <time_horizon>[short_term|medium_term|long_term|all]</time_horizon>
  </assessment_method>

  <risks>
    <risk id="R1">
      <category>[assumption_failure|dependency|behavioral|contextual]</category>
      <description>[risk description]</description>
      <source_assumption>[assumption ID that generated this risk]</source_assumption>
      <trigger>[what would cause this risk to materialize]</trigger>
      <probability>[very_low|low|medium|high|very_high]</probability>
      <impact>[negligible|minor|moderate|major|catastrophic]</impact>
      <risk_score>[calculated score]</risk_score>
      <mitigation>
        <strategy>[avoid|transfer|mitigate|accept]</strategy>
        <actions>
          <action>[specific action]</action>
        </actions>
        <residual_risk>[eliminated|reduced|unchanged]</residual_risk>
      </mitigation>
    </risk>
    <!-- Additional risks -->
  </risks>

  <summary>
    <total_risks>[count]</total_risks>
    <risk_profile>[very_high|high|moderate|low|very_low]</risk_profile>
    <top_risks>
      <ref risk_id="R1"/>
      <ref risk_id="R2"/>
      <ref risk_id="R3"/>
    </top_risks>
    <go_no_go_assessment>[proceed|proceed_with_caution|significant_concerns|do_not_proceed]</go_no_go_assessment>
    <key_assumptions>
      <assumption id="A1" confidence="[value]" status="[status]">[statement]</assumption>
    </key_assumptions>
    <recommendation>[narrative recommendation]</recommendation>
  </summary>
</risk_assessment>
```

**See:** `templates/risk-assessment-output.md` for complete template with guidance.

### 9.2 Secondary Output: Assumption Inventory

```xml
<assumption_inventory>
  <metadata>
    <subject_reference>[what was analyzed]</subject_reference>
    <total_assumptions>[count]</total_assumptions>
    <validation_coverage>[percentage validated]</validation_coverage>
  </metadata>

  <assumptions>
    <assumption id="A1">
      <type>[EXPLICIT|IMPLICIT|STRUCTURAL|LOAD-BEARING|CONTEXTUAL|BEHAVIORAL]</type>
      <statement>[clear, falsifiable statement]</statement>
      <source>[how it was identified]</source>
      <confidence>[0.0-1.0]</confidence>
      <epistemic_label>[VERIFIED|LIKELY|POSSIBLE|SPECULATIVE|UNKNOWN]</epistemic_label>
      <load_bearing_score>[priority score]</load_bearing_score>
      <validation_status>[VALIDATED|PARTIAL|UNVALIDATED|INVALIDATED|CONTESTED]</validation_status>
      <validation_method>[methods used]</validation_method>
      <dependencies>
        <ref>[what depends on this]</ref>
      </dependencies>
      <invalidation_triggers>
        <trigger>[what would make this false]</trigger>
      </invalidation_triggers>
    </assumption>
    <!-- Additional assumptions -->
  </assumptions>
</assumption_inventory>
```

**See:** `templates/assumption-inventory-output.md` for complete template.

### 9.3 Secondary Output: Sensitivity Analysis

```xml
<sensitivity_analysis>
  <metadata>
    <subject_reference>[what was analyzed]</subject_reference>
    <assumptions_analyzed>[count]</assumptions_analyzed>
  </metadata>

  <scenarios>
    <scenario assumption_id="A1">
      <what_if>[Assumption A1 is FALSE]</what_if>
      <immediate_impacts>
        <impact>[description]</impact>
      </immediate_impacts>
      <cascade_effects>
        <effect>[description]</effect>
      </cascade_effects>
      <decision_change>[would decision change? how?]</decision_change>
      <impact_magnitude>[negligible|minor|moderate|major|catastrophic]</impact_magnitude>
    </scenario>
    <!-- Additional scenarios -->
  </scenarios>

  <summary>
    <decision_robustness_score>[0-100]</decision_robustness_score>
    <most_sensitive_assumptions>
      <ref assumption_id="A3"/>
      <ref assumption_id="A7"/>
    </most_sensitive_assumptions>
    <robustness_assessment>[narrative]</robustness_assessment>
  </summary>
</sensitivity_analysis>
```

**See:** `templates/sensitivity-analysis-output.md` for complete template.

---

## 10. Quality Gates

| # | Gate | Criterion | Phase |
|---|------|-----------|-------|
| 1 | **Subject Framed** | Subject boundaries and context explicit | 1 |
| 2 | **All Explicit Captured** | Document scan for assumption markers complete | 2 |
| 3 | **Implicit Probe Done** | At least N surfacing techniques applied (per intensity) | 2 |
| 4 | **Structural Check** | Frame questioning performed (if full_structural) | 2 |
| 5 | **Types Assigned** | Every assumption has type classification | 3 |
| 6 | **Load-Bearing Identified** | Top N critical assumptions flagged | 3 |
| 7 | **Priority Scores** | All assumptions have priority scores | 3 |
| 8 | **Top N Validated** | Top assumptions have validation results | 4 |
| 9 | **Counterfactuals Run** | What-if scenarios for load-bearing assumptions | 4 |
| 10 | **Confidence Calibrated** | All assumptions have epistemic labels | 4 |
| 11 | **Risks Derived** | Assumption-derived risks enumerated | 5 |
| 12 | **Go/No-Go Issued** | Assessment concludes with recommendation | 5 |

### Gate Requirements by Intensity

| Gate | Light | Standard | Rigorous |
|------|-------|----------|----------|
| Surfacing techniques | 2 | 4 | All |
| Load-bearing flagged | 3 | 5 | All scoring > 1.0 |
| Assumptions validated | 3 | 5 | All load-bearing |
| Counterfactuals | Top 1 | Top 3 | All load-bearing |

---

## 11. Workflow Integration

### Upstream Skills

| Skill | Provides | Use Case |
|-------|----------|----------|
| `research-interviewer` | KNOWLEDGE-CORPUS | When subject knowledge needs elicitation first |
| `expert-panel-deliberation` | Multi-perspective input | When diverse expert views inform assumptions |
| `create-research-brief` | Research synthesis | When external research informs assumptions |

### Downstream Skills

| Skill | Receives | Use Case |
|-------|----------|----------|
| `expert-panel-deliberation` | RISK-ASSESSMENT | For panel review of identified risks |
| `generate-ideas` | Assumption gaps | To generate alternatives when assumptions fail |

### Skill Chaining Example

```
research-interviewer      → KNOWLEDGE-CORPUS
                               ↓
assumption-validator      → RISK-ASSESSMENT
                               ↓
expert-panel-deliberation → Validated risk mitigation plan
```

---

## 12. Behavioral Guidelines

### Approach Principles

- **Curious, not adversarial:** Surface assumptions to understand, not to attack
- **Humble about certainty:** Calibrate confidence honestly; overconfidence is dangerous
- **Specific, not vague:** Each assumption should be falsifiable
- **Proportionate effort:** Match validation depth to decision stakes
- **Actionable output:** Every finding should inform a decision or action
- **Transparent reasoning:** Show how assumptions connect to risks
- **Constructive framing:** Present findings to enable better decisions, not to criticize

### Tone Calibration by Intensity

| Intensity | Tone |
|-----------|------|
| **Light** | Collaborative sanity check; quick scan for obvious gaps |
| **Standard** | Thorough review; balanced coverage of key assumptions |
| **Rigorous** | Adversarial stress-test; leave no stone unturned |

### Communication Guidelines

- State assumptions as falsifiable propositions, not vague concerns
- Distinguish between "unvalidated" (unknown) and "invalidated" (known false)
- When confidence is low, say so explicitly
- Provide evidence for validation claims
- Recommend specific actions, not just flag risks

---

## 13. References

| Document | Purpose |
|----------|---------|
| `references/assumption-taxonomy.md` | Detailed type definitions, detection heuristics, examples |
| `references/surfacing-techniques.md` | Step-by-step protocols for 10+ surfacing techniques |
| `references/validation-methods.md` | 8+ validation approaches with cost-benefit analysis |
| `references/load-bearing-analysis.md` | Scoring framework and prioritization algorithm |
| `references/what-if-framework.md` | Structured counterfactual analysis protocol |
| `references/confidence-calibration.md` | Epistemic labeling and calibration techniques |

### Core Library References

| Library | Element | Usage |
|---------|---------|-------|
| `core/skill-patterns.yaml` | PATTERN-06: ADVERSARIAL-VALIDATE | Workflow pattern |
| `core/artifact-contracts.yaml` | CONTRACT-08: RISK-ASSESSMENT | Output format |
| `core/scoring-rubrics.yaml` | RUBRIC-06: CONFIDENCE-CALIBRATION | Epistemic labels |
| `core/scoring-rubrics.yaml` | RUBRIC-07: SEVERITY-SCORING | Risk scoring |
| `core/technique-taxonomy.yaml` | CAT-UR, CAT-MC, CAT-SD | Reasoning techniques |

---

## 14. Templates

| Template | Purpose |
|----------|---------|
| `templates/risk-assessment-output.md` | CONTRACT-08 compliant RISK-ASSESSMENT XML |
| `templates/assumption-inventory-output.md` | Structured assumption catalog |
| `templates/sensitivity-analysis-output.md` | What-if impact analysis |

---

## 15. Examples

### Example 1: Decision Validation — Microservices Migration

```yaml
input:
  subject: "Decision to migrate from monolith to microservices architecture"
  subject_type: architecture
  validation_intensity: rigorous
  assumption_depth: full_structural
  counterfactual_analysis: true
  time_horizon: long_term

flow:
  phase_1:
    framing: "Validate assumptions in architecture migration decision"
    scope: "Technical, organizational, and timeline assumptions"
    stakeholders: ["CTO", "Engineering leads", "Platform team"]

  phase_2:
    explicit_assumptions:
      - A1: "Current monolith cannot scale beyond 10K concurrent users"
      - A2: "Migration can be completed in 18 months"
      - A3: "Team has sufficient microservices expertise"
    implicit_assumptions:
      - A4: "Service boundaries are well-understood"
      - A5: "Operational complexity increase is manageable"
      - A6: "Data consistency requirements can be met with eventual consistency"
      - A7: "Deployment pipeline can be upgraded in parallel"
    structural_assumptions:
      - A8: "Microservices is the right architectural pattern for our needs"
      - A9: "We've correctly identified the performance bottleneck"
    total: 9 assumptions surfaced

  phase_3:
    classification:
      - A1: CONTEXTUAL, LOAD-BEARING (everything depends on this being true)
      - A2: BEHAVIORAL (team velocity assumption)
      - A3: BEHAVIORAL, LOAD-BEARING (critical capability)
      - A8: STRUCTURAL (framing assumption)
    load_bearing_analysis:
      - A1: Dependency=5, Reversibility=2, ValidationCost=2, Confidence=0.6 → Priority=4.0
      - A3: Dependency=5, Reversibility=3, ValidationCost=3, Confidence=0.4 → Priority=4.0
      - A8: Dependency=5, Reversibility=1, ValidationCost=4, Confidence=0.5 → Priority=3.1
    top_5: [A1, A3, A8, A2, A5]

  phase_4:
    validation_results:
      - A1: PARTIAL (load tests show 8K limit, but unclear if that's the monolith's fault)
           Confidence: 0.65, POSSIBLE
      - A3: UNVALIDATED (team has 1 person with production microservices experience)
           Confidence: 0.35, SPECULATIVE
      - A8: PARTIAL (alternatives like modular monolith not fully evaluated)
           Confidence: 0.55, POSSIBLE
    counterfactuals:
      - A3_FALSE: "Team lacks expertise"
        Impact: MAJOR (delays, quality issues, operational incidents)
        Decision change: Would need to hire or postpone
      - A8_FALSE: "Microservices isn't the right pattern"
        Impact: CATASTROPHIC (complete rework, wasted 18 months)
        Decision change: Would choose different architecture

  phase_5:
    risks_derived:
      - R1: "Team capability gap causes delivery failure" (from A3)
           Probability: high, Impact: major, Score: 3.4
      - R2: "Performance bottleneck not actually in monolith" (from A1, A9)
           Probability: medium, Impact: major, Score: 2.8
      - R3: "Microservices complexity exceeds operational capacity" (from A5)
           Probability: medium, Impact: moderate, Score: 2.1
    risk_profile: HIGH
    go_no_go: SIGNIFICANT_CONCERNS

output:
  risk_assessment:
    total_risks: 7
    critical_risks: 0
    high_risks: 2
    profile: HIGH
    recommendation: "SIGNIFICANT_CONCERNS - Do not proceed without addressing team
                     capability gap (A3). Consider hiring 2+ experienced engineers
                     or engaging architecture consultancy. Also evaluate modular
                     monolith alternative before committing to microservices (A8)."
  key_findings:
    - "Load-bearing assumption A3 (team expertise) is SPECULATIVE (confidence 0.35)"
    - "Structural assumption A8 (microservices is right) was not rigorously evaluated"
    - "If A3 is wrong, expect 6-12 month delays and quality issues"
```

---

### Example 2: Strategy Validation — European Market Entry

```yaml
input:
  subject: "Strategy to enter European market in Q3"
  subject_type: strategy
  validation_intensity: standard
  assumption_depth: include_implicit
  counterfactual_analysis: true
  time_horizon: medium_term

flow:
  phase_1:
    framing: "Validate assumptions in EU market entry strategy"
    scope: "Market, regulatory, operational, competitive assumptions"
    stakeholders: ["CEO", "VP Sales", "Legal", "Finance"]

  phase_2:
    explicit_assumptions:
      - A1: "EU market opportunity is $50M annually"
      - A2: "GDPR compliance achievable by Q2"
      - A3: "Can hire local sales team within 3 months"
    implicit_assumptions:
      - A4: "Brand will translate to EU market"
      - A5: "Pricing model works in EU (different from US)"
      - A6: "No significant competitive response for 6 months"
      - A7: "Payment infrastructure compatible with EU systems"
    total: 7 assumptions surfaced

  phase_3:
    load_bearing_analysis:
      - A2: Dependency=5, ValidationCost=3, Confidence=0.4 → Priority=3.0 (LOAD-BEARING)
      - A6: Dependency=4, ValidationCost=4, Confidence=0.3 → Priority=2.1
      - A4: Dependency=4, ValidationCost=3, Confidence=0.5 → Priority=1.3
    top_5: [A2, A6, A1, A4, A5]

  phase_4:
    validation_results:
      - A2: PARTIAL - Legal says 6 months minimum, not 3 months
           Confidence: 0.50, POSSIBLE
      - A6: UNVALIDATED - No competitive intelligence conducted
           Confidence: 0.30, SPECULATIVE
      - A1: PARTIAL - $50M based on industry reports, not validated for our segment
           Confidence: 0.55, POSSIBLE
    counterfactuals:
      - A2_FALSE: "GDPR compliance takes 6+ months"
        Impact: MODERATE (Q3 launch becomes Q4 or later)
      - A6_FALSE: "Competitor responds immediately"
        Impact: MAJOR (first-mover advantage lost, pricing pressure)

  phase_5:
    risks_derived:
      - R1: "GDPR timeline slip delays launch" (from A2)
      - R2: "Competitive response erodes market opportunity" (from A6)
      - R3: "Market opportunity overestimated" (from A1)
    risk_profile: MODERATE
    go_no_go: PROCEED_WITH_CAUTION

output:
  risk_assessment:
    profile: MODERATE
    recommendation: "PROCEED_WITH_CAUTION - Adjust timeline to Q4 to allow GDPR buffer.
                     Conduct competitive intelligence before launch. Validate market
                     size with primary research in target segments."
```

---

### Example 3: Architecture Choice — Event Sourcing

```yaml
input:
  subject: "Use event sourcing for transaction processing system"
  subject_type: architecture
  validation_intensity: standard
  assumption_depth: include_implicit
  counterfactual_analysis: true
  time_horizon: long_term

flow:
  phase_1:
    framing: "Validate assumptions in event sourcing architecture choice"
    scope: "Technical capabilities, team skills, operational requirements"

  phase_2:
    explicit_assumptions:
      - A1: "Full audit trail is a regulatory requirement"
      - A2: "Query patterns are primarily temporal (time-series)"
      - A3: "Event schema will remain stable"
    implicit_assumptions:
      - A4: "Team can learn event sourcing patterns effectively"
      - A5: "Eventual consistency acceptable for all use cases"
      - A6: "Read model rebuild time acceptable in failure scenarios"
    total: 6 assumptions surfaced

  phase_3:
    load_bearing_analysis:
      - A1: Dependency=5, Confidence=0.9 → Priority=0.6 (VALIDATED)
      - A5: Dependency=4, Confidence=0.5 → Priority=2.0
      - A4: Dependency=3, Confidence=0.6 → Priority=1.2
    top_5: [A5, A6, A4, A2, A3]

  phase_4:
    validation_results:
      - A1: VALIDATED - Regulatory docs confirm audit requirement
           Confidence: 0.95, VERIFIED
      - A5: PARTIAL - Finance team needs strong consistency for reconciliation
           Confidence: 0.60, POSSIBLE
      - A4: LIKELY - Team has completed event sourcing training
           Confidence: 0.75, LIKELY
    counterfactuals:
      - A5_FALSE: "Some use cases need strong consistency"
        Impact: MODERATE (need CQRS pattern, adds complexity)

  phase_5:
    risk_profile: LOW
    go_no_go: PROCEED

output:
  risk_assessment:
    profile: LOW
    recommendation: "PROCEED - Core requirement (A1) validated. Implement CQRS pattern
                     to handle strong consistency requirements for finance (A5).
                     Continue team training program."
```

---

## 16. Quick Start

### Minimal Invocation

```
Validate assumptions in: [paste decision/strategy/plan]
```

### Standard Invocation

```
subject_type: decision
validation_intensity: standard
assumption_depth: include_implicit

Subject: [description or document]
```

### Full Parameter Invocation

```
subject_type: strategy
validation_intensity: rigorous
assumption_depth: full_structural
counterfactual_analysis: true
confidence_threshold: 0.8
time_horizon: long_term

Subject: [detailed description or document reference]

Additional context:
- Stakeholders: [who should be consulted]
- Time constraint: [when is decision needed]
- Protected assumptions: [any executive mandates]
```
