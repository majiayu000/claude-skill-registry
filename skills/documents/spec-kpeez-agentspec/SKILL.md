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
<step action="populate">fill AGENTS.md from conversation context:
  - Overview: what the user asked for
  - Key Files: initial guesses based on feature scope
  - Quick Start: first implementation steps
  - Conventions: placeholder if unknown</step>
</steps>

<templates dir="specs/<slug>/">

<template file="AGENTS.md">
# <Title> - Agent Instructions

Read this file first when working on this feature.

## Overview
<!-- 1-2 sentences: what we're building and why -->

## Key Files
<!-- update as you work. format: `path/to/file.ts` - purpose -->

## Conventions
<!-- feature-specific patterns, constraints, or gotchas -->

## Quick Start
<!-- for a new agent: what to read first, what to do first -->
</template>

<template file="design.md">
# <Title> - Design

## Overview

(brief technical approach - fill in during design phase)

## Key Components

(to be defined)

## Data Flow

(to be defined)
</template>

<template file="ledger.md">
# <Title> - Ledger

## Status

- **Phase**: design
- **Blocked**: no

## Done

(nothing yet)

## Next

- [ ] Define the technical approach

## Context

(gotchas, non-obvious things discovered)
</template>

<template file="decisions.md">
# <Title> - Decisions

Log non-obvious technical choices here.

---

(No decisions recorded yet)
</template>

<template file="future-work.md">
# <Title> - Future Work

Ideas and improvements deferred for later.

(Nothing yet)
</template>

<template file="examples/TEST_LOG.md" condition="feature produces executable code">
# <Title> - Test Log

Execution results for verification examples.

---

(No examples run yet)
</template>

</templates>

<example-log-format>
### example_name.py
**Status:** PASS | FAIL
**Date:** YYYY-MM-DD
**Description:** What this example verifies.
**Result:** What happened when run.
---
</example-log-format>
