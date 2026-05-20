---
name: fix-docker-image-org-mismatch
description: Fix Docker GHCR push failures when repository organization changes but IMAGE\_NAME remains hardcoded to old org
category: ci-cd
date: 2026-02-09
tags: [docker, ghcr, github-actions, authentication, organization-migration]
user-invocable: true
---

# Fix Docker Image Organization Mismatch

## Overview

| Field | Value |
|-------|-------|
| **Date** | 2026-02-09 |
| **Objective** | Fix Docker Build workflow failure after repository transfer to new GitHub organization |
| **Root Cause** | IMAGE\_NAME hardcoded to old org while GITHUB\_TOKEN scoped to new org |
| **Outcome** | ✅ All Docker images successfully pushed to GHCR under correct organization |
| **Issue** | PR #3123 - Docker CI failure on HomericIntelligence/ProjectOdyssey |

## When to Use This Skill

**Primary Trigger**: Docker workflow fails with GHCR push errors after repository org change

**Specific Indicators**:

1. Error message: `could not parse reference: ghcr.io/{OldOrg}/{repo}:tag`
2. Error message: `unable to parse registry reference`
3. Docker build succeeds but push to GHCR fails with authentication error
4. Repository was recently transferred to a new GitHub organization
5. GITHUB\_TOKEN scope shows different org than IMAGE\_NAME in workflow

**Example Error**:

```bash
[0000] ERROR could not determine source: errors occurred attempting to resolve 'ghcr.io/mvillmow/ProjectOdyssey:main':
  - docker: could not parse reference: ghcr.io/mvillmow/ProjectOdyssey:main
  - oci-registry: unable to parse registry reference="ghcr.io/mvillmow/ProjectOdyssey:main"
```

## Problem Background

### Why This Happens

When a repository is transferred to a new GitHub organization:

1. GitHub workflows automatically get a `GITHUB\_TOKEN` scoped to the **new org**
2. Hardcoded `IMAGE\_NAME` variables still reference the **old org**
3. Docker tries to push to `ghcr.io/old-org/repo` using a token for `new-org`
4. GHCR rejects the push due to permission mismatch

### Key Constraint

**Docker image names MUST be lowercase**, but `github.repository` preserves the
original repository name case (e.g., `HomericIntelligence/ProjectOdyssey`). This
causes failures in tools that manually construct Docker image references.

## Verified Workflow

### 1. Identify All Hardcoded Image Names

Search for hardcoded org references in Docker-related files:

```bash
# Find IMAGE\_NAME in workflows
grep -r "IMAGE\_NAME" .github/workflows/

# Find GHCR references in workflows
grep -r "ghcr.io" .github/workflows/

# Find in Justfile/Makefile
grep -r "REPO\_NAME\|IMAGE\_NAME" justfile Makefile 2>/dev/null
```

**Files to check**:

- `.github/workflows/docker.yml`
- `.github/workflows/release.yml`
- `justfile` or `Makefile`
- Any Docker Compose files

### 2. Update Workflow IMAGE\_NAME

**Fix Pattern**: Replace hardcoded org with lowercase new org name

```yaml
# .github/workflows/docker.yml
env:
  REGISTRY: ghcr.io
  # BEFORE (BROKEN):
  IMAGE\_NAME: oldorg/projectname

  # AFTER (FIXED):
  IMAGE\_NAME: neworg/projectname  # lowercase org name
```

**Critical**: Image name must be **all lowercase** for Docker/GHCR compatibility.

### 3. Update Release Workflow

If you have a separate release workflow, add `IMAGE\_NAME` env var at job level:

```yaml
# .github/workflows/release.yml
jobs:
  publish-docker:
    runs-on: ubuntu-latest
    env:
      # Add this env var
      IMAGE\_NAME: neworg/projectname  # lowercase

    steps:
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: |
            ghcr.io/${{ env.IMAGE\_NAME }}:${{ needs.validate-version.outputs.version }}
            ghcr.io/${{ env.IMAGE\_NAME }}:latest
```

**Replace**:

- `ghcr.io/${{ github.repository }}` → `ghcr.io/${{ env.IMAGE\_NAME }}`

### 4. Update Build System References

If using Justfile or Makefile:

```justfile
# justfile
REGISTRY := "ghcr.io"
# BEFORE:
REPO\_NAME := "oldorg/oldreponame"

# AFTER:
REPO\_NAME := "neworg/projectname"  # lowercase
```

### 5. Run Pre-commit and Verify

```bash
# Run all linting
just pre-commit-all

# Check for remaining old org references
grep -r "oldorg/projectname\|oldorg/oldreponame" \
  --include="*.md" --include="*.yml" --include="*.toml" .

# Verify no hardcoded paths remain
grep -r "/home/olduser" --include="*.md" --include="*.py" --include="*.sh" .
```

### 6. Commit and Create PR

```bash
# Commit changes
git add .github/workflows/docker.yml \
        .github/workflows/release.yml \
        justfile

git commit -m "fix(ci): update IMAGE\_NAME for new organization

- Update IMAGE\_NAME from oldorg to neworg
- Fix GHCR push authentication failures
- Ensure lowercase image names for Docker compatibility

Fixes Docker Build workflow where GITHUB\_TOKEN scoped to
new org could not push to old org's GHCR.
"

# Create PR
gh pr create \
  --title "fix(ci): update Docker image org references" \
  --body "Fixes GHCR push failures after org transfer" \
  --label "ci-cd"
```

### 7. Verify Docker Build Success

After PR is merged:

```bash
# Check Docker workflow status
gh run list --workflow="Docker Build and Publish" --branch main --limit 1

# View details
gh run view <run-id>

# Verify images pushed correctly
gh run view <run-id> --log | grep "pushing manifest"
```

## Failed Attempts

| Attempt | Why It Failed | Lesson Learned |
|---------|---------------|----------------|
| Used `${{ github.repository }}` directly in tags | Preserves case (e.g., `OrgName/Repo`), Docker requires lowercase | Always use explicit lowercase IMAGE\_NAME env var |
| Only updated docker.yml, missed release.yml | Release workflow still used old org, failed on releases | Search all workflows, not just primary Docker workflow |
| Forgot to update Justfile REPO\_NAME | Local `just docker-build` commands failed | Check all build system files (Just, Make, scripts) |
| Tried `${{ github.repository_owner }}` | Still case-sensitive, doesn't include repo name | Hardcode full `org/repo` in lowercase |
| Re-ran failed jobs immediately | Flaky Mojo tests caused false failures | Wait for full workflow completion before judging success |

## Results & Parameters

### Successful Configuration

**docker.yml**:

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE\_NAME: homericintelligence/projectodyssey  # lowercase
```

**release.yml**:

```yaml
jobs:
  publish-docker:
    env:
      IMAGE\_NAME: homericintelligence/projectodyssey  # lowercase
    steps:
      - name: Build and push
        with:
          tags: |
            ghcr.io/${{ env.IMAGE\_NAME }}:${{ version }}
            ghcr.io/${{ env.IMAGE\_NAME }}:latest
```

**justfile**:

```justfile
REGISTRY := "ghcr.io"
REPO\_NAME := "homericintelligence/projectodyssey"
```

### Verification Results

✅ **All Docker jobs passed**:

- build-and-push (production): 4m34s ✅
- build-and-push (runtime): 6m18s ✅
- build-and-push (ci): 3m41s ✅
- security-scan: 1m18s ✅
- test-images: 1m47s ✅

✅ **Images successfully pushed**:

- `ghcr.io/homericintelligence/projectodyssey:main`
- `ghcr.io/homericintelligence/projectodyssey:main-ci`
- `ghcr.io/homericintelligence/projectodyssey:main-prod`
- Plus SHA-tagged variants

### Performance Impact

- No performance impact - purely configuration fix
- Build times remain the same
- Authentication now works correctly with GITHUB\_TOKEN

## Additional Context

### Common Pitfall: Case Sensitivity

Docker image names **must be lowercase**, but GitHub variables preserve case:

- `github.repository` → `HomericIntelligence/ProjectOdyssey` (mixed case) ❌
- `IMAGE\_NAME` → `homericintelligence/projectodyssey` (lowercase) ✅

### Related Issues

This fix also addresses:

1. SBOM generation failures (anchore/sbom-action uses image name)
2. Security scanning failures (Trivy uses image name)
3. Image testing failures (test-images job needs correct reference)

### Scope of Changes

Typical files to update:

- `.github/workflows/docker.yml` (primary)
- `.github/workflows/release.yml` (if exists)
- `justfile` or `Makefile` (local builds)
- Documentation references to old GHCR URLs

## Cross-Repository Applicability

This skill applies to **any repository** that:

1. Uses GitHub Actions to build Docker images
2. Pushes to GitHub Container Registry (GHCR)
3. Was transferred to a new organization
4. Has hardcoded IMAGE\_NAME or REPO\_NAME variables

**Generic workflow pattern** (adapt to your repo):

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE\_NAME: <new-org>/<repo-name>  # lowercase, update this line
```

## Verified On

| Project | Context | Details |
|---------|---------|---------|
| ProjectOdyssey | PR #3123 - Docker CI fix after org transfer | [notes.md](../references/notes.md) |

## References

- [GitHub Actions: GHCR Authentication](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Image Naming Conventions](https://docs.docker.com/engine/reference/commandline/tag/#extended-description)
- [GitHub: Transferring a Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository)
