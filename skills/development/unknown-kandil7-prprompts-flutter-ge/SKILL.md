# QA Auditor Automation Skill

## Skill Overview

You are an expert QA auditor specializing in comprehensive Flutter application audits for production readiness, compliance certification, and enterprise deployment. This skill performs deep audits covering architecture, security, compliance, testing, performance, and code quality.

**What This Skill Does:**
- Comprehensive audit across 6 categories (architecture, security, compliance, testing, performance, code quality)
- Validates compliance with HIPAA, PCI-DSS, GDPR, SOC2, COPPA, FERPA
- Generates certification-ready audit reports
- Identifies production blockers and critical issues
- Provides actionable remediation steps
- Issues pass/fail certification based on threshold

**Execution Time:** 10-20 minutes

---

## Step 1: Architecture Audit

### 1.1 Clean Architecture Validation

**Check:**
- ✅ Proper layer separation (domain/data/presentation)
- ✅ Dependency flow (presentation → domain ← data)
- ✅ No circular dependencies
- ✅ Repository pattern correctly implemented
- ✅ Use case single responsibility

**Score: /25 points**

---

## Step 2: Security Audit

### 2.1 Authentication Security
- JWT verification (not signing)
- Password security (no storage)
- Session management
- MFA implementation (if applicable)

### 2.2 Data Protection
- Encryption at rest (FlutterSecureStorage)
- HTTPS enforcement
- API key protection
- Sensitive data handling

### 2.3 Compliance-Specific Checks

**HIPAA:**
- PHI encryption (AES-256-GCM)
- Audit logging
- Session timeout (15 min)
- No PHI in logs

**PCI-DSS:**
- No card storage
- Tokenization
- Only last 4 digits displayed
- SAQ validation

**GDPR:**
- Data export capability
- Right to deletion
- Consent management
- Privacy policy

**Score: /25 points**

---

## Step 3: Testing Audit

### 3.1 Coverage Analysis
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

**Requirements:**
- Domain: 90%+
- Data: 80%+
- Presentation: 60%+
- Overall: 70%+

### 3.2 Test Quality
- Unit tests: Complete with mocks
- Widget tests: User interactions
- Integration tests: Complete flows
- No empty tests
- All assertions present

**Score: /20 points**

---

## Step 4: Compliance Audit

**Per Standard (HIPAA, PCI-DSS, GDPR, etc.):**

✅ Required controls implemented
✅ Documentation complete
✅ Audit trail enabled
✅ Security measures in place
✅ User consent obtained
✅ Data minimization applied

**Score: /15 points**

---

## Step 5: Performance Audit

### 5.1 App Performance
- Launch time < 2 seconds
- Screen transitions < 300ms
- API calls timeout properly
- Memory leaks checked
- Frame rate 60fps

### 5.2 Network Performance
- Caching implemented
- Offline mode (if required)
- Retry logic
- Error handling

**Score: /10 points**

---

## Step 6: Code Quality Audit

### 6.1 Static Analysis
```bash
flutter analyze
```

**Requirements:**
- Zero errors
- Zero warnings
- Minimal info messages

### 6.2 Code Standards
- Naming conventions
- Documentation
- TODOs addressed
- Dead code removed

**Score: /5 points**

---

## Step 7: Generate Audit Report

### 7.1 Calculate Overall Score

```
Overall Score =
  Architecture (25%) +
  Security (25%) +
  Testing (20%) +
  Compliance (15%) +
  Performance (10%) +
  Code Quality (5%)

Pass/Fail:
- Pass: Score >= fail_threshold
- Fail: Score < fail_threshold OR critical_issues > 0
```

### 7.2 Create Audit Report

```markdown
# QA Audit Report

**Date:** {{date}}
**Audit Type:** {{audit_type}}
**Auditor:** QA Auditor Skill v1.0.0

---

## Overall Result: {{PASS|FAIL}}

**Overall Score:** {{score}}/100

**Threshold:** {{fail_threshold}}
**Status:** {{score >= fail_threshold ? "✅ PASS" : "❌ FAIL"}}

---

## Scores by Category

| Category | Score | Weight | Status |
|----------|-------|--------|--------|
| Architecture | {{arch_score}}/25 | 25% | {{status}} |
| Security | {{sec_score}}/25 | 25% | {{status}} |
| Testing | {{test_score}}/20 | 20% | {{status}} |
| Compliance | {{comp_score}}/15 | 15% | {{status}} |
| Performance | {{perf_score}}/10 | 10% | {{status}} |
| Code Quality | {{qual_score}}/5 | 5% | {{status}} |

---

## Critical Issues: {{critical_count}}

{{#if critical_issues}}
❌ **PRODUCTION BLOCKER:** Critical issues must be fixed before deployment.

{{#each critical_issues}}
### {{@index}}. {{this.title}}
- **Category:** {{this.category}}
- **Severity:** 🔴 CRITICAL
- **Impact:** {{this.impact}}
- **File:** {{this.file}}:{{this.line}}
- **Issue:** {{this.description}}
- **Fix:** {{this.remediation}}
- **Compliance Impact:** {{this.compliance_impact}}
{{/each}}
{{else}}
✅ No critical issues found.
{{/if}}

---

## Compliance Summary

{{#each compliance_standards}}
### {{this.name}} Compliance

**Overall:** {{this.score}}/100 ({{this.status}})

**Requirements Met:** {{this.requirements_met}}/{{this.total_requirements}}

**Controls:**
{{#each this.controls}}
- {{this.passed ? "✅" : "❌"}} {{this.name}}: {{this.description}}
{{/each}}

{{#if this.violations}}
**Violations:**
{{#each this.violations}}
- {{this.severity}} {{this.description}} ({{this.control_id}})
  - Remediation: {{this.remediation}}
{{/each}}
{{/if}}
{{/each}}

---

## Detailed Findings

### Architecture ({{arch_score}}/25)

✅ **Strengths:**
- Clean Architecture structure properly implemented
- Layer separation maintained
- Repository pattern used correctly

⚠️ **Issues:**
{{#each arch_issues}}
- {{this.description}} ({{this.severity}})
{{/each}}

### Security ({{sec_score}}/25)

{{#if sec_score >= 20}}
✅ **Excellent security posture**
{{else if sec_score >= 15}}
⚠️ **Acceptable with improvements needed**
{{else}}
❌ **Security issues require immediate attention**
{{/if}}

**Findings:**
{{#each sec_findings}}
- {{this.description}} ({{this.severity}})
{{/each}}

### Testing ({{test_score}}/20)

**Coverage:** {{coverage}}%
**Tests:** {{test_count}} total

{{#if test_score >= 16}}
✅ **Well-tested application**
{{else}}
⚠️ **Test coverage below recommended levels**
{{/if}}

**Missing Tests:**
{{#each missing_tests}}
- {{this.file}} ({{this.current_coverage}}% coverage)
{{/each}}

---

## Recommendations

### Immediate Actions (Before Production)

{{#each immediate_actions}}
{{@index}}. **{{this.title}}**
   - Priority: {{this.priority}}
   - Effort: {{this.effort}}
   - Fix: {{this.fix}}
{{/each}}

### Short-term Improvements

{{#each short_term_improvements}}
{{@index}}. {{this.description}}
{{/each}}

### Long-term Enhancements

{{#each long_term_enhancements}}
{{@index}}. {{this.description}}
{{/each}}

---

## Certification

{{#if audit_passed}}
✅ **PASSED QA AUDIT**

This application has passed the QA audit with a score of {{score}}/100.

**Certification Details:**
- Audit Date: {{date}}
- Audit Type: {{audit_type}}
- Compliance Standards: {{compliance_standards}}
- Valid Until: {{expiration_date}} (90 days)

**Certificate Generated:** {{certificate_path}}

**Auditor Signature:**
QA Auditor Skill v1.0.0
🤖 Generated with Claude Code

{{else}}
❌ **FAILED QA AUDIT**

This application did not pass the QA audit.

**Reasons for Failure:**
{{#each failure_reasons}}
- {{this}}
{{/each}}

**Required Actions:**
1. Fix all critical issues
2. Address compliance violations
3. Re-run audit after fixes

**To Re-Audit:**
```bash
@claude use skill automation/qa-auditor
```
{{/if}}

---

**Report Generated:** {{timestamp}}
**Report Path:** {{report_path}}

🤖 Generated with Claude Code
```

---

## Skill Completion

```markdown
✅ QA Audit Complete!

**Result:** {{PASS|FAIL}}
**Score:** {{score}}/100
**Critical Issues:** {{critical_count}}
**Report:** {{report_path}}

{{#if audit_passed}}
🎉 Application is production-ready!
{{else}}
⚠️  Fix issues and re-audit before production deployment.
{{/if}}
```

---

**End of Skill Execution**
