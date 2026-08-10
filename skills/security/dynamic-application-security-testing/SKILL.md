---
name: dynamic-application-security-testing
description: Perform dynamic security testing against running web applications and APIs to discover vulnerabilities through active probing and fuzzing. Use when the user requests dynamic application security testing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Dynamic Application Security Testing

This skill enables the agent to perform Dynamic Application Security Testing (DAST) against running web applications and APIs. Unlike static analysis, DAST interacts with the application at runtime — sending crafted HTTP requests, fuzzing input parameters, and analyzing responses to detect vulnerabilities such as SQL injection, cross-site scripting, server misconfigurations, broken authentication, and insecure API endpoints. The agent configures scan profiles, handles authenticated scanning, interprets results, and produces actionable remediation reports.

## Workflow

1. **Define Target Scope and Scan Policy** — Specify the target URL, application type (traditional web app, SPA, REST API, GraphQL), and scan boundaries. Define which paths and domains are in scope to prevent scanning unintended targets. Select a scan policy: passive-only for low-risk reconnaissance, active for full vulnerability probing, or API-specific for endpoint fuzzing.

2. **Configure Authentication** — For applications behind a login, configure the scanner with valid credentials or session tokens. Set up form-based authentication by specifying the login URL, username/password fields, and a logged-in indicator string. For API testing, configure Bearer tokens, API keys, or OAuth flows so the scanner can reach authenticated endpoints.

3. **Execute the DAST Scan** — Launch the scan using the selected tool (OWASP ZAP, Burp Suite, or Nuclei). The scanner first spiders the application to discover endpoints, then actively probes each endpoint with attack payloads. Monitor scan progress and resource consumption to avoid overwhelming the target environment.

4. **Analyze and Classify Findings** — Review scan results and classify each finding by vulnerability type, severity (using CVSS), confidence level, and affected URL. Filter out informational noise and false positives by verifying that the reported response actually demonstrates the vulnerability.

5. **Generate Remediation Report** — Produce a structured report containing each finding with the vulnerable URL, HTTP request/response evidence, severity rating, CWE identifier, OWASP category mapping, and specific remediation guidance. Export in HTML, JSON, or SARIF format for integration with issue trackers.

6. **Schedule Recurring Scans** — Configure the scan to run on a regular schedule (e.g., nightly against staging) or trigger it on deployment to a QA environment. Compare results across scan runs to track remediation progress and detect newly introduced vulnerabilities.

## Supported Technologies

- **DAST Tools**: OWASP ZAP, Burp Suite Professional/Enterprise, Nuclei, Nikto, Arachni
- **Target Types**: Traditional web apps, Single Page Applications (React, Angular, Vue), REST APIs, GraphQL APIs, WebSocket endpoints
- **Authentication**: Form-based login, HTTP Basic/Digest, Bearer tokens, API keys, OAuth 2.0 flows
- **Output Formats**: HTML report, JSON, XML, SARIF, Markdown
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins, Azure Pipelines

## Usage

Provide the agent with the target URL, authentication credentials if needed, and the desired scan depth. The agent will configure the scanner, execute the test, and deliver a prioritized findings report.

**Prompt example:**

```
Run a DAST scan against our staging application at https://staging.example.com. Use OWASP ZAP with the login form at /login (username: testuser, password: Test@1234). Scan all API endpoints under /api/v2 and generate an HTML report.
```

## Examples

### Example 1: OWASP ZAP Scan Against a Web Application

**ZAP Docker command with authentication:**

```bash
docker run --rm -v $(pwd)/report:/zap/wrk owasp/zap2docker-stable zap-full-scan.py \
  -t https://staging.example.com \
  -r zap-report.html \
  -J zap-report.json \
  -c zap-config.conf \
  --hook=zap-auth-hook.py \
  -z "-config formhandler.fields.field(0).fieldId=username \
      -config formhandler.fields.field(0).value=testuser \
      -config formhandler.fields.field(1).fieldId=password \
      -config formhandler.fields.field(1).value=Test@1234"
```

**Findings Report (excerpt):**

| # | Risk | Alert | URL | CWE | OWASP | Confidence |
|---|------|-------|-----|-----|-------|------------|
| 1 | High | SQL Injection | `POST /api/v2/search` | CWE-89 | A03:2021 | High |
| 2 | High | Cross-Site Scripting (Reflected) | `GET /search?q=<script>` | CWE-79 | A03:2021 | High |
| 3 | Medium | Missing Anti-CSRF Tokens | `POST /api/v2/profile/update` | CWE-352 | A01:2021 | Medium |
| 4 | Medium | Cookie Without Secure Flag | `Set-Cookie: session=...` | CWE-614 | A05:2021 | High |
| 5 | Low | X-Content-Type-Options Header Missing | All responses | CWE-693 | A05:2021 | High |
| 6 | Low | Server Leaks Version Information | `Server: Apache/2.4.49` | CWE-200 | A05:2021 | High |

**Evidence for Finding #1 — SQL Injection:**

```
Request:
  POST /api/v2/search HTTP/1.1
  Content-Type: application/json
  {"query": "test' OR '1'='1' --"}

Response:
  HTTP/1.1 200 OK
  [returned all 4,892 records instead of matching records]

Remediation: Use parameterized queries or ORM methods. Validate and sanitize
all user input before including it in database queries.
```

### Example 2: Custom Nuclei Template for Detecting Exposed Debug Endpoints

**Custom template (`exposed-debug-endpoints.yaml`):**

```yaml
id: exposed-debug-endpoints
info:
  name: Exposed Debug/Admin Endpoints
  author: security-team
  severity: high
  description: Detects debug and admin endpoints that should not be publicly accessible.
  tags: misconfiguration,exposure
  classification:
    cwe-id: CWE-489
    cvss-score: 7.5

http:
  - method: GET
    path:
      - "{{BaseURL}}/debug"
      - "{{BaseURL}}/actuator"
      - "{{BaseURL}}/actuator/env"
      - "{{BaseURL}}/graphql/playground"
      - "{{BaseURL}}/_profiler"
      - "{{BaseURL}}/elmah.axd"
      - "{{BaseURL}}/phpinfo.php"
    stop-at-first-match: false
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "debug"
          - "actuator"
          - "environment"
          - "playground"
        condition: or
```

**Running the scan:**

```bash
nuclei -u https://staging.example.com -t exposed-debug-endpoints.yaml -t cves/ -severity high,critical -json -o nuclei-results.json
```

**Sample output:**

```
[exposed-debug-endpoints] [http] [high] https://staging.example.com/actuator/env
[exposed-debug-endpoints] [http] [high] https://staging.example.com/graphql/playground
[CVE-2021-44228] [http] [critical] https://staging.example.com/api/v2/log
```

## Best Practices

- **Scan staging, never production** — DAST actively sends attack payloads that can corrupt data, trigger alerts, or cause downtime. Always target a staging or QA environment that mirrors production.
- **Combine passive and active scanning** — start with a passive spider to map the application without sending attack payloads, then run active scans on the discovered endpoints for thorough coverage.
- **Configure authentication correctly** — an unauthenticated DAST scan only tests the login page and public endpoints. Most real vulnerabilities exist behind authenticated flows, so always configure valid session credentials.
- **Set scan scope boundaries** — explicitly define which domains and paths are in scope. Without boundaries, the scanner may follow links to third-party sites, CDNs, or payment providers, causing unintended consequences.
- **Compare scan baselines over time** — store scan results and compare each new run against the previous baseline. This reveals newly introduced vulnerabilities and confirms that previously reported issues have been fixed.
- **Pair DAST with SAST** — DAST finds runtime issues that SAST misses (misconfigurations, deployment errors) while SAST catches code-level flaws that DAST cannot reach. Use both for comprehensive coverage.

## Safety Boundaries

- Work only on systems the user owns or is explicitly authorized to assess, and record the approved scope before testing.
- Start with passive or read-only inspection. Obtain explicit approval before active scanning, exploitation, load generation, or disruptive remediation.
- Never expose secrets, extract unrelated data, weaken production controls, or expand beyond the approved targets.
- Preserve evidence, minimize impact, stop on instability, and provide rollback or containment steps for every material change.

## Edge Cases

- **Single Page Applications with client-side routing** — traditional spiders cannot discover routes in React, Angular, or Vue apps because links are rendered by JavaScript. Use ZAP's AJAX Spider or a headless browser-based crawler to properly discover SPA endpoints.
- **API-only applications with no UI** — without a web UI to spider, import an OpenAPI/Swagger spec or Postman collection directly into the scanner to define all endpoints, parameters, and expected request formats.
- **Rate-limited or WAF-protected targets** — aggressive scanning may trigger rate limits or WAF blocks, producing false negatives. Throttle the scan rate, allowlist the scanner IP in the WAF, or test the origin server directly to get accurate results.
- **WebSocket and real-time endpoints** — most DAST tools focus on HTTP request/response patterns. WebSocket connections require specialized tooling or manual testing to probe for injection and authorization issues in real-time message flows.
- **Stateful multi-step workflows** — vulnerabilities in flows like checkout, password reset, or MFA enrollment require the scanner to follow a specific sequence of steps. Define scan sequences or use recorded macros to test these workflows end-to-end.
