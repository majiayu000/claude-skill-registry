---
name: deps
description: Audit and upgrade project dependencies — check for vulnerabilities and outdated packages
disable-model-invocation: true
---

Audit and manage project dependencies: $ARGUMENTS

If no specific action requested, run the full audit.

## Step 1 — Read Current Dependencies
Read the requirements file. List all packages with their current version constraints.

## Step 2 — Check Installed Versions
```bash
# List installed packages (use the package manager from project config)
# Example: pip list, npm list, go list, cargo tree, etc.
```
Compare installed versions against requirements constraints.

## Step 3 — Vulnerability Scan
```bash
# Run the dependency audit command (see project config)
```
Report any known CVEs with severity, affected package, and fixed version.

## Step 4 — Check for Outdated Packages
```bash
# Run the outdated packages command (see project config)
```
For each outdated package, report:
- Current version
- Latest version
- Whether the update is a major/minor/patch bump
- Risk assessment (major bumps may have breaking changes)

## Step 5 — Compatibility Check
For any proposed upgrades:
- Check if the new version supports the project's language version (see stack concepts)
- Check for known incompatibilities between upgraded packages
- Verify framework version compatibility

## Step 6 — Apply Upgrades (if requested)
If user asked to upgrade:
1. Update version constraints in the requirements file
2. Install updated packages
3. Run the test and type-check commands (see project config)
4. If tests fail after upgrade, identify which package caused the failure and roll back that specific upgrade

## Output Format
```
DEPENDENCY AUDIT
════════════════

Vulnerabilities:  X found (Critical: X, High: X, Medium: X)
Outdated:         X packages
Up to date:       X packages

VULNERABILITIES:
  [CRITICAL] package==version — CVE-XXXX-XXXX — description — fix: upgrade to X.Y.Z

OUTDATED:
  package      current → latest   (patch/minor/major)

RECOMMENDATION: <upgrade commands or "all clear">
```