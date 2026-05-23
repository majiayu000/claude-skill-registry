---
name: plan-generator
description: Creates structured plans from requirements. Generates comprehensive plans with steps, dependencies, risks, and success criteria. Coordinates with specialist agents for planning input and validates plan completeness.
allowed-tools: read, write, glob, search, codebase_search, Task
version: 1.0
best_practices:
  - Coordinate with Analyst, PM, Architect for planning input
  - Break down requirements into actionable steps (≤7 per section)
  - Identify dependencies and sequencing
  - Assess risks with mitigation strategies
  - Validate plan completeness and feasibility
error_handling: graceful
streaming: supported
templates: [feature-plan, refactoring-plan, migration-plan, architecture-plan]
---

<identity>
Plan Generator Skill - Creates structured, validated plans from requirements by coordinating with specialist agents and generating comprehensive planning artifacts.
</identity>

<capabilities>
- Creating plans for new features
- Planning refactoring efforts
- Planning system migrations
- Planning architecture changes
- Breaking down complex requirements
- Validating existing plans
</capabilities>

<instructions>
<execution_process>

### Step 1: Analyze Requirements

Parse user requirements:

- Extract explicit requirements
- Identify implicit requirements
- Determine planning scope
- Assess complexity

### Step 2: Coordinate Specialists

Request planning input from relevant agents:

- **Analyst**: Business requirements and market context
- **PM**: Product requirements and user stories
- **Architect**: Technical architecture and design
- **Database Architect**: Data requirements
- **UX Expert**: Interface requirements

### Step 3: Generate Plan Structure

Create plan following template:

- Load template from `.factory/templates/plan-template.md`
- Define objectives
- Break down into steps (≤7 steps per section)
- Identify dependencies
- Assign agents to steps

### Step 4: Assess Risks

Identify risks and mitigation:

- Technical risks
- Resource risks
- Timeline risks
- Dependency risks
- Mitigation strategies

### Step 5: Validate Plan

Validate plan completeness:

- All requirements addressed
- Dependencies mapped
- Success criteria defined
- Risks identified
- Plan is feasible

### Step 6: Generate Artifacts

Create plan artifacts:

- Plan markdown: `.factory/context/artifacts/plan-<id>.md`
- Plan JSON: `.factory/context/artifacts/plan-<id>.json`
- Plan summary
  </execution_process>

<plan_types>
**Feature Development Plan**:

- Objectives: Feature goals
- Steps: Analysis → Design → Implementation → Testing
- Agents: Analyst → PM → Architect → Developer → QA

**Refactoring Plan**:

- Objectives: Code quality goals
- Steps: Analysis → Planning → Implementation → Validation
- Agents: Code Reviewer → Refactoring Specialist → Developer → QA

**Migration Plan**:

- Objectives: Migration goals
- Steps: Analysis → Planning → Execution → Validation
- Agents: Architect → Legacy Modernizer → Developer → QA

**Architecture Plan**:

- Objectives: Architecture goals
- Steps: Analysis → Design → Validation → Documentation
- Agents: Architect → Database Architect → Security Architect → Technical Writer
  </plan_types>

<integration>
**Integration with Planner Agent**:
Planner agent uses this skill to:
- Generate plans from requirements
- Coordinate specialist input
- Validate plan completeness
- Track plan execution
</integration>

<best_practices>

1. **Coordinate Early**: Get specialist input before finalizing plan
2. **Keep Steps Focused**: ≤7 steps per plan section
3. **Map Dependencies**: Clearly identify prerequisites
4. **Assess Risks**: Identify and mitigate risks proactively
5. **Validate Thoroughly**: Ensure plan is complete and feasible
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Example Plan Output**

**Command**: "Generate plan for user authentication feature"

**Generated Plan**:

```markdown
# Plan: User Authentication Feature

## Objectives

- Implement JWT-based authentication
- Support login, logout, and session management
- Provide secure password handling

## Steps

### Step 1: Requirements Analysis

- **Agent**: analyst
- **Dependencies**: none
- **Tasks**: Analyze auth requirements, research best practices
- **Success Criteria**: Requirements document complete

### Step 2: Architecture Design

- **Agent**: architect
- **Dependencies**: Step 1
- **Tasks**: Design auth architecture, select technologies
- **Success Criteria**: Architecture document complete

### Step 3: Implementation

- **Agent**: developer
- **Dependencies**: Step 2
- **Tasks**: Implement auth endpoints, JWT handling, password hashing
- **Success Criteria**: All tests passing, code reviewed

### Step 4: Testing

- **Agent**: qa
- **Dependencies**: Step 3
- **Tasks**: Write tests, perform security testing
- **Success Criteria**: Test coverage >80%, security validated
```

</formatting_example>
</examples>
