---
name: apply-findings
description: "Apply findings by making the suggested code changes. Applies accepted verdicts, escalates ambiguous findings to the user, and offers to note genuine improvements for later. Use when the user asks to \"apply findings\", \"apply fixes\", \"apply suggestions\", \"apply accepted findings\", \"fix the findings\", or \"apply the review results\"."
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

For findings with Escalate verdict, use `AskUserQuestion` to let the user decide. Recommend the genuinely best option: place it first and append `(Recommended)` to its label, judging "best" on technical merit alone (the soundest engineering outcome), independent of how closely the option conforms to the task's original scope. When the choice hinges on product intent or domain knowledge you lack and merit cannot settle it, say so instead of forcing a pick. Give each option a plain-language description that carries the trade-off: its concrete effect and what it costs. When the recommended option also widens the changeset's scope, name both its merit and that scope cost so the user can weigh them.

- **Apply** — make the change
- **Skip** — leave as-is
- **Note for later** — run the `/note-improvement` skill to capture it

## Step 4: Report Results

Summarize what was applied, what was escalated, and what was skipped.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Only edit files. Do not stage, build, or test.
- If two Apply findings conflict (suggest opposite changes to the same code), surface the conflict with `AskUserQuestion`, recommend the genuinely best option on technical merit, and let the user choose, rather than applying either.
