---
description: Expert-guided brainstorming and ideation session. Phase 1 Analysis
user-invocable: true
disable-model-invocation: true
---

# Brainstorm Workflow

**Goal:** Expert guided facilitation through brainstorming techniques with a
final report.

**Agent:** Analyst (Mary) **Phase:** 1 - Analysis

---

## Workflow Architecture

Step-file architecture with branching paths based on technique selection.

## Initialization

Check for project config at `bmad/config.yaml`. Load brainstorming methods from
`./brain-methods.csv`.

## Execution

Read and execute: `./steps/step-01-session-setup.md`
