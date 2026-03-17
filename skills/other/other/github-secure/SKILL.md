---
name: github-secure
description: Configure GitHub repository security with branch protection, Dependabot, security scanning, and CI workflows. Integrates with mern-scaffold, nean-scaffold, and iOS projects.
argument-hint: "[--branch main] [--reviewers auto] [--ralph-mode] [--skip-workflows]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Apply security best practices to a GitHub repository: branch protection, automated security scanning, dependency management, and required CI checks.

**Designed to work with:** `/mern-scaffold`, `/mern-kit`, `/nean-scaffold`, `/nean-kit`, and iOS projects.

## Arguments
- `--branch <n>` — Protected branch name (default: `main`)
- `--reviewers <n>` — Required reviewers for PRs (default: auto-detect). If the repo has only 1 collaborator, defaults to `0` (solo-dev mode). Otherwise defaults to `1`. Use `--reviewers 0` to force solo-dev mode.
- `--ralph-mode` — Configure for Ralph automation (see below)
- `--skip-workflows` — Skip creating CI workflow files (use if existing ci.yml is sufficient)

## Ralph Mode (`--ralph-mode`)

Configures the repository for fully autonomous Ralph operation:

1. **Auto-merge enabled** — PRs can use `gh pr merge --auto`
2. **Required reviews = 0** — No human approval needed for merge
3. **Enforce admins = true** — Rules apply to everyone (safe since no review to bypass)
4. **CI checks still required** — Quality gates remain enforced
5. **All other security settings remain** — Dependabot, secret scanning, etc.

This allows Ralph to:
- Create PRs
- Enable auto-merge on each PR
- Wait for CI to pass
- PR merges automatically
- Continue to next story

**Use when:** Solo developers, personal portfolios, or trusted automation. A solo dev can't meaningfully self-review — CI is the real quality gate.

**For team projects:** Use default settings (reviewers >= 1) and merge PRs manually or via `/github-merge-stack`.

## What gets created/configured

### Files created
```
.github/
├── dependabot.yml              # Automated dependency updates
├── CODEOWNERS                  # Required reviewers by path
├── SECURITY.md                 # Security policy
├── pull_request_template.md    # PR template with checklist
└── workflows/
    ├── security.yml            # CodeQL + dependency review
    ├── pr-check.yml            # PR validation (size, commits)
    └── dependabot-auto-merge.yml  # Auto-merge minor/patch Dependabot PRs
```

**Note:** Does NOT overwrite existing `ci.yml` from scaffold commands.

### Branch protection rules (via gh CLI)
- Require pull request before merging
- Require N approving reviews (0 in ralph-mode)
- Dismiss stale reviews on new commits
- Require status checks to pass (ci, security)
- Require branches to be up to date
- **Require linear history** (pairs with squash-only merge)
- **Enforce admins** (true when reviewers = 0; false when reviewers > 0 for solo-dev bypass)
- **Required conversation resolution** (all review threads must be resolved)
- Block force pushes
- Block deletions

### Repository settings (via gh CLI)
- Enable Dependabot alerts
- Enable Dependabot security updates
- Enable secret scanning
- Enable push protection
- **Enable auto-merge** (always, for flexibility)
- **Delete branch on merge** (auto-cleanup merged branches)
- **Squash merge only** (disable merge commit + rebase for linear history)
- **Disable wiki** (unused, reduces attack surface)
- **Disable forking** (private org-owned repos only — user-owned repos don't support this)

## Prerequisites
- `gh` CLI installed and authenticated
- Admin access to the repository
- Repository must exist on GitHub (use scaffold `--github` first)

## Important: Private Repo Limitations

**CodeQL** code scanning is **free for public repositories only**. For private repos:
- Make the repo public (`gh repo edit --visibility public --accept-visibility-change-consequences`), OR
- Purchase GitHub Advanced Security license, OR
- Use `--skip-workflows` to skip CodeQL setup

**Secret scanning + push protection** also requires GitHub Advanced Security for private repos. For private repos without GHAS, skip the secret scanning API call (it will return 422). These features enable automatically when a repo is made public.

The skill will check repo visibility and warn if private. Recommend making the repo public for open-source projects or personal portfolios.

## Workflow
1. **Verify gh CLI authentication**
   - Confirm `gh auth status` succeeds
   - Detect collaborator count: `gh api "/repos/$REPO/collaborators" --jq length`
   - If `--reviewers` not specified: set to 0 if solo (1 collaborator), else 1
   - Log: "Detected N collaborators, using --reviewers M"
2. **Detect project type** (MERN, NEAN, iOS)
3. **Check repo visibility**
   - `gh repo view --json visibility -q .visibility`
   - If private: skip CodeQL in security.yml, skip secret scanning API calls
   - Log what was skipped and why
4. **Configure repository settings**
   - `gh api PATCH /repos/$REPO` with: delete_branch_on_merge, squash-only, disable wiki, auto-merge
   - Conditionally disable forking (org-owned private repos only)
   - Enable Actions to approve PRs: `gh api PUT /repos/$REPO/actions/permissions/workflow -F can_approve_pull_request_reviews=true -F default_workflow_permissions=read`
5. **Detect GitHub username**
   - `GH_USER=$(gh api user -q .login)`
   - Replace `your-username` with actual username in all template content before writing
   - For SECURITY.md: use GitHub private email `$GH_USER@users.noreply.github.com` or omit email
6. **Create security configuration files**
   - Check if each file already exists (scaffold may have created them)
   - Only create files that are missing
   - If files exist, verify they look correct (right username, right paths)
7. **Harden existing workflow files**
   - For each `.github/workflows/*.yml` that lacks a top-level `permissions:` block, inject one:
     - ci.yml: `permissions: { contents: read }`
     - pr-check.yml: `permissions: { contents: read, pull-requests: write }`
     - security.yml: already has permissions (skip)
   - Pin any `@main` or `@master` action refs to latest release tags
8. **Apply branch protection rules**
9. **Enable repository security features**
10. **Verify configuration**
    - Run automated verification (see reference: verify-github-secure.sh)
    - Query repo settings and branch protection via `gh api`
    - Check all workflow files have `permissions:` blocks
    - Print pass/fail summary

## MERN integration notes

When used after `/mern-scaffold --github`:
- Preserves existing `ci.yml` workflow
- Adds security.yml for CodeQL analysis (JavaScript/TypeScript)
- Configures Dependabot for npm ecosystem
- CODEOWNERS protects `apps/web/src/app/api/` and `packages/shared/`
- Required status checks: `lint-test-build` (from ci.yml). Add `CodeQL Analysis` only if public repo.

## NEAN integration notes

When used after `/nean-scaffold --github`:
- Preserves existing `ci.yml` workflow
- Adds security.yml for CodeQL analysis (JavaScript/TypeScript)
- Configures Dependabot for npm ecosystem
- CODEOWNERS protects:
  - `apps/api/src/modules/` (API modules)
  - `libs/shared/types/` (shared DTOs/interfaces)
  - `libs/api/auth/` (authentication)
  - `libs/api/database/` (entities, migrations)
- Required status check: `Lint, Test & Build` (from ci.yml job `name:`). Add `CodeQL Analysis` only if public repo.
- Dependabot groups Angular, NestJS, and Nx updates separately

## iOS integration notes

When used after `/ios-scaffold --github`:
- Preserves existing `ci.yml` workflow
- Adds security.yml for CodeQL analysis (Swift)
- Configures Dependabot for Swift Package Manager (if Package.swift exists)
- CODEOWNERS protects `App/Sources/Services/` and `Config/`
- Required status check: `Build & Test` (from ci.yml job `name:`). Add `CodeQL Analysis` only if public repo.

## Status Check Context Names

GitHub uses the job `name:` property (not the YAML key) as the status check context when `name:` is set. This matters for branch protection `required_status_checks.contexts`:

| Platform | CI Job `name:` | Status check context |
|----------|---------------|---------------------|
| MERN | *(none set)* | `lint-test-build` |
| NEAN | `Lint, Test & Build` | `Lint, Test & Build` |
| iOS | `Build & Test` | `Build & Test` |

**CodeQL:** Only add `CodeQL Analysis` to required status checks for **public** repos. Private repos without GHAS cannot run CodeQL.

## Security policies applied

### Branch protection
- No direct pushes to main/master
- PRs require review (unless `--ralph-mode`)
- PRs require passing CI
- No force pushes (history protection)

### Dependency security
- Dependabot alerts enabled
- Weekly dependency updates (grouped)
- Security updates auto-created

### Code security
- Secret scanning enabled
- Push protection (blocks commits with secrets)
- CodeQL analysis on PRs

## Output
- Files created
- Branch protection rules applied
- Security features enabled
- Auto-merge enabled
- Verification results
- **Remind that local hooks via `/github-hooks` complement this**

## Reference
For detailed configurations and customization, see `reference/github-secure-reference.md`
