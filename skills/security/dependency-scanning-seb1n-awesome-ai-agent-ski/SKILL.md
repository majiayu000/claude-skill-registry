---
name: dependency-scanning
description: Scan project dependencies for known vulnerabilities, generate software bills of materials, and enforce license compliance across the software supply chain. Use when the user requests dependency scanning or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Dependency Scanning

This skill enables the agent to analyze a project's direct and transitive dependencies for known security vulnerabilities, outdated packages, and license compliance issues. The agent parses manifest and lock files, queries vulnerability databases (NVD, GitHub Advisory, OSV), produces structured reports with CVE identifiers and remediation guidance, and can generate a Software Bill of Materials (SBOM) in standard formats.

## Workflow

1. **Detect Package Ecosystem and Manifest Files** — Identify the project's language ecosystem by locating dependency manifests such as `package.json` and `package-lock.json` (Node.js), `requirements.txt` and `Pipfile.lock` (Python), `pom.xml` or `build.gradle` (Java), `go.sum` (Go), or `Gemfile.lock` (Ruby). Detect monorepo structures with multiple manifests.

2. **Resolve the Full Dependency Tree** — Parse lock files to build the complete dependency graph including transitive dependencies. Identify dependency depth, shared sub-dependencies, and version constraints. Flag phantom dependencies that are used in code but missing from the manifest.

3. **Scan Against Vulnerability Databases** — Query the National Vulnerability Database (NVD), GitHub Advisory Database, and OSV for each resolved package and version. Match results by CPE or PURL identifier. Record CVE IDs, CVSS scores, severity levels, affected version ranges, and fixed versions where available.

4. **Assess License Compliance** — Extract the declared license for each dependency and compare it against the project's license policy. Flag copyleft licenses (GPL, AGPL) in proprietary projects, identify packages with no declared license, and detect license conflicts between direct and transitive dependencies.

5. **Generate SBOM and Vulnerability Report** — Produce a Software Bill of Materials in CycloneDX or SPDX format. Generate a vulnerability report sorted by severity, including CVE identifiers, affected dependency paths, available fix versions, and whether the vulnerable code path is reachable.

6. **Recommend and Apply Fixes** — Suggest the minimum version upgrades required to resolve vulnerabilities without breaking changes. Where possible, generate updated manifest and lock files automatically. Flag cases where no fix is available and suggest alternative packages or workarounds.

## Supported Technologies

- **Node.js**: npm audit, yarn audit, Snyk, Dependabot
- **Python**: pip-audit, Safety, Snyk, Dependabot
- **Java**: OWASP Dependency-Check, Snyk, Maven Enforcer Plugin
- **Go**: govulncheck, Nancy, Snyk
- **Containers**: Trivy, Grype (scan OS packages and application dependencies inside images)
- **SBOM Formats**: CycloneDX (JSON/XML), SPDX (JSON/Tag-Value)
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins, CircleCI

## Usage

Provide the agent with the path to a project directory or a specific manifest file. Optionally specify a license policy or target compliance standard. The agent will perform a full scan and deliver a prioritized vulnerability report.

**Prompt example:**

```
Scan the Node.js project in /app for dependency vulnerabilities. Generate a CycloneDX SBOM and flag any GPL-licensed transitive dependencies.
```

## Examples

### Example 1: Scanning a Node.js Project

**Command:**

```bash
npm audit --json > audit-report.json
```

**Vulnerability Report (excerpt):**

| # | Severity | Package | Installed | Fixed In | CVE | Dependency Path |
|---|----------|---------|-----------|----------|-----|-----------------|
| 1 | Critical | `jsonwebtoken` | 8.5.1 | 9.0.0 | CVE-2022-23529 | direct |
| 2 | High | `minimatch` | 3.0.4 | 3.0.5 | CVE-2022-3517 | express > send > mime > minimatch |
| 3 | High | `qs` | 6.5.2 | 6.5.3 | CVE-2022-24999 | express > qs |
| 4 | Medium | `semver` | 5.7.1 | 5.7.2 | CVE-2022-25883 | nodemon > semver |
| 5 | Low | `cookie` | 0.4.1 | 0.4.2 | CVE-2024-47764 | express > cookie |

**Auto-generated fix in `package.json`:**

```json
{
  "dependencies": {
    "jsonwebtoken": "^9.0.0",
    "express": "^4.19.2"
  },
  "overrides": {
    "minimatch": "3.0.5",
    "semver": "5.7.2"
  }
}
```

### Example 2: Scanning a Python Project with pip-audit

**Command:**

```bash
pip-audit -r requirements.txt --format json --output audit.json --fix --dry-run
```

**Vulnerability Report (excerpt):**

| # | Severity | Package | Installed | Fixed In | CVE | Description |
|---|----------|---------|-----------|----------|-----|-------------|
| 1 | Critical | `cryptography` | 38.0.0 | 41.0.6 | CVE-2023-49083 | NULL pointer dereference when loading PKCS7 certificates |
| 2 | High | `requests` | 2.28.0 | 2.31.0 | CVE-2023-32681 | Leaking Proxy-Authorization header to redirected hosts |
| 3 | High | `Jinja2` | 3.1.1 | 3.1.3 | CVE-2024-22195 | Cross-site scripting via xmlattr filter |
| 4 | Medium | `setuptools` | 65.0.0 | 70.0.0 | CVE-2024-6345 | Remote code execution via download functions |

**Auto-generated `requirements.txt` (fixed):**

```
cryptography==41.0.6    # was 38.0.0 — fixes CVE-2023-49083
requests==2.31.0        # was 2.28.0 — fixes CVE-2023-32681
Jinja2==3.1.3           # was 3.1.1 — fixes CVE-2024-22195
setuptools>=70.0.0      # was 65.0.0 — fixes CVE-2024-6345
Flask==3.0.0
gunicorn==21.2.0
```

## Best Practices

- **Scan on every CI build** — integrate dependency scanning into CI pipelines so that new vulnerabilities are caught before code is merged, not after deployment.
- **Pin dependencies and use lock files** — reproducible builds with lock files ensure that the exact versions scanned in CI are the same versions deployed to production.
- **Monitor transitive dependencies** — over 80% of vulnerabilities in typical projects come from transitive dependencies. Always resolve and scan the full dependency tree, not just direct dependencies.
- **Automate update PRs** — use Dependabot, Renovate, or Snyk to automatically open pull requests when fix versions become available, reducing the window of exposure.
- **Maintain a license allow-list** — define an approved license list (e.g., MIT, Apache-2.0, BSD) and block builds that introduce dependencies with disallowed licenses.
- **Generate SBOMs for every release** — store CycloneDX or SPDX SBOMs alongside release artifacts to support supply chain transparency and incident response.

## Safety Boundaries

- Work only on systems the user owns or is explicitly authorized to assess, and record the approved scope before testing.
- Start with passive or read-only inspection. Obtain explicit approval before active scanning, exploitation, load generation, or disruptive remediation.
- Never expose secrets, extract unrelated data, weaken production controls, or expand beyond the approved targets.
- Preserve evidence, minimize impact, stop on instability, and provide rollback or containment steps for every material change.

## Edge Cases

- **Vulnerabilities with no available fix** — when a CVE exists but no patched version is released, assess whether the vulnerable code path is reachable in your application. If it is, consider replacing the dependency or applying a local patch.
- **Monorepos with mixed ecosystems** — a single repository may contain Node.js, Python, and Go services with separate manifests. Scan each ecosystem independently and produce a unified report.
- **Private registries and internal packages** — packages hosted on private npm registries or internal PyPI servers will not appear in public vulnerability databases. Maintain a private advisory feed or scan internal packages with tools like Trivy that support custom data sources.
- **Version conflicts from overrides** — forcing a transitive dependency to a newer version via npm `overrides` or pip `constraints` can introduce runtime incompatibilities. Always run the test suite after applying automated fixes.
- **Archived or unmaintained dependencies** — a package may have no known CVEs but also no active maintainer. Treat unmaintained packages as a supply chain risk and plan migration to actively maintained alternatives.
