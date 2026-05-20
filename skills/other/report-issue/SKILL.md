---
name: report-issue
description: Creates an issue file tracking a problem observed in a LearningAgent session. Used by the identify skill and can be invoked directly to report issues in real-time.
---

# Report Issue

Create an issue file documenting a problem observed in a LearningAgent session.

## Arguments

- `$0`: Path to the session log folder (e.g., `.deepwork/tmp/agent_sessions/<session_id>/<agent_id>/`)
- `$1`: Brief description of the issue observed

If `$0` is not provided or does not point to an existing directory, stop and output: "Error: session log folder path is required and must be an existing directory."

If `$1` is not provided or is empty, stop and output: "Error: issue description is required."

## Procedure

### Step 1: Determine Issue Name

From the issue description in `$1`, derive a short kebab-case name of 3-6 words maximum. Focus on the most distinctive noun and verb from the failure. Avoid filler words like "the", "a", "in", "with".

Examples:
- `wrong-retry-strategy`
- `missed-validation-edge-case`
- `hallucinated-api-endpoint`

### Step 2: Create Issue File

Create the file at `$0/<issue-name>.issue.yml` with the following content:

```yaml
status: identified
seen_at_timestamps:
  - "<current ISO 8601 timestamp>"
issue_description: |
  <Freeform text from $1 explaining what went wrong.
  Focus on the PROBLEM, not the cause.
  Be specific enough that someone can understand the failure
  without seeing the transcript.>
```

Example of a completed issue file:

```yaml
status: identified
seen_at_timestamps:
  - "2026-02-17T14:32:00Z"
issue_description: |
  The agent retried the tool call 5 times after receiving a 429 response,
  but each retry was issued immediately with no backoff delay. All 5 calls
  occurred within the same second.
```

The YAML block above is the authoritative template. See [issue_yml_format.md](../../doc/issue_yml_format.md) for additional schema details.

### Step 3: Confirm

Output a two-line confirmation:

```
Created: <path to the created issue file>
Recorded: <one-sentence summary of the issue>
```

## Guardrails

- Do NOT add an `investigation_report` field — that is added during the investigate step
- Do NOT set status to anything other than `identified`
- Do NOT modify any other files in the session log folder
- Keep the `issue_description` factual and observable — describe symptoms, not root causes
