---
name: doc-flow
description: AI-Driven Specification-Driven Development (SDD) workflow orchestrator - guides skill selection and general SDD methodology
tags:
  - sdd-workflow
  - layer-0-artifact
  - shared-architecture
  - required-both-approaches
  - ai-assistant
custom_fields:
  layer: 0
  artifact_type: META
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: []
  downstream_artifacts: [BRD, PRD, EARS, BDD, ADR, SYS, REQ, IMPL, CTR, SPEC, TASKS, IPLAN, ICON, REF]
---

# doc-flow (Orchestrator)

## Purpose

This skill serves as the **orchestrator** for the AI-Driven Specification-Driven Development (SDD) workflow. It provides:

1. **Skill Selection Guidance**: Helps determine which artifact-specific skill to use
2. **Workflow Overview**: Complete 16-layer SDD architecture
3. **General SDD Principles**: Specification-driven methodology fundamentals
4. **Integration Guidance**: How skills work together

**For Artifact Creation**: Use the specific artifact skill (doc-brd, doc-prd, doc-ears, doc-bdd, doc-adr, doc-sys, doc-req, doc-impl, doc-ctr, doc-spec, doc-tasks, doc-iplan, doc-ref, doc-naming).

**Authoritative Reference**: [ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md]({project_root}/ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md)

---

## Prerequisites

**⚠️ For New Projects (Greenfield)**: If starting a brand new project with no existing folder structure, use the **`project-init`** skill FIRST to initialize project structure, select domain, create folders, and configure setup. Then return here to begin workflow execution.

**For Existing Projects**: If project is already initialized (docs/ folders exist, domain configured), proceed directly with this skill.

---

## Skill Selection Decision Tree

### "Which Skill Do I Need?"

Answer these questions to find the right skill:

**Q1: What stage are you at in the workflow?**

- **Starting new project with business requirements** → Use `doc-brd` skill
- **Have BRD, need product requirements** → Use `doc-prd` skill
- **Have PRD, need formal requirements** → Use `doc-ears` skill
- **Have EARS, need test scenarios** → Use `doc-bdd` skill
- **Have BDD, need architecture decisions** → Use `doc-adr` skill
- **Have ADR, need system requirements** → Use `doc-sys` skill
- **Have SYS, need atomic requirements** → Use `doc-req` skill
- **Have REQ, need implementation planning** → Use `doc-impl` skill (if complex) or skip to `doc-spec`
- **Have REQ/IMPL, need API contracts** → Use `doc-ctr` skill (if interface requirement)
- **Have REQ/CTR, need technical specifications** → Use `doc-spec` skill
- **Have SPEC, need task breakdown** → Use `doc-tasks` skill
- **Have TASKS, need implementation contracts** → Add Section 8 to TASKS (see `doc-tasks` skill)
- **Have TASKS, need execution plan** → Use `doc-iplan` skill
- **Have IPLAN, ready to code** → Implement code per IPLAN
- **Need supplementary documentation (overview, glossary, guides)** → Use `doc-ref` skill

**Q2: What are you trying to do?**

- **Define business needs and objectives** → `doc-brd`
- **Define product features and KPIs** → `doc-prd`
- **Write formal WHEN-THE-SHALL-WITHIN requirements** → `doc-ears`
- **Create Gherkin test scenarios** → `doc-bdd`
- **Document architecture decisions** → `doc-adr`
- **Define system requirements** → `doc-sys`
- **Define atomic requirements** → `doc-req`
- **Plan project implementation (WHO/WHEN/WHAT)** → `doc-impl`
- **Define API contracts** → `doc-ctr`
- **Write technical specifications** → `doc-spec`
- **Break down into AI tasks** → `doc-tasks`
- **Define implementation contracts for parallel dev** → Add Section 8 to TASKS (see `doc-tasks` skill)
- **Create session execution plan** → `doc-iplan`
- **Create supplementary documentation (project overview, glossary, guides)** → `doc-ref`
- **General guidance or unsure** → Stay with `doc-flow` (this skill)

---

## Complete SDD Workflow (16 Layers)

**Authoritative Reference**: [ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md]({project_root}/ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md)

### Workflow Sequence

```
Strategy (Layer 0)
  ↓
BRD (Layer 1) → doc-brd skill
  ↓
PRD (Layer 2) → doc-prd skill
  ↓
EARS (Layer 3) → doc-ears skill
  ↓
BDD (Layer 4) → doc-bdd skill
  ↓
ADR (Layer 5) → doc-adr skill
  ↓
SYS (Layer 6) → doc-sys skill
  ↓
REQ (Layer 7) → doc-req skill
  ↓
IMPL (Layer 8) [OPTIONAL] → doc-impl skill
  ↓
CTR (Layer 9) [OPTIONAL - IF INTERFACE] → doc-ctr skill
  ↓
SPEC (Layer 10) → doc-spec skill
  ↓
TASKS (Layer 11) → doc-tasks skill
  ↓
IPLAN (Layer 12) → doc-iplan skill
  ↓
Code (Layer 13)
  ↓
Tests (Layer 14)
  ↓
Validation (Layer 15)
```

### Layer Descriptions

| Layer | Artifact | Purpose | Skill |
|-------|----------|---------|-------|
| 0 | **Strategy** | Business owner documents | External (strategy/) |
| 1 | **BRD** | Business requirements | `doc-brd` |
| 2 | **PRD** | Product requirements | `doc-prd` |
| 3 | **EARS** | Formal requirements (WHEN-THE-SHALL) | `doc-ears` |
| 4 | **BDD** | Gherkin test scenarios | `doc-bdd` |
| 5 | **ADR** | Architecture decisions | `doc-adr` |
| 6 | **SYS** | System requirements | `doc-sys` |
| 7 | **REQ** | Atomic requirements | `doc-req` |
| 8 | **IMPL** | Implementation plans (WHO/WHEN) [OPTIONAL] | `doc-impl` |
| 9 | **CTR** | API contracts [OPTIONAL - IF INTERFACE] | `doc-ctr` |
| 10 | **SPEC** | Technical specifications (HOW) | `doc-spec` |
| 11 | **TASKS** | Task breakdown for implementation | `doc-tasks` |
| 11+ | **ICON** | Implementation Contracts (Section 8 of TASKS) | `doc-tasks` |
| 12 | **IPLAN** | Session execution plans | `doc-iplan` |
| 13 | **Code** | Python implementation | Implementation |
| 14 | **Tests** | Test suites | Implementation |
| 15 | **Validation** | BDD + contract + traceability | Validation |

### Optional Layers Decision Logic

**When to Create IMPL (Layer 8)**:
- **Create IMPL When**: Duration ≥2 weeks, teams ≥3, components ≥5, critical budget/timeline, external dependencies
- **Skip IMPL When**: Single component, duration <2 weeks, single developer, low risk
- **Reference**: [ai_dev_flow/WHEN_TO_CREATE_IMPL.md]({project_root}/ai_dev_flow/WHEN_TO_CREATE_IMPL.md)

**When to Create CTR (Layer 9)**:
- **Create CTR When**: Public APIs, event schemas, data models, version compatibility requirements, interface between components
- **Skip CTR When**: Internal logic only, no external interface, no serialization
- **Reference**: [ai_dev_flow/WHEN_TO_CREATE_IMPL.md#when-to-create-ctr-after-impl]({project_root}/ai_dev_flow/WHEN_TO_CREATE_IMPL.md#when-to-create-ctr-after-impl)

---

## General SDD Principles

### 1. Specification-Driven Development Philosophy

**Core Principle**: Formalize before implementing

- **Traditional Approach**: Code first, document later (or never)
- **SDD Approach**: Document first, generate code from specifications

**Why SDD Works**:
- **Clarity**: Requirements are explicit before coding begins
- **Traceability**: Every line of code traces to business requirements
- **Validation**: Tests defined before implementation
- **Consistency**: Templates ensure uniform structure
- **Speed**: Code generation from YAML specifications (48x faster)

### 2. Information Flow Hierarchy

**Changes flow DOWN (never UP)**:

```
strategy/ (WHAT - Product Owner Voice)
    ├── Strategy business logic
    └── Performance targets
              ↓
              ↓ Referenced by
              ↓
📚 docs/ (WHY + HOW - Project Documentation)
    ├── Requirements (WHY)
    ├── Architecture (HOW)
    └── Specifications (IMPLEMENTATION)
              ↓
              ↓ Generates
              ↓
💻 Source Code (Python/Infrastructure)

📝 ai_dev_flow/ feeds into 📚 docs/ for consistency
```

**Golden Rules**:
- Strategy → Documentation → Code (one-way flow)
- Code cannot change strategy
- Always use templates from `ai_dev_flow/` when creating docs in `docs/`
- All business logic must reference `strategy/` sections

### 3. Directory Structure and Roles

**Critical Context**: This project has three key directories with distinct roles:

#### `strategy/` - WHAT (Product Owner Voice)
**Primary Authority**: Authoritative business strategy and domain logic

- `core_algorithm.md` - Primary algorithm specifications
- `strategy_overview.md` - Strategic framework and operating modes
- `risk_management.md` - Risk management policies
- `business_rules.md` - Domain-specific business rules
- `selection_criteria/` - Entry criteria and scoring algorithms
- Performance targets, state machines, resource budgets

**Golden Rule**: All business logic must trace back to these strategy documents.

#### 📚 `docs/` - PROJECT DOCUMENTATION
**Implementation Documentation**: Requirements, architecture, specifications

- `docs/BRD/` - Business Requirements Documents
  - **Nested folder structure**: `docs/BRD/BRD-NN/BRD-NN.S_slug.md`
- `docs/PRD/` - Product Requirements Documents
  - **Nested folder structure**: `docs/PRD/PRD-NN/PRD-NN.S_slug.md`
- `docs/ADR/` - Architecture Decision Records (HOW)
  - **Nested folder structure**: `docs/ADR/ADR-NN/ADR-NN.S_slug.md`
- `docs/BDD/` - BDD acceptance tests (Behavior-Driven Development)
- `docs/CTR/` - API Contracts (dual-file format: .md + .yaml)
- `docs/IMPL/` - Implementation Plans (Project Management: WHO/WHEN)
- `docs/SPEC/` - YAML technical specifications
- `docs/TASKS/` - Code Generation Plans (AI-structured implementation tasks)
- `docs/IPLAN/` - Implementation Plans (session-based execution with bash commands)

**Note**: BRD, PRD, ADR use section-based nested folders by default. Other types use flat structure.

**Purpose**: Document how strategy is implemented through architecture and code.

#### 📝 `ai_dev_flow/` - AUTHORITATIVE DEVELOPMENT STANDARD
**Development Standard and Templates**: The single source of truth for SDD workflow

- **Status**: Authoritative development standard for this project
- **Contents**: Complete SDD workflow (BRD → PRD → EARS → BDD → ADR → SYS → REQ → IMPL → CTR → SPEC → TASKS → IPLAN → Code)
- **Templates**: `{TYPE}-TEMPLATE.{ext}` for each artifact type (BRD, PRD, EARS, BDD, ADR, SYS, REQ, IMPL, CTR, SPEC, TASKS, IPLAN, REF)
- **Indices**: `{TYPE}-00_index.{ext}` listing all documents of each type
- **READMEs**: Detailed usage guides and best practices for each artifact type
- **Standards**: ID naming, traceability format, cross-referencing rules
- **Examples**: Reference implementations with full traceability chains

**Purpose**: Define the complete development methodology with templates, standards, and examples for creating all artifacts.

#### ⚠️ CRITICAL: Archived Documents Restriction

**STRICTLY PROHIBITED: DO NOT access, reference, link to, or use ANY files or directories containing the word "archived" in their path.**

**Automatic Filtering Rules:**
- ❌ Skip any path containing `archived`, `Archived`, `ARCHIVED`, or `archive`
- ❌ Ignore files in directories with "archived" in the name
- ❌ Do not read, suggest, or reference archived content
- ❌ Do not use archived documents even if they appear in search results

**Active Documentation Only:**
- `strategy/` (current strategy - excludes archived subdirs)
- `docs/` (active project documentation)
- `ai_dev_flow/` (authoritative templates and standards)

**If archived content is needed:**
- Stop immediately
- Inform user that content is in archived location
- Request explicit permission before proceeding

### 4. Traceability Importance

**Complete Audit Trail**: Every artifact must trace back to original business requirements

**Benefits**:
- **Impact Analysis**: Know what breaks when requirements change
- **Regulatory Compliance**: Industry-specific audit requirements (ISO, SOC2, etc.)
- **Change Management**: Track all changes through artifact chain
- **Coverage Metrics**: Measure implementation completeness
- **Quality Assurance**: Automated validation prevents gaps

**Implementation**:
- Cumulative tagging hierarchy (see SHARED_CONTENT.md)
- Traceability section in every document
- Bidirectional traceability matrices
- Automated validation scripts

### 5. Upstream Artifact Policy (CRITICAL)

**⚠️ MANDATORY RULE**: Do NOT create missing upstream artifacts. Skip functionality instead.

**Policy Statement**:
If a required upstream artifact is missing, the downstream functionality **MUST NOT be implemented**. This enforces the SDD document hierarchy where every implementation must have proper business/product justification through the complete artifact chain.

**Decision Rules**:

| Situation | Action |
|-----------|--------|
| Upstream exists | Reference with exact document ID |
| Upstream required but missing | **Skip that functionality** - do NOT implement |
| Upstream optional and missing | Use `null` in traceability tag |
| Upstream not applicable | Omit tag entirely |

**Rationale**:
- **Prevents orphaned code**: No implementation without business justification
- **Enforces governance**: Changes must flow through proper channels
- **Maintains audit trail**: Every feature traces to business need
- **Reduces technical debt**: No undocumented "nice-to-have" features

**When Upstream is Missing**:
1. **Stop** - Do not proceed with implementation
2. **Report** - Inform user which upstream artifact is missing
3. **Advise** - Recommend creating upstream artifacts first through proper channels
4. **Skip** - Move on to functionality that has complete upstream chain

**Reference**: [ai_dev_flow/TRACEABILITY.md]({project_root}/ai_dev_flow/TRACEABILITY.md) - Section "Step 3: Decision Rules"

---

## Integration with Other Skills

### Core Workflow Skills

**`project-init`** - Initialize new project structure
- Use BEFORE doc-flow for greenfield projects
- Creates folder structure, domain setup, baseline files
- Reference: `.claude/skills/project-init/SKILL.md`

**`trace-check`** - Validate traceability after artifact creation
- Use AFTER doc-flow to verify bidirectional links
- Validates cumulative tagging, ID formats, link resolution
- Detects orphaned artifacts and traceability gaps
- Reference: `.claude/skills/trace-check/SKILL.md`

**`doc-naming`** - Unified ID naming standards enforcement
- Use for ID format validation across all artifact types
- Validates 4-segment element IDs (TYPE.NN.TT.SS)
- Enforces variable-length DOC_NUM (2+ digits)
- Reference: `.claude/skills/doc-naming/SKILL.md`

**`doc-validator`** - Cross-document validation orchestrator
- Validates traceability across all layers
- Detects gaps, broken links, and format violations
- Runs auto-fix actions for common issues
- Reference: `.claude/skills/doc-validator/SKILL.md`

### Planning & Architecture

**`adr-roadmap`** - Generate implementation roadmaps from ADRs
- Use AFTER creating ADR artifacts
- Creates timeline, risk assessment, dependency mapping
- Reference: `.claude/skills/adr-roadmap/SKILL.md`

**`project-mngt`** - MVP/MMP/MMR planning
- Use for strategic release planning
- Integrates with IMPL artifacts
- Reference: `.claude/skills/project-mngt/SKILL.md`

### Typical Workflow Integration

```text
1. project-init    → Initialize project (greenfield only)
2. doc-brd         → Create BRD
3. doc-prd         → Create PRD
4. doc-ears        → Create EARS
5. doc-bdd         → Create BDD
6. doc-adr         → Create ADR
7. doc-sys         → Create SYS
8. doc-req         → Create REQ
9. doc-impl        → Create IMPL (if complex)
10. doc-ctr        → Create CTR (if interface)
11. doc-spec       → Create SPEC
12. doc-tasks      → Create TASKS
13. doc-iplan      → Create IPLAN
14. Implementation → Execute based on IPLAN
15. trace-check    → Validate traceability
```

---

## Shared Standards

**CRITICAL**: All artifact-specific skills share common standards defined in:

**`.claude/skills/doc-flow/SHARED_CONTENT.md`**

This document contains:
1. Document ID Naming Standards
2. Traceability Section Format
3. Cumulative Tagging Hierarchy
4. Quality Gates & Validation
5. Traceability Matrix Enforcement
6. Documentation Standards
7. Document Control Section Requirements

**All artifact skills (doc-brd through doc-iplan, plus doc-ref, doc-naming) import these shared standards.**

### Diagram Standards (Global Requirement)

**All diagrams MUST use Mermaid syntax.** Text-based diagrams (ASCII art, box drawings) are prohibited.

- **Authority Document**: `ai_dev_flow/DIAGRAM_STANDARDS.md`
- **Syntax Generation**: `mermaid-gen` skill
- **File Management**: `charts-flow` skill (SVG conversion, embedding)

**Allowed Exception**: Directory tree structures (using `├── └── │`) are permitted as they represent file structure, not diagrams.

---

## Validation Overview

### Automated Validation Tools

**Quality Gates Validation:**
```bash
# Validate artifact meets layer transition requirements (≥90%)
./scripts/validate_quality_gates.sh docs/REQ/risk/lim/REQ-03.md

# Artifact-specific validation
./ai_dev_flow/scripts/validate_brd_template.sh docs/BRD/BRD-01.md
./ai_dev_flow/scripts/validate_req_template.sh docs/REQ/api/ib/REQ-02.md

# Link integrity validation
./ai_dev_flow/scripts/validate_links.py --path docs/ --check-anchors
```

**Tag-Based Traceability Validation:**
```bash
# Complete workflow (extract → validate → generate)
python ai_dev_flow/scripts/generate_traceability_matrices.py --auto

# Individual steps
python ai_dev_flow/scripts/extract_tags.py --source src/ docs/ tests/
python ai_dev_flow/scripts/validate_tags_against_docs.py --strict
python ai_dev_flow/scripts/generate_traceability_matrices.py --output docs/generated/matrices/
```

---

## Cross-Document Validation (MANDATORY)

**CRITICAL**: After creating each artifact, execute cross-document validation before proceeding to the next layer.

### Validation Phases

| Phase | Trigger | Command |
|-------|---------|---------|
| Phase 1 | Per-document | `python scripts/validate_cross_document.py --document {doc_path} --auto-fix` |
| Phase 2 | Per-layer complete | `python scripts/validate_cross_document.py --layer {LAYER} --auto-fix` |
| Phase 3 | Final (all layers) | `python scripts/validate_cross_document.py --full --auto-fix` |

### Automatic Validation Loop

```
LOOP:
  1. Run: python scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed to next layer
```

### Layer-Specific Upstream Requirements

| Layer | Artifact | Required Upstream Tags | Tag Count |
|-------|----------|------------------------|-----------|
| 1 | BRD | (none - root) | 0 |
| 2 | PRD | @brd | 1 |
| 3 | EARS | @brd, @prd | 2 |
| 4 | BDD | @brd, @prd, @ears | 3 |
| 5 | ADR | @brd, @prd, @ears, @bdd | 4 |
| 6 | SYS | @brd, @prd, @ears, @bdd, @adr | 5 |
| 7 | REQ | @brd, @prd, @ears, @bdd, @adr, @sys | 6 |
| 8 | IMPL | @brd, @prd, @ears, @bdd, @adr, @sys, @req | 7 |
| 9 | CTR | @brd through @req (+ optional @impl) | 7-8 |
| 10 | SPEC | @brd through @req (+ optional @impl, @ctr) | 7-9 |
| 11 | TASKS | @brd through @spec (+ optional @impl, @ctr) | 8-10 |
| 12 | IPLAN | @brd through @tasks (+ optional @impl, @ctr) | 9-11 |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing cumulative tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
| Broken link | Recalculate path from current location |
| Missing traceability section | Insert from template |

### Validation Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| XDOC-001 | Referenced requirement ID not found | ERROR |
| XDOC-002 | Missing cumulative tag | ERROR |
| XDOC-003 | Upstream document not found | ERROR |
| XDOC-004 | Link target file missing | WARNING |
| XDOC-005 | Anchor in link not found | WARNING |
| XDOC-006 | Tag format invalid | ERROR |
| XDOC-007 | Gap in cumulative tag chain | ERROR |
| XDOC-008 | Circular reference detected | ERROR |
| XDOC-009 | Missing traceability section | ERROR |
| XDOC-010 | Orphaned document (no upstream refs) | WARNING |

### Quality Gate

**Blocking**: YES - Cannot proceed to next layer until Phase 1 validation passes with 0 errors for the current artifact.

---

## Related Resources

### Core Standards (ai_dev_flow/)

**Primary References - Authoritative Development Standard:**

- **Main Guide**: [SPEC_DRIVEN_DEVELOPMENT_GUIDE.md]({project_root}/ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md) - Complete 16-layer workflow
- **Workflow Diagram**: [index.md]({project_root}/ai_dev_flow/index.md#traceability-flow) - Complete Mermaid diagram
- **ID Standards**: [ID_NAMING_STANDARDS.md]({project_root}/ai_dev_flow/ID_NAMING_STANDARDS.md) - File naming, ID format rules
- **Traceability**: [TRACEABILITY.md]({project_root}/ai_dev_flow/TRACEABILITY.md) - Cross-reference format, link standards
- **Quality Gates**: [TRACEABILITY_VALIDATION.md]({project_root}/ai_dev_flow/TRACEABILITY_VALIDATION.md) - Automated quality gates system
- **Platform BRD Guide**: [PLATFORM_VS_FEATURE_BRD.md]({project_root}/ai_dev_flow/PLATFORM_VS_FEATURE_BRD.md) - Platform vs Feature BRD decision guide
- **When to Create IMPL**: [WHEN_TO_CREATE_IMPL.md]({project_root}/ai_dev_flow/WHEN_TO_CREATE_IMPL.md) - IMPL vs direct REQ→SPEC decision guide
- **README**: [README.md]({project_root}/ai_dev_flow/README.md) - Getting started guide

### Templates Location

**All templates located in `ai_dev_flow/{artifact_type}/`:**

- **BRD** (`BRD/`): 3 templates available (comprehensive, simplified, domain-specific)
- **PRD** (`PRD/`): `PRD-TEMPLATE.md`
- **EARS** (`EARS/`): `EARS-TEMPLATE.md`
- **BDD** (`BDD/`): `BDD-TEMPLATE.feature`
- **ADR** (`ADR/`): `ADR-TEMPLATE.md`, Technology Stack reference (ADR-000)
- **SYS** (`SYS/`): `SYS-TEMPLATE.md`
- **REQ** (`REQ/`): `REQ-TEMPLATE.md` (v3.0 with 12 sections)
- **IMPL** (`IMPL/`): `IMPL-TEMPLATE.md`
- **CTR** (`CTR/`): `CTR-TEMPLATE.md` + `CTR-TEMPLATE.yaml` (dual-file)
- **SPEC** (`10_SPEC/`): `SPEC-TEMPLATE.yaml`
- **TASKS** (`TASKS/`): `TASKS-TEMPLATE.md` (includes Section 8 for ICON)
- **ICON** (`ICON/`): `ICON-TEMPLATE.md` (Implementation Contracts)
- **IPLAN** (`IPLAN/`): `IPLAN-TEMPLATE.md`
- **REF** (root): `REF-TEMPLATE.md` (Reference Documents)

**Each artifact type directory also contains:**
- Index file: `{TYPE}-00_index.{ext}`
- README.md: Usage guide and best practices
- Creation Rules: `{TYPE}_CREATION_RULES.md`
- Validation Rules: `{TYPE}_VALIDATION_RULES.md`

---

## Quick Reference Card

### Decision Matrix

| You Have | You Need | Use This Skill |
|----------|----------|----------------|
| Nothing | Business requirements | `doc-brd` |
| BRD | Product requirements | `doc-prd` |
| PRD | Formal requirements | `doc-ears` |
| EARS | Test scenarios | `doc-bdd` |
| BDD | Architecture decisions | `doc-adr` |
| ADR | System requirements | `doc-sys` |
| SYS | Atomic requirements | `doc-req` |
| REQ (complex) | Implementation plan | `doc-impl` |
| REQ (simple) | Technical specs | `doc-spec` |
| REQ/IMPL (interface) | API contracts | `doc-ctr` |
| REQ/CTR | Technical specs | `doc-spec` |
| SPEC | Task breakdown | `doc-tasks` |
| TASKS | Execution plan | `doc-iplan` |
| IPLAN | Code | Implement! |
| Any stage | Supplementary documentation | `doc-ref` |

### Development ROI

- Traditional: 70 hours/component
- SDD: 1.5 hours/component
- Speed increase: 48x faster
- Consistency: 100% (template-based)
- Traceability: Automatic, bidirectional

---

## Usage Example

**User**: "I need to implement position risk limit validation"

**Assistant**: "I'll guide you through the SDD workflow. Let me check what artifacts you have:

**Current Status Check**:
- Do you have a BRD documenting business requirements? [If no → **SKIP** this functionality]
- Do you have a PRD with product requirements? [If no → **SKIP** this functionality]
- Do you have EARS formal requirements? [If no → **SKIP** this functionality]
- Do you have BDD test scenarios? [If no → **SKIP** this functionality]
- Do you have ADR architecture decisions? [If no → **SKIP** this functionality]
- Do you have SYS system requirements? [If no → **SKIP** this functionality]
- Do you have REQ atomic requirements? [If no → **SKIP** this functionality]

**⚠️ CRITICAL: Upstream Artifact Policy**:
If ANY required upstream artifact is missing, **do NOT create it** and **do NOT implement the downstream functionality**. The SDD workflow enforces strict document hierarchy - functionality without proper business/product justification should not exist.

**Next Steps**:
Based on your current progress, I'll recommend the appropriate skill to use next. Each skill will guide you through creating that specific artifact type with proper templates, traceability, and validation."

---

**For detailed artifact creation guidance, use the specific artifact skill (doc-brd, doc-prd, doc-ears, doc-bdd, doc-adr, doc-sys, doc-req, doc-impl, doc-ctr, doc-spec, doc-tasks, doc-iplan, doc-ref, doc-naming).**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2025-12-29 | Fixed workflow sequence; Added doc-naming and doc-validator to Integration section; Updated layer count to 16 |
| 1.1 | 2025-11-30 | Added IPLAN layer, REF documents, ICON section |
| 1.0 | 2025-11-01 | Initial skill creation |
