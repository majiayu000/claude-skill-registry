---
name: "feature-new"
description: "Start new feature with full planning"
argument-hint: "[feature-description]"
---

Creates a new feature branch using git clone for isolated development with full planning.

## Feature description from user input
"$ARGUMENTS"

### Feature Description Validation
  - If empty or missing: "Error: Feature description is required. Please provide a detailed description for planning."

## Process

### Step 1: Create Clone
Run `/create-clone $ARGUMENTS`.

### Step 2: Run Feature Loop
Run `/feature-loop-scheme` to execute the full development workflow.
