---
name: gap-analysis-workflow
description: Identify capability gaps and propose new skills with prioritization. Use when analyzing missing capabilities, planning skill development, performing ontology expansion, or assessing coverage.
argument-hint: "[goal] [scope] [constraints]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash, Edit, Git, Web
context: fork
agent: general-purpose
---

## Intent

Run the composed workflow **gap-analysis-workflow** using atomic capability skills to systematically identify what capabilities are missing and prioritize their development.

**Success criteria:**
- Current capability coverage mapped with evidence
- Gaps identified with clear justification
- Relationships between existing and missing capabilities documented
- Prioritized roadmap for new skill development
- Audit trail of analysis process

**Compatible schemas:**
- `reference/capability_ontology.yaml`
- `reference/workflow_catalog.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `goal` | Yes | string | The analysis objective (e.g., "identify gaps for autonomous deployment") |
| `scope` | Yes | string\|array | Domain, layer, or capability set to analyze |
| `constraints` | No | object | Limits (e.g., max new skills, priority criteria, timeline) |
| `reference_ontology` | No | string | Path to reference ontology for comparison |
| `existing_capabilities` | No | array | List of already-implemented capabilities |

## Procedure

0) **Create checkpoint marker** if mutation might occur:
   - Create `.claude/checkpoint.ok` after confirming rollback strategy

1) **Invoke `/inspect`** and store output as `inspect_out`
   - Examine current capability landscape and documentation

2) **Invoke `/map-relationships`** and store output as `map-relationships_out`
   - Map dependencies and connections between existing capabilities

3) **Invoke `/discover-relationship`** and store output as `discover-relationship_out`
   - Identify implicit relationships and missing links

4) **Invoke `/compare-plans`** and store output as `compare-plans_out`
   - Compare current state against ideal or reference ontology

5) **Invoke `/prioritize`** and store output as `prioritize_out`
   - Rank gaps by impact, effort, and strategic value

6) **Invoke `/generate-plan`** and store output as `generate-plan_out`
   - Create development roadmap for new capabilities

7) **Invoke `/audit`** and store output as `audit_out`
   - Record analysis process and evidence

## Output Contract

Return a structured object:

```yaml
workflow_id: string  # Unique analysis execution ID
goal: string  # Analysis objective
status: completed | partial | failed
current_state:
  capabilities_analyzed: integer
  coverage_percentage: number  # 0.0-1.0
  layers_covered: array[string]
  evidence_anchors: array[string]
gaps_identified:
  total: integer
  by_layer:
    perception: array[string]
    modeling: array[string]
    reasoning: array[string]
    action: array[string]
    safety: array[string]
    meta: array[string]
  by_priority:
    critical: array[string]
    high: array[string]
    medium: array[string]
    low: array[string]
  evidence_anchors: array[string]
relationships:
  existing_dependencies: array[object]
  missing_connections: array[object]
  orphan_capabilities: array[string]
  evidence_anchors: array[string]
comparison:
  reference_ontology: string
  alignment_score: number  # 0.0-1.0
  divergences: array[string]
  evidence_anchors: array[string]
roadmap:
  phases: array[object]
  total_new_skills: integer
  estimated_effort: string
  dependencies: array[object]
  evidence_anchors: array[string]
audit:
  log_path: string
  methodology: string
  evidence_anchors: array[string]
confidence: number  # 0.0-1.0
evidence_anchors: array[string]
assumptions: array[string]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | Unique identifier for this analysis |
| `current_state` | object | Summary of existing capability coverage |
| `gaps_identified` | object | Missing capabilities organized by layer and priority |
| `relationships` | object | Dependency mapping including missing connections |
| `comparison` | object | Alignment with reference ontology |
| `roadmap` | object | Phased development plan for new skills |
| `audit` | object | Analysis methodology and evidence trail |
| `confidence` | number | 0.0-1.0 based on evidence completeness |
| `evidence_anchors` | array | All evidence references collected |
| `assumptions` | array | Explicit assumptions made during analysis |

## Examples

### Example 1: Gap Analysis for Autonomous Code Review

**Input:**
```yaml
goal: "Identify gaps for fully autonomous code review capability"
scope:
  - "reasoning"
  - "safety"
  - "action"
constraints:
  max_new_skills: 10
  priority_criteria:
    - "security_impact"
    - "automation_potential"
reference_ontology: "schemas/capability_ontology.yaml"
```

**Output:**
```yaml
workflow_id: "gap_20240115_120000_codereview"
goal: "Identify gaps for fully autonomous code review capability"
status: completed
current_state:
  capabilities_analyzed: 45
  coverage_percentage: 0.72
  layers_covered:
    - "reasoning"
    - "safety"
    - "action"
  evidence_anchors:
    - "file:schemas/capability_ontology.yaml"
    - "file:skills/critique/SKILL.md"
gaps_identified:
  total: 8
  by_layer:
    perception: []
    modeling:
      - "detect-code-smell"
      - "identify-security-pattern"
    reasoning:
      - "compare-implementations"
      - "evaluate-test-coverage"
    action:
      - "generate-review-comment"
      - "apply-suggested-fix"
    safety:
      - "verify-no-regression"
      - "constrain-auto-merge"
    meta: []
  by_priority:
    critical:
      - "verify-no-regression"
      - "identify-security-pattern"
    high:
      - "detect-code-smell"
      - "constrain-auto-merge"
    medium:
      - "compare-implementations"
      - "generate-review-comment"
    low:
      - "evaluate-test-coverage"
      - "apply-suggested-fix"
  evidence_anchors:
    - "file:schemas/capability_ontology.yaml:nodes"
    - "tool:compare-plans:coverage_analysis"
relationships:
  existing_dependencies:
    - from: "critique"
      to: "evaluate"
      type: "requires"
    - from: "plan"
      to: "critique"
      type: "soft_requires"
  missing_connections:
    - from: "detect-code-smell"
      to: "critique"
      type: "should_precede"
      reason: "Code smells inform critique priorities"
    - from: "verify-no-regression"
      to: "act-plan"
      type: "must_follow"
      reason: "Regression check required after any code change"
  orphan_capabilities: []
  evidence_anchors:
    - "tool:map-relationships:dependency_graph"
    - "tool:discover-relationship:implicit_links"
comparison:
  reference_ontology: "schemas/capability_ontology.yaml"
  alignment_score: 0.72
  divergences:
    - "Missing specialized detection capabilities for code patterns"
    - "No automated fix application in action layer"
    - "Regression verification not formalized"
  evidence_anchors:
    - "tool:compare-plans:ontology_diff"
roadmap:
  phases:
    - phase: 1
      name: "Security Foundation"
      skills:
        - "identify-security-pattern"
        - "verify-no-regression"
      rationale: "Critical for safe autonomous operation"
    - phase: 2
      name: "Detection Enhancement"
      skills:
        - "detect-code-smell"
        - "constrain-auto-merge"
      rationale: "Improves review quality and safety"
    - phase: 3
      name: "Automation Expansion"
      skills:
        - "compare-implementations"
        - "generate-review-comment"
        - "evaluate-test-coverage"
        - "apply-suggested-fix"
      rationale: "Full autonomous review capability"
  total_new_skills: 8
  estimated_effort: "2-3 sprints"
  dependencies:
    - skill: "apply-suggested-fix"
      requires: ["verify-no-regression", "constrain-auto-merge"]
  evidence_anchors:
    - "tool:prioritize:impact_matrix"
    - "tool:generate-plan:roadmap"
audit:
  log_path: ".claude/audit/gap_20240115_120000_codereview.log"
  methodology: "Systematic comparison against reference ontology with layer-by-layer analysis"
  evidence_anchors:
    - "file:.claude/audit/gap_20240115_120000_codereview.log"
confidence: 0.85
evidence_anchors:
  - "file:schemas/capability_ontology.yaml"
  - "tool:map-relationships:dependency_graph"
  - "tool:compare-plans:ontology_diff"
  - "tool:prioritize:impact_matrix"
assumptions:
  - "Reference ontology is current and complete"
  - "Existing skills are correctly implemented"
  - "Priority criteria reflect actual business needs"
```

**Evidence pattern:** Ontology comparison, dependency graph analysis, impact-based prioritization.

## Verification

- [ ] **Coverage Analyzed**: All capabilities in scope examined
- [ ] **Gaps Documented**: Each gap has layer classification and priority
- [ ] **Relationships Mapped**: Dependencies and missing connections identified
- [ ] **Comparison Complete**: Alignment score computed against reference
- [ ] **Roadmap Generated**: Phased plan with dependencies
- [ ] **Audit Trail**: Analysis methodology documented

**Verification tools:** Read (for ontology files), Grep (for capability search), Bash (for validation)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not create new skills during analysis (discovery only)
- Validate all capability references against ontology
- Document assumptions about missing capabilities
- Flag potential security implications of gaps
- Preserve existing ontology structure

## Composition Patterns

**Commonly follows:**
- `inspect` - After initial codebase exploration
- `retrieve` - After fetching reference documentation

**Commonly precedes:**
- `generate-plan` - To create detailed skill specifications
- `prioritize` - To refine gap prioritization
- `summarize` - To create executive summary

**Anti-patterns:**
- Never skip relationship mapping before prioritization
- Never propose skills without checking ontology for existing alternatives
- Never prioritize without defined criteria
- Never generate roadmap without dependency analysis

**Workflow references:**
- See `reference/workflow_catalog.yaml#gap-analysis-workflow` for step definitions
- See `reference/capability_ontology.yaml` for reference structure
