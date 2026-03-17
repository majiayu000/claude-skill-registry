---
name: "quality"
description: "Run quality checks, fix code quality issues, check code style, format code, or perform lint checks"
---

Runs quality checks and fixes in a single pass.

## Process

### Step 1: Slop Agent
Use Task tool with subagent_type="slop-agent" to remove AI-generated slop and fail-fast violations.

### Step 2: Structure Agent
Use Task tool with subagent_type="structure-agent" to enforce top-to-bottom code organization.

### Step 3: Lint Agent
Use Task tool with subagent_type="lint-agent" to format, auto-fix linting, and fix type errors.

Report results to user.
