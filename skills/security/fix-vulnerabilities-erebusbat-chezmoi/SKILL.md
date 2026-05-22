---
name: fix-vulnerabilities
description: Fix security vulnerabilities and Dependabot alerts in project dependencies. Use when the user asks to address security issues, update vulnerable packages, fix CVEs, or runs /fix-vulnerabilities.
metadata:
  category: security
  tools: gh
---

# Fix Vulnerabilities Skill

Detect, validate, and fix security vulnerabilities reported by GitHub Dependabot.

## Prerequisites

- `gh` CLI authenticated with repo access
- Git repository with GitHub remote
- Write access to the repository

## Workflow Overview

```
1. Detect Ecosystem → 2. Fetch Vulnerabilities → 3. Validate Each → 4. Fix by Severity → 5. Quality Checks → 6. Commit → 7. Summary
```

## Step 1: Detect Project Ecosystem

Detect the package ecosystem by checking for lockfiles AND project files together:

| Ecosystem | Lockfile            | Project File                     |
| --------- | ------------------- | -------------------------------- |
| pnpm      | `pnpm-lock.yaml`    | `package.json`                   |
| npm       | `package-lock.json` | `package.json`                   |
| yarn      | `yarn.lock`         | `package.json`                   |
| cargo     | `Cargo.lock`        | `Cargo.toml`                     |
| go        | `go.sum`            | `go.mod`                         |
| bundler   | `Gemfile.lock`      | `Gemfile`                        |
| pip       | `requirements.txt`  | `requirements.txt` or `setup.py` |
| poetry    | `poetry.lock`       | `pyproject.toml`                 |
| pipenv    | `Pipfile.lock`      | `Pipfile`                        |
| composer  | `composer.lock`     | `composer.json`                  |

```bash
ls -la | grep -E "(pnpm-lock|package-lock|yarn.lock|Cargo|go\.(mod|sum)|Gemfile|requirements|poetry|Pipfile|composer)"
```

**IMPORTANT:** Only handle ONE ecosystem per run. If multiple detected, ask user which to address.

## Step 2: Fetch Vulnerabilities from GitHub

```bash
gh repo view --json nameWithOwner -q '.nameWithOwner'

gh api repos/{owner}/{repo}/dependabot/alerts \
  --jq '.[] | select(.state == "open") | {
    number: .number,
    package: .dependency.package.name,
    ecosystem: .dependency.package.ecosystem,
    manifest: .dependency.manifest_path,
    severity: .security_advisory.severity,
    vulnerable_range: .security_vulnerability.vulnerable_version_range,
    patched_version: .security_vulnerability.first_patched_version.identifier,
    advisory_id: .security_advisory.ghsa_id,
    summary: .security_advisory.summary,
    url: .html_url
  }'
```

**Error handling:**
- Auth fails: "Run `gh auth status` to check, then `gh auth login` to fix."
- Rate limited: "Wait a few minutes and retry."
- Repo not found: "Verify you have access to this repo's security alerts."

## Step 3: Validate Each Vulnerability

Check if the vulnerability is already fixed in the current lockfile.

### JavaScript/Node.js (pnpm/npm/yarn)

```bash
pnpm why <package-name>   # or npm ls / yarn why
```

For other ecosystems (Rust, Go, Python, Ruby, PHP), see `references/ecosystems.md`.

**Compare installed version against `patched_version`:**
- If installed >= patched → Already fixed (see `references/error-recovery.md` for dismissal flow)
- If installed < patched → Needs fixing

## Step 4: Fix Vulnerabilities by Severity

Process in order: **HIGH → MEDIUM → (report LOW)**

| Severity | Action                                          |
| -------- | ----------------------------------------------- |
| critical | Fix immediately (treat as high)                 |
| high     | Fix automatically                               |
| medium   | Fix automatically                               |
| low      | Skip and report, ask user for further procedure |

### JavaScript/Node.js Fix Strategies

**Strategy 1: Direct dependency update**

```bash
pnpm update <package-name>   # or npm update / yarn upgrade
```

**Strategy 2: Transitive dependency override (if direct update doesn't resolve)**

For pnpm — add to `package.json`:
```json
{ "pnpm": { "overrides": { "<package-name>": "^<patched-version>" } } }
```

For npm:
```json
{ "overrides": { "<package-name>": "^<patched-version>" } }
```

For yarn:
```json
{ "resolutions": { "<package-name>": "^<patched-version>" } }
```

Then reinstall: `pnpm install` (or npm/yarn equivalent).

**IMPORTANT:** Use caret (`^`) ranges for overrides, not unbounded (`>=`).

For other ecosystem fix strategies (Rust, Go, Python, Ruby, PHP), see `references/ecosystems.md`.

### Breaking Changes

If a fix requires a **major version bump**, STOP and ask the user:
1. Attempt upgrade (rely on quality checks)
2. Skip this vulnerability
3. Show changelog first

## Step 5: Run Quality Checks

**For JavaScript/Node.js**, check `package.json` scripts:
```bash
cat package.json | jq '.scripts | keys[]' | grep -E "(typecheck|type-check|tsc|lint|test|build|check)"
```

Run discovered checks in order: typecheck → lint → test → build.

For other ecosystem check commands, see `references/ecosystems.md`.

Also check `README.md`, `Makefile`, and `.github/workflows/*.yml` for documented commands.

**If checks fail:** Analyze the error, determine if related to the update, and offer options: show full error, rollback, attempt auto-fix, or keep changes.

## Step 6: Commit Changes

### Branch Naming
```
security/{primary-advisory-id}
```

### Commit Style (conventional commits)
```
fix: {brief description of security fix}

- Update axios to ^1.12.0 (GHSA-xxxx: DoS via data: URLs)
- Add pnpm override for qs ^6.14.1 (GHSA-yyyy: arrayLimit bypass)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Grouping Strategy
1. **Complexity** — Simple version bumps together, overrides/patches separately
2. **Risk** — Keep potentially breaking changes isolated
3. **Related vulnerabilities** — Multiple vulns in same package = one commit

### Commit Process
1. Stage specific files (not `git add -A`): `git add package.json pnpm-lock.yaml`
2. Create commit with conventional format
3. Offer to create PR: `gh pr create --title "fix: address {severity}-severity security vulnerabilities" --body "..."`

## Step 7: Generate Summary

```markdown
## Security Vulnerability Fix Summary

### Fixed Vulnerabilities
| Severity | Package | Advisory | Fix Applied |
| -------- | ------- | -------- | ----------- |

### Dismissed (Already Fixed)
| Package | Advisory | Reason |
| ------- | -------- | ------ |

### Skipped (Low Severity)
| Package | Advisory | Summary |
| ------- | -------- | ------- |

### Failed/Requires Manual Review
| Package | Advisory | Reason |
| ------- | -------- | ------ |

### Next Steps
- [ ] Review and merge PR
- [ ] Consider addressing low-severity issues in future sprint
- [ ] Monitor for new advisories
```

For low severity follow-up, ask the user: fix now, create tracking issue, ignore, or review individually.

## Advanced Scenarios

For monorepo handling, partial success recovery, lockfile corruption, and already-fixed dismissal workflows, see `references/error-recovery.md`.

## Notes

- Always verify the repo has a GitHub remote before starting
- Check `gh auth status` if API calls fail
- Prefer minimal changes — don't refactor or "improve" unrelated code
- Keep detailed notes of what was attempted for the summary
- If in doubt, ask the user rather than making assumptions
