---
name: mac-audit
description: Comprehensive macOS development environment health check. Detects brew drift, orphaned packages, security issues, version mismatches, and deferred cleanup readiness.
argument-hint: "[--section <name>] [--deferred-only]"
allowed-tools: Bash, Read, Glob, Grep
---

## Purpose

Audit the macOS development environment for drift, security issues, and cleanup opportunities. Compares current state against the declared Brewfile and AUDIT.md project requirements. Produces a markdown report with pass/warn/fail indicators.

Run quarterly (or after major environment changes) to catch drift before it accumulates.

## Arguments

- No arguments — run all 8 checks
- `--section <name>` — run only one section (brew-drift, orphans, security, versions, services, disk, shell, deferred)
- `--deferred-only` — only check deferred item readiness (quick check)

## Configuration paths

```
BREWFILE=~/Developer/projects/macbook-clean/Brewfile
AUDIT_MD=~/Developer/projects/macbook-clean/AUDIT.md
```

## Output format

Print a markdown report with a timestamp header and sections for each category. Use these indicators:

- `PASS` — healthy, no action needed
- `WARN` — not broken but worth investigating
- `FAIL` — needs attention

Example:

```markdown
## Mac Environment Audit — 2026-02-12

### 1. Brew Drift
- PASS: 0 formulae installed but not in Brewfile
- WARN: 2 formulae in Brewfile but not installed (postgresql@16, gitleaks)
```

## Checks to perform

Run each check inline using Bash commands. Do NOT create or depend on external scripts — keep the skill self-contained.

---

### 1. Brew Drift

**Goal:** Detect packages that have been installed ad-hoc (not declared in Brewfile) or declared but missing.

Steps:

1. Read the Brewfile at `~/Developer/projects/macbook-clean/Brewfile`
2. Extract all formula names (lines starting with `brew "`) and cask names (lines starting with `cask "`)
3. Run `brew leaves` to get currently installed top-level formulae
4. Run `brew list --cask` to get installed casks
5. Compare:
   - **Installed but not in Brewfile** — potential orphans or undeclared additions
   - **In Brewfile but not installed** — missing tools (maybe not yet installed, or removed accidentally)
6. Run `brew bundle check --file=~/Developer/projects/macbook-clean/Brewfile` for the official check
7. Report results with PASS/WARN/FAIL

---

### 2. Orphan Detection

**Goal:** Find formulae that nothing depends on and no project needs.

Steps:

1. For each formula found in check 1 as "installed but not in Brewfile":
   - Run `brew uses --installed <formula>` to see if any installed formula depends on it
   - Cross-reference against known project requirements (Section 8 of AUDIT.md)
2. Flag formulae with **0 dependents AND no project need** as orphan candidates
3. Report each orphan candidate with its status

---

### 3. Security Hygiene

**Goal:** Detect exposed secrets in environment and shell config.

Steps:

1. Run `env | grep -iE 'token|secret|key|password'` and review results
   - Filter out known-safe entries (PATH, HOMEBREW keys, SSH_AUTH_SOCK, etc.)
   - Flag anything that looks like an actual secret value
2. Search `~/.zshrc` for hardcoded credentials:
   - `grep -inE '(token|secret|password|api_key)\s*=' ~/.zshrc`
3. Search `~/.zprofile` for hardcoded credentials:
   - `grep -inE '(token|secret|password|api_key)\s*=' ~/.zprofile`
4. Check for `.env` files outside project directories:
   - `find ~ -maxdepth 2 -name '.env' -not -path '*/Developer/projects/*' -not -path '*/.claude/*' 2>/dev/null`
5. Report PASS if clean, FAIL if secrets found

---

### 4. Version Health

**Goal:** Verify runtime versions match project requirements.

Steps:

1. Check Node.js:
   - `node --version` — should be v22.x (project requirement)
   - `which -a node` — NVM path should come first, should show 1-2 entries (not more)
2. Check Python:
   - `python3 --version` — should be 3.13.x
   - `which -a python3` — should show 1-2 entries (not 4)
3. Check for deprecated Homebrew formulae:
   - `brew info --json=v2 --installed | jq '[.formulae[] | select(.deprecated == true) | .name]'`
4. Check for outdated critical tools:
   - `brew outdated --json=v2 | jq '[.formulae[].name] | length'` — report count
5. Report PASS/WARN/FAIL per runtime

---

### 5. Service Health

**Goal:** Detect services that shouldn't be running, or zombie LaunchAgents.

Steps:

1. Run `brew services list` to get all Homebrew-managed services
2. For each **running** service: check if it has a project need (mongodb-community for hello-mern, postgresql@16 for hello-nean)
3. Flag running services with no project need as WARN
4. Check for LaunchAgent plists that exist but whose service is not running:
   - `ls ~/Library/LaunchAgents/ 2>/dev/null | grep homebrew`
   - Cross-reference against `brew services list` — if a plist exists but service is stopped/error, flag as zombie
5. Report results

---

### 6. Disk Usage

**Goal:** Flag large caches and scattered node_modules.

Steps:

1. Check sizes of key directories (use `du -sh`, suppress errors):
   - `/opt/homebrew`
   - `~/.npm`
   - `~/Library/Caches/Homebrew`
   - `~/Library/Caches/pip`
   - `~/.nvm`
   - `~/.pnpm-store` (if exists)
2. Flag any cache over 1 GB as WARN
3. Check for `node_modules` directories outside `~/Developer/projects/`:
   - `find ~ -maxdepth 4 -name node_modules -type d -not -path '*/Developer/projects/*' -not -path '*/.nvm/*' 2>/dev/null`
4. Report findings with sizes

---

### 7. Shell Config Health

**Goal:** Detect PATH and config issues that cause confusion.

Steps:

1. Check for duplicate PATH entries:
   - `echo $PATH | tr ':' '\n' | sort | uniq -d`
2. Check for non-existent directories in PATH:
   - `echo $PATH | tr ':' '\n' | while read -r d; do [ ! -d "$d" ] && echo "$d"; done`
   - Exclude known Apple system bootstrap paths (`/var/run/com.apple.security.cryptexd/`)
3. Check for duplicate aliases in `~/.zshrc`:
   - `grep '^alias ' ~/.zshrc | awk -F= '{print $1}' | sort | uniq -d`
4. Check if `~/.profile` exists and is empty (pointless file)
5. Check if `~/.bash_profile` exists (leftover from bash)
6. Report PASS/WARN per finding

---

### 8. Deferred Item Readiness

**Goal:** Check whether items deferred during remediation are now safe to remove.

For each deferred item, run the specified check and report status:

| Deferred Item | Condition to Become Safe | Check Command |
|---------------|------------------------|---------------|
| Homebrew `node` | No installed formulae depend on it | `brew uses --installed node` |
| `python@3.14` | semgrep no longer depends on it | `brew uses --installed python@3.14` |
| `icu4c@76` | All dependents removed or upgraded | `brew uses --installed icu4c@76` |
| `icu4c@77` | All dependents removed or upgraded | `brew uses --installed icu4c@77` |
| `postgresql@14` | Data migrated to @16, @14 stopped | Check `brew services list` for @14 stopped AND @16 running |

Report for each item:

- **SAFE TO REMOVE** — condition met, dependents list is empty (or service conditions met)
- **NOT YET** — condition not met; list what still depends on it
- **CHANGED** — dependent count differs from expected baseline (worth investigating)

Expected baselines (from initial audit):
- `node`: 4 dependents (eslint, mongodb-community, mongosh, prettier)
- `python@3.14`: 1 dependent (semgrep)
- `icu4c@76`: 6 dependents (eslint, maven, openjdk, openjdk@11, postgresql@14, prettier)
- `icu4c@77`: 8 dependents (composer, libpq, mysql@8.0, openjdk@17, openjdk@21, opensearch, php, php@8.1)
- `postgresql@14`: running via LaunchAgent

---

## After the audit

1. Present the full report to the user
2. If any FAIL items exist, recommend immediate action
3. If any deferred items show SAFE TO REMOVE, ask if the user wants to proceed with removal
4. If orphan candidates are found, ask if they should be added to the Brewfile (intentional) or uninstalled (not needed)
5. Suggest updating the Brewfile if drift is detected
