---
name: dast-zap
description: >
  Dynamic application security testing (DAST) using OWASP ZAP (Zed Attack Proxy) with passive and active scanning,
  API testing, and OWASP Top 10 vulnerability detection. Use when: (1) Performing runtime security testing of web
  applications and APIs, (2) Detecting vulnerabilities like XSS, SQL injection, and authentication flaws in deployed
  applications, (3) Automating security scans in CI/CD pipelines with Docker containers, (4) Conducting authenticated
  testing with session management, (5) Generating security reports with OWASP and CWE mappings for compliance.
version: 0.1.0
maintainer: SirAppSec
category: appsec
tags: [dast, zap, web-security, owasp, vulnerability-scanning, api-testing, penetration-testing]
frameworks: [OWASP, CWE]
dependencies:
  tools: [docker]
  optional: [python3, java]
references:
  - https://www.zaproxy.org/docs/
  - https://www.zaproxy.org/docs/docker/
  - https://www.zaproxy.org/docs/desktop/start/features/
---

# DAST with OWASP ZAP

## Overview

OWASP ZAP (Zed Attack Proxy) is an open-source DAST tool that acts as a manipulator-in-the-middle proxy to intercept,
inspect, and test web application traffic for security vulnerabilities. ZAP provides automated passive and active
scanning, API testing capabilities, and seamless CI/CD integration for runtime security testing.

## Quick Start

### Baseline Scan (Docker)

Run a quick passive security scan:

```bash
docker run -t zaproxy/zap-stable zap-baseline.py -t https://target-app.com -r baseline-report.html
```

### Full Active Scan (Docker)

Perform comprehensive active vulnerability testing:

```bash
docker run -t zaproxy/zap-stable zap-full-scan.py -t https://target-app.com -r full-scan-report.html
```

### API Scan with OpenAPI Spec

Test APIs using OpenAPI/Swagger specification:

```bash
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable zap-api-scan.py \
  -t https://api.target.com \
  -f openapi \
  -d /zap/wrk/openapi-spec.yaml \
  -r /zap/wrk/api-report.html
```

## Core Workflow

### Step 1: Define Scan Scope and Target

Identify the target application URL and define scope:

```bash
# Set target URL
TARGET_URL="https://target-app.com"

# For authenticated scans, prepare authentication context
# See references/authentication_guide.md for detailed setup
```

**Scope Considerations:**
- Exclude third-party domains and CDN URLs
- Include all application subdomains and API endpoints
- Respect scope limitations in penetration testing engagements

### Step 2: Run Passive Scanning

Execute passive scanning to analyze traffic without active attacks:

```bash
# Baseline scan performs spidering + passive scanning
docker run -t zaproxy/zap-stable zap-baseline.py \
  -t $TARGET_URL \
  -r baseline-report.html \
  -J baseline-report.json
```

**What Passive Scanning Detects:**
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Information disclosure in responses
- Cookie security issues (HttpOnly, Secure flags)
- Basic authentication weaknesses
- Application fingerprinting data

### Step 3: Execute Active Scanning

Perform active vulnerability testing (requires authorization):

```bash
# Full scan includes spidering + passive + active scanning
docker run -t zaproxy/zap-stable zap-full-scan.py \
  -t $TARGET_URL \
  -r full-scan-report.html \
  -J full-scan-report.json \
  -z "-config api.addrs.addr.name=.* -config api.addrs.addr.regex=true"
```

**Active Scanning Coverage:**
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Path Traversal
- Command Injection
- XML External Entity (XXE)
- Server-Side Request Forgery (SSRF)
- Security Misconfigurations

**WARNING:** Active scanning performs real attacks. Only run against applications you have explicit authorization to test.

### Step 4: Test APIs with Specifications

Scan REST, GraphQL, and SOAP APIs:

```bash
# OpenAPI/Swagger API scan
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable zap-api-scan.py \
  -t https://api.target.com \
  -f openapi \
  -d /zap/wrk/openapi.yaml \
  -r /zap/wrk/api-report.html

# GraphQL API scan
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable zap-api-scan.py \
  -t https://api.target.com/graphql \
  -f graphql \
  -d /zap/wrk/schema.graphql \
  -r /zap/wrk/graphql-report.html
```

Consult `references/api_testing_guide.md` for advanced API testing patterns including authentication and rate limiting.

### Step 5: Handle Authentication

For testing authenticated application areas:

```bash
# Use bundled script for authentication setup
python3 scripts/zap_auth_scanner.py \
  --target $TARGET_URL \
  --auth-type form \
  --login-url https://target-app.com/login \
  --username testuser \
  --password-env ZAP_AUTH_PASSWORD \
  --output auth-scan-report.html
```

Authentication methods supported:
- Form-based authentication
- HTTP Basic/Digest authentication
- OAuth 2.0 flows
- API key/token authentication
- Script-based custom authentication

See `references/authentication_guide.md` for detailed authentication configuration.

### Step 6: Analyze Results and Generate Reports

Review findings by risk level:

```bash
# Generate multiple report formats
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable zap-full-scan.py \
  -t $TARGET_URL \
  -r /zap/wrk/report.html \
  -J /zap/wrk/report.json \
  -x /zap/wrk/report.xml
```

**Risk Levels:**
- **High**: Critical vulnerabilities requiring immediate remediation (SQLi, RCE, authentication bypass)
- **Medium**: Significant security weaknesses (XSS, CSRF, sensitive data exposure)
- **Low**: Security concerns with lower exploitability (information disclosure, minor misconfigurations)
- **Informational**: Security best practices and observations

Map findings to OWASP Top 10 using `references/owasp_mapping.md`.

## Automation & CI/CD Integration

### GitHub Actions Integration

Add ZAP scanning to GitHub workflows:

```yaml
# .github/workflows/zap-scan.yml
name: ZAP Security Scan
on: [push, pull_request]

jobs:
  zap_scan:
    runs-on: ubuntu-latest
    name: OWASP ZAP Baseline Scan
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'https://staging.target-app.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'
```

### Docker Automation Framework

Use YAML-based automation for advanced workflows:

```bash
# Create automation config (see assets/zap_automation.yaml)
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable \
  zap.sh -cmd -autorun /zap/wrk/zap_automation.yaml
```

The bundled `assets/zap_automation.yaml` template includes:
- Environment configuration
- Spider and AJAX spider settings
- Passive and active scan policies
- Authentication configuration
- Report generation

### CI/CD Best Practices

- Use **baseline scans** for every commit/PR (low false positives)
- Run **full scans** on staging environments before production deployment
- Configure **API scans** for microservices and REST endpoints
- Set **failure thresholds** to break builds on high-severity findings
- Generate **SARIF reports** for GitHub Security tab integration

See `scripts/ci_integration.sh` for complete CI/CD integration examples.

## Security Considerations

- **Authorization**: Always obtain written authorization before scanning production systems or third-party applications
- **Rate Limiting**: Configure scan speed to avoid overwhelming target applications or triggering DDoS protections
- **Sensitive Data**: Never include production credentials in scan configurations; use environment variables or secrets management
- **Scan Timing**: Run active scans during maintenance windows or against dedicated testing environments
- **Legal Compliance**: Adhere to computer fraud and abuse laws; unauthorized scanning may be illegal
- **Audit Logging**: Log all scan executions, targets, findings, and remediation actions for compliance audits
- **Data Retention**: Sanitize scan reports before sharing; they may contain sensitive application data
- **False Positives**: Manually verify findings before raising security incidents; DAST tools generate false positives

## Bundled Resources

### Scripts (`scripts/`)

- `zap_baseline_scan.sh` - Automated baseline scanning with configurable targets and reporting
- `zap_full_scan.sh` - Comprehensive active scanning with exclusion rules
- `zap_api_scan.py` - API testing with OpenAPI/GraphQL specification support
- `zap_auth_scanner.py` - Authenticated scanning with multiple authentication methods
- `ci_integration.sh` - CI/CD integration examples for Jenkins, GitLab CI, GitHub Actions

### References (`references/`)

- `authentication_guide.md` - Complete authentication configuration for form-based, OAuth, and token authentication
- `owasp_mapping.md` - Mapping of ZAP alerts to OWASP Top 10 2021 and CWE classifications
- `api_testing_guide.md` - Advanced API testing patterns for REST, GraphQL, SOAP, and WebSocket
- `scan_policies.md` - Custom scan policy configuration for different application types
- `false_positive_handling.md` - Common false positives and verification techniques

### Assets (`assets/`)

- `zap_automation.yaml` - Automation framework configuration template
- `zap_context.xml` - Context configuration with authentication and session management
- `scan_policy_modern_web.policy` - Scan policy optimized for modern JavaScript applications
- `scan_policy_api.policy` - Scan policy for REST and GraphQL APIs
- `github_action.yml` - GitHub Actions workflow template
- `gitlab_ci.yml` - GitLab CI pipeline template

## Common Patterns

### Pattern 1: Progressive Scanning (Speed vs. Coverage)

Start with fast scans and progressively increase depth:

```bash
# Stage 1: Quick baseline scan (5-10 minutes)
docker run -t zaproxy/zap-stable zap-baseline.py -t $TARGET_URL -r baseline.html

# Stage 2: Full spider + passive scan (15-30 minutes)
docker run -t zaproxy/zap-stable zap-baseline.py -t $TARGET_URL -r baseline.html -c baseline-rules.tsv

# Stage 3: Targeted active scan on critical endpoints (1-2 hours)
docker run -t zaproxy/zap-stable zap-full-scan.py -t $TARGET_URL -r full.html -c full-rules.tsv
```

### Pattern 2: API-First Testing

Prioritize API security testing:

```bash
# 1. Test API endpoints with specification
docker run -v $(pwd):/zap/wrk/:rw -t zaproxy/zap-stable zap-api-scan.py \
  -t https://api.target.com -f openapi -d /zap/wrk/openapi.yaml -r /zap/wrk/api.html

# 2. Run active scan on discovered API endpoints
# (ZAP automatically includes spidered API routes)

# 3. Test authentication flows
python3 scripts/zap_auth_scanner.py --target https://api.target.com --auth-type bearer --token-env API_TOKEN
```

### Pattern 3: Authenticated Web Application Testing

Test complete application including protected areas:

```bash
# 1. Configure authentication context
# See assets/zap_context.xml for template

# 2. Run authenticated scan
python3 scripts/zap_auth_scanner.py \
  --target https://app.target.com \
  --auth-type form \
  --login-url https://app.target.com/login \
  --username testuser \
  --password-env APP_PASSWORD \
  --verification-url https://app.target.com/dashboard \
  --output authenticated-scan.html

# 3. Review session-specific vulnerabilities (CSRF, privilege escalation)
```

### Pattern 4: CI/CD Security Gate

Implement ZAP as a security gate in deployment pipelines:

```bash
# Run baseline scan and fail build on high-risk findings
docker run -t zaproxy/zap-stable zap-baseline.py \
  -t https://staging.target.com \
  -r baseline-report.html \
  -J baseline-report.json \
  --hook=scripts/ci_integration.sh

# Check exit code
if [ $? -ne 0 ]; then
  echo "Security scan failed! High-risk vulnerabilities detected."
  exit 1
fi
```

## Integration Points

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, Azure DevOps, CircleCI
- **Issue Tracking**: Jira, GitHub Issues (via SARIF), ServiceNow
- **Security Tools**: Defect Dojo (vulnerability management), SonarQube, OWASP Dependency-Check
- **SDLC**: Pre-production testing phase, security regression testing, penetration testing preparation
- **Authentication**: Integrates with OAuth providers, SAML, API gateways, custom authentication scripts
- **Reporting**: HTML, JSON, XML, Markdown, SARIF (for GitHub Security), PDF (via custom scripts)

## Troubleshooting

### Issue: Docker Container Cannot Reach Target Application

**Solution**: For scanning applications running on localhost or in other containers:

```bash
# Scanning host application from Docker container
# Use docker0 bridge IP instead of localhost
HOST_IP=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
docker run -t zaproxy/zap-stable zap-baseline.py -t http://$HOST_IP:8080

# Scanning between containers - create shared network
docker network create zap-network
docker run --network zap-network -t zaproxy/zap-stable zap-baseline.py -t http://app-container:8080
```

### Issue: Scan Completes Too Quickly (Incomplete Coverage)

**Solution**: Increase spider depth and scan duration:

```bash
# Configure spider to crawl deeper
docker run -t zaproxy/zap-stable zap-baseline.py \
  -t $TARGET_URL \
  -r report.html \
  -z "-config spider.maxDepth=10 -config spider.maxDuration=60"
```

For JavaScript-heavy applications, use AJAX spider or Automation Framework.

### Issue: High False Positive Rate

**Solution**: Create custom scan policy and rules file:

```bash
# Use bundled false positive handling guide
# See references/false_positive_handling.md

# Generate rules file to suppress false positives
# Format: alert_id  URL_pattern  parameter  CWE_id  WARN|IGNORE|FAIL
echo "10202  https://target.com/static/.*  .*  798  IGNORE" >> .zap/rules.tsv

docker run -t zaproxy/zap-stable zap-baseline.py -t $TARGET_URL -c .zap/rules.tsv
```

### Issue: Authentication Session Expires During Scan

**Solution**: Configure session re-authentication:

```bash
# Use bundled authentication script with session monitoring
python3 scripts/zap_auth_scanner.py \
  --target $TARGET_URL \
  --auth-type form \
  --login-url https://target.com/login \
  --username testuser \
  --password-env PASSWORD \
  --re-authenticate-on 401,403 \
  --verification-interval 300
```

### Issue: Scan Triggering Rate Limiting or WAF Blocking

**Solution**: Reduce scan aggressiveness:

```bash
# Slower scan with delays between requests
docker run -t zaproxy/zap-stable zap-baseline.py \
  -t $TARGET_URL \
  -r report.html \
  -z "-config scanner.threadPerHost=1 -config scanner.delayInMs=1000"
```

## References

- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ZAP Docker Documentation](https://www.zaproxy.org/docs/docker/)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [ZAP Automation Framework](https://www.zaproxy.org/docs/automate/automation-framework/)
- [GitHub Actions for ZAP](https://github.com/zaproxy/action-baseline)
