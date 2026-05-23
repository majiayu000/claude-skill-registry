---
name: faion-user-researcher
description: "User research: personas, user interviews, jobs-to-be-done, pain point research."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Task, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# User Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

User research and validation for product/startup development. Handles personas, user interviews, jobs-to-be-done, pain point mining, problem validation, survey design, and value proposition testing.

## Context Discovery

### Auto-Investigation

Check these signals before starting user research:

| Signal | Location | What to Check |
|--------|----------|---------------|
| Existing personas | .aidocs/product_docs/user-personas.md | Current user archetypes |
| Pain points | .aidocs/product_docs/pain-points.md | Known user problems |
| Interview data | .aidocs/product_docs/interview-notes/ | Previous interview findings |
| JTBD framework | .aidocs/product_docs/jobs-to-be-done.md | User motivations |
| Value proposition | .aidocs/product_docs/value-proposition.md | Problem-solution fit |
| Survey data | .aidocs/product_docs/surveys/ | Quantitative research |
| User validation | .aidocs/product_docs/problem-validation.md | Validation results |
| Product specs | .aidocs/todo/, .aidocs/in-progress/ | Current feature development |
| Analytics | .aidocs/product_docs/analytics/ | User behavior data |
| Customer feedback | Support tickets, reviews | Real user complaints/requests |

### Discovery Questions

```yaml
- question: "What user research do you need?"
  header: "Research Type"
  multiSelect: false
  options:
    - label: "Build user personas"
      description: "Create user archetypes and profiles"
    - label: "Conduct user interviews"
      description: "Talk to users to understand needs"
    - label: "Identify pain points"
      description: "Research user problems and frustrations"
    - label: "Jobs-to-be-done analysis"
      description: "Understand user motivations and context"
    - label: "Problem validation"
      description: "Validate if problem is worth solving"
    - label: "Value proposition design"
      description: "Define how product solves user problems"

- question: "What stage is your product in?"
  header: "Product Stage"
  multiSelect: false
  options:
    - label: "Idea/concept"
      description: "No product yet, exploring problem space"
    - label: "Pre-launch"
      description: "Building MVP, validating problem-solution fit"
    - label: "Post-launch"
      description: "Have users, optimizing product"

- question: "Do you have access to target users?"
  header: "User Access"
  multiSelect: false
  options:
    - label: "Yes, existing user base"
      description: "Can interview/survey current users"
    - label: "Need to recruit users"
      description: "Will find target users in communities"
    - label: "No users yet"
      description: "Will use secondary research/personas"

- question: "What's your primary research goal?"
  header: "Research Goal"
  multiSelect: false
  options:
    - label: "Understand user needs"
      description: "Discover what problems users have"
    - label: "Validate problem exists"
      description: "Confirm problem is worth solving"
    - label: "Test solution fit"
      description: "Check if product solves user problems"
    - label: "Segment users"
      description: "Identify different user types"
```

---

## Quick Reference

| Research Area | Key Files |
|---------------|-----------|
| **Personas** | persona-building.md, ai-persona-building.md, audience-segmentation.md |
| **Interviews** | user-interviews.md, user-interviews-methods.md, ai-interview-analysis.md |
| **Pain Points** | pain-point-research.md, problem-validation.md |
| **Validation** | validation-methods.md, user-validation-methods.md, problem-validation-2026.md |
| **JTBD** | jobs-to-be-done.md |
| **Value Prop** | value-proposition-design.md |
| **Surveys** | survey-design.md, user-research-at-scale.md |
| **Use Cases** | use-case-mapping.md, feature-discovery.md |

---

## Decision Tree

| If you need... | Use |
|---------------|-----|
| User profiles | persona-building.md, ai-persona-building.md |
| Pain points | pain-point-research.md, problem-validation.md |
| User motivations | jobs-to-be-done.md |
| Value proposition | value-proposition-design.md |
| Interview structure | user-interviews.md, user-interviews-methods.md |
| Validate problem | problem-validation.md, validation-methods.md |
| Survey questions | survey-design.md |
| Segment users | audience-segmentation.md |
| Map use cases | use-case-mapping.md, feature-discovery.md |
| Define success metrics | success-metrics-definition.md |

---

## Research Modes

| Mode | Output | Files Used |
|------|--------|------------|
| personas | user-personas.md | persona-building.md, ai-persona-building.md |
| pains | pain-points.md | pain-point-research.md, problem-validation.md |
| validate | problem-validation.md | validation-methods.md, problem-validation-2026.md |
| interviews | interview-guide.md | user-interviews.md, user-interviews-methods.md |
| jtbd | jobs-to-be-done.md | jobs-to-be-done.md |

---

## Methodologies (21)

### Persona Building (4)
- Persona building
- AI-assisted persona building
- AI persona building
- Audience segmentation

### User Interviews (4)
- User interviews
- User interviews methods
- AI interview analysis
- User research at scale

### Problem & Pain Points (3)
- Pain point research
- Problem validation
- Problem validation 2026

### Validation Methods (3)
- Validation methods
- User validation methods
- Synthetic users

### Jobs-to-be-Done (1)
- Jobs-to-be-done framework

### Value & Use Cases (4)
- Value proposition design
- Use case mapping
- Feature discovery
- Opportunity solution trees

### Research Instruments (2)
- Survey design
- Success metrics definition

---

## Key Frameworks

| Framework | Purpose | File |
|-----------|---------|------|
| **JTBD** | User motivations & context | jobs-to-be-done.md |
| **Value Prop Canvas** | Problem-solution fit | value-proposition-design.md |
| **Mom Test** | Interview questions | user-interviews-methods.md |
| **Persona Template** | User archetypes | persona-building.md |
| **Opportunity Solution Trees** | Feature prioritization | opportunity-solution-trees.md |

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Personas | user-personas.md |
| Pain Points | pain-points.md |
| Validation | problem-validation.md |
| Interviews | interview-guide.md |
| JTBD | jobs-to-be-done.md |
| Value Prop | value-proposition.md |
| Surveys | survey-questionnaire.md |

---

## Integration

### Parent Skill
Orchestrated by `faion-researcher` skill.

### Related Sub-Skills
- **faion-market-researcher** - Market sizing, competitors, pricing

### Next Steps
After user research complete:
- UX design → `faion-ux-ui-designer`
- Feature specs → `faion-sdd`
- Product roadmap → `faion-product-manager`

---

*faion-user-researcher v1.0*
*Sub-skill of faion-researcher*
*21 methodologies | User Research & Validation*
