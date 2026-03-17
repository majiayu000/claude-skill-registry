---
description: Import external issues from GitHub, Jira, or Azure DevOps and create SpecWeave increments with platform suffixes (G/J/A). Supports filtering and duplicate prevention. Use when saying "import issues", "pull from github", "grab jira issues", or "import from ado".
argument-hint: "[platform] [filter-query]"
---

# External Issue Import

Import issues from external trackers (GitHub, JIRA, Azure DevOps) and create SpecWeave increments with platform-specific suffixes: **G** (GitHub), **J** (JIRA), **A** (ADO).

---

## Workflow

### STEP 1: Load Configuration

1. Read `.specweave/config.json` — check `sync` section
2. Identify which platforms are configured (`sync.github`, `sync.jira`, `sync.ado`)
3. If NO platforms configured:
   - Tell user: "No external tools configured. Run `/sw:sync-setup` to connect GitHub, JIRA, or ADO."
   - **STOP**

### STEP 2: Platform Selection

1. If user specified a platform in the command argument (e.g., `/sw:import github`), use that
2. If multiple platforms configured and none specified, ask user which to import from:
   - Use AskUserQuestion with configured platforms as options
3. Validate the selected platform is configured and has credentials

### STEP 3: Filter Configuration

Ask user for optional filters (or parse from arguments):

- **Status**: open (default), closed, all
- **Labels**: comma-separated label filter
- **Date range**: last N months (default: 3)
- **Milestone/Epic**: filter by milestone or epic
- **Search query**: text search in title/description
- **Max items**: limit results (default: 20)

If user provides no filters, use defaults: open issues, last 3 months, max 20.

### STEP 4: Fetch External Issues

1. Read credentials from `.env` or environment:
   - GitHub: `GITHUB_TOKEN` or `gh auth status`
   - JIRA: `JIRA_EMAIL` + `JIRA_API_TOKEN` + domain from config
   - ADO: `ADO_PAT` + org/project from config

2. Use the platform's API to fetch issues matching filters:
   - **GitHub**: `gh api repos/{owner}/{repo}/issues` with query params
   - **JIRA**: JIRA REST API v3 with JQL query
   - **ADO**: ADO REST API with WIQL query

3. Parse results into a display-friendly list

### STEP 5: Display and Select

Present issues in a numbered table:

```
# | ID        | Title                          | Status | Priority | Labels
--|-----------|--------------------------------|--------|----------|--------
1 | #123      | Fix login redirect loop        | open   | P1       | bug
2 | #456      | Add dark mode support          | open   | P2       | feature
3 | #789      | Update API documentation       | open   | P3       | docs
```

Ask user to select which issues to import:
- Single: "1"
- Multiple: "1,3,5"
- All: "all"
- Range: "1-5"

### STEP 6: Duplicate Detection

For each selected issue, check if already imported:

1. Generate the canonical `external_ref` string:
   - GitHub: `github#{owner}/{repo}#{issue_number}`
   - JIRA: `jira#{project_key}#{issue_key}`
   - ADO: `ado#{org}/{project}#{work_item_id}`

2. Scan ALL `.specweave/increments/**/metadata.json` files for matching `external_ref`
   - Check: active, _archive, _abandoned, _paused directories

3. For duplicates found:
   - Report: "Skipping #{issue_id} — already imported as {increment_id}"
   - Remove from selection

### STEP 7: Create Increments

For each non-duplicate selected issue:

1. **Generate increment ID** with platform suffix:
   - GitHub issue #123 "fix-login-bug" → `0271G-fix-login-bug`
   - JIRA PROJ-456 "payment-flow" → `0272J-payment-flow`
   - ADO #789 "ci-pipeline" → `0273A-ci-pipeline`

2. **Create increment files** via `createIncrementTemplates()` with `externalSource`:
   - `metadata.json` — includes `external_ref`, `origin: "external"`, `source_platform`
   - `spec.md` — pre-filled with issue title, description, and acceptance criteria
   - `plan.md` — template (to be completed via architect skill)
   - `tasks.md` — derived from acceptance criteria if available, template otherwise

3. **Map priority**: Use external priority if available, default to P2
4. **Map type**: bug → bug, feature/epic/story → feature

### STEP 8: Post-Import Summary

Display results:

```
Import Complete
===============

Created:
  - 0271G-fix-login-bug (from GitHub #123)
  - 0273A-ci-pipeline (from ADO #789)

Skipped (duplicates):
  - GitHub #456 — already imported as 0200G-dark-mode

Errors: none

Next steps:
  - /sw:do 0271G  — Start working on first import
  - /sw:auto 0271G — Run autonomously
```

---

## Platform Suffix Reference

| Platform | Suffix | Example |
|----------|--------|---------|
| GitHub   | G      | `0271G-fix-login-bug` |
| JIRA     | J      | `0272J-payment-flow` |
| ADO      | A      | `0273A-ci-pipeline` |
| Legacy   | E      | `0111E-old-import` (backwards compat) |

---

## Edge Cases

### No issues found
Tell user "No matching issues found. Try adjusting filters." Suggest broader search.

### External tool API error
Report the error clearly. Suggest checking credentials: "Run `/sw:sync-setup` to verify credentials."

### Issue has no description
Create spec with title only and mark as needs-review.

### Issue has no acceptance criteria
Create template-style tasks.md with placeholder tasks.

### Rate limiting
Report rate limit and suggest waiting or reducing the import batch size.

### Umbrella / multi-repo project
If in an umbrella project with multiple repos under `repositories/`, ask which repo's `.specweave/` should receive the increment.

---

## Configuration Reference

Required in `.specweave/config.json`:

```json
{
  "sync": {
    "enabled": true,
    "github": { "enabled": true, "owner": "...", "repo": "..." },
    "jira": { "enabled": true, "domain": "...", "projectKey": "..." },
    "ado": { "enabled": true, "organization": "...", "project": "..." }
  }
}
```

Credentials in `.env` (never committed):
```
GITHUB_TOKEN=ghp_...
JIRA_EMAIL=user@example.com
JIRA_API_TOKEN=...
ADO_PAT=...
```
