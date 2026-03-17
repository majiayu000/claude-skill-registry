---
name: sast-semgrep
description: >
  Static application security testing (SAST) using Semgrep for vulnerability detection,
  security code review, and secure coding guidance with OWASP and CWE framework mapping.
  Use when: (1) Scanning code for security vulnerabilities across multiple languages,
  (2) Performing security code reviews with pattern-based detection, (3) Integrating
  SAST checks into CI/CD pipelines, (4) Providing remediation guidance with OWASP Top 10
  and CWE mappings, (5) Creating custom security rules for organization-specific patterns,
  (6) Analyzing dependencies for known vulnerabilities.
version: 0.1.0
maintainer: SirAppSec
category: appsec
tags: [sast, semgrep, vulnerability-scanning, code-security, owasp, cwe, security-review]
frameworks: [OWASP, CWE, SANS-25]
dependencies:
  python: ">=3.8"
  packages: [semgrep]
  tools: [git]
references:
  - https://semgrep.dev/docs/
  - https://owasp.org/Top10/
  - https://cwe.mitre.org/
---

# SAST with Semgrep

## Overview

Perform comprehensive static application security testing using Semgrep, a fast, open-source
static analysis tool. This skill provides automated vulnerability detection, security code
review workflows, and remediation guidance mapped to OWASP Top 10 and CWE standards.

## Quick Start

Scan a codebase for security vulnerabilities:

```bash
semgrep --config=auto --severity=ERROR --severity=WARNING /path/to/code
```

Run with OWASP Top 10 ruleset:

```bash
semgrep --config="p/owasp-top-ten" /path/to/code
```

## Core Workflows

### Workflow 1: Initial Security Scan

1. Identify the primary languages in the codebase
2. Run `scripts/semgrep_scan.py` with appropriate rulesets
3. Parse findings and categorize by severity (CRITICAL, HIGH, MEDIUM, LOW)
4. Map findings to OWASP Top 10 and CWE categories
5. Generate prioritized remediation report

### Workflow 2: Security Code Review

1. For pull requests or commits, run targeted scans on changed files
2. Use `semgrep --diff` to scan only modified code
3. Flag high-severity findings as blocking issues
4. Provide inline remediation guidance from `references/remediation_guide.md`
5. Link findings to secure coding patterns

### Workflow 3: Custom Rule Development

1. Identify organization-specific security patterns to detect
2. Create custom Semgrep rules in YAML format using `assets/rule_template.yaml`
3. Test rules against known vulnerable code samples
4. Integrate custom rules into CI/CD pipeline
5. Document rules in `references/custom_rules.md`

### Workflow 4: CI/CD Integration

1. Add Semgrep to CI/CD pipeline using `assets/ci_config_examples/`
2. Configure baseline scanning for pull requests
3. Set severity thresholds (fail on CRITICAL/HIGH)
4. Generate SARIF output for security dashboards
5. Track metrics: vulnerabilities found, fix rate, false positives

## Security Considerations

- **Sensitive Data Handling**: Semgrep scans code locally; ensure scan results don't leak
  secrets or proprietary code patterns. Use `--max-lines-per-finding` to limit output.

- **Access Control**: Semgrep scans require read access to source code. Restrict scan
  result access to authorized security and development teams.

- **Audit Logging**: Log all scan executions with timestamps, user, commit hash, and
  findings count for compliance auditing.

- **Compliance**: SAST scanning supports SOC2, PCI-DSS, and GDPR compliance requirements.
  Maintain scan history and remediation tracking.

- **Safe Defaults**: Use `--config=auto` for balanced detection. For security-critical
  applications, use `--config="p/security-audit"` for comprehensive coverage.

## Language Support

Semgrep supports 30+ languages including:
- **Web**: JavaScript, TypeScript, Python, Ruby, PHP, Java, C#, Go
- **Mobile**: Swift, Kotlin, Java (Android)
- **Infrastructure**: Terraform, Dockerfile, YAML, JSON
- **Other**: C, C++, Rust, Scala, Solidity

## Bundled Resources

### Scripts

- `scripts/semgrep_scan.py` - Full-featured scanning with OWASP/CWE mapping and reporting
- `scripts/baseline_scan.sh` - Quick baseline scan for CI/CD
- `scripts/diff_scan.sh` - Scan only changed files (for PRs)

### References

- `references/owasp_cwe_mapping.md` - OWASP Top 10 to CWE mapping with Semgrep rules
- `references/remediation_guide.md` - Vulnerability remediation patterns by category
- `references/rule_library.md` - Curated list of useful Semgrep rulesets

### Assets

- `assets/rule_template.yaml` - Template for creating custom Semgrep rules
- `assets/ci_config_examples/` - CI/CD integration examples (GitHub Actions, GitLab CI)
- `assets/semgrep_config.yaml` - Recommended Semgrep configuration

## Common Patterns

### Pattern 1: Daily Security Baseline Scan

```bash
# Run comprehensive scan and generate report
scripts/semgrep_scan.py --config security-audit \
  --output results.json \
  --format json \
  --severity HIGH CRITICAL
```

### Pattern 2: Pull Request Security Gate

```bash
# Scan only changed files, fail on HIGH/CRITICAL
scripts/diff_scan.sh --fail-on high \
  --base-branch main \
  --output sarif
```

### Pattern 3: Vulnerability Research

```bash
# Search for specific vulnerability patterns
semgrep --config "r/javascript.lang.security.audit.xss" \
  --json /path/to/code | jq '.results'
```

### Pattern 4: Custom Rule Validation

```bash
# Test custom rule against vulnerable samples
semgrep --config assets/custom_rules.yaml \
  --test tests/vulnerable_samples/
```

## Integration Points

### CI/CD Integration

- **GitHub Actions**: Use `semgrep/semgrep-action@v1` with SARIF upload
- **GitLab CI**: Run as security scanning job with artifact reports
- **Jenkins**: Execute as build step with quality gate integration
- **pre-commit hooks**: Run lightweight scans on staged files

See `assets/ci_config_examples/` for ready-to-use configurations.

### Security Tool Integration

- **SIEM/SOAR**: Export findings in JSON/SARIF for ingestion
- **Vulnerability Management**: Integrate with Jira, DefectDojo, or ThreadFix
- **IDE Integration**: Use Semgrep IDE plugins for real-time detection
- **Secret Scanning**: Combine with tools like trufflehog, gitleaks

### SDLC Integration

- **Requirements Phase**: Define security requirements and custom rules
- **Development**: IDE plugins provide real-time feedback
- **Code Review**: Automated security review in PR workflow
- **Testing**: Integrate with security testing framework
- **Deployment**: Final security gate before production

## Severity Classification

Semgrep findings are classified by severity:

- **CRITICAL**: Exploitable vulnerabilities (SQLi, RCE, Auth bypass)
- **HIGH**: Significant security risks (XSS, CSRF, sensitive data exposure)
- **MEDIUM**: Security weaknesses (weak crypto, missing validation)
- **LOW**: Code quality issues with security implications
- **INFO**: Security best practice recommendations

## Performance Optimization

For large codebases:

```bash
# Use --jobs for parallel scanning
semgrep --config auto --jobs 4

# Exclude vendor/test code
semgrep --config auto --exclude "vendor/" --exclude "test/"

# Use lightweight rulesets for faster feedback
semgrep --config "p/owasp-top-ten" --exclude-rule "generic.*"
```

## Troubleshooting

### Issue: Too Many False Positives

**Solution**:
- Use `--exclude-rule` to disable noisy rules
- Create `.semgrepignore` file to exclude false positive patterns
- Tune rules using `--severity` filtering
- Add `# nosemgrep` comments for confirmed false positives (with justification)

### Issue: Scan Taking Too Long

**Solution**:
- Use `--exclude` for vendor/generated code
- Increase `--jobs` for parallel processing
- Use targeted rulesets instead of `--config=auto`
- Run incremental scans with `--diff`

### Issue: Missing Vulnerabilities

**Solution**:
- Use comprehensive rulesets: `p/security-audit` or `p/owasp-top-ten`
- Consult `references/rule_library.md` for specialized rules
- Create custom rules for organization-specific patterns
- Combine with dynamic analysis (DAST) and dependency scanning

## Advanced Usage

### Creating Custom Rules

See `references/rule_library.md` for guidance on writing effective Semgrep rules.
Use `assets/rule_template.yaml` as a starting point.

Example rule structure:
```yaml
rules:
  - id: custom-sql-injection
    patterns:
      - pattern: execute($QUERY)
      - pattern-inside: |
          $QUERY = $USER_INPUT + ...
    message: Potential SQL injection from user input concatenation
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-89"
      owasp: "A03:2021-Injection"
```

### OWASP Top 10 Coverage

This skill provides detection for all OWASP Top 10 2021 categories.
See `references/owasp_cwe_mapping.md` for complete coverage matrix.

## Best Practices

1. **Baseline First**: Establish security baseline before enforcing gates
2. **Progressive Rollout**: Start with HIGH/CRITICAL, expand to MEDIUM over time
3. **Developer Training**: Educate team on common vulnerabilities and fixes
4. **Rule Maintenance**: Regularly update rulesets and tune for your stack
5. **Metrics Tracking**: Monitor vulnerability trends, MTTR, and false positive rate
6. **Defense in Depth**: Combine with DAST, SCA, and manual code review

## References

- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Semgrep Rule Registry](https://semgrep.dev/explore)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)
