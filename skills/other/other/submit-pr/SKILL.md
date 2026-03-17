---
name: submit-pr
description: Create a pull request for the current feature branch. Generates a PR description from commits, runs pre-submission checks, and optionally activates the Deployment Council for production-impacting changes. Use when your feature branch is ready to merge to main.
---

# Submit Pull Request Workflow

Create a well-documented pull request for the current feature branch, following the project's trunk-based development workflow and PR template.

> [!CAUTION]
> **Scope boundary**: This skill pushes code, creates pull requests, monitors CI, and commits CI fixes (with user approval). It does **NOT** implement new features or run formal code reviews. When the PR is created and CI passes, **stop** — the workflow is complete.

> [!WARNING]
> **Checkpoint protocol.** When this workflow reaches a `### CHECKPOINT`, you **must** actively prompt the user for a decision — do not simply present information and continue. Use your agent's interactive prompting mechanism (e.g., `AskUserQuestion` in Claude Code) to require an explicit response before proceeding. This prevents queued or in-flight messages from being misinterpreted as approval. If your agent lacks interactive prompting, output the checkpoint content and **stop all work** until the user explicitly responds.

## Step 1: Pre-Submission Checks

Verify the branch is ready for a pull request:

1. Confirm we are on a feature branch (not `main`). If on `main`, stop and ask the user to create a feature branch first.

2. Sync with main:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

   If there are conflicts, stop and help the user resolve them before proceeding.

3. Run your project's quality checks:

   ```
   # Adapt to your project's toolchain
   type-check      # TypeScript tsc, mypy, etc.
   lint            # ESLint, Ruff, golangci-lint, etc.
   format:check    # Prettier, Black, gofmt, etc.
   test            # Vitest, Jest, pytest, etc.
   build           # If a build step exists
   ```

   If formatting checks fail, auto-fix by running the formatter on the reported files and stage the changes.

4. Perform a final security scan on changed files:

   - Are there hardcoded secrets, API keys, or credentials in the diff?
   - Are all user inputs validated and sanitized?
   - Are authentication and authorization checks present on new endpoints?
   - Are error responses safe? (no internal details leaked)
   - Are dependencies free of known CVEs?

   > **Claude Code optimization**: If the `/security-scanning:security-sast` skill is available, use it for enhanced automated scanning. Otherwise, follow the manual checklist above.

If any check fails, report the failure clearly and ask the user whether to fix it now or proceed anyway.

## Step 2: Analyze Changes

Understand what this PR contains:

1. Run `git log origin/main..HEAD --oneline` to see all commits on this branch
2. Run `git diff origin/main...HEAD --stat` to see the file change summary
3. Run `git diff origin/main...HEAD` to read the actual changes

Determine:

- **Type of change**: feature, fix, docs, refactor, test, chore (from commit prefixes)
- **Scope**: frontend, backend, full-stack, infrastructure
- **Includes database migrations?** (check for migration files or schema changes)
- **Includes infrastructure changes?** (containers, CI/CD, environment files)
- **Includes security-sensitive changes?** (auth, authorization, API security, secrets)
- **Related issues**: Extract from commit messages (Closes #NNN, Fixes #NNN)

## Step 3: Deployment Council Review (Conditional)

Activate the Deployment Council from the skill's `councils/deployment-council.md` if ANY of these are true:

- Database migrations are included
- Container or infrastructure files changed
- Environment variables were added or modified
- Authentication or authorization code changed
- CI/CD pipeline files modified

If activated, read the council template and run through the full Deployment Checklist. For each council member, read their agent definition from the skill's `agents/` directory and use the complexity tier specified to calibrate review depth. Adapt the checklist to your deployment infrastructure:

### Platform Engineer (Lead)

- Application builds and packages successfully for deployment?
- Environment variables configured?
- Health check endpoints working?
- Resource limits set (CPU, memory)?
- Logging and monitoring configured?
- Rollback strategy defined?

### Security Engineer

- Secrets managed securely (not in code)?
- HTTPS/TLS configured?
- API authentication working?
- CORS configured correctly?
- Security headers configured (e.g., Content-Security-Policy, X-Frame-Options, HSTS)?
- No high-severity vulnerabilities?

### QA Lead

- E2E tests passing?
- Critical user flows validated?
- Performance testing completed?
- No known P0/P1 bugs?
- Regression tests passing?
- Smoke tests defined for post-deployment?

### Deployment Decision

- **Status**: Approved / Not Ready / Blocked
- **Deployment Strategy**: Rolling / Blue-Green / Canary
- **Rollback Plan**: How to rollback if issues arise

### CHECKPOINT (only if Deployment Council was activated): Present the deployment readiness assessment to the user. Wait for confirmation before proceeding.

## Step 4: Generate PR Description

If your project has a PR template (e.g., `.github/PULL_REQUEST_TEMPLATE.md`), use it. Otherwise, generate a complete PR with these sections:

### Title

- Format: `<type>(<scope>): <short description>` matching conventional commits
- Keep under 70 characters
- Use the primary commit type and scope

### Body

**Description**: Synthesize from commit messages and changed files. Explain the why, not just the what.

**Type of Change**: Auto-detect from commit prefixes and mark the appropriate checkbox.

**Related Issues**: Extract from commit messages (`Closes #NNN`).

**Changes Made**: Bullet list of key changes, organized by area (frontend, backend, database, etc.).

**Testing**: Document what tests were added/updated and how to manually test.

**Checklist**: Pre-fill based on actual state:

- Check items that are actually done (tests pass, lint passes, etc.)
- Leave unchecked items that still need attention

**Breaking Changes**: Flag if any API contracts, database schemas, or public interfaces changed.

**Deployment Notes**: Include migration steps, new environment variables, infrastructure changes. Reference Deployment Council findings if activated.

### Changelog Entry

If the PR includes user-facing changes, draft a changelog entry:

- Determine the category: Added / Changed / Fixed / Removed
- Write a one-line description from the user's perspective
- Reference the PR number

### CHECKPOINT: Present the PR title and full body to the user. Allow them to review and request edits before submission.

## Step 5: Push and Create PR

1. Push the branch to the remote:

   ```bash
   git push origin <branch-name> -u
   ```

2. Create the PR. Using the GitHub CLI as an example:

   ```bash
   gh pr create --title "<title>" --body "<body>" --base main
   ```

   Adapt to your project's version control platform if not using GitHub.

3. If the PR template includes labels, add appropriate labels.

## Step 6: Monitor CI Pipeline

After creating the PR, watch the CI pipeline until it completes:

1. Check for the latest CI run on the branch.

2. Monitor the run until it finishes. Using GitHub CLI as an example:

   ```bash
   gh run list --branch <branch-name> --limit 1 --json databaseId,status
   gh run watch <run-id> --exit-status
   ```

3. If CI **fails**, fetch the failed job logs and diagnose:
   - **Formatting failures**: Auto-fix with the formatter, commit, push, and re-watch. No checkpoint needed.
   - **All other failures**: **CHECKPOINT** — present the diagnosis and proposed fix to the user. Wait for approval before committing. After approval, fix, commit, push, and re-watch.

4. If CI **passes**: proceed to Step 7.

## Step 7: Post-PR Summary

Present to the user:

- PR URL (clickable link)
- Summary of what was submitted
- CI status (all checks passing)
- Changelog entry (if generated)
- Reminder about branch lifecycle: delete branch after merge

If the Deployment Council was activated, remind the user of any deployment-specific steps that need to happen after merge.

> [!TIP]
> **Workflow complete.** The PR is submitted and CI is green. After the PR is merged and the branch is deleted, the feature lifecycle is done.
>
> **Pipeline**: `/plan-feature` → `/build-feature` or `/build-api` → `/review-code` → **`/submit-pr`** (you are here)
>
> If the user wants to start the next feature, suggest: "Run `/plan-feature` to begin planning the next feature."
