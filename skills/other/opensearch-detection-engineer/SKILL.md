---
name: opensearch-detection-engineer
description: "OpenSearch detection engineering: SIGMA authoring, query DSL translation, MITRE ATT&CK mapping, anomaly detection, correlation rules, SOC incident escalation. Use for SIEM detection authoring, threshold tuning, alert validation, and Tier-1/Tier-2 escalation workflows."
version: 1.0.0
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - siem detection
    - sigma rule
    - mitre att&ck mapping
    - detection engineering
    - opensearch detection
    - anomaly detection rule
    - soc escalation
    - detection validation
    - threat correlation rule
    - security analytics
  pairs_with:
    - opensearch-elasticsearch-engineer
  category: engineering
---

# OpenSearch Detection Engineering

Methodology for authoring and validating SIEM detections on OpenSearch Security Analytics: SIGMA rules, query DSL translation, MITRE ATT&CK mapping, anomaly detection, correlation, and SOC incident escalation. Vendor-neutral framework with OpenSearch-specific API patterns.

## When to Use

| Trigger | Action |
|---------|--------|
| Author a new SIGMA rule or DSL detector | Load `detection-engineering.md`, follow 6-section lifecycle |
| Translate SIGMA to OpenSearch DSL | Load `detection-engineering.md` for translation patterns |
| Tune false positive rate or threshold | Load `detection-engineering.md` for calibration steps |
| Build escalation package or run SOC handoff | Load `incident-escalation.md` for 9-field gate |
| Diagnose detector creation failure or alert flood | Load `detection-safety-patterns.md` for OpenSearch failure modes |
| Map detection to MITRE ATT&CK | Load `detection-engineering.md` for tactic/technique catalog |

## Hardcoded Behaviors (Always Apply)

- **MITRE ATT&CK on every detection.** Include technique ID (e.g., `T1110.003`), tactic name (e.g., `Credential Access`), and kill chain phase with every rule, alert, or detector. Tactic alone is insufficient — technique IDs enable coverage gap analysis.
- **Field-existence check before rule creation.** Run `GET {index}/_mapping` and confirm every field referenced in the rule exists in the target index mapping before submitting the detector. Absent fields cause silent failure or misleading errors.
- **Concrete API commands.** Provide `PUT _mapping`, `POST _aliases`, `POST /_plugins/_security_analytics/...` — not abstract advice.
- **Escalation package validation.** Before recommending escalation, verify all 9 fields are present (ticket ID, alert link, MITRE mapping, timeline, investigation actions, impact analysis, evidence artifacts, containment recommendation, 5 Ws). Missing fields fail QA.
- **Severity tier governs SLA.** Reference response-time tiers as binding requirements, not advisory targets. Configure tier defaults per organization; defaults are documented in `incident-escalation.md`.
- **Tier-1 vs Tier-2 distinction.** Distinguish runbook-driven triage and enrichment (Tier-1) from deep-dive investigation (Tier-2) when authoring use case docs and escalation paths.
- **Detection-owned index recommendation.** When a detector bootstraps field aliases, recommend a dedicated index separate from the ingestion datastream — bootstrap is destructive on shared indices.
- **KPI framing.** Frame detection changes in terms of TTD / TTR / MTTR / FP rate / escalation quality score impact. Track measurable outcomes, not activity.

## Default Behaviors (ON unless disabled)

- **6-section use case lifecycle template.** Produce use case documentation in the standardized format (General Info, Context, Outcomes, Detection Logic, Continuous Improvement, Analyst Support). See `incident-escalation.md`.
- **SIGMA → DSL translation with field validation.** When given a SIGMA rule, translate to OpenSearch query DSL and flag any fields not present in the target mapping before proposing detector creation.
- **False positive suppression patterns.** Apply CIDR exclusions, service-account prefixes, and time-window suppression in monitor queries — surfaced explicitly, never silently suppressed.

## Optional Behaviors (OFF unless enabled)

- **Purple team / tabletop support.** Map detection coverage against MITRE ATT&CK gaps for red/blue exercises.
- **Log source onboarding.** Field availability analysis, cardinality checks, and coverage mapping for new sources.

## Hard Gate Patterns

Before creating or modifying a detector, check for these. If found, STOP and resolve before continuing.

| Pattern | Why Blocked | Fix |
|---------|-------------|-----|
| Proposed rule field absent from index mapping | Detector creation fails silently or with misleading error | `GET {index}/_mapping`; confirm field exists; adjust rule or add field |
| MITRE mapping missing technique ID OR tactic | Coverage analysis broken; cannot align to ATT&CK matrix | Specify both `T####.###` and tactic category |
| Escalation package missing any of 9 required fields | Incomplete escalations fail QA gate; reduce escalation quality score | Validate all 9 fields before submitting; see `incident-escalation.md` |
| Chained findings monitor on high-frequency schedule | Creates/deletes query indices on every run, causing index count flood | Use static query indices; see `detection-safety-patterns.md` |
| Field alias bootstrap on shared datastream | Destructive bootstrap overwrites existing aliases | Create detection-owned index; see `detection-safety-patterns.md` |
| Alias type conflict on detector target index | `PUT _mapping` cannot remove stale alias; detector creation blocked | Reindex to clean index; see `detection-safety-patterns.md` |

## Verification STOP Blocks

After authoring a detection rule, STOP and confirm: "Have I verified every field name exists in the target index mapping via `GET {index}/_mapping`? Assumption is the failure mode."

After recommending escalation, STOP and confirm: "Does the package include all 9 required fields? Missing fields fail the QA gate."

After creating a chained findings monitor, STOP and confirm: "Does this monitor create a new query index per run? Index flood is a confirmed production failure mode."

After any MITRE mapping, STOP and confirm: "Did I include both technique ID (T####.###) and tactic category?"

## Anti-Rationalization

| Rationalization Attempt | Why It's Wrong | Required Action |
|------------------------|----------------|-----------------|
| "The field probably exists in the index" | Absent fields cause silent detector failures | Run `GET {index}/_mapping` before proposing any rule |
| "Chained findings monitors are fine on default settings" | Index flood is a confirmed production failure mode | Check monitor type and schedule; flag and remediate |
| "The escalation looks complete enough" | Incomplete packages reduce escalation quality score | Validate all 9 fields explicitly |
| "MITRE tactic is enough without technique ID" | Technique IDs enable precise coverage gap analysis | Include both (e.g., T1110.003 + Credential Access) |
| "Auto-mapping is fine for a detection index" | Alias bootstrap is destructive on shared indices | Use detection-owned index with explicit mapping |
| "SLAs are guidelines" | Response times are KPI-tracked organizational commitments | Reference exact tier times; treat as binding |

## Blocker Criteria

STOP and ask the user when:

| Situation | Why Stop | Ask This |
|-----------|----------|----------|
| Index mapping unknown before detector creation | Cannot validate field existence | "Can you run `GET {index}/_mapping` and share the output?" |
| Log source schema not provided for new detection | Cannot check field normalization | "What log format and field names does this source produce?" |
| Severity tier not specified for escalation | Cannot determine SLA | "What severity tier: Very High / High / Medium / Low?" |
| Chained findings monitor schedule unknown | Cannot assess index flood risk | "What is the monitor run interval?" |

## Reference Loading Table

| Signal | Reference | What it adds |
|--------|-----------|--------------|
| SIGMA authoring, DSL translation, MITRE mapping, detector creation, field normalization, FP suppression | `references/detection-engineering.md` | MITRE quick reference, SIGMA format, DSL translation, anomaly detector setup, correlation rules, OpenStack/Keystone field-mapping example |
| Incident escalation, severity tiers, SLA targets, use case template, KPIs, RACI | `references/incident-escalation.md` | Severity SLA defaults, 9-field escalation checklist, 6-section use case template, KPI definitions and queries |
| Detector creation failures, alias conflicts, index flood, field alias bootstrap, type coercion | `references/detection-safety-patterns.md` | Chained findings index flood fix, field alias bootstrap remediation, alias-vs-text conflict diagnosis, error-fix mapping table |

## Workflow

### Phase 1: Scope the Detection

1. Identify attack scenario, data source, and severity tier
2. Map to MITRE ATT&CK (technique ID + tactic + kill chain phase)
3. Confirm log source is ingested and schema is known

**Gate:** MITRE technique ID + tactic recorded; log source schema available.

### Phase 2: Validate Field Availability

1. `GET {index}/_mapping` for each field referenced in the proposed rule
2. Run cardinality checks for any field used in `terms` aggregations
3. Identify missing fields → add to mapping OR adjust rule

**Gate:** Every field in the rule exists in the target mapping. Cardinality is bounded.

### Phase 3: Author Detection

1. Choose methodology (rule-based / threshold / anomaly / correlation) per scenario
2. Write SIGMA rule first (vendor-neutral)
3. Translate to OpenSearch DSL via patterns in `detection-engineering.md`
4. Apply FP suppression filters (CIDR, service-account prefixes, time windows)

**Gate:** SIGMA + DSL both produced; FP suppressions documented.

### Phase 4: Validate Detection Safety

1. Check for chained findings index flood pattern (if using chained monitors)
2. Check for field alias bootstrap risk on shared datastreams
3. Recommend detection-owned index if bootstrap risk present
4. See `detection-safety-patterns.md` for full safety checklist

**Gate:** No hard-gate patterns triggered.

### Phase 5: Document Use Case (6-section template)

1. General Info, Context, Outcomes, Detection Logic, Continuous Improvement, Analyst Support
2. Capture KPI baselines (TTD, FP rate target, review cadence)
3. Link runbook for Tier-1 triage steps

**Gate:** All 6 sections populated; runbook linked.

### Phase 6: Calibrate and Tune

1. Run monitor in dry-run mode for 5 business days
2. Export findings; label TPs and FPs
3. Adjust threshold until FP rate ≤ 10%
4. Document threshold decision in use case doc

**Gate:** FP rate measured against target; tuning logged.

### Phase 7: Escalation Path (when alert fires)

1. Validate alert against use case detection logic
2. Build escalation package (all 9 fields)
3. Apply severity SLA from tier table
4. Hand off per RACI in `incident-escalation.md`

**Gate:** 9-field package complete; SLA window identified; recipient confirmed.

## Capabilities and Limitations

### What This Skill CAN Do
- Author and tune SIGMA rules, OpenSearch custom rules, threshold monitors, anomaly detectors with MITRE mapping
- Diagnose mapping failures (alias-vs-text, field alias bootstrap, type coercion) with concrete API fix commands
- Detect and fix chained findings index flood
- Design correlation rules for cross-source enrichment
- Write 9-field escalation packages aligned to severity SLAs
- Produce 6-section use case lifecycle documentation
- Define KPI baselines (TTD, TTR, MTTR, FP rate, escalation quality)

### What This Skill CANNOT Do
- General OpenSearch cluster operations (shard sizing, JVM tuning, ILM unrelated to SIEM) — pair with `opensearch-elasticsearch-engineer`
- Log pipeline infrastructure changes (Fluentd topology, ingestion architecture)
- Application code development — use language-specific agents
- Terraform/IaC resource management

When asked to perform unavailable actions, explain the limitation and suggest the appropriate agent.
