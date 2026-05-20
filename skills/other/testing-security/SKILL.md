---
name: testing-security
cluster: testing
description: "Security test: DAST OWASP ZAP/Nuclei, SAST Semgrep/Bandit, Snyk/Trivy, detect-secrets/TruffleHog"
tags: ["security-test","dast","sast","snyk","testing"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "security test dast sast sca snyk trivy secrets scanning zap nuclei"
---

# testing-security

## Purpose
This skill automates security testing by integrating DAST tools (OWASP ZAP, Nuclei), SAST tools (Semgrep, Bandit), SCA tools (Snyk, Trivy), and secrets scanners (detect-secrets, TruffleHog) to identify vulnerabilities in code, applications, and secrets.

## When to Use
Use this skill during CI/CD pipelines, before deployments, or for periodic audits; ideal for projects with web apps, APIs, or codebases in languages like Python, Java, or JavaScript where security flaws could lead to breaches.

## Key Capabilities
- DAST: Run OWASP ZAP for active scanning of web apps, detecting issues like XSS or SQLi; use Nuclei for custom vulnerability templates.
- SAST: Execute Semgrep for pattern-based code analysis (e.g., YAML rulesets) or Bandit for Python-specific flaws like insecure imports.
- SCA: Leverage Snyk to scan dependencies for known CVEs via SBOM analysis; use Trivy for container image scanning with vulnerability databases.
- Secrets Detection: Apply detect-secrets to scan files for patterns like API keys; use TruffleHog for Git history scans to find exposed secrets.
- Integration: Combine tools in a single workflow, e.g., run SAST on code changes and DAST on staging environments.

## Usage Patterns
Always configure tools via environment variables for authentication (e.g., `$ZAP_API_KEY` for OWASP ZAP, `$SNYK_TOKEN` for Snyk). Start with a baseline scan on new projects, then automate in scripts.

- Pattern 1: For CI/CD, trigger SAST on pull requests and DAST on builds; example: Use GitHub Actions to run Semgrep on diffed files.
- Pattern 2: For local testing, chain tools sequentially—first run Trivy on Docker images, then Nuclei on URLs.
- Example 1: To scan a Python repo for SAST and secrets: Install tools, run Bandit on files, then detect-secrets; output results to a JSON report for parsing.
- Example 2: For a web app, perform DAST: Start OWASP ZAP in daemon mode, use `zap-cli` to scan a URL, and follow with Nuclei for specific exploits.

## Common Commands/API
Use these exact commands in scripts or terminals; ensure dependencies are installed (e.g., via pip or Docker).

- OWASP ZAP (DAST): Start with `zap.sh -daemon -port 8080`, then scan via `zap-cli -p 8080 quick-scan --spider https://target.com --report html`. API endpoint: POST to `/JSON/core/action/newSession/` with `$ZAP_API_KEY`.
- Nuclei (DAST): Run `nuclei -t templates/ -u https://target.com -o results.txt`; use config file like `nuclei-config.yaml` with severity levels.
- Semgrep (SAST): Execute `semgrep --config p/default --lang python .`; customize with a `.semgrep.yml` file: `rules: - id: no-os-system patterns: - pattern: os.system(...)`.
- Bandit (SAST): Command: `bandit -r /path/to/code -f json`; ignore paths via `-x tests/`.
- Snyk (SCA): Authenticate with `$SNYK_TOKEN`, then `snyk test --file=requirements.txt`; API: GET `https://snyk.io/api/v1/org/{orgId}/projects` for project lists.
- Trivy (SCA): Scan image: `trivy image myimage:latest --exit-code 1 --severity CRITICAL`; config via `.trivy.yaml` with `ignoreUnfixed: true`.
- detect-secrets (Secrets): Run `detect-secrets scan > .secrets.baseline`; use with Git hook: `detect-secrets hook --baseline .secrets.baseline`.
- TruffleHog (Secrets): Command: `trufflehog git https://github.com/repo --since-commit HEAD~1`; filter with `--regex` for patterns.

## Integration Notes
Integrate via scripts or orchestration tools like Jenkins or GitHub Actions; pass outputs as JSON for chaining. For auth, set env vars like `$TRIVY_USERNAME` and `$TRIVY_PASSWORD`. Use Docker images (e.g., `owasp/zap2docker-stable`) for isolated runs. Config formats: YAML for Semgrep rules (e.g., `{ patterns: [pattern: "regex"] }`), JSON for Snyk reports. Ensure tools are version-pinned (e.g., Semgrep v0.100.0) to avoid breaking changes.

## Error Handling
Check exit codes after each command (e.g., Semgrep returns non-zero on findings); parse errors from stdout, like OWASP ZAP's JSON responses for "error" keys. Common issues: Network errors in DAST—retry with `zap-cli --retries 3`; authentication failures—verify env vars (e.g., if `$SNYK_TOKEN` is invalid, output "Auth error"). Log all outputs to files and handle via try-catch in scripts, e.g., in Bash: `zap-cli quick-scan || echo "Scan failed: $?" >> error.log`. For API calls, check HTTP status codes (e.g., 401 for unauthorized).

## Graph Relationships
- Related to: "testing" cluster (e.g., links to unit-testing or integration-testing skills for combined workflows).
- Depends on: OWASP ZAP for DAST, Semgrep for SAST.
- Integrates with: Snyk API for SCA, TruffleHog for secrets in version control systems.
