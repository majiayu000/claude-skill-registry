---
name: foundation-first
category: design
version: 2.0.0
description: Build on psychology, personas, journeys, emotions—BEFORE code (Australian-enhanced)
author: Unite Group
priority: 2
triggers:
  - foundation
  - persona
  - journey
  - psychology
  - user research
  - ux
  - emotional design
  - acceptance criteria
---

# Foundation-First Architecture

Build on psychology, personas, journeys, emotions, scenarios, quality, and metrics—BEFORE code.

## The 7-Layer Foundation

| Layer | Focus | Key Files |
|-------|-------|-----------|
| 7 | Business Alignment | AARRR metrics, sales funnel |
| 6 | Quality Standards | Nielsen heuristics, page scores |
| 5 | Acceptance Criteria | BDD scenarios (Gherkin) |
| 4 | Emotional Architecture | Step-by-step emotional states |
| 3 | Journey Mapping | Stages, steps, routes |
| 2 | User Definition | Personas with psychology |
| 1 | Psychology Foundation | Cialdini, Fogg, cognitive psychology |
| + | Structural | 8 missing states checklist |

## Psychology Quick Reference

**Cialdini's 7 Principles:** Reciprocity, Commitment, Social Proof, Authority, Liking, Scarcity, Unity

**Fogg Model:** Behavior = Motivation × Ability × Prompt

**AARRR Metrics:** Acquisition → Activation → Retention → Revenue → Referral

## The 8 Missing States

Every component needs: Empty, Loading, Error, Success, Partial, Offline, Permission, Confirmation

## Workflow

```bash
# 1. Define persona with psychology
cp .journeys/_templates/persona-enhanced.template.yaml .journeys/personas/my-user.yaml

# 2. Map core journey
cp .journeys/_templates/journey.template.yaml .journeys/journeys/core-journey.yaml

# 3. Add emotional architecture
cp .journeys/_templates/emotional-map.template.yaml .journeys/emotions/journey-emotions.yaml

# 4. Write acceptance criteria
cp .journeys/_templates/scenario.template.feature .journeys/scenarios/feature.feature
```

## The Shift

| Old Way | Foundation-First |
|---------|------------------|
| "Build a form" | "Enable user to commit to action" |
| "Add validation" | "Prevent user feeling stupid" |
| "Show error" | "Help user understand and fix" |
| "Track clicks" | "Measure journey conversion" |
| "Design page" | "Design all 8 states" |

## Australian Market Context

### Cultural Psychology
- **Mateship**: Build trust through straightforward communication, no corporate jargon
- **Tall Poppy**: Avoid bragging, let results speak (testimonials > self-promotion)
- **Fair Go**: Emphasize value, honesty, no hidden fees
- **Tradie Culture**: Practical, no-nonsense UX for tradies (contractors, builders, restorers)

### Australian Personas
When creating personas for Australian market:
- Include location context (Brisbane, Sydney, Melbourne)
- Reference Australian regulations (Privacy Act 1988, WHS)
- Use Australian language (colour, organisation, licence)
- Consider regional differences (QLD tropical vs VIC temperate)

### Australian Journey Mapping
- Account for Australian timezone (AEST/AEDT)
- Consider mobile-first (high smartphone usage)
- Include offline states (regional areas, spotty reception)
- Reference Australian payment methods (BPAY, POLi, EFTPOS)

## Design System Integration (2025-2026)

**CRITICAL**: All foundation work must align with locked design system:
- **Tokens**: Reference `.claude/data/design-tokens.json`
- **Aesthetic**: Bento grids, glassmorphism, micro-interactions
- **Icons**: NO Lucide (deprecated) - AI-generated custom only
- **Shadows**: Soft colored (NEVER pure black)
- **Colors**: Primary #0D9488 (teal), semantic colors

## Acceptance Criteria Template (Australian)

```gherkin
Feature: [Feature Name]
  As a [Australian persona]
  I want to [goal]
  So that [Australian market benefit]

  Background:
    Given the user is in Brisbane, Australia
    And the date format is DD/MM/YYYY
    And currency is displayed as AUD

  Scenario: [Happy path]
    Given [initial state]
    When [action]
    Then [expected outcome with Australian context]
    And [emotional state: confident/relieved/empowered]

  Scenario: Error state (Australian compliance)
    Given [error condition]
    When [action]
    Then [error message in en-AU]
    And [help text references Australian regulations if applicable]
    And [emotional state: supported, not blamed]
```

## Rules

- Ask "which journey?" before coding
- Reference psychology in design decisions
- Check emotional states in code reviews
- Include journey context in bug reports
- No component ships without 8 states
- **NEW**: Verify Australian context in all UX copy (en-AU spelling)
- **NEW**: Validate design against locked tokens (NO Lucide icons)

## Integration with Spec Builder

This skill is automatically loaded by `.claude/agents/spec-builder/` during the 6-phase interview:
- **Phase 1 (Vision)**: Psychology principles applied
- **Phase 2 (Users)**: Personas with Australian context
- **Phase 3 (Technical)**: 8 states checklist
- **Phase 4 (Design)**: Design system integration
- **Phase 5 (Business)**: AARRR metrics
- **Phase 6 (Implementation)**: Acceptance criteria

See: `.journeys/`, `MASTER-INDEX.yaml`
