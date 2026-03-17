---
# VERSION: 2.88.0
name: prd
description: "Product Requirements Document generation and management with INVEST-compliant user stories"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

# PRD System

Generate and manage Product Requirements Documents (PRDs) with INVEST-compliant user stories for structured task breakdown.

## When to Use

- Planning new features or major enhancements
- Breaking down complex projects into user stories
- Creating structured task lists for Ralph Loop execution
- Documenting requirements for team collaboration
- Converting PRDs into actionable implementation tasks

## PRD Structure

| Section | Purpose |
|---------|---------|
| **Overview** | Brief description and business value |
| **Goals** | Measurable objectives |
| **User Stories** | INVEST-compliant stories with acceptance criteria |
| **Technical Requirements** | Architecture, stack, dependencies, security |
| **Success Criteria** | Metrics and targets |
| **Out of Scope** | What's explicitly NOT included |
| **Implementation Plan** | Phased tasks breakdown |
| **Risks & Mitigations** | Potential issues and solutions |

## Commands

### Create PRD
```
ralph prd create "Implement OAuth2 authentication"
ralph prd create "Add real-time notifications" --priority high
```
Creates file in `tasks/prd-<feature>.md`

### Convert to Stories
```
ralph prd convert tasks/prd-auth.md
```
Creates actionable user stories in `tasks/prd-auth.json`

### Show Status
```
ralph prd status
```
Shows progress across all PRDs

### Get Next Story
```
ralph prd next
```
Returns next uncompleted story

## User Story Format (INVEST)

```
As a {{persona}},
I want to {{action}},
So that {{benefit}}.

Acceptance Criteria:
- [ ] {{criterion_1}}
- [ ] {{criterion_2}}
- [ ] {{criterion_3}}
```

**INVEST Principles:**
- **I**ndependent: Can be completed standalone
- **N**egotiable: Details can be adjusted
- **V**aluable: Provides user/business value
- **E**stimable: Complexity can be estimated
- **S**mall: Fits within iteration limits
- **T**estable: Clear acceptance criteria

## Integration with Ralph Loop

```
0. PRD CREATION     → ralph prd create "feature"
1. /clarify         → Intensive questions (populate PRD)
2. /classify        → Complexity routing
3. PLAN             → User approval (review PRD)
4. PRD CONVERSION   → ralph prd convert tasks/prd-feature.md
5. EXECUTION        → ralph loop --prd tasks/prd-feature.json
6. /gates           → Quality validation per story
7. /retrospective   → Propose PRD improvements
→ VERIFIED_DONE
```

## Best Practices

1. **Start with Overview** - Clear problem statement before solutions
2. **Measurable Goals** - Use specific metrics (e.g., "reduce load time by 30%")
3. **INVEST Stories** - Ensure each story is independent and testable
4. **Scope Management** - Explicitly document "Out of Scope" items
5. **Risk Assessment** - Identify risks early with mitigations
6. **Stakeholder Review** - Get approval before converting to stories
7. **Iterative Execution** - Execute one story at a time with validation

## Related Skills

- `/clarify` - Intensive questions (populate PRD details)
- `/loop` - Execute PRD stories iteratively
- `/orchestrator` - Full workflow with PRD integration
- `/plan` - Plan-state management for execution tracking
