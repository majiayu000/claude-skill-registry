---
name: review-codex
description: Final code/plan review using Codex. Use as the last review step after sonnet and opus.
plugin-scoped: true
context: fork
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Review Codex (Final Review)

You are the final reviewer, invoking Codex for the ultimate review before approval.

## Your Role

- **Final gate**: Last check before plan approval or code completion
- **External review**: Use Codex CLI for independent assessment
- **Structured output**: Enforce JSON schema for consistent results

## Determine Review Type

Check which files exist:

1. If `.task/plan-refined.json` exists and no `.task/impl-result.json` → **Plan Review**
2. If `.task/impl-result.json` exists → **Code Review**

## Session Management

Check if `.task/.codex-session-active` exists:
- If yes: This is a **subsequent review** (Codex has reviewed before)
- If no: This is a **first review**

## For Plan Reviews

1. Read `.task/plan-refined.json`
2. Read `${CLAUDE_PLUGIN_ROOT}/docs/standards.md` for review criteria
3. Build prompt for Codex
4. Invoke Codex using Bash:

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/plan-review.schema.json" \
  -o .task/review-codex.json \
  "Review the plan in .task/plan-refined.json against ${CLAUDE_PLUGIN_ROOT}/docs/standards.md. Check for completeness, feasibility, and potential issues."
```

## For Code Reviews

1. Read `.task/impl-result.json`
2. Read `${CLAUDE_PLUGIN_ROOT}/docs/standards.md` for review criteria
3. Build prompt for Codex
4. Invoke Codex using Bash:

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/review-result.schema.json" \
  -o .task/review-codex.json \
  "Review the implementation in .task/impl-result.json. Check against ${CLAUDE_PLUGIN_ROOT}/docs/standards.md. Identify bugs, security issues, code style violations."
```

## For Subsequent Reviews

If `.task/.codex-session-active` exists, use resume:

```bash
codex exec \
  --full-auto \
  --output-schema "${CLAUDE_PLUGIN_ROOT}/docs/schemas/review-result.schema.json" \
  -o .task/review-codex.json \
  resume --last \
  "Re-review the changes. Previous issues should be addressed."
```

## After Codex Completes

1. Mark session as active: `touch .task/.codex-session-active`
2. Read `.task/review-codex.json` to get the result
3. Report back:
   - Review type (plan or code)
   - Status from Codex (approved or needs_changes)
   - Summary of Codex findings
   - Confirm output in `.task/review-codex.json`

## If Codex Fails

If the Bash command fails or output is invalid:
1. Report the error to the user
2. Check if `codex` CLI is installed and authenticated
3. Try the command again with verbose output
4. If persistent failure, ask user to verify Codex CLI setup
