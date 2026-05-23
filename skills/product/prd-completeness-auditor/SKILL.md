---
name: prd-completeness-auditor
version: "2.0"
description: >
  Systematic completeness audit of Product Requirements Documents using
  100+ item MECE checklist, severity-classified gap detection, and anti-pattern scanning.
  PROACTIVELY activate for: (1) PRD review before development handoff,
  (2) Requirements completeness assessment, (3) Identifying ambiguous requirements,
  (4) PRD template validation, (5) Finding missing stakeholder needs,
  (6) Detecting inconsistent acceptance criteria.
  Triggers: "audit PRD", "review requirements", "check PRD completeness",
  "validate requirements document", "PRD review", "requirements audit",
  "find gaps in PRD", "requirements completeness check", "PRD quality check"
---

# PRD Completeness Auditor

A systematic audit system that evaluates Product Requirements Documents against a comprehensive 116-item checklist, detecting gaps, classifying severity, identifying anti-patterns, and generating actionable remediation plans. Implements the GAP-AUDIT pattern (PATTERN-08) to produce CONTRACT-07 compliant GAP-INVENTORY output.

---

## 1. Purpose

This skill provides 12 core capabilities:

| # | Capability | Phase | Description |
|---|------------|-------|-------------|
| 1 | **Reference Load** | 1 | Load PRD checklist and calibrate to document type |
| 2 | **Document Parse** | 1 | Extract PRD structure and section boundaries |
| 3 | **MECE Map** | 2 | Apply 10-dimension coverage framework to PRD sections |
| 4 | **Item-by-Item Verify** | 3 | Check each of 116 checklist items against PRD content |
| 5 | **Gap Detect** | 3 | Identify missing, incomplete, or ambiguous elements |
| 6 | **Classify Gap Type** | 4 | Categorize gaps using 6-type taxonomy |
| 7 | **Score Severity** | 4 | Apply RUBRIC-07 (impact, likelihood, detectability) |
| 8 | **Anti-Pattern Scan** | 4 | Detect 15+ known PRD anti-patterns |
| 9 | **Evidence Cite** | 4 | Link each gap to specific PRD location with evidence |
| 10 | **Impact Assess** | 5 | Evaluate downstream development impact per gap |
| 11 | **Remediate Suggest** | 5 | Generate fix recommendations from pattern catalog |
| 12 | **Synthesize Report** | 6 | Produce GAP-INVENTORY + executive summary + remediation plan |

---

## 2. When to Use

**Ideal for:**
- Reviewing PRDs before development handoff
- Assessing requirements completeness for sprint planning
- Validating PRD against organizational standards
- Pre-flight check before stakeholder sign-off
- Identifying gaps that could cause scope creep
- Auditing legacy PRDs for maintenance or migration
- Quality gate before technical design phase

**Avoid when:**
- PRD is in early ideation phase (too early for formal audit)
- Document is not a PRD (use appropriate auditor)
- PRD author is unavailable for clarification on gaps
- Quick brainstorm or exploration (formal audit adds overhead)
- Document is a technical spec, not product requirements

---

## 3. Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prd_content` | string | **yes** | — | PRD document content or file reference |
| `prd_type` | enum | no | `feature` | feature \| epic \| product \| initiative |
| `audit_depth` | enum | no | `standard` | quick \| standard \| comprehensive |
| `severity_threshold` | enum | no | `all` | critical_only \| high_and_above \| all |
| `focus_areas` | list | no | `all` | Specific sections to emphasize in audit |
| `include_anti_patterns` | boolean | no | `true` | Whether to scan for PRD anti-patterns |
| `output_format` | enum | no | `full` | full \| executive \| remediation_only |

### PRD Type Effects

| Type | Checklist Items | Focus Areas |
|------|-----------------|-------------|
| **feature** | 106 items | User stories, acceptance criteria, functional requirements |
| **epic** | 106 items | Cross-feature dependencies, phasing, rollout strategy |
| **product** | 100 items | Strategic alignment, market context, success metrics |
| **initiative** | 92 items | Business case, organizational impact, stakeholders |

### Audit Depth Effects

| Depth | Behavior |
|-------|----------|
| **quick** | High-priority items only (40 items), structural gaps, no anti-patterns |
| **standard** | Full checklist, anti-patterns, standard remediation |
| **comprehensive** | Full checklist, deep anti-pattern analysis, detailed remediation with templates |

---

## 4. Six-Phase Workflow

### Phase 1: Reference Loading & Context

**Purpose:** Load checklist and establish audit context.

**Steps:**
1. Receive PRD content (inline or file reference)
2. Load `prd-requirements-checklist.md` reference
3. Calibrate checklist based on `prd_type`:
   - Filter items by applicability matrix
   - Adjust severity levels for document type
   - Set critical items that must be present
4. Parse PRD to identify structure:
   - Extract section headers and hierarchy
   - Identify section boundaries
   - Note document format (markdown, docx, wiki)
5. Load `mece-coverage-framework.md` for structural validation
6. Initialize gap tracking structure with empty findings

**Techniques Used:**
- `document_structure_extraction` - Parse document hierarchy
- `checklist_calibration` - Adjust criteria for context

**Quality Gate:** Checklist calibrated for PRD type; PRD structure parsed with sections identified

**Output:** Calibrated checklist (N items) + PRD structure map

---

### Phase 2: MECE Scope Mapping

**Purpose:** Map PRD sections to coverage dimensions and identify structural gaps.

**Steps:**
1. Load 10 MECE coverage dimensions from `mece-coverage-framework.md`:
   - D1: Problem Space
   - D2: User Context
   - D3: Business Context
   - D4: Solution Requirements
   - D5: User Experience
   - D6: Quality Criteria
   - D7: Dependencies
   - D8: Risk Landscape
   - D9: Execution Context
   - D10: Technical Fit
2. Map each PRD section to exactly one dimension:
   - Assign based on content, not just header
   - Flag orphan sections (don't fit any dimension)
   - Flag missing dimensions (no sections mapped)
3. Identify structural gaps:
   - Dimension with no coverage = CRITICAL structural gap
   - Dimension with partial coverage = SIGNIFICANT structural gap
4. Note sections present but outside standard structure
5. Calculate initial coverage score per dimension

**Techniques Used:**
- `mece_gap_detection` (CAT-PR-GA) - Identify coverage gaps in structure
- `completeness_verification` (CAT-PR-GA) - Verify all dimensions addressed

**Quality Gate:** All 10 MECE dimensions assessed; structural gaps flagged

**Output:** Coverage mapping with dimension scores and structural gap list

---

### Phase 3: Item-by-Item Verification

**Purpose:** Verify each checklist item against PRD content.

**Steps:**

For each checklist item (PC-01 through TC-08):

```
1. LOCATE RELEVANT SECTION
   └─ Based on dimension mapping from Phase 2

2. ASSESS PRESENCE
   ├─ PRESENT: Item clearly addressed
   ├─ PARTIAL: Item mentioned but incomplete
   └─ ABSENT: No evidence of item

3. EVALUATE QUALITY (if present)
   ├─ CLEAR: Unambiguous and actionable
   ├─ AMBIGUOUS: Multiple interpretations possible
   ├─ INCONSISTENT: Contradicts other content
   ├─ INCOMPLETE: Missing key details
   └─ OUTDATED: Stale information

4. RECORD EVIDENCE
   ├─ Location: Section/line reference
   ├─ Quote: Supporting text from PRD
   └─ Assessment: Pass/fail with rationale

5. FLAG FOR GAP CLASSIFICATION (if needed)
   └─ Any non-PRESENT or non-CLEAR items
```

**Verification Rules by Section:**

| Section | Items | Critical Items | Verification Approach |
|---------|-------|----------------|----------------------|
| Problem & Context | PC-01 to PC-15 | PC-01, PC-02, PC-05 | Check for evidence-backed problem |
| User & Stakeholder | US-01 to US-12 | US-01, US-02, US-05 | Verify persona specificity |
| Goals & Success | GS-01 to GS-10 | GS-01, GS-02, GS-03 | Check measurability |
| Requirements | RQ-01 to RQ-18 | RQ-01, RQ-02, RQ-05 | Verify testability |
| User Stories | ST-01 to ST-14 | ST-01, ST-02 | Check INVEST compliance |
| Acceptance Criteria | AC-01 to AC-12 | AC-01, AC-02, AC-03 | Verify Gherkin-like structure |
| Dependencies | DP-01 to DP-08 | DP-01, DP-02 | Check bidirectional links |
| Risks & Assumptions | RA-01 to RA-10 | RA-01, RA-02 | Verify mitigation plans |
| Timeline & Scope | TS-01 to TS-09 | TS-01, TS-04, TS-05 | Check explicit boundaries |
| Technical | TC-01 to TC-08 | TC-01 (if applicable) | Verify feasibility notes |

**Techniques Used:**
- `completeness_verification` (CAT-PR-GA) - Check presence of each item
- `negative_space_analysis` (CAT-PR-GA) - Identify what's NOT said
- `exhaustive_edge_case_enumeration` (CAT-PR-CE) - Find uncovered scenarios

**Quality Gate:** 100% of applicable checklist items evaluated

**Output:** Verification matrix with item-level results and evidence

---

### Phase 4: Gap Classification & Severity Scoring

**Purpose:** Classify detected gaps and score severity using RUBRIC-07.

**Steps:**

#### 4.1 Gap Classification

For each gap identified in Phase 3, apply gap taxonomy (from `gap-taxonomy.md`):

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
    │       │       │       ├─ IS IT FACTUALLY CORRECT?
    │       │       │       │   ├─ NO → INCORRECT
    │       │       │       │   └─ YES
    │       │       │       │       └─ IS IT CURRENT?
    │       │       │       │           ├─ NO → OUTDATED
    │       │       │       │           └─ YES → No gap
```

#### 4.2 Severity Scoring

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

#### 4.3 Anti-Pattern Scan

If `include_anti_patterns` is true, scan for 15+ patterns from `anti-patterns-catalog.md`:

| ID | Anti-Pattern | Severity | Detection Signal |
|----|--------------|----------|------------------|
| AP-01 | Scope Creep Enabler | HIGH | No "Out of Scope" section |
| AP-02 | Solution Contamination | CRITICAL | HOW before WHAT |
| AP-03 | Stakeholder Soup | MEDIUM | Undefined decision authority |
| AP-04 | Metric-Free Zone | HIGH | No success metrics |
| AP-05 | Assumption Blindness | HIGH | No assumptions listed |
| AP-06 | Edge Case Avoidance | MEDIUM | Happy path only |
| AP-07 | Dependency Denial | CRITICAL | No external dependencies |
| AP-08 | Timeline Fantasy | HIGH | Unrealistic milestones |
| AP-09 | Acceptance Vagueness | CRITICAL | Non-testable criteria |
| AP-10 | User Story Stuffing | MEDIUM | Giant epics as stories |
| AP-11 | Risk Minimization | HIGH | No risk register |
| AP-12 | Technical Debt Deferral | MEDIUM | No technical constraints |
| AP-13 | Stakeholder Exclusion | HIGH | Missing key personas |
| AP-14 | Scope Definition Deficit | CRITICAL | No explicit boundaries |
| AP-15 | Priority Inflation | MEDIUM | Everything is P0 |

#### 4.4 Evidence Linking

For each gap and anti-pattern:
- Cite specific PRD location (section, line)
- Quote relevant text as evidence
- Note what's missing vs. what's present
- Link to checklist item ID

**Techniques Used:**
- `severity_scoring` (RUBRIC-07) - Score gaps by impact
- `full_consistency_matrix` (CAT-PR-ECR) - Cross-reference for inconsistencies
- `anti_pattern_detection` - Match known failure patterns

**Quality Gate:** All gaps classified with type and severity; anti-patterns checked

**Output:** Classified gap list with severity scores and evidence

---

### Phase 5: Impact Assessment & Remediation

**Purpose:** Assess downstream impact and generate remediation recommendations.

**Steps:**

#### 5.1 Impact Assessment

For each gap, assess development impact:

| Impact Type | Description | Example |
|-------------|-------------|---------|
| **BLOCKING** | Cannot proceed to development | No user definition |
| **DEGRADING** | Will cause rework or quality issues | Vague acceptance criteria |
| **COSMETIC** | Minor polish, can address later | Formatting inconsistencies |

#### 5.2 Remediation Matching

Match each gap to remediation pattern from `remediation-patterns.md`:

| Gap Type | Primary Pattern | Action |
|----------|-----------------|--------|
| MISSING | Add Content | Write new section using template |
| INCOMPLETE | Expand Content | Fill in missing details |
| INCONSISTENT | Reconcile Content | Resolve contradictions |
| AMBIGUOUS | Clarify Content | Add specificity/metrics |
| INCORRECT | Correct Content | Fix factual errors |
| OUTDATED | Update Content | Refresh stale information |

#### 5.3 Effort Estimation

Estimate remediation effort:

| Effort Level | Definition | Time Range |
|--------------|------------|------------|
| **trivial** | Quick fix, obvious solution | < 30 min |
| **small** | Clear scope, single section | 30 min - 2 hours |
| **medium** | Multiple sections or research needed | 2 - 8 hours |
| **large** | Significant rework or stakeholder input | 1+ days |

#### 5.4 Priority Assignment

Assign remediation priority:

| Priority | Criteria | Timeline |
|----------|----------|----------|
| **immediate** | CRITICAL gaps, blocks development | Before any dev work |
| **short_term** | HIGH gaps, causes significant rework | Before sprint start |
| **long_term** | MEDIUM gaps, degrades quality | During development |
| **optional** | LOW gaps, nice-to-have | When convenient |

#### 5.5 Blocking Issues Identification

Flag blocking issues that MUST be resolved:
- All CRITICAL severity gaps
- Any gap that prevents scope understanding
- Dependencies that can't be validated
- Acceptance criteria that can't be tested

**Techniques Used:**
- `impact_chain_analysis` - Trace downstream effects
- `remediation_pattern_matching` - Match to fix templates

**Quality Gate:** All CRITICAL and HIGH gaps have remediation paths

**Output:** Remediation recommendations per gap with effort and priority

---

### Phase 6: Synthesis & Output Generation

**Purpose:** Produce final GAP-INVENTORY artifact and optional summaries.

**Steps:**

#### 6.1 GAP-INVENTORY Compilation

Compile all findings into CONTRACT-07 compliant structure:
- Populate `source_reference` with PRD identifier
- Set `source_type` to "document"
- Build `audit_criteria` with checklist reference
- Compile `gaps` array with all classified gaps
- Add `anti_patterns` array if detected
- Calculate `summary` statistics

#### 6.2 Summary Statistics

Generate:
- `total_gaps`: Count of all gaps
- `by_severity`: {critical: N, high: N, medium: N, low: N}
- `by_category`: {missing: N, incomplete: N, inconsistent: N, ...}
- `overall_assessment`: Based on gap profile
- `blocking_issues`: List of gap IDs that must be fixed
- `coverage_score`: Percentage of checklist items passed

**Assessment Thresholds:**

| Assessment | Criteria |
|------------|----------|
| **critical_issues** | Any CRITICAL gap OR >5 HIGH gaps |
| **significant_gaps** | No CRITICAL but >3 HIGH gaps |
| **minor_issues** | No CRITICAL, <=3 HIGH, some MEDIUM/LOW |
| **acceptable** | No CRITICAL/HIGH, only MEDIUM/LOW |
| **excellent** | <5 total gaps, all LOW |

#### 6.3 Executive Summary (if requested)

Generate stakeholder-friendly summary:
- At-a-glance metrics table
- Traffic light status by section
- Top 3 strengths
- Top 3 critical issues
- Recommended next actions

#### 6.4 Remediation Plan (if requested)

Generate prioritized action plan:
- Priority 1: Immediate (blocking issues)
- Priority 2: Short-term (before development)
- Priority 3: During development
- Priority 4: Optional improvements
- Tracking table with owners and status

#### 6.5 Output Selection

Based on `output_format` parameter:
- **full**: GAP-INVENTORY + Executive Summary + Remediation Plan
- **executive**: Executive Summary only
- **remediation_only**: Remediation Plan only

**Techniques Used:**
- `artifact_synthesis` - Compile structured output
- `stakeholder_communication` - Tailor for audience

**Quality Gate:** Output validates against CONTRACT-07 schema

**Output:** GAP-INVENTORY artifact + requested summaries

---

## 5. Gap Taxonomy

### The 6 Gap Types

| # | Type | Definition | Detection Signal | Remediation |
|---|------|------------|------------------|-------------|
| 1 | **MISSING** | Required element completely absent | No section/content found | Add content |
| 2 | **INCOMPLETE** | Present but lacking required detail | TBD, TODO, truncated | Expand content |
| 3 | **INCONSISTENT** | Contradicts other PRD sections | Conflicting statements | Reconcile content |
| 4 | **AMBIGUOUS** | Multiple interpretations possible | Vague terms, no metrics | Clarify content |
| 5 | **INCORRECT** | Factually wrong information | Technical impossibilities | Correct content |
| 6 | **OUTDATED** | Was correct but no longer current | References deprecated items | Update content |

**Reference:** See `references/gap-taxonomy.md` for detailed detection heuristics and examples.

---

## 6. Output Specifications

### 6.1 GAP-INVENTORY Format

Aligns with CONTRACT-07 from artifact-contracts.yaml.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gap_inventory contract="CONTRACT-07" version="1.0">

  <metadata>
    <artifact_id>GI-[YYYY-MM-DD]-[5-char-hash]</artifact_id>
    <contract_type>GAP-INVENTORY</contract_type>
    <created_at>[ISO 8601]</created_at>
    <created_by>prd-completeness-auditor</created_by>
    <confidence>[0.0-1.0]</confidence>
    <provenance>
      <source_artifact>[PRD identifier]</source_artifact>
      <audit_date>[ISO 8601 date]</audit_date>
      <audit_depth>[quick|standard|comprehensive]</audit_depth>
      <prd_type>[feature|epic|product|initiative]</prd_type>
      <checklist_version>1.0</checklist_version>
      <items_checked>[N]</items_checked>
    </provenance>
  </metadata>

  <source_reference>[PRD document identifier]</source_reference>
  <source_type>document</source_type>

  <audit_criteria>
    <checklist_reference>prd-requirements-checklist.md v1.0</checklist_reference>
    <criteria_list>
      <criterion id="[PC-01]">[Item description]</criterion>
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
      <checklist_ref>[PC-01]</checklist_ref>
      <location>[PRD section/line]</location>
      <description>[Gap description]</description>
      <evidence>[What indicates this gap]</evidence>
      <impact>[Consequence if not addressed]</impact>
      <remediation>
        <recommendation>[How to fix]</recommendation>
        <pattern_ref>[RP-PC-01]</pattern_ref>
        <effort>[trivial|small|medium|large]</effort>
        <priority>[immediate|short_term|long_term|optional]</priority>
      </remediation>
    </gap>
  </gaps>

  <anti_patterns>
    <pattern id="AP-02">
      <name>Solution Contamination</name>
      <instances>
        <instance location="[section]">[Quote]</instance>
      </instances>
      <remediation>[How to address]</remediation>
    </pattern>
  </anti_patterns>

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
    <anti_patterns_detected>[N]</anti_patterns_detected>
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

```markdown
# PRD Audit Summary: [PRD Title]

**Audit Date:** [Date]
**PRD Type:** [Type]
**Overall Assessment:** [STATUS]

## At a Glance

| Metric | Value |
|--------|-------|
| Total Gaps | [N] |
| Critical Issues | [N] |
| Blocking Issues | [N] |
| Checklist Coverage | [X%] |
| Ready for Development | [YES/NO/WITH CONDITIONS] |

## Key Findings

### Strengths
1. **[Strength]:** [Description]
2. **[Strength]:** [Description]

### Critical Issues (Must Fix)
1. **[Issue]:** [Description] — Fix: [Action]

## Recommendation
[Next steps summary]
```

### 6.3 Remediation Plan Format

```markdown
# PRD Remediation Plan: [PRD Title]

## Priority 1: Immediate

| # | Gap | Category | Effort | Action |
|---|-----|----------|--------|--------|
| 1 | GAP-XXX | [type] | [effort] | [action] |

### Detailed Actions
[Per-gap remediation with templates]

## Priority 2: Short-Term
[Same structure]

## Tracking
| Gap ID | Priority | Target Date | Owner | Status |
|--------|----------|-------------|-------|--------|
```

**Reference:** See `templates/` directory for complete templates with examples.

---

## 7. Quality Gates

| # | Gate | Criterion | Phase |
|---|------|-----------|-------|
| 1 | **Checklist Calibrated** | Checklist adjusted for PRD type with applicable items identified | 1 |
| 2 | **PRD Parsed** | All sections identified with structure map created | 1 |
| 3 | **MECE Mapped** | All 10 coverage dimensions assessed with scores | 2 |
| 4 | **Items Verified** | 100% of applicable checklist items evaluated | 3 |
| 5 | **Gaps Classified** | All gaps assigned type from 6-type taxonomy | 4 |
| 6 | **Severity Scored** | All gaps scored using 3-dimension RUBRIC-07 | 4 |
| 7 | **Anti-Patterns Scanned** | All 15+ anti-patterns checked (if enabled) | 4 |
| 8 | **Remediation Assigned** | All CRITICAL/HIGH gaps have remediation paths | 5 |
| 9 | **Output Validated** | GAP-INVENTORY conforms to CONTRACT-07 schema | 6 |

---

## 8. Workflow Integration

This skill serves as a quality gate in the product development workflow:

```
┌─────────────────────────────────────┐
│     PRD COMPLETENESS AUDITOR        │  ◀── THIS SKILL
│                                     │
└────────────────┬────────────────────┘
                 │
                 │ Input: PRD Document
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 1: Reference Loading         │
│  • Load prd-requirements-checklist  │
│  • Calibrate for prd_type           │
│  • Parse PRD structure              │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 2: MECE Scope Mapping        │
│  • Apply 10-dimension framework     │
│  • Map sections to dimensions       │
│  • Flag structural gaps             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 3: Item-by-Item Verification │  ◀── Perfect Recall techniques
│  • Check 116 checklist items        │      mece_gap_detection
│  • Record presence and quality      │      completeness_verification
│  • Cite evidence locations          │      negative_space_analysis
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 4: Gap Classification        │  ◀── RUBRIC-07 severity scoring
│  • Apply 6-type gap taxonomy        │
│  • Score severity (3 dimensions)    │
│  • Scan for 15+ anti-patterns       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 5: Impact & Remediation      │
│  • Assess development impact        │
│  • Match to remediation patterns    │
│  • Identify blocking issues         │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Phase 6: Synthesis                 │  ◀── CONTRACT-07 output
│  • Compile GAP-INVENTORY            │
│  • Generate executive summary       │
│  • Create remediation plan          │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  OUTPUT: GAP-INVENTORY              │
│  + Executive Summary                │
│  + Remediation Plan                 │
└─────────────────────────────────────┘
```

### Artifact Flow

| This Skill Produces | Consumed By |
|---------------------|-------------|
| GAP-INVENTORY (CONTRACT-07) | Product owner review, development planning |
| Executive Summary | Stakeholder communication, go/no-go decisions |
| Remediation Plan | PRD author, product team action items |

### Integration Points

| Upstream | This Skill | Downstream |
|----------|------------|------------|
| PRD authoring | **Audit** | Technical design |
| Requirements gathering | **Validate** | Sprint planning |
| Stakeholder interviews | **Check quality** | Development handoff |

---

## 9. Behavioral Guidelines

- **Systematic not judgmental:** Report gaps objectively, not as criticism
- **Evidence-based:** Every gap must have cited evidence from the PRD
- **Constructive:** Focus on remediation, not just problems
- **Calibrated:** Severity reflects actual development impact
- **Complete:** Check every applicable item, don't skip
- **Efficient:** Match audit depth to context needs
- **Actionable:** Every gap should have a clear path to resolution

---

## 10. References

| File | Purpose |
|------|---------|
| `references/prd-requirements-checklist.md` | 116 checklist items organized by PRD section |
| `references/severity-classification.md` | RUBRIC-07 implementation with scoring dimensions |
| `references/gap-taxonomy.md` | 6 gap types with detection heuristics |
| `references/remediation-patterns.md` | Fix patterns catalog by gap type and section |
| `references/anti-patterns-catalog.md` | 15+ PRD anti-patterns with detection signals |
| `references/mece-coverage-framework.md` | 10 coverage dimensions for PRD audits |

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
| `templates/gap-inventory-output.md` | CONTRACT-07 compliant XML template with field guidance |
| `templates/executive-summary-output.md` | Stakeholder summary template with traffic lights |
| `templates/remediation-plan-output.md` | Prioritized action plan template with tracking |

---

## 12. Examples

### Example 1: Standard Feature PRD Audit

```yaml
input:
  prd_content: "[Feature PRD for checkout optimization - 2500 words]"
  prd_type: feature
  audit_depth: standard
  include_anti_patterns: true
  output_format: full

flow:
  phase_1:
    - Loaded feature checklist (106 items applicable)
    - Parsed PRD: 12 sections identified
    - Structure: Problem → Users → Goals → Requirements → Stories → AC
  phase_2:
    - Mapped to 10 MECE dimensions
    - D7 (Dependencies) has no coverage → structural gap
    - D8 (Risk Landscape) minimal coverage → structural gap
  phase_3:
    - Verified 106 items
    - 78 PRESENT + CLEAR
    - 12 PARTIAL
    - 16 ABSENT
  phase_4:
    - 28 gaps classified
    - 2 CRITICAL: No acceptance criteria for error handling (AC-05), No dependencies listed (DP-01)
    - 5 HIGH: Vague success metrics (GS-03), Missing edge cases (RQ-08, ST-07)
    - 9 MEDIUM: Incomplete user personas (US-03, US-04)
    - 12 LOW: Minor formatting, optional items
    - Anti-patterns: AP-07 (Dependency Denial), AP-06 (Edge Case Avoidance)
  phase_5:
    - 2 blocking issues identified
    - Remediation assigned to all CRITICAL/HIGH
    - Total remediation effort: ~6 hours
  phase_6:
    - Generated GAP-INVENTORY (CONTRACT-07 compliant)
    - Generated Executive Summary
    - Generated Remediation Plan with 4 priority tiers

output:
  total_gaps: 28
  by_severity: { critical: 2, high: 5, medium: 9, low: 12 }
  blocking_issues: 2
  overall_assessment: significant_gaps
  coverage_score: 73%
  recommendation: "Address 2 critical gaps before development. Estimated effort: 2-3 hours for blocking issues."
```

### Example 2: Comprehensive Epic PRD Audit

```yaml
input:
  prd_content: "[Epic PRD for payment platform redesign - 8000 words]"
  prd_type: epic
  audit_depth: comprehensive
  include_anti_patterns: true
  output_format: full

flow:
  phase_1:
    - Loaded epic checklist (106 items)
    - Parsed PRD: 18 sections, complex hierarchy
    - Noted: Multiple phased releases defined
  phase_2:
    - All 10 dimensions covered
    - D4 (Solution Requirements) heavily weighted
    - Cross-phase dependencies complex
  phase_3:
    - Verified 106 items
    - 82 PRESENT
    - 14 PARTIAL
    - 10 ABSENT
  phase_4:
    - 24 gaps classified
    - 1 CRITICAL: Phase 2 dependencies on Phase 1 unclear (DP-03)
    - 7 HIGH: Rollback strategy missing (RA-05), Migration path vague (TC-04)
    - 10 MEDIUM: User stories too large (ST-08), Success metrics per phase unclear
    - 6 LOW: Documentation gaps
    - Anti-patterns: AP-10 (User Story Stuffing), AP-01 (Scope Creep Enabler)
  phase_5:
    - 1 blocking issue
    - Comprehensive remediation with templates
    - Recommended: Break Phase 2 into sub-phases
  phase_6:
    - Full GAP-INVENTORY with 24 detailed entries
    - Executive Summary with phase-by-phase assessment
    - Detailed Remediation Plan with 15 action items

output:
  total_gaps: 24
  by_severity: { critical: 1, high: 7, medium: 10, low: 6 }
  anti_patterns_detected: 2
  blocking_issues: 1
  overall_assessment: significant_gaps
  coverage_score: 77%
  recommendation: "Critical: Clarify Phase 1→2 dependencies before architecture work begins."
```

### Example 3: Quick Focused Audit

```yaml
input:
  prd_content: "[Product PRD for mobile app v2.0 - 4000 words]"
  prd_type: product
  audit_depth: quick
  focus_areas: [acceptance_criteria, success_metrics]
  include_anti_patterns: false
  output_format: executive

flow:
  phase_1:
    - Loaded quick checklist (40 high-priority items)
    - Filtered to focus areas: AC-01 to AC-12, GS-01 to GS-10 (22 items)
  phase_2:
    - Quick dimension scan
    - D6 (Quality Criteria) and D3 (Business Context) targeted
  phase_3:
    - Verified 22 items in focus areas
    - 14 PRESENT
    - 5 PARTIAL
    - 3 ABSENT
  phase_4:
    - 8 gaps in focus areas
    - 0 CRITICAL
    - 2 HIGH: Success metrics not measurable (GS-03), AC missing for API endpoints (AC-07)
    - 4 MEDIUM
    - 2 LOW
  phase_5:
    - Quick remediation notes
    - Estimated effort: 2-3 hours
  phase_6:
    - Executive Summary only (per output_format)

output:
  total_gaps: 8
  focus_areas_checked: [acceptance_criteria, success_metrics]
  by_severity: { critical: 0, high: 2, medium: 4, low: 2 }
  overall_assessment: minor_issues
  coverage_score: 64% (in focus areas)
  recommendation: "Good foundation. Refine success metrics with quantifiable targets before launch planning."
```

---

## Quick Start

```
/prd-completeness-auditor
prd_content: "[Paste PRD or provide file path]"
prd_type: feature
audit_depth: standard
```
