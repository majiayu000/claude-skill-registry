---
name: doc-tasks
description: Create Task Breakdown (TASKS) - Layer 11 artifact decomposing SPEC into AI-structured TODO tasks
tags:
  - sdd-workflow
  - layer-11-artifact
  - shared-architecture
custom_fields:
  layer: 11
  artifact_type: TASKS
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD,PRD,EARS,BDD,ADR,SYS,REQ,IMPL,CTR,SPEC]
  downstream_artifacts: [IPLAN]
---

# doc-tasks

## Purpose

Create **Task Breakdown (TASKS)** - Layer 11 artifact in the SDD workflow that decomposes SPEC into actionable, AI-structured TODO tasks for implementation.

**Layer**: 11

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5), SYS (Layer 6), REQ (Layer 7), IMPL (Layer 8), CTR (Layer 9), SPEC (Layer 10)

**Downstream Artifacts**: IPLAN (Layer 12), Code (Layer 13)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ docs/ADR/ docs/SYS/ docs/REQ/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating TASKS, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream SPEC**: Read technical specifications (PRIMARY SOURCE)
3. **Template**: `ai_dev_flow/TASKS/TASKS-TEMPLATE.md`
4. **Creation Rules**: `ai_dev_flow/TASKS/TASKS_CREATION_RULES.md`
5. **Validation Rules**: `ai_dev_flow/TASKS/TASKS_VALIDATION_RULES.md`
6. **Validation Script**: `./ai_dev_flow/scripts/validate_tasks.sh`
7. **Implementation Contracts Guide**: `ai_dev_flow/TASKS/IMPLEMENTATION_CONTRACTS_GUIDE.md`

## When to Use This Skill

Use `doc-tasks` when:
- Have completed BRD through SPEC (Layers 1-10)
- Ready to break down SPEC into actionable tasks
- Preparing for implementation planning (Layer 12)
- Need structured TODO format for AI agents
- You are at Layer 11 of the SDD workflow

## Reserved ID Exemption (TASKS-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `TASKS-00_*.md`

**Document Types**:
- Index documents (`TASKS-00_index.md`)
- Traceability matrix templates (`TASKS-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Implementation contracts checklists (`TASKS-00_IMPLEMENTATION_CONTRACTS_CHECKLIST.md`)
- Glossaries, registries

**Rationale**: Reserved ID 000 documents are framework infrastructure (indexes, templates, reference materials), not project artifacts requiring traceability or quality gates.

**Validation Behavior**: Skip all checks when filename matches `TASKS-00_*` pattern.

## Element ID Format (MANDATORY)

**Pattern**: `TASKS.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Task | 18 | TASKS.02.18.01 |
| Task Item | 30 | TASKS.02.30.01 |

> **REMOVED PATTERNS** - Do NOT use:
> - `TASK-XXX` → Use `TASKS.NN.18.SS`
> - `T-XXX` → Use `TASKS.NN.18.SS`
>
> **Reference**: [ID_NAMING_STANDARDS.md — Cross-Reference Link Format](../ID_NAMING_STANDARDS.md#cross-reference-link-format-mandatory)

**Fix**: Replace `### TASK-01: Implementation` with `### TASKS.02.18.01: Implementation`

## TASKS-Specific Guidance

### 1. AI-Structured TODO Format

**Purpose**: Break SPEC into tasks consumable by AI coding agents

**Format**:
```markdown
## Tasks

### Phase 1: Project Setup (3 tasks)

**TASKS.01.18.01: Initialize Project Structure**
- **Action**: Create directory structure per SPEC architecture
- **Files to Create**:
  - `src/controllers/data_validation_controller.py`
  - `src/services/data_validator.py`
  - `src/repositories/data_repository.py`
  - `src/models/data_request.py`
- **Dependencies**: None
- **Estimated Effort**: 30 minutes
- **SPEC Reference**: SPEC-01:implementation.modules
- **Success Criteria**: All directories and empty files created

**TASKS.01.18.02: Set Up Development Environment**
- **Action**: Configure Python environment and dependencies
- **Files to Create**: `requirements.txt`, `pyproject.toml`
- **Dependencies**: TASKS.01.18.01
- **Estimated Effort**: 1 hour
- **SPEC Reference**: SPEC-01:deployment.container
- **Success Criteria**: `pip install -r requirements.txt` succeeds

### Phase 2: Data Models (2 tasks)

**TASKS.01.18.03: Implement DataRequest Model**
- **Action**: Create Pydantic model per CTR-01 schema
- **Files to Modify**: `src/models/data_request.py`
- **Dependencies**: TASKS.01.18.02
- **Estimated Effort**: 1 hour
- **SPEC Reference**: SPEC-01:interfaces.data_models
- **CTR Reference**: CTR-01#/components/schemas/DataRequest
- **Success Criteria**: Model validates per schema, unit tests pass
```

### 2. Required Sections

**Document Control** (MANDATORY - First section before all numbered sections)

**Core Sections**:
1. **Overview**: Summary of task breakdown
2. **Task Hierarchy**: Phases and task groups
3. **Tasks**: Detailed task breakdown (primary content)
4. **Dependencies Graph**: Visual task dependencies (Mermaid diagram)
5. **Effort Summary**: Total effort by phase
6. **Traceability**: Section 7 format with cumulative tags
7. **Implementation Contracts**: Section 8 (MANDATORY) - Contracts provided/consumed

### 3. Task Numbering Format

**Format**: `TASKS.{SPEC-ID}.18.{SEQ}` (unified element ID format)

**Example**: `TASKS.01.18.03` means:
- SPEC-01 (from SPEC-01_data_validation.yaml)
- Element type 18 (Task)
- Sequence 03 (third task in breakdown)

**Benefits**:
- Links task directly to SPEC
- Unique task IDs across project
- Easy to reference in commits

### 4. Task Fields (Required)

**Each task MUST include**:

1. **Task ID**: TASKS.{SPEC-ID}.18.{SEQ}
2. **Title**: Short description (5-10 words)
3. **Action**: What to do (imperative form)
4. **Files to Create/Modify**: Specific file paths
5. **Dependencies**: Other TASK IDs (or "None")
6. **Estimated Effort**: Time estimate
7. **SPEC Reference**: Section in SPEC (e.g., SPEC-01:implementation.modules)
8. **Success Criteria**: How to verify completion
9. **Optional: CTR Reference**: Link to contract if applicable

### 5. Phase Organization

**Typical Phases**:

1. **Phase 1: Project Setup** (infrastructure, environment)
2. **Phase 2: Data Models** (schemas, models, validation)
3. **Phase 3: Business Logic** (services, core algorithms)
4. **Phase 4: API Layer** (controllers, endpoints)
5. **Phase 5: Error Handling** (error codes, middleware)
6. **Phase 6: Configuration** (env vars, feature flags)
7. **Phase 7: Testing** (unit, integration, performance)
8. **Phase 8: Deployment** (Docker, CI/CD, monitoring)

### 6. Dependencies Graph

**Use Mermaid diagram ONLY** (text-based diagrams prohibited per `ai_dev_flow/DIAGRAM_STANDARDS.md`):

```markdown
## Dependencies Graph

```mermaid
graph TD
    T001[TASKS.01.18.01: Project Setup]
    T002[TASKS.01.18.02: Dev Environment]
    T003[TASKS.01.18.03: DataRequest Model]
    T004[TASKS.01.18.04: ValidationResponse Model]
    T005[TASKS.01.18.05: Data Repository]
    T006[TASKS.01.18.06: Data Validator Service]
    T007[TASKS.01.18.07: API Controller]

    T001 --> T002
    T002 --> T003
    T002 --> T004
    T002 --> T005
    T003 --> T006
    T004 --> T006
    T005 --> T006
    T006 --> T007
```
```

### 7. Effort Summary

**Format**:
```markdown
## Effort Summary

| Phase | Tasks | Total Effort |
|-------|-------|--------------|
| Phase 1: Project Setup | 2 | 1.5 hours |
| Phase 2: Data Models | 2 | 2 hours |
| Phase 3: Business Logic | 3 | 4 hours |
| Phase 4: API Layer | 1 | 1.5 hours |
| Phase 5: Error Handling | 2 | 2 hours |
| Phase 6: Configuration | 1 | 1 hour |
| Phase 7: Testing | 3 | 3 hours |
| Phase 8: Deployment | 2 | 2 hours |
| **TOTAL** | **16** | **17 hours** |

**Assumptions**:
- Developer familiar with Python and FastAPI
- PostgreSQL database already provisioned
- OAuth service already available
```

### 8. Implementation Contracts (MANDATORY)

**Section 8 is required for ALL TASKS files**. Implementation Contracts enable parallel development of dependent TASKS files.

**Structure**:

```markdown
## 8. Implementation Contracts

### 8.1 Contracts Provided by This TASKS
@icon: TASKS-XXX:ContractName
@icon-role: provider

- **Contract Name**: [Interface name]
- **Type**: Protocol Interface | Exception Hierarchy | State Machine | Data Model | DI Interface
- **Consumers**: List of TASKS IDs that depend on this contract
- **Purpose**: Brief description

### 8.2 Contracts Consumed by This TASKS
@icon: TASKS-YYY:OtherContract
@icon-role: consumer

- **Provider**: TASKS-YYY
- **Contract Name**: [Interface name]
- **Purpose**: Why this TASKS needs this contract

### 8.3 No Contracts
If this TASKS provides no contracts and consumes no contracts, state explicitly:
"This TASKS document neither provides nor consumes implementation contracts."
```

**When to Create Contracts**:
- TASKS has 3+ downstream dependencies
- Shared interfaces across multiple implementation sessions
- Complex state machines or exception hierarchies
- Parallel development required

**Contract Types**:
1. **Protocol Interfaces**: `typing.Protocol` with method signatures
2. **Exception Hierarchies**: Typed exceptions with error codes
3. **State Machine Contracts**: `Enum` states with valid transitions
4. **Data Models**: Pydantic/TypedDict schemas
5. **DI Interfaces**: ABC classes for dependency injection

**Reference**: See `ai_dev_flow/TASKS/IMPLEMENTATION_CONTRACTS_GUIDE.md` for detailed guidance.

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

**For hierarchical requirements (BRD, PRD, EARS, BDD, SYS, REQ)**:
- **Always use**: `TYPE.NN.TT.SS` (dot separator, 4-segment unified format)
- **Never use**: `TYPE-NN:NNN` (colon separator - DEPRECATED)
- **Never use**: `TYPE.NN.TT` (3-segment format - DEPRECATED)

Examples:
- `@brd: BRD.17.01.01` ✅
- `@brd: BRD.017.001` ❌ (old 3-segment format)


## Cumulative Tagging Requirements

**Layer 11 (TASKS)**: Must include tags from Layers 1-10

**Tag Count**: 8-10 tags (minimum 8, maximum 10)

### Element Type Codes for Cumulative Tags

| Artifact | Element Type | Code | Example |
|----------|--------------|------|---------|
| BRD | Business Requirement | 01 | BRD.01.01.03 |
| PRD | Product Feature | 07 | PRD.01.07.02 |
| EARS | Statement | 25 | EARS.01.25.01 |
| BDD | Scenario | 14 | BDD.01.14.01 |
| SYS | System Requirement | 26 | SYS.01.26.01 |
| REQ | Atomic Requirement | 27 | REQ.01.27.01 |
| IMPL | Implementation Phase | 29 | IMPL.01.29.01 |

**Minimum (IMPL and CTR skipped)**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 11):
```markdown
@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.26.01
@req: REQ.01.27.01
@spec: SPEC-01
```

**Maximum (IMPL, CTR, and ICON included)**:
```markdown
@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.26.01
@req: REQ.01.27.01
@impl: IMPL.01.29.01
@ctr: CTR-01
@spec: SPEC-01
@icon: TASKS-01:DataValidator  # if providing or consuming implementation contracts
@icon-role: provider  # or consumer
```

## Upstream/Downstream Artifacts

**Upstream Sources**:
- **BRD** (Layer 1) - Business requirements
- **PRD** (Layer 2) - Product features
- **EARS** (Layer 3) - Formal requirements
- **BDD** (Layer 4) - Test scenarios
- **ADR** (Layer 5) - Architecture decisions
- **SYS** (Layer 6) - System requirements
- **REQ** (Layer 7) - Atomic requirements
- **IMPL** (Layer 8) - Implementation approach (optional)
- **CTR** (Layer 9) - Data contracts (optional)
- **SPEC** (Layer 10) - Technical specifications (PRIMARY SOURCE)

**Downstream Artifacts**:
- **IPLAN** (Layer 12) - Implementation plans (created in `docs/IPLAN/`)
- **Code** (Layer 13) - Implementation

**Same-Type Document Relationships** (conditional):
- `@related-tasks: TASKS-NN` - TASKS sharing implementation context
- `@depends-tasks: TASKS-NN` - TASKS that must be completed first

## Validation Checks

### Tier 1: Errors (Blocking)

| Check | Description |
|-------|-------------|
| CHECK 1 | Filename format valid (TASKS-NN_slug_tasks.md) |
| CHECK 2 | YAML frontmatter present with required fields |
| CHECK 3 | Document Control table complete (8 fields) |
| CHECK 4 | All 8 required sections present |
| CHECK 5 | Section 8 (Implementation Contracts) exists with 8.1/8.2/8.3 subsection |
| CHECK 6 | All 8 required traceability tags present |
| CHECK 7 | Parent SPEC reference valid and file exists |
| CHECK 8 | Element ID format compliance (TASKS.NN.TT.SS) |

### Tier 2: Warnings

| Check | Description |
|-------|-------------|
| CHECK W1 | Scope section has exclusions documented |
| CHECK W2 | Plan has at least 3 numbered steps |
| CHECK W3 | SPEC line references present |
| CHECK W4 | At least 3 acceptance criteria checkboxes |
| CHECK W5 | BDD scenario reference in acceptance criteria |
| CHECK W6 | @icon-role tag present if @icon tag used |

### Tier 3: Info

| Check | Description |
|-------|-------------|
| CHECK I1 | Time estimates present in plan |
| CHECK I2 | Optional @impl and @ctr tags present |
| CHECK I3 | ICON references valid and files exist |

## Creation Process

### Step 1: Read Upstream SPEC

Read SPEC (Layer 10) - technical specifications to decompose.

### Step 2: Reserve ID Number

Check `ai_dev_flow/TASKS/` for next available ID number.

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: TASKS-01, TASKS-99, TASKS-102
- ❌ Incorrect: TASKS-001, TASKS-009 (extra leading zero not required)

**ID Matching**: TASKS ID typically matches SPEC ID (TASKS-01 from SPEC-01).

### Step 3: Create TASKS File

**File naming**: `ai_dev_flow/TASKS/TASKS-NN_{slug}_tasks.md`

**Example**: `ai_dev_flow/TASKS/TASKS-01_data_validation_tasks.md`

### Step 4: Fill Document Control Section

Complete metadata and Document Revision History table.

### Step 5: Write Overview

Summarize task breakdown approach.

### Step 6: Define Phases

Organize tasks into logical phases (8 typical phases).

### Step 7: Create Detailed Tasks

For each task in SPEC:
- Assign TASK ID (TASKS.{SPEC-ID}.18.{SEQ})
- Write clear Action (imperative)
- List Files to Create/Modify
- Identify Dependencies
- Estimate Effort
- Reference SPEC section
- Define Success Criteria

### Step 8: Create Dependencies Graph

Use Mermaid diagram to visualize task dependencies.

### Step 9: Calculate Effort Summary

Summarize total effort by phase.

### Step 10: Add Cumulative Tags

Include all 8-10 upstream tags (@brd through @spec).

### Step 11: Create/Update Traceability Matrix

**MANDATORY**: Update `ai_dev_flow/TASKS/TASKS-00_TRACEABILITY_MATRIX-TEMPLATE.md`

### Step 12: Validate TASKS

```bash
./ai_dev_flow/scripts/validate_tasks.sh ai_dev_flow/TASKS/TASKS-01_*.md

python ai_dev_flow/scripts/validate_tags_against_docs.py --artifact TASKS-01 --expected-layers brd,prd,ears,bdd,adr,sys,req,impl,contracts,spec --strict
```

### Step 13: Commit Changes

Commit TASKS file and traceability matrix.

## Validation

### Automated Validation

```bash
# Quality gates
./scripts/validate_quality_gates.sh ai_dev_flow/TASKS/TASKS-01_*.md

# Task format validation
./ai_dev_flow/scripts/validate_tasks.sh ai_dev_flow/TASKS/TASKS-01_*.md

# Cumulative tagging
python ai_dev_flow/scripts/validate_tags_against_docs.py \
  --artifact TASKS-01 \
  --expected-layers brd,prd,ears,bdd,adr,sys,req,impl,contracts,spec \
  --strict
```

### Manual Checklist

- [ ] Document Control section at top
- [ ] Overview explains breakdown approach
- [ ] Tasks organized into phases (8 typical phases)
- [ ] Each task has TASKS.{SPEC-ID}.18.{SEQ} ID
- [ ] Each task has all required fields
- [ ] Dependencies identified (or "None")
- [ ] Effort estimates provided
- [ ] SPEC references included
- [ ] Success Criteria clear and testable
- [ ] Dependencies Graph (Mermaid diagram) created
- [ ] Effort Summary calculated
- [ ] **Section 8 Implementation Contracts** completed (provider/consumer/none)
- [ ] Cumulative tags: @brd through @spec (8-10 tags) included
- [ ] `@icon` tags added if providing/consuming contracts
- [ ] Traceability matrix updated

### Diagram Standards
All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Common Pitfalls

1. **Vague tasks**: Tasks must be specific and actionable
2. **Missing dependencies**: Must identify task dependencies
3. **No effort estimates**: Effort required for planning
4. **Missing SPEC references**: Each task must link to SPEC section
5. **No success criteria**: Must define how to verify completion
6. **Missing cumulative tags**: Layer 11 must include all 8-10 upstream tags
7. **Missing Section 8**: Implementation Contracts section is MANDATORY
8. **Text-based diagrams**: Use Mermaid ONLY for Dependencies Graph
9. **Legacy task IDs**: Use TASKS.NN.18.SS, NOT TASK-XXX or T-XXX

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
python ai_dev_flow/scripts/validate_cross_document.py --document docs/TASKS/TASKS-NN_slug.md --auto-fix

# Layer validation (Phase 2) - run when all TASKS documents complete
python ai_dev_flow/scripts/validate_cross_document.py --layer TASKS --auto-fix
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| TASKS (Layer 11) | @brd, @prd, @ears, @bdd, @adr, @sys, @req, @spec (+ @impl, @ctr if created) | 8-10 tags |

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

After creating TASKS, use:

**`doc-iplan`** - Create Implementation Plans (Layer 12)

The IPLAN will:
- Reference TASKS as upstream source
- Include all 9-11 upstream tags
- Convert tasks to bash command sequences
- Provide session-based execution plan

## Reference Documents

TASKS artifacts do not support REF documents. Reference documents are limited to **BRD and ADR types only** per the SDD framework.

For supplementary documentation needs, create:
- **BRD-REF**: Business context documentation
- **ADR-REF**: Task estimation guides, dependency analysis reports

## Related Resources

- **Template**: `ai_dev_flow/TASKS/TASKS-TEMPLATE.md` (primary authority)
- **TASKS Creation Rules**: `ai_dev_flow/TASKS/TASKS_CREATION_RULES.md`
- **TASKS Validation Rules**: `ai_dev_flow/TASKS/TASKS_VALIDATION_RULES.md`
- **TASKS README**: `ai_dev_flow/TASKS/README.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`

**Section Templates** (for documents >25K tokens):
- Index template: `ai_dev_flow/TASKS/TASKS-SECTION-0-TEMPLATE.md`
- Content template: `ai_dev_flow/TASKS/TASKS-SECTION-TEMPLATE.md`
- Reference: `ai_dev_flow/ID_NAMING_STANDARDS.md` (Section-Based File Splitting)

## Quick Reference

**TASKS Purpose**: Decompose SPEC into actionable AI-structured TODO tasks

**Layer**: 11

**Element ID Format**: `TASKS.NN.18.SS`
- Task = 18
- Task Item = 30

**Removed Patterns**: TASK-XXX, T-XXX

**Tags Required**: @brd through @spec (8-10 tags)

**Format**: AI-structured TODO with phases

**Task ID Format**: TASKS.{SPEC-ID}.18.{SEQ}

**Required Task Fields**:
- Task ID, Title, Action
- Files to Create/Modify
- Dependencies
- Estimated Effort
- SPEC Reference
- Success Criteria

**Key Sections**:
- Task Hierarchy (phases)
- Detailed Tasks (primary content)
- Dependencies Graph (Mermaid)
- Effort Summary
- Implementation Contracts (Section 8 - MANDATORY)

**Next**: doc-iplan
