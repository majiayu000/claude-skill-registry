---
name: npm-supply-chain-check
description: Detect known malicious npm package versions and install-time supply-chain indicators in repositories, lockfiles, and node_modules. Use when a user mentions an npm compromise, Shai-Hulud, the Keyv/cacheable incident, suspicious preinstall scripts, credential-stealing packages, or asks whether a JavaScript project was exposed to a package supply-chain attack. Do not use as a general CVE or license audit.
---

# NPM Supply Chain Check

Run an evidence-bounded, read-only scan. Distinguish a dependency reference from
proof that malicious code executed, and never read or print secret values.

## Workflow

### 1. Fix the scan boundary

Resolve the exact repository or directory first. Default to the current
repository only. Do not silently expand a repo scan to the user's home directory,
all worktrees, global package caches, or CI systems.

### 2. Check intelligence freshness

Read `references/shai-hulud-2026-iocs.json` when investigating that incident.
It is a dated minimum baseline, not a complete list of every affected community
package. For an active incident, also check current primary sources such as the
npm registry and maintainer/security advisories before declaring a version safe.
Do not modify the bundled baseline during an ordinary scan.

### 3. Run the deterministic scanner

From this skill directory:

```bash
python3 scripts/scan_npm_supply_chain.py <target> --format text
```

Use JSON when another tool will consume the result:

```bash
python3 scripts/scan_npm_supply_chain.py <target> --format json
```

Add `--deep` only when source and built JavaScript files should also be searched
for network and campaign strings. Deep mode still reports paths and indicators,
not surrounding file contents.

Exit codes are machine-checkable:

- `0`: scan completed and found no indicators in the checked scope.
- `1`: one or more affected versions or suspicious indicators were found.
- `2`: the scan could not complete because its target or IOC data was invalid.

### 4. Classify the evidence

| Evidence | Meaning |
|---|---|
| Affected version in a manifest or lockfile | Exposure candidate; it does not prove installation or execution. |
| Affected version under `node_modules` | Malicious package content may have been present locally. |
| Known malicious SHA-256 | High-confidence local artifact match. |
| IOC preinstall command or campaign/network string | Strong suspicious-content evidence; inspect provenance and timing. |
| IOC filename with a different hash | Triage lead only; filenames such as `setup.mjs` can be legitimate. |
| No findings | No known indicators in this scope and baseline; not proof of a clean machine. |

Correlate positive results with installation timestamps, CI run history, package
manager logs, and the incident exposure window. Do not claim credential theft
solely from a lockfile match.

## Operating Contract

Direct actions: Run read-only local scans, inspect public advisories and registry
metadata, and report exact package, version, path, indicator, scope, and
confidence. For a positive result, recommend pausing installs and affected CI
jobs, isolating suspect runners or machines, preserving logs, and rotating
potentially exposed credentials from a known-clean device.

Escalate before: Ask for explicit authorization before any action that would:

- delete `node_modules`, caches, logs, or suspicious files;
- reinstall dependencies or regenerate lockfiles;
- revoke or rotate npm, GitHub, cloud, Kubernetes, Vault, payment, or chat tokens;
- upload local artifacts or secret-bearing logs to a third party.

Those actions change evidence or external state and require explicit user
authorization. If asked to remediate, make a reversible evidence copy or record
hashes first and name the exact target before changing it.

Evidence-backed pushback: When a user proposes only upgrading or reinstalling
after strong local execution evidence, explain that package replacement does not
revoke credentials that may already have been copied. Ground that warning in the
scanner finding and the credential classes targeted by the current incident
source.

Feedback loop: When a new affected package, version, hash, or stable IOC is
confirmed by a credible source, update the JSON baseline and add a regression
fixture before treating the detector as current.

## Gotchas

- npm unpublishing prevents new downloads but does not remove local installs,
  package-manager caches, container layers, or CI artifacts.
- Valid npm provenance proves how a package was published, not that the source
  repository or maintainer account was uncompromised.
- Floating declarations such as `latest` do not prove which historical version
  was installed. Prefer lockfiles, installed manifests, and install logs.
- Transitive packages may be absent from the root `package.json`; scan the
  lockfile and `node_modules` when available.
- Binary `bun.lockb` files are reported as unsupported rather than silently
  treated as clean. Use a text lockfile or Bun tooling to resolve exact versions.
- The bundled IOC list is intentionally source-attributed and dated. Extend it
  through a reviewed data update, not an invented fallback.

## Report

Return:

```markdown
## NPM Supply-Chain Check
- scope: <absolute target>
- baseline: <incident and updated_at>
- result: clean | suspicious | affected | incomplete
- confidence: low | medium | high

## Findings
- <severity> <path> - <package/version or IOC and what it proves>

## Limits
- <missing lockfile, unsupported binary lock, stale baseline, or unchecked external scope>

## Next Actions
1. <smallest safe action>
```

The check is done only when a fresh scanner result is available, all warnings
are surfaced, and conclusions stay within the scanned target and IOC baseline.

## Resources

- `scripts/scan_npm_supply_chain.py`: read-only repository, lockfile,
  `node_modules`, preinstall, filename, hash, and optional deep-string scanner.
- `references/shai-hulud-2026-iocs.json`: dated machine-readable baseline for
  the August 2026 Keyv/cacheable Shai-Hulud incident.
