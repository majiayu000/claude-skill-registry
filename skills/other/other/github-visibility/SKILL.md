---
name: github-visibility
description: "Toggle GitHub repo between private and public with security hardening, contribution lockdown, and pre-flight safety checks."
argument-hint: "<public|private> [--force] [--skip-security-check]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose

Safely toggle a GitHub repository between private and public visibility. Applies the right security and access settings for each state. Public repos become read-only showcases — clone and fork only, no outside contributions.

**Designed to work alongside:** `/github-secure`. Detects whether it's been run and adapts (patches `security.yml` CodeQL job, patches branch protection status checks). Does not invoke `github-secure`.

## Arguments

- `<public|private>` — **Required.** Target visibility. No auto-toggle — explicit target prevents accidents.
- `--force` — Bypass pre-flight sensitive data check (use when you've already audited).
- `--skip-security-check` — Skip secret scanning entirely (faster, less safe).

## What gets changed

### Going public
- Visibility → public
- Issues, wiki, discussions, projects → disabled
- Secret scanning + push protection → enabled (free for public repos)
- Dependabot alerts + auto-fixes → enabled
- CodeQL → enabled in `security.yml` (if exists)
- Branch protection → add push restrictions (owner-only), add `CodeQL Analysis` to required checks
- `.github/workflows/close-external-prs.yml` → created (auto-closes fork PRs)
- `LICENSE` → created with MIT template (if missing)

### Going private
- Visibility → private
- Issues, wiki, discussions, projects → stay disabled
- Secret scanning → auto-disabled by GitHub
- CodeQL → conditional `if: github.repository_visibility == 'public'` added to `security.yml`
- Branch protection → remove push restrictions, remove `CodeQL Analysis` from required checks
- `.github/workflows/close-external-prs.yml` → deleted (not needed when private)
- `LICENSE` → left in place

## Prerequisites

- `gh` CLI installed and authenticated
- Admin access to the repository
- Repository must exist on GitHub
- Must be run from within the git repo

## Workflow

### Step 1: Validate environment

```bash
# Verify gh CLI
gh auth status

# Detect repo info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
GH_USER=$(gh api user -q .login)
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
CURRENT_VIS=$(gh repo view --json visibility -q .visibility)
```

If already at target visibility → exit early with message: "Repository is already <target>. No changes needed."

### Step 2: Pre-flight safety checks (private → public only)

Skip if `--skip-security-check` or `--force`. Any failure blocks unless `--force`.

**Run all four checks. If any find issues, report them and block.**

1. **Tracked sensitive files** — Check for `.env`, `.pem`, `.key`, `.p12`, `.credentials`, `.secret`, `.pfx`, `id_rsa`, `id_ed25519` in tracked files
2. **Secrets in tracked files** — Scan for AWS keys (`AKIA`), Stripe keys (`sk_live_`), GitHub tokens (`ghp_`, `gho_`, `github_pat_`), generic passwords (`password\s*=`, `secret\s*=`), connection strings (`mongodb+srv://`, `postgres://`)
3. **Historical sensitive files** — Check git history for files ever committed matching the sensitive patterns
4. **`.gitignore` coverage** — Verify `.gitignore` exists and covers `.env*`, `*.pem`, `*.key`, `node_modules/`

If blocked → output the file list, suggest `git filter-repo` for historical files, mention `--force` as escape hatch.

See `reference/github-visibility-reference.md` for the complete scan script.

### Step 3: Detect `github-secure` state

Check for indicators that `/github-secure` has been run:

```bash
HAS_SECURITY_YML=false
HAS_CODEOWNERS=false
HAS_DEPENDABOT=false
HAS_BRANCH_PROTECTION=false

[ -f .github/workflows/security.yml ] && HAS_SECURITY_YML=true
[ -f .github/CODEOWNERS ] && HAS_CODEOWNERS=true
[ -f .github/dependabot.yml ] && HAS_DEPENDABOT=true
gh api "/repos/$REPO/branches/$DEFAULT_BRANCH/protection" >/dev/null 2>&1 && HAS_BRANCH_PROTECTION=true
```

Store results — used in steps 6 and 7.

### Step 4: Change visibility

```bash
gh repo edit --visibility <target> --accept-visibility-change-consequences
```

### Step 5: Configure repo features

**Going public:**
```bash
gh repo edit --enable-issues=false
gh repo edit --enable-wiki=false
gh repo edit --enable-discussions=false
gh repo edit --enable-projects=false
```

**Going private:**
Issues, wiki, discussions, projects stay disabled (user preference).
```bash
gh repo edit --enable-issues=false
gh repo edit --enable-wiki=false
gh repo edit --enable-discussions=false
gh repo edit --enable-projects=false
```

### Step 6: Security scanning

**Going public (free for public repos):**

```bash
# Enable secret scanning + push protection
gh api --method PATCH "/repos/$REPO" --input - <<'EOF'
{
  "security_and_analysis": {
    "secret_scanning": {"status": "enabled"},
    "secret_scanning_push_protection": {"status": "enabled"}
  }
}
EOF

# Enable Dependabot alerts + auto-fixes
gh api --method PUT "/repos/$REPO/vulnerability-alerts"
gh api --method PUT "/repos/$REPO/automated-security-fixes"
```

If `security.yml` exists:
- If CodeQL job has `if: github.repository_visibility == 'public'` → remove the condition
- If CodeQL job is missing → add it

**Going private:**
- Secret scanning auto-disabled by GitHub (no action needed)
- If `security.yml` exists → add condition to CodeQL job: `if: github.repository_visibility == 'public'`

See `reference/github-visibility-reference.md` for CodeQL conditional patterns.

### Step 7: Branch protection adjustments

**Only if branch protection exists** (`HAS_BRANCH_PROTECTION=true`). If no branch protection → skip with warning: "No branch protection found. Skipping adjustments. Consider running /github-secure."

Uses read-modify-write pattern — reads current config, merges changes, writes back. Does not overwrite existing settings.

**Going public:**
- Add **push restrictions** → only `$GH_USER` can push directly
- Add `CodeQL Analysis` to required status checks (if `security.yml` has CodeQL)

**Going private:**
- Remove push restrictions (`"restrictions": null`)
- Remove `CodeQL Analysis` from required status checks

See `reference/github-visibility-reference.md` for the read-modify-write scripts.

### Step 8: Auto-close external PRs workflow

**Going public:**
Create `.github/workflows/close-external-prs.yml` using template from reference file.
- Triggers on `pull_request_target: [opened]`
- Closes PRs from forks or non-owner authors
- Posts polite message: "This repository is not accepting external contributions. Feel free to fork and modify for your own use."

**Going private:**
Delete `.github/workflows/close-external-prs.yml` if it exists.

See `reference/github-visibility-reference.md` for the full workflow template.

### Step 9: LICENSE file (public only)

**Going public:**
If no `LICENSE`, `LICENSE.md`, or `LICENSE.txt` exists → create `LICENSE` with MIT template using current year and `$GH_USER`.

**Going private:**
Leave LICENSE in place (no harm in keeping it).

See `reference/github-visibility-reference.md` for the MIT LICENSE template.

### Step 10: Commit changes

Stage any created/modified files and commit:

```bash
git add -A .github/workflows/close-external-prs.yml LICENSE .github/workflows/security.yml 2>/dev/null || true
# Only commit if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "chore: configure repo for <target> visibility"
fi
```

### Step 11: Verify and report

```bash
# Verify visibility
gh repo view --json visibility -q .visibility

# Verify features
gh repo view --json hasIssuesEnabled,hasWikiEnabled,hasDiscussionsEnabled,hasProjectsEnabled

# Verify security (public only)
gh api "/repos/$REPO" --jq '.security_and_analysis'

# Verify branch protection (if it exists)
gh api "/repos/$REPO/branches/$DEFAULT_BRANCH/protection" --jq '{
  push_restrictions: .restrictions,
  required_checks: .required_status_checks.contexts
}' 2>/dev/null || echo "No branch protection configured"
```

See `reference/github-visibility-reference.md` for the full verification script.

Print summary table of all changes applied/skipped. Include recommendations:
- If `github-secure` wasn't run → suggest running `/github-secure`
- If going public → suggest adding repo description and topics for discoverability: `gh repo edit --description "..." --add-topic "..."`

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Already at target visibility | Exit early, no changes |
| `github-secure` never run | Complete visibility change, recommend running `/github-secure` |
| No branch protection exists | Skip branch protection adjustments, log warning |
| No `security.yml` exists | Skip CodeQL adjustments, log info |
| Pre-flight finds secrets in history | Block with recommendation to use `git filter-repo` |
| Pre-flight finds tracked sensitive files | Block with file list and recommendation to remove them |
| `.gitignore` missing or incomplete | Warn but do not block |
| LICENSE already exists | Skip LICENSE creation |
| `close-external-prs.yml` already exists (going public) | Overwrite with current template |
| `close-external-prs.yml` missing (going private) | Skip deletion, no error |

## Output

- Visibility change confirmation
- Repo features configured
- Security scanning status
- Branch protection adjustments
- Files created/modified/deleted
- Verification results (pass/fail summary)
- Recommendations

## Reference

For detailed templates, scripts, and configurations, see `reference/github-visibility-reference.md`
