---
name: scout-plan-build
description: Run scout, plan, then implement; use when you want an end-to-end discovery, plan, and build flow.
---

# Scout Plan Build

## Overview

Run Scout, then Plan, then Build using the generated plan.

## Inputs

- Feature description

## Workflow

1. Run Scout to gather files and docs.
2. Run Plan to create `plans/<feature>.md`.
3. Run Build using the plan file.

## Output

- Plan file path, implementation summary, tests run
