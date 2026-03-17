---
name: root-cause-analysis
description: "Structured root cause analysis for software, data quality, AI/ML, and legal/compliance incidents. Use when investigating failures, writing postmortems, analysing breaches, or building corrective action plans. Triggers on: RCA, root cause, postmortem, incident, failure analysis, breach investigation, corrective action, CAPA, 5 whys."
version: "1.0"
tier: domain
token_budget: 4000
requires: []
---

# Root Cause Analysis (RCA) Skill

Structured methodology for investigating failures across software engineering, data quality, AI/ML systems, and UK legal/regulatory compliance. Combines Google SRE blameless postmortem culture, FCA/TPR regulatory expectations, ISO 37301/42001 standards, and CAPA discipline into a single executable framework.

---

## When To Use

**Trigger conditions:**
- A system failure, outage, or degraded service has occurred
- Data quality issues discovered in a pipeline or knowledge graph
- AI/ML system produced incorrect, hallucinated, or harmful output
- A regulatory breach or compliance nonconformity is identified
- User requests a postmortem, RCA, failure analysis, or incident review
- Pipeline stage failure rate drops below threshold (e.g., 90%)
- Action items from a previous RCA need tracking or review

**Severity threshold:** Use for any incident beyond a trivial one-off bug fix. If the failure could recur, affected users/data, or has regulatory implications, an RCA is warranted.

---

## Core Principles

1. **Blameless by default.** Focus on systems, not individuals. When human error appears, investigate the systems that allowed it. Reference roles ("the on-call engineer"), not names.
2. **Contributing factors, not singular root cause.** Complex systems fail from intersecting conditions (Swiss Cheese Model). Identify all contributing factors; classify each as root cause, contributing factor, or mitigator.
3. **Systemic thinking.** Look beyond the immediate trigger to governance, process, tooling, and culture. The same root cause can surface through different contributing factors across separate incidents.
4. **Document for posterity.** Every RCA must produce a tamper-evident record that satisfies both internal learning and external regulatory scrutiny (FCA, TPR, PRA).
5. **Close the loop.** An RCA without tracked corrective actions is waste. 60% of post-incident action items never get completed (industry average). Every action item must have an owner, a deadline, and a verification step.

---

## Step 0: Classify the Incident

Before starting analysis, classify the incident type and severity. This determines which methodology path to follow and what regulatory obligations may apply.

### Incident Type

| Type | Description | Methodology Path |
|------|-------------|------------------|
| **Software** | System outage, degraded service, deployment failure | SRE Postmortem (Section A) |
| **Data Quality** | Pipeline failure, incorrect data, missing records, schema drift | Data Quality RCA (Section B) |
| **AI/ML** | Hallucination, bias, drift, grounding failure, confabulation | AI Incident Analysis (Section C) |
| **Legal/Compliance** | Regulatory breach, nonconformity, governance failure | Compliance Investigation (Section D) |
| **Hybrid** | Crosses multiple types (e.g., AI hallucination causing compliance breach) | Use primary type + supplementary sections |

### Severity Classification

Assess across four dimensions. The highest dimension determines overall severity.

| Dimension | Critical (SEV-1) | Major (SEV-2) | Moderate (SEV-3) | Minor (SEV-4) |
|-----------|-------------------|----------------|-------------------|----------------|
| **User/Member Impact** | All users, complete outage | Most users, degraded | Subset of users | Individual users |
| **Data Integrity** | Loss, corruption, or exposure | Integrity risk, no loss | No data impact | No data impact |
| **Regulatory** | Reportable breach (TPR/FCA) | Significant deficiency | Minor nonconformity | Observation only |
| **Financial** | Direct loss or compensation | Significant risk | Minimal | None |
| **Response** | All-hands, exec/SMF notification | Full incident team | Team lead + on-call | Standard ticket |

**Rule:** If unsure between two levels, treat as the higher one.

**Regulatory reporting triggers:**
- TPR: Breach likely to be of material significance (General Code) -- report within 10 working days
- FCA: PRIN 11 (relations with regulators) -- notify without delay for significant issues
- PRA: Operational incident exceeding impact tolerance thresholds (SS1/21, CP17/24)

---

## Step 1: Gather Evidence and Build Timeline

### Data Sources

Collect from all available sources before analysis begins:

| Source | What to Capture |
|--------|----------------|
| **Logs/Monitoring** | Error logs, metric anomalies, alert triggers, dashboard screenshots |
| **Deployment/Config** | Recent changes, PRs merged, config updates, feature flag changes |
| **Communication** | Slack messages, email threads, incident channel, call transcripts |
| **Pipeline** | Audit log entries (`pipeline_audit.jsonl`), stage outputs, hash chain verification |
| **Review Queue** | Flagged items (`review_queue.jsonl`), pending/resolved items |
| **User Reports** | Complaints, support tickets, member communications |

### Timeline Format

Use UTC timestamps. Tag each entry with a category:

```
HH:MM UTC - [CATEGORY] Description [Actor/System]

Categories: DETECTION | ESCALATION | DIAGNOSIS | MITIGATION | COMMUNICATION | RESOLUTION | DEPLOYMENT
```

### Seven Key Timestamps (AWS pattern)

Always capture these minimum timestamps to calculate response intervals:

| # | Timestamp | Interval Calculated |
|---|-----------|---------------------|
| 1 | Last deployment/config change | -- |
| 2 | Incident start (actual, may be before detection) | -- |
| 3 | Detection (alert fired or reported) | Time to Detect (3-2) |
| 4 | First responder engaged | Time to Engage (4-3) |
| 5 | Root cause identified | Time to Diagnose (5-4) |
| 6 | Mitigation applied | Time to Mitigate (6-5) |
| 7 | Incident resolved | Time to Resolve (7-2) |

---

## Step 2: Analyse Contributing Factors

### 2a. Ishikawa Categories (adapted for software/legal)

Systematically explore each category. Not all will apply to every incident.

| Category | Software/DevOps | Legal/Compliance |
|----------|-----------------|------------------|
| **People** | Skill gaps, fatigue, understaffing, miscommunication | Training gaps, SMF accountability, delegation failures |
| **Process** | Missing runbooks, inadequate testing, unclear escalation | Policy gaps, governance deficiencies, reporting delays |
| **Technology** | Software bugs, infrastructure failures, monitoring gaps | System of record failures, calculation errors, IT controls |
| **Data** | Schema drift, data quality, pipeline failures, missing records | Incomplete member records, incorrect calculations, stale data |
| **Environment** | Network, cloud region, config, third-party dependencies | Regulatory changes, market conditions, scheme events |
| **Governance** | Missing review gates, insufficient oversight | ESOG gaps, committee oversight, internal controls |

### 2b. Five Whys Chain

For each identified contributing factor, drill to the systemic root:

```
Problem: [Describe the observed failure]
Why 1: [Proximate cause -- what directly caused the failure?]
Why 2: [Process gap -- why was that possible?]
Why 3: [Systemic factor -- why does the process have that gap?]
Why 4: [Governance/cultural -- why hasn't the systemic factor been addressed?]
Why 5: [Root cause -- what underlying assumption or structure allows this?]
```

**Stopping rule:** If your candidate root cause can be preceded by another "why" that is actionable, you haven't gone deep enough. If fixing the identified cause would permanently prevent this class of failure, you've found the root.

**Common failure patterns from experience:**
- Stopping at "human error" without investigating the system that permitted it
- Confusing symptoms (server OOM) with root causes (no memory limits configured)
- Accepting the first plausible explanation without testing alternatives

### 2c. Classify Each Factor

| Role | Definition | Action |
|------|------------|--------|
| **Root Cause** | Primary trigger; if removed, prevents this class of incident | Must have a preventive action item |
| **Contributing Factor** | Worsened impact or delayed resolution | Should have a mitigation action item |
| **Mitigator** | Reduced impact; was a defence that partially worked | Should be strengthened |

### 2d. Rank Factors

Score each factor on three dimensions (1-5 scale):

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| **Impact** | Negligible effect on severity | Moderate contribution | Primary driver of severity |
| **Recurrence Likelihood** | Unlikely without intervention | Possible | Near-certain |
| **Remediation Cost** | Trivial fix | Moderate effort | Major initiative |

Priority = Impact x Recurrence Likelihood (remediation cost informs scheduling, not priority).

---

## Step 3: Determine Corrective and Preventive Actions

### Action Item Types (CAPA framework)

| Type | Purpose | Example |
|------|---------|---------|
| **Detect** | Find issues faster | Add monitoring alert for pipeline failure rate |
| **Prevent** | Eliminate root cause | Insert Stage 5.5 quality gate between extraction and verification |
| **Mitigate** | Reduce impact if recurrence | Add circuit breaker / confidence downgrade on flagged items |
| **Process** | Improve response procedures | Update runbook, add escalation path to review queue |
| **Document** | Capture knowledge | Update Memory MCP, create anti-pattern entry |

### Action Item Requirements

Every action item MUST have:

```yaml
- id: "AI-01"
  description: "Specific, actionable description"
  type: "detect | prevent | mitigate | process | document"
  owner: "Named individual (not a team)"
  due_date: "YYYY-MM-DD"
  urgency: "critical | high | medium | low"
  tracker: "JIRA/Linear/GitHub issue URL"
  acceptance_criteria:
    - "Measurable condition that proves completion"
  status: "open | in_progress | blocked | complete"
```

### Urgency SLAs

| Urgency | SLA | Trigger |
|---------|-----|---------|
| **Critical** | 3 days | Immediate risk of recurrence or regulatory exposure |
| **High** | 14 days | Significant reliability or compliance improvement |
| **Medium** | 30 days | Hardening measure, no immediate risk |
| **Low** | 90 days | Long-term enhancement, documentation |

---

## Step 4: Produce the RCA Report

### Report Template

```markdown
# Root Cause Analysis: [Title]

**RCA ID:** RCA-YYYY-MM-DD-NNN
**Date:** YYYY-MM-DD
**Authors:** [Names]
**Status:** Draft | In Review | Final
**Severity:** Critical | Major | Moderate | Minor
**Type:** Software | Data Quality | AI/ML | Compliance | Hybrid

---

## Summary

[2-3 sentence plain-language description of what happened, quantified impact]

## Impact Assessment

| Metric | Value |
|--------|-------|
| Duration | [minutes/hours] |
| Users/Members Affected | [count or percentage] |
| Data Records Affected | [count] |
| Financial Impact | [amount or "none"] |
| SLA/SLO Breaches | [count] |
| Regulatory Reporting Required | Yes/No |

## Timeline

| Time (UTC) | Category | Event |
|------------|----------|-------|
| HH:MM | DEPLOYMENT | [Description] |
| HH:MM | DETECTION | [Description] |
| ... | ... | ... |

**Response Intervals:**
- Time to Detect: [X minutes]
- Time to Engage: [X minutes]
- Time to Mitigate: [X minutes]
- Time to Resolve: [X minutes]

## Contributing Factors

### CF-01: [Factor Name] -- ROOT CAUSE
**Category:** [People | Process | Technology | Data | Environment | Governance]

**Five Whys:**
1. Why: [Answer]
2. Why: [Answer]
3. Why: [Answer]
4. Why: [Answer]
5. Why: [Answer]

**Evidence:** [What data supports this conclusion]

### CF-02: [Factor Name] -- CONTRIBUTING
[Same structure]

## Lessons Learned

### What Went Well
- [Item]

### What Went Wrong
- [Item]

### Where We Got Lucky
- [Item]

## Action Items

| ID | Description | Type | Owner | Due | Status |
|----|-------------|------|-------|-----|--------|
| AI-01 | [Specific action] | Prevent | [Name] | YYYY-MM-DD | Open |
| AI-02 | [Specific action] | Detect | [Name] | YYYY-MM-DD | Open |

## Audit Trail

- Pipeline audit chain: [VALID/INVALID] ([N] entries)
- Review queue chain: [VALID/INVALID] ([N] entries)
- RCA hash: [SHA-256 of this document]

---

**Sign-off:** [Author], [Date]
```

---

## Section A: Software Incident RCA

### Four Diagnostic Questions (AWS pattern)

After completing the contributing factor analysis, answer these:

1. **Detection:** Could we have detected this faster? What monitoring, alerting, or observability changes would reduce TTD?
2. **Diagnosis:** Could we have diagnosed this faster? What runbooks, dashboards, or tooling would reduce TTD?
3. **Mitigation:** Could we have mitigated this faster? What circuit breakers, rollback mechanisms, or failover would reduce TTM?
4. **Prevention:** Can we prevent recurrence? What architectural, process, or governance changes address the root cause?

### Software-Specific Factors

| Factor | Common Root Causes |
|--------|--------------------|
| Deployment failure | Missing staging environment, inadequate CI/CD gates, config drift |
| Monitoring gap | Alert fatigue, missing coverage, threshold miscalibration |
| Cascade failure | Missing circuit breakers, tight coupling, no graceful degradation |
| Data corruption | Schema migration error, race condition, missing validation |

---

## Section B: Data Quality RCA

### Data Quality Dimensions

Assess which dimensions were violated:

| Dimension | Question | Detection Method |
|-----------|----------|------------------|
| **Completeness** | Are all expected records present? | Count validation, NULL checks |
| **Accuracy** | Do values match the authoritative source? | NLI verification, grounding checks |
| **Consistency** | Are values consistent across systems? | Cross-reference validation |
| **Timeliness** | Is data current as of the expected date? | Freshness monitoring |
| **Uniqueness** | Are there unexpected duplicates? | Deduplication checks |
| **Validity** | Do values conform to expected formats/ranges? | Schema validation, regex patterns |

### Pipeline Failure Investigation

For pipeline-specific failures (e.g., Stage 5/5.5/6/7):

1. **Identify the failure point** -- Which stage failed? What was the input vs expected output?
2. **Check upstream data** -- Was the input to the failing stage correct?
3. **Verify transformations** -- Did any intermediate step corrupt or lose data?
4. **Check for duplicates** -- Use `head(collect(v))` pattern to handle multiple `DERIVES_FROM_VERSION` rows
5. **Validate against audit log** -- Cross-reference `pipeline_audit.jsonl` hash chain
6. **Check review queue** -- Were items flagged but not routed to the review queue?

### Data Quality RCA-Specific Actions

| Pattern | Root Cause | Corrective Action |
|---------|------------|-------------------|
| Non-entity stakeholders ("P", "Regulations") | LLM treated instruments/shorthand as actors | Remap table in QC stage (Stage 5.5 pattern) |
| Grounding failures (<30% overlap) | Extraction doesn't match source text | NLI verification gate, confidence downgrade |
| Duplicate records | Missing deduplication in Cypher query | `head(collect(v))` deduplication pattern |
| Missing audit trail | Review queue not wired to failing stage | Wire all failure-producing stages to review queue |

---

## Section C: AI/ML Incident Analysis

### AI Failure Classification

| Type | Description | Severity Modifier |
|------|-------------|-------------------|
| **Hallucination** | Factually incorrect output presented as fact | +1 severity if in regulated domain |
| **Confabulation** | Plausible-sounding but nonexistent citations/references | +1 severity if used for legal advice |
| **Grounding Failure** | Output not supported by retrieved context (RAG) | Check retrieval pipeline first |
| **Bias** | Systematic unfairness in outputs across demographics | Potential regulatory breach (EA 2010) |
| **Data Drift** | Training/production distribution mismatch | Monitor with statistical tests |
| **Concept Drift** | Relationship between inputs and target has changed | Requires model retraining assessment |

### AI-Specific Contributing Factors

Extend the Ishikawa categories with:

| Category | AI-Specific Factors |
|----------|---------------------|
| **Model** | Training data bias, knowledge cutoff, temperature settings, prompt design |
| **Retrieval** | Irrelevant context, missing documents, embedding drift, index staleness |
| **Grounding** | No verification gate, bag-of-words instead of NLI, insufficient overlap threshold |
| **Governance** | No human-in-the-loop, missing AI system inventory, unclear accountability |

### AI RCA Supplementary Section

Add to the report template:

```markdown
## AI/ML Supplementary Analysis

### Model Identification
- Model: [name, version, provider]
- Training cutoff: [date]
- Guardrails: [list active filters/gates]

### Failure Classification
- Type: [Hallucination | Confabulation | Grounding | Bias | Drift]
- Scope: [Single output | Pattern | Systemic]

### Grounding Assessment
- Was output grounded in retrieved context? [Yes/No/Partial]
- Citation validity: [All valid | Some invalid | Fabricated]
- Verification method used: [NLI | Bag-of-words | Manual | None]

### Rigor Classification (Task-Aware)
- Task type: [Statutory claim | Obligation extraction | Navigation | Database query | Exploration | Overview]
- Required rigor: [Ultra-high | High | Medium | Low]
- Actual rigor applied: [Level]
- Gap: [Description if rigor was insufficient]
```

### Key Anti-Pattern: Bag-of-Words Verification

**NEVER** use cosine similarity or word overlap for semantic verification in legal/compliance contexts. Example failure:
- Source: "must NOT invest"
- Extraction: "must invest"
- Word overlap: 90% -- FALSE PASS

**Always use NLI** (Natural Language Inference) with entailment confidence >0.9 for legal correctness.

---

## Section D: Compliance Investigation RCA

### UK Regulatory Framework

This section applies when the incident has regulatory implications under FCA, PRA, or TPR rules.

### FCA Root Cause Analysis Requirements (DISP App 3.4)

The FCA mandates a four-stage progression:

1. **Symptom Identification** -- Management information showing patterns (complaint spikes, service failures, data anomalies)
2. **Initial Investigation** -- Detailed technical/operational inquiry into the fault
3. **Root Cause Analysis** -- Move beyond the immediate fault to systemic weaknesses in governance, systems, and controls
4. **Preventative and Remedial Actions** -- Corrective measures addressing the root cause, including governance restructuring, enhanced testing, and customer remediation

### FCA Root Cause Classification (ORX Taxonomy)

Classify root causes using the Basel/ORX operational risk categories:

| Category | Sub-Categories |
|----------|----------------|
| **People** | Skills, conduct, capacity, training, communication |
| **Process** | Design, execution, documentation, change management |
| **Systems** | IT failure, data quality, calculation error, interface |
| **External** | Vendor failure, regulatory change, market event, fraud |

### TPR Breach Materiality Assessment

When a pension scheme breach is identified, assess materiality across three dimensions:

**Causation:** Was it caused by dishonesty, negligence, reckless behaviour, poor governance, deficient administration, or incomplete guidance?

**Impact:** Does it affect significant membership proportions, benefit calculations, governance competency, internal controls, or record-keeping?

**Response:** Was the investigation prompt and effective? (Reduces materiality.) Was there delay or failure to notify? (Elevates materiality.)

**Reporting deadline:** Most cases within 10 working days to TPR.

### SMCR Accountability Mapping

For FCA-regulated firms, every RCA must identify:

```markdown
### SMCR Accountability
- **Accountable SMF:** [SMF role holder for the affected area]
- **Statement of Responsibilities:** [Reference to SoR section]
- **Reasonable Steps Evidence:**
  - [ ] Management information was reviewed
  - [ ] Escalation occurred promptly
  - [ ] Corrective action was implemented
  - [ ] Delegation was appropriate with oversight
  - [ ] Decision rationale was documented
```

### ISO 37301 Corrective Action Requirements

For compliance management system nonconformities:

1. React and control -- contain immediately
2. Address consequences -- manage compliance breaches or downstream harm
3. Investigate root cause -- systematic analysis (this RCA)
4. Implement corrective action -- eliminate root cause, not just symptom
5. Verify effectiveness -- confirm corrective action prevents recurrence
6. Document everything -- retain records of nonconformity, analysis, actions, and outcomes

### ISO 42001 AI Incident Requirements

For AI management system incidents:

1. Develop playbooks for responding to AI incidents (harmful outputs, bias, security breaches)
2. Enable logging and traceability at appropriate lifecycle phases
3. Detect system performance outside intended operating conditions
4. Update AI risk register if the incident reveals new risks
5. Document assumptions that were violated

---

## Step 4b: Recursive Language Model (RLM) Verification Layer

An additional verification pass where the model recursively interrogates its own RCA analysis. This catches shallow reasoning, confirmation bias, and logical gaps that a single-pass analysis misses. Based on the recursive decomposition pattern from the RLM agent architecture.

### Purpose

The RLM layer treats the draft RCA as an input document and subjects it to adversarial scrutiny across multiple dimensions. Each verification pass may trigger a recursive refinement cycle. The model acts as both analyst and red-team reviewer.

### RLM Verification Protocol

Execute these five verification passes sequentially. Each pass produces a verdict: **PASS**, **WEAK** (needs strengthening), or **FAIL** (analysis is flawed, must revise before finalising).

#### Pass 1: Causal Chain Integrity

Verify the logical coherence of each Five Whys chain.

```
For each contributing factor's Five Whys chain:

1. FORWARD TEST: Read Why 1 → Why 5 sequentially.
   - Does each "why" logically follow from the previous answer?
   - Are there logical leaps or unsupported assumptions?
   - Flag any step where the causal link is asserted without evidence.

2. REVERSE TEST: Read Why 5 → Why 1 (root → symptom).
   - If the root cause (Why 5) were eliminated, would each subsequent
     "why" in the chain also be resolved?
   - If not, the chain has a broken link — the root cause is insufficient.

3. ALTERNATIVE PATH TEST: For each "why" answer, ask:
   - "Is there a different, equally plausible answer to this why?"
   - If yes, the analysis may have prematurely converged on one
     causal chain. Branch and explore the alternative.

4. DEPTH TEST: For the identified root cause (Why 5), ask one more "why":
   - If the answer is actionable and non-trivial, the analysis
     stopped too early. Add Why 6 and re-evaluate.
   - If the answer is philosophical, organisational culture, or
     "the nature of software", the depth is sufficient.
```

**Verdict criteria:**
- PASS: All chains survive forward, reverse, alternative, and depth tests
- WEAK: One chain has a plausible alternative path not explored
- FAIL: A chain has a broken reverse link (root cause doesn't explain symptom)

#### Pass 2: Contributing Factor Completeness

Verify that the Ishikawa analysis hasn't missed obvious categories.

```
For each Ishikawa category (People, Process, Technology, Data, Environment, Governance):

1. Was this category explicitly considered?
   - If dismissed, is the dismissal justified?

2. COUNTERFACTUAL TEST: For each identified contributing factor, ask:
   - "If only this factor were present and all others were absent,
     would the incident still have occurred?"
   - If YES for any single factor → that factor is sufficient
     (likely the root cause)
   - If NO for all factors → the incident required multiple conditions
     (Swiss Cheese Model applies; document the combination)

3. ABSENCE TEST: For each category NOT identified as contributing:
   - "Could a failure in [category] have worsened detection,
     diagnosis, or resolution time?"
   - If yes, add as a contributing factor even if not causal.

4. HISTORICAL PATTERN CHECK:
   - Search Memory MCP for similar past incidents:
     mcp__memory__search_nodes query: "[incident type] lesson"
   - Do historical patterns suggest a factor category that
     this analysis overlooked?
```

**Verdict criteria:**
- PASS: All 6 categories considered, counterfactuals tested, no gaps
- WEAK: One category dismissed without justification
- FAIL: A clearly relevant category was not considered at all

#### Pass 3: Action Item Sufficiency

Verify that corrective actions actually address root causes.

```
For each root cause / contributing factor:

1. COVERAGE TEST: Is there at least one action item that
   directly addresses this factor?
   - Root causes MUST have a "prevent" type action
   - Contributing factors SHOULD have a "mitigate" or "detect" action

2. SPECIFICITY TEST: For each action item, ask:
   - "If I handed this action item to someone with no context,
     could they implement it?"
   - Reject vague items: "improve monitoring" → FAIL
   - Accept specific items: "Add alerting rule for Stage 7
     failure rate <95% in Grafana dashboard X" → PASS

3. RECURRENCE TEST: For each "prevent" action item, ask:
   - "After implementing this action, could the exact same
     incident recur through a different path?"
   - If yes, the action addresses a symptom, not the root cause.
     Either the root cause analysis is shallow, or additional
     preventive actions are needed.

4. SIDE EFFECT TEST: For each action item, ask:
   - "Could implementing this action introduce new failure modes?"
   - Example: Adding a QC gate (Stage 5.5) could block legitimate
     obligations if the remap table is too aggressive.
   - Document mitigations for identified side effects.
```

**Verdict criteria:**
- PASS: All factors have specific, sufficient actions; recurrence test passes
- WEAK: Actions are specific but one root cause lacks a preventive action
- FAIL: Actions are vague, or a root cause has no corresponding action

#### Pass 4: Evidence and Reasoning Audit

Verify that conclusions are grounded in evidence, not assumptions.

```
For each factual claim in the RCA report:

1. GROUNDING TEST: Is the claim supported by:
   - Log data, monitoring output, or system records?
   - Audit trail entries (pipeline_audit.jsonl, review_queue.jsonl)?
   - Direct observation or reproduction of the failure?
   - If supported by none of the above, mark as UNVERIFIED ASSUMPTION.

2. CONFIRMATION BIAS TEST: List all evidence that CONTRADICTS
   the identified root cause. Ask:
   - "What evidence would I expect to see if the root cause
     were different?"
   - "Is that counter-evidence absent because it doesn't exist,
     or because I didn't look for it?"

3. NARRATIVE COHERENCE TEST: Read the RCA summary and ask:
   - "Does the narrative tell a coherent story from trigger
     to root cause to resolution?"
   - "Would a reader unfamiliar with the system understand
     what happened and why?"

4. REGULATORY EVIDENCE TEST (for compliance RCAs):
   - "Would this evidence satisfy an FCA/TPR/PRA examiner?"
   - "Are there gaps that a regulator would challenge?"
   - Apply the SMCR 'reasonable steps' standard:
     Is the evidence sufficient to demonstrate that oversight
     was adequate?
```

**Verdict criteria:**
- PASS: All claims grounded, counter-evidence explicitly addressed
- WEAK: 1-2 unverified assumptions, but non-critical to conclusions
- FAIL: Core conclusion rests on an unverified assumption

#### Pass 5: Recursive Decomposition Challenge

The final adversarial pass. Attempt to invalidate the entire RCA.

```
1. STEEL-MAN ALTERNATIVE: Construct the strongest possible
   alternative explanation for the incident that contradicts
   the identified root cause.
   - What evidence supports this alternative?
   - What evidence contradicts it?
   - If the alternative is equally plausible, the RCA is
     insufficiently discriminating — more investigation needed.

2. SCOPE CHALLENGE: Ask:
   - "Is the RCA scope too narrow? Could this incident be
     a symptom of a larger systemic issue not captured here?"
   - "Is the RCA scope too broad? Are we attributing multiple
     unrelated issues to a single root cause?"

3. TEMPORAL CHALLENGE: Ask:
   - "Could the timeline be wrong? Would a different sequence
     of events change the root cause identification?"
   - Verify that correlation has not been confused with causation.

4. SECOND-ORDER EFFECTS: Ask:
   - "What happens 6 months after all corrective actions are
     implemented? Are there second-order consequences?"
   - "Could the corrective actions create a false sense of
     security that reduces vigilance?"

5. META-ANALYSIS LINK: Ask:
   - "Does this RCA connect to patterns from previous RCAs?"
   - "If the same Ishikawa category keeps appearing across
     incidents, is there a meta-root-cause?"
```

**Verdict criteria:**
- PASS: Alternative explanation is weaker, scope is appropriate, no temporal confusion
- WEAK: Alternative is plausible but less well-supported
- FAIL: Alternative explanation is equally or more plausible

### RLM Verdict Summary

Record the results in the RCA report:

```markdown
## RLM Verification Results

| Pass | Test | Verdict | Notes |
|------|------|---------|-------|
| 1 | Causal Chain Integrity | PASS/WEAK/FAIL | [Brief note] |
| 2 | Contributing Factor Completeness | PASS/WEAK/FAIL | [Brief note] |
| 3 | Action Item Sufficiency | PASS/WEAK/FAIL | [Brief note] |
| 4 | Evidence and Reasoning Audit | PASS/WEAK/FAIL | [Brief note] |
| 5 | Recursive Decomposition Challenge | PASS/WEAK/FAIL | [Brief note] |

**Overall RLM Verdict:** [VALIDATED | NEEDS REVISION | REJECTED]

Scoring:
- VALIDATED: All passes PASS, or <=2 WEAK with no FAIL
- NEEDS REVISION: Any FAIL, or >=3 WEAK
- REJECTED: >=2 FAIL (RCA must be substantially reworked)
```

### Recursive Refinement Loop

If the RLM verdict is NEEDS REVISION or REJECTED:

```
1. For each FAIL/WEAK pass:
   a. Identify the specific deficiency
   b. Gather additional evidence or explore alternative hypotheses
   c. Revise the affected section of the RCA

2. Re-run ONLY the failed/weak passes (not the full RLM suite)

3. Maximum 3 refinement iterations:
   - Iteration 1: Address FAILs
   - Iteration 2: Address remaining WEAKs
   - Iteration 3: Final validation pass
   - If still not VALIDATED after 3 iterations:
     escalate for human review with explicit
     documentation of what remains unresolved

4. Each iteration is logged in the audit trail:
   log_stage(stage="rca_rlm", event="rlm_iteration",
     details={"iteration": N, "verdict": "...", "deficiencies": [...]})
```

### RLM in Practice: Worked Example

From the stakeholder remediation RCA:

**Pass 1 (Causal Chain Integrity):**
- Forward test: Each "why" logically follows -- PASS
- Reverse test: If the QC gate existed (Why 5 eliminated), extraction errors would be caught before Stage 7 -- PASS
- Alternative path: "Could the root cause be LLM prompt quality rather than a missing gate?" -- investigated; prompt quality is a contributing factor, but even with a perfect LLM, a QC gate is needed for defence in depth -- root cause stands
- Depth test: Why 6 for "why wasn't systematic testing done?" leads to "early-stage project with limited QA budget" -- organisational, not actionable at the technical level -- depth sufficient
- **Verdict: PASS**

**Pass 3 (Action Item Sufficiency):**
- Stage 5.5 insertion directly addresses root cause (missing gate) -- PASS
- Remap table addresses contributing factor (known bad patterns) -- PASS
- Side effect test: Could the remap table be too aggressive? -- Yes, "P" could be a valid stakeholder in some contexts. Mitigation: context-dependent remapping, not blanket replacement -- documented
- **Verdict: PASS** (with documented side effect mitigation)

**Pass 5 (Recursive Decomposition Challenge):**
- Steel-man alternative: "The root cause is that the LLM is fundamentally unreliable for stakeholder extraction, and a QC gate is just a workaround." -- This is valid as a contributing factor but not the root cause; the system must be designed to handle imperfect ML output (defence in depth). The QC gate is the correct architectural response.
- **Verdict: PASS**

**Overall: VALIDATED** (5 PASS, 0 WEAK, 0 FAIL)

---

## Step 5: Verify, Compound, and Close

### 5a. Quality Gates

Before finalising the RCA report:

- [ ] **Blamelessness Gate**: Report focuses on systems, not individuals
- [ ] **Depth Gate**: Five Whys reached systemic root cause (not just proximate)
- [ ] **Evidence Gate**: Every contributing factor has supporting evidence
- [ ] **Action Gate**: Every root cause/contributing factor has at least one action item
- [ ] **Ownership Gate**: Every action item has a named owner and due date
- [ ] **Audit Gate**: Hash chain verified (pipeline_audit.jsonl, review_queue.jsonl)
- [ ] **Regulatory Gate**: If reportable, notification timeline documented
- [ ] **PII Gate**: Personal data redacted from all stored records

### 5b. Audit Trail Integration

Write RCA events to the tamper-evident audit log:

```python
# Using existing audit_log.py infrastructure
from scripts.utils.audit_log import log_stage

log_stage(
    run_id=run_id,
    stage="rca",
    event="rca_completed",
    details={
        "rca_id": "RCA-2026-02-06-001",
        "severity": "moderate",
        "root_causes": ["missing_qc_gate"],
        "action_items": 4,
        "status": "final"
    }
)
```

### 5c. Compound to Memory MCP

After completing the RCA, persist learnings:

```
mcp__memory__create_entities
  entities: [{
    "name": "[Descriptive Pattern/Lesson Name]",
    "entityType": "lesson | anti-pattern | pattern",
    "observations": [
      "[Specific, actionable learning]",
      "[Root cause and fix applied]",
      "Discovered: RCA-YYYY-MM-DD-NNN"
    ]
  }]
```

Create relations to the affected project:
```
mcp__memory__create_relations
  relations: [{
    "from": "[lesson name]",
    "to": "[project name]",
    "relationType": "learned_during"
  }]
```

### 5d. Action Item Follow-Up

Schedule verification reviews:

| Urgency | First Review | Closure Review |
|---------|-------------|----------------|
| Critical | 3 days | 7 days |
| High | 14 days | 30 days |
| Medium | 30 days | 60 days |
| Low | 60 days | 90 days |

At each review:
1. Is the action item complete?
2. Has the corrective action been verified effective?
3. Has the issue recurred since implementation?
4. Should the action item be escalated or de-prioritised?

### 5e. Meta-Analysis

Periodically (quarterly or after 5+ RCAs), analyse across incidents:

- **Recurring themes**: Do the same Ishikawa categories keep appearing?
- **Action item completion rate**: Are corrective actions being implemented? (Target: >80%)
- **Recurrence rate**: Are resolved root causes staying resolved?
- **Response improvement**: Are TTD, TTM, TTR trending down?
- **Prevention vs detection ratio**: Are we investing more in prevention than firefighting?

---

## Anti-Patterns

| Pattern | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| Blame-focused RCA | People hide information; same failures recur | Focus on systems; reference roles not names |
| Stopping at proximate cause | Treats symptoms, not disease | Apply Five Whys to systemic level |
| Single root cause fixation | Misses interacting conditions in complex systems | Contributing factors model (Swiss Cheese) |
| RCA without action items | Analysis without change is waste | Every factor must have a corrective action |
| Orphaned action items | 60% of post-incident items never completed | Owner + deadline + tracker + verification |
| Bag-of-words verification | Misses semantic inversions ("must NOT" vs "must") | NLI with entailment >0.9 |
| Unreviewed postmortem | "Might as well never have existed" | Mandate peer review + team discussion |
| Analysis paralysis | Weeks of diagrams, no fixes | Time-box RCA to 5-7 business days |
| Treating each incident in isolation | Misses systemic patterns | Maintain incident database; quarterly meta-analysis |
| Regulatory checkbox RCA | FCA explicitly flags this as poor practice | Substantive analysis with measurable outcomes |

---

## Quick Reference: RCA Decision Tree

```
Incident Detected
    |
    v
[Step 0] Classify type and severity
    |
    v
[Step 1] Gather evidence, build timeline (7 key timestamps)
    |
    v
[Step 2] Analyse contributing factors
    |-- Ishikawa categories (People/Process/Technology/Data/Environment/Governance)
    |-- Five Whys for each factor
    |-- Classify: Root Cause / Contributing / Mitigator
    |-- Rank: Impact x Recurrence Likelihood
    |
    v
[Step 3] Define corrective actions (CAPA)
    |-- Type: Detect / Prevent / Mitigate / Process / Document
    |-- Owner + Due Date + Acceptance Criteria
    |
    v
[Step 4] Produce RCA report (template above)
    |
    v
[Step 4b] RLM Verification Layer (5 passes)
    |-- Pass 1: Causal Chain Integrity (forward/reverse/alternative/depth)
    |-- Pass 2: Contributing Factor Completeness (counterfactual/absence/history)
    |-- Pass 3: Action Item Sufficiency (coverage/specificity/recurrence/side-effect)
    |-- Pass 4: Evidence and Reasoning Audit (grounding/bias/narrative/regulatory)
    |-- Pass 5: Recursive Decomposition Challenge (steel-man/scope/temporal/meta)
    |-- Verdict: VALIDATED / NEEDS REVISION / REJECTED
    |-- If not VALIDATED: recursive refinement loop (max 3 iterations)
    |
    v
[Step 5] Verify, compound, close
    |-- Quality gates (8 checks)
    |-- Audit trail entry
    |-- Memory MCP compound
    |-- Schedule follow-up reviews
```

---

## Integration Points

### Existing Infrastructure
- **Audit Log**: `scripts/utils/audit_log.py` -- hash-chained JSONL at `data/audit/pipeline_audit.jsonl`
- **Review Queue**: `scripts/utils/review_queue.py` -- hash-chained JSONL at `data/audit/review_queue.jsonl`
- **Review CLI**: `scripts/review_cli.py` -- `list`, `summary`, `resolve`, `verify --audit`
- **RCA Reports**: `data/rca/` directory (gitignored)

### MCP Tools
- `mcp__memory__create_entities` -- persist lessons and anti-patterns
- `mcp__memory__add_observations` -- enrich existing entities with new learnings
- `mcp__memory__search_nodes` -- check for related historical RCAs
- `mcp__memory__create_relations` -- link lessons to projects and incidents

### Upstream Skills
- `compound-memory` -- feeds RCA learnings into knowledge graph
- `legislation-verification` -- verification gates for legal/compliance RCAs
- `output-verification` -- pre-delivery quality checks

### Regulatory References
- FCA DISP App 3.4 (complaints root cause analysis)
- FCA PRIN 2A.9 (Consumer Duty monitoring)
- PRA SS1/21 (operational resilience impact tolerances)
- TPR General Code 2024 (breach reporting, ESOG)
- ISO 37301:2021 Clause 10.2 (compliance corrective action)
- ISO/IEC 42001:2023 Clause 10.2 (AI management corrective action)

---

## Worked Example: Stakeholder Remediation RCA

This example is drawn from an actual RCA conducted on the apex-helix pipeline.

**Problem:** 23 obligations across 6 Acts failed Stage 7 verification. 20 failed stakeholder validation, 3 failed grounding checks.

**Five Whys (stakeholder failures):**
1. Why did Stage 7 reject these obligations? -- Stakeholder values were non-entity strings ("P", "Regulations", "contribution notice")
2. Why were non-entity strings in the stakeholder field? -- The LLM extraction (Stage 5) treated legislative shorthand and instruments as actors
3. Why didn't anything catch this before Stage 7? -- No validation step existed between extraction (Stage 5) and verification (Stage 7)
4. Why was there no validation step? -- The pipeline assumed LLM extraction was reliable for stakeholder classification
5. Why was that assumption made? -- No systematic testing of stakeholder extraction quality across the full corpus

**Root Cause:** Missing quality gate between extraction and verification stages.

**Corrective Action:** Stage 5.5 (`stage5_5_obligation_qc.py`) inserted into pipeline:
- Registry-matches stakeholders against canonical list
- Fuzzy-remaps known bad patterns (remap table)
- Flags ambiguous stakeholders for human review
- Downgrades confidence on unresolvable items to 0.5
- Pre-checks grounding overlap

**Result:** 3,447 obligations QC'd, 99.9% pass rate, 14 remapped, 1 flagged. Stage 7 re-run: 99.8% pass rate (7 failures, all legitimate edge cases).

**Lesson compounded:** Pipeline stages must have QC gates between ML-generated output and downstream processing. Trust but verify.
