---
name: snyk
description: Snyk security scanning for dependencies. Use for vulnerability scanning.
---

# Snyk

Snyk is a developer security platform. It finds and fixes vulnerabilities in your code (SAST), open source dependencies (SCA), container images, and infrastructure as code (IaC).

## When to Use

- **Dependency Checking**: "Does `lodash` have a vulnerability?" (SCA).
- **Container Security**: Scanning your Dockerfile base image for CVEs.
- **IDE Integration**: Real-time feedback in VS Code / IntelliJ while you code.

## Quick Start

```bash
# Install CLI
npm install -g snyk

# Authenticate
snyk auth

# Test dependencies
snyk test

# Monitor (Continuous watching for new vulns)
snyk monitor
```

## Core Concepts

### Vulnerability Database

Snyk maintains a proprietary DB (Intel) that often alerts faster than the public NVD.

### Fix PRs

Snyk can automatically open a Pull Request to upgrade a vulnerable dependency to the patched version.

### Reachability Analysis

Determines if a vulnerable function in a library is _actually called_ by your code. prioritization.

## Best Practices (2025)

**Do**:

- **Enable Snyk in CI**: Fail the build if `High` or `Critical` vulnerabilities are introduced.
- **Use Snyk Code**: For SAST (finding bugs in your own code).
- **Prioritize Reachable Vulns**: Don't waste time patching libraries you don't even use the dangerous part of.

**Don't**:

- **Don't Ignore Low Severity**: Bulk triage them, but don't let them accumulate forever ("Death by a thousand cuts").
- **Don't blindly upgrade**: Verify breaking changes. Snyk usually warns about this.

## Troubleshooting

| Error             | Cause                  | Solution                                                            |
| :---------------- | :--------------------- | :------------------------------------------------------------------ |
| `Auth Failed`     | Token expired/missing. | Run `snyk auth` again or set `SNYK_TOKEN` env var.                  |
| `Too many issues` | Legacy codebase.       | Use `.snyk` file to ignore known/wont-fix issues or set a baseline. |

## References

- [Snyk Documentation](https://docs.snyk.io/)
- [Snyk CLI](https://docs.snyk.io/snyk-cli)
