---
name: test-plan-generator
description: Automatically generate comprehensive QA test plans when user mentions testing requirements, QA needs, or asks what should be tested. Analyzes code changes and features to create structured test scenarios. Invoke when user mentions "test plan", "QA", "what to test", "testing requirements", or "test scenarios".
---

# Test Plan Generator

Automatically generate comprehensive QA test plans based on features and changes.

## Philosophy

Comprehensive test planning prevents bugs and ensures quality before release.

### Core Beliefs

1. **Plan Before Execute**: Structured test plans catch more issues than ad-hoc testing
2. **Cover All Scenarios**: Think through happy paths, edge cases, and error conditions
3. **Prioritize by Risk**: Test critical functionality first, nice-to-haves later
4. **Documentation Enables Consistency**: Written test plans ensure repeatable quality checks

### Why Test Plans Matter

- **Complete Coverage**: Systematic approach ensures nothing is missed
- **Team Alignment**: Everyone knows what needs testing
- **Risk Mitigation**: Critical paths get appropriate attention
- **Regression Prevention**: Document scenarios to test after every change

## When to Use This Skill

Activate this skill when the user:
- Asks "what should QA test?"
- Says "I need a test plan"
- Mentions "testing requirements" or "test scenarios"
- Shows a new feature and asks "how should this be tested?"
- Asks "what test cases do I need?"
- References QA, testing coverage, or manual testing

## Decision Framework

Before creating a test plan, consider:

### What's Being Tested?

1. **New feature** → Focus on functional + acceptance testing
2. **Bug fix** → Focus on regression + edge cases
3. **Refactoring** → Focus on regression + integration testing
4. **Configuration change** → Focus on deployment + smoke testing
5. **Security update** → Focus on security + regression testing

### What's the Risk Level?

- **High** - Payment processing, authentication, data deletion → Comprehensive testing
- **Medium** - New feature, UI changes → Standard testing
- **Low** - Documentation, minor UI tweaks → Quick smoke test

### What Testing Levels Are Needed?

**Always include**:
- ✅ Functional testing (does it work?)
- ✅ Acceptance criteria validation

**Consider adding**:
- Security testing (user input, auth, permissions)
- Performance testing (large datasets, concurrent users)
- Accessibility testing (keyboard nav, screen readers)
- Browser/device testing (responsive, cross-browser)
- Integration testing (API calls, third-party services)

### What's the Platform?

**Drupal-specific tests**:
- Config imports/exports
- Update hooks
- Permissions and roles
- Cache clearing
- Cron jobs

**WordPress-specific tests**:
- Permalink changes
- ACF field sync
- Custom post types
- Shortcodes
- Widget areas

### Decision Tree

```
User requests test plan
    ↓
Analyze changes (git diff, feature description)
    ↓
Assess risk level (High/Medium/Low)
    ↓
Identify test types needed
    ↓
Generate scenarios by priority
    ↓
Add platform-specific tests
    ↓
Present structured test plan
```

## Quick Reference

See `/test-plan` command documentation for detailed test plan structure and examples.

This skill provides the same comprehensive test plan generation but is automatically invoked during conversation when the user expresses a need for test planning.

## Integration with /test-plan Command

- **This Skill**: Auto-invoked conversationally
  - "What should I test for this feature?"
  - "Need test scenarios"

- **`/test-plan` Command**: Explicit comprehensive generation
  - Full project test plan generation
  - Git history analysis
  - Structured documentation output
