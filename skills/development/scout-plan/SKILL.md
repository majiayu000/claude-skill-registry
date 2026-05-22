---
name: scout-plan
description: Run a codebase scout and then produce an implementation plan; use when you want discovery followed by planning.
---

# Scout Plan

## Overview

Run Scout, then Plan, passing the file list and docs into planning.

## Inputs

- Feature description
- Scout scale (optional)

## Workflow

1. Run Scout with the chosen scale and capture the ranked file list and any docs.
2. Run Plan with the feature description and include the scout outputs as context.
3. Save the plan in `plans/`.

## Output

- Scout file list and plan file path
