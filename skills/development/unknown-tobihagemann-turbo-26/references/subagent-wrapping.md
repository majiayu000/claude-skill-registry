# Subagent Wrapping

If you are a subagent invoking `/peer-review`, read this before you do anything else, then follow the guardrails.

## Guardrails

1. **Wait synchronously** for `/peer-review` to return. Do not return early. Forward codex's complete output verbatim as your final result.
2. **Do not use `Monitor`.** Run codex via the Bash tool (`timeout: 3600000`, do not set `run_in_background`).
3. **Treat as peer-review failure** (not as a successful empty result):
   - Premature return before codex completes
   - `"Waiting for codex to finish"` text
   - Empty output
   - Partial output (missing dimensions in a multi-dimension fan-out)
4. **Report the failure cause specifically** (usage limit, timeout, error message) when applicable.

## Failure Reporting

`/peer-review` Step 4 specifies an `AskUserQuestion` gate for failure modes. You cannot reach the user. If codex returned partial output, emit Step 4's "Incomplete output" notice verbatim and name what is missing. If codex returned nothing or failed, emit Step 4's "No output / codex failed" notice verbatim. Do not synthesize an empty no-finding peer review.
