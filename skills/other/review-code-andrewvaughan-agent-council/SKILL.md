---
name: review-code
description: Run a comprehensive multi-perspective code review on current changes. Activates the Review Council (security, quality, documentation, domain review) and runs automated security scanning. Use before creating a pull request or when you want a thorough review of your work.
---

# Code Review Workflow

Run a comprehensive, multi-perspective code review on the current branch changes. This skill activates the Review Council and integrates automated security scanning to catch issues before they reach a pull request.

> [!CAUTION]
> **Scope boundary**: This skill reviews code and commits fixes. It does **NOT** create pull requests, push to remote, or merge anything. When the review is complete, **stop** and suggest the user run `/submit-pr` next. Do not proceed to PR creation — that is `/submit-pr`'s job.

> [!WARNING]
> **Checkpoint protocol.** When this workflow reaches a `### CHECKPOINT`, you **must** actively prompt the user for a decision — do not simply present information and continue. Use your agent's interactive prompting mechanism (e.g., `AskUserQuestion` in Claude Code) to require an explicit response before proceeding. This prevents queued or in-flight messages from being misinterpreted as approval. If your agent lacks interactive prompting, output the checkpoint content and **stop all work** until the user explicitly responds.

## Step 1: Analyze Current Changes

Identify all changes on the current branch:

1. Run `git diff origin/main...HEAD` to see all changes relative to main
2. Run `git diff` and `git diff --cached` to catch any uncommitted work
3. Run `git status` to see modified, added, and deleted files

Categorize changed files by layer based on your project's directory structure:

- **Frontend**: UI components, pages, styles, client-side logic
- **Backend**: API routes, services, business logic, server-side code
- **Database**: Schema files, migrations, seed data
- **Configuration**: Config files, CI/CD, container definitions, environment files
- **Documentation**: Markdown files, docs directories
- **Tests**: Test files (`.test.*`, `.spec.*`)

Present a summary of changed files by category to the user.

## Step 2: Run Formatting and Lint Checks

Run your project's formatting and lint commands before the council review to catch mechanical issues early. Common examples:

```
# Adapt to your project's toolchain
format:check    # Prettier, Black, gofmt, etc.
lint            # ESLint, Ruff, golangci-lint, etc.
```

If formatting checks fail, fix them immediately by running the auto-formatter on the reported files and stage the changes. Do not include formatting issues in the council review — just fix them.

## Step 3: Run Automated Security Scanning

Perform static application security testing (SAST) on all changed files. Scan for:

<details>
<summary>SAST Scanning Checklist</summary>

- Are all database queries parameterized? (SQL/NoSQL injection)
- Are user inputs sanitized before rendering? (XSS — reflected, stored, DOM-based)
- Are state-changing endpoints protected against CSRF?
- Are there hardcoded secrets, API keys, passwords, or connection strings?
- Are authentication flows following secure patterns? (no auth bypass paths)
- Are error messages leaking internal details? (stack traces, DB structure)
- Are dependencies free of known CVEs?
- Are file uploads validated and restricted?
- Are authorization checks present on all protected endpoints?

</details>

If backend files are changed, also perform a hardening review:

- Is input validation comprehensive on all user-facing inputs?
- Are authentication and authorization checks present and correct?
- Are error responses safe? (no internal details leaked)
- Are secrets managed securely? (environment variables, vaults — not hardcoded)
- Are security headers configured? (CSP, HSTS, X-Frame-Options)
- Are rate limits configured on public endpoints?

Collect all findings with severity levels (Critical, High, Medium, Low, Info).

> **Claude Code optimization**: If the `/security-scanning:security-sast` and `/security-scanning:security-hardening` skills are available, use them for enhanced automated scanning. Otherwise, follow the manual checklists above.

## Step 4: Run Accessibility Audit (if frontend changes)

If any frontend files (UI components, CSS, HTML templates) are in the changeset, check WCAG compliance on modified components:

<details>
<summary>Accessibility Checklist</summary>

- Do text and interactive elements meet color contrast ratios? (4.5:1 for normal text, 3:1 for large text)
- Can all interactive elements be reached and operated via keyboard alone?
- Are ARIA attributes used correctly? (roles, labels, live regions)
- Is focus managed properly during dynamic content changes? (modals, route transitions)
- Is semantic HTML used? (`<button>` not `<div onClick>`, `<nav>`, `<main>`, `<article>`)
- Are images and icons given accessible names? (`alt` text, `aria-label`)
- Are form inputs associated with labels?
- Does the page make sense when read linearly by a screen reader?

</details>

> **Claude Code optimization**: If the `/ui-design:accessibility-audit` skill is available, use it for enhanced automated WCAG compliance checking. Otherwise, follow the manual checklist above.

## Step 5: Activate the Review Council

Read the Review Council template from the skill's `councils/review-council.md` and conduct the full council review. For each council member, read their agent definition from the skill's `agents/` directory and use the complexity tier specified to calibrate review depth.

### Security Engineer (Lead)

- Review all SAST findings from Step 3
- Check for OWASP Top 10 vulnerabilities in the changed code
- Validate input sanitization on any new endpoints or forms
- Check secrets management (no hardcoded credentials, API keys, tokens)
- Verify authentication and authorization logic
- **Vote**: Approve / Concern / Block
- **Findings**: List each issue with severity and file location
- **Recommendations**: Specific fixes for each finding

### QA Lead

- Assess test coverage for changed files
- Check if new functionality has corresponding tests
- Identify untested edge cases and boundary conditions
- Verify error scenarios are tested
- Check if test coverage meets the >80% target
- **Vote**: Approve / Concern / Block
- **Findings**: Missing tests, coverage gaps, untested scenarios
- **Recommendations**: Specific tests to add

### DevX Engineer

- Check if documentation is updated for user-facing changes
- Review code readability and clarity of complex logic
- Verify README/docs reflect any new features or changes
- Check that public APIs have proper documentation comments
- **Vote**: Approve / Concern / Block
- **Findings**: Documentation gaps, unclear code sections
- **Recommendations**: Documentation and clarity improvements

### Domain Specialist

Select the appropriate specialist based on changed files:

- **Frontend Specialist** if frontend files changed
- **Backend Specialist** if backend files changed
- **Both** if changes span frontend and backend

Review domain-specific best practices:

- Component patterns, state management, rendering performance (frontend)
- Framework patterns, service architecture, API design (backend)
- Schema design, query optimization, migration safety (database)
- **Vote**: Approve / Concern / Block
- **Findings**: Pattern violations, anti-patterns, performance concerns
- **Recommendations**: Specific improvements

## Step 6: Present Consolidated Review Report

Present the full review report organized by severity:

### Critical / Blocking Issues

Issues that must be fixed before merge (any Block vote or Critical SAST finding).

### High Priority Issues

Issues strongly recommended to fix (High SAST findings, Concern votes with security implications).

### Medium Priority Issues

Issues worth fixing but not blocking (Medium SAST findings, code quality concerns).

### Low Priority / Suggestions

Nice-to-have improvements (Low findings, style suggestions, minor documentation gaps).

### Review Decision Summary

- **Overall Status**: Approved / Needs Changes / Blocked
- **Council Votes**: Summary of each member's vote
- **Action Items**: Prioritized list of what to fix

### CHECKPOINT: Present all findings to the user. Ask which items they want to address now. Wait for instructions before proceeding.

## Step 7: Apply Fixes

For each item the user approves for fixing:

1. Apply the fix
2. Re-run the relevant check (lint, test, type-check, or security scan) to verify the fix
3. Stage the changes

If the user asks to skip certain findings, note them as deferred items for Step 9.

### CHECKPOINT: Present the applied fixes to the user. Confirm all changes look correct before committing.

## Step 8: Commit

If the user approves:

1. Stage all changes
2. Commit with an appropriate conventional commit message (e.g., `fix(security): address SAST findings` or `refactor: address code review feedback`)

## Step 9: Track Deferred Work

If any review findings were deferred (not fixed in this cycle), document them so they don't get lost.

### Check for Deferred Items

Review the following sources for deferred work:

1. **Skipped findings**: Items the user chose not to address from the review report
2. **Low priority suggestions**: Items categorized as Low/Info that weren't fixed
3. **Council recommendations**: Improvements suggested by council members that are out of scope for this PR

### Document Deferred Work

For each deferred item, create a tracking issue in your project's issue tracker with the finding description, context on why it was deferred, and what needs to happen.

> [!TIP]
> Not every review generates deferred work. If all findings were addressed or accepted, skip this step entirely. Don't manufacture follow-up issues just to have them.

## Step 10: Hand Off — STOP Here

> [!CAUTION]
> **This skill's work is done.** Do NOT proceed to create a pull request, push to remote, or merge anything. Those are separate skills with their own workflows and checkpoints.

Suggest the next step — then **stop**:

- If ready for PR: "Run `/submit-pr` to create a pull request"
- If more work needed: "Continue implementation, then run `/review-code` again when ready"

**Do not push the branch, create a PR, or invoke `/submit-pr` from within this skill.**
