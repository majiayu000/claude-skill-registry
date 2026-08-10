---
name: security-audit
description: Perform a broad, authorized security audit across application, infrastructure, identity, dependencies, and operations. Use when the user needs a scoped security posture review; use the SAST, DAST, dependency-scanning, or threat-modeling skill when the request is limited to one specialist activity.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Security Audit

This skill enables the agent to conduct a thorough security audit across web applications, APIs, cloud infrastructure, and backend services. The agent systematically examines authentication mechanisms, authorization controls, input validation, encryption practices, logging configurations, and deployment settings. Findings are mapped to industry frameworks such as the OWASP Top 10, CWE identifiers, and compliance standards including SOC 2 and PCI-DSS.

## Workflow

1. **Gather System Information** — Collect details about the target environment including the technology stack, architecture diagrams, network topology, deployment model, and third-party integrations. Review configuration files, environment variables, and infrastructure-as-code templates to build a complete picture of the attack surface.

2. **Define Audit Scope and Compliance Targets** — Establish the boundaries of the audit by identifying which components, environments, and data flows are in scope. Map audit objectives to relevant compliance frameworks such as SOC 2 Type II, PCI-DSS, HIPAA, or internal security policies. Create a checklist derived from the OWASP Top 10 and CWE/SANS Top 25 to ensure systematic coverage.

3. **Perform Automated Vulnerability Scanning** — Run automated scanners against the target to identify known vulnerabilities. Use tools like OWASP ZAP for web applications, Trivy or Grype for container images, and ScoutSuite or Prowler for cloud infrastructure. Aggregate raw findings for manual review.

4. **Conduct Manual Security Review** — Manually inspect authentication flows, session management, role-based access controls, input sanitization routines, cryptographic implementations, error handling, and logging practices. Examine source code for hardcoded secrets, insecure deserialization, and business logic flaws that automated tools frequently miss.

5. **Analyze and Classify Findings** — Assess each finding for severity (Critical, High, Medium, Low, Informational) using CVSS scoring. Assign CWE identifiers and map findings to the relevant OWASP Top 10 category. Evaluate exploitability, blast radius, and business impact to produce a prioritized risk ranking.

6. **Generate Audit Report with Remediation Plan** — Produce a structured report containing an executive summary, detailed findings with evidence and reproduction steps, risk ratings, and specific remediation recommendations with estimated effort. Include a compliance gap analysis showing pass/fail status against the targeted framework controls.

## Supported Technologies

- **Web Frameworks**: Express.js, Django, Flask, Spring Boot, Rails, ASP.NET
- **Cloud Platforms**: AWS (IAM, S3, EC2, RDS, Lambda), GCP, Azure
- **Container & Orchestration**: Docker, Kubernetes, ECS
- **Scanning Tools**: OWASP ZAP, Prowler, ScoutSuite, Trivy, Grype, Checkov
- **Compliance Frameworks**: OWASP Top 10, CWE/SANS Top 25, SOC 2, PCI-DSS, HIPAA, NIST 800-53

## Usage

Provide the agent with access to the application source code, infrastructure configuration, or a target URL along with the desired compliance scope. The agent will execute the full audit workflow and deliver a prioritized findings report.

**Prompt example:**

```
Perform a security audit of the Node.js Express application in /app. Focus on OWASP Top 10 coverage and SOC 2 compliance. Include CWE IDs and remediation steps for every finding.
```

## Examples

### Example 1: Auditing a Node.js Express Application

**Target**: E-commerce API built with Express.js, Sequelize ORM, and JWT authentication.

**Findings Report (excerpt):**

| # | Severity | Title | CWE | OWASP Category |
|---|----------|-------|-----|----------------|
| 1 | Critical | SQL injection in product search endpoint | CWE-89 | A03:2021 Injection |
| 2 | High | JWT secret stored in plaintext in `.env` committed to repo | CWE-798 | A07:2021 Identification and Authentication Failures |
| 3 | High | Missing rate limiting on `/api/login` | CWE-307 | A07:2021 Identification and Authentication Failures |
| 4 | Medium | Verbose error messages expose stack traces in production | CWE-209 | A04:2021 Insecure Design |
| 5 | Medium | CORS policy allows wildcard origin with credentials | CWE-942 | A05:2021 Security Misconfiguration |
| 6 | Low | HTTP security headers missing (X-Content-Type-Options, CSP) | CWE-693 | A05:2021 Security Misconfiguration |

**Remediation for Finding #1:**

```javascript
// BEFORE — vulnerable to SQL injection
app.get('/api/products', async (req, res) => {
  const results = await sequelize.query(
    `SELECT * FROM products WHERE name LIKE '%${req.query.search}%'`
  );
  res.json(results);
});

// AFTER — parameterized query
app.get('/api/products', async (req, res) => {
  const results = await sequelize.query(
    'SELECT * FROM products WHERE name LIKE :search',
    { replacements: { search: `%${req.query.search}%` }, type: QueryTypes.SELECT }
  );
  res.json(results);
});
```

### Example 2: Auditing AWS Infrastructure

**Target**: Production AWS account running a three-tier web application.

**Prowler scan command:**

```bash
prowler aws --compliance soc2 pci_dss --output-formats json html --output-directory ./audit-report
```

**Findings Report (excerpt):**

| # | Severity | Finding | AWS Service | Compliance Control |
|---|----------|---------|-------------|-------------------|
| 1 | Critical | S3 bucket `prod-user-uploads` has public read access enabled | S3 | PCI-DSS 7.1, SOC 2 CC6.1 |
| 2 | High | IAM user `deploy-bot` has inline AdministratorAccess policy | IAM | SOC 2 CC6.3 |
| 3 | High | RDS instance `prod-db` has encryption at rest disabled | RDS | PCI-DSS 3.4, SOC 2 CC6.1 |
| 4 | Medium | CloudTrail logging is not enabled for all regions | CloudTrail | SOC 2 CC7.2 |
| 5 | Medium | Security group `sg-0abc123` allows SSH (port 22) from 0.0.0.0/0 | EC2 | PCI-DSS 1.3 |

**Remediation for Finding #2:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ecr:GetAuthorizationToken", "ecs:UpdateService", "ecs:DescribeServices"],
      "Resource": "arn:aws:ecs:us-east-1:123456789012:service/prod-cluster/web-service"
    }
  ]
}
```

## Best Practices

- **Audit regularly on a schedule** — perform audits quarterly at minimum and after every major release or infrastructure change, not just annually.
- **Combine automated and manual testing** — automated scanners catch known vulnerability patterns, but manual review is essential for business logic flaws, authorization bypasses, and chained attack scenarios.
- **Use CWE and CVSS consistently** — assign CWE identifiers and CVSS scores to every finding so that stakeholders can compare severity across audits and track remediation trends.
- **Verify remediation with retesting** — after fixes are deployed, re-run the relevant audit checks to confirm the vulnerability is resolved and no regressions were introduced.
- **Maintain an audit trail** — store all audit reports, evidence, and remediation records in a centralized repository to support compliance reviews and incident investigations.
- **Scope audits to include third-party integrations** — payment gateways, OAuth providers, and SaaS APIs introduce risk that is easy to overlook when auditing only first-party code.

## Safety Boundaries

- Work only on systems the user owns or is explicitly authorized to assess, and record the approved scope before testing.
- Start with passive or read-only inspection. Obtain explicit approval before active scanning, exploitation, load generation, or disruptive remediation.
- Never expose secrets, extract unrelated data, weaken production controls, or expand beyond the approved targets.
- Preserve evidence, minimize impact, stop on instability, and provide rollback or containment steps for every material change.

## Edge Cases

- **Microservices with inconsistent security postures** — one service may enforce authentication while another internal service trusts all traffic. Audit inter-service communication and verify that zero-trust principles are applied even within the private network.
- **Legacy systems without source code access** — when source code is unavailable, rely on black-box testing, traffic analysis, and configuration review. Document the reduced coverage explicitly in the audit report.
- **Serverless and event-driven architectures** — Lambda functions, Step Functions, and event triggers have ephemeral execution contexts. Audit IAM execution roles, event source permissions, and ensure sensitive data is not logged to CloudWatch in plaintext.
- **Multi-tenant applications** — verify that tenant isolation is enforced at the data layer, API layer, and infrastructure layer. Test for horizontal privilege escalation between tenant accounts.
- **Applications behind WAF or CDN** — automated scanners may only test the WAF-filtered surface. Where possible, also test the origin directly to identify vulnerabilities the WAF is masking rather than fixing.
