---
name: review
description: Cross-cutting artifact review using a two-file filesystem protocol. Works across windows without copy-paste.
---

# Review

Review any artifact (ADR, doc, code design) using a two-file message bus. Each context writes only its own file.

## Protocol

- `<slug>.findings.md` — owned by the **reviewer**; deleted on acceptance
- `<slug>.response.md` — owned by the **author**; deleted on acceptance

## Reviewer workflow

1. Read the artifact.
2. Write findings to `<slug>.findings.md`:
   ```
   # Review: <artifact name>
   ## Findings
   ### Critical
   - [path:line or section] Issue. Suggested fix.
   ### Major / Minor
   - ...
   ## Decision: Request Changes | Approve
   ```
3. Tell the author: "findings written to `<slug>.findings.md`."

## Author workflow

1. Read `<slug>.findings.md`.
2. For each finding: fix, defer (with reason), or reject (with reason).
3. Write response to `<slug>.response.md`:
   ```
   # Response: <artifact name>
   ## Responses
   - [Finding ref] Fixed | Deferred: <reason> | Rejected: <reason>
   ## Artifact status: Revised | Accepted as-is
   ```
4. Tell the reviewer: "response written to `<slug>.response.md`."

## Closing the loop

Reviewer reads `<slug>.response.md`. If satisfied: both files deleted, artifact accepted. If not: iterate.

## Notes

- Use `<issue-number>-<slug>` naming for issue-linked reviews (e.g., `540-cadence-adr`).
- This protocol is relay-agnostic — future tooling can automate the file exchange.
