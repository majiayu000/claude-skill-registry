---
name: followup-cleanup
description: Clean a review plan for handoff to a coding agent — prune false positives, add stale-data warnings
user-invocable: true
disable-model-invocation: true
---
Prepare the current plan for handoff to a coding agent. Two steps:

## Step 1 — Prune false positives

Review the plan and remove items that were validated as false positives, non-issues, or by-design behavior. These confuse the coding agent and waste tokens on work that shouldn't be done.

Keep an item only if it needs context for a surviving item (e.g., "we investigated X and found it's fine, but the adjacent code at Y does need fixing" — keep X as context for Y).

Remove everything else that was ruled out during validation. The coding agent should see a clean, actionable list — not the full investigation trail.

## Step 2 — Add stale-data warnings

Other agents may have modified this repo and committed changes between when the review was done and when the coding agent runs. The plan references specific files and line numbers that may have shifted.

Add an explicit warning at the top of the plan:

> **Before implementing any change:** Validate that the issue still exists at the referenced location. Line numbers may have shifted due to other commits. Read the current code at each location before modifying it. Do not blindly apply fixes to line numbers from this plan.

This is especially important for plans produced by review skills that use explore agents — the explore agents read code at a point in time, and the code may have changed since.
