---
name: code-quality-auditor
description: Proactively audits developer work to ensure completeness and production-readiness. This skill should be used when reviewing code changes, validating task completion, or verifying that work meets industry standards—catching incomplete implementations, deferred features, hardcoded values, missing tests, and shortcuts before code goes to production.
---

# Code Quality Auditor

## Overview

The Code Quality Auditor is a proactive quality assurance tool that validates developer work against a comprehensive checklist. Rather than just checking if code runs, it ensures:

- All tasks from the list are actually implemented (not deferred with TODOs)
- Tests exist and pass for new functionality
- No hardcoded values, shortcuts, or stub implementations remain
- Code follows industry standards and best practices
- Work is production-ready, not "cheated"

## When to Use This Skill

Trigger this skill when:
- A developer finishes implementing features and wants validation
- Before committing or creating a pull request
- When code review needs to verify completeness
- To ensure nothing was deferred with TODO comments
- To catch technical shortcuts or incomplete implementations

## Core Audit Workflow

### Step 1: Identify the Scope
Define what's being audited:
- **Code changes**: Which files were modified/created?
- **Task list**: What were the original requirements (GitHub Issues, task list, requirements)?
- **Test coverage**: What tests should exist?

Ask the developer or extract from:
- Git diff/PR changes
- Associated issues/tickets
- Commit messages
- Code review context

### Step 2: Scan for Red Flags
Use automated scanning to detect:
- TODO/FIXME/HACK/XXX comments (deferred work indicator)
- Hardcoded values (magic numbers, URLs, API keys, credentials)
- Stub/mock implementations left in production code
- Disabled or skipped tests without justification
- Empty implementations, console.log debugging, empty catch blocks
- Comments indicating "future work," "placeholder," "temporary," "will fix later"

Load [incomplete-work-patterns.md](references/incomplete-work-patterns.md) for complete detection patterns.

### Step 3: Verify Task Completion
Cross-reference implementation against original task list:
- Is every listed requirement actually implemented?
- Does code match the acceptance criteria?
- Are edge cases and error scenarios handled?
- Is the implementation real or just stubbed?

### Step 4: Check Test Coverage
Verify testing is adequate:
- New functionality has tests
- Tests are not skipped/disabled
- Tests pass (run test suite)
- Critical paths have integration tests
- Error scenarios are tested

Load [testing-requirements.md](references/testing-requirements.md) for testing standards.

### Step 5: Evaluate Code Quality
Assess implementation quality:
- Does code follow best practices and avoid anti-patterns?
- Is error handling proper (no silent failures)?
- Are there security issues (hardcoded secrets, unsafe input validation)?
- Is documentation clear where needed?
- Does code meet performance requirements?

Load [code-smells.md](references/code-smells.md) and [industry-standards.md](references/industry-standards.md) for evaluation criteria.

### Step 6: Generate Audit Results
Produce a concise, actionable checklist:
- Categorize issues by severity (Critical/Major/Minor)
- Provide specific code locations
- Include remediation guidance
- Keep output focused and brief (not overwhelming)

## Severity Levels

**Critical** 🔴
- Missing core functionality from requirements
- Tests failing or missing entirely
- Hardcoded credentials or security vulnerabilities
- Code cannot run in production
- Deferred work via TODO comments

**Major** 🟠
- Edge cases not handled
- Incomplete error handling
- Hardcoded configuration values that should be configurable
- Missing documentation for complex logic
- Anti-patterns in implementation

**Minor** 🟡
- Code style issues
- Missing comments in non-critical areas
- Potential optimizations
- Warning-level test coverage gaps

## Output Format

Keep audit results concise and actionable:

```
Code Quality Audit Results
===========================

⚠️  CRITICAL (2 issues)
- [ ] Line 45: Hardcoded API URL - move to config
- [ ] Missing user login tests - add coverage

🟠 MAJOR (1 issue)
- [ ] Line 123: Empty catch block - add error logging

✅ MINOR (0 issues)

Overall: 🟡 Work requires remediation before merge
```

## Audit Execution Tips

1. **Be thorough but concise**: Find all issues, present them briefly
2. **Provide specifics**: "Line X in file Y" not vague descriptions
3. **Include context**: Show problematic code snippet
4. **Give guidance**: What to fix, not just what's wrong
5. **Check both code and tests**: Many issues hide in test files
6. **Verify against original requirements**: Ensure nothing was omitted
7. **Run actual tests**: Don't just look for test files—verify they pass

## Reference Materials

Use these guides during the audit:

- [code-smells.md](references/code-smells.md) - Common implementation mistakes and anti-patterns
- [incomplete-work-patterns.md](references/incomplete-work-patterns.md) - Patterns indicating deferred/incomplete work
- [testing-requirements.md](references/testing-requirements.md) - What adequate testing looks like
- [industry-standards.md](references/industry-standards.md) - Production-readiness standards
