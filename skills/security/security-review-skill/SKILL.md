---
document_name: "security-review.skill.md"
location: ".claude/skills/security-review.skill.md"
codebook_id: "CB-SKILL-SECREVIEW-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for security code reviews"
skill_metadata:
  category: "security"
  complexity: "advanced"
  estimated_time: "15-60 min per PR"
  prerequisites:
    - "Security knowledge"
    - "Code access"
category: "skills"
status: "active"
tags:
  - "skill"
  - "security"
  - "review"
ai_parser_instructions: |
  This skill defines procedures for security reviews.
  Section markers: === SECTION ===
---

# Security Review Skill

=== PURPOSE ===

This skill provides procedures for conducting security code reviews. Security Lead has BLOCKING authority for security issues.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(security-lead) @ref(CB-AGENT-SECURITY-001) | Primary skill for security reviews |

---

=== PROCEDURE: Security Review Checklist ===

**Template:** @ref(CB-TPL-SECREVIEW-001)

### Authentication
- [ ] Authentication required for protected routes
- [ ] Session management is secure
- [ ] Password policies enforced
- [ ] MFA implemented where required

### Authorization
- [ ] Authorization checks on all endpoints
- [ ] Role-based access control implemented
- [ ] Principle of least privilege followed
- [ ] No privilege escalation possible

### Input Validation
- [ ] All inputs validated and sanitized
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding)
- [ ] Command injection prevented
- [ ] Path traversal prevented

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit
- [ ] PII handled appropriately
- [ ] No secrets in code or logs

### Error Handling
- [ ] Errors don't expose sensitive info
- [ ] Stack traces not exposed to users
- [ ] Errors logged appropriately

### Dependencies
- [ ] No known vulnerable dependencies
- [ ] Dependencies from trusted sources
- [ ] Dependency versions pinned

---

=== PROCEDURE: OWASP Top 10 Check ===

Review against OWASP Top 10:

1. **Broken Access Control**
2. **Cryptographic Failures**
3. **Injection**
4. **Insecure Design**
5. **Security Misconfiguration**
6. **Vulnerable Components**
7. **Authentication Failures**
8. **Data Integrity Failures**
9. **Logging Failures**
10. **SSRF**

---

=== PROCEDURE: Security Finding Documentation ===

**Format:**
```markdown
### [SEVERITY] Finding Title

**Location:** file.js:line
**Type:** [Injection/XSS/Auth/etc.]
**Severity:** [Critical/High/Medium/Low]

**Description:**
What the vulnerability is.

**Impact:**
What could happen if exploited.

**Recommendation:**
How to fix it.

**References:**
- [CWE-XXX](link)
```

---

=== SEVERITY DEFINITIONS ===

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Immediate exploitation risk | Block, fix immediately |
| High | Significant security risk | Block, fix before merge |
| Medium | Moderate risk | Block, create issue |
| Low | Minor issue | Advisory, create issue |

---

=== ANTI-PATTERNS ===

### Rubber Stamp Reviews
**Problem:** Approving without thorough review
**Solution:** Follow checklist, document findings

### Missing Context
**Problem:** Reviewing code without understanding flow
**Solution:** Understand authentication/authorization context

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(vulnerability-assessment) | Broader vulnerability context |
| @skill(compliance-check) | Compliance implications |
