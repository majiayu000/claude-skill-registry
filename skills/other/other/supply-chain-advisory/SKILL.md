---
name: supply-chain-advisory
description: 'Supply chain security patterns for dependency management: known-bad version
  detection, incident response, lockfile auditing, and artifact scanning.
  Do not use for general CVE triage unrelated to dependency supply chain.'
version: 1.9.3
alwaysApply: false
category: infrastructure
tags:
- security
- supply-chain
- dependencies
- vulnerability
- pypi
dependencies:
- error-patterns
provides:
  infrastructure:
  - supply-chain-scanning
  - dependency-auditing
  - incident-response
  patterns:
  - known-bad-detection
  - lockfile-audit
  - artifact-scanning
usage_patterns:
- dependency-security-check
- incident-response
- supply-chain-audit
complexity: intermediate
model_hint: standard
estimated_tokens: 500
progressive_loading: true
modules:
- modules/scanning-patterns.md
- modules/incident-response.md
role: hook-target
---

## Overview

Supply chain attacks bypass traditional code review by compromising upstream
dependencies. This skill provides patterns for detecting, preventing, and
responding to compromised packages in Python ecosystems.

## When To Use

- After a supply chain advisory is published
- When auditing dependencies for a new or existing project
- During incident response for a suspected compromise
- When adding the SessionStart hook to a project

## When NOT To Use

- General CVE triage unrelated to dependency supply chain
- Application-level vulnerability scanning (use a SAST tool)
- License compliance audits (different concern)

## Known-Bad Versions Blocklist

The blocklist lives at `${CLAUDE_SKILL_DIR}/known-bad-versions.json`.
It is consumed by:

1. **SessionStart hook** — warns per-session when compromised versions detected
2. **`make supply-chain-scan`** — CI/local scanning target
3. **This skill** — manual audit guidance

### Blocklist Format

```json
{
  "package_name": [{
    "versions": ["x.y.z"],
    "date": "YYYY-MM-DD",
    "description": "What the attack did",
    "indicators": ["files or patterns to search for"],
    "source": "advisory URL",
    "severity": "critical|high|medium"
  }]
}
```

### Adding a New Entry

1. Add the entry to `${CLAUDE_SKILL_DIR}/known-bad-versions.json`
2. Add version exclusions (`!=x.y.z`) to affected `pyproject.toml` files
3. Document in `docs/dependency-audit.md` under Supply Chain Incidents
4. Run `make supply-chain-scan` to verify detection works

## Quick Scan Commands

### Check all lockfiles on machine for known-bad versions

```bash
# Scan uv.lock files for a specific compromised version
grep -r "package_name.*version" --include="uv.lock" /path/to/projects

# Search for malicious artifacts
find /path/to/projects -name "suspicious_file.pth" 2>/dev/null

# Check installed versions in virtualenvs
find /path/to/projects -path "*/.venv/lib/*/PACKAGE*/METADATA" \
  -exec grep "^Version:" {} +
```

### Verify lockfile hash integrity

`uv.lock` includes SHA256 hashes for every package. If a package is
re-published with different content under the same version, `uv sync`
will fail with a hash mismatch. This is your strongest automatic defense.

## Defense Layers

| Layer | Tool | Catches |
|-------|------|---------|
| **Lockfile hashes** | uv.lock SHA256 | Tampered re-published versions |
| **Version exclusions** | pyproject.toml `!=` | Known-bad versions on fresh resolve |
| **SessionStart hook** | sanctum hook | Per-session warning for compromised deps |
| **CI scanning** | OSV + Safety | CVE database + advisory matching |
| **Artifact scanning** | make supply-chain-scan | Malicious files (.pth, scripts) |

## Limitations

- Zero-day supply chain attacks have no prior advisory — lockfile hashes
  are the only automatic defense during the attack window
- Safety/CVE databases lag behind real-world compromises
- OSV provides broader coverage but is still reactive
