---
name: plan-analysis
description: Use when the user provides an implementation plan file and asks to analyze it, assess impact, update specifications, or verify planned changes. Triggers on keywords like "analyze plan", "implementation plan", "assess impact", "update spec from plan", "verify plan".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Implementation Plan Analysis & Specification Update

Expert full-stack analyst for implementation plan analysis, impact assessment, and specification updates.

**IMPORTANT**: Think hard, plan step-by-step todo list first. Preserve todo list through all operations.

**⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` before starting analysis — validation checkpoints, evidence chains, confidence levels.

---

## Phase 1: Plan Analysis (External Memory)

Build knowledge model in `.ai/workspace/analysis/[plan-name].md`.

### 1A: Initialization & Discovery

- Read and parse implementation plan completely
- Extract features, requirements, phases, dependencies
- Catalog all planned code changes (new files, modifications, deletions)
- Identify affected components, services, layers, integration points

### 1B: Knowledge Graph Construction

For each file, document:
- `currentContent`, `plannedChanges`, `changeImpactAnalysis`
- `testingRequirements`, `specificationMapping`, `testCaseImpact`

### 1C: Specification Mapping

- Test case mapping (existing tests affected)
- Business requirement mapping (new vs existing)
- Entity relationship impact, workflow integration
- Coverage gap analysis

### 1D: Overall Analysis

Write summary: end-to-end workflows, architecture patterns, business logic changes, integration points, test coverage.

---

## Phase 2: Detailed Analysis

1. **Implementation Impact**: Component impact, integration points, data flow, platform compliance
2. **Business Logic**: New rules, modified workflows, validation requirements
3. **Testing Strategy**: Coverage requirements, new scenarios, regression needs
4. **Specification Update Strategy**: Integration, traceability, existing coverage preservation
5. **Rollback & Safety**: Backup procedures, rollback plan, validation checkpoints

---

## Phase 3: Approval Gate

**CRITICAL**: Present comprehensive analysis for explicit approval. **DO NOT** proceed without it.

---

## Phase 4: Specification Update Execution

Once approved:
1. Backup original specification
2. Read and parse existing specification
3. Execute updates: requirements, entity relationships, test cases, traceability matrix
4. Quality assurance validation

---

## Success Validation

- **Requirements Traceability**: All plan requirements mapped
- **Test Coverage**: All changes covered by tests
- **Workflow Validation**: End-to-end workflows documented
- **Regression Prevention**: Existing functionality protected


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
