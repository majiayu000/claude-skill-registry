---
name: spec-templates
description: Provides reusable markdown templates and outlines for OpenSpec proposals, design docs, ADRs, READMEs, and changelogs.
category: documentation
---

# Spec & Doc Templates

**Trigger Keywords**: template, outline, spec, proposal, ADR, design doc, README, changelog, release notes, structure

**Agent Integration**: Used by `spec-writer`, `technical-writer`, and planning-focused agents when structuring docs before drafting.

## OpenSpec Proposal Outline
```
# Proposal: <Title>
**Change ID:** `<id>`
**Status:** Draft
**Date:** YYYY-MM-DD
**Author:** <name>

## Executive Summary
## Background
## Goals
## Scope / Non-Goals
## Approach
## Risks & Mitigations
## Validation & Metrics
## Open Questions
```

## Tasks Checklist Outline
```
# Implementation Tasks
**Change ID:** `<id>`
**Status:** Draft|Ready for Implementation

## Overview
<short description>

## Tasks
- [ ] High-level task
  - [ ] Subtask with validation note
```

## Spec Delta Outline
```
# Spec: <Capability Name>
**Capability**: <kebab-case>
**Status**: Draft
**Related**: <optional list>

## Overview
<short description>

## ADDED|MODIFIED|REMOVED Requirements
### Requirement: <Title>
<description>

#### Scenario: <Name>
**Given** ...
**When** ...
**Then** ...
```

## ADR Outline
```
# ADR <ID>: <Title>
Status: Proposed|Accepted|Superseded
Date: YYYY-MM-DD
Context
Decision
Consequences
Alternatives
Open Questions
```

## README Section Ordering (for this plugin)
1. Overview and purpose
2. Installation and setup
3. Quickstart (commands/agents examples)
4. Command reference
5. Agent reference
6. Configuration and hooks
7. Workflows and examples
8. Troubleshooting and support

## Changelog / Release Notes
- Version heading (with date)
- Added / Changed / Fixed / Deprecated / Removed / Security
- Migration or upgrade steps when needed
- Verification checklist or links to tasks/specs
