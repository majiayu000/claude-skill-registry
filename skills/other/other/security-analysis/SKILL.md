---
name: security-analysis
description: "Use when conducting threat modeling (STRIDE), building attack trees, running SAST scans, writing custom Semgrep rules, extracting security requirements, or mapping controls to compliance frameworks."
---

# Security Analysis

## STRIDE Threat Modeling

| Category | Threat | Control Family | Key Questions |
|----------|--------|----------------|---------------|
| **Spoofing** | Impersonation | Authentication | Token validation? Session prediction? |
| **Tampering** | Data modification | Integrity | Input validation? Data signing? |
| **Repudiation** | Deny actions | Logging/Audit | Tamper-proof logs? Coverage gaps? |
| **Info Disclosure** | Data leakage | Encryption | Error message leaks? Encryption gaps? |
| **DoS** | Availability | Rate limiting | Resource exhaustion vectors? |
| **Elevation** | Privilege escalation | Authorization | Consistent authz checks? Parameter manipulation? |

## Risk Scoring

```
Risk = Impact x Likelihood (each 1-4)

Score >= 12: Critical (immediate remediation)
Score >= 6:  High (sprint priority)
Score >= 3:  Medium (backlog)
Score < 3:   Low (accept or defer)
```

## Attack Tree Patterns

- **OR nodes**: any child path achieves the goal (attacker picks easiest)
- **AND nodes**: all children required (harder to execute)
- **Prioritize**: unmitigated leaf nodes with LOW difficulty
- **Key insight**: OR nodes at the root mean you must mitigate ALL paths; AND nodes mean disrupting one path is sufficient

## STRIDE-to-Requirements Mapping

| STRIDE Category | Security Domains | Default Requirements |
|----------------|-----------------|---------------------|
| Spoofing | Authentication, Session Mgmt | Strong auth, token verification, session binding |
| Tampering | Input Validation, Data Protection | Input allowlisting, integrity signatures |
| Repudiation | Audit Logging | Immutable security event logs |
| Info Disclosure | Data Protection, Crypto | Encrypt at rest + transit, suppress error details |
| DoS | Availability, Input Validation | Rate limiting, resource quotas |
| Elevation | Authorization | RBAC/ABAC, least privilege, consistent authz checks |

## Controls Library (Preferred Defaults)

| Control | Type | Layer | Mitigates | Compliance Refs |
|---------|------|-------|-----------|----------------|
| MFA | Preventive | App | Spoofing | PCI-DSS 8.3, OWASP V2 |
| Input Validation | Preventive | App | Tampering | OWASP V5 |
| Encryption at Rest | Preventive | Data | Info Disclosure | PCI-DSS 3.4, GDPR Art. 32 |
| Security Event Logging | Detective | App | Repudiation | PCI-DSS 10.2, GDPR Art. 30 |
| RBAC | Preventive | App | Elevation | PCI-DSS 7.1 |
| Rate Limiting | Preventive | App | DoS | OWASP API |

## SAST Tool Selection

| Tool | Best For | Use When |
|------|----------|----------|
| **Semgrep** | Custom rules, fast scans, multi-language | Default choice. Free, fast, excellent custom rules |
| **SonarQube** | Code quality + security combined | Need quality gates, tech debt tracking, enterprise reporting |
| **CodeQL** | Deep dataflow analysis, vulnerability research | GitHub-native, open-source projects, complex vulnerability patterns |
| **Bandit** | Python-specific scanning | Python projects, complement to Semgrep |
| **ESLint Security** | JS/TS inline feedback | Already using ESLint, want IDE-integrated security checks |

**Default stack**: Semgrep (all languages) + language-specific linter (Bandit/ESLint security plugin).

## SAST Rule Strategy

### Start Narrow, Expand Gradually
1. Begin with `p/security-audit` + `p/owasp-top-ten` rulesets
2. Block CI only on `ERROR` severity -- `WARNING` as informational
3. After team adapts (~2 weeks), add language-specific rules
4. Custom rules only for org-specific patterns

### High-Value Rules (Always Enable)
- **Injection**: SQL via string formatting, command injection via `shell=True`, XSS via `innerHTML`
- **Secrets**: hardcoded API keys, AWS credentials (`AKIA...`), JWT secrets in source
- **Insecure patterns**: `pickle.loads()`, `yaml.load()` with untrusted data, `random` for security ops

## CI Integration

### Pipeline Placement
```
PR opened -> lint -> unit tests -> SAST scan -> build -> integration tests
```
Run SAST early (before build) for fast feedback. Gate on errors only, not warnings.

### GitHub Actions
```yaml
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp-top-ten
```

### False Positive Management
- `# nosemgrep: rule-id` with mandatory comment explaining why
- Exclude `tests/`, `vendor/`, `node_modules/`, `generated/`
- Review suppressions quarterly -- code changes may invalidate them

## Custom Semgrep Rules

```yaml
rules:
  - id: no-raw-sql
    pattern: cursor.execute("... %s ..." % $VAR)
    message: "Use parameterized queries, not string formatting"
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-89"

  - id: no-innerHTML-user-input
    pattern: $ELEM.innerHTML = $VAR
    message: "Use textContent or DOMPurify.sanitize()"
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: "CWE-79"
```

## Vulnerability Quick Reference

| Vulnerability | Detection | Fix |
|---------------|-----------|-----|
| SQL Injection | String formatting in queries | Parameterized queries, ORM |
| XSS | innerHTML, v-html, dangerouslySetInnerHTML | textContent, DOMPurify |
| Command Injection | os.system(), shell=True | subprocess with array args |
| Path Traversal | Unsanitized file paths | os.path.realpath + prefix check |
| Hardcoded Secrets | Regex patterns in source | Environment variables, secret managers |
| Insecure Deserialization | pickle.loads, yaml.load | json.loads, yaml.safe_load |

## Threat Model Document Structure

1. **System Overview** - data flow diagram + trust boundaries
2. **Assets** - sensitivity classification per asset
3. **STRIDE Analysis** - table per category with impact/likelihood
4. **Attack Trees** - mermaid diagrams for top 3 scenarios
5. **Mitigation Plan** - threat/control/status/coverage matrix
6. **Recommendations** - tiered: immediate (critical), 30-day (high), 90-day (improvements)

## Requirement Traceability

Every security requirement must link back to:
- **Threat ID** it mitigates
- **Compliance control** it satisfies (PCI-DSS, HIPAA, GDPR, SOC2, OWASP)
- **Acceptance criteria** (testable, specific)
- **Priority** derived from risk score (not gut feel)

## Compliance Framework Quick Reference

| Framework | Auth Controls | Data Protection | Audit | Crypto |
|-----------|--------------|----------------|-------|--------|
| PCI-DSS | 8.1-8.3 | 3.4-3.5, 4.1 | 10.1-10.3 | 3.5-3.6 |
| HIPAA | 164.312(d) | 164.312(a)(2)(iv) | 164.312(b) | -- |
| GDPR | -- | Art. 25, 32 | Art. 30 | Art. 32 |
| OWASP ASVS | V2.1-V2.3 | V8.1-V8.3 | -- | V6.1-V6.2 |

## Agent Team Mode

For comprehensive threat modeling of complex systems with multiple trust boundaries and compliance requirements.

### Team Configuration

```yaml
team:
  recommended_size: 4
  agent_roles:
    - name: stride-analyst
      type: Explore
      focus: "STRIDE category analysis per component and trust boundary"
      skills_loaded: ["security:security-analysis"]
    - name: attack-tree-builder
      type: Explore
      focus: "Attack tree construction from STRIDE findings, path prioritization"
      skills_loaded: ["security:security-analysis"]
    - name: sast-scanner
      type: general-purpose
      focus: "SAST rule execution, custom Semgrep rule generation, false positive triage"
      skills_loaded: ["security:security-analysis"]
    - name: compliance-mapper
      type: Explore
      focus: "Map findings to PCI-DSS, HIPAA, GDPR, OWASP ASVS controls"
      skills_loaded: ["security:compliance-and-data-privacy"]
  file_ownership: "shared-read-only"
  lead_mode: "hands-on"
```

### Team Workflow

1. Lead defines system boundaries, assets, and trust boundaries
2. stride-analyst and attack-tree-builder work in parallel (attack-tree-builder uses STRIDE findings as they arrive)
3. sast-scanner runs automated scans concurrently
4. compliance-mapper maps all discovered threats to compliance controls
5. Lead synthesizes into Threat Model Document (system overview, STRIDE table, attack trees, mitigation plan, recommendations)

### Single-Agent Fallback

Without team mode, execute all phases sequentially (default behavior). Team mode is an optional enhancement.

## Gotchas

- OR-node attack trees need ALL paths mitigated; missing one leaves the goal achievable
- Risk scores should drive requirement priority -- don't let stakeholder politics override
- Detective controls (logging) are necessary but insufficient alone; pair with preventive
- Error messages are an info disclosure vector -- generic errors externally, detailed internally
- Session management is often the weakest STRIDE link; model it explicitly
- Compliance mapping gaps surface best through automated traceability matrices, not manual review
