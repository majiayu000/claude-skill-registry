---
name: apply-findings
description: "Apply findings by making the suggested code changes. Applies accepted verdicts, escalates ambiguous findings to the user, and offers to note skipped genuine improvements. Use when the user asks to \"apply findings\", \"apply fixes\", \"apply suggestions\", \"apply accepted findings\", \"fix the findings\", or \"apply the review results\"."
---

# Apply Findings

Apply evaluated findings from the conversation context. Findings must have been through `/evaluate-findings` first.

## Step 1: Identify Findings

Collect all findings from the conversation context. Findings should have Verdict columns (Apply, Skip, Escalate) from `/evaluate-findings`.

If findings are unevaluated (raw output without verdicts), stop and say to run `/evaluate-findings` first.

## Step 2: Apply in File Order

Group Apply findings by file path and apply in file order to minimize context switching. For each finding:

1. Read the full function or logical block at the referenced location
2. Verify the finding still applies to the current code
3. Make the fix
4. If the finding renames an identifier, search the file for all occurrences of the old name before marking the fix complete. The cited location is often only one of several references.

If a finding references code that has changed since it was generated (e.g., by a prior fix in this same run), re-assess whether it still applies. Skip if the code has diverged.

## Step 3: Handle Escalated Findings

For findings with Escalate verdict, use `AskUserQuestion` to present the trade-offs and let the user decide. Include your technical recommendation alongside the options. When options differ on both scope/intent adherence (what the task was scoped to do) and technical merit (what's engineering-wise better), state both axes explicitly — don't silently fold scope concerns into the technical recommendation.

- **Apply** — make the change
- **Skip** — leave as-is
- **Note for later** — run the `/note-improvement` skill to capture it

## Step 4: Handle Skipped Improvements

Do not surface findings skipped as false positives or subjective preferences. For findings skipped solely because they are pre-existing, out of scope, or disproportionate, use `AskUserQuestion` to ask whether the user wants to apply the improvement now or note it for later:

- **Apply now** — make the change inline
- **Note for later** — run the `/note-improvement` skill to capture it

## Step 5: Report Results

Summarize what was applied, what was escalated, and what was skipped.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Only edit files. Do not stage, build, or test.
- If two findings conflict (suggest opposite changes to the same code), skip both and report the conflict.
