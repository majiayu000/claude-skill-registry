---
name: issue
description: Create a GitHub issue with AIDE label conventions and GitHub Issue Type.
---

# Issue

Create issues consistently with required labels so work is trackable.

## Inputs

- Title (required)
- Body (required) — use Goals / Scope / Non-Goals / Success Criteria structure; plain bullets, no checklists
- Issue Type: `feature` | `bug` | `technical-debt` | `chore` | `documentation` | `research` | `epic`
- Priority: `critical` | `high` | `medium` | `low`
- Area: `area:<name>`
- Status: `status:needs-spec` | `status:ready` | `status:in-progress`
- Optional: repo override (`owner/repo`)

## Workflow

1. Build labels list: `priority:<x>,area:<y>,status:<z>` (add `Epic` label if type is epic).

2. Create issue:
   ```
   gh issue create --title "..." --body "..." --label "priority:<x>,area:<y>,status:<z>"
   ```

3. Set GitHub Issue Type:
   ```
   python .aide/tools/set-issue-type.py --issue <num> --type <type>
   ```
   Fail if this step fails.

4. Output the created issue URL.

## Notes

- Do not use checklists (`- [ ]`) in issue bodies; use plain bullets.
- For batch issue creation, use `/scope` with the issue-creator tool instead.
