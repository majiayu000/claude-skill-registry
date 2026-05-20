---
name: dogfood
description: Systematically explore and test a web application to find bugs, UX issues, and other problems. Use when asked to "dogfood", "QA", "exploratory test", "find issues", "bug hunt", "test this app/site/platform", or review the quality of a web application. Produces a structured report with full reproduction evidence -- screenshots and detailed repro steps for every issue -- so findings can be handed directly to the responsible teams.
---

# Dogfood

Systematically explore a web application, find issues, and produce a report with full reproduction evidence for every finding.

Use the native machine to interact with the browser -- take screenshots, navigate URLs, check console errors, etc. Figure out the best tools available on the system (screencapture, AppleScript, etc.) and use them as needed.

## Setup

Only the **Target URL** is required. Everything else has sensible defaults -- use them unless the user explicitly provides an override.

| Parameter | Default | Example override |
|-----------|---------|-----------------|
| **Target URL** | _(required)_ | `vercel.com`, `http://localhost:3000` |
| **Output directory** | `./dogfood-output/` | `Output directory: /tmp/qa` |
| **Scope** | Full app | `Focus on the billing page` |
| **Authentication** | None | `Sign in to user@example.com` |

If the user says something like "dogfood vercel.com", start immediately with defaults. Do not ask clarifying questions unless authentication is mentioned but credentials are missing.

## Workflow

```
1. Initialize    Set up output dirs, open browser, report file
2. Authenticate  Sign in if needed (ask user for help with OTP/2FA)
3. Orient        Take initial screenshot, map app structure
4. Explore       Systematically visit pages and test features
5. Document      Screenshot each issue as found
6. Wrap up       Update summary counts
```

### 1. Initialize

Create the output directory structure and copy the report template:

```bash
mkdir -p {OUTPUT_DIR}/screenshots
cp {SKILL_DIR}/templates/dogfood-report-template.md {OUTPUT_DIR}/report.md
```

Open the target URL in the browser and fill in the report header fields.

### 2. Authenticate

If the app requires login, ask the user to sign in manually in the browser. Wait for them to confirm they're logged in before proceeding.

For complex auth flows (OTP, SSO, 2FA): ask the user to complete authentication and confirm when ready.

### 3. Orient

Take an initial screenshot to understand the app structure. Identify the main navigation elements and map out the sections to visit.

### 4. Explore

Read [references/issue-taxonomy.md](references/issue-taxonomy.md) for the full list of what to look for and the exploration checklist.

**Strategy -- work through the app systematically:**

- Start from the main navigation. Visit each top-level section.
- Within each section, test interactive elements: click buttons, fill forms, open dropdowns/modals.
- Check edge cases: empty states, error handling, boundary inputs.
- Try realistic end-to-end workflows (create, edit, delete flows).
- Check the browser console for errors periodically.

**At each page:** navigate there, take a screenshot, check console for errors. Use your judgment on how deep to go -- spend more time on core features and less on peripheral pages.

### 5. Document Issues (Repro-First)

Steps 4 and 5 happen together -- explore and document in a single pass. When you find an issue, stop exploring and document it immediately before moving on.

Every issue must be reproducible. When you find something wrong, do not just note it -- prove it with evidence.

**Choose the right level of evidence for the issue:**

#### Interactive / behavioral issues (functional, ux, console errors on action)

These require user interaction to reproduce. Capture before/during/after screenshots. Ask the user to perform actions you can't do programmatically. Write numbered repro steps in the report, each referencing its screenshot.

#### Static / visible-on-load issues (typos, placeholder text, clipped text, misalignment, console errors on load)

These are visible without interaction -- a single screenshot is sufficient. Write a brief description and reference the screenshot in the report.

**For all issues:**

1. **Append to the report immediately.** Do not batch issues for later. Write each one as you find it so nothing is lost if the session is interrupted.
2. **Increment the issue counter** (ISSUE-001, ISSUE-002, ...).

### 6. Wrap Up

Aim to find **5-10 well-documented issues**, then wrap up. Depth of evidence matters more than total count -- 5 issues with full repro beats 20 with vague descriptions.

After exploring:

1. Re-read the report and update the summary severity counts so they match the actual issues. Every `### ISSUE-` block must be reflected in the totals.
2. Tell the user the report is ready and summarize findings: total issues, breakdown by severity, and the most critical items.

## Guidance

- **Repro is everything.** Every issue needs proof -- but match the evidence to the issue. Interactive bugs need step-by-step screenshots. Static bugs only need a single screenshot.
- **Verify reproducibility before collecting evidence.** Verify the issue is reproducible with at least one retry before documenting.
- **Collaborate with the user for interactions.** Ask the user to perform clicks, form fills, and other interactions when needed. You handle the screenshots and documentation.
- **Write repro steps that map to screenshots.** Each numbered step in the report should reference its corresponding screenshot.
- **Be thorough but use judgment.** Explore like a real user would. If something feels off, investigate.
- **Write findings incrementally.** Append each issue as you discover it. Never batch all issues for the end.
- **Never delete output files.** Do not `rm` screenshots or the report mid-session. Work forward, not backward.
- **Never read the target app's source code.** You are testing as a user, not auditing code.
- **Check the console.** Many issues are invisible in the UI but show up as JS errors or failed requests.
- **Test like a user, not a robot.** Try common workflows end-to-end. Enter realistic data.

## References

| Reference | When to Read |
|-----------|--------------|
| [references/issue-taxonomy.md](references/issue-taxonomy.md) | Start of session -- calibrate what to look for, severity levels, exploration checklist |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/dogfood-report-template.md](templates/dogfood-report-template.md) | Copy into output directory as the report file |
