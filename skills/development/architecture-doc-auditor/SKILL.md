---
name: architecture-doc-auditor
version: "2.0"
description: >
  Systematic completeness audit of Architecture Documentation using
  188-item viewpoint-based checklist, severity-classified gap detection,
  technical debt indicators, and architecture anti-pattern scanning.
  Supports TOGAF, C4, arc42, and IEEE 42010 frameworks.
  PROACTIVELY activate for: (1) Architecture review gates,
  (2) ADR validation before implementation, (3) C4 diagram completeness check,
  (4) Technical debt assessment, (5) Pre-implementation validation,
  (6) Governance compliance audit, (7) Design doc handoff review.
  Triggers: "audit architecture", "review ADR", "check architecture doc",
  "validate design doc", "architecture review", "audit C4 diagrams",
  "check system context", "technical debt assessment", "architecture health check",
  "governance review", "architecture completeness"
---

# Architecture Documentation Auditor

A systematic audit system that evaluates Architecture Documentation against a comprehensive 188-item viewpoint-based checklist, detecting gaps, classifying severity, identifying technical debt signals, scanning for architecture anti-patterns, and generating actionable remediation roadmaps. Implements the GAP-AUDIT pattern (PATTERN-08) to produce CONTRACT-07 compliant GAP-INVENTORY output with Architecture Health Score extensions.

---

## 1. Purpose

This skill provides 12 core capabilities:

| # | Capability | Phase | Description |
|---|------------|-------|-------------|
| 1 | **Framework Detect** | 1 | Identify architecture framework (TOGAF, C4, arc42, IEEE 42010) |
| 2 | **Document Parse** | 1 | Extract architecture structure, diagrams, and decision records |
| 3 | **Viewpoint Map** | 2 | Apply 14-viewpoint coverage framework to document sections |
| 4 | **Item-by-Item Verify** | 3 | Check each of 188 checklist items against content |
| 5 | **Gap Detect** | 3 | Identify missing, incomplete, or inconsistent elements |
| 6 | **Classify Gap Type** | 4 | Categorize gaps using 6-type taxonomy |
| 7 | **Score Severity** | 4 | Apply RUBRIC-07 (impact, likelihood, detectability) |
| 8 | **Anti-Pattern Scan** | 5 | Detect 25 architecture anti-patterns |
| 9 | **Debt Signal Detect** | 5 | Identify 25+ technical debt indicators |
| 10 | **Quality Attribute Validate** | 4 | Verify ISO 25010 quality attribute coverage |
| 11 | **Remediate Suggest** | 5 | Generate fix recommendations with effort estimates |
| 12 | **Synthesize Report** | 6 | Produce GAP-INVENTORY + Health Score + Debt Roadmap |

---

## 2. When to Use

**Ideal for:**
- Architecture review gates before implementation
- ADR validation before development starts
- C4 diagram completeness verification
- Technical debt assessment and tracking
- Pre-implementation readiness check
- Governance and compliance audits
- Design document handoff to development teams
- Architecture decision board preparation
- System modernization planning
- Security architecture review

**Avoid when:**
- Document is code, not architecture (use code review)
- Operational runbook review (use operations auditor)
- Early ideation phase (architecture not yet defined)
- Quick clarifying questions (formal audit adds overhead)
- Infrastructure-as-Code review (use IaC auditor)
- API specification only (use API spec auditor)

---

## 3. Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `document` | string | **yes** | — | Architecture document content or file reference |
| `document_type` | enum | no | `design_doc` | adr \| design_doc \| system_context \| container \| component \| deployment \| sequence \| data_flow |
| `framework` | enum | no | `auto` | togaf \| c4 \| arc42 \| ieee_42010 \| custom \| auto |
| `audit_depth` | enum | no | `standard` | surface \| standard \| exhaustive |
| `viewpoints` | list | no | `core_10` | List of viewpoint IDs (V1-V14) to validate |
| `quality_attributes` | list | no | `all` | ISO 25010 attributes to validate |
| `include_debt_assessment` | boolean | no | `true` | Whether to scan for technical debt indicators |
| `include_anti_patterns` | boolean | no | `true` | Whether to scan for architecture anti-patterns |
| `governance_context` | enum | no | `team` | enterprise \| team \| project |
| `output_format` | enum | no | `full` | full \| executive \| debt_roadmap_only |

### Document Type Effects

| Type | Primary Viewpoints | Checklist Focus |
|------|-------------------|-----------------|
| **adr** | V10 | Decision structure, rationale, consequences |
| **design_doc** | V1-V10 | Full viewpoint coverage |
| **system_context** | V1, V6, V7 | External actors, integrations, boundaries |
| **container** | V2, V5, V6 | Technology choices, communication patterns |
| **component** | V3, V6 | Internal structure, interfaces |
| **deployment** | V4, V8 | Infrastructure, scaling, operations |
| **sequence** | V6 | API flows, interaction patterns |
| **data_flow** | V5, V7 | Data stores, flows, security |

### Audit Depth Effects

| Depth | Behavior |
|-------|----------|
| **surface** | Critical items only (~60 items), structural gaps, no anti-patterns |
| **standard** | Full checklist for relevant viewpoints, anti-patterns, standard remediation |
| **exhaustive** | All viewpoints including conditional, deep anti-pattern analysis, debt indicators, detailed remediation |

### Governance Context Effects

| Context | Compliance Level | Output Focus |
|---------|-----------------|--------------|
| **enterprise** | Full compliance frameworks (SOC2, GDPR, PCI-DSS) | Governance reporting, compliance matrix |
| **team** | Standard architecture practices | Team handoff, implementation readiness |
| **project** | Minimal viable documentation | Quick assessment, critical gaps only |

---

## 4. Six-Phase Workflow

### Phase 1: Document Intake & Framework Detection

**Purpose:** Load document and establish audit context.

**Steps:**
1. Receive architecture document (inline or file reference)
2. Detect architecture framework:
   - C4: Look for Context/Container/Component/Code levels
   - arc42: Look for 12-section template structure
   - TOGAF: Look for ADM phase artifacts
   - IEEE 42010: Look for formal viewpoint definitions
3. Load `architecture-checklist.md` reference
4. Calibrate checklist based on `document_type`:
   - Filter items by viewpoint applicability
   - Adjust severity levels for document type
   - Set critical items that must be present
5. Parse document to identify structure:
   - Extract section headers and hierarchy
   - Identify diagram references and types
   - Note ADRs (Architecture Decision Records)
   - Detect technology stack references
6. Load `viewpoint-catalog.md` for structural validation
7. Initialize gap tracking structure with empty findings

**Techniques Used:**
- `document_structure_extraction` - Parse document hierarchy
- `framework_detection` - Identify architecture methodology
- `checklist_calibration` - Adjust criteria for context

**Quality Gate:** Framework identified; checklist calibrated for document type; structure parsed with sections identified

**Output:** Calibrated checklist (N items) + Document structure map + Detected framework

---

### Phase 2: Viewpoint Mapping & Scope Definition

**Purpose:** Map document sections to architecture viewpoints and identify structural gaps.

**Steps:**
1. Load viewpoint framework from `viewpoint-catalog.md`:

   **Core Viewpoints (Always Assess):**
   - V1: Context & Scope (system boundary, external actors)
   - V2: Container Architecture (major components, technology choices)
   - V3: Component Design (internal structure, interfaces)
   - V4: Deployment Topology (infrastructure, scaling)
   - V5: Data Architecture (data stores, flows, ownership)
   - V6: Integration & APIs (contracts, protocols, versioning)
   - V7: Security Architecture (auth, encryption, compliance)
   - V8: Operational Concerns (monitoring, SLOs, runbooks)
   - V9: Cross-Cutting Concerns (logging, caching, config)
   - V10: Decision Record (ADRs, rationale, consequences)

   **Conditional Viewpoints (If Applicable):**
   - V11: Multi-tenancy (SaaS/multi-tenant systems)
   - V12: Event Architecture (event-driven systems)
   - V13: Migration Path (legacy modernization)
   - V14: Compliance Matrix (regulated industries)

2. Map each document section to viewpoints:
   - Assign based on content, not just header
   - Flag orphan sections (don't fit any viewpoint)
   - Flag missing viewpoints (no sections mapped)
3. Identify structural gaps:
   - Core viewpoint with no coverage = CRITICAL structural gap
   - Core viewpoint with partial coverage = HIGH structural gap
   - Conditional viewpoint missing when applicable = MEDIUM gap
4. Check for applicable conditional viewpoints:
   - Multi-tenancy: Evidence of tenant-based requirements
   - Event architecture: Event-driven patterns mentioned
   - Migration: Legacy system references
   - Compliance: Regulatory requirements mentioned
5. Calculate initial coverage score per viewpoint

**Techniques Used:**
- `completeness_verification` (CAT-PR-GA) - Verify all viewpoints addressed
- `viewpoint_mapping` - Map sections to architectural concerns

**Quality Gate:** All applicable viewpoints assessed; structural gaps flagged

**Output:** Viewpoint coverage map with scores and structural gap list

---

### Phase 3: Systematic Coverage Verification

**Purpose:** Verify each checklist item against document content.

**Steps:**

For each checklist item (V1-01 through V10-20):

```
1. LOCATE RELEVANT SECTION
   └─ Based on viewpoint mapping from Phase 2

2. ASSESS PRESENCE
   ├─ PRESENT: Item clearly addressed
   ├─ PARTIAL: Item mentioned but incomplete
   └─ ABSENT: No evidence of item

3. EVALUATE QUALITY (if present)
   ├─ CLEAR: Unambiguous and actionable
   ├─ AMBIGUOUS: Multiple interpretations possible
   ├─ INCONSISTENT: Contradicts other content
   ├─ INCOMPLETE: Missing key details
   └─ OUTDATED: Stale or deprecated references

4. RECORD EVIDENCE
   ├─ Location: Section/diagram reference
   ├─ Quote: Supporting text from document
   └─ Assessment: Pass/fail with rationale

5. FLAG FOR GAP CLASSIFICATION (if needed)
   └─ Any non-PRESENT or non-CLEAR items
```

**Verification Rules by Viewpoint:**

| Viewpoint | Items | Critical Items | Verification Approach |
|-----------|-------|----------------|----------------------|
| V1: Context | V1-01 to V1-15 | V1-01, V1-02, V1-03 | Check boundary definition, external actors |
| V2: Container | V2-01 to V2-25 | V2-01, V2-02, V2-05 | Verify technology choices documented |
| V3: Component | V3-01 to V3-18 | V3-01, V3-02 | Check internal structure clarity |
| V4: Deployment | V4-01 to V4-22 | V4-01, V4-05, V4-10 | Verify infrastructure defined |
| V5: Data | V5-01 to V5-18 | V5-01, V5-02, V5-05 | Check data stores and flows |
| V6: Integration | V6-01 to V6-15 | V6-01, V6-02, V6-05 | Verify API contracts exist |
| V7: Security | V7-01 to V7-25 | V7-01, V7-02, V7-05, V7-10 | Check auth, encryption, audit |
| V8: Operations | V8-01 to V8-18 | V8-01, V8-05, V8-10 | Verify monitoring, SLOs defined |
| V9: Cross-Cutting | V9-01 to V9-12 | V9-01, V9-05 | Check logging, config patterns |
| V10: Decisions | V10-01 to V10-20 | V10-01, V10-02, V10-05 | Verify ADR structure and coverage |

**Techniques Used:**
- `completeness_verification` (CAT-PR-GA) - Check presence of each item
- `negative_space_analysis` (CAT-PR-GA) - Identify what's NOT documented
- `consistency_check` (CAT-PR-ECR) - Cross-reference between viewpoints

**Quality Gate:** 100% of applicable checklist items evaluated

**Output:** Verification matrix with item-level results and evidence

---

### Phase 4: Quality Attribute Validation

**Purpose:** Validate coverage of ISO 25010 quality attributes.

**Steps:**

#### 4.1 Quality Attribute Mapping

Map document content to quality attributes from `quality-attributes.md`:

| Quality Attribute | Primary Viewpoints | Validation Criteria |
|------------------|-------------------|---------------------|
| **Performance** | V4, V5 | Latency targets, throughput requirements, resource limits |
| **Scalability** | V4, V2 | Scaling strategy, elasticity approach, capacity planning |
| **Security** | V7, V6 | Auth mechanisms, encryption, audit logging, compliance |
| **Reliability** | V8, V4 | Availability targets, fault tolerance, DR strategy |
| **Maintainability** | V3, V10 | Modularity, testability, decision rationale |
| **Interoperability** | V6, V1 | API standards, protocol choices, versioning |
| **Portability** | V4, V2 | Platform dependencies, abstraction layers |
| **Usability** | V6, V10 | API ergonomics, developer experience |

#### 4.2 Coverage Assessment

For each quality attribute:
1. Identify explicit coverage in primary viewpoints
2. Check for implicit coverage in secondary viewpoints
3. Assess coverage level: EXPLICIT / IMPLICIT / MISSING
4. Note measurement approaches if present

#### 4.3 Gap Identification

Flag quality attribute gaps:
- MISSING in primary viewpoint = HIGH gap
- MISSING in all viewpoints = CRITICAL gap for regulated contexts

**Techniques Used:**
- `quality_attribute_validation` - Map concerns to ISO 25010
- `coverage_assessment` - Evaluate attribute coverage

**Quality Gate:** All quality attributes assessed with coverage level

**Output:** Quality attribute coverage matrix

---

### Phase 5: Technical Debt & Anti-Pattern Detection

**Purpose:** Identify technical debt signals and architecture anti-patterns.

**Steps:**

#### 5.1 Gap Classification

For each gap identified in Phases 3-4, apply gap taxonomy (from `gap-taxonomy.md`):

```
IS ELEMENT PRESENT?
├─ NO → MISSING
└─ YES
    ├─ IS IT COMPLETE?
    │   ├─ NO → INCOMPLETE
    │   └─ YES
    │       ├─ DOES IT CONTRADICT OTHER CONTENT?
    │       │   ├─ YES → INCONSISTENT
    │       │   └─ NO
    │       │       ├─ IS IT CLEAR AND UNAMBIGUOUS?
    │       │       │   ├─ NO → AMBIGUOUS
    │       │       │   └─ YES
    │       │       │       ├─ IS IT TECHNICALLY CORRECT?
    │       │       │       │   ├─ NO → INCORRECT
    │       │       │       │   └─ YES
    │       │       │       │       └─ IS IT CURRENT?
    │       │       │       │           ├─ NO → OUTDATED
    │       │       │       │           └─ YES → No gap
```

#### 5.2 Severity Scoring

Apply SEVERITY-SCORING (RUBRIC-07) with three dimensions:

| Dimension | Weight | Scale |
|-----------|--------|-------|
| **Impact** | 0.5 | 1=Low, 2=Medium, 3=High, 4=Critical |
| **Likelihood** | 0.3 | 1=Rare, 2=Possible, 3=Likely, 4=Certain |
| **Detectability** | 0.2 | 1=Obvious, 2=Moderate, 3=Difficult, 4=Hidden |

**Calculation:**
```
severity_score = (impact × 0.5) + (likelihood × 0.3) + (detectability × 0.2)

CRITICAL: score >= 3.5
HIGH: 2.5 <= score < 3.5
MEDIUM: 1.5 <= score < 2.5
LOW: score < 1.5
```

#### 5.3 Architecture Anti-Pattern Scan

If `include_anti_patterns` is true, scan for 25 patterns from `anti-patterns-catalog.md`:

**Structural Anti-Patterns:**

| ID | Anti-Pattern | Severity | Detection Signal |
|----|--------------|----------|------------------|
| AA-01 | Big Ball of Mud | CRITICAL | No clear component boundaries |
| AA-02 | Distributed Monolith | CRITICAL | Microservices with tight coupling |
| AA-03 | Database Monolith | HIGH | All services sharing single database |
| AA-04 | God Service | HIGH | One service handling everything |
| AA-05 | Circular Dependencies | CRITICAL | A depends on B depends on A |
| AA-06 | Golden Hammer | MEDIUM | Same tech used regardless of fit |
| AA-07 | Vendor Lock-in Blindness | HIGH | No abstraction over proprietary services |
| AA-08 | Accidental Complexity | HIGH | Over-engineering indicators |

**Documentation Anti-Patterns:**

| ID | Anti-Pattern | Severity | Detection Signal |
|----|--------------|----------|------------------|
| AA-09 | Diagram Divorce | CRITICAL | Diagrams don't match text |
| AA-10 | ADR Amnesia | HIGH | Decisions made without records |
| AA-11 | Stale Blueprints | HIGH | Docs reference deprecated systems |
| AA-12 | View Vacuum | CRITICAL | Missing entire viewpoint |
| AA-13 | C4 Confusion | MEDIUM | Mixed abstraction levels in diagrams |
| AA-14 | Prose Overload | MEDIUM | Walls of text, no diagrams |
| AA-15 | Technology Tourism | LOW | Tech name-dropping without rationale |
| AA-16 | Abstraction Allergy | MEDIUM | Only code-level detail, no conceptual |

**Operational Anti-Patterns:**

| ID | Anti-Pattern | Severity | Detection Signal |
|----|--------------|----------|------------------|
| AA-17 | Observability Omission | HIGH | No monitoring/alerting strategy |
| AA-18 | SLO Silence | HIGH | No reliability targets |
| AA-19 | Deployment Darkness | CRITICAL | No deployment documentation |
| AA-20 | Capacity Blindness | HIGH | No scaling strategy |
| AA-21 | Runbook Roulette | MEDIUM | No operational procedures |

**Security Anti-Patterns:**

| ID | Anti-Pattern | Severity | Detection Signal |
|----|--------------|----------|------------------|
| AA-22 | Trust Assumption | CRITICAL | "Internal network is secure" |
| AA-23 | Auth Afterthought | HIGH | Security bolted on later |
| AA-24 | Secret Scatter | CRITICAL | Credentials in configs/code |
| AA-25 | Compliance Complacency | HIGH | No compliance mapping |

#### 5.4 Technical Debt Detection

If `include_debt_assessment` is true, scan for indicators from `technical-debt-indicators.md`:

| Category | Indicators | Severity Range |
|----------|------------|----------------|
| **Architectural Debt** | Shared databases, sync coupling, missing abstractions | HIGH-CRITICAL |
| **Documentation Debt** | Stale diagrams, missing rationale, undocumented interfaces | MEDIUM-HIGH |
| **Infrastructure Debt** | Manual deployments, missing DR, hardcoded config | MEDIUM-HIGH |
| **Security Debt** | Undocumented auth, missing encryption, no audit strategy | HIGH-CRITICAL |
| **API Debt** | Breaking changes, no versioning, inconsistent contracts | MEDIUM-HIGH |

#### 5.5 Remediation Matching

Match each gap to remediation pattern:

| Gap Type | Primary Pattern | Action |
|----------|-----------------|--------|
| MISSING | Add Content | Write new section using template |
| INCOMPLETE | Expand Content | Fill in missing details |
| INCONSISTENT | Reconcile Content | Resolve contradictions |
| AMBIGUOUS | Clarify Content | Add specificity/metrics |
| INCORRECT | Correct Content | Fix technical errors |
| OUTDATED | Update Content | Refresh stale information |

**Effort Estimation:**

| Effort Level | Definition | Time Range |
|--------------|------------|------------|
| **trivial** | Quick fix, obvious solution | < 30 min |
| **small** | Clear scope, single viewpoint | 30 min - 2 hours |
| **medium** | Multiple viewpoints or research needed | 2 - 8 hours |
| **large** | Significant rework or stakeholder input | 1+ days |

**Techniques Used:**
- `severity_scoring` (RUBRIC-07) - Score gaps by impact
- `full_consistency_matrix` (CAT-PR-ECR) - Cross-reference for inconsistencies
- `anti_pattern_detection` - Match known failure patterns
- `debt_signal_detection` - Identify technical debt indicators

**Quality Gate:** All gaps classified with type and severity; anti-patterns and debt signals detected

**Output:** Classified gap list + Anti-pattern findings + Debt indicators

---

### Phase 6: Synthesis & Governance Reporting

**Purpose:** Produce final GAP-INVENTORY artifact with Architecture Health Score.

**Steps:**

#### 6.1 GAP-INVENTORY Compilation

Compile all findings into CONTRACT-07 compliant structure:
- Populate `source_reference` with document identifier
- Set `source_type` to "architecture"
- Build `audit_criteria` with viewpoint-based checklist
- Compile `gaps` array with all classified gaps
- Add `anti_patterns` array if detected
- Add `technical_debt` section with indicators
- Calculate `summary` statistics

#### 6.2 Architecture Health Score

Calculate overall architecture health:

```xml
<architecture_health>
  <overall_score>[0-100]</overall_score>
  <by_viewpoint>
    <!-- Score per viewpoint -->
  </by_viewpoint>
  <by_quality_attribute>
    <!-- Coverage per ISO 25010 attribute -->
  </by_quality_attribute>
  <technical_debt_summary>
    <!-- Debt indicator counts by category -->
  </technical_debt_summary>
  <c4_maturity>
    <!-- Completeness of C4 levels if applicable -->
  </c4_maturity>
</architecture_health>
```

**Health Score Calculation:**
```
viewpoint_score = (items_passed / items_total) × 100 per viewpoint
overall_score = weighted_average(viewpoint_scores) - severity_penalties

Severity Penalties:
- CRITICAL gap: -10 points
- HIGH gap: -5 points
- Anti-pattern: -3 points
- Debt indicator: -2 points
```

**Health Status Thresholds:**

| Status | Score Range | Interpretation |
|--------|-------------|----------------|
| **HEALTHY** | 80-100 | Ready for implementation |
| **ADEQUATE** | 60-79 | Minor gaps, proceed with awareness |
| **AT_RISK** | 40-59 | Significant gaps, address before proceeding |
| **CRITICAL** | 0-39 | Major gaps, not ready for implementation |

#### 6.3 Summary Statistics

Generate:
- `total_gaps`: Count of all gaps
- `by_severity`: {critical: N, high: N, medium: N, low: N}
- `by_category`: {missing: N, incomplete: N, inconsistent: N, ...}
- `by_viewpoint`: Gap count per viewpoint
- `overall_assessment`: Based on health score
- `blocking_issues`: List of gap IDs that must be fixed
- `coverage_score`: Percentage of checklist items passed

**Assessment Thresholds:**

| Assessment | Criteria |
|------------|----------|
| **critical_issues** | Any CRITICAL gap OR overall_score < 40 |
| **significant_gaps** | No CRITICAL but score 40-59 OR >3 HIGH gaps |
| **minor_issues** | Score 60-79, only MEDIUM/LOW gaps |
| **acceptable** | Score 80-89, few gaps |
| **excellent** | Score 90+, minimal gaps |

#### 6.4 Executive Summary (if requested)

Generate stakeholder-friendly summary:
- At-a-glance metrics table
- Viewpoint coverage spider chart data
- Quality attribute coverage radar chart data
- Top 3 strengths
- Top 3 critical issues
- Risk heat map data
- Recommended next actions

#### 6.5 Debt Remediation Roadmap (if requested)

Generate prioritized technical debt paydown plan:
- Priority 1: Immediate (blocking issues)
- Priority 2: Short-term (before implementation)
- Priority 3: Medium-term (during implementation)
- Priority 4: Long-term (continuous improvement)
- Effort/impact quadrant
- Quick wins identification
- Strategic investments

#### 6.6 Output Selection

Based on `output_format` parameter:
- **full**: GAP-INVENTORY + Health Report + Debt Roadmap
- **executive**: Executive Summary only
- **debt_roadmap_only**: Technical Debt Roadmap only

**Techniques Used:**
- `artifact_synthesis` - Compile structured output
- `health_score_calculation` - Compute architecture health
- `stakeholder_communication` - Tailor for audience

**Quality Gate:** Output validates against CONTRACT-07 schema with architecture extensions

**Output:** GAP-INVENTORY artifact + Architecture Health Score + requested summaries

---

## 5. Gap Taxonomy

### The 6 Gap Types

| # | Type | Definition | Architecture Detection Signal | Remediation |
|---|------|------------|------------------------------|-------------|
| 1 | **MISSING** | Required element completely absent | No viewpoint coverage, no ADRs found, deployment undocumented | Add content |
| 2 | **INCOMPLETE** | Present but lacking required detail | TBD in diagrams, partial API specs, rationale missing | Expand content |
| 3 | **INCONSISTENT** | Contradicts other sections | Context shows 5 services, container shows 8; ADR contradicts implementation | Reconcile content |
| 4 | **AMBIGUOUS** | Multiple interpretations possible | "Scalable architecture" without metrics, "secure by design" without controls | Clarify content |
| 5 | **INCORRECT** | Technically wrong information | References deprecated API, shows removed service, wrong technology | Correct content |
| 6 | **OUTDATED** | Was correct but no longer current | Shows v1 API when v3 current, references decommissioned database | Update content |

**Reference:** See `references/architecture-checklist.md` for detailed detection heuristics per checklist item.

---

## 6. Output Specifications

### 6.1 GAP-INVENTORY Format

Aligns with CONTRACT-07 from artifact-contracts.yaml with architecture extensions.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gap_inventory contract="CONTRACT-07" version="1.0">

  <metadata>
    <artifact_id>GI-ARCH-[YYYY-MM-DD]-[5-char-hash]</artifact_id>
    <contract_type>GAP-INVENTORY</contract_type>
    <created_at>[ISO 8601]</created_at>
    <created_by>architecture-doc-auditor</created_by>
    <confidence>[0.0-1.0]</confidence>
    <provenance>
      <source_artifact>[Document identifier]</source_artifact>
      <audit_date>[ISO 8601 date]</audit_date>
      <audit_depth>[surface|standard|exhaustive]</audit_depth>
      <document_type>[adr|design_doc|system_context|...]</document_type>
      <framework_detected>[togaf|c4|arc42|ieee_42010|custom]</framework_detected>
      <checklist_version>1.0</checklist_version>
      <items_checked>[N]</items_checked>
      <viewpoints_assessed>[list]</viewpoints_assessed>
    </provenance>
  </metadata>

  <source_reference>[Document identifier]</source_reference>
  <source_type>architecture</source_type>

  <audit_criteria>
    <checklist_reference>architecture-checklist.md v1.0</checklist_reference>
    <viewpoint_framework>viewpoint-catalog.md v1.0</viewpoint_framework>
    <criteria_list>
      <criterion id="[V1-01]" viewpoint="V1">[Item description]</criterion>
      <!-- All checked items -->
    </criteria_list>
    <coverage_scope>[What this audit covered]</coverage_scope>
  </audit_criteria>

  <gaps>
    <gap id="GAP-001">
      <category>[missing|incomplete|inconsistent|ambiguous|incorrect|outdated]</category>
      <severity>[critical|high|medium|low]</severity>
      <severity_score>
        <impact>[1-4]</impact>
        <likelihood>[1-4]</likelihood>
        <detectability>[1-4]</detectability>
        <composite>[calculated]</composite>
      </severity_score>
      <viewpoint>[V1-V14]</viewpoint>
      <checklist_ref>[V1-01]</checklist_ref>
      <location>[Document section/diagram]</location>
      <description>[Gap description]</description>
      <evidence>[What indicates this gap]</evidence>
      <impact>[Consequence if not addressed]</impact>
      <remediation>
        <recommendation>[How to fix]</recommendation>
        <effort>[trivial|small|medium|large]</effort>
        <priority>[immediate|short_term|medium_term|long_term]</priority>
      </remediation>
    </gap>
  </gaps>

  <anti_patterns>
    <pattern id="AA-02">
      <name>Distributed Monolith</name>
      <severity>CRITICAL</severity>
      <instances>
        <instance location="[section]">[Evidence quote]</instance>
      </instances>
      <remediation>[How to address]</remediation>
    </pattern>
  </anti_patterns>

  <technical_debt>
    <indicator id="TD-A01">
      <category>architectural</category>
      <name>Shared database between services</name>
      <severity>HIGH</severity>
      <evidence>[Where detected]</evidence>
      <remediation_cost>large</remediation_cost>
    </indicator>
  </technical_debt>

  <architecture_health>
    <overall_score>[0-100]</overall_score>
    <overall_status>[HEALTHY|ADEQUATE|AT_RISK|CRITICAL]</overall_status>
    <by_viewpoint>
      <viewpoint id="V1" name="Context & Scope" score="[0-100]" status="[status]"/>
      <viewpoint id="V2" name="Container" score="[0-100]" status="[status]"/>
      <!-- All assessed viewpoints -->
    </by_viewpoint>
    <by_quality_attribute>
      <attribute name="Performance" coverage="[EXPLICIT|IMPLICIT|MISSING]"/>
      <attribute name="Security" coverage="[EXPLICIT|IMPLICIT|MISSING]"/>
      <!-- All quality attributes -->
    </by_quality_attribute>
    <technical_debt_summary>
      <total_indicators>[N]</total_indicators>
      <by_category>
        <architectural>[N]</architectural>
        <documentation>[N]</documentation>
        <infrastructure>[N]</infrastructure>
        <security>[N]</security>
        <api>[N]</api>
      </by_category>
    </technical_debt_summary>
    <c4_maturity>
      <level_1_complete>[true|false]</level_1_complete>
      <level_2_complete>[true|false]</level_2_complete>
      <level_3_complete>[true|false]</level_3_complete>
      <level_4_complete>[true|false]</level_4_complete>
    </c4_maturity>
  </architecture_health>

  <summary>
    <total_gaps>[N]</total_gaps>
    <by_severity>
      <critical>[N]</critical>
      <high>[N]</high>
      <medium>[N]</medium>
      <low>[N]</low>
    </by_severity>
    <by_category>
      <missing>[N]</missing>
      <incomplete>[N]</incomplete>
      <inconsistent>[N]</inconsistent>
      <ambiguous>[N]</ambiguous>
      <incorrect>[N]</incorrect>
      <outdated>[N]</outdated>
    </by_category>
    <by_viewpoint>
      <v1>[N]</v1>
      <v2>[N]</v2>
      <!-- Gap count per viewpoint -->
    </by_viewpoint>
    <anti_patterns_detected>[N]</anti_patterns_detected>
    <debt_indicators_detected>[N]</debt_indicators_detected>
    <overall_assessment>[critical_issues|significant_gaps|minor_issues|acceptable|excellent]</overall_assessment>
    <blocking_issues>
      <issue ref="GAP-001">[Brief description]</issue>
    </blocking_issues>
    <coverage_score>
      <items_passed>[N]</items_passed>
      <items_total>[N]</items_total>
      <percentage>[X%]</percentage>
    </coverage_score>
  </summary>

</gap_inventory>
```

### 6.2 Executive Summary Format

See `templates/architecture-health-report.md` for complete template.

### 6.3 Debt Remediation Roadmap Format

See `templates/debt-remediation-roadmap.md` for complete template.

---

## 7. Quality Gates

| # | Gate | Criterion | Phase |
|---|------|-----------|-------|
| 1 | **Framework Detected** | Architecture methodology identified or marked as custom | 1 |
| 2 | **Checklist Calibrated** | Checklist adjusted for document type with applicable items | 1 |
| 3 | **Document Parsed** | All sections identified with structure map created | 1 |
| 4 | **Viewpoints Mapped** | All applicable viewpoints assessed with scores | 2 |
| 5 | **Items Verified** | 100% of applicable checklist items evaluated | 3 |
| 6 | **Quality Attributes Checked** | All ISO 25010 attributes assessed for coverage | 4 |
| 7 | **Gaps Classified** | All gaps assigned type from 6-type taxonomy | 5 |
| 8 | **Severity Scored** | All gaps scored using 3-dimension RUBRIC-07 | 5 |
| 9 | **Anti-Patterns Scanned** | All 25 anti-patterns checked (if enabled) | 5 |
| 10 | **Debt Indicators Scanned** | All debt categories checked (if enabled) | 5 |
| 11 | **Health Score Calculated** | Overall architecture health score computed | 6 |
| 12 | **Output Validated** | GAP-INVENTORY conforms to CONTRACT-07 schema | 6 |

---

## 8. Workflow Integration

This skill serves as a quality gate in the architecture development workflow:

```
┌─────────────────────────────────────┐
│   ARCHITECTURE DOC AUDITOR          │  ◀── THIS SKILL
│                                     │
└────────────────┬────────────────────┘
                 │
                 │ Input: Architecture Document
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 1: Intake & Framework        │
│  • Detect framework (C4/arc42/...)  │
│  • Load architecture-checklist      │
│  • Parse document structure         │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 2: Viewpoint Mapping         │
│  • Apply 14-viewpoint framework     │
│  • Map sections to viewpoints       │
│  • Flag structural gaps             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 3: Coverage Verification     │  ◀── Perfect Recall techniques
│  • Check 188 checklist items        │      completeness_verification
│  • Record presence and quality      │      consistency_check
│  • Cite evidence locations          │      negative_space_analysis
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 4: Quality Attributes        │  ◀── ISO 25010 validation
│  • Map to 8 quality attributes      │
│  • Assess coverage level            │
│  • Flag quality gaps                │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 5: Debt & Anti-Patterns      │  ◀── RUBRIC-07 severity scoring
│  • Classify gaps (6 types)          │
│  • Score severity (3 dimensions)    │
│  • Scan 25 anti-patterns            │
│  • Detect 25+ debt indicators       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 6: Synthesis                 │  ◀── CONTRACT-07 + Health Score
│  • Compile GAP-INVENTORY            │
│  • Calculate Architecture Health    │
│  • Generate remediation roadmap     │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  OUTPUT: GAP-INVENTORY              │
│  + Architecture Health Score        │
│  + Technical Debt Roadmap           │
└─────────────────────────────────────┘
```

### Artifact Flow

| This Skill Produces | Consumed By |
|---------------------|-------------|
| GAP-INVENTORY (CONTRACT-07) | Architecture review board, governance |
| Architecture Health Score | Executive reporting, readiness gates |
| Debt Remediation Roadmap | Technical leadership, sprint planning |

### Integration Points

| Upstream | This Skill | Downstream |
|----------|------------|------------|
| Architecture authoring | **Audit** | Implementation |
| ADR creation | **Validate** | Development sprint |
| C4 diagram creation | **Check completeness** | Technical design |
| Design doc drafting | **Quality gate** | Governance approval |

---

## 9. Behavioral Guidelines

- **Systematic not judgmental:** Report gaps objectively, not as criticism
- **Evidence-based:** Every gap must have cited evidence from the document
- **Constructive:** Focus on remediation, not just problems
- **Calibrated:** Severity reflects actual implementation impact
- **Complete:** Check every applicable item, don't skip viewpoints
- **Framework-aware:** Respect the architecture methodology being used
- **Debt-conscious:** Surface technical debt signals for proactive management
- **Actionable:** Every gap should have a clear path to resolution

---

## 10. References

| File | Purpose |
|------|---------|
| `references/architecture-standards.md` | TOGAF, C4, arc42, IEEE 42010 frameworks |
| `references/architecture-checklist.md` | 188 checklist items organized by viewpoint |
| `references/viewpoint-catalog.md` | 14 viewpoint definitions with concerns |
| `references/quality-attributes.md` | ISO 25010 quality model with validation |
| `references/technical-debt-indicators.md` | 25+ debt signals with detection |
| `references/anti-patterns-catalog.md` | 25 architecture anti-patterns |
| `references/compliance-frameworks.md` | SOC2, GDPR, PCI-DSS requirements |

### External References

| File | Purpose |
|------|---------|
| `@core/artifact-contracts.yaml` | CONTRACT-07 (GAP-INVENTORY) schema |
| `@core/scoring-rubrics.yaml` | RUBRIC-07 (SEVERITY-SCORING) specification |
| `@core/technique-taxonomy.yaml` | Perfect Recall techniques (CAT-PR-GA) |
| `@core/skill-patterns.yaml` | GAP-AUDIT pattern (PATTERN-08) |

---

## 11. Templates

| File | Purpose |
|------|---------|
| `templates/gap-inventory-output.md` | CONTRACT-07 compliant XML template with architecture extensions |
| `templates/architecture-health-report.md` | Executive dashboard with viewpoint scores |
| `templates/debt-remediation-roadmap.md` | Prioritized technical debt paydown plan |

---

## 12. Examples

### Example 1: ADR Audit

```yaml
input:
  document: "[ADR-047: Adopt Event-Driven Architecture for Order Processing]"
  document_type: adr
  framework: auto
  audit_depth: standard
  include_anti_patterns: true

flow:
  phase_1:
    - Framework: Custom (MADR-like structure detected)
    - Loaded ADR-focused checklist (V10: 20 items)
    - Parsed: Title, Status, Context, Decision, Consequences
  phase_2:
    - Primary viewpoint: V10 (Decision Record)
    - Secondary viewpoints assessed: V2 (Container), V6 (Integration)
    - Structural gap: No explicit alternatives section
  phase_3:
    - Verified 20 ADR items + 15 related items
    - 28 PRESENT + CLEAR
    - 4 PARTIAL
    - 3 ABSENT
  phase_4:
    - Quality attributes: Performance EXPLICIT, Scalability IMPLICIT, Reliability MISSING
  phase_5:
    - 7 gaps classified
    - 0 CRITICAL
    - 2 HIGH: Missing rollback strategy (V10-15), No SLO impact assessment (V10-18)
    - 3 MEDIUM: Vague consequences (V10-10), Missing stakeholder sign-off (V10-20)
    - 2 LOW: No review date (V10-19)
    - Anti-patterns: AA-10 (partial - alternatives not documented)
  phase_6:
    - Architecture Health Score: 72 (ADEQUATE)
    - ADR ready with minor gaps

output:
  total_gaps: 7
  by_severity: { critical: 0, high: 2, medium: 3, low: 2 }
  health_score: 72
  health_status: ADEQUATE
  overall_assessment: minor_issues
  recommendation: "Address rollback strategy and SLO impact before implementation."
```

### Example 2: C4 System Context Audit

```yaml
input:
  document: "[System Context Diagram + Description for Payment Gateway]"
  document_type: system_context
  framework: c4
  audit_depth: standard
  viewpoints: [V1, V6, V7]

flow:
  phase_1:
    - Framework: C4 (Level 1 - System Context)
    - Loaded Context-focused checklist (52 items)
    - Parsed: Diagram, external actors, integrations
  phase_2:
    - V1 (Context): Full coverage
    - V6 (Integration): Partial coverage
    - V7 (Security): Minimal coverage
    - Structural gap: Trust boundaries not defined
  phase_3:
    - Verified 52 items
    - 38 PRESENT
    - 8 PARTIAL
    - 6 ABSENT
  phase_4:
    - Security: MISSING (trust boundaries undefined)
    - Interoperability: EXPLICIT
    - Reliability: IMPLICIT
  phase_5:
    - 14 gaps classified
    - 2 CRITICAL: No trust boundaries (V1-09), External auth flow missing (V7-01)
    - 4 HIGH: SLA dependencies undocumented (V1-13), API versioning unclear (V6-05)
    - 5 MEDIUM
    - 3 LOW
    - Anti-patterns: AA-22 (Trust Assumption)
  phase_6:
    - Architecture Health Score: 58 (AT_RISK)
    - C4 Level 1 incomplete for security context

output:
  total_gaps: 14
  by_severity: { critical: 2, high: 4, medium: 5, low: 3 }
  health_score: 58
  health_status: AT_RISK
  c4_maturity: { level_1_complete: false }
  blocking_issues: 2
  overall_assessment: significant_gaps
  recommendation: "CRITICAL: Define trust boundaries and external auth flows before container design."
```

### Example 3: Comprehensive Design Document Audit

```yaml
input:
  document: "[Design Doc: Inventory Management Service Redesign - 12,000 words]"
  document_type: design_doc
  framework: arc42
  audit_depth: exhaustive
  include_debt_assessment: true
  governance_context: enterprise

flow:
  phase_1:
    - Framework: arc42 (11 of 12 sections present)
    - Loaded full checklist (188 items)
    - Parsed: 24 sections, 8 diagrams, 5 ADRs inline
  phase_2:
    - All 10 core viewpoints assessed
    - Conditional V11 (Multi-tenancy) applicable
    - V8 (Operations) weakest coverage
    - V10 (Decisions) strong with 5 ADRs
  phase_3:
    - Verified 188 items
    - 142 PRESENT
    - 28 PARTIAL
    - 18 ABSENT
  phase_4:
    - All 8 quality attributes assessed
    - Security: EXPLICIT
    - Performance: EXPLICIT
    - Reliability: IMPLICIT (needs SLOs)
    - Operability: MISSING
  phase_5:
    - 46 gaps classified
    - 1 CRITICAL: No disaster recovery strategy (V4-20)
    - 8 HIGH: Missing monitoring strategy (V8-01), SLOs undefined (V8-05)
    - 22 MEDIUM
    - 15 LOW
    - Anti-patterns: AA-17 (Observability Omission), AA-18 (SLO Silence)
    - Technical debt: 8 indicators detected
      - TD-D01: Diagrams >6 months stale
      - TD-A03: No bounded contexts defined
      - TD-I02: Manual deployment steps
  phase_6:
    - Architecture Health Score: 64 (ADEQUATE)
    - Compliance gap: SOC2 monitoring requirements not met

output:
  total_gaps: 46
  by_severity: { critical: 1, high: 8, medium: 22, low: 15 }
  anti_patterns_detected: 2
  debt_indicators_detected: 8
  health_score: 64
  health_status: ADEQUATE
  by_viewpoint:
    V1: 2 gaps, V2: 4 gaps, V3: 3 gaps, V4: 6 gaps
    V5: 4 gaps, V6: 5 gaps, V7: 3 gaps, V8: 12 gaps
    V9: 4 gaps, V10: 2 gaps, V11: 1 gap
  blocking_issues: 1
  overall_assessment: significant_gaps
  recommendation: "Address DR strategy (CRITICAL) and operability gaps before architecture review board."
  debt_remediation:
    immediate: ["DR strategy", "Monitoring strategy"]
    short_term: ["SLO definition", "Deployment automation"]
    medium_term: ["Diagram refresh", "Bounded context documentation"]
```

---

## Quick Start

```
/architecture-doc-auditor
document: "[Paste architecture document or provide file path]"
document_type: design_doc
audit_depth: standard
```
