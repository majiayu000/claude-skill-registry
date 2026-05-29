---
id: US-003
feature: FS-155
title: Convert Tech-Lead Agent to Skill
status: completed
priority: P0
created: 2026-01-06
project: specweave
external:
  github:
    issue: 992
    url: https://github.com/anton-abyzov/specweave/issues/992
---

# US-003: Convert Tech-Lead Agent to Skill

**Feature**: [FS-155](./FEATURE.md)

**As a** user asking about code quality
**I want** the Tech-Lead skill to auto-activate
**So that** I get code review guidance automatically

---

## Acceptance Criteria

- [x] **AC-US3-01**: Tech-Lead moved from `agents/tech-lead/` to `skills/tech-lead/SKILL.md`
- [x] **AC-US3-02**: Description optimized for "code review", "best practices"
- [x] **AC-US3-03**: Review checklists in progressive disclosure
- [x] **AC-US3-04**: Skill activates for code quality prompts

---

## Implementation

**Increment**: [0155-native-plugin-skill-architecture](../../../../increments/0155-native-plugin-skill-architecture/spec.md)

**Tasks**: See increment tasks.md for implementation details.


## Tasks

- [x] **T-003**: Convert Tech-Lead Agent to Skill
- [x] **T-004**: Convert QA-Lead Agent to Skill
- [x] **T-005**: Convert Security Agent to Skill
- [x] **T-006**: Convert Docs-Writer Agent to Skill
- [x] **T-007**: Convert Other Domain Agents to Skills
