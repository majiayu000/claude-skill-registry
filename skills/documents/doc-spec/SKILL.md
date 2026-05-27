---
name: doc-spec
description: Create Technical Specifications (SPEC) - Layer 10 artifact using YAML format for implementation-ready specifications
tags:
  - sdd-workflow
  - layer-10-artifact
  - shared-architecture
custom_fields:
  layer: 10
  artifact_type: SPEC
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD,PRD,EARS,BDD,ADR,SYS,REQ,IMPL,CTR]
  downstream_artifacts: [TASKS, IPLAN, Code]
---

# doc-spec

## Purpose

Create **Technical Specifications (SPEC)** - Layer 10 artifact in the SDD workflow that defines implementation-ready specifications in YAML format, providing complete technical details for code generation.

**Layer**: 10

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5), SYS (Layer 6), REQ (Layer 7), IMPL (Layer 8), CTR (Layer 9)

**Downstream Artifacts**: TASKS (Layer 11), IPLAN (Layer 12), Code (Layer 13)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ docs/ADR/ docs/SYS/ docs/REQ/ docs/IMPL/ docs/CTR/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating SPEC, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream REQ**: Read atomic requirements (PRIMARY SOURCE)
3. **Upstream CTR**: Read contracts if Layer 9 created
4. **Template**: `ai_dev_flow/SPEC/SPEC-TEMPLATE.yaml`
5. **Creation Rules**: `ai_dev_flow/SPEC/SPEC_CREATION_RULES.md`
6. **Validation Rules**: `ai_dev_flow/SPEC/SPEC_VALIDATION_RULES.md`
7. **Validation Script**: `./ai_dev_flow/scripts/validate_spec_template.sh` (under development - use template for manual validation until available)

## Reserved ID Exemption (SPEC-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `SPEC-00_*.md`, `SPEC-00_*.yaml`

**Document Types**:
- Index documents (`SPEC-00_index.md`)
- Traceability matrix templates (`SPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

**Rationale**: Reserved ID 000 documents are framework infrastructure (indexes, templates, reference materials), not project artifacts requiring traceability or quality gates.

**Validation Behavior**: Skip all checks when filename matches `SPEC-00_*` pattern.

## When to Use This Skill

Use `doc-spec` when:
- Have completed BRD through REQ (Layers 1-7)
- Ready to create implementation-ready specifications
- Preparing for code generation or implementation
- Need complete technical details in structured format
- You are at Layer 10 of the SDD workflow

## SPEC-Specific Guidance

### 1. YAML Format (MANDATORY)

**Format**: Pure YAML (not markdown)

**Structure**:
```yaml
# SPEC-NN: [Specification Title]

metadata:
  spec_id: SPEC-01
  title: "Order Validation Service Specification"
  version: "1.0.0"
  created_date: "2025-01-15"
  updated_date: "2025-01-15"
  status: "approved"
  owner: "team-backend"
  task_ready_score: "✅ 95% (Target: ≥90%)"

cumulative_tags:
  brd: ["BRD.01.01.03"]
  prd: ["PRD.01.07.02"]
  ears: ["EARS.01.25.01"]
  bdd: ["BDD.01.14.01"]
  adr: ["ADR-033", "ADR-045"]
  sys: ["SYS.01.26.01"]
  req: ["REQ.01.27.01"]
  impl: ["IMPL.01.29.01"]  # optional
  contracts: ["CTR-01"]  # optional

overview:
  purpose: "Define trade order validation service implementation"
  scope: "Validate trade orders against position limits and business rules"
  requirements:
    - "REQ-risk-limits-01"
    - "REQ-risk-limits-02"

architecture:
  pattern: "layered"
  layers:
    - name: "controller"
      technology: "FastAPI"
      description: "REST API endpoint handlers"
    - name: "service"
      technology: "Python"
      description: "Business logic and validation"
    - name: "repository"
      technology: "SQLAlchemy"
      description: "Database access layer"

interfaces:
  api_endpoints:
    - endpoint: "/api/v1/trades/validate"
      method: "POST"
      contract_ref: "CTR-01"
      authentication: "Bearer token"
      rate_limit: "@threshold: PRD.NN.limit.api.requests_per_second"
      rate_limit_window: "1min"

  data_models:
    - model: "TradeOrderRequest"
      schema_ref: "CTR-01#/components/schemas/TradeOrderRequest"
    - model: "ValidationResponse"
      schema_ref: "CTR-01#/components/schemas/ValidationResponse"

implementation:
  modules:
    - name: "controllers/trade_validation_controller.py"
      purpose: "API endpoint handlers"
      dependencies: ["services/trade_validator.py"]

    - name: "services/trade_validator.py"
      purpose: "Business logic and validation"
      dependencies:
        - "repositories/position_repository.py"
        - "models/trade_order.py"

    - name: "repositories/position_repository.py"
      purpose: "Database access for positions"
      dependencies: ["database/connection.py"]

  functions:
    - name: "validate_trade_order"
      module: "services/trade_validator.py"
      signature: "async def validate_trade_order(order: TradeOrderRequest) -> ValidationResponse"
      purpose: "Validate trade order against all rules"
      algorithm:
        - "1. Validate symbol exists"
        - "2. Check quantity is positive"
        - "3. Validate price within range"
        - "4. Check position limits"
        - "5. Return validation result"

error_handling:
  error_codes:
    - code: "INVALID_SYMBOL"
      http_status: 400
      message: "Symbol not found in approved list"
      recovery: "user_correction"

    - code: "LIMIT_EXCEEDED"
      http_status: 403
      message: "Position limit exceeded"
      recovery: "reduce_position"

configuration:
  environment_variables:
    - name: "MAX_POSITION_DELTA"
      type: "float"
      default: "0.50"
      required: true

  feature_flags:
    - name: "enable_strict_validation"
      default: false
      description: "Enable enhanced validation rules"

testing:
  unit_tests:
    - test: "test_validate_valid_order"
      module: "tests/unit/test_trade_validator.py"
      coverage_target: 95

  integration_tests:
    - test: "test_validation_endpoint"
      module: "tests/integration/test_trade_api.py"

  performance_tests:
    - test: "test_validation_latency"
      target: "P95 < 50ms"

deployment:
  container:
    image: "trade-validator:1.0.0"
    base: "python:3.11-slim"

  resources:
    cpu: "1000m"
    memory: "512Mi"

  scaling:
    min_replicas: 2
    max_replicas: 10
    target_cpu: 70

monitoring:
  metrics:
    - name: "validation_latency_ms"
      type: "histogram"
      labels: ["endpoint", "status"]

    - name: "validation_errors_total"
      type: "counter"
      labels: ["error_code"]

  alerts:
    - alert: "HighValidationLatency"
      condition: "P95 > 100ms"
      severity: "warning"

traceability:
  upstream_sources:
    - artifact: "BRD-01"
      sections: ["section-3"]
    - artifact: "PRD-01"
      sections: ["feature-2"]
    - artifact: "REQ-risk-limits-01"
      sections: ["all"]

  downstream_artifacts:
    - "TASKS-01"
    - "IPLAN-01"
    - "Code: src/services/trade_validator.py"
```

### 2. Element ID Format (MANDATORY)

**Pattern**: `SPEC.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Step | 15 | SPEC.02.15.01 |
| Interface | 16 | SPEC.02.16.01 |
| Data Model | 17 | SPEC.02.17.01 |
| Validation Rule | 21 | SPEC.02.21.01 |
| Specification Element | 28 | SPEC.02.28.01 |

> **REMOVED PATTERNS** - Do NOT use legacy formats:
> - `STEP-XXX` - Use `SPEC.NN.15.SS` instead
> - `IF-XXX` or `INT-XXX` - Use `SPEC.NN.16.SS` instead
> - `DM-XXX` or `MODEL-XXX` - Use `SPEC.NN.17.SS` instead
> - `VR-XXX` - Use `SPEC.NN.21.SS` instead

**Reference**: [ID_NAMING_STANDARDS.md - Cross-Reference Link Format](../ai_dev_flow/ID_NAMING_STANDARDS.md#cross-reference-link-format-mandatory)

### 3. Required Top-Level Sections

**MANDATORY Sections**:
1. **metadata**: Spec ID, title, version, dates, status, owner, task_ready_score
2. **cumulative_tags**: All upstream tags (7-9 tags depending on layers)
3. **overview**: Purpose, scope, requirements
4. **architecture**: Pattern, layers, technologies
5. **interfaces**: API endpoints, data models
6. **implementation**: Modules, functions, algorithms
7. **error_handling**: Error codes, HTTP status, recovery
8. **configuration**: Environment variables, feature flags
9. **testing**: Unit, integration, performance tests
10. **deployment**: Container, resources, scaling
11. **monitoring**: Metrics, alerts, logging
12. **traceability**: Upstream sources, downstream artifacts

### 4. TASKS-Ready Scoring System

**Purpose**: Measures SPEC maturity and readiness for progression to TASKS implementation planning.

**Format in Metadata**:
```yaml
metadata:
  task_ready_score: "✅ 95% (Target: ≥90%)"
```

**Status and TASKS-Ready Score Mapping**:

| TASKS-Ready Score | Required Status |
|-------------------|-----------------|
| ≥90% | approved |
| 70-89% | in_review |
| <70% | draft |

**Scoring Criteria**:
- **YAML Completeness (25%)**: All metadata fields, traceability chain, all sections populated
- **Interface Definitions (25%)**: External APIs with CTR contracts, internal interfaces, data schemas
- **Implementation Specifications (25%)**: Behavior enables code generation, performance/security quantifiable
- **Code Generation Readiness (25%)**: Machine-readable fields, TASKS-ready metadata

**Quality Gate**: Score <90% prevents TASKS artifact creation.

### 5. Threshold Registry Integration

**Purpose**: Prevent magic numbers by referencing centralized threshold registry.

**When @threshold Tag is Required**: Use for ALL quantitative values that are:
- Performance configurations (latencies, throughput, IOPS)
- Timeout configurations (connection, read, write timeouts)
- Rate limiting values (requests per second, burst limits)
- Resource limits (memory, CPU, storage)
- Circuit breaker configurations

**@threshold Tag Format in YAML**:
```yaml
# String value format
performance:
  p95_latency_ms: "@threshold: PRD.NN.perf.api.p95_latency"

# Comment format for documentation
timeout:
  request_ms: 5000  # @threshold: PRD.NN.timeout.request.sync
```

**Invalid (hardcoded values)**:
```yaml
performance:
  p95_latency_ms: 200
timeout:
  request_ms: 5000
rate_limit:
  requests_per_second: 100
```

**Valid (registry references)**:
```yaml
performance:
  p95_latency_ms: "@threshold: PRD.NN.perf.api.p95_latency"
timeout:
  request_ms: "@threshold: PRD.NN.timeout.request.sync"
rate_limit:
  requests_per_second: "@threshold: PRD.NN.limit.api.requests_per_second"
```

### 6. cumulative_tags Field (CRITICAL)

**CRITICAL**: SPEC must include cumulative_tags section with ALL upstream tags

**Element Type Codes for Cumulative Tags**:
| Tag | Artifact | Element Type | Code |
|-----|----------|--------------|------|
| brd | BRD | Business Requirement | 01 |
| prd | PRD | Product Feature | 07 |
| ears | EARS | EARS Statement | 25 |
| bdd | BDD | Scenario | 14 |
| adr | ADR | Document reference | (dash notation) |
| sys | SYS | System Requirement | 26 |
| req | REQ | Atomic Requirement | 27 |
| impl | IMPL | Implementation Phase | 29 |
| contracts | CTR | Document reference | (dash notation) |

**Format (maximum - IMPL and CTR included)**:
```yaml
cumulative_tags:
  brd: ["BRD.01.01.03", "BRD.01.01.05"]
  prd: ["PRD.01.07.02", "PRD.01.07.15"]
  ears: ["EARS.01.25.01", "EARS.01.25.02"]
  bdd: ["BDD.01.14.01"]
  adr: ["ADR-033", "ADR-045"]
  sys: ["SYS.01.26.01", "SYS.01.26.07"]
  req: ["REQ.01.27.01"]
  impl: ["IMPL.01.29.01"]
  contracts: ["CTR-01"]
```

**Format (minimum - IMPL and CTR skipped)**:
```yaml
cumulative_tags:
  brd: ["BRD.01.01.03"]
  prd: ["PRD.01.07.02"]
  ears: ["EARS.01.25.01"]
  bdd: ["BDD.01.14.01"]
  adr: ["ADR-033", "ADR-045"]
  sys: ["SYS.01.26.01"]
  req: ["REQ.01.27.01"]
```

**Tag Count**: 7-9 tags (minimum 7, maximum 9)

### 7. contract_ref Field

**Purpose**: Link SPEC to CTR (if Layer 9 created)

**Format**:
```yaml
interfaces:
  api_endpoints:
    - endpoint: "/api/v1/trades/validate"
      method: "POST"
      contract_ref: "CTR-01"  # Link to contract
      contract_path: "#/paths/~1api~1v1~1trades~1validate/post"  # JSON Pointer

  data_models:
    - model: "TradeOrderRequest"
      schema_ref: "CTR-01#/components/schemas/TradeOrderRequest"
```

### 8. Implementation Readiness

**100% Implementation-Ready**: SPEC must contain ALL information needed to write code

**Checklist**:
- [ ] All modules identified with file paths
- [ ] All functions identified with signatures
- [ ] All algorithms documented step-by-step
- [ ] All data models linked to schemas
- [ ] All error codes defined
- [ ] All configuration specified
- [ ] All tests specified
- [ ] Deployment requirements complete

## Tag Format Convention (By Design)

The SDD framework uses two distinct notation systems for cross-references:

| Notation | Format        | Artifacts                               | Purpose                                                             |
|----------|---------------|----------------------------------------|---------------------------------------------------------------------|
| Dash     | TYPE-NN      | ADR, SPEC, CTR, IPLAN, ICON            | Technical artifacts - references to files/documents                 |
| Dot      | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, IMPL, TASKS | Hierarchical artifacts - references to elements inside documents |

**Key Distinction**:
- `@adr: ADR-033` → Points to the document `ADR-033_risk_limit_enforcement.md`
- `@brd: BRD.17.01.01` → Points to element 01.01 inside document `BRD-017.md`

## Unified Element ID Format (MANDATORY)

**For hierarchical requirements (BRD, PRD, EARS, BDD, SYS, REQ, IMPL)**:
- **Always use**: `TYPE.NN.TT.SS` (dot separator, 4-segment unified format)
- **Never use**: `TYPE-NN:NNN` (colon separator - DEPRECATED)
- **Never use**: `TYPE.NN.TT` (3-segment format - DEPRECATED)

Examples:
- `@brd: BRD.17.01.01` ✅
- `@brd: BRD.017.001` ❌ (old 3-segment format)

## Validation Checks

### Tier 1: Errors (Blocking)

| Check | Description |
|-------|-------------|
| CHECK 1 | YAML Syntax Validation (parseable) |
| CHECK 2 | Required Metadata Fields (version, status, task_ready_score) |
| CHECK 3 | TASKS-Ready Score format (✅ emoji + percentage + target) |
| CHECK 4 | Complete Traceability Chain (cumulative_tags section) |
| CHECK 5 | Element ID Format (`SPEC.NN.TT.SS`) |

### Tier 2: Warnings (Recommended)

| Check | Description |
|-------|-------------|
| CHECK 6 | Interface Specifications (CTR contract references) |
| CHECK 7 | Implementation Readiness (code generation enabling) |
| CHECK 8 | Code Generation Compatibility (TASKS creation) |

### Tier 3: Info

| Check | Description |
|-------|-------------|
| CHECK 9 | Threshold Registry Integration (@threshold references) |
| CHECK 10 | Performance benchmarks defined |

## Upstream/Downstream Artifacts

**Upstream Sources**:
- **BRD** (Layer 1) - Business requirements
- **PRD** (Layer 2) - Product features
- **EARS** (Layer 3) - Formal requirements
- **BDD** (Layer 4) - Test scenarios
- **ADR** (Layer 5) - Architecture decisions
- **SYS** (Layer 6) - System requirements
- **REQ** (Layer 7) - Atomic requirements (PRIMARY SOURCE)
- **IMPL** (Layer 8) - Implementation approach (optional)
- **CTR** (Layer 9) - Data contracts (optional)

**Downstream Artifacts**:
- **TASKS** (Layer 11) - Task breakdown
- **IPLAN** (Layer 12) - Implementation plans
- **Code** (Layer 13) - Implementation

**Same-Type Document Relationships** (conditional):
- `@related-spec: SPEC-NN` - SPECs sharing implementation context
- `@depends-spec: SPEC-NN` - SPEC that must be implemented first

## Creation Process

### Step 1: Read Upstream Artifacts

Focus on REQ (Layer 7) and optionally CTR (Layer 9).

### Step 2: Reserve ID Number

Check `docs/SPEC/` for next available ID number (or create `docs/SPEC/` directory if first SPEC).

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: SPEC-01, SPEC-99, SPEC-102
- ❌ Incorrect: SPEC-001, SPEC-009 (extra leading zero not required)

### Step 3: Create SPEC File

**File naming**: `docs/SPEC/SPEC-NN_{slug}.yaml`

**Example**: `docs/SPEC/SPEC-01_trade_validation.yaml`

**IMPORTANT**: Pure YAML format (NOT markdown)

**Note**: Templates and examples are in `ai_dev_flow/SPEC/` while project-specific SPECs go in `docs/SPEC/`.

### Step 4: Fill Metadata Section

Complete spec_id, title, version, dates, status, owner, task_ready_score.

### Step 5: Add Cumulative Tags

Include all 7-9 upstream tags (brd through req/impl/contracts).

### Step 6: Define Overview

Purpose, scope, and requirements list.

### Step 7: Specify Architecture

Pattern, layers, and technologies (reference ADR decisions).

### Step 8: Define Interfaces

API endpoints (with contract_ref), data models (with schema_ref).

### Step 9: Document Implementation

Modules (file paths), functions (signatures), algorithms (step-by-step).

### Step 10: Specify Error Handling

Error codes, HTTP status, messages, recovery procedures.

### Step 11: Define Configuration

Environment variables, feature flags, defaults. Use @threshold for quantitative values.

### Step 12: Specify Testing

Unit tests, integration tests, performance tests with targets.

### Step 13: Define Deployment

Container, resources, scaling, environment.

### Step 14: Add Monitoring

Metrics, alerts, logging requirements.

### Step 15: Add Traceability

Upstream sources and downstream artifacts.

### Step 16: Create/Update Traceability Matrix

**MANDATORY**: Create or update `docs/SPEC/SPEC-00_TRACEABILITY_MATRIX.md` (use template from `ai_dev_flow/SPEC/SPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`)

### Step 17: Validate SPEC

```bash
# YAML validation
yamllint docs/SPEC/SPEC-01_*.yaml

# Schema validation (use SPEC_SCHEMA.yaml as reference)
# Manual: Compare against ai_dev_flow/SPEC/SPEC_SCHEMA.yaml structure

# Cumulative tagging validation
python ai_dev_flow/scripts/validate_tags_against_docs.py --artifact SPEC-01 --expected-layers brd,prd,ears,bdd,adr,sys,req,impl,contracts --strict

# Cross-document validation
python ai_dev_flow/scripts/validate_cross_document.py --document docs/SPEC/SPEC-01_*.yaml
```

### Step 18: Commit Changes

Commit SPEC file and traceability matrix.

## Validation

### Automated Validation

```bash
# YAML validation
yamllint docs/SPEC/SPEC-01_*.yaml

# Schema validation (use SPEC_SCHEMA.yaml as reference)
# Manual: Compare against ai_dev_flow/SPEC/SPEC_SCHEMA.yaml structure

# Cumulative tagging validation
python ai_dev_flow/scripts/validate_tags_against_docs.py \
  --artifact SPEC-01 \
  --expected-layers brd,prd,ears,bdd,adr,sys,req,impl,contracts \
  --strict

# Cross-document validation
python ai_dev_flow/scripts/validate_cross_document.py --document docs/SPEC/SPEC-01_*.yaml
```

### Manual Checklist

- [ ] Pure YAML format (not markdown)
- [ ] Metadata section complete with task_ready_score
- [ ] cumulative_tags section with 7-9 upstream tags
- [ ] Overview defines purpose and scope
- [ ] Architecture references ADR decisions
- [ ] Interfaces link to CTR (if Layer 9 created)
- [ ] Implementation specifies modules with file paths
- [ ] Functions have signatures and algorithms
- [ ] Error handling complete
- [ ] Configuration uses @threshold for quantitative values
- [ ] Testing requirements defined
- [ ] Deployment requirements complete
- [ ] Monitoring specified
- [ ] Traceability links to upstream/downstream
- [ ] 100% implementation-ready
- [ ] Element IDs use `SPEC.NN.TT.SS` format

### Diagram Standards
All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Common Pitfalls

1. **Markdown format**: SPEC must be pure YAML, not markdown
2. **Missing cumulative_tags**: Must include all 7-9 upstream tags
3. **No contract_ref**: Must link to CTR if Layer 9 created
4. **Vague implementation**: Must specify exact file paths and signatures
5. **Missing algorithms**: Functions need step-by-step algorithms
6. **Incomplete**: Must be 100% implementation-ready
7. **Hardcoded values**: Use @threshold for performance/timeout/rate limits
8. **Wrong element IDs**: Use `SPEC.NN.TT.SS`, not legacy `STEP-XXX`, `IF-XXX`, `DM-XXX`
9. **Wrong cumulative tag codes**: Use correct element type codes (EARS=25, BDD=14, SYS=26, REQ=27, IMPL=29)

## Post-Creation Validation (MANDATORY - NO CONFIRMATION)

**CRITICAL**: Execute this validation loop IMMEDIATELY after document creation. Do NOT proceed to next document until validation passes.

### Automatic Validation Loop

```
LOOP:
  1. Run: python ai_dev_flow/scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed
```

### Validation Command

```bash
# Per-document validation (Phase 1)
python ai_dev_flow/scripts/validate_cross_document.py --document docs/SPEC/SPEC-NN_slug.yaml --auto-fix

# Layer validation (Phase 2) - run when all SPEC documents complete
python ai_dev_flow/scripts/validate_cross_document.py --layer SPEC --auto-fix
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| SPEC (Layer 10) | @brd, @prd, @ears, @bdd, @adr, @sys, @req (+ @impl, @ctr if created) | 7-9 tags |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing upstream tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
| Broken link | Recalculate path from current location |
| Missing traceability section | Insert from template |

### Validation Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| XDOC-001 | Referenced requirement ID not found | ERROR |
| XDOC-002 | Missing cumulative tag | ERROR |
| XDOC-003 | Upstream document not found | ERROR |
| XDOC-006 | Tag format invalid | ERROR |
| XDOC-007 | Gap in cumulative tag chain | ERROR |
| XDOC-009 | Missing traceability section | ERROR |

### Quality Gate

**Blocking**: YES - Cannot proceed to next document until Phase 1 validation passes with 0 errors.

---

## Next Skill

After creating SPEC, use:

**`doc-tasks`** - Create Task Breakdown (Layer 11)

The TASKS will:
- Reference this SPEC as upstream source
- Include all 8-10 upstream tags
- Break SPEC into actionable tasks
- Provide AI-structured TODO format

## Reference Documents

SPEC artifacts do not support REF documents. Reference documents are limited to **BRD and ADR types only** per the SDD framework.

For supplementary documentation needs, create:
- **BRD-REF**: Business context documentation
- **ADR-REF**: Technical reference guides (API quick references, implementation guides)

## Related Resources

- **Template**: `ai_dev_flow/10_SPEC/SPEC-TEMPLATE.yaml` (primary authority)
- **SPEC Creation Rules**: `ai_dev_flow/10_SPEC/SPEC_CREATION_RULES.md`
- **SPEC Validation Rules**: `ai_dev_flow/10_SPEC/SPEC_VALIDATION_RULES.md`
- **SPEC Schema**: `ai_dev_flow/10_SPEC/SPEC_SCHEMA.yaml`
- **SPEC README**: `ai_dev_flow/10_SPEC/README.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`

## Quick Reference

**SPEC Purpose**: Implementation-ready technical specifications

**Layer**: 10

**Element ID Format**: `SPEC.NN.TT.SS`
- Step = 15
- Interface = 16
- Data Model = 17
- Validation Rule = 21
- Specification Element = 28

**Removed Patterns**: STEP-XXX, IF-XXX, INT-XXX, DM-XXX, MODEL-XXX, VR-XXX

**Tags Required**: @brd through @req/impl/contracts (7-9 tags)

**Format**: Pure YAML (not markdown)

**Key Features**:
- cumulative_tags section (CRITICAL)
- contract_ref field (links to CTR)
- schema_ref field (links to data models)
- @threshold references for quantitative values
- 100% implementation-ready
- All modules, functions, algorithms specified

**TASKS-Ready Score**: ≥90% required for "approved" status

**Quality Gate**: Must be 100% implementation-ready

**Next**: doc-tasks
