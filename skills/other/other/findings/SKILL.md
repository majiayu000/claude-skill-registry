---
name: findings
description: Write reviewer findings to a <slug>.findings.md file for any scoped review target.
---

# Findings

Write reviewer findings for any scoped target using a two-file message bus. This command applies to a file, ADR, doc set, PR context, diff, uncommitted workspace, or another named review scope.

## Protocol

- `<slug>.findings.md` — owned by the **reviewer**; primary output of this command; deleted on acceptance
- `<slug>.response.md` — owned by the **author**; deleted on acceptance

## Inputs

- Review target or scope
- Slug for the exchange files
- Optional existing `<slug>.response.md` when iterating

## Reviewer workflow

1. Read the target under review. If `<slug>.response.md` already exists, read it before revising findings.
2. Write findings to `<slug>.findings.md`:
   ```
   # Review: <target name>
   ## Findings
   ### Critical
   - [path:line or section] Issue. Suggested fix.
   ### Major / Minor
   - ...
   ## Decision: Request Changes | Approve
   ```
3. Tell the author: "findings written to `<slug>.findings.md`."

Do not stop at chat-only review output. The findings file is the contract.

## Author workflow

1. Read `<slug>.findings.md`.
2. For each finding: fix, defer (with reason), or reject (with reason).
3. Write response to `<slug>.response.md`:
   ```
   # Response: <target name>
   ## Responses
   - [Finding ref] Fixed | Deferred: <reason> | Rejected: <reason>
   ## Target status: Revised | Accepted as-is
   ```
4. Tell the reviewer: "response written to `<slug>.response.md`."

## Closing the loop

Reviewer reads `<slug>.response.md`. If satisfied: both files deleted, target accepted. If not: iterate.

## Notes

- Use a stable slug for the review scope: `pr-524`, `workspace-uncommitted`, `movement-system`, `2026-03-01-network-flow-logistics-system`.
- Use `<issue-number>-<slug>` naming when the review is tied to a GitHub issue.
- This protocol is relay-agnostic; future tooling can automate the file exchange.
