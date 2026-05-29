---
name: verify-ui
description: Build assets, run server, and get visual approval before committing observable changes.
---

## When to use
- Before committing any changes that affect observable UI behavior
- This includes: templates, components, styles, handlers, models surfaced in UI, migrations
- When CLAUDE.md or `/commit` skill directs you here

## Prerequisites
- Changes to verify should already be implemented (not staged/committed yet)

## Workflow

1) **Build static assets**:
   - Run `templ generate` to regenerate templ files
   - Run `make css` to rebuild Tailwind CSS
   - Report any errors and stop if build fails

2) **Database migrations** (if applicable):
   - Check for pending migrations: `make migrate-status`
   - If pending, ask user before running: `make migrate`
   - Skip if no database changes

3) **Start server**:
   - Run `go run ./cmd/tfo-webapp` in background
   - Wait for server to be ready (check output for listening message)
   - Report the URL (typically http://localhost:8080)

4) **Request visual inspection**:
   - Tell user: "Server running at http://localhost:8080 - please verify the UI"
   - Use AskUserQuestion to get approval:
     - "Does the UI look correct?"
     - Options: "Yes, looks good" / "No, needs changes"

5) **Handle response**:
   - If approved: Stop server, report ready to commit
   - If not approved: Stop server, ask what needs to change, do NOT proceed to commit

6) **Cleanup**:
   - Always stop the background server when done

## Output
- Commands run and their outcomes
- Server URL for inspection
- User's verification decision
- Clear next step (proceed to commit or fix issues)
