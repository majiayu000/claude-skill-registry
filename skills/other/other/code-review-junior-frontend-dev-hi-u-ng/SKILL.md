---
name: code-review
description: Review code for quality, security, performance, and maintainability.
  Auto-activate after code modifications.
---

# Code Review Skill

## Purpose
Ensure consistent, thorough code reviews.

## Review Checklists

### Security Checklist
Reference: [checklists/security.md](checklists/security.md)
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output encoding used
- [ ] Authentication verified
- [ ] Authorization checked

### Performance Checklist
Reference: [checklists/performance.md](checklists/performance.md)
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Efficient algorithms
- [ ] Resource cleanup
- [ ] Pagination implemented

### Maintainability Checklist
Reference: [checklists/maintainability.md](checklists/maintainability.md)
- [ ] Code is readable
- [ ] Functions are focused
- [ ] Types are complete
- [ ] Tests exist
- [ ] Documentation present

### Accessibility Checklist (Frontend)
Reference: [checklists/accessibility.md](checklists/accessibility.md)
- [ ] Semantic HTML
- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Color contrast
- [ ] Focus management

## Issue Severity Guidelines

### Critical
- Security vulnerabilities
- Data loss potential
- Production breaking
- Compliance violations

### Warning
- Performance issues
- Missing error handling
- Incomplete types
- Missing tests

### Suggestion
- Naming improvements
- Refactoring opportunities
- Documentation gaps
- Style consistency

## Report Template
Use: [templates/review-report.md](templates/review-report.md)

## Review Process

### 1. Gather Context
- Understand the purpose of the changes
- Review related tickets/requirements
- Check the scope of modifications

### 2. Review Code
- Apply relevant checklists
- Check against project patterns
- Verify business logic

### 3. Categorize Findings
- Assign severity levels
- Group by type
- Prioritize fixes

### 4. Generate Report
- Use report template
- Include actionable recommendations
- Reference specific lines/files

## Best Practices

### Do
- Be specific about issues
- Provide fix suggestions
- Acknowledge good practices
- Focus on code, not author
- Ask questions when unclear

### Don't
- Be vague or unhelpful
- Request unnecessary changes
- Block for style preferences
- Make it personal
- Skip security checks

## Storage Location
Save reports to: `docs/reviews/code-review-{session}.md`
