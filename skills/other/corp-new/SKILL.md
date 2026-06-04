---
name: corp-new
description: Use when creating, verifying, or registering a private corp-* department repository for a founder or company operating system, including local repo setup, GitHub repository creation or cloning, safe synchronization, and registration in an HQ Markdown file.
---

# Corp New

Create or verify a private `corp-*` department repository and register it in a local HQ Markdown file.

## What The Skill May Change

After approval, this skill may create a local folder, initialize git, create a private GitHub repository, clone an existing repository, commit a minimal README, push committed work, fetch from origin, and edit one HQ table row.

Stop and ask for explicit approval after the dry-run summary before any create, clone, commit, push, or HQ edit.

## Configuration

Resolve configuration in this order: explicit user request, environment variables, project instructions, then documented defaults.

Required values from the user or project config:

| Value | Env var | Default |
|---|---|---|
| Department label | `DEPARTMENT_LABEL` | ask the user |
| Department domain | `DEPARTMENT_DOMAIN` | ask the user |
| GitHub owner or org | `GITHUB_OWNER` | ask the user |
| Local repositories root | `CORP_REPOS_ROOT` | `~/Documents/GitHub` |
| HQ Markdown file | `HQ_FILE` | ask the user |
| Repository prefix | `REPO_PREFIX` | `corp-` |

Optional values:

- `DEPARTMENT_TABLE_HEADING`: heading or marker near the department table.
- `DEPARTMENT_SLUG`: explicit slug override.

Ask before making changes if the department label, department domain, `GITHUB_OWNER`, or `HQ_FILE` cannot be resolved. Repositories are private by design; do not offer public visibility unless the user explicitly overrides the skill's safety model.

## Preflight

Before creating or editing anything:

```bash
git --version
gh auth status
gh api user --jq '.login'
test -d "$CORP_REPOS_ROOT"
test -f "$HQ_FILE"
```

Reject unsafe targets:

- archive/history folders for `HQ_FILE`;
- slug that does not match `^corp-[a-z0-9][a-z0-9-]*$` unless the user explicitly overrides;
- ambiguous ownership when an existing department could already own the domain.

## Read-Only Preflight Result

Report this before the dry run:

```text
Local folder: exists | missing | conflict
GitHub repo: exists | missing | inaccessible
HQ row: exists | missing | ambiguous
Proposed action: create | clone | register | update existing row | verify only
```

## Dry Run Summary

Before making changes, show a short summary:

```text
Department: <Human label>
Slug: <corp-slug>
Local path: <CORP_REPOS_ROOT>/<corp-slug>
GitHub repo: <GITHUB_OWNER>/<corp-slug>
HQ file: <HQ_FILE>
HQ row: | <Human label> | `<local path>`; [GitHub](https://github.com/<GITHUB_OWNER>/<corp-slug>) | <domain> |
```

Stop here and ask for explicit approval. Continue only after the user approves the proposed mutations.

## Workflow

1. Normalize the department.
   - Prefer `<REPO_PREFIX><domain>` as the slug.
   - Keep the human label short, for example `Media`, `Legal`, `Analytics`.
   - Keep the domain description operational, for example `media assets and publishing workflows`.

2. Inspect existing state.
   - Local: `test -d "$CORP_REPOS_ROOT/$SLUG"`.
   - GitHub: `gh repo view "$GITHUB_OWNER/$SLUG" --json name,visibility,url,sshUrl,defaultBranchRef`.
   - HQ: `rg -n "$SLUG|$DEPARTMENT_LABEL" "$HQ_FILE"`.

3. Create missing resources.
   - If local folder is missing and GitHub exists, clone it into `$CORP_REPOS_ROOT/$SLUG`.
   - If GitHub is missing and local folder is a git repo, create a private remote and push committed work:
     `gh repo create "$GITHUB_OWNER/$SLUG" --private --source "$CORP_REPOS_ROOT/$SLUG" --remote origin --push`.
   - If both are missing, create the local folder, initialize git, add a minimal `README.md`, commit, create the private GitHub repo, and push.
   - If local exists with unrelated uncommitted work, preserve it. Push only committed changes unless the user explicitly asks to commit current work.

4. Sync safely.
   - Run `git -C "$CORP_REPOS_ROOT/$SLUG" fetch origin`.
   - Check `git -C "$CORP_REPOS_ROOT/$SLUG" status --short --branch`.
   - Push only when the current branch is ahead and no pull/rebase decision is needed.
   - Never force-push, reset, delete, or discard user work.

5. Register in HQ.
   - Add or update exactly one row in the department table:
     `| <Human label> | \`<local path>\`; [GitHub](https://github.com/<GITHUB_OWNER>/<SLUG>) | <domain> |`
   - Keep the HQ edit minimal.
   - Do not copy department content into HQ; link to the owner repo.

6. Verify.
   - Confirm GitHub visibility is `PRIVATE`.
   - Confirm default branch and URL from `gh repo view`.
   - Confirm local remote points to the configured GitHub repo.
   - Show the exact HQ row changed.

## Minimal README

When bootstrapping an empty department repo, use a small neutral README:

```markdown
# <Department Name>

Owner repository for <department domain>.

## Scope

- <primary responsibility>
- <secondary responsibility>

## Source of truth

This repository owns department-specific workflows and artifacts. Cross-department routing lives in the HQ file.
```

## Final Response

Report only verified facts:

```text
Created or verified: <GITHUB_OWNER>/<SLUG>
Visibility: PRIVATE
Local path: <path>
GitHub: <url>
Default branch: <branch>
HQ row: <exact row>
Skipped: <anything intentionally left untouched>
```

## Boundaries

This skill manages department repository registration. Product claims, pricing, secrets, billing evidence, customer data, and operational runbooks belong in the appropriate owner repository and must not be copied into the HQ index.
