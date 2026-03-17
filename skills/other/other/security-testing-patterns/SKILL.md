---
name: security-testing-patterns
description: Security testing patterns including SAST, DAST, penetration testing, and vulnerability assessment techniques. Use when implementing security testing pipelines, conducting security audits, or validating application security controls.
---

# Security Testing Patterns

Expert guidance for implementing comprehensive security testing strategies including static analysis, dynamic testing, penetration testing, and vulnerability assessment.

## When to Use This Skill

- Implementing security testing pipelines in CI/CD
- Conducting security audits and vulnerability assessments
- Validating application security controls and defenses
- Performing penetration testing and security reviews
- Configuring SAST/DAST tools and interpreting results
- Testing authentication and authorization mechanisms
- Evaluating API security and compliance with OWASP standards
- Integrating security scanning into development workflows
- Responding to security findings and prioritizing remediation
- Training teams on security testing methodologies

## Core Concepts

### Security Testing Pyramid (Layered Approach)

1. **Unit Security Tests** - Test security functions (encryption, validation)
2. **SAST** - Static analysis during development
3. **SCA** - Dependency and component vulnerability scanning
4. **DAST** - Dynamic testing in running applications
5. **IAST** - Interactive analysis combining SAST and DAST
6. **Penetration Testing** - Manual security testing by experts
7. **Red Team Exercises** - Adversarial simulation testing

### Testing Categories

**Static Testing (SAST)**
- Analyzes source code without execution
- Early detection in development lifecycle
- Complete code coverage
- High false positive rates

**Dynamic Testing (DAST)**
- Tests running applications
- Detects runtime and configuration issues
- Language agnostic
- Requires deployed environment

**Composition Analysis (SCA)**
- Scans dependencies for vulnerabilities
- Tracks license compliance
- Automated remediation options

**Manual Testing**
- Penetration testing
- Business logic validation
- Complex attack scenarios

## Quick Reference

| Task | Load reference |
| --- | --- |
| Static Application Security Testing (SAST) | `skills/security-testing-patterns/references/sast.md` |
| Dynamic Application Security Testing (DAST) | `skills/security-testing-patterns/references/dast.md` |
| Software Composition Analysis (SCA) | `skills/security-testing-patterns/references/sca.md` |
| Penetration Testing Techniques | `skills/security-testing-patterns/references/penetration-testing.md` |
| API Security Testing (OWASP Top 10) | `skills/security-testing-patterns/references/api-security.md` |
| Fuzzing and Property-Based Testing | `skills/security-testing-patterns/references/fuzzing.md` |
| Security Automation Pipeline | `skills/security-testing-patterns/references/automation-pipeline.md` |

## Security Testing Workflow

### Phase 1: Planning
1. Define security requirements and threat model
2. Select appropriate testing tools and techniques
3. Establish baseline security posture
4. Set severity thresholds and acceptance criteria

### Phase 2: Automated Testing
1. **SAST** - Integrate into IDE and CI/CD pipeline
2. **SCA** - Configure dependency scanning (npm audit, Snyk, Dependabot)
3. **DAST** - Schedule scans against deployed environments
4. **Container Scanning** - Scan Docker images (Trivy, Aqua)

### Phase 3: Manual Testing
1. Authentication and authorization testing
2. Business logic vulnerability assessment
3. API security testing (OWASP API Top 10)
4. Penetration testing and exploitation

### Phase 4: Analysis and Remediation
1. Triage findings by severity and exploitability
2. Eliminate false positives
3. Prioritize remediation based on risk
4. Track vulnerabilities to resolution
5. Verify fixes with regression testing

### Phase 5: Continuous Monitoring
1. Monitor for new vulnerabilities in dependencies
2. Re-scan after code changes
3. Conduct periodic penetration tests
4. Update security baselines and policies

## Common Mistakes

### Tool Selection
- **Wrong**: Using only SAST or only DAST
- **Right**: Layered approach combining multiple testing types

### False Positive Management
- **Wrong**: Ignoring or suppressing findings without review
- **Right**: Systematic triage process with security team validation

### Integration Timing
- **Wrong**: Security testing only before release
- **Right**: Continuous security testing throughout development

### Scope Definition
- **Wrong**: Testing only main application code
- **Right**: Include dependencies, APIs, infrastructure, and third-party integrations

### Remediation Priority
- **Wrong**: Fixing all findings equally
- **Right**: Risk-based prioritization (severity × exploitability × business impact)

### Authentication in Testing
- **Wrong**: DAST scans without authentication
- **Right**: Configure authenticated scanning to test protected features

## Best Practices

1. **Shift Left**: Integrate security testing early in development
2. **Continuous Testing**: Automate security scans in CI/CD pipelines
3. **Layered Approach**: Combine SAST, DAST, SCA, and manual testing
4. **Risk-Based Testing**: Prioritize testing based on threat model
5. **False Positive Management**: Establish process for triaging findings
6. **Remediation Tracking**: Use SIEM/SOAR for vulnerability management
7. **Regular Updates**: Keep security tools and signatures current
8. **Security Champions**: Train developers in security testing
9. **Metrics and KPIs**: Track security posture over time
10. **Compliance Validation**: Map tests to regulatory requirements

## Resources

- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **OWASP API Security**: https://owasp.org/www-project-api-security/
- **NIST SP 800-115**: Technical Guide to Information Security Testing
- **PTES**: Penetration Testing Execution Standard
- **SANS Security Testing**: https://www.sans.org/security-resources/
- **HackerOne Methodology**: https://www.hackerone.com/ethical-hacker/hack-learn
- **PortSwigger Academy**: https://portswigger.net/web-security
