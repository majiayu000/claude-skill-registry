---
name: github-pr-lifecycle
description: "Manage GitHub pull requests via GitHub MCP: open PRs, update descriptions, request reviews, check CI status, resolve conflicts, and merge using the repo's preferred strategy."
---

# GitHub PR Lifecycle

## Required inputs
- Identify `owner`, `repo`, `base` branch, and `head` branch.
- Confirm merge strategy (merge, squash, rebase) and required checks.

## Preflight
- Confirm GitHub MCP auth can read/write PRs and request reviews.
- Determine required checks and approval rules from repo settings.
- If the PR already exists, reuse it and avoid creating duplicates.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. Create or fetch the PR and confirm the title and description match intent.
2. Ensure the PR references issues or tickets if required by repo policy.
3. Request reviewers based on CODEOWNERS or team ownership.
4. Check CI status, required checks, and review approvals.
5. Resolve conflicts or request updates if checks fail.
6. Merge when requirements are satisfied, and post a final summary.

## MCP call patterns
- Use PR list/search to locate related work.
- Use checks API to verify required status checks.
- Use review requests to route to correct owners.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a lifecycle summary: PR -> status -> blockers -> next action.

## Guardrails
- Do not merge without required approvals and checks.
- Avoid changing base or head branches without explicit instruction.
