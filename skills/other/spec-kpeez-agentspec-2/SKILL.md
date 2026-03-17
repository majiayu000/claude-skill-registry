---
name: spec
description: Create feature specs for context continuity across agent sessions. Use when starting a new feature or when user runs /spec new.
---

# /spec - Feature Spec Management

## Commands

### /spec new <name>

Creates a feature spec directory with standard template files.

<steps>
<step action="slugify">lowercase name, replace spaces with hyphens → `<slug>`</step>
<step action="check-exists">error if `specs/<slug>/` exists</step>
<step action="mkdir">`specs/<slug>/`</step>
<step action="create-files">write all templates below to `specs/<slug>/`</step>
<step action="create-examples" condition="feature produces executable code">create `examples/` with TEST_LOG.md</step>
<step action="populate">fill AGENTS.md from conversation context (overview, key files, quick start)</step>
<step action="update-index">append row to `specs/INDEX` (create with header `slug\tphase\tblocked\tdesc` if missing)</step>
</steps>

<templates dir="specs/<slug>/">

<template file="AGENTS.md">
# <Title> - Agent Instructions
<!-- overview | key files | conventions | quick start -->
Read this file first when working on this feature.
</template>

<template file="CLAUDE.md">
@AGENTS.md
</template>

<template file="design.md">
# <Title> - Design
<!-- overview | key components | data flow -->
</template>

<template file="implementation.md">
# <Title> - Implementation

## Status
- **Phase**: design
- **Blocked**: no

## Done

## Next
- [ ] Define the technical approach

## Context
</template>

<template file="decisions.md">
# <Title> - Decisions
<!-- append: ## Title / Context / Decision / Alternatives / Rationale -->
</template>

<template file="future-work.md">
# <Title> - Future Work
</template>

<template file="examples/TEST_LOG.md" condition="feature produces executable code">
# <Title> - Test Log
<!-- format: ### name / Status: PASS|FAIL / Date / Description / Result -->
</template>

</templates>

### /spec status

Read and display `specs/INDEX`. If missing, scan `specs/*/implementation.md` to rebuild it.
