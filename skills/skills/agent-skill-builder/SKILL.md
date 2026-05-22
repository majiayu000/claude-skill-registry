---
name: Building Agent Skills
description: Assists in creating Agent Skills of varying complexity levels (simple, moderate, complex). Use when the user wants to create, design, or build a new Agent Skill, or when they need guidance on skill architecture, workflow design, schema validation, or template structure.
---

# Overview

This skill enables the creation of Agent Skills following established best practices and patterns. It provides a structured workflow for gathering requirements, determining appropriate complexity (archetype), planning structure, generating artifacts, and validating the resulting skill.

The skill supports three archetypes:
- **Simple**: Single SKILL.md with inline instructions
- **Moderate**: SKILL.md with separate reference files
- **Complex**: Full Phase/Stage/Step hierarchy with schemas and scripts

# Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Workflow: Building Agent Skills](#workflow-building-agent-skills)
  - [Important Workflow Guidelines](#important-workflow-guidelines)
  - [Phase 1: Discovery](#phase-1-discovery)
    - [Stage 1: Requirements Gathering](#stage-1-requirements-gathering)
    - [Stage 2: Analysis](#stage-2-analysis)
  - [Phase 2: Planning](#phase-2-planning)
    - [Stage 3: Design](#stage-3-design)
  - [Phase 3: Implementation](#phase-3-implementation)
    - [Stage 4: Foundation](#stage-4-foundation)
    - [Stage 5: References](#stage-5-references)
    - [Stage 6: Automation](#stage-6-automation)
  - [Phase 4: Validation](#phase-4-validation)
    - [Stage 7: Quality Assurance](#stage-7-quality-assurance)
  - [Phase 5: Iteration](#phase-5-iteration)
    - [Stage 8: Refinement](#stage-8-refinement)

# Prerequisites

**Before starting the workflow** you **MUST**:
1. Present complete workflow structure (Phases, Stages, Steps) to user
2. Explain Phase approval gates
3. Wait for user acknowledgment

# Workflow: Building Agent Skills

This workflow guides you through creating an Agent Skill from requirements to validation. The workflow is organized into five distinct phases:

**Phase 1: Discovery** - Gather requirements and analyze complexity needs.

**Phase 2: Planning** - Design the skill structure and file organization.

**Phase 3: Implementation** - Generate all skill artifacts.

**Phase 4: Validation** - Verify skill correctness and quality.

**Phase 5: Iteration** - Refine based on feedback and ensure readiness.

## Important Workflow Guidelines

**When executing this workflow** you **MUST**:
- Follow Phases, Stages, and Steps in order
- Announce Stage completions to the user
- Present complete Phase output at Phase boundaries
- Obtain explicit user approval before proceeding to the next Phase

## Phase 1: Discovery

### Stage 1: Requirements Gathering
**Objective**: Understand what the user needs to build

#### Step 1: Gathering Requirements
See [Gathering Requirements Workflow Step Reference](references/workflow/01-gathering-requirements.md) for detailed guidance.

### Stage 2: Analysis
**Objective**: Determine appropriate skill architecture

#### Step 2: Determining Archetype
See [Determining Archetype Workflow Step Reference](references/workflow/02-determining-archetype.md) for detailed guidance.

---

**Phase 1 Approval Gate:** Present complete requirements and archetype decision. Obtain explicit user approval before Phase 2.

---

## Phase 2: Planning

### Stage 3: Design
**Objective**: Create approved blueprint for the skill

#### Step 3: Planning Structure
See [Planning Structure Workflow Step Reference](references/workflow/03-planning-structure.md) for detailed guidance.

---

**Phase 2 Approval Gate:** Present complete structure plan including file manifest and generation order. Obtain explicit user approval before Phase 3.

---

## Phase 3: Implementation

### Stage 4: Foundation
**Objective**: Generate core skill definition

#### Step 4: Generating SKILL.md
See [Generating SKILL.md Workflow Step Reference](references/workflow/04-generating-skill-md.md) for detailed guidance.

### Stage 5: References
**Objective**: Generate supporting documentation

#### Step 5: Generating Workflow References
See [Generating Workflow References Step Reference](references/workflow/05-generating-workflow-references.md) for detailed guidance.

#### Step 6: Generating Schemas
See [Generating Schemas Workflow Step Reference](references/workflow/06-generating-schemas.md) for detailed guidance.

### Stage 6: Automation
**Objective**: Generate executable components

#### Step 7: Generating Scripts
See [Generating Scripts Workflow Step Reference](references/workflow/07-generating-scripts.md) for detailed guidance.

---

**Phase 3 Approval Gate:** Present all generated artifacts for review. Obtain explicit user approval before Phase 4.

---

## Phase 4: Validation

### Stage 7: Quality Assurance
**Objective**: Verify skill correctness

#### Step 8: Validating Skill
See [Validating Skill Workflow Step Reference](references/workflow/08-validating-skill.md) for detailed guidance.

---

**Phase 4 Approval Gate:** Present validation results. Obtain explicit user approval before Phase 5.

---

## Phase 5: Iteration

### Stage 8: Refinement
**Objective**: Incorporate user feedback

#### Step 9: Iterating on Feedback
See [Iterating on Feedback Workflow Step Reference](references/workflow/09-iterating-on-feedback.md) for detailed guidance.
