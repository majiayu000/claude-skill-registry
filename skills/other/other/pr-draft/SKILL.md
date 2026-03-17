---
name: pr-draft
description: Create a draft PR with a validated body template and issue linkage.
---

# PR Draft

Create a draft PR using a consistent template. Validate body locally before opening.

## Inputs

Base branch (default `main`), head branch (default current), PR title, issue number, summary bullets (1-4), implementation checklist items, validation checklist items.

## Workflow

1. **Confirm branch state** — Verify not on `main`. Verify at least one commit exists. Push if needed:
   ```
   git push -u origin <branch>
   ```

2. **Build PR body** — Write a temporary markdown file:
   ```markdown
   Fixes #<number>

   ## Summary
   - <bullet>

   ## Implementation Plan
   - [ ] <step>

   ## Validation
   - [ ] <criterion>
   ```

3. **Validate body** — Run:
   ```
   powershell -ExecutionPolicy Bypass -File tools/validate_pr_body.ps1 -Body (Get-Content -Raw <tmpfile>)
   ```
   Fix and re-run until green.

4. **Create draft PR** — Run:
   ```
   gh pr create --draft --base <base> --head <head> --title "<title>" --body-file <tmpfile>
   ```

5. **Verify & cleanup** — Run `gh pr view --json number,url,body`. Confirm formatting persisted. Delete the temporary body file.

## Output

PR URL, linked issue number, validation result.
