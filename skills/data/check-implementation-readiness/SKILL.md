---
description:
  Validate PRD, UX, Architecture, and Epics alignment before implementation.
  Phase 3 Solutioning
user-invocable: true
disable-model-invocation: true
---

# Implementation Readiness Workflow

**Goal:** Ensure PRD, UX, Architecture, and Epics/Stories are aligned and ready
for implementation.

**Agent:** Architect (Winston) **Phase:** 3 - Solutioning

---

## Workflow Architecture

Step-file architecture with 6 validation steps.

## Initialization

Check for project config at `bmad/config.yaml`. Requires all planning artifacts.

## Execution

Read and execute: `./steps/step-01-document-discovery.md`
