---
name: ac-qa-reviewer
description: Quality assurance review for implementations. Use when reviewing code quality, checking implementation standards, performing QA cycles, or validating feature quality.
---

# AC QA Reviewer

Perform quality assurance reviews on feature implementations.

## Purpose

Reviews completed features for code quality, adherence to standards, security issues, and best practices before marking features as complete.

## Quick Start

```python
from scripts.qa_reviewer import QAReviewer

reviewer = QAReviewer(project_dir)
result = await reviewer.review_feature("auth-001")
```

## Review Dimensions

### Code Quality
- Clean code principles
- DRY (Don't Repeat Yourself)
- SOLID principles
- Code complexity metrics

### Security
- Input validation
- SQL injection prevention
- XSS prevention
- Secure authentication

### Performance
- Algorithm efficiency
- Database query optimization
- Memory usage
- Caching opportunities

### Testing
- Test coverage
- Test quality
- Edge case coverage
- Integration tests

### Documentation
- Code comments
- API documentation
- README updates
- Type annotations

## Review Result

```json
{
  "feature_id": "auth-001",
  "approved": true,
  "score": 85,
  "dimensions": {
    "code_quality": {"score": 90, "issues": []},
    "security": {"score": 85, "issues": ["Consider rate limiting"]},
    "performance": {"score": 80, "issues": []},
    "testing": {"score": 88, "issues": []},
    "documentation": {"score": 82, "issues": ["Add docstring to validate_token"]}
  },
  "blocking_issues": [],
  "suggestions": [
    "Consider extracting authentication middleware",
    "Add rate limiting for login endpoint"
  ],
  "auto_fixable": ["missing_docstring"]
}
```

## QA Workflow

```
1. SCAN    → Static analysis of changed files
2. ANALYZE → Check against quality rules
3. SECURITY → Security-specific checks
4. REVIEW  → Contextual code review
5. REPORT  → Generate review report
6. FIX     → Auto-fix simple issues (optional)
7. APPROVE → Mark as QA passed or request changes
```

## Quality Gates

```yaml
gates:
  minimum_score: 70
  blocking_categories:
    - security_critical
    - test_failures
  required_checks:
    - linting_passes
    - type_checks_pass
    - tests_pass
    - coverage_minimum
```

## Auto-Fix Capabilities

The reviewer can automatically fix:
- Missing type hints
- Formatting issues
- Simple code style violations
- Missing docstrings (basic)

## Integration

- Input: Completed features from `ac-task-executor`
- Uses: `ac-code-validator` for static analysis
- Reports to: `ac-state-tracker`

## API Reference

See `scripts/qa_reviewer.py` for full implementation.
