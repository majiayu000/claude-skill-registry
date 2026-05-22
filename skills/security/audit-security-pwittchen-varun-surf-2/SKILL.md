---
name: audit-security
description: Quick security audit checking for hardcoded secrets, SSRF vectors, injection points, dependency issues, and missing security headers
---

# Security Audit Skill

Perform a focused security audit on the codebase, checking for common vulnerabilities and security misconfigurations.

## Instructions

Run through each security check systematically and report all findings.

### 1. Hardcoded Secrets Detection

Search for potential secrets in the codebase:

```bash
# Patterns to search for
API_KEY, api_key, apiKey, ApiKey
PASSWORD, password, Password, passwd
SECRET, secret, Secret
TOKEN, token, Token
CREDENTIAL, credential, Credential
PRIVATE_KEY, private_key, privateKey
AUTH, auth (in assignment context)
Bearer, Basic (hardcoded auth headers)
```

**Using Grep tool**, search for these patterns in:
- `src/main/java/**/*.java`
- `src/main/resources/*.yml`
- `src/main/resources/*.properties`
- `*.env*` files (except .env.example)
- `docker-compose*.yml`

**Exclude**:
- Test files (`src/test/**`)
- Comments explaining what secrets are needed
- Environment variable references (`${...}`, `System.getenv()`)
- Configuration property placeholders

### 2. SSRF Vector Analysis

Identify potential Server-Side Request Forgery vulnerabilities:

**Search for**:
- URL construction from user input
- HTTP client calls with dynamic URLs
- `new URL()`, `URI.create()`, `HttpRequest.newBuilder()`
- OkHttp, RestTemplate, WebClient with variable URLs
- Redirect following without validation

**Check**:
- Are URLs validated against allowlists?
- Is there URL scheme validation (http/https only)?
- Are internal IPs blocked (127.0.0.1, 10.x, 192.168.x, 169.254.x)?
- Is redirect following limited?

**In this project, examine**:
- `GoogleMapsService.java` - URL unshortening
- `ForecastService.java` - Windguru API calls
- Strategy implementations - weather station fetches

### 3. Injection Point Detection

Search for potential injection vulnerabilities:

**Command Injection**:
```java
Runtime.exec(), ProcessBuilder
String concatenation with external input
```

**SQL Injection** (if applicable):
```java
String query = "SELECT * FROM " + userInput
Statement.execute() with concatenated strings
```

**Log Injection**:
```java
log.info("User: " + userInput)  // without sanitization
```

**XSS in responses**:
```java
Returning user input in HTML without encoding
```

**Check for**:
- String concatenation in sensitive operations
- Missing input validation/sanitization
- Unparameterized queries or commands

### 4. Dependency Security Check

Analyze `build.gradle` for:

**Version Issues**:
- Outdated dependencies with known CVEs
- Dependencies without version pinning
- Use of deprecated libraries

**Key dependencies to check**:
```
spring-boot-starter-* (current: 3.5.x)
okhttp (current: 4.12.x)
gson
spring-ai-*
playwright (for E2E)
```

**Recommend**:
- Running `./gradlew dependencyUpdates` if available
- Checking against NIST NVD or Snyk database
- Using OWASP dependency-check plugin

### 5. Security Headers Analysis

Check for missing security headers in responses:

**Required headers**:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy`
- `Referrer-Policy`

**Check locations**:
- Spring Security configuration (if present)
- WebFilter implementations
- Controller response modifications
- `nginx.conf` (if applicable)
- `NettyConfig.java` or similar

### 6. Additional Quick Checks

**Authentication/Authorization**:
- Are endpoints properly secured?
- Is there rate limiting?
- Session management issues?

**Sensitive Data Exposure**:
- Stack traces in error responses?
- Verbose error messages?
- Debug endpoints enabled in prod?

**CORS Configuration**:
- Overly permissive CORS (`*`)?
- Credentials allowed with wildcard origin?

## Output Format

```markdown
## Security Audit Report

### Summary
| Category | Issues Found | Severity |
|----------|--------------|----------|
| Hardcoded Secrets | X | Critical/None |
| SSRF Vectors | X | High/Medium/None |
| Injection Points | X | Critical/None |
| Dependencies | X | High/Medium/Low |
| Security Headers | X | Medium/None |

### Critical Issues (Immediate Action Required)

#### [Issue Title]
**File**: `path/to/file.java:line`
**Type**: [Hardcoded Secret / Injection / etc.]
**Risk**: [What could happen if exploited]
**Evidence**:
```java
// problematic code
```
**Remediation**: [How to fix]

### High Priority Issues

#### [Issue Title]
...

### Medium Priority Issues

#### [Issue Title]
...

### Low Priority / Informational

- [Finding 1]
- [Finding 2]

### Passed Checks

- No hardcoded secrets found in source code
- Dependencies are up to date
- [Other positive findings]

### Recommendations

1. [Priority recommendation]
2. [Additional recommendation]
3. [Long-term improvement]
```

## Execution Steps

1. **Secrets scan**: Use `Grep` to search for secret patterns across the codebase
2. **SSRF analysis**: Read HTTP client code and URL handling logic
3. **Injection check**: Search for string concatenation patterns in sensitive contexts
4. **Dependency review**: Read `build.gradle` and check versions
5. **Headers check**: Examine security configuration and filters
6. **Compile report**: Organize findings by severity

## Notes

- Focus on actionable findings, not theoretical risks
- Distinguish between actual secrets and configuration placeholders
- Consider the context (e.g., test data vs production code)
- For dependencies, note that patch versions usually don't have CVEs
- This is a quick audit; recommend periodic deep security reviews
