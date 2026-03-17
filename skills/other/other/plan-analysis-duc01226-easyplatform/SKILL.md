---
name: plan-analysis
version: 1.0.1
description: "[Planning] Use when the user provides an implementation plan file and asks to analyze it, assess impact, update specifications, or verify planned changes. Triggers on keywords like "analyze plan", "implementation plan", "assess impact", "update spec from plan", "verify plan"."

allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Analyze an implementation plan, assess its impact on the codebase, and update specification documents accordingly.

**Workflow:**

1. **Discovery** — Parse plan, extract requirements, catalog planned changes
2. **Knowledge Graph** — Build detailed component-level impact map with test/spec mappings
3. **Analysis** — Assess architecture impact, business logic changes, testing strategy
4. **Approval Gate** — Present findings for explicit user approval before any spec updates
5. **Spec Update** — Execute approved changes to specification documents

**Key Rules:**

- Planning-only skill -- never implement code changes
- Always collaborate and get user approval before proceeding
- Maintain bidirectional traceability between plan and specification

# Implementation Plan Analysis & Specification Update

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan analysis, validate findings with user approval.
> **ASK** user to confirm the analysis before any next steps.

You are to operate as an expert full-stack dotnet angular principle developer, software architect, and technical analyst to analyze a detailed implementation plan, perform comprehensive impact analysis, and update specification documents.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` and `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN IMPLEMENTATION PLAN ANALYSIS

Build a structured knowledge model in `.ai/workspace/analysis/[plan-name].analysis.md`.

### PHASE 1A: INITIALIZATION AND DISCOVERY

1. **Initialize** the analysis file with standard headings

### IMPLEMENTATION PLAN COMPREHENSIVE ANALYSIS

**IMPLEMENTATION_PLAN_DEEP_ANALYSIS**: Thorough analysis of the implementation plan file:

1. **Plan Structure Analysis**:
    - Read and parse the implementation plan completely
    - Extract all planned features, requirements, and changes
    - Identify implementation phases and dependencies
    - Document under `## Implementation Plan Overview`

2. **Requirements Extraction**:
    - Parse Knowledge Graph from implementation plan
    - Extract new business requirements
    - Map functional and non-functional requirements
    - Identify changed business workflows
    - Document under `## Extracted Requirements`

3. **Planned Changes Analysis**:
    - Catalog all planned code changes (new files, modifications, deletions)
    - Identify affected components, services, and layers
    - Map file-level changes to business capabilities
    - Extract integration points
    - Document under `## Planned Changes Analysis`

4. **Architecture Impact Assessment**:
    - Analyze how changes affect overall system architecture
    - Identify CQRS pattern impacts (new Commands/Queries/Events)
    - Map domain entity changes and repository patterns
    - Document under `## Architecture Impact Assessment`

5. **Existing Specification Analysis**:
    - Read and analyze existing specification document structure
    - Identify current test cases, requirements, entity relationships
    - Map existing test coverage to planned changes
    - Document under `## Current Specification Analysis`

**AFFECTED_COMPONENTS_DISCOVERY**: For each planned change, discover:

- Direct Dependencies
- Indirect Dependencies
- Test Coverage Impact
- API Integration Impact
- Cross-Service Communication
- Database Schema Impact

Save to `## Comprehensive File List` with:

- `filePath`, `changeType`, `relationshipType`, `impactLevel`
- `serviceContext`, `planContext`, `specificationRelevance`

### PHASE 1B: KNOWLEDGE GRAPH CONSTRUCTION

**IMPORTANT: MUST DO WITH TODO LIST**

For each file, document in `## Knowledge Graph`:

- Standard fields plus plan-specific:
- `currentContent`: Existing functionality (if file exists)
- `plannedChanges`: Specific changes planned
- `changeImpactAnalysis`: How changes affect other components
- `testingRequirements`: New test cases needed
- `specificationMapping`: How component maps to spec sections
- `testCaseImpact`: Existing test cases needing modification

### PHASE 1C: SPECIFICATION MAPPING ANALYSIS

- **Test Case Mapping**: Which existing test cases are affected
- **Business Requirement Mapping**: How new requirements relate to existing
- **Entity Relationship Impact**: Changes to entity relationships
- **Workflow Integration**: How new workflows integrate with existing
- **Coverage Gap Analysis**: Areas where new test cases needed

### PHASE 1D: OVERALL ANALYSIS

Write comprehensive summary showing:

- Complete end-to-end workflows affected
- Architectural patterns impacted
- Business logic workflow changes
- Integration points affected
- Comprehensive test coverage requirements

---

## PHASE 2: COMPREHENSIVE ANALYSIS AND PLANNING

Generate detailed analysis under these headings:

1. **Implementation Impact Analysis**: Component impact, integration points, data flow changes, platform compliance

2. **Business Logic Analysis**: New business rules, modified workflows, validation requirements

3. **Testing Strategy Analysis**: Test coverage requirements, new test scenarios, regression testing needs

4. **Specification Update Strategy**: How to integrate new requirements, maintain traceability, preserve existing coverage

5. **Rollback and Safety Strategy**: Backup procedures, rollback plan, validation checkpoints

---

## PHASE 3: APPROVAL GATE

**CRITICAL**: Present comprehensive analysis for explicit approval. **DO NOT** proceed without it.

---

## PHASE 4: SPECIFICATION UPDATE EXECUTION

Once approved, execute with MANDATORY steps:

1. **Backup Original Specification**
2. **Read and Parse Existing Specification**
3. **Execute Planned Updates**:
    - New Requirements Integration
    - Entity Relationship Updates
    - Test Case Enhancement
    - Traceability Matrix Updates
    - Coverage Analysis Updates
4. **Maintain Specification Structure**
5. **Quality Assurance Validation**

---

## SUCCESS VALIDATION

Verify under `## Specification Validation`:

- **Requirements Traceability**: All plan requirements mapped
- **Test Coverage Validation**: All changes covered by tests
- **Business Workflow Validation**: End-to-end workflows documented
- **Integration Testing Coverage**: Cross-service impacts covered
- **Regression Prevention**: Existing functionality protected

---

## Plan Analysis Guidelines

- **Plan-Driven Analysis**: Base all analysis on the detailed implementation plan
- **Specification Structure Preservation**: Maintain standardized specification format
- **Comprehensive Impact Assessment**: Analyze direct and indirect effects
- **End-to-End Workflow Mapping**: Understand affected business processes
- **Enterprise Architecture Awareness**: Respect platform patterns
- **Quality-Focused Testing**: Create comprehensive test specifications
- **Specification Completeness**: Ensure full traceability
- **Risk Assessment and Mitigation**: Identify risks and provide rollback strategies
- **Bidirectional Traceability**: Maintain clear mapping between plan and spec
- **Coverage Preservation**: Maintain existing test coverage while adding new

## Related

- `planning`
- `feature-implementation`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
  1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
  2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## REMINDER — Planning-Only Skill

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with user approval after analysis.
> **ASK** user to confirm findings before any execution begins.
> **ASK** user for clarification when multiple approaches exist.
