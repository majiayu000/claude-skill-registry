---
name: create-feature-flag-plan
description: Plan progressive delivery with feature flag lifecycle management when the user asks to create a feature flag plan, rollout strategy, or progressive delivery plan
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[feature name to create a flag plan for]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: feature-flags, rollout, delivery
---

# Create Feature Flag Plan

## Overview

Generate a feature flag lifecycle plan for progressive delivery. Covers flag naming, rollout stages from internal to beta to GA, kill switch behavior, monitoring requirements at each stage, and a cleanup plan with a deadline and owner for flag removal. Prevents flag debt and ensures safe, observable rollouts.

## Workflow

1. **Read engineering context** -- Scan `.chalk/docs/engineering/` for existing feature flag conventions, architecture docs, and monitoring infrastructure. Check `.chalk/docs/product/` for the PRD or pitch that describes the feature being flagged.

2. **Parse the feature** -- Extract from `$ARGUMENTS` the feature to create a flag plan for. If unspecified, ask the user to name the feature.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/engineering/` to find the highest numbered file. The next number is `highest + 1`.

4. **Define the flag** -- Name the flag following conventions found in engineering docs, or default to `enable_<feature_slug>`. Specify the flag type (boolean, percentage, user-segment) and default value (always off).

5. **Plan rollout stages**:
   - **Internal** (team only): Who tests, what to validate, success criteria to advance
   - **Beta** (selected users/accounts): Selection criteria, opt-in mechanism, feedback channel, success criteria to advance
   - **GA** (all users): Ramp schedule (e.g., 10% -> 25% -> 50% -> 100%), monitoring checkpoints at each ramp

6. **Define kill switch behavior** -- What happens when the flag is turned off mid-rollout: data handling, in-flight operations, user communication, rollback procedure.

7. **Specify monitoring at each stage** -- What metrics, alerts, and dashboards to watch. Define thresholds that trigger a rollback (e.g., error rate > 1%, p95 latency > 500ms).

8. **Set cleanup plan** -- Define: cleanup deadline (date by which the flag must be removed), owner responsible for removal, what "removal" means (delete flag checks, remove old code path, update tests).

9. **Write the file** -- Save to `.chalk/docs/engineering/<n>_feature_flag_plan_<feature-slug>.md`.

10. **Confirm** -- Share the file path and highlight the rollback triggers and cleanup deadline.

## Output

- **File**: `.chalk/docs/engineering/<n>_feature_flag_plan_<feature-slug>.md`
- **Format**: Plain markdown with flag definition, rollout stages table, kill switch section, and cleanup plan
- **First line**: `# Feature Flag Plan: <Feature Name>`

## Anti-patterns

- **No cleanup deadline** -- Flags without removal dates become permanent. Every flag plan must have a cleanup date and an owner. Treat it as tech debt with a due date.
- **Binary rollout** -- Going from 0% to 100% with no intermediate stages defeats the purpose of progressive delivery. Always define at least internal, beta, and GA stages.
- **No rollback triggers** -- "We will monitor" is not a plan. Define specific metric thresholds that trigger an automatic or manual rollback.
- **Flag naming chaos** -- Inconsistent naming (camelCase, snake_case, random prefixes) makes flags impossible to audit. Follow or establish a naming convention.
- **Missing kill switch behavior** -- What happens to in-flight requests when you flip the flag off? If you have not answered this, the rollback plan is incomplete.
