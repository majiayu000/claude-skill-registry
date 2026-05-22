---
name: playwright-security-runner
description: Dynamic security testing of web forms using Playwright browser automation. Sends actual payloads to test for vulnerabilities. REQUIRES USER CONFIRMATION before execution. Use when user wants to "test payloads", "dynamic security test", "exploit testing", "penetration test forms".
---

# Playwright Security Runner

Dynamic security testing with real browser automation. This skill **sends actual payloads** to targets.

## CRITICAL: Safety Protocols

**This skill sends real requests. ALWAYS get user confirmation first.**

### Before Running:
1. Show the user what payloads will be sent
2. Confirm the target is authorized for testing
3. Warn if target appears to be production

### Confirmation Template:
```
Security Test Plan

Target: http://localhost:3000/login
Payloads to send:
1. [XSS] <script>alert(1)</script> -> username field
2. [SQLi] ' OR '1'='1 -> password field

This will send real requests to the target.
Potential bounty: $5,000 - $15,000

Proceed? (yes/no)
```

## Quick Start

```bash
# Install dependencies
cd ${CLAUDE_PLUGIN_ROOT}/skills/playwright-security-runner && npm install

# Dry run - shows what would be tested (SAFE)
npm --prefix ${CLAUDE_PLUGIN_ROOT}/skills/playwright-security-runner run dev -- \
  --url "http://localhost:3000/login" \
  --dry-run

# Actually run tests (REQUIRES CONFIRMATION)
npm --prefix ${CLAUDE_PLUGIN_ROOT}/skills/playwright-security-runner run dev -- \
  --url "http://localhost:3000/login" \
  --test xss,sqli

# Or after building
npm --prefix ${CLAUDE_PLUGIN_ROOT}/skills/playwright-security-runner run build
node ${CLAUDE_PLUGIN_ROOT}/skills/playwright-security-runner/dist/index.js \
  --url "http://localhost:3000/login" \
  --test xss,sqli
```

## Test Types

| Type | What It Tests | Payloads |
|------|--------------|----------|
| `xss` | Cross-site scripting | Script tags, event handlers |
| `sqli` | SQL injection | Quotes, UNION, comments |
| `auth` | Authentication | Bypass attempts |

## Options

| Option | Description |
|--------|-------------|
| `--url <url>` | Target URL (required) |
| `--form <selector>` | CSS selector for form (optional) |
| `--test <types>` | Comma-separated test types |
| `--dry-run` | Show plan without executing |
| `--screenshot` | Capture screenshots of results |
| `--json` | Output as JSON |
| `--headed` | Run with visible browser |

## Safety Features

### 1. Production Detection
```
WARNING: Production URL Detected

The target URL appears to be a production system:
https://example.com/login

Security testing against production:
- May cause service disruption
- Could trigger security alerts
- May violate terms of service

Ensure you have authorization to test this target.
```

### 2. Dry Run Mode
```bash
npm run dev -- --url "http://target.com" --dry-run
```

Output:
```
DRY RUN MODE

Target: http://target.com/login
Form: All forms
Tests: xss, sqli

Payloads that would be sent:

[XSS] - Bounty: $500 - $10,000
  1. script-tag: <script>alert(1)</script>...
  2. img-onerror: <img src=x onerror=alert(1)>...

No requests sent. Remove --dry-run to execute tests.
```

## Output Format

### Vulnerability Found
```markdown
## VULNERABILITY FOUND

**Type**: Reflected XSS
**Severity**: HIGH
**Bounty Estimate**: $2,000 - $10,000

**Target**: http://localhost:3000/search
**Field**: query
**Payload**: <script>alert(1)</script>

**Evidence**:
- Payload reflected in response without encoding
- Alert dialog triggered

**Screenshot**: ./screenshots/xss-001.png
```

## Integration Workflow

1. **Static Analysis First** (safe - no requests)
2. **Review Findings** - Identify high-value targets
3. **Dry Run** - Still safe, just planning
4. **Get Confirmation** - Show payload list to user
5. **Execute Tests** - Now sending payloads
6. **Document Findings** - Screenshots as evidence

## Important Notes

- **localhost/staging only**: Prefer testing against development environments
- **Authorization required**: Ensure you have permission to test
- **Rate limiting**: Built-in delays between requests (200ms)
- **Evidence collection**: Screenshots and logs for bug reports

## External Resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
