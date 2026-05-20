---
name: scope
description: Decompose an accepted ADR into GitHub issues using the issue-creator tool.
---

# Scope

Turn an accepted ADR into a set of GitHub issues. Read AGENTS.md if not in context.

## Inputs

Path to the accepted ADR file (or paste contents). Optionally: repo override (`owner/repo`).

## Workflow

1. **Read ADR** — Extract: Context, Decision, Success Criteria, and any explicit scope boundaries.

2. **Identify work units** — Break the decision into discrete, independently deliverable chunks. Each chunk becomes one issue.

3. **Write spec file** — Create a temporary spec in issue-creator batch format:

   ```
   ## Epic: <title>
   Goal: <from ADR Decision>
   ADR: <path-to-adr>

   ### Issue: <title>
   Goal: <what this chunk delivers>
   Success Criteria:
   - <measurable criterion>
   Non-Goals: <explicit exclusions>
   ```

4. **Run issue-creator** — Execute:
   ```
   python .aide/tools/issue-creator/issue-creator.py <spec-file>
   ```

5. **Verify** — Confirm each issue was created with correct labels and GitHub Issue Type. Output issue URLs.

6. **Cleanup** — Delete the temporary spec file.

## Reference

- Issue-creator format + errors: `.aide/docs/agents/issue-creator-ref.md`
- Full tool docs: `.aide/tools/issue-creator/README.md`
