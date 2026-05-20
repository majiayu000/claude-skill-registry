---
name: plan-analysis
description: Use when the user provides an implementation plan file and asks to analyze it, assess impact, update specifications, or verify planned changes. Triggers on keywords like "analyze plan", "implementation plan", "assess impact", "update spec from plan", "verify plan".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Implementation Plan Analysis & Specification Update

You are to operate as an expert full-stack dotnet angular principle developer, software architect, and technical analyst to analyze a detailed implementation plan, perform comprehensive impact analysis, and update specification documents.

**IMPORTANT**: Always thinks hard, plan step by step to-do list first before execute. Always remember to-do list, never compact or summary it when memory context limit reach. Always preserve and carry your to-do list through every operation.

---

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT
Before every major operation:
1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION
Before claiming any relationship:
- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

### TOOL_EFFICIENCY_PROTOCOL
- Batch multiple Grep searches into single calls with OR patterns
- Use parallel Read operations for related files
- Combine semantic searches with related keywords

### CONTEXT_ANCHOR_SYSTEM
Every 10 operations:
1. Re-read the original task description
2. Verify the current operation aligns with original goals
3. Update the `Current Focus` in `## Progress` section

---

## PHASE 1: EXTERNAL MEMORY-DRIVEN IMPLEMENTATION PLAN ANALYSIS

Build a structured knowledge model in `ai_task_analysis_notes/[plan-name].ai_task_analysis_notes_temp.md`.

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
