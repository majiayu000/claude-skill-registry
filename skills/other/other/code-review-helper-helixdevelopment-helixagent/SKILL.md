---
name: code-review-helper
description: Systematic code review workflows with bundled utilities for analyzing code quality, detecting patterns, and providing structured feedback. Use this skill when reviewing pull requests or conducting code audits.
---

# Code Review Helper Skill

Systematic code review workflows with utilities for thorough, consistent reviews.

## Overview

This skill provides structured workflows and utilities for conducting high-quality code reviews. It emphasizes:
- Systematic analysis across multiple dimensions
- Automated pattern detection
- Structured feedback format
- Constructive, actionable suggestions

## Review Process

### 1. Initial Context Gathering

Before reviewing, understand the change:

```shell
# View PR metadata
gh pr view <pr-number> --repo <owner/repo>

# Check file changes
gh pr diff <pr-number> --repo <owner/repo>

# Review CI status
gh pr checks <pr-number> --repo <owner/repo>
```

### 2. Systematic Analysis

Review across these dimensions:

**Correctness**
- Does the code do what it claims?
- Are edge cases handled?
- Are error conditions addressed?

**Clarity**
- Is the code easy to understand?
- Are names descriptive?
- Is complexity justified?

**Testing**
- Are there adequate tests?
- Do tests cover edge cases?
- Are tests clear and maintainable?

**Documentation**
- Is public API documented?
- Are complex algorithms explained?
- Are assumptions stated?

**Performance**
- Are there obvious inefficiencies?
- Are large operations appropriate?
- Is caching used where beneficial?

**Security**
- Are inputs validated?
- Are sensitive data handled properly?
- Are dependencies trustworthy?

### 3. Pattern Detection

Use bundled utilities to detect common issues:

```python
# Import review helpers
from review_helpers import (
    check_naming_conventions,
    detect_code_smells,
    analyze_complexity,
    find_duplicate_code,
    check_test_coverage
)

# Analyze code
naming_issues = check_naming_conventions("path/to/file.py")
smells = detect_code_smells("path/to/file.py")
complexity = analyze_complexity("path/to/file.py")
duplicates = find_duplicate_code("src/")
coverage = check_test_coverage("tests/", "src/")

# Report findings
for issue in naming_issues + smells:
    print(f"⚠️ {issue}")
```

### 4. Structured Feedback Format

Provide feedback in this format:

```markdown
## Summary
[Brief overview of the PR and general assessment]

## Strengths
- [Positive aspect 1]
- [Positive aspect 2]

## Issues Found

### Critical
- [ ] **[File:Line]**: [Description]
  - Why: [Explanation]
  - Fix: [Suggestion]

### Important
- [ ] **[File:Line]**: [Description]
  - Why: [Explanation]
  - Fix: [Suggestion]

### Minor
- [ ] **[File:Line]**: [Description]
  - Why: [Explanation]
  - Fix: [Suggestion]

## Suggestions
- [Non-blocking improvement 1]
- [Non-blocking improvement 2]

## Questions
- [Clarification needed 1]
- [Clarification needed 2]

## Overall Assessment
[Approve / Request Changes / Comment]
```

## Bundled Utilities

### review_helpers.py

Provides automated analysis functions:

**check_naming_conventions(filepath)**
- Validates Python naming conventions
- Checks for PEP 8 compliance
- Returns list of naming issues

**detect_code_smells(filepath)**
- Identifies common anti-patterns
- Detects magic numbers
- Finds long functions/classes
- Reports deeply nested code

**analyze_complexity(filepath)**
- Calculates cyclomatic complexity
- Identifies complex functions
- Suggests refactoring candidates

**find_duplicate_code(directory)**
- Detects code duplication
- Uses AST-based analysis
- Reports similar code blocks

**check_test_coverage(test_dir, source_dir)**
- Analyzes test-to-code ratio
- Identifies untested code paths
- Suggests missing test cases

## Common Review Patterns

### Pattern: Security-Sensitive Code

When reviewing authentication, authorization, or data handling:

```markdown
**Security Checklist**:
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS prevention (if web)
- [ ] Secrets not hardcoded
- [ ] Sensitive data encrypted
- [ ] Access control enforced
- [ ] Audit logging included
```

### Pattern: Performance-Critical Code

When reviewing loops, database queries, or large data operations:

```markdown
**Performance Checklist**:
- [ ] N+1 queries avoided
- [ ] Appropriate indexes used
- [ ] Caching considered
- [ ] Bulk operations used where possible
- [ ] Memory usage reasonable
- [ ] Algorithmic complexity acceptable
```

### Pattern: API Changes

When reviewing public API modifications:

```markdown
**API Checklist**:
- [ ] Backward compatibility maintained or migration path provided
- [ ] Documentation updated
- [ ] Examples provided
- [ ] Error handling clear
- [ ] Type hints complete
- [ ] Deprecation warnings added if needed
```

## Best Practices

### Be Constructive

Focus on improvement, not criticism:

```markdown
# Unhelpful
This code is terrible.

# Helpful
This function is hard to test due to tight coupling. Consider using dependency injection to improve testability.
```

### Provide Context

Explain why something matters:

```markdown
# Incomplete
This variable name is bad.

# Complete
The variable name 'x' is unclear. Consider 'customer_count' which better expresses the domain concept and improves readability.
```

### Suggest Alternatives

When requesting changes, show how:

```markdown
# Vague
This needs to be refactored.

# Specific
Consider extracting this logic into a separate function for better testability and reuse.
```

### Prioritize Issues

Distinguish between blocking and non-blocking feedback:

```markdown
**Blocking**: Security vulnerability in password handling (line 42)
**Important**: Missing input validation (line 67)
**Nice-to-have**: Consider extracting helper function (line 123)
**Question**: Why use X instead of Y here? (line 89)
```

## Integration with Other Tools

### With Shell Tool

```shell
# Check for common issues
rg "TODO|FIXME|XXX" --type py src/
grep -r "import \*" src/
find src/ -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

### With Patch Tool

```patch file.py
<<<<<<< ORIGINAL
def process_data(data):
    result = []
    for item in data:
        result.append(transform(item))
    return result
=======
def process_data(data):
    """Process data items with transformation.

    Args:
        data: Iterable of items to process

    Returns:
        List of transformed items
    """
    return [transform(item) for item in data]
>>>>>>> UPDATED
```

### With ast-grep

```shell
# Find patterns
sg --pattern 'except: $$$' --lang python src/
sg --pattern 'print($MSG)' --lang python src/
sg --pattern 'def $FUNC($ARGS): pass' --lang python src/
```

## Workflow Example

Complete review workflow:

```python
#!/usr/bin/env python3
"""Automated code review workflow."""

from review_helpers import (
    check_naming_conventions,
    detect_code_smells,
    analyze_complexity,
    find_duplicate_code
)

def review_pr(pr_number: int, repo: str):
    """Conduct automated review of PR."""

    # Get changed files
    files = get_pr_files(pr_number, repo)

    # Analyze each file
    all_issues = []
    for filepath in files:
        if filepath.endswith('.py'):
            issues = []
            issues.extend(check_naming_conventions(filepath))
            issues.extend(detect_code_smells(filepath))

            complexity = analyze_complexity(filepath)
            if complexity > 10:
                issues.append(f"High complexity: {complexity}")

            all_issues.extend([(filepath, issue) for issue in issues])

    # Check for duplicates across files
    duplicates = find_duplicate_code("src/")

    # Generate review comment
    comment = format_review_comment(all_issues, duplicates)

    # Post review
    post_pr_review(pr_number, repo, comment)

if __name__ == "__main__":
    review_pr(123, "owner/repo")
```

## Tips for Reviewers

1. **Review small chunks**: Don't try to review 1000+ line PRs in one sitting
2. **Test the code**: Pull the branch and run it locally when possible
3. **Consider context**: Understand the business requirements and constraints
4. **Be timely**: Review promptly to unblock authors
5. **Distinguish preferences from problems**: Not all feedback is blocking
6. **Learn from reviews**: Use reviews as learning opportunities

## Tips for Authors

1. **Keep PRs small**: Aim for <300 lines when possible
2. **Write descriptive PR descriptions**: Explain what, why, and how
3. **Self-review first**: Review your own diff before requesting review
4. **Respond to feedback**: Address comments or explain why not
5. **Ask questions**: Clarify unclear feedback

## Related

- [GitHub PR Workflow](https://github.com/ErikBjare/gptme/blob/master/docs/lessons/workflows/git.md) - Git practices
- [gptme patch tool](https://gptme.org/docs/tools.html#patch) - Code modification
