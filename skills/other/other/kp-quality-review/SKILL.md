---
name: kp-quality-review
description: "Reviews knowledge pack quality: educational accuracy, grade-level appropriateness, accessibility compliance, learning pathway coherence, assessment alignment, and parallel instruction pattern conformance. Use when reviewing pack content after validation."
metadata:
  extensions:
    gsd-skill-creator:
      triggers:
        intents:
          - "pack.*review"
          - "pack.*quality"
          - "education.*review"
          - "accessibility.*check"
        files:
          - "src/knowledge/packs/**/.skillmeta"
          - "src/knowledge/packs/**/vision.md"
        contexts:
          - "pack quality review"
          - "educational review"
        threshold: 0.7
      token_budget: "1.0%"
      version: 1
      enabled: true
      plan_origin: "244-chipset-agent-definitions"
      phase_origin: "244"
---

# Quality Review

## Purpose

Reviews pack content for educational quality beyond schema compliance. The KP-06 reviewer agent uses this skill to assess educational accuracy, grade-level appropriateness, accessibility compliance, learning pathway coherence, and assessment alignment with stated learning outcomes. Also verifies that parallel instruction patterns (NFR-06) are consistently applied across packs for token caching optimization.

## Capabilities

- Educational accuracy review: content factually correct, age-appropriate, culturally sensitive
- Grade-level appropriateness: activities match stated grade ranges, complexity scales properly
- Accessibility compliance: .skillmeta includes accessibility metadata fields, content is screen-reader-friendly
- Learning pathway coherence: module prerequisites form a valid DAG, pathways cover all learning styles
- Assessment alignment: rubric criteria map to stated learning outcomes, formative/summative balance
- Parallel instruction pattern conformance: packs use shared template structure for caching (NFR-06)
- Cross-pack consistency: similar subjects use consistent terminology, formatting, and structure
- Content completeness: vision docs cover all required sections, activities span all grade levels

## Review Checklist

1. Vision document has Vision, Problem Statement, Core Concepts, Modules, Assessment, Parent Guidance sections
2. Modules YAML has correct prerequisite ordering (no forward references within pack)
3. Activities span at least 3 of 5 learning pathways (Maker, Academic, Curiosity, Social, Parent-Guided)
4. Assessment rubric has all 4 levels (Beginning, Developing, Proficient, Advanced)
5. Resources are categorized by audience and include at least 3 categories
6. .skillmeta grade_levels cover Foundation through at least High School
7. Parallel instruction patterns are followed (shared sections use template format)
8. Accessibility stubs present in .skillmeta
9. Translation stubs present in .skillmeta

## Dependencies

- kp-content-validation skill must pass first (validator is the gate)
- Pack runtime API for structured access to pack content

## Token Budget Rationale

1.0% budget covers the review methodology, checklist, and quality criteria. The reviewer reads pack content but does not hold validation engine internals, keeping context focused on quality dimensions.
