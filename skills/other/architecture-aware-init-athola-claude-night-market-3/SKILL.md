---
name: architecture-aware-init
description: Selects architecture paradigm via research before scaffolding. Use when architecture is undecided and the choice needs justification and documentation.
alwaysApply: false
category: project-initialization
tags:
- architecture
- initialization
- research
- decision-making
- best-practices
dependencies:
- archetypes:architecture-paradigms
tools: []
usage_patterns:
- new-project-setup
- architecture-selection
- best-practices-research
- template-customization
complexity: advanced
model_hint: deep
estimated_tokens: 1800
progressive_loading: true
modules:
- modules/research-flow.md
- modules/paradigm-selection.md
- modules/scaffold-generation.md
- modules/script-integration.md
---

# Architecture-Aware Project Initialization

## Overview

Project initialization that combines online research, archetype
selection, template customization, and decision documentation
into one workflow. Use this skill when the architecture is
undecided and the choice deserves justification.

## When to Use This Skill

- Starting a new project and unsure which architecture fits best
- Wanting modern, industry-standard architecture choices
- Needing justification for architectural decisions
- Wanting templates customized to the chosen paradigm

Use **instead of** `project-init` when architecture is undecided.
Use **before** `project-specification` to establish the
architectural foundation.

## Required TodoWrite Items

1. `arch-init:research-completed` -- Online research completed
2. `arch-init:paradigm-selected` -- Architecture paradigm chosen
3. `arch-init:templates-customized` -- Templates adapted to paradigm
4. `arch-init:decision-recorded` -- ADR created

## 5-Step Workflow

### Steps 1-2: Gather context, research best practices

Load `modules/research-flow.md` for the full project-context
questionnaire and the three-tier search strategy. Output: a
synthesis brief that feeds Step 3.

### Step 3: Select the architecture paradigm

Load `modules/paradigm-selection.md` for the decision matrix
(team size by domain complexity) and the special-case overrides
(streaming, serverless, microkernel, etc.). Two routes:

- Use the `archetypes:architecture-paradigms` skill for guided
  exploration.
- Use the matrix directly for a fast recommendation.

### Step 4-5: Customize templates and record the decision

Load `modules/scaffold-generation.md` for the paradigm-specific
directory layouts (Functional Core / Hexagonal / Microservices
shown; others delegated to the corresponding
`archetypes:architecture-paradigm-{name}` skill) and the ADR
template.

## Output: Initialization Package

After completing the workflow, the project has:

1. A directory structure matched to the chosen architecture
2. Configuration that reflects the paradigm (test layout,
   tooling, dependency hints)
3. An ADR explaining why this paradigm was chosen
4. Links to the relevant paradigm skill for ongoing
   implementation guidance
5. References to similar real-world projects from Step 2

## Script Integration

The interactive workflow above is the default. For automation,
load `modules/script-integration.md` for the three Python
helpers under `plugins/attune/scripts/` (architecture researcher,
template customizer, full interactive flow) and library-style
import examples.

## Integration with Existing Commands

This skill enhances `/attune:project-init` by adding an
architecture-selection phase before scaffolding:

```bash
# Standard initialization (no architecture decision)
/attune:project-init --lang python --name my-project

# Architecture-aware initialization
/attune:brainstorm                  # Explore project needs
Skill(architecture-aware-init)      # Select architecture
/attune:project-init --arch <paradigm> --name my-project
```

## Example Session

User: "I'm creating a Python web API for a fintech application.
Team of 8 developers, complex business rules, need high security
and audit trails."

- Step 1 context: Web API, highly complex domain, 5-15
  engineers, security and auditability requirements.
- Step 2 research: queries for fintech API patterns, audit-trail
  architecture, CQRS+ES Python examples.
- Step 3 selection: research plus decision matrix yields CQRS +
  Event Sourcing.
- Step 4 templates: command-handler module, query-handler
  module, event store, aggregate patterns, projection handlers.
- Step 5 ADR: documents why CQRS/ES fits (auditability, complex
  rules, regulatory compliance).

Result: project initialized with paradigm-appropriate structure
and clear decision rationale.

## Related Skills

- `Skill(archetypes:architecture-paradigms)` -- paradigm catalog
- `Skill(archetypes:architecture-paradigm-*)` -- per-paradigm
  implementation guidance
- `Skill(attune:project-brainstorming)` -- ideation before
  architecture
- `Skill(attune:project-specification)` -- requirements after
  the paradigm is chosen

## See Also

- `/attune:project-init` -- basic project initialization
- `/attune:blueprint` -- architecture planning after paradigm
  selection
- `plugins/archetypes/README.md` -- full paradigm reference
