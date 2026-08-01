---
name: context-engineering
description: Comprehensive context engineering and management system based on the
  framework C = A(c₁, c₂, c₃, c₄, c₅, c₆). Use this skill when users work with context
  files, ask about context engineering, need to
---

---
name: Context Engineering
description: Comprehensive context engineering and management system based on the framework C = A(c₁, c₂, c₃, c₄, c₅, c₆). Use this skill when users work with context files, ask about context engineering, need to create/update/analyze contexts, validate context quality, detect discrepancies between contexts, or manage their Context Engineering system. Triggers include: "create a context", "analyze context", "check for inconsistencies", "validate context quality", "update context", "context engineering", "manage contexts", "c1-c6 components", or when working with .claude/contexts/ directories.
---

# Context Engineering Skill

Expert system for managing the complete lifecycle of context files in Context Engineering systems based on the framework **C = A(c₁, c₂, c₃, c₄, c₅, c₆)**.

## Core Capabilities

This skill provides comprehensive context management including:

- **Classification**: Categorize content into the correct component type (c₁-c₆)
- **Creation**: Generate well-structured context files from source materials
- **Analysis**: Evaluate context quality using the 4-dimensional framework
- **Validation**: Detect contradictions, gaps, and discrepancies across contexts
- **Updates**: Evolve contexts with proper semantic versioning
- **Inventory**: List, categorize, and manage context portfolios

## Communication Principles

- **Decisive**: Make clear recommendations with transparent reasoning ("This is c₂ because...", not "Could be c₁ or c₂...")
- **Quantified**: Use quality grades (A-F), numeric scores (0.XX), estimated impact when possible
- **Actionable**: Provide specific steps ("Update lines 45-67 of file.md"), not generalities
- **Conservative with destructive changes**: Ask confirmation before deleting contexts or making MAJOR changes
- **Autonomous with low-risk operations**: Create, list, analyze without constantly asking
- **Offer next steps**: Always end with "Would you like me to...?" or "Next steps: [1] [2] [3]"

## Framework Overview

### The Six Components

**C = A(c₁, c₂, c₃, c₄, c₅, c₆)** where:
- **c₁ (Instructions)**: HOW to do things - methodologies, workflows, processes
- **c₂ (Knowledge)**: WHAT things are - domain knowledge, theories, frameworks
- **c₃ (Tools)**: Technical capabilities - APIs, functions, available tools
- **c₄ (Memory)**: Past experiences - decisions, learnings, historical context
- **c₅ (State)**: Current situation - active resources, present configuration
- **c₆ (Query)**: Immediate request - user's current question or task

### Quality Framework

Quality is measured across 4 dimensions:

**Q = α·Relevance + β·Completeness + γ·Consistency + δ·Efficiency**

Where:
- **α = 0.40** (Relevance): I(Context; Query) - mutual information
- **β = 0.30** (Completeness): Coverage of required elements
- **γ = 0.20** (Consistency): Absence of contradictions
- **δ = 0.10** (Efficiency): Information density per token

**Grading Scale:**
- **A (≥0.90)**: Excellent, production-ready
- **B (0.80-0.89)**: Good, minor improvements optional
- **C (0.70-0.79)**: Acceptable, refinement recommended
- **D (0.60-0.69)**: Deficient, requires significant work
- **F (<0.60)**: Inadequate, consider rewriting

## Instructions (c₁)

Detailed methodologies and workflows for context management:

- [Component Classification](c1-instructions/01_component_classification.md) - Decision tree for classifying content into c₁-c₆
- [Context Creation](c1-instructions/02_context_creation.md) - 6-step workflow for creating new contexts
- [Context Updates](c1-instructions/03_context_updates.md) - Process for updating contexts with semantic versioning
- [Context Deletion](c1-instructions/04_context_deletion.md) - Safe workflow for removing obsolete contexts
- [Inventory & Listing](c1-instructions/05_inventory_listing.md) - Methods for inventorying and cataloging contexts
- [Individual Quality Analysis](c1-instructions/06_individual_quality_analysis.md) - 4-dimensional framework for quality evaluation
- [Discrepancy Detection](c1-instructions/07_discrepancy_detection.md) - Process for detecting contradictions between contexts
- [Interaction Patterns](c1-instructions/08_interaction_patterns.md) - 5 patterns for context management interactions
- [Communication Principles](c1-instructions/09_communication_principles.md) - Guidelines for decisive, quantified, actionable communication
- [Context Retrieval Protocol](c1-instructions/10_context_retrieval_protocol.md) - Multi-agent strategy for loading relevant contexts before tasks
- [Continuous Learning Feedback](c1-instructions/11_continuous_learning_feedback.md) - Feedback loop for continuous improvement after significant tasks

## Knowledge (c₂)

Theoretical foundations, frameworks, and algorithms:

- [Component Theory](c2-knowledge/01_component_theory.md) - Complete theory of the C = A(c₁-c₆) framework
- [4-Dimensional Quality Framework](c2-knowledge/02_4_dimensional_quality_framework.md) - Quality formula: Q = α·R + β·C + γ·S + δ·E
- [Grading Scale](c2-knowledge/03_grading_scale.md) - A-F scale for context quality
- [Semantic Versioning](c2-knowledge/04_semantic_versioning.md) - MAJOR.MINOR.PATCH versioning principles
- [Contradiction Detection Algorithm](c2-knowledge/05_contradiction_algorithm.md) - Pseudocode for detecting contradictions
- [Completeness Algorithm](c2-knowledge/06_completeness_algorithm.md) - Algorithm for evaluating context completeness
- [Dependency Algorithm](c2-knowledge/07_dependency_algorithm.md) - Validation of references and dependencies
- [Metadata Standards](c2-knowledge/08_metadata_standards.md) - YAML frontmatter standards
- [Content Standards](c2-knowledge/09_content_standards.md) - Best practices for content structure

## Templates

Reusable markdown templates for standardized reporting:

- [Quality Report Template](templates/quality_report_template.md) - Template for individual quality analysis reports
- [Discrepancy Report Template](templates/discrepancy_report_template.md) - Template for contradiction and gap reports
- [Autonomy Rules](c1-instructions/12_autonomy_rules.md) - Decision framework for when to ask confirmation vs act autonomously

## Usage Guidelines

### When to Use This Skill

- User is working with context files in their project
- Creating new contexts from source documents (PDFs, docs, etc.)
- Analyzing existing contexts for quality or completeness
- Validating consistency across multiple contexts
- Updating contexts with new information
- Managing the context portfolio (listing, prioritizing, organizing)
- Troubleshooting context-related issues

### Typical Workflows

**1. Creating a New Context:**
1. Analyze source material
2. Classify into appropriate component (c₁-c₆)
3. Extract and structure content
4. Apply metadata standards
5. Validate quality
6. Save to appropriate location

**2. Analyzing Context Quality:**
1. Read context file
2. Evaluate across 4 dimensions (Relevance, Completeness, Consistency, Efficiency)
3. Calculate quality score and grade
4. Identify specific improvement opportunities
5. Generate quality report

**3. Detecting Discrepancies:**
1. Identify related contexts
2. Extract claims and assertions
3. Cross-reference for contradictions
4. Identify gaps and missing links
5. Generate discrepancy report with recommendations

## Progressive Disclosure

Supporting documentation is loaded only when needed to manage context efficiently. Claude will reference the appropriate instruction files, knowledge bases, or templates based on the specific task at hand.

## Version

**Skill Version**: 1.1.0
**Last Updated**: 2025-10-24
**Framework**: Context Engineering C = A(c₁, c₂, c₃, c₄, c₅, c₆)

**Changelog:**
- 1.1.0 (2025-10-24): Added context retrieval protocol and continuous learning feedback instructions
- 1.0.0 (2025-01-22): Initial release
